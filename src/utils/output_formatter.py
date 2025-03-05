"""
結果出力モジュール
"""
import os
import csv
from typing import Dict, Any, List, TextIO, Tuple


class OutputFormatter:
    """分析結果の出力フォーマットを担当するクラス"""
    
    def __init__(self, output_file: str):
        """
        初期化
        
        Args:
            output_file (str): 出力CSVファイルのパス
        """
        self.output_file = output_file
        
    def print_results(self, results: Dict[str, Dict[str, Any]]) -> None:
        """
        分析結果を標準出力に表示する
        
        Args:
            results (Dict[str, Dict[str, Any]]): カテゴリごとの分析結果
        """
        print("\n===== ゲームストアレビュー解析結果 =====\n")
        
        # カテゴリごとに結果を表示
        for category_key, category_data in results.items():
            category_name = category_data['name']
            comment_count = category_data['comment_count']
            satisfaction_score = category_data['satisfaction_score']
            
            print(f"■ {category_name}")
            print(f"  コメント件数: {comment_count}")
            print(f"  ユーザー満足度スコア: {satisfaction_score:.2f}")
            
            # サブカテゴリの結果を表示
            if 'subcategories' in category_data and category_data['subcategories']:
                print("  サブカテゴリ:")
                for subcategory_key, subcategory_data in category_data['subcategories'].items():
                    subcategory_name = subcategory_data['name']
                    subcategory_comment_count = subcategory_data['comment_count']
                    subcategory_satisfaction_score = subcategory_data['satisfaction_score']
                    
                    if subcategory_comment_count > 0:
                        print(f"    ・{subcategory_name}")
                        print(f"      コメント件数: {subcategory_comment_count}")
                        print(f"      ユーザー満足度スコア: {subcategory_satisfaction_score:.2f}")
            
            print("")
    
    def export_to_csv(self, results: Dict[str, Dict[str, Any]]) -> None:
        """
        分析結果をCSVファイルに出力する
        
        Args:
            results (Dict[str, Dict[str, Any]]): カテゴリごとの分析結果
        """
        # 出力ディレクトリが存在しなければ作成
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        # CSV形式で結果を出力
        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # ヘッダー行を書き込む
            writer.writerow(['カテゴリ', 'サブカテゴリ', 'コメント件数', 'ユーザー満足度スコア'])
            
            # カテゴリごとの結果を書き込む
            for category_key, category_data in results.items():
                category_name = category_data['name']
                comment_count = category_data['comment_count']
                satisfaction_score = category_data['satisfaction_score']
                
                # カテゴリの合計行
                writer.writerow([
                    category_name,
                    '合計',
                    comment_count,
                    f"{satisfaction_score:.2f}"
                ])
                
                # サブカテゴリの行
                if 'subcategories' in category_data:
                    for subcategory_key, subcategory_data in category_data['subcategories'].items():
                        subcategory_name = subcategory_data['name']
                        subcategory_comment_count = subcategory_data['comment_count']
                        subcategory_satisfaction_score = subcategory_data['satisfaction_score']
                        
                        if subcategory_comment_count > 0:
                            writer.writerow([
                                category_name,
                                subcategory_name,
                                subcategory_comment_count,
                                f"{subcategory_satisfaction_score:.2f}"
                            ])
        
        print(f"\nCSVファイルに結果を出力しました: {self.output_file}") 