import streamlit as st
import pandas as pd
import tempfile
from flashcards_generator import take_word_list
from datetime import datetime

st.set_page_config(
    page_title="Flashcard Creator App 📚",
    initial_sidebar_state="expanded",
    layout="wide"
)

st.markdown(
    """
    <style>
        div[data-testid="column"] {
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 100vh;
        }
        
        /* Ajuste adicional para mobile */
        @media (max-width: 640px) {
            div[data-testid="column"] {
                height: 90vh;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sua coluna principal com o chat
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
  # Seu conteúdo do chat aqui
  st.title("Flashcard Creator App")
  word_input = st.chat_input("Digite a palavra que deseja estudar")


if "words" not in st.session_state:
  st.session_state.words = []


if word_input:
  st.session_state["words"].append(word_input.capitalize())

with st.sidebar:
  card_title = st.title("Flashcard Creator App 📚")

  st.divider()

  select_words = st.multiselect(
      "Palavras Adicionadas:",
      st.session_state.words,
      st.session_state.words
  )

  st.divider()

  button_to_create_cards = st.button("Gerar Flashcards", type="primary")

  clean_words = st.button("Limpar Palavras", type="secondary")

if clean_words:
  st.session_state.words = []
  st.rerun()


if select_words and button_to_create_cards:
  df_temporary = pd.DataFrame(select_words, columns=["Palavras"])

  df = take_word_list(df_temporary)

  with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmpfile:
    df.to_csv(tmpfile.name, index=False, header=False,
              sep=";", decimal=",", encoding="utf-8")
    tmp_filename = tmpfile.name

  with open(tmp_filename, "rb") as f:
    st.sidebar.divider()
    st.sidebar.download_button(
        label="📥 Baixar Flashcards",
        data=f,
        file_name=f"cards_{datetime.now().strftime('%Y-%m-%d')}.csv",
        mime="text/csv",
        type="primary"
    )
