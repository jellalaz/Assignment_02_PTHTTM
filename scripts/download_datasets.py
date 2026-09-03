"""
Dataset Download Script for Assignment 02
Downloads the three required Kaggle datasets using kagglehub and organizes them into data/raw/ directories.

Datasets:
1. Diabetes: ghnshymsaini/diabetes-prediction-dataset
2. House Price: chershi/house-price-prediction-dataset-2000-rows
3. E-commerce: nicapotato/womens-ecommerce-clothing-reviews
"""

import os
import shutil
import sys
from pathlib import Path
import kagglehub
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASETS = [
    {
        "name": "Diabetes Prediction Dataset",
        "slug": "ghnshymsaini/diabetes-prediction-dataset",
        "dest_dir": PROJECT_ROOT / "data" / "raw" / "diabetes",
        "app": "Application 1 — Diabetes"
    },
    {
        "name": "House Price Prediction Dataset",
        "slug": "chershi/house-price-prediction-dataset-2000-rows",
        "dest_dir": PROJECT_ROOT / "data" / "raw" / "house_price",
        "app": "Application 2 — House Price"
    },
    {
        "name": "Women's E-Commerce Clothing Reviews",
        "slug": "nicapotato/womens-ecommerce-clothing-reviews",
        "dest_dir": PROJECT_ROOT / "data" / "raw" / "ecommerce",
        "app": "Application 3 — E-Commerce"
    }
]


def download_all():
    print(f"Using Python: {sys.executable}")
    print("=" * 70)
    print("Starting Kaggle Dataset Acquisition for Assignment 02...")
    print("=" * 70)

    summary = []

    for item in DATASETS:
        print(f"\n[{item['app']}]")
        print(f"Dataset: {item['name']}")
        print(f"Kaggle Slug: {item['slug']}")
        dest_dir = item["dest_dir"]
        dest_dir.mkdir(parents=True, exist_ok=True)

        try:
            print(f"Downloading via kagglehub.dataset_download('{item['slug']}')...")
            downloaded_path = kagglehub.dataset_download(item["slug"])
            print(f"Downloaded to cache: {downloaded_path}")

            # Copy all files from downloaded folder into dest_dir
            src_path = Path(downloaded_path)
            csv_files = []
            for file_path in src_path.glob("**/*"):
                if file_path.is_file():
                    target_file = dest_dir / file_path.name
                    shutil.copy2(file_path, target_file)
                    print(f"  -> Copied to: {target_file} ({target_file.stat().st_size:,} bytes)")
                    if target_file.suffix.lower() == ".csv":
                        csv_files.append(target_file)

            # Inspect primary CSV
            if csv_files:
                primary_csv = sorted(csv_files, key=lambda f: f.stat().st_size, reverse=True)[0]
                df = pd.read_csv(primary_csv)
                print(f"  Verified CSV: {primary_csv.name}")
                print(f"  Shape: {df.shape} (rows: {df.shape[0]}, cols: {df.shape[1]})")
                print(f"  Columns: {list(df.columns)}")
                summary.append({
                    "app": item["app"],
                    "slug": item["slug"],
                    "csv": primary_csv.name,
                    "rows": df.shape[0],
                    "cols": df.shape[1],
                    "status": "SUCCESS"
                })
            else:
                summary.append({
                    "app": item["app"],
                    "slug": item["slug"],
                    "csv": "None",
                    "rows": 0,
                    "cols": 0,
                    "status": "NO_CSV_FOUND"
                })

        except Exception as e:
            print(f"  ERROR downloading {item['slug']}: {e}")
            summary.append({
                "app": item["app"],
                "slug": item["slug"],
                "csv": "None",
                "rows": 0,
                "cols": 0,
                "status": f"FAILED: {e}"
            })

    print("\n" + "=" * 70)
    print("DATASET ACQUISITION SUMMARY:")
    print("=" * 70)
    for s in summary:
        print(f"• {s['app']}: {s['status']} | CSV: {s['csv']} | Shape: ({s['rows']}, {s['cols']})")

    return summary


if __name__ == "__main__":
    download_all()
