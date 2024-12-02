import requests

def extrair_nomes_m3u(arquivo_m3u):
    with open(arquivo_m3u, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    nomes = []
    for linha in linhas:
        if linha.startswith('#EXTINF:'):
            info = linha.split(',')
            nome = info[-1].strip()
            nomes.append(nome)
    return nomes

def obter_id_tmdb(nome, api_key):
    url = f"https://api.themoviedb.org/3/search/multi?api_key={api_key}&query={nome}"
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        if 'results' in dados and dados['results']:
            print(f"ID encontrado para {nome}: {dados['results'][0]['id']}")
            return dados['results'][0]['id']
        else:
            print(f"No results found for {nome}")
            return None
    else:
        print(f"Error fetching data for {nome}, status code: {response.status_code}")
        return None

def armazenar_em_txt(dados, arquivo_txt):
    print(f"Armazenando dados em {arquivo_txt}")
    with open(arquivo_txt, 'w', encoding='utf-8') as f:
        for nome, id_tmdb in dados.items():
            if id_tmdb is not None:
                f.write(f"{nome}: {id_tmdb}\n")
    print("Armazenamento concluído")

def main():
    api_key = 'SUA_API_KEY_DO_TMDB'
    nomes_filmes_series = extrair_nomes_m3u('lista.m3u')
    ids_filmes_series = {}

    for nome in nomes_filmes_series:
        id_tmdb = obter_id_tmdb(nome, api_key)
        ids_filmes_series[nome] = id_tmdb

    print("IDs obtidos:", ids_filmes_series)
    armazenar_em_txt(ids_filmes_series, 'resultados.txt')
    print("Dados armazenados em resultados.txt")

if __name__ == '__main__':
    main()
