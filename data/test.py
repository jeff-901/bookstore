with open("a.txt", "r") as f:
    data = f.read()
with open("a.txt", "w") as f:
    f.write(data)
    f.writelines(["1,2,3\n", "erb\n", "you\n"])
