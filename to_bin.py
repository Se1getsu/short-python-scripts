# 【内容】
# 2年次必修『応用解析』の時に即興で作った 10→2進数 変換プログラム。
# 即興でかなり雑なプログラムになってたので、使いやすさのために少し手を加えた。
# 小数を変換した際に周期を示してくれる。
# 
# 【実行例】
# >> 3.14
# 11.0[01000111101011100001]

def to_bin(inp):

    if '.' not in inp: inp += '.0'
    elif inp.endswith('.'): inp += '0'
    sei, sho = inp.split('.')

    res = bin(int(sei))[2:]
    m = int(sho)
    e = -len(sho)
    if m: res += '.'

    a = {}
    while m not in a:
        a[m] = len(res)

        m *= 2
        if m >= 10**(-e):
            res += '1'
            m -= 10**(-e)
        else:
            res += '0'

    res_a = res[:a[m]]
    res_b = res[a[m]:]

    res = res_a
    if res_b != '0': res += '[' + res_b + ']'

    return res

print('''\
入力された10進数を2進数に変換します。小数もOK。
結果が循環小数の場合、周期を[ ]で示します。
''')
while 1:
    try:
       print(to_bin(input('>> '))+'\n')
    except Exception as e:
       print('Error')
       #raise