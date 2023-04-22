# 【内容】
# 下記サイトにて公開している「フィア問実践編」の２問目を作った時の
# 個人的な回答です。さらなる高速化の余地は多大にあると思います。
# https://bokeshi.simdif.com/problems.html

import time

start = time.time()

for n in range(10000,100000):
    ln = [int(c) for c in str(n)]
    
    for m in range(int(ln[0]*10**8/n),10000):
        lm = [int(c) for c in str(m)]

        k=ln[0]*10**8
        for i in range(4): k += ln[i+1]*lm[i] * 10**(6-2*i)
        
        if n*m==k: print('%s × %s = %s' % (n,m,k))

print(time.time()-start) # 8分25秒


##import time
##
##start = time.time()
##
##for n in range(10000,100000):
##    ln = [int(c) for c in str(n)]
##    
##    for m in range(int(ln[0]*10**8/n+1),10000):
##        lm = [int(c) for c in str(m)]
##
##        k = str(ln[0])
##        for i in range(4):k += '%02d' % (ln[i+1]*lm[i])
##        
##        if n*m==int(k): print('%s × %s = %s' % (n,m,k))
##
##print(time.time()-start) # 8分52秒
