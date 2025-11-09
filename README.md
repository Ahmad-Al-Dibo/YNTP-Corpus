# YNTP-100: Benchmark Dataset voor Gepersonaliseerde Responsvoorspelling

## Overzicht
De **YNTP-100 dataset** (YouTube Noise Text Patterns) is een zorgvuldig samengestelde benchmarkdataset voor onderzoek naar gepersonaliseerde responsgeneratie en next-token voorspelling. De dataset bevat 100 hoogwaardige voorbeelden met meertalige dekking en is bedoeld om modellen te verbeteren in tekstvoorspelling, conversatie-AI en responspersonalizatie.

---

## Datasetdetails

- **Naam:** YNTP-100
- **Type:** Tekstvoorspelling / Responsgeneratie
- **Omvang:** 100 voorbeelden
- **Taal:** Meertalig (o.a. Engels, Nederlands)
- **Bron:** Verzameld en voorbewerkt uit openbare YouTube-comments en posts
- **Formaat:** JSON / CSV (elke entry bevat context en verwachte respons)

---

## Doelstelling
Het doel van de YNTP-100 dataset is om een gestandaardiseerde benchmark te bieden voor:

- Gepersonaliseerde responsvoorspelling
- Meertalige tekstmodellering
- Evaluatie van next-token voorspellingmodellen
- Onderzoek in conversatie-AI en tekstgeneratie

---

## Gebruik

### Dataset Laden
```python
import json

with open('YNTP-100.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(data[0])
