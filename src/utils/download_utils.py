"""
Download utilities with progress bar support
"""
import os
import urllib.request
from tqdm import tqdm


def download_with_progress(url, filepath):
    """Download file with progress bar"""
    class ProgressBar:
        def __init__(self):
            self.pbar = None

        def __call__(self, block_num, block_size, total_size):
            if not self.pbar:
                self.pbar = tqdm(
                    desc="Downloading",
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                )
            downloaded = block_num * block_size
            if downloaded < total_size:
                self.pbar.update(block_size)
            else:
                self.pbar.close()

    progress = ProgressBar()
    urllib.request.urlretrieve(url, filepath, progress)


def prepare_dataset(dataset_name, data_url, target_dir=None):
    """
    Generic dataset preparation function
    
    Args:
        dataset_name: Name of the dataset for display
        data_url: URL to download the dataset
        target_dir: Directory to download to (default: current directory)
    """
    if target_dir is None:
        target_dir = os.getcwd()
    
    train_file_path = os.path.join(target_dir, "train.txt")
    
    print(f"📁 Dataset directory: {target_dir}")
    print(f"📄 Target file: {train_file_path}")
    print(f"🔖 Dataset: {dataset_name}")

    if not os.path.exists(train_file_path):
        print(f"🔗 Downloading from: {data_url}")
        print("📥 Starting download...")
        
        try:
            download_with_progress(data_url, train_file_path)
            file_size = os.path.getsize(train_file_path) / (1024*1024)  # MB
            print(f"✅ Dataset downloaded successfully! ({file_size:.1f} MB)")
        except Exception as e:
            print(f"❌ Download failed: {e}")
            # Clean up partial download
            if os.path.exists(train_file_path):
                os.remove(train_file_path)
            raise
    else:
        file_size = os.path.getsize(train_file_path) / (1024*1024)  # MB
        print(f"✅ Dataset already exists ({file_size:.1f} MB)")
        print("🚀 Ready to use!")
    
    return train_file_path