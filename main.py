from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from app.bot import gerar_resposta_llm
from app.config import TMDB_API_KEY
from app.tmdb import buscar_filme_tmdb, buscar_filmes_mesmo_genero

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/perguntar")
async def perguntar(request: QueryRequest):
    try:
        if not request.query:
            raise HTTPException(status_code=400, detail="Por favor, informe um nome de filme válido.")

        # Buscar filme no TMDb
        filme = buscar_filme_tmdb(request.query)
        if not filme or "title" not in filme:
            # Retornar filmes populares como sugestão
            url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=pt-BR"
            response = requests.get(url)
            if response.status_code == 200:
                filmes_populares = response.json().get("results", [])[:5]
                sugestoes = []
                for filme in filmes_populares:
                    if "title" in filme:
                        sugestoes.append({
                            "titulo": filme["title"],
                            "descricao": filme.get("overview", "Descrição não disponível."),
                            "poster": f"https://image.tmdb.org/t/p/w500{filme['poster_path']}" if filme.get("poster_path") else None
                        })
                return {
                    "resposta": "Desculpe, não encontrei esse filme. Aqui estão algumas sugestões de filmes populares:",
                    "sugestoes": sugestoes
                }
            else:
                return {"resposta": "Desculpe, não encontrei esse filme e não pude carregar sugestões."}

        # Buscar filmes do mesmo gênero
        genero_ids = filme.get("genero_ids", [])
        filmes_mesmo_genero = buscar_filmes_mesmo_genero(genero_ids)

        # Montar resposta
        resposta = {
            "resposta": f"🎬 O filme '{filme['title']}' foi encontrado!",
            "detalhes": {
                "titulo": filme["title"],
                "descricao": filme.get("overview", "Descrição não disponível."),
                "data_lancamento": filme.get("release_date", "Data não encontrada."),
                "nota_tmdb": filme.get("vote_average", "Nota não disponível."),
                "poster": f"https://image.tmdb.org/t/p/w500{filme['poster_path']}" if filme.get("poster_path") else None,
                "generos": filme.get("generos", [])
            },
            "filmes_mesmo_genero": filmes_mesmo_genero
        }

        return resposta

    except HTTPException as e:
        return {"erro": str(e.detail)}
    except Exception as e:
        return {"erro": f"Ocorreu um erro inesperado: {str(e)}"}