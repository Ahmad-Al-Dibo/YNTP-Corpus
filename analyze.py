import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

OUT_DIR = Path("outputs")
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True)

df = pd.read_csv(OUT_DIR / "combined_all_languages.csv")

# --- Basic cleanup ---
df["resp_chars"] = df["response"].fillna("").map(len)
df["resp_tokens"] = df["response"].fillna("").map(lambda x: len(x.split()))

# --- Length stats per language ---
length_stats = (
    df.groupby("language")
      .agg(mean_chars=("resp_chars", "mean"),
           median_chars=("resp_chars", "median"),
           mean_tokens=("resp_tokens", "mean"),
           median_tokens=("resp_tokens", "median"),
           total_responses=("response", "count"))
      .reset_index()
)
length_stats.to_csv(OUT_DIR / "length_stats_by_language.csv", index=False)

# --- Lexical diversity per language ---
def lexical_diversity(series):
    words = []
    for t in series.fillna("").astype(str):
        words.extend(t.lower().split())
    total = len(words)
    unique = len(set(words))
    return unique / total if total > 0 else np.nan

lex_div = (df.groupby("language")["response"]
             .apply(lexical_diversity)
             .reset_index(name="lexical_diversity"))
lex_div.to_csv(OUT_DIR / "lexical_diversity.csv", index=False)

# --- TF-IDF similarity across all responses per language ---
similarity_rows = []
for lang, subset in df.groupby("language"):
    responses = subset["response"].fillna("").tolist()
    if len(responses) < 2:
        continue
    tfidf = TfidfVectorizer().fit_transform(responses)
    sim_matrix = cosine_similarity(tfidf)
    # mean of upper triangle (excluding diagonal)
    upper = sim_matrix[np.triu_indices_from(sim_matrix, k=1)]
    similarity_rows.append({
        "language": lang,
        "mean_tfidf_cosine": np.mean(upper),
        "median_tfidf_cosine": np.median(upper)
    })
sim_df = pd.DataFrame(similarity_rows)
sim_df.to_csv(OUT_DIR / "tfidf_similarity_summary.csv", index=False)

# --- Visualization ---
for lang in df["language"].unique():
    subset = df[df["language"] == lang]
    plt.figure()
    plt.hist(subset["resp_tokens"].dropna(), bins=15)
    plt.title(f"Response token distribution ({lang})")
    plt.xlabel("Token count")
    plt.ylabel("Frequency")
    plt.savefig(FIG_DIR / f"hist_tokens_{lang}.png")
    plt.close()

print("✅ Analysis complete. Results saved in 'outputs/' folder.")
