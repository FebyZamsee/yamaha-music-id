
from itertools import zip_longest

with open("akunNEW.txt",encoding="utf-8") as f:
    akunlist = f.read().strip().splitlines()
with open("no", encoding="utf-8") as f:
    nomerlist = f.read().strip().splitlines()

akunAll = []

for no,akun in zip_longest(nomerlist,akunlist,fillvalue=""):
    x = akun.split(" ")
    print(x)
    em = x[0]
    pw = x[1]
    akunAll.append(f"\n{em} {pw} {no}")

for x in akunAll:
    with open("result","a") as f:
        f.write(x)