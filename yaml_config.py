import yaml
import os
from pathlib import Path
import argparse

parser = argparse.ArgumentParser("Create YAML file for YOLO model")
parser.add_argument('--input_path', required=True, help='Root path to dataset')
parser.add_argument('--output_path', default="", help='Output path to dataset')
args = parser.parse_args()

def create_data_yaml(classes_path, yaml_path, data_root="data"):
    # Ensure classes.txt exists
    if not os.path.exists(classes_path):
        print(f"[ERROR] classes.txt not found")
        return

    # Read class names
    with open(classes_path, "r") as f:
        classes_names = [line.strip() for line in f if line.strip()]

    if not classes_names:
        print("[ERROR] no class names found in classes.txt")
        return

    # create YAML dictionary
    data_yaml = {
        "path": f"{data_root}",
        "train": "train/images",
        "val": "validation/images",
        "numOfClasses": len(classes_names),
        "names": classes_names
    }

    # write to YAML file
    with open(yaml_path, "w") as f:
        yaml.dump(data_yaml, f, sort_keys=False)

    print(f"[INFO] created YAML file at: {yaml_path}")

create_data_yaml(classes_path=Path(args.input_path) / "classes.txt",
                 yaml_path=Path(args.output_path) / "data.yaml",
                 data_root="data")