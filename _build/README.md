# サイトの自動生成スクリプト（_build）

科目別ガイド（`/subjects/`）のページを更新するスクリプトをまとめたフォルダです。
このフォルダはサイトには公開されません（`.vercelignore` で除外）。

## いちばん大事なルール

- **公開中のHTMLが正本**です。スクリプトは、各ページの「自分が担当する部分」だけを書き換えます。
- 科目ページを更新したあとは、必ずこの1行を実行します。

```
python3 _build/run.py
```

- 何度実行しても、変更がなければ何も変わりません（冪等）。
- 変更が出るかどうかだけ確かめたいときは、`python3 _build/run.py --check` を使います。0 page(s) would change と出れば、公開中のページとスクリプトが一致しています。

## 実行の順番（run.py が自動で守ります）

| 順番 | スクリプト | 担当する部分 |
|---|---|---|
| 1 | `apsci/ap_content.py` | AP理系の「学ぶ内容」（単元と出題比率の表） |
| 2 | `apsci/subj_content.py` | IB・MYP・IGCSE・A Level・Lower Secondaryの「学ぶ内容」 |
| 3 | `univreq/subj_majors.py` | 「大学の学部で求められる度合い」のグラフ |
| 4 | `apjp/build_apjp.py` | AP 日本語と日本文化のページ全体 |
| 5 | `econ/build_econ.py` | AP ミクロ経済・マクロ経済のページ全体 |
| 6 | `psych/build_psych.py` | AP 心理学のページ全体 |
| 7 | `math/build_math.py` | AP 微積分AB・BC、プレカルキュラスのページ全体 |

4〜7のページは専用のビルダーが持っているため、1の処理は自動でスキップされます。

## 内容を変えたいとき

| 変えたいもの | 編集するファイル |
|---|---|
| AP日本語の文章（他のAIで直した和訳など） | `apjp/edits.json`（`apjp/export_text.py` で書き出し → 編集 → 取り込み） |
| AP日本語の採点基準（英語原文と和訳） | `apjp/rubric_en.py` |
| 経済の単元・例題の採点基準・コツ | `econ/econ_data.py` |
| 心理学の単元・採点基準・コツ | `psych/psych_data.py` |
| 微積分・プレカルキュラスの単元・指示語・コツ | `math/math_data.py` |
| AP理系の単元と出題比率 | `apsci/ap_content.py` の `UNITS` |
| 大学の学部の必須科目データ | `univreq/` のデータ（`uk_data*.py` など） |

編集したら `python3 _build/run.py` を実行し、`git diff` で確認してからアップロードします。

## 使ってはいけないもの

- `subj/build_subjects.py` と `subj/build_services.py` は、ページを一から作り直す古い生成スクリプトです。
  実行すると、その後HTMLに直接加えた修正（料金表、プランカード、文章の修正など）が消えます。
  誤って実行しないよう、`--force` を付けないと動かないようにしています。新しい科目ページを作るときだけ使い、そのあと必ず `run.py` を実行します。

## 公式資料の版

| 科目 | 資料 |
|---|---|
| AP 日本語と日本文化 | Course and Exam Description（Effective Fall 2026） |
| AP ミクロ経済・マクロ経済 | Course and Exam Description（Effective Fall 2026） |
| AP 心理学 | Course and Exam Description（Effective Fall 2025） |
| AP 微積分AB・BC | Course and Exam Description（2027年5月の試験形式を反映した版） |
| AP プレカルキュラス | Course and Exam Description（2027年5月の試験形式を反映した版） |
| AP理系の単元と出題比率 | AP Central / AP Students の各科目ページ（2026-27年度） |

PDFそのものは著作権の都合でこのフォルダに入れていません。
