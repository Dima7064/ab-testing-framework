# 🧪 A/B Testing Framework for Product Analysts

Профессиональный Python-фреймворк для автоматизации рутины продуктового аналитика при проведении A/B-тестов.

## 📊 Что внутри?

Фреймворк покрывает 90% задач, с которыми сталкивается аналитик в бигтехе (Яндекс, Ozon, Т-Банк) при работе с экспериментами:

- **Sample Size & MDE:** Расчет необходимого размера выборки и минимального детектируемого эффекта.
- **SRM Check:** Автоматическая проверка Sample Ratio Mismatch (валидность рандомизации).
- **Frequentist Analysis:** Z-test для конверсий и T-test Уэлча для непрерывных метрик (с расчетом доверительных интервалов).
- **CUPED:** Снижение дисперсии на основе предэкспериментальных данных (ускорение тестов).
- **Multiple Testing:** Поправки Бонферрони и FDR (Benjamini-Hochberg) для защиты от p-hacking.
- **CLI Interface:** Возможность запускать расчеты прямо из терминала.

## 🚀 Установка

```bash
git clone https://github.com/ТВОЙ_НИК/ab-testing-framework.git
cd ab-testing-framework
python -m venv .venv
source .venv/bin/activate  # Для Windows: .venv\Scripts\activate
pip install -r requirements.txt

txt
💻 Примеры использования (CLI)
Фреймворк можно использовать прямо из командной строки:

Проверка SRM:
python cli.py srm --control 10000 --treatment 10200

Расчет размера выборки:
python cli.py sample-size --baseline 0.10 --mde 0.05

Анализ конверсии (Z-test):
python cli.py analyze --control_conv 1000 --control_total 10000 --treatment_conv 1150 --treatment_total 10000

🧑‍💻 Использование как библиотеки
from ab_framework.frequentist import analyze_conversion, format_report
from ab_framework.cuped import apply_cuped
import pandas as pd

# 1. Анализ конверсии
result = analyze_conversion(
    control_conversions=100, control_total=1000,
    treatment_conversions=120, treatment_total=1000
)
print(format_report(result))

# 2. Применение CUPED
df = pd.read_csv("data.csv")
df_cuped, metrics = apply_cuped(df, pre_metric_col="pre_gmv", post_metric_col="gmv")

🧪 Тестирование
Проект покрыт юнит-тестами (pytest). Для запуска:
pytest tests/ -v

```
