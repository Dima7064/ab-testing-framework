# 🧪 A/B Testing Framework for Product Analysts

A professional Python framework designed to automate the routine tasks of a product analyst during A/B testing.

## 📊 Features

This framework covers 90% of the tasks a product analyst faces in big tech (Yandex, Ozon, T-Bank) when working with experiments:

- **Sample Size & MDE:** Calculate the required sample size and the Minimum Detectable Effect.
- **SRM Check:** Automated Sample Ratio Mismatch validation (randomization check).
- **Frequentist Analysis:** Z-test for conversions and Welch's t-test for continuous metrics (with confidence intervals).
- **CUPED:** Variance reduction based on pre-experiment data (speed up your tests).
- **Multiple Testing:** Bonferroni and FDR (Benjamini-Hochberg) adjustments to protect against p-hacking.
- **CLI Interface:** Run calculations directly from your terminal.

## 🚀 Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/Dima7064/ab-testing-framework.git
cd ab-testing-framework
python -m venv .venv

# For Windows:
.venv\Scripts\activate

# For Mac/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

## 💻 Usage (CLI)

You can use the framework directly from the command line:

**SRM Check:**

```bash
python cli.py srm --control 10000 --treatment 10200
```

**Sample Size Calculation:**

```bash
python cli.py sample-size --baseline 0.10 --mde 0.05
```

**Conversion Analysis (Z-test):**

```bash
python cli.py analyze --control_conv 1000 --control_total 10000 --treatment_conv 1150 --treatment_total 10000
```

## 🧑‍💻 Usage as a Library

```python
from ab_framework.frequentist import analyze_conversion, format_report
from ab_framework.cuped import apply_cuped
import pandas as pd

# 1. Conversion Analysis
result = analyze_conversion(
    control_conversions=100, control_total=1000,
    treatment_conversions=120, treatment_total=1000
)
print(format_report(result))

# 2. Applying CUPED (Variance Reduction)
df = pd.read_csv("data.csv")
df_cuped, metrics = apply_cuped(df, pre_metric_col="pre_gmv", post_metric_col="gmv")
print(f"Variance reduction: {metrics['variance_reduction']:.2%}")
```

## 🧪 Testing

The project is covered with unit tests (pytest). To run them:

```bash
pytest tests/ -v
```
