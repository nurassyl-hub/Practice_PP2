
import os

# Task: Create nested directories
os.makedirs("nested/deep/folder", exist_ok=True)

# Task: List files and folders
print("Contents of current directory:", os.listdir("."))
