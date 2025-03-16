"""UI components for the movie chatbot."""
import streamlit as st
from typing import Dict, Any

def exibir_detalhes_filme(detalhes: Dict[str, Any]):
    """Exibe os detalhes do filme principal."""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if detalhes["poster"]:
            st.image(detalhes["poster"], use_column_width=True)
    
    with col2:
        st.markdown(f"### {detalhes['titulo']}")
        st.markdown(f"**Data de Lançamento:** {detalhes['data_lancamento']}")
        st.markdown(f"**Nota TMDb:** ⭐ {detalhes['nota_tmdb']}")
        st.markdown("**Descrição:**")
        st.markdown(f"_{detalhes['descricao']}_")

def exibir_criticas(criticas: list):
    """Exibe as críticas do filme."""
    st.markdown("### 📝 Críticas")
    if not criticas:
        st.markdown('<div class="warning-message">Nenhuma crítica disponível.</div>', unsafe_allow_html=True)
        return

    for critica in criticas:
        with st.container():
            st.markdown('<div class="review-card">', unsafe_allow_html=True)
            st.markdown(f'<span class="review-author">👤 {critica["autor"]}</span>', unsafe_allow_html=True)
            if critica["nota"]:
                st.markdown(f'<span class="review-rating">⭐ {critica["nota"]}/10</span>', unsafe_allow_html=True)
            st.markdown(f'<div class="review-content">{critica["conteudo"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

def exibir_filme_card(filme: Dict[str, Any], is_similar: bool = False):
    """Exibe um card de filme com informações básicas."""
    with st.container():
        st.markdown('<div class="movie-card">', unsafe_allow_html=True)
        
        cols = st.columns([1, 2])
        with cols[0]:
            poster_path = filme.get("poster_path") if is_similar else filme.get("poster")
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if is_similar else poster_path
                st.image(poster_url, use_column_width=True)
        
        with cols[1]:
            title = filme.get("title") if is_similar else filme.get("titulo")
            overview = filme.get("overview") if is_similar else filme.get("descricao")
            
            st.markdown(f'<div class="movie-title">{title}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="movie-description">{overview}</div>', unsafe_allow_html=True)
            
            if filme.get("nota"):
                st.markdown(f'<div class="movie-info">⭐ {filme["nota"]}/10</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def exibir_filmes_relacionados(relacionados: list):
    """Exibe os filmes relacionados."""
    if not relacionados:
        return

    st.markdown("### 🎬 Filmes Relacionados")
    for filme in relacionados:
        exibir_filme_card(filme, is_similar=False)