# 📚 BookIQ — Intelligent Book Summarization Platform

> **POC** · NLP · Extractive Summarization · NLTK · Streamlit · SQLite · ROUGE Evaluation

An AI-powered book summarization platform that accepts book text (file upload or paste), applies NLP preprocessing, intelligent chunking, and TF-IDF extractive summarization to produce concise summaries with key idea extraction, keyword analysis, and ROUGE quality scores.

---

## 📌 Overview

| Field           | Details                                                             |
|-----------------|---------------------------------------------------------------------|
| **Domain**      | NLP — Book Summarization & Key Idea Extraction                      |
| **Language**    | Python 3.10+                                                        |
| **NLP Engine**  | NLTK + TF-IDF Extractive Summarization                              |
| **Framework**   | Streamlit + Plotly                                                  |
| **Database**    | SQLite (via built-in `db.py`)                                       |
| **Auth**        | Role-based (admin / user) with SHA-256 password hashing            |
| **Input**       | .txt file, .pdf file (needs PyMuPDF), or paste text directly        |
| **Evaluation**  | ROUGE-1 Precision, Recall, F1                                       |

---

## 🗂️ Project Structure

```
BookIQ/
│
├── sample_books/
│   ├── sherlock_holmes.txt          ← Built-in sample book
│   └── great_expectations.txt       ← Built-in sample book
│
├── database/
│   └── bookiq.db                    ← Auto-created SQLite database
│
├── output/                          ← Generated exports (auto-created)
│
├── scripts/
│   ├── nlp_engine.py               ← NLP core: clean, chunk, summarize, ROUGE
│   └── db.py                       ← SQLite database layer
│
├── streamlit/
│   └── app.py                      ← Full web application
│
├── requirements.txt                 ← Python dependencies
└── README.md                        ← This file
```

---

## ⚙️ Setup & Installation

### 1. Navigate to the Project

```powershell
cd BookIQ
```

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows PowerShell
# OR
source .venv/bin/activate            # macOS / Linux
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

> **Note:** `pymupdf` is only needed for PDF upload support. The app works fully without it for `.txt` files.

### 4. Download NLTK Data (Auto-handled)

The app downloads required NLTK packages automatically on first run. If you prefer to do it manually:

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
```

---

## 🚀 Running the Application

```powershell
cd streamlit
streamlit run app.py
```

Open your browser at: **http://localhost:8501**

---

## 🔐 Login Credentials

| Username | Password   | Role  |
|----------|------------|-------|
| `raghav` | `raghav123`| User  |
| `admin`  | `admin123` | Admin |
| `demo`   | `demo123`  | User  |

---

## 🌐 Application Pages

| Page                | Description                                                              |
|---------------------|--------------------------------------------------------------------------|
| 📖 Summarize Book   | Upload / paste / load sample book → generate AI summary instantly        |
| 📚 My Library       | View all your books, browse summaries, download, delete                  |
| 📊 Analytics        | ROUGE scores, compression trends, length preferences, usage charts       |
| 🛡️ Admin Panel      | (Admin only) User management, all-books view, full access log            |

---

## 🤖 NLP Pipeline

```
Input Text (paste / .txt / .pdf)
        │
        ▼
   clean_text()
   • Normalize unicode  • Remove noise
   • Fix whitespace     • Language detection
        │
        ▼
   chunk_text()
   • Split into overlapping word-boundary chunks
   • Default: 800 words/chunk, 80-word overlap
        │
        ▼
   extractive_summary() — per chunk
   • TF-IDF word frequency scoring
   • Top-N sentence selection
   • Re-order by original position
        │
        ▼
   Combine chunk summaries → Final summary pass
        │
        ├── extract_keywords()    → Top-10 content words
        ├── extract_key_ideas()   → 5 diverse key sentences
        └── rouge1_score()        → Precision / Recall / F1
        │
        ▼
   Display + Save to SQLite
```

---

## 📊 Summary Length Options

| Setting    | Sentences/Chunk | Final Sentences | Best For              |
|------------|-----------------|-----------------|------------------------|
| `short`    | 3               | 4               | Quick overview          |
| `medium`   | 5               | 7               | Balanced understanding  |
| `detailed` | 8               | 12              | Deep comprehension      |

---

## 🗃️ Database Schema

### `users`
| Column        | Type    | Description                  |
|---------------|---------|------------------------------|
| id            | INTEGER | Primary key                  |
| username      | TEXT    | Unique login name            |
| password_hash | TEXT    | SHA-256 hashed password      |
| role          | TEXT    | `admin` or `user`            |
| created_at    | TEXT    | ISO timestamp                |

### `books`
| Column      | Type    | Description                     |
|-------------|---------|----------------------------------|
| id          | INTEGER | Primary key                     |
| user_id     | INTEGER | Foreign key → users             |
| title       | TEXT    | Book title                      |
| author      | TEXT    | Author name                     |
| tags        | TEXT    | Comma-separated tags            |
| raw_text    | TEXT    | Full original text              |
| word_count  | INTEGER | Total words                     |
| language    | TEXT    | Detected language               |
| uploaded_at | TEXT    | ISO timestamp                   |

### `summaries`
| Column       | Type    | Description                    |
|--------------|---------|--------------------------------|
| id           | INTEGER | Primary key                    |
| book_id      | INTEGER | Foreign key → books            |
| user_id      | INTEGER | Foreign key → users            |
| summary_text | TEXT    | Generated summary              |
| key_ideas    | TEXT    | Newline-separated key ideas    |
| keywords     | TEXT    | Comma-separated keywords       |
| length_pref  | TEXT    | short / medium / detailed      |
| style_pref   | TEXT    | paragraph / bullets            |
| rouge_f1     | REAL    | ROUGE-1 F1 score               |
| compression  | REAL    | Compression percentage         |
| created_at   | TEXT    | ISO timestamp                  |

### `access_logs`
| Column    | Type    | Description              |
|-----------|---------|--------------------------|
| id        | INTEGER | Primary key              |
| user_id   | INTEGER | Who performed the action |
| action    | TEXT    | LOGIN / SUMMARIZE / etc. |
| detail    | TEXT    | Extra context            |
| timestamp | TEXT    | ISO timestamp            |

---

## 📈 ROUGE-1 Evaluation

The app computes ROUGE-1 against the first 3,000 words of the original text:

| Metric    | Meaning                                          |
|-----------|--------------------------------------------------|
| Precision | What fraction of summary words appear in source  |
| Recall    | What fraction of source words appear in summary  |
| F1        | Harmonic mean of precision and recall            |

---

## 🛠️ Tech Stack

| Layer         | Technology                              |
|---------------|-----------------------------------------|
| Language      | Python 3.10+                            |
| NLP           | NLTK 3.8+ (tokenization, stopwords)     |
| Summarization | TF-IDF extractive (custom engine)       |
| Web Framework | Streamlit 1.32+                         |
| Visualization | Plotly 5                                |
| Database      | SQLite 3 (built-in Python)              |
| Auth          | SHA-256 password hashing                |
| PDF Support   | PyMuPDF (optional)                      |

---

## 🗺️ Module Mapping to POC Spec

| POC Requirement                        | Implemented In                    |
|----------------------------------------|-----------------------------------|
| File upload (txt, pdf)                 | `app.py` — Upload File tab        |
| Paste text input                       | `app.py` — Paste Text tab         |
| Metadata capture (title, author, tags) | `app.py` input fields             |
| Database schema                        | `db.py` — 4-table SQLite schema   |
| Secure authentication + RBAC          | `db.py` — SHA-256 + role field    |
| Search and filter books               | `app.py` — Library search bar     |
| Text cleaning & normalization         | `nlp_engine.py` — clean_text()    |
| Chunking with overlap                 | `nlp_engine.py` — chunk_text()    |
| NLP summarization model               | `nlp_engine.py` — TF-IDF engine  |
| Key idea extraction                   | `nlp_engine.py` — extract_key_ideas() |
| Keyword extraction                    | `nlp_engine.py` — extract_keywords()  |
| Summary length & style controls       | `app.py` — settings section       |
| Download / export summary (.txt)      | `app.py` — download buttons       |
| ROUGE evaluation metrics              | `nlp_engine.py` — rouge1_score()  |
| Analytics dashboard                   | `app.py` — Analytics page         |
| Admin panel + access logs             | `app.py` — Admin Panel page       |

---

## 📄 License

This project is a Proof of Concept (POC) for educational and demonstration purposes.

---

*BookIQ · Intelligent Book Summarization Platform · Built with ❤️ using Python + NLTK + Streamlit*
