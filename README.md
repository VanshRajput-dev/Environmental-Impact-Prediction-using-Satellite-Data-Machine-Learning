# ⚖️ AI-Powered Legal Document Simplifier

> A privacy-preserving NLP pipeline that transforms complex legal clauses into plain English — grounded in 13,000+ real lawyer-labeled contracts.

---

## 📌 Overview

Most people — freelancers, small business owners, students — sign contracts without fully understanding what they're agreeing to. Hiring a lawyer for every clause is expensive and slow.

This system reads any legal clause and instantly tells you:
- **What it means** in plain English
- **How risky it is** with a confidence score
- **What similar clauses** look like in real contracts

Built as an NLP mini-project using a five-stage pipeline: anonymization → embedding → risk classification → LLM explanation → semantic retrieval.

---

## 🤔 How Is This Different From ChatGPT?

When you ask ChatGPT to simplify a legal clause, it guesses from training data — it has no access to real labeled contracts and no way to show you what similar clauses look like in practice.

This system is different in three ways:

| Feature | This System | ChatGPT |
|---|---|---|
| Privacy | Anonymizes entities before any LLM call | Sends raw text to external API |
| Grounding | Retrieves real clauses from 13,000+ labeled contracts | Generates from training data |
| Risk Score | Trained classifier with confidence % | Generic opinion |
| Similar Clauses | Cosine similarity over real SEC-filed contracts | None |
| Architecture | 5-stage NLP pipeline | Single prompt |

---

## 🧠 NLP Techniques Used

| Technique | Tool | Purpose |
|---|---|---|
| Named Entity Recognition | spaCy `en_core_web_sm` | Identify and anonymize persons, orgs, dates, money |
| Sentence Embeddings | `all-MiniLM-L6-v2` (Sentence-BERT) | Convert clauses to 384-dim semantic vectors |
| Cosine Similarity Search | scikit-learn | Retrieve most similar real clauses from database |
| Text Classification | Logistic Regression on embeddings | Predict risk level (low / medium / high) with confidence |
| Abstractive Generation | LLaMA 3.1 via Groq | Generate plain-English simplification |

---

## ⚙️ System Architecture

```
Input Legal Text
       │
       ▼
[ Anonymizer ]           spaCy NER → replace PERSON, ORG, DATE, MONEY
       │                 with placeholders → privacy preserved
       │
       ├──────────────► [ Risk Classifier ]
       │                 MiniLM embedding → LogisticRegression
       │                 → level + confidence score
       │
       ├──────────────► [ LLM — Groq/LLaMA 3.1 ]
       │                 Single structured call on anonymized text
       │                 → simplified + risk_explanation (JSON)
       │
       └──────────────► [ Similarity Search ]
                         Cosine similarity over CUAD clause embeddings
                         → top-5 real similar clauses with scores
       │
       ▼
[ Deanonymizer ]         Restore original entity names in LLM output
       │
       ▼
[ API Response ]
```

---

## 📊 Dataset

The clause database and risk classifier are trained on the **CUAD (Contract Understanding Atticus Dataset)**:
- 510 real commercial contracts from SEC EDGAR filings
- 13,101 clauses labeled by law students, reviewed by experienced lawyers
- 41 clause types including Anti-Assignment, Exclusivity, Governing Law, Termination
- Licensed under CC BY 4.0

> Source: Hendrycks et al., NeurIPS 2021 — [arxiv.org/abs/2103.06268](https://arxiv.org/abs/2103.06268)

---

## 🚀 Features

- 🔒 **Privacy-Preserving** — entities anonymized before any external API call
- 📊 **Risk Classification** — trained classifier returns `low / medium / high` + confidence %
- 🔍 **Semantic Retrieval** — finds real similar clauses from 13,000+ labeled examples
- 💬 **Plain English Output** — LLM explains the clause in language a non-lawyer can understand
- ✅ **41 Tested Cases** — full pytest suite covering unit + integration + edge cases

---

## 💻 Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI + Uvicorn |
| NER | spaCy `en_core_web_sm` |
| Embeddings | Sentence-Transformers `all-MiniLM-L6-v2` |
| Classifier | scikit-learn LogisticRegression |
| LLM | LLaMA 3.1 8B via Groq API |
| Frontend | React (v0) |
| Testing | pytest + FastAPI TestClient |

---

## ▶️ Setup

```bash
# Clone the repository
git clone https://github.com/Kshitizbansal02/legal-document-simplifier-nlp.git
cd legal-document-simplifier-nlp/backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Set your Groq API key
echo GROQ_API_KEY=your_key_here > .env

# Train the risk classifier (run once)
python scripts/Train_risk.py

# Start the API
uvicorn main:app --reload
```

API docs available at: `http://localhost:8000/docs`

---

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

41 tests across 5 categories:
- `TestHealth` — API startup and model loading
- `TestAnonymizer` — NER entity detection and restoration
- `TestSimilarity` — embedding search and score ordering
- `TestRiskPrediction` — classifier output validation
- `TestAnalyzeEndpoint` — full pipeline integration
- `TestEdgeCases` — empty input, long input, mixed language

---

## 📡 API Reference

### `POST /api/v1/analyze`

**Request:**
```json
{ "text": "The Licensee shall not assign or sublicense any rights without prior written consent." }
```

**Response:**
```json
{
  "anonymized_text": "The [PERSON_1] shall not assign...",
  "simplified": "You cannot give away your rights without getting permission first.",
  "risk_explanation": "This limits your flexibility and could trap you in the agreement.",
  "risk": {
    "level": "high",
    "confidence": 0.827,
    "description": "Significant legal or financial risk. Legal counsel strongly advised.",
    "method": "classifier"
  },
  "similar_clauses": [
    {
      "clause_text": "Licensee may not assign this Agreement...",
      "clause_type": "Anti-Assignment",
      "risk_level": "high",
      "score": 0.746
    }
  ]
}
```

---

## ⚠️ Limitations

- spaCy occasionally misclassifies legal role words (e.g. "Licensee") as persons — this is a known limitation of general-purpose NER on legal text
- Risk classifier performance depends on CUAD label distribution — uncommon clause types may have lower accuracy
- LLM responses are non-deterministic at higher temperatures; system uses `temperature=0.2` for consistency

---

## 🔮 Future Improvements

- 🌍 Multi-language support (Hindi, Tamil)
- 🔊 Voice-based clause explanation
- ☁️ Cloud deployment
- 🤖 Fine-tuned legal-specific embedding model (legal-bert)
- 📄 Full document upload (PDF/DOCX) instead of single clause

---

## 👨‍💻 Authors

**Kshitiz Bansal** — B.Tech CSE (AIML)

---

## 📜 License

This project is for academic and educational purposes. Dataset (CUAD) is licensed under CC BY 4.0.