# 【内容】
# 2年次必修『統計データ解析基礎』
# 回帰分析 の課題を解くために作った即興プログラム

n = 10
xb = 2.66
yb = 15.7
Sxx = 12.564
Sxy = 33.98
Syy = 94.1

bh1 = Sxy/Sxx
bh0 = yb - bh1*xb
mh  = "%f + %fx" % (bh0, bh1)
SR  = Sxy**2/Sxx
Se  = Syy-SR
pR  = 1
pe  = n-2
VR  = SR/pR
Ve  = Se/pe
F0  = VR/Ve
ST  = Syy
R2  = SR/ST

'''
Python script> python
Python 3.7.0 (default, Aug 27 2018, 08:06:50) 
[Clang 9.1.0 (clang-902.0.39.2)] on unknown
Type "help", "copyright", "credits" or "license" for more information.
>>> from test04 import *
>>> bh0+bh1*2.66
15.7
>>> bh0+bh1*4.5
20.676376950015918
>>> 21-bh0+bh1*4.5
24.664597262018464
>>> 21-(bh0+bh1*4.5)
0.3236230499840822
>>> VR
91.90070041388091
>>> Ve
0.27491244826488526
>>> F0
334.2907932831481
>>> R2
0.9766280596586707
'''
