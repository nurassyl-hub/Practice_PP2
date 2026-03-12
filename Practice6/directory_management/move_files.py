
import shutil
import os

# Task: Move/copy files between directories
if not os.path.exists("test_move.txt"):
    with open("test_move.txt", "w") as f: f.write("Move me")

os.makedirs("destination", exist_ok=True)
shutil.move("test_move.txt", "destination/test_move.txt")
print("File moved to destination/ folder.")
