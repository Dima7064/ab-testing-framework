# 🧪 A/B Testing Framework для продуктовых аналитиков

Профессиональная Python-библиотека для автоматизации рутины продуктового аналитика при проведении A/B-тестов.

## 📊 Что внутри?

Фреймворк покрывает 90% задач, с которыми сталкивается аналитик в бигтехе (Яндекс, Ozon, Т-Банк) при работе с экспериментами:

- **Sample Size & MDE:** Расчет необходимого размера выборки и минимального детектируемого эффекта.
- **SRM Check:** Автоматическая проверка Sample Ratio Mismatch (валидность рандомизации).
- **Frequentist Analysis:** Z-test для конверсий и T-test Уэлча для непрерывных метрик (с расчетом доверительных интервалов).
- **CUPED:** Снижение дисперсии на основе предэкспериментальных данных (ускорение тестов).
- **Multiple Testing:** Поправки Бонферрони и FDR (Benjamini-Hochberg) для защиты от p-hacking.
- **CLI Interface:** Возможность запускать расчеты прямо из терминала.

## 🚀 Установка

Склонируйте репозиторий и установите зависимости:

```bash
git clone https://github.com/Dima7064/ab-testing-framework.git
cd ab-testing-framework
python -m venv .venv

# Для Windows:
.venv\Scripts\activate

# Для Mac/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

## 💻 Примеры использования (CLI)

**Проверка SRM:**

```bash
python cli.py srm --control 10000 --treatment 10200
```

**Расчет размера выборки:**

```bash
python cli.py sample-size --baseline 0.10 --mde 0.05
```

**Анализ конверсии (Z-test):**

```bash
python cli.py analyze --control_conv 1000 --control_total 10000 --treatment_conv 1150 --treatment_total 10000
```

## 🧑‍💻 Использование как библиотеки

```python
from ab_framework.frequentist import analyze_conversion, format_report
from ab_framework.cuped import apply_cuped
import pandas as pd

# 1. Анализ конверсии
result = analyze_conversion(
    control_conversions=100, control_total=1000,
    treatment_conversions=120, treatment_total=1000
)
print(format_report(result))

# 2. Применение CUPED (Снижение дисперсии)
df = pd.read_csv("data.csv")
df_cuped, metrics = apply_cuped(df, pre_metric_col="pre_gmv", post_metric_col="gmv")
print(f"Снижение дисперсии: {metrics['variance_reduction']:.2%}")
```

## 🧪 Тестирование

Проект покрыт юнит-тестами (pytest). Для запуска:

```bash
pytest tests/ -v
```
