# 【内容】
# 高校時代に掛け算の暗算にハマってて、その時に作ったやつです。
# 無限に2桁×2桁の暗算が練習できます。
# 私は算盤とかやってないので、2桁×2桁だと平均12秒くらいかかります。

import random
import time

def rn():return random.randint(1,9)

print("掛け算練習開始！")

try:
    while True:
        a,b = 0,0
        for _ in range(2): a = a*10 + rn()
        for _ in range(2): b = b*10 + rn()

        time.sleep(1)
        stime = time.time()

        print("・", end='')
        while True:
            
            try:
                ans = int(input("%s × %s = "%(a,b)))
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                ans = -1
                
            if ans == a*b:
                break
            else:
                print("　", end='')

        tm = round(time.time() - stime, 1)
        if tm < 2:
            hk = "Too fast!!!"
        elif tm < 5:
            hk = "Unbelievable!!!"
        elif tm < 10:
            hk = "Excellent!!"
        elif tm < 20:
            hk = "Great!"
        elif tm < 30:
            hk = "Good!"
        else:
            hk = "Too slow!"
        print("%s（%s秒）" % (hk,tm))

except KeyboardInterrupt:
    print("終了します")
    

