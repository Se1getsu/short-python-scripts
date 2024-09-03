# 【内容】
# 縦5点、横5点のスリザーリンクを解くプログラム。
#
# 【例】
# problem = [2,2,None,None,2,2,None,None,None,None,None,None,None,None,None,None]
# answer[0] = [0, 1, 2, 7, 12, 11, 10, 5, 0]
# answer[1] = [0, 5, 10, 11, 12, 7, 2, 1, 0]
#  0--1--2--3--4
#  | 2| 2|  |  |
#  5--6--7--8--9
#  | 2| 2|  |  |
# 10-11-12-13-14
#  |  |  |  |  |
# 15-16-17-18-19
#  |  |  |  |  |
# 20-21-22-23-24

problem = [None if c == '_' else int(c) for c in """
_121
0__2
_222
_2_1
""".replace('\n','')]

# ==== Code ====

def decr(problem, row, column):
    if problem[i := 4*row+column] != None: problem[i] -= 1

def judge(problem, answer):
    if not(pb := problem[:]) or answer[0] != answer[-1]: return False
    for r,c,v in [(p//5, p%5, q-p) for p,q in zip(answer, answer[1:])]:
        if r and c and v<0: decr(pb, r-1, c-1)
        if r and c-4 and v in {-5,1}: decr(pb, r-1, c)
        if r-4 and c and v in {-1,5}: decr(pb, r, c-1)
        if r-4 and c-4 and v>0: decr(pb, r, c)
    return not [v for v in pb if v]

def _solve(problem, retanss, answer):
    if (h := answer[:-1]) and answer[-1] in h:
        if answer[-1] == answer[0] and judge(problem, answer): retanss.append(answer)
    elif answer:
        s,p = answer[0], answer[-1]
        for v,c in (-5, p>4 and s<=p-5),(-1, p%5 and s<=p-1),(1, p%5-4),(5, p<20):
            if c: _solve(problem, retanss, answer+[p+v])
    else:
        for p in range(25): _solve(problem, retanss, [p])

def solve(problem):
    _solve(problem, anss := [], [])
    minl = min(len(a) for a in anss) if anss else 0
    return [a for a in anss if len(a) == minl]

if __name__ == "__main__":
    [*map(print,solve(problem)or["解なし"])]
