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

problem = [(int(c) if c != '_' else None) for c in """
_12_
0__2
_222
_2_1
""".replace('\n','')]

def decr(problem, row, column):
    if problem[i := row * 4 + column] != None: problem[i] -= 1

def judge(problem, answer):
    if answer[0]-answer[-1]: return False
    pb = problem[:]
    for p, v in [(p, q-p) for p,q in zip(answer, answer[1:])]:
        r, c = p//5, p%5
        if (r and c and v<0): decr(pb, r-1, c-1)
        if (r and c-4 and v in {-5,1}): decr(pb, r-1, c)
        if (r-4 and c and v in {-1,5}): decr(pb, r, c-1)
        if (r-4 and c-4 and v>0): decr(pb, r, c)
    return len([v for v in pb if v]) == 0

def _solve(problem, retanss, answer):
    if (h:=answer[:-1]) and answer[-1] in h:
        if answer[-1] == answer[0] and judge(problem, answer): retanss.append(answer)
    elif answer:
        f, p = answer[0], answer[-1]
        if p>4 and f<=p-5: _solve(problem, retanss, answer+[p-5])
        if p%5 and f<=p-1: _solve(problem, retanss, answer+[p-1])
        if p%5-4: _solve(problem, retanss, answer+[p+1])
        if p<20: _solve(problem, retanss, answer+[p+5])
    else:
        for p in range(25): _solve(problem, retanss, [p])

def solve(problem):
    anss = []
    _solve(problem, anss, [])
    min_length = min([len(a) for a in anss])
    anss = [a for a in anss if len(a) == min_length]
    return anss

if __name__ == "__main__":
    for answer in solve(problem): print(answer)
