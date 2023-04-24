# 【内容】
# プールスケッチ(plsk.net)という、自由にメモを保存できるサイトがあります。
# そのサイトに保存したメモは最終更新から 100日経過 で消される危険があります。
# なので消されるのを防ぐために最終更新日を更新する という目的のプログラムです。
# 下の設定の[2]のオプションを1にすれば、ローカルにバックアップを取ることもできます。
# メモ内に別のメモのURLが貼ってある場合、そのURL先のメモも、メモ化再帰で更新されます。

from bs4 import BeautifulSoup
import datetime
import os
import re
import requests
import sys
import time

class option:
	def __init__(self, length): self.d = [""]*length; self.v = [None]*length
session = requests.Session(); OP = option( 3 )

# ＝＝＝＝＝＝＝＝＝＝＝＝【設定】＝＝＝＝＝＝＝＝＝＝＝＝
s = """\
sample-by-se1getsu	サンプル (タブの後に書いたものはコメントとして扱われる）
#dummy_memo			#で無効化できる
"""
IDLIST = []
for l in s.split('\n'):
	for c in '#\t　': l = l[:l.find(c)] if c in l else l
	if l: IDLIST.append(l)

OP.d[0] = "最終更新日を更新する。"
OP.d[1] = "末尾 _backup を付加したIDにバックアップを保存する。"
OP.d[2] = " ./Archive フォルダにバックアップを保存する。"
OP.v[0] = 1
OP.v[1] = 1
OP.v[2] = 1
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

print("【対象】\n"+ s +"\n【機能】")
for d, v in zip(OP.d, OP.v): print("・" + (d if v else ""))

# URLを開く
def Post(url, data=None, js=False):
    while True:
        try:
            res = session.post(url,data)

            if js:
                res = res.json()
                if not res:
                    print("[!] JSONの読み取りに失敗"); continue
                if js==str: eval("res"+js)
            return res

        except Exception as e:
            print("[!] 読み取りエラー：%s（%s）" % (e.__class__.__name__, e))
            time.sleep(3)


# 読み取る
def Read_plsk(id):
	res = None
	res = Post("http://plsk.net/"+id)
	soup = BeautifulSoup(res.text, 'html.parser')
	try:
	    text = soup.select("#message")[0].contents[0]
	except IndexError:
		return ""
	for k,v in {"&lt;":'<', "&gt;":'>'}.items(): text = text.replace(k,v)
	return text


# 書き込む
def Write_plsk(id, txt):
	url = "http://plsk.net/edit.php"
	date = {"id":id, "txt":txt}
	Post(url,date)


# アーカイブ
def Archive(id, txt):
	with open("%s/%s.txt"%(path, id), "w") as f: f.write(txt)


#更新
def Update_plsk(id):
	global updated
	
	if id in updated: return
	txt = Read_plsk(id)
	updated.add(id)
	
	contain_ids = set(s[len('plsk.net/'):] for s in re.findall('plsk.net\/[-_a-zA-Z0-9]+', txt))
	for cid in contain_ids - updated:
		Update_plsk(cid)
	
	if txt:
		if OP.v[1]: Write_plsk(id+'_backup',txt)
		if OP.v[2]: Archive(id,txt)
		if OP.v[0]:
			Write_plsk(id,txt)
			print("Updated:", id)
		else:
			print("Checked:", id)
	#time.sleep(0.5)


input("\nこの設定で更新します。続行するにはエンターを押して下さい。")
updated = set()

if OP.v[2]:
	dir = "./Archive/" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
	try: os.mkdir(dir)
	except FileExistsError: print("[Error] アーカイブに失敗しました。時間をおいてお試しください。"); sys.exit()
	dir += "/"

for id in IDLIST:
	if OP.v[2]: path = dir+id; os.mkdir(path)
	Update_plsk(id)

print("Conpleted.")