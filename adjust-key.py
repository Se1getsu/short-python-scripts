# 【内容】
# ライアーで弾けるようにピッチを合わせるプログラムです。
# この調なら半音いくつ下げれば弾ける！とか分かる人には不要なプログラムです。
# note_name に弾きたい曲の音階を書きます。低ド=0, 低ド♯=1, 低レ=2, ...
# lyre はスメールで貰える方のライアーです。kotoは璃月で売ってるやつです。

register = {
"lyre": [ 0, 2, 3, 5, 7, 9,10,
         12,14,15,17,19,21,22,
         24,25,27,29,31,32,34 ],
"koto": [ 0, 2, 4, 5, 7, 9,11,
         12,14,16,17,19,21,23,
         24,26,28,29,31,33,35 ]
}
note_name = """
ど れ み ふ そ ら し
ド レ ミ フ ソ ラ シ
ﾄﾞ ﾚ ﾐ ﾌｧ ｿ ﾗ ｼ
""".split()


score = """\
15 10 15 8 13 17 25 20 22
17 18 20 18 20 13 17 18 20 17 18
"""


def name(inst, p):
	return note_name[register[inst].index(p)]

print("【結果】")
tones = {int(s) for s in score.split()}
i = -1-min(tones); res = []
while max(tones)+i < 36:
	i += 1
	if min(tones)+i < 0: continue
	okFlg = {inst: True for inst in register.keys()}
	
	for t in tones:
		for inst, regi in register.items():
			if t+i not in regi: okFlg[inst] = False
	
	for inst, flg in okFlg.items():
		if flg:
			res.append((inst, i))
			print("%2d: %s %s-%s (%+i)" % (
					len(res),
					inst,
					name(inst, min(tones)+i),
					name(inst, max(tones)+i),
					i
				))

print()
for num, (inst, i) in enumerate(res):
	print("【No.%s】" % (num+1))
	s = score
	for j in range(21)[::-1]:
		p = register[inst][j]
		s = s.replace(str(p-i), name(inst, p))
	print(s)