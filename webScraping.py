import requests
import json
from bs4 import BeautifulSoup


url_base = 'https://lista.mercadolivre.com.br/'
produto_nome = input('Qual produto deseja? ')

# Alterado para formatar o nome do produto na URL corretamente
produto_nome_formatado = produto_nome.strip().replace(' ', '-')
response = requests.get(url_base + produto_nome_formatado)

# Verifica se a requisição foi bem sucedida
if response.status_code == 200:
    site = BeautifulSoup(response.text, 'html.parser')

    # Verifica se há resultados para a pesquisa
    if site.find('div', attrs={'class': 'empty-search'}):
        print('Nenhum resultado encontrado para a pesquisa.')
    else:
        produtos = site.find_all('li', attrs={'class': 'ui-search-layout__item'})

        menor_valor = float('inf')
        maior_valor = float('-inf')
        infos = []

        for produto in produtos:

            titulo = produto.find('h2', attrs={'class': 'ui-search-item__title'})
            link = produto.find('a', attrs={'class': 'ui-search-link'})
            preco = produto.find('span', attrs={'class': 'price-tag-fraction'})

            if preco:
                valor = float(preco.text.replace('.', '').replace(',', '.'))
                infos.append({
                    "Titulo": titulo.text,
                    "Link": link['href'],
                    "Valor": valor
                })
                menor_valor = min(menor_valor, valor)
                maior_valor = max(maior_valor, valor)

                print("Titulo:", titulo.text)
                print("Link do produto:", link['href'])
                print(f'Valor: R$ {valor:.2f}')
                print("\n\n")

        # Salva as informações em um arquivo json
        with open('dados_mercado_livre.json', 'w', encoding='UTF-8') as arquivo:
            json.dump(infos, arquivo, ensure_ascii=False, indent=4)

        print("Produto com menor valor: R$ {:.2f}".format(menor_valor))
        print("Produto com maior valor: R$ {:.2f}".format(maior_valor))

else:
    print('Erro ao buscar página.')
