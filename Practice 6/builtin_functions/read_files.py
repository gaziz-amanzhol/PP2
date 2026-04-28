# read()
with open("sample.txt", "r") as f:
    content = f.read()
    print("Full content:")
    print(content)

with open("sample.txt", "r") as f:
    line = f.readline()
    print("\nFirst line:")
    print(line)

with open("sample.txt", "r") as f:
    lines = f.readlines()
    print("\nAll lines:")
    print(lines)
