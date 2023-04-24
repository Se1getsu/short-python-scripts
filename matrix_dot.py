﻿# 【内容】
# 行列の内積を計算するコードです。
# 1年生が作ったコードが酷かったので、私なりに作り直してみました。

import numpy as np

def input_matrix(name):
    listX = []
    while True:
        inp = input('%s>> ' % name)
        if inp == '': break
        new_row = inp.split(' ')
        listX.append(new_row)
        if len(listX[-1]) != len(listX[0]):
            raise ValueError()
    
    return np.array(listX, dtype=int)

try:
    a = input_matrix('A')
    b = input_matrix('B'); print()

    print(np.dot(a,b))
    
except Exception:
    #raise
    print('エラー')