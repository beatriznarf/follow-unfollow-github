import requests

usuario = "beatriznarf"
token = ""

headers = {}
if token:
    headers["Authorization"] = f"token {token}"

def get_lista(url):
    lista = []
    page = 1
    while True:
        resp = requests.get(f"{url}?per_page=100&page={page}", headers=headers)
        if resp.status_code != 200:
            print("Erro:", resp.json())
            break
        dados = resp.json()
        if not dados:
            break
        lista.extend([user["login"] for user in dados])
        page += 1
    return set(lista)

# Seguidores e usuarios que estou seguindo
seguidores = get_lista(f"https://api.github.com/users/{usuario}/followers")
seguidos   = get_lista(f"https://api.github.com/users/{usuario}/following")

# Usuarios que nao estao seguindo de volta
nao_seguem_de_volta = sorted(seguidos - seguidores)

# Usuarios que me segue mas eu não sigo
eu_nao_sigo = sorted(seguidores - seguidos)


print(f"\n{'🚫 Não me seguem de volta':<50} {'↔️ Eu ainda não sigo':<50}")
print("-" * 100)

for i in range(max(len(nao_seguem_de_volta), len(eu_nao_sigo))):
    col1 = f"{nao_seguem_de_volta[i]} -> https://github.com/{nao_seguem_de_volta[i]}" if i < len(nao_seguem_de_volta) else ""
    col2 = f"{eu_nao_sigo[i]} -> https://github.com/{eu_nao_sigo[i]}" if i < len(eu_nao_sigo) else ""
    print(f"{col1:<50} {col2:<50}")