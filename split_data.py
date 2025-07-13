# -------------- Imports --------------
import os
import shutil
import random
from pathlib import Path
import argparse
import json

# -------------- Command Line Argument --------------
def parse_args():
    parser = argparse.ArgumentParser("Split YOLO-style dataset into training and validation set")
    parser.add_argument('--input_path', required=True, help='Root path to dataset with images/ and labels/')
    parser.add_argument('--output_path', default='data_split', help='Directory to save split data')
    parser.add_argument('--train_pct', default=0.8, type=float, help='Fraction of data for training (e.g., 0.8 for 80%)')
    return parser.parse_args()

# -------------- Validate inputs --------------
def validate_args(args):
    if not os.path.isdir(args.input_path):
        raise ValueError(f"{args.input_path} is not a valid directory")

    img_path = Path(args.input_path) / 'images'
    label_path = Path(args.input_path) / 'labels'
    if not img_path.exists() or not label_path.exists():
        raise FileNotFoundError("Must contain 'images/' and 'labels/'")
    if not (0.01 <= args.train_pct <= 0.99):
        raise ValueError("Training percentage must be between 0.01 and 0.99")
    return img_path, label_path


# -------------- output paths --------------
def output_paths(output_path):
    structure = {
        'train/images' : output_path / 'train/images',
        'train/labels' : output_path / 'train/labels',
        'validation/images' : output_path / 'validation/images',
        'validation/labels' : output_path / 'validation/labels',
    }

    # -------------- Create output folders --------------
    for path in structure.values():
        path.mkdir(parents=True, exist_ok=True)
    return structure

# -------------- Get all img files --------------
def split_dataset(images_path, train_pct):
    all_images = list(images_path.glob('**/*.[jp][pn]g'))
    random.shuffle(all_images)

    train_count = int(len(all_images) * train_pct)
    return all_images[:train_count], all_images[train_count:]

# -------------- Helper: Move files --------------
def move_files(images_path, labels_path, target_img_dir, target_label_dir):
    for img in images_path:
        lbl = f"{Path(img).stem}.txt"
        label_path = labels_path / lbl

        # Prepare destination paths
        dest_img = target_img_dir / os.path.basename(img)
        dest_lbl = target_label_dir / lbl

        shutil.copy2(img, dest_img)

        if label_path.exists():
            shutil.copy2(label_path, dest_lbl)

def main():
    args = parse_args()
    images_path, labels_path = validate_args(args)
    train_images, val_images = split_dataset(images_path, args.train_pct)

    output_dirs = output_paths(Path(args.output_path))

    # -------------- Split the Dataset --------------
    move_files(train_images, labels_path, output_dirs['train/images'], output_dirs['train/labels'])
    move_files(val_images, labels_path, output_dirs['validation/images'], output_dirs['validation/labels'])

if __name__ == "__main__":
    main()