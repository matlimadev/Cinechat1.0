"""API client for the movie chatbot."""
import requests
from typing import Optional, Dict, Any
import streamlit as st

def consultar_filme(pergunta: str) -> Optional[Dict[str, Any]]:
    """Consulta a API do chatbot de filmes."""
    url = "http://localhost:8000/perguntar"
    try:
        response = requests.post(url, json={"query": pergunta}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro na comunicação com o servidor: {str(e)}")
        return None