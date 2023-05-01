# 【内容】
# ランダムな かな を任意の文字数で出力します。
# 多分何かに使ったんだと思いますが忘れました。

import random

KANA = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよ"

while 1:
	n = int(input("\n文字数："))
	print(''.join([ random.choice(KANA) for _ in '*'*n ]))