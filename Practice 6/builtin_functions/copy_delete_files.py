import shutil
import os

# copy file
shutil.copy("sample.txt", "backup.txt")
print("File copied")

if os.path.exists("backup.txt"):
    os.remove("backup.txt")
    print("File deleted")
