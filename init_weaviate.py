# init_weaviate.py
import weaviate

# Conectar ao Weaviate
client = weaviate.Client("http://localhost:8080")

# Definir o schema
schema = {
    "classes": [
        {
            "class": "Filme",
            "description": "Um filme com informações do TMDb",
            "properties": [
                {
                    "name": "title",
                    "dataType": ["string"],
                    "description": "Título do filme"
                },
                {
                    "name": "overview",
                    "dataType": ["string"],
                    "description": "Descrição do filme"
                },
                {
                    "name": "release_date",
                    "dataType": ["string"],
                    "description": "Data de lançamento"
                },
                {
                    "name": "vote_average",
                    "dataType": ["number"],
                    "description": "Nota média do filme"
                },
                {
                    "name": "poster_path",
                    "dataType": ["string"],
                    "description": "Caminho do poster do filme"
                }
            ]
        }
    ]
}

# Criar o schema no Weaviate
client.schema.create(schema)

print("Schema criado com sucesso!")