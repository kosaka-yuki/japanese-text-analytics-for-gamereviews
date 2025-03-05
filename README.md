# ゲームストアレビュー テキスト解析ツール

このプロジェクトは、ゲームのストアレビューを日本語テキスト解析し、ゲーム運営に有効な形で情報を抽出するツールです。

## 機能

- TSVファイル形式のレビューデータを読み込み
- Janomeライブラリを使用した日本語テキスト解析
- カテゴリごとのコメント件数とユーザー満足度スコアの集計
- 結果の標準出力とCSV形式でのファイル出力

## 動作フロー

1. input_data.tsvファイルをpandasフレームワークで読み込む
2. input_data.tsvの4列目（content）がストアレビューのテキストなので、それに対してjanomeでテキスト解析を行う
3. config/categories.yamlに記載されている情報を参照し、カテゴリ別に「コメント件数」「ユーザー満足度スコア」を標準出力する
4. 出力結果はoutput/result.csvとしてCSV形式でファイル出力する

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

## プロジェクト構造

```
.
├── config/                   # 設定ファイル
│   └── categories.yaml       # カテゴリ定義ファイル
├── input_data.tsv            # 入力データファイル
├── output/                   # 出力ディレクトリ
│   └── result.csv            # 解析結果出力ファイル
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
└── README.md                 # このファイル
```

## 技術スタック

- Python 3.8+
- pandas: データフレーム処理
- janome: 日本語テキスト形態素解析
- pyyaml: YAML設定ファイル読み込み
