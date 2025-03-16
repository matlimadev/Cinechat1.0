
1. Pré-requisitos
   - **Python 3.8 ou superior**: Certifique-se de que o Python está instalado na sua máquina.
   - **Pip**: O gerenciador de pacotes do Python deve estar instalado.
   - **Weaviate**: O Weaviate deve estar rodando localmente ou em um servidor acessível. Você pode rodar o Weaviate localmente usando Docker.

2. Configuração do Ambiente
   - Clone o repositório: Se você ainda não fez isso, clone o repositório do projeto para o seu ambiente local.
   - Crie um ambiente virtual (opcional, mas recomendado):
     bash
     python -m venv venv
     source venv/bin/activate  # No Windows use venv\Scripts\activate
     
Instale as dependências:
     bash
     pip install -r requirements.txt
    

3. Configuração do Weaviate
    Inicie o Weaviate:
     Se você estiver rodando o Weaviate localmente, você pode iniciá-lo usando Docker:
     bash
     docker run -d -p 8080:8080 --name weaviate semitechnologies/weaviate:latest
   
     Crie o schema no Weaviate:
     Execute o script `init_weaviate.py` para criar o schema necessário:
     bash
     python init_weaviate.py
  

### 4. **Configuração do TMDb**
   - **Obtenha uma chave de API do TMDb**:
     - Crie uma conta no [TMDb](https://www.themoviedb.org/) se ainda não tiver uma.
     - Gere uma chave de API na seção de configurações da sua conta.
   - **Configure a chave de API**:
     - Crie um arquivo `.env` na raiz do projeto e adicione a chave de API do TMDb:
       ```plaintext
       TMDB_API_KEY=sua_chave_api_aqui
       ```

### 5. **Executando o Backend (FastAPI)**
   - **Inicie o servidor FastAPI**:
     ```bash
     uvicorn main:app --reload
     ```
   - O servidor estará rodando em `http://localhost:8000`.

### 6. **Executando o Frontend (Streamlit)**
   - **Inicie o aplicativo Streamlit**:
     ```bash
     streamlit run app.py
     ```
   - O aplicativo estará disponível em `http://localhost:8501`.

### 7. **Usando o Aplicativo**
   - **Pesquise por um filme**:
     - No navegador, acesse `http://localhost:8501`.
     - Digite o nome de um filme na caixa de pesquisa e clique em "Buscar".
   - **Visualize os resultados**:
     - O aplicativo exibirá detalhes do filme, críticas, filmes relacionados e filmes do mesmo gênero.

### 8. **Testando a API**
   - **Teste a API diretamente**:
     - Você pode testar a API diretamente usando ferramentas como `curl` ou Postman.
     - Exemplo de requisição:
       ```bash
       curl -X POST "http://localhost:8000/perguntar" -H "Content-Type: application/json" -d '{"query": "Inception"}'
       ```

### 9. **Parando o Aplicativo**
   - **Parar o Streamlit**:
     - No terminal onde o Streamlit está rodando, pressione `Ctrl+C` para parar o servidor.
   - **Parar o FastAPI**:
     - No terminal onde o FastAPI está rodando, pressione `Ctrl+C` para parar o servidor.
   - **Parar o Weaviate**:
     - Se estiver rodando localmente com Docker, você pode parar o contêiner com:
       ```bash
       docker stop weaviate
       ```

