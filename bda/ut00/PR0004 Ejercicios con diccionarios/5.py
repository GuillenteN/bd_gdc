dict = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4
}
out = {}
for key, value in dict.items():
    out[value] = key

print(out)