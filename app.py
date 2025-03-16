"""Main application file for the movie chatbot."""
import streamlit as st
from api import consultar_filme
from components import (
    exibir_detalhes_filme,
    exibir_criticas,
    exibir_filme_card,
    exibir_filmes_relacionados
)
from styles import CUSTOM_CSS

# Configure page settings
st.set_page_config(
    page_title="Chatbot de Filmes 🎬",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
st.markdown(f"<style>{CUSTOM_CSS}</style>", unsafe_allow_html=True)

def main():
    st.title("🎬 Chatbot de Filmes")
    st.markdown("### Descubra informações sobre seus filmes favoritos")
    
    # Input do usuário com label oculto
    pergunta = st.text_input(
        "Pesquise um filme:",  # Adicionando um label
        placeholder="Digite o nome de um filme...",
        key="movie_input"
    )
    
    # Botão de busca
    if st.button("🔍 Buscar"):
        if not pergunta.strip():
            st.warning("Por favor, digite o nome de um filme.")
            return
            
        with st.spinner("Buscando informações..."):
            resposta = consultar_filme(pergunta)
            
            if resposta:
                # Exibir mensagem principal
                st.markdown(f'<div class="success-message">{resposta["resposta"]}</div>', unsafe_allow_html=True)
                
                # Exibir detalhes do filme principal
                if "detalhes" in resposta:
                    st.markdown("---")
                    exibir_detalhes_filme(resposta["detalhes"])
                    
                    # Exibir críticas se disponíveis
                    if "criticas" in resposta["detalhes"]:
                        st.markdown("---")
                        exibir_criticas(resposta["detalhes"]["criticas"])
                    
                    # Exibir filmes relacionados se disponíveis
                    if "relacionados" in resposta["detalhes"]:
                        st.markdown("---")
                        exibir_filmes_relacionados(resposta["detalhes"]["relacionados"])
                
                # Exibir filmes do mesmo gênero
                if "filmes_mesmo_genero" in resposta and resposta["filmes_mesmo_genero"]:
                    st.markdown("---")
                    st.markdown("### 🎬 Filmes do Mesmo Gênero")
                    for filme in resposta["filmes_mesmo_genero"]:
                        exibir_filme_card(filme, is_similar=False)
                
                # Mensagem quando não há informações adicionais
                if not any([
                    resposta.get("detalhes"),
                    resposta.get("filmes_mesmo_genero"),
                    resposta.get("sugestoes")
                ]):
                    st.markdown('<div class="warning-message">Nenhuma informação adicional disponível.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
