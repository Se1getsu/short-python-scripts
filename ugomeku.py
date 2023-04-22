# 【内容】
# 色んなマークがCUI画面上をうごめきます。
# 正直言ってキモいです。
# 恐らく、これを書いた時の私は疲れていたのでしょう。
# こんなのを書こうと思った動機が思い出せません。
# iOSのモバイルCの環境だと綺麗に見れますが、PC環境だとアニメーションぽく見えないかもしれません。

import time
import random

SIZE = {'x':77, 'y':41}
#SIZE = {'x':96, 'y':51}
class Point():
	locates = {}
	count = 0
	
	def __init__(self):
		if self.count == (SIZE['x']+1)*(SIZE['y']+1): raise Exception("マップが満杯です。")
		self.num = Point.count
		Point.count += 1
		self.shape = random.choice('●■▼▲◆♥♣★♦♠')
		while True:
			self.x = random.randint(0,SIZE['x'])
			self.y = random.randint(0,SIZE['y'])
			if (self.x,self.y) not in Point.locates: break
		Point.locates[(self.x,self.y)] = self.num
	
	def move(self, dx, dy):
		to_x = max(0,min(SIZE['x'],self.x+dx))
		to_y = max(0,min(SIZE['y'],self.y+dy))
		if (to_x,to_y) not in Point.locates:
			del Point.locates[(self.x,self.y)]
			self.x, self.y = to_x, to_y
			Point.locates[(self.x,self.y)] = self.num

def PrintMap():
	global ps
	oup = '\n　'+'＝'*(SIZE['x']+1)
	for y in range(0,SIZE['y']+1):
		oup += '\nⅡ'
		for x in range(0,SIZE['x']+1):
			if (x,y) in Point.locates:
				oup += '%s'%ps[Point.locates[(x,y)]].shape
			else:
				oup += '　'
		oup += 'Ⅱ'
	oup += '\n　'+'＝'*(SIZE['x']+1)
	print(oup, end='')

ps = [Point() for _ in range(100)]

while True:
	oup = ''
	PrintMap()
	time.sleep(0.05)
	for p in ps:
		p.move(*[random.randint(-1,1) for _ in range(2)])