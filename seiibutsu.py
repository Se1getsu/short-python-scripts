# 【内容】
# 完全に自分用ですが、原神の聖遺物の情報入力したら 装備するおすすめのキャラ出してくれるツールです。
# 誰にも合わない場合は ごみです って表示されるので安心して処分(延聖)できます。
# 以下のリンクで使っている様子を確認できます。
# https://dl.dropboxusercontent.com/s/eofc1qlj9vxfyoq/2023-02-15%2012.49.52.mov
# 
# CHARAS には https://gamewith.jp/genshin で調べたキャラ別の適正オプションを載せています。
# 　ただし私が引く可能性があるキャラ・育ててるキャラのしか載せてません。
# has_dict には今装備中の聖遺物のランクを入力し、それ未満のランクの聖遺物は提案しません。

has_dict = {
#   'キャラ': '花羽砂杯冠',
  '煙緋・炎': 'SSSSＳＡＥ',
  '煙緋・楽': 'ＡＳＳＡ　',
      '香菱': 'ＳSSＢＡＳ',
      '行秋': 'ＳSSＡＢＡ', # 杯はＡだがマイナス補正でＢにしている
      '雷電': 'ＡＳＡＢＤ',
      '夜蘭': 'ＳＳＳＳＳ',
  'バーバラ': 'ＡＡＡＳＢ',
  'ベネット': 'ＡＡＢＡＣ',
'スクロース': 'ＡＡＡＡＡ',
  'ティナリ': 'SSＡＡＡＳ',
      '草蛍': 'ＤＡＳＤ　',
    'ノエル': 'ＡＣ　　　',

      '鍾離': '　　Ａ　　',
      '万葉': '　　－－－', # (熟知砂杯冠)
      '綾香': '　　　Ｓ　',
  'ナヒーダ': '　SS－－－', # (熟知砂杯冠)
      '心海': '　　　Ｂ　',
  'ニィロウ': '　Ｓ－－－', # (ＨＰ砂杯冠)
      '宵宮': 'ＡSSＳ　　',
  'ハイゼン': 'ＳSS　　　',
}



RANK_POINT = {'SS': 816, 'Ｓ': 814, 'Ａ': 812, 'Ｂ': 810, 'Ｃ': 808, 'Ｄ': 800, 'Ｅ': 0}
def rank(p):
	if p >= RANK_POINT['SS']:   return 'SS' # 会 で 会率/会ダ 両方揃う
	elif p >= RANK_POINT['Ｓ']: return 'Ｓ' # 1,2,3位 のサブOPが揃う
	elif p >= RANK_POINT['Ａ']: return 'Ａ' # 1,2位 のサブOPのみ
	elif p >= RANK_POINT['Ｂ']: return 'Ｂ'
	elif p >= RANK_POINT['Ｃ']: return 'Ｃ' # 1位 のサブOPのみ
	elif p >= RANK_POINT['Ｄ']: return 'Ｄ' # メインOPのみ
	else: return 'Ｅ'

SERIES = {
	'any': '任意',
	'ai': '愛され少女',
	'um': '海染硨磲',
	'ka': '雷の怒り',
	'ki': '金メッキ',
	'ke': '剣闘士',
	'ky': '旧貴族',
	'st': '逆飛び',
	'sj': '砂上の楼閣',
	'sr': '森林の記憶',
	'sm': 'しめ縄',
	'ss': '辰砂往生録',
	'su': '翠緑の影',
	'se': '千岩牢固',
	'so': '蒼白の炎',
	'cz': '血染め',
	'cr': '沈淪',
	'ha': '華館夢醒形骸記',
	'ho': '炎魔女',
	'hy': '氷風',
	'yu': '悠久',
	'rai': '来歆',
	'rak': '楽園',
	're': '烈火',
	'ga': '楽団',
	'ze': '絶縁',
	'else': 'その他'
}

BUI = '花羽砂杯冠'

STATUS = {
	'kk': '会',
	'h': 'HP',
	'hp': 'HP%',
	'k': '攻',
	'kp': '攻%',
	'b': '防',
	'bp': '防%',
	'kr': '会率',
	'kd': '会ダ',
	'c': 'チ',
	'j': '熟',
	'y': '癒',
	'ho':'炎','mi':'水','ko':'氷','km':'雷','i':'岩','kz':'風','ku':'草','bu':'物理'
}

# 聖遺物クラス
class Seiibutu:
	def __init__(self, seri, idx, main, sub):
		self.seri = seri.split('/') if type(seri) == str else seri
		self.idx = idx
		self.main = main.split('/') if type(main)==str else main
		self.sub = sub.split('/') if type(sub)==str else sub
	
	def __str__(self):
		try:
			main = [STATUS[m] for m in self.main]
			sub = [STATUS[s] for s in self.sub]
		except KeyError:
			return "Error"
		else:
			return "[%s|%s] %s - %s" % ('/'.join(SERIES[s] for s in self.seri), BUI[self.idx], '/'.join(main), '/'.join(sub))


# 何番目のステータスかでポイントを計算
def calc_p(opl, op, mainFlg=False):
	if op in {'kr', 'kd'} and 'kk' in opl: op = 'kk'
	if op not in opl: return 0, -1
	n = opl.index(op)
	p = [8,4,2,1][n] if n < 4 else 1	
	return (100*p if mainFlg else p), n

# キャラクタークラス
class Chara:
	def __init__(self, name, seri, data):
		self.name = name
		self.seri = seri.split('/') if type(seri) == str else seri
		self.data = [Seiibutu('any', i, *s.split()) for i,s in enumerate(data.split('  '))]
		self.nowPoint = [None]*5
		# 杯の第一候補のMSが元素だった場合は、杯以外をseriで固定する
		if self.data[3].main[0] in {'ho','mi','ko','kz','i','km','ku'}:
			for i in [0,1,2,4]: self.data[i].seri = self.seri
		else:
			for i in [0,1]: self.data[i].seri = self.seri
	
	def __str__(self):
		res = "名前：%s\tシリーズ：%s" % (self.name, '/'.join(SERIES[s] for s in self.seri))
		for i in range(5): res += "\n%s：%s" % (BUI[i], self.data[i])
		return res
	
	def has(self, s):
		s = s.replace('SS', '＊').replace('　', 'Ｅ').replace('－', 'Ｅ')
		assert len(s) == 5
		for i,c in enumerate(s):
			assert c in 'ＥＤＣＢＡＳ＊'
			self.nowPoint[i] = RANK_POINT[c.replace('＊', 'SS')]
	
	def p(self, sei):
		p = 0; sb = self.data[sei.idx]
		
		# シリーズ
		if sb.seri[0] != 'any' and sei.seri[0] not in sb.seri: return 0, ''
		
		# メインステータス
		for op in sei.main:
			delta, _ = calc_p(sb.main, op, True)
			p += delta
		
		# サブステータス
		subHave = [False]*len(sb.sub)
		for op in sei.sub:
			delta, idx = calc_p(sb.sub, op)
			if delta:
				if subHave[idx]: delta//=2  #会心系で、会率/会ダともにある場合は2つ目のポイントを半減
				subHave[idx] = True
			p += delta
		
		# サブステが3の場合、希望の残り1つのステータスを添えてreturn
		if len(sei.sub) == 3:
			expp = 0
			for idx in range(len(sb.sub)):
				if not subHave[idx]:
					expp, _ = calc_p(sb.sub, sb.sub[idx]); break
			else:
				return p, ''
			return p, (p+expp, sb.sub[idx])
		else:
			return p, ''

#＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
CHARAS = {
	Chara( '煙緋・炎', 'ho', 'h kk/kp/c  k kk/kp/c  kp/c kk/c/j  ho/kp kd/kr/kp  kr kk/kp/c' ),
	Chara( '煙緋・楽', 'ga', 'h kk/kp/c  k kk/kp/c  kp/c kk/c/j  ho/kp kd/kr/kp  kr kk/kp/c' ),
	Chara( '香菱', 'ze', 'h kk/c/kp  k kk/c/kp  c/kp kk/c/kp  ho kk/c/kp  kk kk/c/kp' ),
	Chara( '行秋', 'ze', 'h c/kk/kp  k c/kk/kp  c kk/kp  mi c/kk/kp  kk c/kk/kp' ),
	Chara( '雷電', 'ze', 'h c/kd/kr  k c/kd/kr  kp/c kd/kr/j  kp/km c/kd/kr  kk c/kp/j' ),
	Chara( '夜蘭', 'ze', 'h kk/hp/c  k kk/hp/c  hp kk/c/h  mi kk/hp/c  kd/kr kk/hp/c' ),
	Chara( 'ベネット', 'ky', 'h kk/kp/c  k kk/kp/c  kp/c kk/kp/c  ho kk/kp/c  kk kk/kp/c' ),
	Chara( 'バーバラ', 'um', 'h hp/c/j/kp  k hp/c/j/kp  hp c/j/kp  mi hp/c/j  y hp/c/j' ),
	Chara( 'スクロース', 'su', 'h j/c/kp  k j/c/kp  j c/kp/kk  j c/kp/kk  j c/kp/kk' ),
	Chara( 'ティナリ', 'sr', 'h kk/j/c  k kk/j/c  j kk/c/kp  ku kk/j/c  kk kk/j/c' ),
	Chara( '草蛍', 'sr', 'h j/kk/c  k j/kk/c  c j/kk/kp  ku/j j/kk/c  kk/j j/kk/c' ),
	Chara( 'ノエル', 'ha', 'h bp/kr/kd  k bp/kr/kd  bp kr/kd/c  i bp/kr/kd  kr/kd bp/kr/kd' ),
	
	Chara( '鍾離', 'se/yu', 'h hp/kk/c  k hp/kk/c  hp kk/c/kp  i hp/kk/c  kr/kd hp/kk/c' ),
	Chara( '万葉', 'su', 'h j/c/kp  k j/c/kp  j c/kp/kk  j c/kp/kk  j c/kp/kk' ),
	Chara( '綾香', 'hy', 'h kk/kp/c  k kk/kp/c  kp kk/c/k  ko kk/kp/c  kd/kr kp/c/k' ),
	Chara( 'ナヒーダ', 'sr', 'h j/kk/kp  k j/kk/kp  j kk/kp/c  j kk/kp/c  j kk/kp/c' ),
	Chara( '心海', 'um', 'h hp/c/j  k hp/c/j  hp c/j  mi hp/c/j  y hp/c/j' ),
	Chara( 'ニィロウ', 'ga', 'h hp/j/c  k hp/j/c  hp j/c  hp j/c  hp j/c' ),
	Chara( '宵宮', 'sm/rai', 'h kk/kp/j  k kk/kp/j  kp kk/j/c  ho kk/kp/j  kd/kr kk/kp/j' ),
	Chara( 'ハイゼン', 'ki', 'h kk/j/c  k kk/j/c  j kk/c/kp  ku kk/j/c  kk kk/j/c' ),
}
for c in CHARAS: c.has(has_dict[c.name])
#＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝


print('【登録中のキャラ】')
for c in CHARAS: print(c)

want_seri = set()
for c in CHARAS: want_seri |= set(c.seri)

print('\n＝＝＝＝＝＝＝＝＝＝＝＝＝＝')
print('☆ 聖遺物判定ツール ☆')
print("ランクはＡ以上を目指しましょう。理想は全てＳ以上で揃えることです。")
while 1:
	
	# シリーズ入力
	print('\n'+' '.join(list(SERIES)[1:]))
	count = 2
	while count:
		seri = input('シリーズ >> ')
		if not seri: count -= 1; continue
		if seri not in SERIES or seri == 'any':
			if seri in ('sh', 'si'):
				print('?> 森林:sr  しめ縄:sm  辰砂往生録:ss')
			elif seri in ('ch', 'ti'):
				print('?> 血染め:cz  沈淪:cr')
			elif seri == 'sa':
				print('?> 逆飛び:st  砂上の楼閣:sj')
			elif seri == 'ra':
				print('?> 来歆:rai  楽園:rak')
			elif seri == 'tu':
				print('?> しめ縄:sm')
			else:
				print('無効なシリーズ')
			continue
		break
	else: continue
	
	# 部位入力
	print('a b c d e')
	count = 2
	while count:
		idx = input('部位 >> ')
		if not idx: count -= 1; continue
		if idx not in list('abcde'): print('無効な部位'); continue
		idx = 'abcde'.index(idx)
		break
	else: continue
	
	# （必要性チェック）
	if idx in {0,1} and seri not in want_seri:
		print('そのシリーズが必要なキャラはいません。'); continue
	
	# メインOP入力
	print(' '.join(list(STATUS)[1:]))
	ss_mis = []    # 誤って入力したサブステのsplitedリストを保存
	if idx == 0:
		print('メイン >> h'); ms = ['h']
	elif idx == 1:
		print('メイン >> k'); ms = ['k']
	else:
		count = 2
		while count:
			ms = input('メイン >> ').split()
			if not ms: count -= 1; continue
			if not set(ms) <= set(STATUS) or 'kk' in ms: print('無効なステータス'); continue
			if len(ms) > 1:
				if len(ms) in {3,4}:
					ss_mis = ms
					print('サブステータスを記憶しました。'); continue
				print('ステータス過剰'); continue
			break
		else: continue
	
	# （必要性チェック）
	sei = Seiibutu(seri, idx, ms, [])
	fuyoFlg = True
	for ch in CHARAS:
		p, _ = ch.p(sei)
		if p:
			fuyoFlg = False
			print("┃%s: %s" % ("　"*(5-len(ch.name))+ch.name, ch.data[idx]))
	if fuyoFlg:
		print('そのメインOPが必要なキャラはいません。')
		continue
	
	# サブOP入力
	count = 2
	while count:
		if ss_mis:
			ss = ss_mis; ss_mis = []
			print('サブ >>', ' '.join(ss))
		else:
			ss = input('サブ >> ').split()
		if not ss: count -= 1; continue
		if not set(ss) <= set(STATUS) or 'kk' in ms: print('無効なステータス'); continue
		if len(ss) < 3: print('ステータス不足'); continue
		if len(ss) > 4: print('ステータス過剰'); continue
		break
	else: continue
	
	# 入力内容確認
	sei = Seiibutu(seri, idx, ms, ss)
	print(); print(sei); print()
	
	# 最低表示ランクを設定
	base_minp = 100
	if idx not in {0,1}: base_minp = 810 if len(sei.sub)==3 else 806
	print("最低表示ランク：%s(%sP)" % (rank(base_minp), base_minp))
	
	
	# 結果表示
	print("＝＝＝＝＝［結果］＝＝＝＝＝", end='')
	gomiFlg = True
	for ch in CHARAS:
		p, exps = ch.p(sei)
		pp = exps[0] if exps else p
		minp = max(base_minp, ch.nowPoint[idx])
		
		if pp >= minp:
			gomiFlg = False
			if exps:
				print("\n【%s→%s】%s - %sP→%sP" % (rank(p), rank(pp), ch.name, p, pp)
				    + ("（現状維持）" if pp == ch.nowPoint[idx] else ""))
				print(ch.data[sei.idx])
				print("※期待：%s" % STATUS[exps[1]])
			else:
				print("\n【%s】%s - %sP" % (rank(p), ch.name, p)
				    + ("（現状維持）" if p == ch.nowPoint[idx] else ""))
				print(ch.data[sei.idx])
		
		# メインOPが、第二候補の場合も表示
		elif pp < 800 and pp+400 >= max(minp,500):
			gomiFlg = False
			d = (8 - p//100)*100
			if exps:
				print("\n〖%s→%s〗%s - %sP→%sP" % (rank(p+d), rank(pp+d), ch.name, p, pp)
				    + ("（現状維持）" if pp == ch.nowPoint[idx] else ""))
				print(ch.data[sei.idx])
				print("※期待：%s" % STATUS[exps[1]])
			else:
				print("\n〖%s〗%s - %sP" % (rank(p+d), ch.name, p)
				    + ("（現状維持）" if p == ch.nowPoint[idx] else ""))
				print(ch.data[sei.idx])
	
	if gomiFlg: print("\nごみです")
	print("＝＝＝＝＝＝＝＝＝＝＝＝＝＝")
		
	
	
	
	
	