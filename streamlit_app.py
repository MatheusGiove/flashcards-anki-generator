import streamlit as st
import pandas as pd
import tempfile
from flashcards_generator import take_word_list
from datetime import datetime
from st_paywall import add_auth

st.set_page_config(
    page_title="FlashForge",
    initial_sidebar_state="expanded",
    layout="wide",
    page_icon="✨"
)

st.markdown("""
    <div style="
        border: 2px solid #AA44EE;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #1E1E1E;
        color: white;
        text-align: center;">
        <h1>✨ Crie flashcards para estudar inglês no Anki! ✨</h1>
        <p>Adicione palavras e gere flashcards otimizados para seus estudos de inglês.</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2, gap="large")

if "words" not in st.session_state:
  st.session_state.words = []

col1.subheader("Adicionar Palavras:")
word_input = col1.chat_input("Digite a palavra aqui")

if word_input:
  st.session_state["words"].append(word_input.capitalize())

card_title = col2.subheader("Gerenciador de Palavras:")

select_words = col2.multiselect(
    "Palavras Adicionadas:",
    st.session_state.words,
    st.session_state.words
)

with st.sidebar:
  st.markdown("""
    <div style="
        border: 2px solid #AA44EE;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #1E1E1E;
        color: white;
        text-align: center;">
        <h1>FlashForge</h1>
    </div>
""", unsafe_allow_html=True)

  st.markdown("""
    <div style="
        border: 2px solid #AA44EE;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #1E1E1E;
        color: white;
        text-align: center;">
        <h2>💎 OneDrive Bilíngue: 💎</h2>
        <ul style="text-align: left;">
            <li>📚 Desbloqueie +1300 flashcards em inglês para turbinar seus estudos!</li>
            <li>🚀 Aprenda de forma contínua: todo dia, 20 novos flashcards são adicionados ao drive.</li>
            <li>🎯 Estude no Anki e aprimore seu vocabulário de forma eficiente!</li>
        </ul>
    </div>
  """, unsafe_allow_html=True)

  add_auth(
      required=False,
      show_redirect_button=True,
      subscription_button_text="💎🔥Tenha acesso a +1400 palavras e acelere seus estudos!🔗 🔥💎",
      button_color="#AA44EE",
      use_sidebar=True
  )

  with st.expander("Como usar"):
    st.markdown("""
    **1.** Adicione palavras na caixa de texto.

    **2.** Clique em "Gerar Flashcards" para criar.
    
    **3.** Exporte o arquivo CSV para usar no Anki ou outra ferramenta.  
    """)

  with st.expander("Entre em contato"):
    st.markdown(""" 
    🔗 **LinkedIn:** [Link](https://www.linkedin.com/in/matheusgiove)\n
    🌐 **GitHub:** [Link](https://www.github.com/MatheusGiove/)
    """)

  st.write("v1.0.1-alpha")


def create_flashcards():
  df_temporary = pd.DataFrame(select_words, columns=["Palavras"])

  df = take_word_list(df_temporary)

  with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmpfile:
    df.to_csv(tmpfile.name, index=False, header=False,
              sep=";", decimal=",", encoding="utf-8")
    tmp_filename = tmpfile.name

  with open(tmp_filename, "rb") as f:
    download = st.download_button(
        label="📥 Baixar Flashcards",
        data=f,
        file_name=f"cards_{datetime.now().strftime('%Y-%m-%d')}.csv",
        mime="text/csv",
        type="primary"
    )


if len(select_words) > 0:
  button_to_create_cards = col1.button("Gerar Flashcards", type="primary")
  clean_words = col2.button("Limpar Palavras", type="secondary")

  if clean_words:
    st.session_state.words = []
    st.rerun()

  if button_to_create_cards:
    st.divider()
    if len(select_words) > 20:
      st.error(
          "Só é possível gerar até 20 flashcards por vez. Selecione até 20 palavras.")
    else:
      waiting = st.warning("Aguarde enquanto geramos os flashcards...")
      create_flashcards()
      st.success("Flashcards gerados com sucesso!")
      waiting.empty()
