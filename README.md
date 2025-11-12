
# 🧪 Technical Overview — YNTP Corpus Analysis Toolkit

This repository provides a **reproducible, modular analysis framework** for the  
**Your Next Token Prediction (YNTP) Corpus**, organized per language (`en/`, `cn/`, `jp/`).  
Each folder contains multiple JSON session files (`*_1.json`, `*_2.json`, …) representing multi-day conversations.

---

## ⚙️ 1 · System Architecture

```

YNTP-Analysis/
├── data/
│   ├── en/      # English JSON sessions
│   ├── cn/      # Chinese JSON sessions
│   └── jp/      # Japanese JSON sessions
├── outputs/     # All generated CSVs & plots
├── preprocess.py   # Flattens JSON into tabular format
├── analyze.py      # Performs quantitative and lexical analysis
├── requirements.txt
└── README.md (this file)

```

### Core Design Principles
| Principle | Description |
|------------|-------------|
| **Language-agnostic** | Scripts automatically detect and process any `data/<lang>/` folder. |
| **Stateless processing** | Each run rebuilds all outputs for deterministic results. |
| **Scientific transparency** | Every intermediate artifact (`CSV`, `figure`) is stored under `/outputs/`. |
| **Extensibility** | New analyses can be added via modular functions in `analyze.py`. |

---

## 🧩 2 · Data Flow

```

Raw JSON ──▶ preprocess.py ──▶ combined_all_languages.csv
└──────────────────────────────┬──────────────────┘
▼
analyze.py
├── length_stats_by_language.csv
├── lexical_diversity.csv
├── tfidf_similarity_summary.csv
└── figures/*.png

````

### JSON Input Assumptions
Each file (e.g., `en_1.json`) has this approximate schema:
```json
{
  "day_1": [
    {"speaker": "user", "message": "...", "response": "..."},
    {"speaker": "npc",  "message": "...", "response": "..."}
  ],
  "day_2": [...],
  ...
}
````

All files in the same folder share the same schema.

---

## 🧱 3 · Preprocessing Stage (`preprocess.py`)

### Responsibilities

1. Recursively scans all subfolders in `/data/`.
2. Loads every `*.json` file, flattens nested structures.
3. Adds metadata fields:

   * `language` (folder name)
   * `file` (source file)
   * `day`, `index`, `speaker`, `message`, `response`
4. Performs minimal cleaning (whitespace normalization).

### Output

* `outputs/combined_all_languages.csv`
  One row per dialogue turn across all languages.

---

## 📊 4 · Analysis Stage (`analyze.py`)

### 4.1 Length Statistics

Computes per-language:

* Mean / median characters
* Mean / median tokens
  → `outputs/length_stats_by_language.csv`

### 4.2 Lexical Diversity

Uses the type–token ratio:
[
\text{lexical diversity} = \frac{\text{unique tokens}}{\text{total tokens}}
]
→ `outputs/lexical_diversity.csv`

### 4.3 TF-IDF Cosine Similarity

* Vectorizes all responses per language with **scikit-learn** `TfidfVectorizer`
* Computes pairwise **cosine similarity**
* Reports mean / median of the upper-triangle matrix
  → `outputs/tfidf_similarity_summary.csv`

### 4.4 Visualizations

Histograms of token counts per language
→ `outputs/figures/hist_tokens_<lang>.png`

---

## 🧮 5 · Mathematical Notes

### Tokenization

Simple whitespace segmentation
[
N_{tokens}(r) = |\text{split}(r, " ")|
]

### Cosine Similarity

[
\text{cosine}(x, y) = \frac{x · y}{|x| |y|}
]
where *x* and *y* are TF-IDF vectors.

### Lexical Diversity Caveat

Sensitive to corpus length; consider **MTLD** or **VOCD-D** for deeper stylistic analyses.

---

## 🧠 6 · Extensibility Hooks

| Module                | Extension Idea                                               | Notes                                 |
| --------------------- | ------------------------------------------------------------ | ------------------------------------- |
| `analyze_.py`      | Add `SentenceTransformer` embeddings for semantic similarity | Replace TF-IDF block                  |
| `analyze.py`      | Add statistical tests (Mann-Whitney, t-test)                 | Compare response lengths per language |
| `utils.py` *(future)* | Add text-normalization (stemming, stopword filtering)        | For cross-lingual comparability       |
| New script            | Longitudinal drift analysis (day-to-day change)              | Requires session alignment            |

---

## 🧪 7 · Reproducibility & Environment

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python preprocess.py
python analyze.py
```

Environment:

* Python ≥ 3.10
* Deterministic behavior (no random seed usage in baseline TF-IDF stage)
* All figures saved as static `.png` for reproducibility

---

## 📈 8 · Output Summary

| File                             | Description                     |
| -------------------------------- | ------------------------------- |
| **combined_all_languages.csv**   | Flattened raw data              |
| **length_stats_by_language.csv** | Average/median response lengths |
| **lexical_diversity.csv**        | Type–token ratio per language   |
| **tfidf_similarity_summary.csv** | Lexical similarity summary      |
| **figures/**                     | Histograms of response lengths  |

---

## 🧭 9 · Scientific Context

This toolkit supports replication and secondary analysis of

> *Your Next Token Prediction: A Multilingual Benchmark for Long-Term Conversational Reasoning*
> arXiv preprint 2510.14398 (2025).

It enables quantitative evaluation of lexical consistency, verbosity, and language-specific patterns across YNTP sessions.

---

## 📜 10 · License

MIT License © 2025 Weetschapper Ahmad Al Dibo
Free for academic and research use. Please cite the above arXiv paper when publishing results.
```

