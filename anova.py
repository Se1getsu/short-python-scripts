# 【内容】
# 2年次必修『統計データ解析基礎』で作成した分散分析プログラム。
# A_{ij} を入力すると
# 総平方和 S_T,  A間平方和 S_A,  誤差平方和 S_E,
# 自由度 φ_T, φ_A, φ_E
# を出力する。

import itertools

def input_data():
    a = []
    while 1:
        s = input('> ')
        if not s: break
        a.append([int(d) for d in s.split()])
    return a

a = input_data()

st, sa, se = [0.]*3
pt, pa, pe = [0]*3

fl = list(itertools.chain.from_iterable(a))
xbb = sum(fl) / len(fl)
for l in a:
    xb = sum(l) / len(l)
    for x in l:
        st += (x-xbb)**2
        sa += (xb-xbb)**2
        se += (x-xb)**2

        pt += 1; pe += 1
    pa += 1; pe -= 1
pt -= 1; pa -= 1

print(f"""
st = {st}
sa = {sa}
se = {se}
pt = {pt}
pa = {pa}
pe = {pe}
""")