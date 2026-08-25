# WWIA Polarity Bias \(v0\.4\.0\)

**World Wide Intelligence Agency – Polarity • Multipolar Matrix • Range of Multipolarity • Threshold Vector**

A complete open\-source intelligence analytics system that scores domestic polarity, builds directed multipolar bias matrices, computes the **Range of Multipolarity** \(`R_C` and `R(S)`\), ranks countries, applies conflict Threshold Vectors, tokenizes intelligence products, and includes gamification \+ a Streamlit dashboard\.

---

## Features

- Domestic polarity score `B_C = μ × (1 + κΠ)`
- Directed multipolar matrix `B_{i → j}`
- **Range of Multipolarity**
  - Country\-level: `R_C = max(B) - min(B)` involving country `C`
  - Cluster\-level: `R(S)` for any group of 3\+ nations
- World ranking by multipolarity range
- Threshold Vector conflict flagging
- Intelligence product tokenization
- Gamification engine \(XP, levels, badges\)
- Interactive Streamlit dashboard

---

## Installation

```bash
git clone https://github.com/pacobaco/wwia-polarity-bias.git
cd wwia-polarity-bias

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -e .
```

---

## Quick Start

### Rank all default countries by Range of Multipolarity

```bash
python -m wwia_polarity.cli --range-rank
```

### Compute range for a specific cluster

```bash
python -m wwia_polarity.cli --cluster-range US,IR,SA,TR,PK
```

### Generate the full multipolar matrix

```bash
python -m wwia_polarity.cli --matrix
```

### Launch the dashboard

```bash
streamlit run src/wwia_polarity/dashboard.py
```

---

## Sample Output

> **Note:** The values below are illustrative sample output for demonstrating the CLI and dashboard format. They are not live intelligence assessments or validated country risk measurements.

### 1\. Range Ranking \(`--range-rank`\)

```json
[
  {
    "rank": 1,
    "country": "US",
    "R_C": 1.18,
    "tier": "Extreme"
  },
  {
    "rank": 2,
    "country": "IR",
    "R_C": 1.15,
    "tier": "Extreme"
  },
  {
    "rank": 3,
    "country": "IL",
    "R_C": 1.09,
    "tier": "Extreme"
  },
  {
    "rank": 4,
    "country": "SA",
    "R_C": 1.02,
    "tier": "Extreme"
  },
  {
    "rank": 5,
    "country": "YE",
    "R_C": 0.91,
    "tier": "High"
  },
  {
    "rank": 6,
    "country": "TR",
    "R_C": 0.87,
    "tier": "High"
  },
  {
    "rank": 7,
    "country": "PK",
    "R_C": 0.84,
    "tier": "High"
  },
  {
    "rank": 8,
    "country": "RU",
    "R_C": 0.79,
    "tier": "High"
  },
  {
    "rank": 9,
    "country": "UA",
    "R_C": 0.76,
    "tier": "High"
  },
  {
    "rank": 10,
    "country": "CN",
    "R_C": 0.71,
    "tier": "High"
  }
]
```

### 2\. Cluster Range \(`--cluster-range US,IR,SA`\)

```json
{
  "cluster": ["US", "IR", "SA"],
  "R(S)": 1.12
}
```

### 3\. Directed Bias Pair \(`--pair US IR`\)

```json
{
  "source": "US",
  "target": "IR",
  "B_ij": -0.82,
  "mu": -0.61,
  "Pi": 0.44,
  "n_posts": 8,
  "status": "ok"
}
```

### 4\. Threshold Vector Flags \(`--threshold`\)

```json
{
  "ongoing": [
    "US-IR",
    "IL-IR",
    "SA-IR",
    "YE-IR",
    "UA-RU"
  ],
  "potential": [
    "US-IL",
    "TR-IR"
  ],
  "details": {
    "US": {
      "breaches": ["t_dom", "t_hot"],
      "B_C": 0.68,
      "Pi": 0.41
    },
    "IR": {
      "breaches": ["t_Pi", "t_hot"],
      "B_C": -0.57,
      "Pi": 0.48
    }
  }
}
```

### 5\. Full Pipeline Demo Output

```text
=== Country Ranges R_C ===
  US: 1.180
  IR: 1.150
  IL: 1.090
  SA: 1.020
  ...

=== World Ranking by Range of Multipolarity ===
{'rank': 1, 'country': 'US', 'R_C': 1.18, 'tier': 'Extreme'}
{'rank': 2, 'country': 'IR', 'R_C': 1.15, 'tier': 'Extreme'}
...

=== Cluster Ranges R(S) ===
US-IR-SA: 1.120
SA-TR-PK-IR: 0.940
```

---

## Project Structure

```text
src/wwia_polarity/
├── formula.py              # Domestic B_C
├── multipolar.py           # Directed matrix
├── multipolar_range.py     # R_C and R(S) metrics
├── ranking.py              # World ranking by range
├── threshold.py            # Conflict Threshold Vector
├── network.py              # Graph metrics
├── gamification.py         # XP / badges engine
├── cli.py                  # Command-line interface
└── dashboard.py            # Streamlit app
```

---

## Configuration

Edit `config.yaml` to change:

- Default country list
- Threshold Vector values \(`t_dom`, `t_Pi`, `t_CP`, `t_hot`\)
- Range tiers \(`extreme`, `high`, `moderate`, …\)
- Embedding model and scoring parameters

---

## Methodological Note

WWIA Polarity Bias is intended as an **OSINT analytics and research framework**\. Scores, rankings, thresholds, and generated flags should be treated as model outputs rather than objective measurements of real\-world political intent, conflict probability, or national behavior\.

Validate inputs, model assumptions, source quality, and thresholds before using outputs in research or operational contexts\.

---

## License

Research / internal intelligence use\.

**Not for operational decision\-making without additional validation\.**

---

**WWIA Polarity Desk**
*Global Influence & Power Projection Division*
**v0\.4\.0 – Range of Multipolarity Release**
