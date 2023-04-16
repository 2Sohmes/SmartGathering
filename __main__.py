import requests
import re
from sys import stdout

def searchUrls(text):
    urls_list = []
    filtered_list = list(dict.fromkeys(re.findall(r'href=[\'"]?([^\'" >]+)', text)))
    for url in filtered_list:
        if (url.startswith("#") or url.startswith("/")) and len(url) > 1:
            urls_list.append(f"{domain[:len(domain) - 1]}{url}")
        elif domain in url:
            urls_list.append(url)

    return list(dict.fromkeys(urls_list))

def backline():
    print('\r', end='')

if __name__ == '__main__':
    domain = "http://" + str(input("Domain: ")) + "/"
    wordlist_path = str(input("Wordlist: "))
    user_agent = ""

    request = requests.options(domain, headers={'user-agent': user_agent})
    status_code = request.status_code
    try:
        date = request.headers['date']
    except:
        date = 'Nenhum'

    try:
        server = request.headers['server']
    except:
        server = 'Nenhum'

    try:
        allow = request.headers['allow']
    except:
        allow = 'Nenhum'

    print('''
  Informações iniciais:
    Status Code: {}
    Data do Servidor: {}
    Tecnologiais: {}
    Métodos Permitidos: {}
    '''.format(status_code, date, server, allow))

    request = requests.get(domain, headers={'user-agent': user_agent})
    urls = searchUrls(request.text)
    wordlist = []


    # Carregando wordlist diretorio
    print("Carregando wordlist...")
    wordlist_file = open(wordlist_path, 'r')
    for word in wordlist_file:
        word = word.replace('\n', '')
        url = f"{domain[:len(domain) - 1]}{word if word.startswith('/') else ('/' + word)}"
        if url not in wordlist:
            wordlist.append(url)
    wordlist_file.close()
    print(f'Wordlist carregada com {len(wordlist)} entradas!')
    print('\nIniciando processo de busca de diretórios...')
    print('Diretórios encontrados:\n')

    for url in urls:
        request = requests.get(url, headers={'user-agent': user_agent})
        status_code = request.status_code
        result = f'  => {url} - {status_code}'
        if 200 <= status_code <= 299:
            print(result)

    for url in wordlist:
        if url not in urls:
            request = requests.get(url, headers={'user-agent': user_agent})
            status_code = request.status_code
            if 200 <= status_code <= 299:
                result = f'  => {url} - {status_code}'
                print(result)
                if len(request.text) > 0:
                    searched_urls = searchUrls(request.text)
                    for searched_url in searched_urls:
                        if searched_url not in urls:
                            urls.append(searched_url)





