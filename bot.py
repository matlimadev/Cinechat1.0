from transformers import pipeline
from sentence_transformers import SentenceTransformer

def gerar_resposta_llm(detalhes_filme, similares, criticas):
    # Carregar o modelo de geração de texto
    generator = pipeline('text-generation', model='gpt2')

    # Contexto baseado no filme principal
    contexto = f"O filme {detalhes_filme['titulo']} foi lançado em {detalhes_filme['data_lancamento']}. {detalhes_filme['descricao']}. Ele tem uma nota média de {detalhes_filme['nota_tmdb']} no TMDb."

    # Adicionar filmes semelhantes ao contexto
    if similares:
        contexto += "\nFilmes semelhantes:\n" + "\n".join([f"- {f['titulo']}" for f in similares])

    # Adicionar críticas ao contexto
    if criticas:
        contexto += "\nCríticas:\n" + "\n".join([f"{c['autor']}: {c['conteudo']}" for c in criticas])

    # Gerar a resposta
    resposta = generator(contexto, max_length=500, num_return_sequences=1)
    return resposta[0]['generated_text']