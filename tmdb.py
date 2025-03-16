import requests
import weaviate
from weaviate.connect import ConnectionParams  # Importe a classe ConnectionParams
from .config import TMDB_API_KEY, TMDB_BASE_URL, WEAVIATE_URL
from sentence_transformers import SentenceTransformer

# Configurar a conexão com o Weaviate
connection_params = ConnectionParams.from_url(WEAVIATE_URL, grpc_port=50051)  # Adicionado grpc_port
client = weaviate.WeaviateClient(connection_params)  # Passe o objeto ConnectionParams

# Carregar o modelo de embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

def gerar_embedding(texto):
    return model.encode(texto).tolist()

def buscar_filme_tmdb(titulo):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": titulo, "language": "pt-BR"}

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            filme = data["results"][0]
            filme_id = filme["id"]
            
            # Buscar detalhes do filme para obter os gêneros
            detalhes_url = f"{TMDB_BASE_URL}/movie/{filme_id}"
            detalhes_response = requests.get(detalhes_url, params={"api_key": TMDB_API_KEY, "language": "pt-BR"})
            detalhes_filme = detalhes_response.json()
            
            # Buscar críticas
            criticas = buscar_criticas_tmdb(filme_id)
            
            # Buscar filmes relacionados
            relacionados = buscar_filmes_relacionados_tmdb(filme_id)
            
            filme_data = {
                "id": filme["id"],
                "title": filme.get("title", "Título não disponível"),
                "overview": filme.get("overview", "Descrição não disponível."),
                "release_date": filme.get("release_date", "Data não encontrada."),
                "vote_average": filme.get("vote_average", "Nota não disponível."),
                "poster_path": filme.get("poster_path"),
                "criticas": criticas,
                "relacionados": relacionados,
                "generos": [genero["name"] for genero in detalhes_filme.get("genres", [])],
                "genero_ids": [genero["id"] for genero in detalhes_filme.get("genres", [])]  # IDs dos gêneros
            }
            # Adicionar o filme ao Weaviate
            adicionar_filme_ao_weaviate(filme_data)
            return filme_data
    return None

def buscar_criticas_tmdb(filme_id):
    url = f"{TMDB_BASE_URL}/movie/{filme_id}/reviews"
    params = {"api_key": TMDB_API_KEY, "language": "pt-BR"}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        criticas = []
        for review in data.get("results", [])[:5]:  # Limitar a 5 críticas
            criticas.append({
                "autor": review.get("author", "Anônimo"),
                "conteudo": review.get("content", "Sem conteúdo disponível"),
                "nota": review.get("author_details", {}).get("rating", "Sem nota")
            })
        return criticas
    return []

def buscar_filmes_relacionados_tmdb(filme_id):
    url = f"{TMDB_BASE_URL}/movie/{filme_id}/recommendations"
    params = {"api_key": TMDB_API_KEY, "language": "pt-BR"}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        relacionados = []
        for filme in data.get("results", [])[:5]:  # Limitar a 5 filmes relacionados
            relacionados.append({
                "titulo": filme.get("title", "Título não disponível"),
                "descricao": filme.get("overview", "Descrição não disponível"),
                "poster_path": filme.get("poster_path"),
                "nota": filme.get("vote_average", "Sem nota")
            })
        return relacionados
    return []

def buscar_filmes_mesmo_genero(genero_ids, k=5):
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "pt-BR",
        "with_genres": ",".join(map(str, genero_ids)),  # Filtra por gêneros
        "sort_by": "popularity.desc",  # Ordena por popularidade
        "page": 1
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        filmes = []
        for filme in data.get("results", [])[:k]:  # Limita a k filmes
            filmes.append({
                "titulo": filme.get("title", "Título não disponível"),
                "descricao": filme.get("overview", "Descrição não disponível"),
                "poster_path": filme.get("poster_path"),
                "nota": filme.get("vote_average", "Sem nota")
            })
        return filmes
    return []

def adicionar_filme_ao_weaviate(filme):
    # Verificar se o Weaviate está acessível antes de tentar adicionar
    try:
        client.schema.get()  # Testa conexão com o Weaviate
    except Exception as e:
        print(f"Erro ao conectar ao Weaviate: {e}")
        return
    
    # Verificar se o filme já existe no Weaviate
    result = client.query.get(
        class_name="Filme",
        properties=["title"]
    ).with_where({
        "path": ["title"],
        "operator": "Equal",
        "valueString": filme["title"]
    }).do()

    if result and "data" in result and "Get" in result["data"] and "Filme" in result["data"]["Get"]:
        # Filme já existe, não adicionar novamente
        print(f"O filme '{filme['title']}' já está no Weaviate.")
        return

    # Gerar embedding para a descrição do filme
    embedding = gerar_embedding(filme["overview"])

    # Adicionar o filme ao Weaviate
    client.data.create(
        data_object={
            "title": filme["title"],
            "overview": filme["overview"],
            "release_date": filme["release_date"],
            "vote_average": filme["vote_average"],
            "poster_path": filme["poster_path"]
        },
        class_name="Filme",
        vector=embedding
    )
    print(f"Filme '{filme['title']}' adicionado ao Weaviate com sucesso.")
