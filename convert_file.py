from PIL import Image
import argparse
import os
import pillow_heif

# Register HEIC support
pillow_heif.register_heif_opener()

parser = argparse.ArgumentParser("Split YOLO-style dataset into training and validation set")
parser.add_argument('--input_path', required=True, help='Root path to dataset with images/ and labels/')
parser.add_argument('--input_type', required=True, help='File type to change')
parser.add_argument('--output_type', required=True, help='File type to return')
args = parser.parse_args()

input_ext = f".{args.input_type.strip('.').lower()}"
output_ext = f".{args.output_type.strip('.').lower()}"

all_entries = os.listdir(args.input_path)

for file in all_entries:
    root, ext = os.path.splitext(file)
    if ext.lower() == input_ext:
        input_file = os.path.join(args.input_path, file)
        output_file = os.path.join(args.input_path, root + output_ext)

        try:
            print(input_file)
            img = Image.open(input_file)
            img.save(output_file)
            print(f"{file} => {output_file}")
            if os.path.exists(input_file):
                os.remove(input_file)
        except FileNotFoundError:
            print(f"Error: Input file not found at {file}")
        except Exception as e:
            print(f"An error occurred: {e}")