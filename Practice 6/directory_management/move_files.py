import shutil
import os

os.makedirs("source", exist_ok=True)
os.makedirs("destination", exist_ok=True)

with open("source/test.txt", "w") as f:
    f.write("test content")

shutil.move("source/test.txt", "destination/test.txt")
print("File moved")
