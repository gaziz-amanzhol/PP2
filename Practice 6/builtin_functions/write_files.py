# write mode
with open("output.txt", "w") as f:
    f.write("This is a new file\n")
    f.write("Second line\n")

with open("output.txt", "a") as f:
    f.write("Appended line\n")

print("File created and updated")
