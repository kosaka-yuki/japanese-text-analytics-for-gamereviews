# ゲームストアレビュー テキスト解析ツール

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

このプロジェクトは、ゲームのストアレビューを日本語テキスト解析し、ゲーム運営に有効な形で情報を抽出するツールです。

## 機能

- TSVファイル形式のレビューデータを読み込み（テキストおよび点数）
- Janomeライブラリを使用した日本語テキスト解析
- カテゴリごとのコメント件数、平均点数、ユーザー満足度スコアの集計
- 結果の標準出力とCSV形式でのファイル出力（Shift-JISエンコーディング）
- サブカテゴリごとのコメント一覧をTSV形式で出力

## 動作フロー

1. input_data.tsvファイルをpandasフレームワークで読み込む
   - 1列目: ID
   - 2列目: 日付
   - 3列目: レビュー投稿者
   - 4列目: レビューテキスト
   - 5列目: ストアレビューの点数（星の数）
2. input_data.tsvの4列目（content）がストアレビューのテキストなので、それに対してjanomeでテキスト解析を行う
3. config/categories.yamlに記載されている情報を参照し、カテゴリ別に「コメント件数」「平均点数」「ユーザー満足度スコア」を標準出力する
4. 出力結果はoutput/result.csv（Shift-JIS）としてCSV形式でファイル出力する
5. カテゴリとサブカテゴリごとのコメント一覧をoutput/comment_list.tsv（UTF-8）としてTSV形式で出力する

## インストール

必要なライブラリをインストールします。

```
pip install pandas janome pyyaml
```

## 使用方法

以下のコマンドでツールを実行します。

```
python run_analyzer.py
```


### サンプルデータの利用

プロジェクトにはサンプルデータが含まれています。以下の手順でサンプルデータを使用できます：

```
# サンプル設定ファイルをコピー
cp example/config/categories_sample.yaml config/categories.yaml
# サンプル入力データをコピー
cp example/input_data_sample.tsv input_data.tsv
# 解析を実行
python run_analyzer.py
```

詳細な情報は `example/README.md` を参照してください。

## プロジェクト構造

```
.
├── config/                   # 設定ファイル
│   └── categories.yaml       # カテゴリ定義ファイル
├── example/                  # サンプルデータディレクトリ
│   ├── config/               # サンプル設定ファイル
│   │   └── categories_sample.yaml  # サンプルカテゴリ定義
│   ├── input_data_sample.tsv # サンプル入力データ
│   └── README.md             # サンプルデータの説明
├── input_data.tsv            # 入力データファイル
├── output/                   # 出力ディレクトリ
│   ├── result.csv            # 解析結果出力ファイル（Shift-JIS）
│   └── comment_list.tsv      # コメント一覧ファイル（UTF-8）
├── src/                      # ソースコード
│   ├── analyzer/             # テキスト解析モジュール
│   │   ├── __init__.py
│   │   └── text_analyzer.py  # テキスト解析クラス
│   ├── data/                 # データ処理モジュール
│   │   ├── __init__.py
│   │   └── loader.py         # データ読み込みクラス
│   ├── utils/                # ユーティリティモジュール
│   │   ├── __init__.py
│   │   └── output_formatter.py # 出力フォーマッタクラス
│   ├── __init__.py
│   └── main.py               # メイン実行スクリプト
├── run_analyzer.py           # 実行スクリプト
├── pyproject.toml            # プロジェクト設定ファイル
├── LICENSE                   # MITライセンスファイル
└── README.md                 # このファイル
```

## 出力ファイル形式

### result.csv（Shift-JIS）
- カテゴリ: カテゴリ名
- サブカテゴリ: サブカテゴリ名（カテゴリの集計行は「合計」）
- コメント件数: 該当するコメントの数
- 平均点数: 該当するコメントの平均ストア評価点数（1〜5）
- ユーザー満足度スコア: 計算されたユーザー満足度スコア

### comment_list.tsv（UTF-8）
- カテゴリ: カテゴリ名
- サブカテゴリ: サブカテゴリ名
- ストア点数: レビューのストア評価点数（1〜5）
- コメント: レビューのテキスト内容

## 技術スタック

- Python 3.8+
- pandas: データフレーム処理
- janome: 日本語テキスト形態素解析
- pyyaml: YAML設定ファイル読み込み

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)のもとで公開されています。詳細は[LICENSE](LICENSE)ファイルをご覧ください。
