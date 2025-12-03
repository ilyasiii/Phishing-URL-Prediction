"""
Feature extraction pipeline for phishing URL detection.
Extracts lexical, structural, and text-based features from URLs.
"""
import re
import math
from urllib.parse import urlparse, unquote
from collections import Counter
import numpy as np
import tldextract
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from scipy.sparse import hstack, csr_matrix


class URLLexicalFeatures(BaseEstimator, TransformerMixin):
    """Extract numeric lexical features from URLs."""
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        """
        X: array-like of URL strings
        Returns: numpy array of shape (n_samples, n_features)
        """
        features = []
        for url in X:
            features.append(self._extract_features(url))
        return np.array(features, dtype=np.float32)
    
    def _extract_features(self, url):
        """Extract all lexical features from a single URL."""
        parsed = urlparse(url)
        extracted = tldextract.extract(url)
        
        # Basic lengths
        url_length = len(url)
        hostname = parsed.netloc
        hostname_length = len(hostname)
        path = parsed.path
        path_length = len(path)
        query = parsed.query or ''
        query_length = len(query)
        
        # Token counts
        num_dots = url.count('.')
        num_hyphens = url.count('-')
        num_underscores = url.count('_')
        num_slashes = url.count('/')
        num_questionmarks = url.count('?')
        num_equal = url.count('=')
        num_at = url.count('@')
        num_ampersand = url.count('&')
        num_exclamation = url.count('!')
        num_space = url.count(' ')
        num_tilde = url.count('~')
        num_comma = url.count(',')
        num_plus = url.count('+')
        num_asterisk = url.count('*')
        num_hashtag = url.count('#')
        num_dollar = url.count('$')
        num_percent = url.count('%')
        
        # Count digits and letters
        num_digits = sum(c.isdigit() for c in url)
        num_letters = sum(c.isalpha() for c in url)
        
        # Ratios
        digit_letter_ratio = num_digits / max(num_letters, 1)
        
        # Domain features
        domain = extracted.registered_domain or extracted.domain
        domain_length = len(domain) if domain else 0
        subdomain = extracted.subdomain
        num_subdomains = subdomain.count('.') + 1 if subdomain else 0
        
        # TLD features
        tld = extracted.suffix
        tld_length = len(tld) if tld else 0
        
        # Check for IP address in hostname
        ip_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        has_ip = 1 if ip_pattern.search(hostname) else 0
        
        # Protocol
        is_https = 1 if parsed.scheme == 'https' else 0
        
        # Entropy
        entropy = self._calculate_entropy(url)
        
        # Path tokens
        path_tokens = len([t for t in re.split(r'[/\-_.]', path) if t])
        
        # Suspicious patterns
        has_double_slash_in_path = 1 if '//' in path else 0
        has_at_symbol = 1 if '@' in url else 0
        
        # Query parameters count
        num_params = query.count('=')
        
        return [
            url_length,
            hostname_length,
            path_length,
            query_length,
            num_dots,
            num_hyphens,
            num_underscores,
            num_slashes,
            num_questionmarks,
            num_equal,
            num_at,
            num_ampersand,
            num_exclamation,
            num_space,
            num_tilde,
            num_comma,
            num_plus,
            num_asterisk,
            num_hashtag,
            num_dollar,
            num_percent,
            num_digits,
            num_letters,
            digit_letter_ratio,
            domain_length,
            num_subdomains,
            tld_length,
            has_ip,
            is_https,
            entropy,
            path_tokens,
            has_double_slash_in_path,
            has_at_symbol,
            num_params,
        ]
    
    def _calculate_entropy(self, s):
        """Calculate Shannon entropy of a string."""
        if not s:
            return 0.0
        counts = Counter(s)
        total = len(s)
        entropy = -sum((count / total) * math.log2(count / total) for count in counts.values())
        return entropy
    
    def get_feature_names(self):
        """Return feature names for the lexical features."""
        return [
            'url_length', 'hostname_length', 'path_length', 'query_length',
            'num_dots', 'num_hyphens', 'num_underscores', 'num_slashes',
            'num_questionmarks', 'num_equal', 'num_at', 'num_ampersand',
            'num_exclamation', 'num_space', 'num_tilde', 'num_comma',
            'num_plus', 'num_asterisk', 'num_hashtag', 'num_dollar',
            'num_percent', 'num_digits', 'num_letters', 'digit_letter_ratio',
            'domain_length', 'num_subdomains', 'tld_length', 'has_ip',
            'is_https', 'entropy', 'path_tokens', 'has_double_slash_in_path',
            'has_at_symbol', 'num_params',
        ]


def extract_path_query(urls):
    """Extract path + query from URLs for TF-IDF."""
    result = []
    for url in urls:
        try:
            parsed = urlparse(url)
            path = unquote(parsed.path)
            query = unquote(parsed.query or '')
            combined = path + ' ' + query
            result.append(combined)
        except Exception:
            result.append('')
    return result


def extract_domain(urls):
    """Extract registered domain from URLs for char n-grams."""
    result = []
    for url in urls:
        try:
            extracted = tldextract.extract(url)
            domain = extracted.registered_domain or extracted.domain or ''
            result.append(domain)
        except Exception:
            result.append('')
    return result


def build_feature_pipeline(path_max_features=25000, domain_max_features=10000):
    """
    Build the complete feature extraction pipeline.
    
    Returns:
        sklearn Pipeline that transforms URLs into feature matrix
    """
    # Path/query TF-IDF vectorizer
    path_tfidf = TfidfVectorizer(
        analyzer='word',
        token_pattern=r"(?u)\b[\w-]{2,}\b",
        ngram_range=(1, 2),
        max_features=path_max_features,
        min_df=5,
        sublinear_tf=True,
        lowercase=True,
    )
    
    # Domain character n-grams vectorizer
    domain_tfidf = TfidfVectorizer(
        analyzer='char',
        ngram_range=(3, 5),
        max_features=domain_max_features,
        min_df=5,
        sublinear_tf=True,
        lowercase=True,
    )
    
    # Combine all feature extractors
    feature_union = FeatureUnion([
        ('lexical', URLLexicalFeatures()),
        ('path_tfidf', Pipeline([
            ('extract', FunctionTransformer(extract_path_query, validate=False)),
            ('tfidf', path_tfidf)
        ])),
        ('domain_ngrams', Pipeline([
            ('extract', FunctionTransformer(extract_domain, validate=False)),
            ('tfidf', domain_tfidf)
        ])),
    ])
    
    return feature_union


class URLFeatureExtractor:
    """
    Main feature extractor class that wraps the pipeline.
    Provides fit, transform, and save/load functionality.
    """
    
    def __init__(self, path_max_features=25000, domain_max_features=10000):
        self.pipeline = build_feature_pipeline(path_max_features, domain_max_features)
        self.is_fitted = False
    
    def fit(self, urls, y=None):
        """Fit the feature extraction pipeline on URLs."""
        self.pipeline.fit(urls, y)
        self.is_fitted = True
        return self
    
    def transform(self, urls):
        """Transform URLs into feature matrix."""
        if not self.is_fitted:
            raise ValueError("Feature extractor must be fitted before transform.")
        return self.pipeline.transform(urls)
    
    def fit_transform(self, urls, y=None):
        """Fit and transform in one step."""
        return self.fit(urls, y).transform(urls)
    
    def save(self, filepath):
        """Save the fitted pipeline to disk."""
        import joblib
        if not self.is_fitted:
            raise ValueError("Cannot save unfitted feature extractor.")
        joblib.dump(self, filepath)
    
    @staticmethod
    def load(filepath):
        """Load a fitted pipeline from disk."""
        import joblib
        return joblib.load(filepath)
