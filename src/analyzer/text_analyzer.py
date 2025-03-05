"""
テキスト解析モジュール
"""
from janome.tokenizer import Tokenizer
from typing import Dict, List, Any, Tuple, Set
import pandas as pd
import re
import time


class TextAnalyzer:
    """テキスト解析を担当するクラス"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初期化
        
        Args:
            config (Dict[str, Any]): 設定の辞書（カテゴリー、感情表現、否定表現など）
        """
        self.categories = config['categories']
        self.sentiment_words = config['sentiment_words']
        self.negation_patterns = config['negation_patterns']
        self.category_weights = config['category_weights']
        self.tokenizer = Tokenizer()
        
        # キーワードのキャッシュを作成
        self._prepare_keyword_cache()
        
    def _prepare_keyword_cache(self):
        """キーワードのキャッシュを作成して検索を高速化する"""
        self.category_keywords_cache = {}  # カテゴリごとのキーワードキャッシュ
        
        for category_key, category_data in self.categories.items():
            self.category_keywords_cache[category_key] = {}
            
            if 'subcategories' in category_data:
                for subcategory_key, subcategory_data in category_data['subcategories'].items():
                    # キーワードリストを取得
                    keywords = set()
                    
                    if 'keywords' in subcategory_data:
                        keywords.update(subcategory_data['keywords'])
                    
                    self.category_keywords_cache[category_key][subcategory_key] = keywords
        
    def analyze_reviews(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        レビューテキストを解析してカテゴリごとの統計を集計する
        
        Args:
            df (pd.DataFrame): レビューデータのデータフレーム
        
        Returns:
            Dict[str, Dict[str, Any]]: カテゴリごとの分析結果
        """
        # 結果を格納する辞書
        category_results = {}
        
        # カテゴリとサブカテゴリを初期化
        for category_key, category_data in self.categories.items():
            category_results[category_key] = {
                'name': category_data['name'],
                'comment_count': 0,
                'satisfaction_score': 0,
                'subcategories': {}
            }
            
            if 'subcategories' in category_data:
                for subcategory_key, subcategory_data in category_data['subcategories'].items():
                    category_results[category_key]['subcategories'][subcategory_key] = {
                        'name': subcategory_data['name'],
                        'comment_count': 0,
                        'satisfaction_score': 0,
                    }
        
        # 処理の進捗を表示するための変数
        total_reviews = len(df)
        processed_reviews = 0
        start_time = time.time()
        last_progress_time = start_time
        
        # レビューを1つずつ解析
        for _, row in df.iterrows():
            try:
                # 欠損値や数値型のチェック
                content = str(row['content']) if pd.notna(row['content']) else ""
                
                # スコアが欠損値や文字列の場合は処理をスキップ
                if pd.isna(row['score']):
                    continue
                
                try:
                    score = int(row['score'])
                except (ValueError, TypeError):
                    continue
                
                # 空のレビューはスキップ
                if not content.strip():
                    continue
                
                # レビューテキストを解析し、対応するカテゴリを特定
                matched_categories = self._categorize_review(content)
                
                # 各カテゴリの統計を更新
                for category_key, subcategories in matched_categories.items():
                    if category_key in category_results:
                        # カテゴリ重み付けがある場合は適用
                        weight = self.category_weights.get(category_key, 1.0)
                        
                        # 感情スコアの計算（否定表現を考慮）
                        sentiment_score = self._calculate_sentiment_score(content)
                        
                        # 重み付けされたスコア
                        weighted_score = score * weight + sentiment_score
                        
                        category_results[category_key]['comment_count'] += 1
                        category_results[category_key]['satisfaction_score'] += weighted_score
                        
                        # サブカテゴリの統計を更新
                        for subcategory_key in subcategories:
                            if 'subcategories' in category_results[category_key] and subcategory_key in category_results[category_key]['subcategories']:
                                category_results[category_key]['subcategories'][subcategory_key]['comment_count'] += 1
                                category_results[category_key]['subcategories'][subcategory_key]['satisfaction_score'] += weighted_score
                
                # 進捗状況の更新
                processed_reviews += 1
                current_time = time.time()
                
                # 5秒ごとに進捗を表示
                if current_time - last_progress_time >= 5:
                    progress_percent = (processed_reviews / total_reviews) * 100
                    elapsed_time = current_time - start_time
                    reviews_per_second = processed_reviews / elapsed_time if elapsed_time > 0 else 0
                    
                    print(f"進捗: {processed_reviews}/{total_reviews} ({progress_percent:.1f}%) - {reviews_per_second:.1f}件/秒")
                    last_progress_time = current_time
                
            except Exception as e:
                print(f"レビュー解析中にエラーが発生しました: {e}")
                continue
        
        # 平均満足度スコアを計算
        for category_key, category_data in category_results.items():
            if category_data['comment_count'] > 0:
                category_data['satisfaction_score'] /= category_data['comment_count']
            else:
                category_data['satisfaction_score'] = 0
                
            if 'subcategories' in category_data:
                for subcategory_key, subcategory_data in category_data['subcategories'].items():
                    if subcategory_data['comment_count'] > 0:
                        subcategory_data['satisfaction_score'] /= subcategory_data['comment_count']
                    else:
                        subcategory_data['satisfaction_score'] = 0
        
        # 処理時間の表示
        total_time = time.time() - start_time
        print(f"解析完了: {processed_reviews}件のレビューを {total_time:.1f}秒で処理しました ({processed_reviews/total_time:.1f}件/秒)")
        
        return category_results
    
    def _categorize_review(self, content: str) -> Dict[str, List[str]]:
        """
        レビューテキストをカテゴリに分類する
        
        Args:
            content (str): レビューテキスト
        
        Returns:
            Dict[str, List[str]]: カテゴリごとの該当サブカテゴリのリスト
        """
        # 形態素解析
        try:
            tokens = list(self.tokenizer.tokenize(content))
            token_surfaces = [token.surface for token in tokens]
        except Exception as e:
            print(f"形態素解析中にエラーが発生しました: {e}")
            return {}
        
        # マッチしたカテゴリとサブカテゴリを記録
        matched_categories = {}
        
        # 各カテゴリを検査
        for category_key, category_data in self.categories.items():
            matched_subcategories = []
            
            if 'subcategories' in category_data:
                for subcategory_key, subcategory_data in category_data['subcategories'].items():
                    # キャッシュを使用して高速化
                    if self._match_keywords_cached(content, token_surfaces, category_key, subcategory_key):
                        matched_subcategories.append(subcategory_key)
            
            if matched_subcategories:
                matched_categories[category_key] = matched_subcategories
        
        return matched_categories
    
    def _match_keywords_cached(self, content: str, token_surfaces: List[str], category_key: str, subcategory_key: str) -> bool:
        """
        キャッシュを使用してキーワードマッチングを高速化する
        
        Args:
            content (str): 元のテキスト内容
            token_surfaces (List[str]): 形態素解析されたトークンの表層形のリスト
            category_key (str): カテゴリキー
            subcategory_key (str): サブカテゴリキー
        
        Returns:
            bool: マッチする場合はTrue、それ以外はFalse
        """
        if category_key in self.category_keywords_cache and subcategory_key in self.category_keywords_cache[category_key]:
            keywords = self.category_keywords_cache[category_key][subcategory_key]
            
            # 単語レベルでの検索
            for keyword in keywords:
                if keyword in content:
                    return True
            
            # トークンレベルでの検索（精度向上のため）
            for keyword in keywords:
                if keyword in token_surfaces:
                    return True
        
        return False
    
    def _calculate_sentiment_score(self, content: str) -> float:
        """
        テキストの感情スコアを計算する
        
        Args:
            content (str): レビューテキスト
        
        Returns:
            float: 感情スコア（正の値は肯定的、負の値は否定的）
        """
        score = 0.0
        
        # 否定表現の検出
        has_negation = any(pattern in content for pattern in self.negation_patterns)
        
        # ポジティブワードの検出
        positive_matches = [word for word in self.sentiment_words.get('positive', []) if word in content]
        
        # ネガティブワードの検出
        negative_matches = [word for word in self.sentiment_words.get('negative', []) if word in content]
        
        # 否定表現がある場合、ポジティブとネガティブを反転
        if has_negation:
            score -= len(positive_matches) * 0.2
            score += len(negative_matches) * 0.1
        else:
            score += len(positive_matches) * 0.2
            score -= len(negative_matches) * 0.2
        
        return score 