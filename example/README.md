# サンプルデータ

このディレクトリには、テキスト分析ツールをテストするためのサンプルデータが含まれています。

## ディレクトリ構造

```
example/
├── config/
│   └── categories_sample.yaml  # カテゴリ定義サンプルファイル
└── input_data_sample.tsv       # 入力データサンプルファイル
```

## サンプルファイルの説明

### 1. input_data_sample.tsv

TSV形式のゲームレビューサンプルデータです。以下の列を含みます：

1. ID - レビューの一意識別子
2. 日付 - レビュー投稿日
3. 著者 - レビュー投稿者
4. レビューテキスト - レビュー本文
5. スコア - 評価スコア（1-5）

### 2. categories_sample.yaml

カテゴリ定義のサンプルYAMLファイルです。以下の構造になっています：

- ゲームカテゴリ定義（game_review_categories）
  - ゲームメカニクス（game_mechanics）
    - コアゲームプレイ（core_gameplay）
    - プログレッション（progression）
  - ビジネスモデル（business_model）
    - ガチャ（gacha）
    - 課金システム（payment）

## 使用方法

1. サンプルファイルを本番環境にコピーします：
   ```
   cp example/config/categories_sample.yaml config/categories.yaml
   cp example/input_data_sample.tsv input_data.tsv
   ```

2. 分析を実行します：
   ```
   uv run run_analyzer.py
   ```

3. 結果は `output/result.csv` と `output/comment_list.tsv` に出力されます。

## カスタマイズ

- `categories.yaml` ファイルを編集して、カテゴリ、サブカテゴリ、キーワードを追加または変更できます。
- 独自の入力データを使用する場合は、`input_data_sample.tsv`と同じ列構造を持つTSVファイルを用意してください。 