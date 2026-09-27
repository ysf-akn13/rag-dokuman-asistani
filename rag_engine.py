import os
import time
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# .env dosyasındaki API anahtarını yükle
load_dotenv()

# Google'ın kullanmanı istediği güncel model listesi
VALID_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash"
]

def get_client():
    """Google GenAI istemcisini başlatır."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY bulunamadı! .env dosyanızı kontrol edin.")
    return genai.Client(api_key=api_key)

def get_embeddings():
    """Lokalde çalışan HuggingFace embedding modelini çağırır."""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def extract_pdf_text(pdf_docs):
    """Yüklenen PDF dosyalarından metin çıkarır."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    return text

def create_vector_store(text_content):
    """Metni parçalar ve FAISS vektör veritabanını oluşturur."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_text(text_content)
    
    embeddings = get_embeddings()
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

def format_docs(docs):
    """Bulunan belge parçalarını tek bir metinde birleştirir."""
    return "\n\n".join(doc.page_content for doc in docs)

def answer_question(user_query):
    """RAG ve güncel Gemini 3.5 modelleri ile yanıt üretir."""
    embeddings = get_embeddings()
    vector_store = FAISS.load_local(
        "faiss_index", 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(user_query)
    context = format_docs(docs)

    prompt = f"""Sen yüklenen dokümanlara göre soruları yanıtlayan yardımcı bir asistansın.
Yalnızca sağlanan bağlamı (context) kullanarak soruyu yanıtla.
Eğer cevabı verilen bağlamda bulamazsan 'Verilen dokümanda bu sorunun cevabı bulunmamaktadır.' de.
Tahminde bulunma veya uydurma cevap verme.

Bağlam:
{context}

Soru: {user_query}
"""

    client = get_client()
    last_error = None

    for model_name in VALID_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            last_error = e
            err_msg = str(e)
            
            # Yoğunluk (503) varsa 1 saniye bekleip yedek modele geç
            if "503" in err_msg or "UNAVAILABLE" in err_msg:
                time.sleep(1)
                continue
            
            continue

    raise RuntimeError(f"Model çağrısı başarısız oldu. Son hata: {last_error}")