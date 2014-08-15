# coding: utf-8

import pygame, sys
from enum import Enum
from pygame.locals import * # QUIT, MOUSEMOTION, and K_ESCAPE are defined.
import math, random

# Define Const variables
WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256
COL_INVADERS = 12
ROW_INVADERS = 5
NUM_INVADERS = COL_INVADERS * ROW_INVADERS
NUM_BULLETS = 10

class Objects(Enum):
	MYSHIP = 0
	INVADER = 1
	MISSILE = 2
	BULLET = 3

imageData = [
	"1010010111011011100000011110011100100100001001000011110000011000",
	"1010010101011010101111010011110001011010101001010001100000100100",
	"0000000000011000000110000001100000011000000110000001100000000000",
	"0000000000011000000110000001100000011000000110000001100000000000"
]

# Color Definitions
whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)
blueColor = pygame.Color(0, 0, 255)
redColor = pygame.Color(255, 0, 0)
greenColor = pygame.Color(0, 255, 0)

imageColor = [
	greenColor,
	redColor,
	blueColor,
	whiteColor
]

class Sprite:
	# 8pixelの矩形
	SIZE = 8

	def __init__(self, x, y, id):
		self.objectid = id
		self.x = x
		self.y = y
		self.dx = self.dy = 0

	def move(self):
		self.x += self.dx
		self.y += self.dy
	
	def hit(self, sp):	
		if sp == None:
			return False
		return (self.x <= sp.x <= self.x + Sprite.SIZE or sp.x <= self.x <= sp.x + Sprite.SIZE) and (self.y <= sp.y <= self.y + Sprite.SIZE or sp.y <= self.y <= sp.y + Sprite.SIZE)


def drawSprite(sp):
	if sp == None: return
	img = imageData[sp.objectid.value]
	color = imageColor[sp.objectid.value]
	
	pixArr = pygame.PixelArray(windowSurfaceObj)

	for y in range(Sprite.SIZE):
		for x in range(Sprite.SIZE):
			# 画面に書ききれない部分は、描画しない
			if not (sp.x + x < WINDOW_WIDTH and sp.y + y < WINDOW_HEIGHT):
				continue
			if img[y * Sprite.SIZE + x] == '1':
				pixArr[sp.x + x][sp.y + y] = color
	del pixArr

# pygameの初期化
pygame.init()

# 時計の初期化
fpsClock = pygame.time.Clock()

# window生成
windowSurfaceObj = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Invaders Game presented by Maru.')
	

def init():
	# オブジェクトの生成
	myship = Sprite(WINDOW_WIDTH / 2, int(WINDOW_HEIGHT * 0.8), Objects.MYSHIP)
	missile = None
	invaders = []
	for i in range(ROW_INVADERS):
		for j in range(COL_INVADERS):
			invaders.append(Sprite((WINDOW_WIDTH / COL_INVADERS) * j + Sprite.SIZE / 2, (WINDOW_HEIGHT / (ROW_INVADERS * 2)) * i, Objects.INVADER))
	bullets = []
	for i in range(NUM_BULLETS):
		bullets.append(None)
			 
	# イベントループスタート
	while True:
		# Clear the screen
		windowSurfaceObj.fill(blackColor)
		
		# Event Handling
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_LEFT:
					myship.dx = -1
				elif event.key == K_RIGHT:
					myship.dx = 1
				elif event.key == K_SPACE:
					if missile == None:
						missile = Sprite(myship.x, myship.y, Objects.MISSILE)
						missile.dy = -1
			elif event.type == KEYUP:
				if event.key in (K_LEFT, K_RIGHT):
					myship.dx = 0

					
		# ############
		# 位置の更新
		# ############
		
		# playerの船を動かす
		myship.move()

		# playerのミサイルを動かす
		if missile != None:
			missile.move()
			if missile.y < 0: # ミサイルが画面から出たら
				del missile
				missile = None

		# invadersのミサイルを動かす
		for i in range(NUM_BULLETS):
			if bullets[i] != None:
				bullets[i].move()
				if bullets[i].hit(myship):
					print "My Ship was broken"
					pygame.quit()
					sys.exit()
				if bullets[i].y > WINDOW_HEIGHT:
					bullets[i] = None

		# invadersを動かす
		for i in range(NUM_INVADERS):
			if invaders[i] != None:
				invaders[i].move()
				if invaders[i].hit(missile):
					invaders[i] = None
					continue
				if math.ceil(random.random() * 100) < 10:
					for j in range(NUM_BULLETS):
						if bullets[j] == None:
							bullets[j] = Sprite(invaders[i].x, invaders[i].y, Objects.BULLET)
							bullets[j].dy = 1
							break
		
		# 描画
		drawSprite(myship)
		drawSprite(missile)
		for i in range(NUM_INVADERS):
			drawSprite(invaders[i])
		for i in range(NUM_BULLETS):
			drawSprite(bullets[i])
			
		
		# Draw all objects to the actual screen
		pygame.display.update()
		
		# 30fpsになるまで待つ
		fpsClock.tick(30)

if __name__ == '__main__':
	init()
	
