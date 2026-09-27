import os
import streamlit as st
from rag_engine import extract_pdf_text, create_vector_store, answer_question

st.set_page_config(page_title="RAG Doküman Asistanı", page_icon="📚", layout="wide")

st.title("📚 RAG Tabanlı Doküman Soru-Cevap Asistanı")
st.write("PDF dokümanlarınızı yükleyin, indeksleyin ve içerik hakkında soru sorun.")

# Sol Yan Menü - Doküman Yükleme
with st.sidebar:
    st.header("1. Doküman Yükleme")
    uploaded_files = st.file_uploader("PDF dosyalarını seçin", type=["pdf"], accept_multiple_files=True)
    
    if st.button("Dokümanları İşle ve İndeksle"):
        if uploaded_files:
            with st.spinner("Metinler çıkarılıyor ve vektör veritabanı oluşturuluyor..."):
                raw_text = extract_pdf_text(uploaded_files)
                if raw_text.strip():
                    create_vector_store(raw_text)
                    st.success("Dokümanlar başarıyla indekslendi! Artık soru sorabilirsiniz.")
                else:
                    st.error("PDF dosyalarından okunabilir metin çıkarılamadı.")
        else:
            st.warning("Lütfen en az bir PDF dosyası yükleyin.")

# Ana Ekran - Soru Cevap Alanı
st.header("2. Dokümanınız Hakkında Soru Sorun")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmiş mesajları görüntüle
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girişi
if user_prompt := st.chat_input("Sorunuzu buraya yazın..."):
    # İndeks klasörü kontrolü
    if not os.path.exists("faiss_index"):
        st.error("Lütfen önce sol taraftan bir PDF yükleyip 'Dokümanları İşle' butonuna basın.")
    else:
        # Kullanıcı mesajını ekle
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Asistan cevabını üret
        with st.chat_message("assistant"):
            with st.spinner("Doküman taranıyor..."):
                try:
                    response = answer_question(user_prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Bir hata oluştu: {str(e)}")