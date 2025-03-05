"""
ゲームストアレビュー解析メインスクリプト
"""
import os
import sys
from src.data.loader import DataLoader
from src.analyzer.text_analyzer import TextAnalyzer
from src.utils.output_formatter import OutputFormatter


def main():
    """
    メイン実行関数
    """
    # 設定ファイルのパス
    input_file = "input_data.tsv"
    config_file = "config/categories.yaml"
    output_file = "output/result.csv"
    
    try:
        # データの読み込み
        print("レビューデータとカテゴリ設定を読み込んでいます...")
        data_loader = DataLoader(input_file, config_file)
        reviews_df = data_loader.load_reviews()
        config = data_loader.load_categories()
        
        print(f"レビューデータ: {len(reviews_df)}件")
        print(f"カテゴリ数: {len(config['categories'])}個")
        print(f"感情表現単語数: ポジティブ {len(config['sentiment_words'].get('positive', []))}語、ネガティブ {len(config['sentiment_words'].get('negative', []))}語")
        
        # テキスト解析
        print("テキスト解析を実行中...")
        analyzer = TextAnalyzer(config)
        results = analyzer.analyze_reviews(reviews_df)
        
        # 結果出力
        output_formatter = OutputFormatter(output_file)
        output_formatter.print_results(results)
        output_formatter.export_to_csv(results)
        
        print("解析が完了しました。")
        return 0
        
    except Exception as e:
        print(f"エラーが発生しました: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main()) 