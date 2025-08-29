# Dataset File Name: train.txt
# Download file from huggingface if file does not exist
import os
import sys

# Add src to path for import
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../src'))
from utils.download_utils import prepare_dataset

# Same directory as this file
cur_path = os.path.dirname(os.path.realpath(__file__))
train_data_url = "https://huggingface.co/datasets/leyanpan/sat-solver/resolve/main/large-500k/SAT_6_10_skewed_large.txt?download=true"

prepare_dataset("SAT 6-10 Skewed State Large", train_data_url, cur_path)
