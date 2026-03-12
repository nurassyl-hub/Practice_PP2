
# Task: Read and print file contents
try:
    with open("sample.txt", "r") as f:
        print("--- File Content ---")
        print(f.read())
except FileNotFoundError:
    print("Run write_files.py first!")
