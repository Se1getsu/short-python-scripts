# 【内容】
# 高校時代にボットのコマンドで実装した素因数分解プログラムです。
# Python の int の仕様を活かして、とんでもなく大きい数字が入力されても対応できます。
# 様々な素因数分解アルゴリズムを組み合わせて実装しています。
# コマンド実行のために長時間停止してはいけないので、ある程度やってだめそうなら
# 諦めて、割れたところまでの結果を出力します。
#
# 「だよ(｀・∀・´)」は結果が正確であることを表します。
# 「かな(*‘ω‘ *)」はロー法を信用した場合の結果です。
# 「これ以上分解できるかはわかんない(*´･ω･*)」は途中で諦めた結果です。

import time
def sendText(s): print(s)
arg=[""]
kt = time.time()

while True:
    arg[0] = input(">> ")

    kt = time.time()
    #読み取り
    try:N=int(arg[0])
    except:
        sendText("引数が正しく指定されていません")
        continue

    #ロー法
    def gcd(a,b):return gcd(b,a%b) if a%b else b
    def f(n):return (n**2+1)%N
    def factor1(n):
        x=2;y=2;d=1;cnt=1
        while d==1:
            cnt+=1;x=f(x);y=f(f(y));d=gcd(abs(x-y),n)
            if cnt==10**5:raise Exception("Time out!")  # 10**5: 9-10, 10**6: 12-13
        return d

    #試し割り法
    def factor2(n):
        global fcts
        sq=n**0.5
        for i in [2,3,5,7,11,13,17,19,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]:
            if n**0.5>sq:break
            while n%i==0:fctadd(i);n//=i
        if n!=1:fctadd(n)
            
    #素因数を保存する変数
    fcts={}
    def fctadd(n):
        global fcts
        if n in fcts:fcts[n]+=1
        else:fcts[n]=1

    #計算
    def factor(n):
        global rely
        while n!=1:
            if n<=10201:
                factor2(n);break
            else:
                try:
                    fct=factor1(n)
                except Exception as e:
                    fctadd(n);rely[1]=0;return
                else:
                    n//=fct
                    if n==1:rely[0]=0;fctadd(fct)
                    else:factor(fct)
    rely=[1]*2;factor(N)
        

    #結果表示
    def lnum(i):
        s=""
        for c in str(i):s+='⁰¹²³⁴⁵⁶⁷⁸⁹'[int(c)]
        return s
    oup=""
    for k,v in fcts.items():oup+=str(k)+lnum(v)*int(bool(v-1))+" * "
    if rely[1]:sendText(oup[:-3]+(" だよ(｀・∀・´)" if rely[0] else " かな(*‘ω‘ *)"))
    else:sendText(oup[:-3]+" これ以上分解できるかはわかんない(*´･ω･*)")
    print(round(time.time()-kt, 3))
