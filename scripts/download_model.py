import os
import argparse
from urllib.request import urlretrieve


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def download(url, out_path):
    print(f"Downloading {url} -> {out_path}")
    urlretrieve(url, out_path)
    print("Done")


def main():
    parser = argparse.ArgumentParser(description='Download model artifacts into models/')
    parser.add_argument('--model-url', required=True, help='Public URL to xgboost_model.pkl')
    parser.add_argument('--feature-url', required=True, help='Public URL to feature_extractor.pkl')
    parser.add_argument('--out-dir', default='models')
    args = parser.parse_args()

    ensure_dir(args.out_dir)
    model_path = os.path.join(args.out_dir, 'xgboost_model.pkl')
    feat_path = os.path.join(args.out_dir, 'feature_extractor.pkl')

    download(args.model_url, model_path)
    download(args.feature_url, feat_path)


if __name__ == '__main__':
    main()
