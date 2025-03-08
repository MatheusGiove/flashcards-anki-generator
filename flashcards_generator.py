from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st
import pandas as pd

openai_api_key = st.secrets["openai"]["api_key"]

template = """
You are an English teacher from the United States giving lessons to a student from Brazil who is learning English.

Instructions:

- Analyze the word provided and give a translation and meaning.
- If there is more than one translation, use hyphens. Maximum of 5 translations. (Example: "Casa - Lar")
- Use 3 example sentences (minimum 3 words, maximum 6).
- For words with multiple meanings, use sentences that demonstrate each sense.
- Avoid difficult words in the examples.
- Explain the meaning in no more than 10 words.
- Highlight the word in sentences with <b>[Word]</b>.
- In the 3 example sentences, you can use one in the past, one in the present, and one in the future.
- If possible, provide synonyms for the word.
- If the word has cultural relevance, idiomatic usage, or is part of a phrasal verb, add a tip.

Final format should be exactly as follows:

<p>[Word] <span>/[Phonetic transcription]/</span></p>
<br>
<p><em>Part of Speech:</em> [Class in Portuguese]</p>
<p><em>Translation:</em> [Translation in Portuguese]</p>
<p><em>Meaning:</em> [Brief meaning in Portuguese]</p>
<p><em>Synonym:</em> [synonym 1 in English], [synonym 2 in English]</p>
<br>
<p><em>Tip:</em> [Cultural tip or idiomatic use, if necessary]</p>
<br>
<p>[Example sentence in the present]</p>
<p>[Example sentence in the past]</p>
<p>[Example sentence in the future]</p>

- The [] are just to highlight parts of the response, do not include them in the final response.

---

**Example:**

<p>Run <span>/rʌn/</span></p>
<br>
<p><em>Part of Speech:</em> Verbo</p>
<p><em>Translation:</em> Correr - Funcionar</p>
<p><em>Meaning:</em> Movimentar-se rápido - Fazer algo funcionar</p>
<p><em>Synonym:</em> Sprint, Jog, Operate</p>
<br>
<p><em>Tip:</em> "Run" também é usado em expressões como "run out of time".</p>
<br>
<p>I <b>run</b> every day.</p>
<p>She <b>ran</b> yesterday.</p>
<p>I will <b>run</b> tomorrow.</p>

Now that you understand the instructions, let's begin!

The word to be studied is: "{word}"
"""

prompt = PromptTemplate.from_template(template=template)

chat = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini-2024-07-18",
    openai_api_key=openai_api_key
)

chain = prompt | chat


def take_word_list(dataframe):
  words = dataframe

  inputs = [{"word": word} for word in words["Palavras"]]

  results = chain.batch(inputs)

  explanation = [result.content for result in results]

  df = pd.DataFrame({
      "Word": words["Palavras"],
      "Explanation": explanation
  })

  return df
