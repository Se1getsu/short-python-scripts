# 【内容】
# 以下のポストで紹介されていた6手前に置いた自分の印が消えるマルバツゲーム
# https://x.com/sg3lu/status/1810582497719370119?s=61&t=BgVCi1o5sUSRxYLIBmGMwA
# その評価値を求めるプログラムです。結論として、このゲームは13手先手必勝です。
#
# 【操作方法】
# 評価値が高い手がプラスで表示されます。評価値の 最大/最小 は +17/-17 です。
#  1 | 2 | 3
# ---+---+---
#  4 | 5 | 6
# ---+---+---
#  7 | 8 | 9
# bで一手前の状態に戻ります。
# qで終了します。

from itertools import permutations

探索ログ表示 = False

WIN = set()
for t in [
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
    (1, 4, 7),
    (2, 5, 8),
    (3, 6, 9),
    (1, 5, 9),
    (3, 5, 7),
]:
    for s in permutations(t):
        WIN.add(s)

# 存在可能な盤面を全て列挙し、0を代入した辞書を作る
def init_result_keys():
    result = {
        (0, 0, 0, 0, 0, 0): 0
    }

    for i in range(1, 7):
        for s in permutations(range(1,10), i):
            s = tuple([0] * (6 - i) + list(s))
            if s[::2] not in WIN: # 終局しているのに敗者が行動をしている盤面はあり得ないので弾く
                result[s] = 0
    return result

# 既に終局である盤面には -17 の評価をつける
def check_already_win(result):
    for s in result:
        if s[1::2] in WIN: result[s] = -17

# 次の手で 勝ち or 負け が確定する手に + or - の評価をつける
def check_win_lose(result):
    new_result = {}
    for s in result:
        if result[s] != 0: # 既に結果が分かっている状態はスキップ
            new_result[s] = result[s]
            continue
        ps = []
        for a in set(range(1, 10)) - set(s):
            next_s = s[1:] + (a,)
            ps.append(result[next_s])

        min_ps = min(ps)
        if min_ps < 0: # 勝ち -> 相手にとって一番悪い評価値を採用
            if 探索ログ表示: print(1 - min_ps, s)
            new_result[s] = - min_ps - 1
        elif 0 in ps: # 確定していない手がある -> まだ勝ち筋があるかもしれないので保留
            new_result[s] = 0
        else: # 負け確 -> 相手にとって一番悪い評価値を採用
            if 探索ログ表示: print(1 - min_ps, s)
            new_result[s] = - min_ps + 1
    return new_result

# 必勝法が判明したパターンの割合を表示
def print_result_info(result, i):
    not_zero = len([p for p in result.values() if p != 0])
    entire = len(result)
    if 探索ログ表示: print("%d: 判明パターン:% 6d / %d (% 4.2f%%)" % (i, not_zero, entire, not_zero / entire * 100))
    return not_zero

# 探索を行う。
def search():
    result = init_result_keys()
    check_already_win(result)
    print_result_info(result, 0)

    not_zero = 0
    i = 1
    while 1:
        result = check_win_lose(result)
        nz = print_result_info(result, i)
        if nz == not_zero: break
        not_zero = nz
        i += 1

    return result

# 探索結果と棋譜を元に、盤面と評価値を表示する。
def print_board(result, moves):
    s = tuple(moves[-6:])
    p = result[s]
    end = p in (+17, -17)
    oup = f"棋譜: {''.join(map(str, moves[6:]))}\n" if moves[6:] else ""
    if end:
        oup += f"終局です。\n"
    elif p == 0:
        oup += "お互いが最善の手を打ち続けると勝負がつきません。\n"
    else:
        will_win = ["後手(O)", "先手(X)"][((p > 0) - len(moves)) % 2]
        oup += f"あと{16-abs(p)+1}手で{will_win}が勝ちます。\n"

    for a in range(1, 10):
        if a in s:
            oup += [" O ", " X "][(len(moves) - moves[::-1].index(a)) % 2]
        elif (next_s := s[1:] + (a,)) in result:
            oup += "%+3d" % -result[next_s]
        else:
            oup += "   "

        if a in (3, 6):
            oup += "\n---+---+---\n"
        elif a != 9:
            oup += "|"

    print(oup + "\n")

if __name__ == "__main__":
    result = search()
    if 探索ログ表示: print("=" * 16 + "\n")

    moves = [0, 0, 0, 0, 0, 0]
    print_board(result, moves)

    while 1:
        turn = "XO"[len(moves) % 2]
        hand = input(f"{turn}(1-9|b|q)> ")
        if hand == "b": # 一手戻る
            if len(moves) == 6: continue
            moves = moves[:-1]
        elif hand == "q":
            break
        elif hand.isdecimal() and 1 <= int(hand) <= 9:
            hand = int(hand)
            if hand in moves[-6:]: continue
            moves.append(hand)
        else:
            continue

        print()
        print_board(result, moves)
