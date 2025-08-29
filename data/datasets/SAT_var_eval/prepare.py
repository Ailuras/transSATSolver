import os
import sys
from tqdm import tqdm
import urllib.request

# Add src to path for import  
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../src'))
from utils.download_utils import download_with_progress

# Same directory as this file
cur_path = os.path.dirname(os.path.realpath(__file__))
dataset_folder = "num_var_test"
output_folder = cur_path

print(f"📁 Dataset directory: {cur_path}")
print(f"🔖 Dataset: SAT Variable Evaluation Test Set")

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# List of file names to download
file_names = []
for num_var in range(4, 21):
    for condition in ["Random", "Skewed", "Var", "Marginal"]:
        file_name = f"SAT_{num_var}_{condition}_Test.txt"
        file_names.append(file_name)

# Base URL for downloading files
base_url = "https://huggingface.co/datasets/leyanpan/sat-solver/resolve/main/"

# Function to download a file with progress bar
def download_file(file_name):
    file_url = base_url + dataset_folder + "/" + file_name + "?download=true"
    output_path = os.path.join(output_folder, file_name)
    if not os.path.exists(output_path):
        print(f"📥 Downloading {file_name}...")
        try:
            download_with_progress(file_url, output_path)
            file_size = os.path.getsize(output_path) / 1024  # KB
            print(f"✅ {file_name} downloaded ({file_size:.1f} KB)")
        except Exception as e:
            print(f"❌ Failed to download {file_name}: {e}")
            if os.path.exists(output_path):
                os.remove(output_path)
            raise
    else:
        file_size = os.path.getsize(output_path) / 1024  # KB  
        print(f"✅ {file_name} already exists ({file_size:.1f} KB)")

# Download files with overall progress
print(f"📦 Total files to process: {len(file_names)}")
downloaded_count = 0
existing_count = 0

for i, file_name in enumerate(file_names, 1):
    print(f"\n[{i}/{len(file_names)}] Processing {file_name}...")
    output_path = os.path.join(output_folder, file_name)
    if os.path.exists(output_path):
        existing_count += 1
        file_size = os.path.getsize(output_path) / 1024
        print(f"✅ Already exists ({file_size:.1f} KB)")
    else:
        download_file(file_name)
        downloaded_count += 1

print(f"\n🎉 Dataset preparation complete!")
print(f"📊 Summary: {existing_count} files existed, {downloaded_count} files downloaded")
print(f"🚀 Ready to use!")
