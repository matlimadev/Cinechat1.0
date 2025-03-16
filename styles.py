"""CSS styles for the Streamlit application."""

CUSTOM_CSS = """
    .main { padding: 2rem; }
    .stButton>button {
        width: 100%;
        background-color: #3B82F6;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: 600;
    }
    .stButton>button:hover { background-color: #2563EB; }
    .movie-card {
        background-color: #1F2937;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .movie-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .movie-info { color: #9CA3AF; margin-bottom: 0.5rem; }
    .movie-description { color: #D1D5DB; }
    .review-card {
        background-color: #374151;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .review-author { color: #60A5FA; font-weight: 600; }
    .review-rating { color: #FBBF24; font-weight: 600; }
    h1 {
        text-align: center;
        color: white;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .stTextInput>div>div>input {
        background-color: #374151;
        color: white;
        border: 1px solid #4B5563;
    }
    .stTextInput>div>div>input:focus {
        border-color: #3B82F6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
    }
    .stSpinner>div>div { border-color: #3B82F6 transparent; }
    .success-message {
        background-color: #065F46;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .warning-message {
        background-color: #92400E;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .error-message {
        background-color: #991B1B;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
"""