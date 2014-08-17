# coding: utf-8
import pygame, sys
from pygame.locals import * # QUIT, MOUSEMOTION, and K_ESCAPE are defined.
from DangeonGenerator import DangeonGenerator

COLOR_BLACK = 1
COLOR_RED = 2
COLOR_BLUE = 3

NUM_ROW = 3
NUM_COL = 5

# pixel単位
CELL_WIDTH = 100 
CELL_HEIGHT = 100

WINDOW_WIDTH = CELL_WIDTH * NUM_COL
WINDOW_HEIGHT = CELL_HEIGHT * NUM_ROW

whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)
redColor = pygame.Color(255, 0, 0)
blueColor = pygame.Color(0, 0, 255)

pygame.init()
fpsClock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("dungeon viewer")

 # TODO: NUM_COL, NUM_ROWも設定できたほうがよいか
data = DangeonGenerator.GetMap(WINDOW_WIDTH, WINDOW_HEIGHT)

while True:
	window.fill(whiteColor)
	
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				data = DangeonGenerator.GetMap(WINDOW_WIDTH, WINDOW_HEIGHT)
	
	# 描画
	if data != None:
		pixArray = pygame.PixelArray(window)
		
		for y in range(WINDOW_HEIGHT):
			for x in range(WINDOW_WIDTH):
				if data[y][x] == COLOR_BLACK: # TODO 1でいいのか
					pixArray[x][y] = blackColor
				elif data[y][x] == COLOR_RED: #削除候補
					pixArray[x][y] = redColor
				elif data[y][x] == COLOR_BLUE: #削除候補
					pixArray[x][y] = blueColor					
		
		del pixArray
	
	
	pygame.display.update()
	fpsClock.tick(60)




