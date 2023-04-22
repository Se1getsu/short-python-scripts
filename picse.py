# 【内容】
# 高校時代に作った、ピクトセンスで単語を検索するプログラムです。
# 下に設定してある辞書から単語をスクレイピングして集めます。
# クエリの一覧は下にあるコメントを参照してください。

import requests
from bs4 import BeautifulSoup
import copy

WIDTH = 40

# 読み込む辞書IDを設定
dids = tuple()
exec("dids = "
##     #一般・総合・初級
##     "1,2,"
     #一般・総合・中級
     "3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,"
##     #一般・総合・上級
##     "18,19,20,21,22,"
##     #一般・超上級２
##     "8713,"
     #誰でも簡単に書けそうな物
     "13975,"
##     #カスタム
##     ","
)


'''
【クエリ一覧】

5            5文字
あ           ヒント

f あ         "あ"を含むものを検索
if w=="あ"   条件式で検索
g            検索結果適用

：           絞り込み初期化
：：：       終了

'''


# 表示用
def printws(ws:set):
    print('No words.' if len(ws)==0 else 'There are %s words.'%len(ws))
    m = 0
    oup = ""
    for w in ws:
        if m + len(w) < WIDTH:
            oup += w+'　'
            m += len(w)+1
        elif m + len(w) == WIDTH:
            oup += w+'\n'
            m = 0
        else:
            oup += '\n'+w+'　'
            m = len(w)+1
    print(oup+'\n')

# 辞書を読み込む
words = set()

for did in dids:

    # 辞書にアクセスしてスープ取得
    res = requests.get("https://pictsense.com/dic/n%s" % did)
    soup = BeautifulSoup(res.text, "html.parser")

    # 単語の一覧を要素に追加
    elm = soup.select("#words")[0]
    for i in range(1,len(elm)-1):
        words.add(str(elm.contents[i].contents[0]))

    # 辞書名表示
    dname = soup.select("#base > article > h2")[0].contents[0][3:]
    print("\"%s\" has been loaded." % dname)

print("Loaded %s words from %s dictionaries." % (len(words), len(dids)))
print("＝" * WIDTH + '\n')

#【準備完了】



# fw:条件で絞り込んだ単語を保存する
fw = copy.copy(words)
idx = 0

while True:
    
    q = input("Query: ")
    qs = q.split(' ')
    def ql(n:int): return len(qs)==n


    if q=='':
        continue

    # 終了クエリ
    elif q in {":::","：：："}: break


    # リセット
    elif q in {":","："}:
        fw = copy.copy(words)
        idx = 0


    # 検索結果を適用　g
    elif q in {"g", "G"}:
        try: fw = kfw
        except: print("No search results left.")


    # 文字数で絞り込む　sl:int
    elif ql(1) and qs[0].isdecimal():
        sl = int(qs[0])

        # 絞り込みリセット
        fw = copy.copy(words)
        idx = 0
        
        for w in copy.copy(fw):
            if len(w)!=sl: fw.remove(w)
            
        printws(fw)


    # 文字で絞り込む　s:str
    elif ql(1):
        for c in qs[0]:
            
            # w[idx]がcの単語を絞り込む
            for w in copy.copy(fw):
                try:
                    if w[idx] != c: fw.remove(w)
                except IndexError: fw.remove(w)
                
            idx = -idx-1 if idx>=0 else -idx
                
        printws(fw)


    # 任意の条件式を満たすものを検索　if ce:wを用いた条件式
    elif len(qs)>1 and qs[0]=="if":
        ce = q[len("if")+1:]

        kfw = copy.copy(fw)
        for w in fw:
            if not eval(ce): kfw.remove(w)
            
        printws(kfw)


    # 任意の条件式を満たすものを検索　f ss:含む文字列..
    elif len(qs)>1 and qs[0]=="f":
        ss = qs[1:]

        kfw = set()
        for w in fw:
            for s in ss:
                if s in w:
                    kfw.add(w)
                    break
            
        printws(kfw)


    # 無効なクエリ
    else:
        print("Invalid query!")



print("Finished without any exceptions.")










