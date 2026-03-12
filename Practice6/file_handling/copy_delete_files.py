
import shutil
import os

# Task: Copy and back up files using shutil
if os.path.exists("sample.txt"):
    shutil.copy("sample.txt", "sample_backup.txt")
    print("Backup created: sample_backup.txt")
    
    # Task: Delete files safely
    # os.remove("sample_backup.txt") 
    # print("Backup deleted safely.")
else:
    print("No file to copy. Run write_files.py first.")
