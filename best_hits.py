#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
best_hits_wide_polars.py
~~~~~~~~~~~~~~~~~~~~~~~~
Создаёт «широкую» таблицу: sample_id + top1-topN.
Запуск:
    python best_hits_wide_polars.py -i report_only_mycobacterium.tsv -o best_hits_wide.tsv -n 5
"""
import polars as pl
import argparse
from pathlib import Path

def build_row(df: pl.DataFrame, col: str, top_n: int) -> dict:
    """Вернёт dict: {'sample_id': ..., 'top1': '(name frac)', …} для одного *_frac-столбца."""
    sample_id = col.split(".", 1)[0]

    # TOP-N строк по убыванию fraction
    top_hits = (
        df.select(["name", col])
          .sort(col, descending=True)                     # сортировка :contentReference[oaicite:0]{index=0}
          .head(top_n)                                    # взять N строк :contentReference[oaicite:1]{index=1}
    )

    # сформировать список строк "(taxon frac)"
    formatted = [
        f"({row['name']} {row[col]:.5f})"
        for row in top_hits.iter_rows(named=True)
    ]

    # дополняем None, если в образце < N таксонов
    while len(formatted) < top_n:
        formatted.append(None)

    # собираем в словарь: sample_id, top1, top2, …
    row_dict = {"sample_id": sample_id}
    row_dict.update({f"top{i+1}": formatted[i] for i in range(top_n)})
    return row_dict

def main(args):
    df = pl.read_csv(args.input, separator="\t")           # чтение TSV :contentReference[oaicite:2]{index=2}
    frac_cols = [c for c in df.columns if c.endswith(".tsv_frac")]
    if not frac_cols:
        raise SystemExit("❌ Нет столбцов с суффиксом '.tsv_frac'.")

    # строим список строк-словарей
    rows = [build_row(df, col, args.top) for col in frac_cols]

    # превращаем в DataFrame и пишем единым TSV
    wide_df = pl.DataFrame(rows)                           # создание нового DF :contentReference[oaicite:3]{index=3}
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    wide_df.write_csv(args.out, separator="\t")            # запись с табуляцией :contentReference[oaicite:4]{index=4}
    print(f"✔ Сохранён файл: {args.out}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Сформировать wide-таблицу (sample_id + top1-topN) из *_frac столбцов."
    )
    p.add_argument("-i", "--input", default="report_only_mycobacterium.tsv",
                   help="Входной TSV (по умолчанию report_only_mycobacterium.tsv)")
    p.add_argument("-o", "--out",   default="best_hits_wide.tsv",
                   help="Выходной TSV (по умолчанию best_hits_wide.tsv)")
    p.add_argument("-n", "--top",   type=int, default=5,
                   help="Сколько лучших хитов сохранять (по умолчанию 5)")
    args = p.parse_args()
    main(args)
