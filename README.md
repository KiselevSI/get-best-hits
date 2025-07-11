```markdown
# best_hits_wide_polars.py

## Назначение
`best_hits_wide_polars.py` — утилита, которая берёт объединённый TSV-отчёт Bracken,  
сформированный скриптом **`combine_bracken_outputs.py`**, и превращает его в
«широкую» таблицу **sample_id + top1…topN**.  
В каждой колонке `top1…topN` хранится *N* лучших таксонов для образца в формате

```

(TaxonName fraction)

````

---

## Установка

```bash
python -m pip install "polars>=0.20"
````

> Требуется Python ≥ 3.8.

---

## Использование

```bash
python best_hits_wide_polars.py \
  -i <combined_bracken_report.tsv> \
  -o <wide_table.tsv> \
  -n <N>
```

| Опция           | Значение по умолчанию         | Описание                                       |
| --------------- | ----------------------------- | ---------------------------------------------- |
| `-i`, `--input` | `combined_bracken_report.tsv` | Входной TSV от `combine_bracken_outputs.py`    |
| `-o`, `--out`   | `best_hits_wide.tsv`          | Путь к wide-таблице                            |
| `-n`, `--top`   | `5`                           | Сколько лучших таксонов заносить в `top1…topN` |

### Быстрый пример

```bash
# собрали Bracken-файлы в единый TSV
combine_bracken_outputs.py --files *.bracken.tsv \
                           -o combined_bracken_report.tsv

# превращаем в wide-формат, берём 5 лучших хитов
python best_hits_wide_polars.py \
       -i combined_bracken_report.tsv \
       -o best_hits_wide.tsv \
       -n 5
```

---

## Формат входных данных

* **TSV** с табуляцией.
* Названия фракционных столбцов оканчиваются на `.tsv_frac`
  (так их создаёт `combine_bracken_outputs.py`).
* Столбец `name` содержит таксон.

---

## Формат выходных данных

* TSV-таблица.
* Первая колонка: `sample_id` (имя образца без суффикса `.tsv_frac`).
* Далее — `top1…topN`; если таксонов меньше *N*, ячейки заполняются `None`.

### Пример выходной таблицы (`-n 5`)

| sample\_id | top1                      | top2                  | top3                  | top4                  | top5                      |
| ---------- | ------------------------- | --------------------- | --------------------- | --------------------- | ------------------------- |
| sampleA    | (M. tuberculosis 0.83421) | (M. avium 0.09543)    | (M. kansasii 0.04510) | (M. gordonae 0.01526) | None                      |
| sampleB    | (M. gordonae 0.52210)     | (M. kansasii 0.32455) | (M. avium 0.08611)    | (M. szulgai 0.05523)  | (M. tuberculosis 0.01201) |

---

## Часто встречающиеся ошибки

| Сообщение                                 | Причина / решение                                                           |
| ----------------------------------------- | --------------------------------------------------------------------------- |
| `❌ Нет столбцов с суффиксом '.tsv_frac'.` | Входной TSV не похож на вывод `combine_bracken_outputs.py`. Проверьте файл. |
| `FileNotFoundError`                       | Неправильный путь к входному файлу.                                         |


