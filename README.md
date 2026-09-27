# 📚 RAG Tabanlı Doküman Soru-Cevap Asistanı

**Streamlit**, **FAISS**, **HuggingFace Embeddings** ve **Google Gemini API** kullanılarak geliştirilmiş; yerel öncelikli (local-first) ve yüksek performanslı bir Retrieval-Augmented Generation (RAG) sistemidir.

Bu uygulama, kullanıcıların PDF formatındaki dokümanlarını yüklemelerine ve doğal dilde sorular sormalarına olanak tanır. Yüklenen dokümanlar yerel ortamda vektörleştirilerek indekslenir ve Google Gemini modelleri kullanılarak yalnızca doküman içeriğine dayalı, tutarlı yanıtlar üretilir.

---

## 📸 Genel Bakış ve Mimari

Geleneksel hazır kütüphane yapılandırmalarının aksine, bu projede **hibrit bir çalışma mimarisi** benimsenmiştir:

1. **Yerel Embedding (Vektörleştirme):** Metin parçaları, harici API bağımlılığını ve maliyetlerini ortadan kaldırmak amacıyla HuggingFace'in `all-MiniLM-L6-v2` modeli ile doğrudan kullanıcının bilgisayarında vektörleştirilir.
2. **Vektör Veritabanı:** Üretilen vektörler, hızlı benzerlik aramaları için bellek içi (in-memory) **FAISS** vektör veritabanında saklanır.
3. **Esnek LLM Entegrasyonu:** Google'ın resmi `google-genai` SDK'sı kullanılarak, sunucu yoğunluğu (HTTP 503) veya model güncellemelerine karşı otomatik **model geçişi (fallback) ve tekrar deneme (retry)** mekanizması kurgulanmıştır.

---

## ✨ Öne Çıkan Özellikler

- **Gizlilik Odaklı Yerel Vektörleştirme:** Hassas doküman verileri dış servis API'lerine gönderilmeden yerel makinede işlenir.
- **Hızlı Benzerlik Araması:** FAISS altyapısı sayesinde yüksek hızlı bağlam yakalama.
- **Doğrudan Bağlama Dayalı Yanıtlar:** Geliştirilen yönlendirmeler (prompt engineering) sayesinde modelin doküman dışına çıkıp uydurma (hallucination) cevap üretmesi engellenir.
- **Hata Toleranslı Mimarisi:** Google GenAI istek sınırları veya geçici sunucu kesintilerinde uygulamanın çökmesini engelleyen yedekli model stratejisi.

---

## 🛠️ Kullanılan Teknolojiler

- **Kullanıcı Arayüzü:** [Streamlit](https://streamlit.io/)
- **Vektör Veritabanı:** [FAISS](https://github.com/facebookresearch/faiss)
- **Embedding Modeli:** HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
- **PDF İşleme:** `pypdf`
- **LLM Motoru:** [Google GenAI SDK](https://pypi.org/project/google-genai/) (Gemini Flash Serisi)
- **Metin Parçalama:** LangChain Text Splitters

---

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Python 3.10 veya üzeri
- Geçerli bir Google Gemini API Anahtarı ([Google AI Studio](https://aistudio.google.com/)'dan ücretsiz alınabilir)

### Kurulum Adımları

1. **Projeyi klonlayın:**
   ```bash
   git clone https://github.com/13yusuf/rag-dokuman-asistani.git
   (https://github.com/kullanici_adin/rag-dokuman-asistani.git)
   cd rag-dokuman-asistani
