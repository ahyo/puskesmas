from collections import Counter

file1 = open('diagnosis.txt', 'r')
Lines = file1.readlines()

count = 0
# Strips the newline character
data = []
for line in Lines:
    teks = line.split()
    data.append(teks[1])

res = dict(Counter(data))
print(res)
