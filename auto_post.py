# 【内容】
# この記事に貼っている 質問フォームに質問を送信するデモ動画 を
# 撮影するために作ったオートメーションです。Macで動きます。
# https://oucrc.net/articles/h_w5s19w6

import pyautogui as pg
import pyperclip
from time import sleep
        
def type(s):
    pg.keyDown('command')
    for c in s:
        pyperclip.copy(c)
        pg.press('v')
    pg.keyUp('command')

print("start")
pg.moveTo(500, 920)
pg.moveTo(350, 666, 0.2)
for _ in range(3): pg.click()
pg.moveTo(440, 910, 0.2)

sleep(0.2)

type("これはデモです。\nここに質問を入力して、送信ボタンを押すことで質問を送信することができます。")

sleep(0.2)
pg.click()
pg.moveTo(375, 790, 0.2)
sleep(0.2)
pg.click()

print("end")
