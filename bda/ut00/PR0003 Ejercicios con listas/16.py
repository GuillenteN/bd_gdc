l1 = [ 1, 4, 6, 8, 9]
l2 = [ 3, 4, 6, 9, 12]
res = []
for item in l1:
    if item in l2:
        res.append(item)
print(res)