# coding: utf-8
import random, math
from collections import namedtuple

NUM_ROW = 3
NUM_COL = 5

Rect = namedtuple('Rect', 'x y w h')
Path = namedtuple('Path', 'start end')

COLOR_BLACK = 1
COLOR_RED = 2
COLOR_BLUE = 3

TOP = 1
LEFT = 2
RIGHT = 3
BOTTOM = 4

# color=1 is black. color=2 is red.
class Point(namedtuple('Point', 'x y color')):
	def __new__(cls, x, y, color=COLOR_BLACK):
		return super(Point, cls).__new__(cls, x, y, color)

class DangeonGenerator:
	
	@classmethod
	def GetMap(cls, width, height):
		data = [[0 for x in range(width)] for y in range(height)]
		
		# 部屋の描画
		rooms = cls.getRoomInfo(width, height)
		for room in rooms:
			if room != None:
				for y in range(room.y, room.y + room.h):
					for x in range(room.x, room.x + room.w):
						data[y][x] = 1

        # 通路の描画
		routes = cls.getRouteInfo(rooms, width, height)
		for route in routes:
			for point in route:
				data[point.y][point.x] = point.color
		
		return data
	
	@classmethod
	def getRouteInfo(cls, rooms, width, height):
		paths = []
		# 経路候補を算出
		for i in range(len(rooms) - 1):
			for j in range(i + 1, len(rooms)):
				# (方法1) 部屋の中心を基準に経路を計算する
				paths.append(Path(start=Point(x=rooms[i].x + rooms[i].w / 2, y=rooms[i].y + rooms[i].h / 2), 
							 	  end=Point(x=rooms[j].x + rooms[j].w / 2, y=rooms[j].y + rooms[j].h / 2)))

		# 経路選別
		# (1)長さがhight/2より小さいものだけ残す
		#paths = filter(lambda p: cls.getLength(p) < height / 2, paths)

		
		# (2)線と線が交差しているものは、どちらかまびく
		if len(paths) > 1:
			tmp = []
			for i in range(len(paths) - 1):
				for j in range(i + 1, len(paths)):
					if cls.isCross(paths[i], paths[j]) == True:
						p = paths[i] if cls.getLength(paths[i]) > cls.getLength(paths[j]) else paths[j]
						if p not in tmp: tmp.append(p)
			paths = filter(lambda p: p not in tmp, paths)
		
		# (3)線と長方形が２点で交差しているものは、まびく
		tmp = []
		for p in paths:
			for r in rooms:
				count = 0
				if cls.isCross(p, Path(start=Point(x=r.x, y=r.y), end=Point(x=r.x + r.w, y=r.y))): #上
					count += 1
				if cls.isCross(p, Path(start=Point(x=r.x, y=r.y), end=Point(x=r.x, y=r.y + r.h))): #左
					count += 1 
				if cls.isCross(p, Path(start=Point(x=r.x + r.w, y=r.y), end=Point(x=r.x + r.w, y=r.y + r.h))): #右
					count += 1 
				if cls.isCross(p, Path(start=Point(x=r.x, y=r.y + r.h), end=Point(x=r.x + r.w, y=r.y + r.h))): #下
					count += 1
				if count > 1:
					tmp.append(p) #削除候補
					break
		paths = filter(lambda p: p not in tmp, paths)
		
		
		# pathからrouteに変換
		routes = []
		#for t in tmp:
		#	routes.append(cls.getLine(t.start, t.end, COLOR_RED))		
		for p in paths:
			routes.append(cls.getLine(p.start, p.end, COLOR_BLUE))


		return routes

	@classmethod
	def isCross(cls, path1, path2):
		# 線分path1が、path2を含む直線と交差するか
		ts2 = (path2.start.y - path1.start.y) * (path1.end.x - path1.start.x) + (path1.end.y - path1.start.y) * (path1.start.x - path2.start.x)
		te2 = (path2.end.y - path1.start.y) * (path1.end.x - path1.start.x) + (path1.end.y - path1.start.y) * (path1.start.x - path2.end.x)
		
		# 線分path2が、path1を含む直線と交差するか
		ts1 = (path1.start.y - path2.start.y) * (path2.end.x - path2.start.x) + (path2.end.y - path2.start.y) * (path2.start.x - path1.start.x)
		te1 = (path1.end.y - path2.start.y) * (path2.end.x - path2.start.x) + (path2.end.y - path2.start.y) * (path2.start.x - path1.end.x)			
		return ts1 * te1 < 0 and ts2 * te2 < 0

		
	@classmethod
	def getLength(cls, path):
		return int(((path.start.x - path.end.x)**2 + (path.start.y - path.end.y)**2)**0.5)
		
		
	@classmethod
	def getRoomInfo(cls, width, height):
		rooms = [None for c in range(NUM_COL * NUM_ROW)]
		for r in range(len(rooms)):
			if random.randint(1, 3) == 1:
				t = cls.getRoom(width/NUM_COL, height/NUM_ROW)
				# ローカル座標からグローバル座標に変換
				gx = t.x + (r % NUM_COL) * width / NUM_COL
				gy = t.y + (r // NUM_COL) * height / NUM_ROW
				rooms[r] = Rect(x=gx, y=gy, w=t.w, h=t.h)
		rooms = filter(lambda x: x != None, rooms)
		return rooms

	# 1/5 - 4/5の大きさになるようなrandom rectを返す
	# x, yはローカル座標
	@classmethod	
	def getRoom(cls, width, height):
		maxw = width * 4 / 5
		minw = width / 5
		maxh = height * 4 / 5		
		minh = height / 5		
		w = random.randint(minw, maxw)
		h = random.randint(minh, maxh)
		
		x = (width - w) / 2 - 1 # 配列は0からスタートするため1ひく
		y = (height - h) / 2 - 1 # 配列は0からスタートするため1ひく

		rect = Rect(x=x, y=y, w=w, h=h)
		return rect
		
	@classmethod
	def getLine(cls, start, end, color=COLOR_BLACK):
		data =  cls.line(start, end, [Point(x=start.x, y=start.y, color=color)], color) # TODO pythonの再帰の書き方がよくわからない
		return data
	
	@classmethod	
	def line(cls, start, end, data, color=COLOR_BLACK):
		x = start.x
		y = start.y
		movedParam = -1 # x: 0 , y: 1
		if (x > end.x or x < end.x) and (y > end.y or y < end.y):
			movedParam = random.randint(0, 1)
		elif x > end.x or x < end.x:
			movedParam = 0
		elif y > end.y or y < end.y:
			movedParam = 1
		else:
			return
		
		if movedParam == 0:
			x = x + 1 if x < end.x else x - 1
		elif movedParam == 1:
			y = y + 1 if y < end.y else y - 1
		data.append(Point(x=x, y=y, color=color))
		cls.line(Point(x=x, y=y, color=color), end, data, color)
		return data
		