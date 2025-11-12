import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import re

DATA_ROOT = Path("data")   # hoofdmap van YNTP-Corpus
OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)

def clean_text(t):
    if not isinstance(t, str):
        return ""
    return re.sub(r"\s+", " ", t).strip()

def flatten_json(dataset, file_label, lang):
    rows = []
    for day, entries in dataset.items():
        for i, e in enumerate(entries):
            rows.append({
                "language": lang,
                "file": file_label,
                "day": day,
                "index": i,
                "speaker": e.get("speaker"),
                "message": clean_text(e.get("message")),
                "response": clean_text(e.get("response")),
            })
    return rows

def load_language(lang_folder: Path):
    all_rows = []
    print(f"\n📂 Processing language folder: {lang_folder.name}")
    for js_file in tqdm(sorted(lang_folder.glob("*.json"))):
        with open(js_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        all_rows.extend(flatten_json(data, js_file.name, lang_folder.name))
    return pd.DataFrame(all_rows)

if __name__ == "__main__":
    all_languages = [p for p in DATA_ROOT.iterdir() if p.is_dir()]
    frames = []
    for lang_path in all_languages:
        frames.append(load_language(lang_path))
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(OUT_DIR / "combined_all_languages.csv", index=False)
    print(f"\n✅ Combined dataset saved to {OUT_DIR/'combined_all_languages.csv'} ({len(df)} rows)")
