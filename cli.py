"""CLI (Command Line Interface) для A/B Testing Framework.

Примеры запуска:
    python cli.py srm --control 10000 --treatment 10200
    python cli.py sample-size --baseline 0.10 --mde 0.05
    python cli.py analyze --control_conv 1000 --control_total 10000 --treatment_conv 1150 --treatment_total 10000
"""

import argparse
import sys
from ab_framework.srm import check_srm
from ab_framework.sample_size import calculate_sample_size
from ab_framework.frequentist import analyze_conversion, format_report


def main():
    parser = argparse.ArgumentParser(description="A/B Testing Framework CLI")
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # Команда 1: SRM Check
    parser_srm = subparsers.add_parser("srm", help="Проверка Sample Ratio Mismatch")
    parser_srm.add_argument("--control", type=int, required=True, help="Размер Control группы")
    parser_srm.add_argument("--treatment", type=int, required=True, help="Размер Treatment группы")

    # Команда 2: Sample Size
    parser_ss = subparsers.add_parser("sample-size", help="Расчет размера выборки")
    parser_ss.add_argument("--baseline", type=float, required=True, help="Базовая конверсия (например, 0.10)")
    parser_ss.add_argument("--mde", type=float, required=True, help="Ожидаемый относительный прирост (например, 0.05)")
    parser_ss.add_argument("--alpha", type=float, default=0.05, help="Уровень значимости (по умолчанию 0.05)")
    parser_ss.add_argument("--power", type=float, default=0.80, help="Мощность (по умолчанию 0.80)")

    # Команда 3: Analyze Conversion
    parser_an = subparsers.add_parser("analyze", help="Анализ конверсии (Z-test)")
    parser_an.add_argument("--control_conv", type=int, required=True, help="Конверсии в Control")
    parser_an.add_argument("--control_total", type=int, required=True, help="Всего пользователей в Control")
    parser_an.add_argument("--treatment_conv", type=int, required=True, help="Конверсии в Treatment")
    parser_an.add_argument("--treatment_total", type=int, required=True, help="Всего пользователей в Treatment")

    args = parser.parse_args()

    if args.command == "srm":
        result = check_srm({"control": args.control, "treatment": args.treatment})
        print(f"=== SRM Check ===")
        print(f"Chi2: {result['chi2']:.4f}")
        print(f"p-value: {result['p_value']:.4f}")
        print(result["message"])
        if result["is_srm"]:
            sys.exit(1)  # Возвращаем код ошибки, если SRM сломан

    elif args.command == "sample-size":
        result = calculate_sample_size(
            baseline_rate=args.baseline,
            mde_relative=args.mde,
            alpha=args.alpha,
            power=args.power
        )
        print(f"=== Sample Size Calculation ===")
        print(f"Базовая конверсия: {args.baseline:.2%}")
        print(f"Ожидаемый MDE: {args.mde:.2%}")
        print(f"Требуемый размер выборки на группу: {result['sample_size_per_group']:,}")
        print(f"Общий размер выборки: {result['total_sample_size']:,}")

    elif args.command == "analyze":
        result = analyze_conversion(
            control_conversions=args.control_conv,
            control_total=args.control_total,
            treatment_conversions=args.treatment_conv,
            treatment_total=args.treatment_total
        )
        print("=== A/B Analysis ===")
        print(format_report(result))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
