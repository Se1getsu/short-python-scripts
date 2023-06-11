# 【内容】
# テンパズルを解くプログラムです。
# 反則技を許可を 1 にしたら、2 と 4 をくっつけて 24 にするとかいう
# 反則技を使ってきます。
# 解が見つからない場合は最も近い近似解を出力します。


#＝＝[config]＝＝=
反則技を許可 = 1
#＝＝＝＝＝＝＝＝=

def fi(v):
	return str(int(v)) if v.is_integer() else str(round(v,4))

def ev(s):
    global v, closest, oup
    try:
        v = round(float(eval(s)),10)

        delta = abs(v-N)
        if delta == 0: return v

        if delta < closest:
            closest = delta
            oup[0] = ''
            return N
        elif delta == closest:
            return N
        else:
            return -114514

    except:
        return -114514

def prnt(s):
	global oup
	s = s.replace('*','*')
	ts = '\t' if len(s)>7 else '\t\t'
	oup[1 if v==N else 0] += '%s%s= %s\n' % (s,ts,fi(v))

def kaijo(n):
	return eval('*'.join(['1']+[str(i+1) for i in range(n)]))

# 並び替え
def func2(a):
    abk = a[:]
    dct = set()
    for i in range(4):
        for j in range(3):
            for k in range(2):
                a = abk[:]
                l = a.pop(i),a.pop(j),a.pop(k),a.pop(0)
                if l not in dct:
                    func(l);dct.add(l)

# 演算子の追加
def func(a):
    opr = list('+-*/')
    if 反則技を許可: opr += ['']
    for k in opr:
        for l in opr:
            for m in opr:
                s=a[0]+k+a[1]+l+a[2]+m+a[3]
                if ev(s)==N:prnt(s)
                
                s='('+a[0]+k+a[1]+')'+l+a[2]+m+a[3]
                if k and ev(s)==N:prnt(s)
                s='('+a[0]+k+a[1]+l+a[2]+')'+m+a[3]
                if (k or l) and ev(s)==N:prnt(s)
                s=a[0]+k+'('+a[1]+l+a[2]+')'+m+a[3]
                if l and ev(s)==N:prnt(s)
                
                s=a[0]+k+'('+a[1]+l+a[2]+m+a[3]+')'
                if (l or m) and ev(s)==N:prnt(s)
                s=a[0]+k+a[1]+l+'('+a[2]+m+a[3]+')'
                if m and ev(s)==N:prnt(s)

                if not(k and l and m): continue

                s='('+a[0]+k+a[1]+')'+l+'('+a[2]+m+a[3]+')'
                if k and m and ev(s)==N:prnt(s)
                s='(('+a[0]+k+a[1]+')'+l+a[2]+')'+m+a[3]
                if ev(s)==N:prnt(s)
                s='('+a[0]+k+'('+a[1]+l+a[2]+'))'+m+a[3]
                if ev(s)==N:prnt(s)
                s=a[0]+k+'(('+a[1]+l+a[2]+')'+m+a[3]+')'
                if ev(s)==N:prnt(s)
                s=a[0]+k+'('+a[1]+l+'('+a[2]+m+a[3]+'))'
                if ev(s)==N:prnt(s)
                

closest = 2147483647
oup = ['','']
a = input('数の一覧 >> ').split(' ')
N = float(input('作りたい数 >> '))

func2(a)

if not oup[1]: oup[1] = 'なし'
print('''
【近似解】
%s
【解】
%s''' % tuple(oup))

