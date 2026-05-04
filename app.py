import streamlit as st
import google.generativeai as genai
import PyPDF2

# Configurare Pagina
st.set_page_config(page_title="MedQuiz AI - Grile Automate", layout="centered")
st.title("🩺 MedQuiz AI")
st.subheader("Transformă cursurile în grile de medicină")

# Setup Gemini
api_key = st.sidebar.text_input("Introdu Gemini API Key:", type="password")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Interfața de încărcare
uploaded_file = st.file_uploader("Încarcă cursul (PDF)", type="pdf")
num_questions = st.slider("Câte grile dorești?", 5, 20, 10)

if st.button("Generează Grile ✨") and uploaded_file and api_key:
    with st.spinner("Gemini analizează textul și creează întrebările..."):
        context = extract_text_from_pdf(uploaded_file)
        
        prompt = f"""
        Ești un expert în educație medicală. Bazându-te pe următorul text, generează {num_questions} grile de tip medicină.
        Fiecare grilă trebuie să aibă:
        1. O întrebare clară.
        2. 5 variante de răspuns (A, B, C, D, E).
        3. Răspunsul corect.
        4. O scurtă explicație a răspunsului bazată pe text.

        Text: {context[:10000]}  # Limităm la primele 10k caractere pentru demo
        
        Format output: Markdown clar.
        """
        
        response = model.generate_content(prompt)
        st.markdown("---")
        st.markdown(response.text)
        
        # Opțiune de download simplă
        st.download_button("Descarcă Grilele", response.text, file_name="grile_medicina.txt")
else:
    if not api_key:
        st.info("Te rugăm să introduci cheia API în bara laterală pentru a începe.")
