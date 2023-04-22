# 【内容】
# ナップサック問題(切手問題)の計算用に作ったプログラムです。
# 本体のコードは圧縮されて読めなくなってますね。
# まぁ別にこんなありふれたプログラムを読みたい人はいないでしょうから、
# 展開はしないでおきます。

価格一覧 = 100,40
目標金額 = 550

#計算コード
exec('''P=価格一覧\ndef S(w,r=0,q=[]):\n^if r==len(P)-1:m=w%P[r];n,v=P[r]-m,w//P[r];return (min(m,n),[q+[v],q+[v+1]] if m==n else [q+[v]] if m<n else [q+[v+1]]) if w>0 else (abs(w),[q+[0]])\n^else:\n^^s,t=w,[] \n^^for v in range(w//P[r]+2):\n^^^d,x=S(w-v*P[r],r+1,q+[v]);d=abs(d)\n^^^if d<s:s,t=d,x\n^^^elif d==s:t+=x\n^^return s,t\ny=S(目標金額)[1];exec('print("結果：次の%s通りが見つかりました。\\\\n"%len(y));c=0'+';b,c,z=0,c+1,y[c]\\nfor a,p in zip(P,z):b+=a*p;print("%s円 %s個"%(a,p))\\nprint("合計：%s円\\\\n"%b)'*len(y))'''.replace('^',' '*4))