"""
データ読み込みモジュール
"""
import os
import pandas as pd
import yaml
from typing import Dict, List, Any, Optional, Tuple
import re


class DataLoader:
    """データ読み込みを担当するクラス"""
    
    def __init__(self, input_file: str, config_file: str):
        """
        初期化
        
        Args:
            input_file (str): 入力TSVファイルのパス
            config_file (str): 設定YAMLファイルのパス
        """
        self.input_file = input_file
        self.config_file = config_file
        
    def load_reviews(self) -> pd.DataFrame:
        """
        レビューデータをTSVファイルから読み込む
        
        Returns:
            pd.DataFrame: レビューデータのデータフレーム
        """
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"入力ファイルが見つかりません: {self.input_file}")
        
        # TSVファイルを読み込む（ヘッダーなしを想定、5列目が点数）
        df = pd.read_csv(self.input_file, sep='\t', header=None)
        
        # 最低5列あるか確認
        if df.shape[1] < 5:
            raise ValueError(f"入力ファイルの列数が不足しています：{df.shape[1]}列（最低5列必要）")
        
        # 列名を設定
        column_names = ['id', 'date', 'author', 'content', 'score']
        df.columns = column_names + list(df.columns[5:])  # 5列目以降があれば追加
        
        # scoreを数値型に変換（失敗したら欠損値に）
        df['score'] = pd.to_numeric(df['score'], errors='coerce')
        
        return df
    
    def load_categories(self) -> Dict[str, Any]:
        """
        カテゴリー設定をYAMLファイルから読み込む
        
        Returns:
            Dict[str, Any]: 全設定の辞書（カテゴリー、感情表現、否定表現など）
        """
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"設定ファイルが見つかりません: {self.config_file}")
        
        try:
            # YAMLファイルを読み込む
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 必須キーの確認
            required_keys = ['game_review_categories']
            missing_keys = [key for key in required_keys if key not in config]
            
            if missing_keys:
                raise ValueError(f"設定ファイルに必要なキーがありません: {', '.join(missing_keys)}")
            
            # 設定全体を返す（カテゴリ、感情表現、否定表現など）
            return {
                'categories': config['game_review_categories'],
                'sentiment_words': config.get('sentiment_words', {}),
                'negation_patterns': config.get('negation_patterns', []),
                'category_weights': config.get('category_weights', {})
            }
            
        except yaml.YAMLError as e:
            print(f"YAMLファイルの解析エラー: {e}")
            print("サンプルカテゴリを使用します。")
            # エラーが発生した場合はサンプルカテゴリを返す
            return self._get_sample_config()
    
    def _get_sample_config(self) -> Dict[str, Any]:
        """
        サンプル設定を生成する（YAMLファイルが読み込めない場合のフォールバック）
        
        Returns:
            Dict[str, Any]: サンプル設定
        """
        return {
            'categories': self._get_sample_categories(),
            'sentiment_words': {
                'positive': ['良い', 'いい', '素晴らしい', '楽しい', '面白い'],
                'negative': ['悪い', '最悪', 'つまらない', '難しい', 'バグ']
            },
            'negation_patterns': ['ない', 'ません', 'なかった'],
            'category_weights': {
                'game_mechanics': 1.0,
                'monetization': 1.0
            }
        }
    
    def _get_sample_categories(self) -> Dict[str, Any]:
        """
        サンプルカテゴリ設定を生成する
        
        Returns:
            Dict[str, Any]: サンプルカテゴリ設定
        """
        return {
            'game_mechanics': {
                'name': 'ゲームメカニクス',
                'subcategories': {
                    'core_gameplay': {
                        'name': 'コアゲームプレイ',
                        'keywords': ['バトル', '戦闘', '操作', 'システム', 'ゲームプレイ']
                    }
                }
            },
            'monetization': {
                'name': '課金・マネタイズ',
                'subcategories': {
                    'gacha': {
                        'name': 'ガチャ',
                        'keywords': ['ガチャ', '確率', '課金', '無課金', '有償', '石', 'レア']
                    }
                }
            }
        } 