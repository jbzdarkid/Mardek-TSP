import os, re, ast
from PIL import Image

def paste(map, image, x, y, h=1):
	map.paste(image, (x*16, (y+3-h)*16, (x+1)*16, (y+3)*16), image)

def main():
	for file in os.listdir('data'):
		if file == '.DS_Store':
			continue
		debug = False
		print file
		if file == 'frame_211.txt':
			debug = True
		try:
			data = ast.literal_eval(open('data/'+file, 'rb').read())
		except Exception as e:
			print 'Error parsing file', file
			print e
			continue
		tileset = Image.open('tilesets/'+data['tileset']+'.png')
		w, h = tileset.size
		w, h = w/16, h/16
		tiles = [[None for _ in range(h)] for __ in range(w)]
		# First, we parse the tileset.
		# All tiles in columns 0-9 are single-height
		# All tiles in columns 10-19 are double-height
		# Exception: Tiles in row 0 are single-height
		# All tiles in columns 20-29 are triple-height
		for x in range(w):
			for y in range(0, h, 1):
				tiles[x][y] = tileset.crop((x*16, y*16, (x+1)*16, (y+1)*16))
		for x in range(10, min(w, 20)):
			for y in range(1, h, 2):
				tiles[x][y] = tileset.crop((x*16, y*16, (x+1)*16, (y+2)*16))
		for x in range(20, min(w, 30)):
			for y in range(1, h, 3):
				tiles[x][y] = tileset.crop((x*16, y*16, (x+1)*16, (y+3)*16))
		if debug:
			print data['tileset']
			print data['areaname']
		# I extend the map 2 tiles vertically to allow for 2- and 3- tile sprites that are placed on the top row.
		map = Image.new('RGB', (len(data['map'][0])*16, (len(data['map'])+2)*16), 'black')
		# Second, we add map tiles
		for x in range(len(data['map'][0])):
			for y in range(len(data['map'])):
				tileId = data['map'][y][x]
				coords = int(str(tileId)[1:])
				h = int(str(tileId)[0:1])
				_x = coords%10 + (h-1)*10
				_y = coords/10*h + 1
				# Water is handled separately, idk how
				paste(map, tiles[_x][_y], x, y, h)
		# Third, we add sprites
		for sprite in data['A_sprites']:
			if sprite['model'] == 'o_Crystal':
				crystal = Image.open('sprites/obj_Crystal.png').crop((0, 0, 16, 16))
				paste(map, crystal, sprite['x'], sprite['y'])
			elif sprite['model'][:7] == 'BIGDOOR':
				doors = Image.open('sprites/BIGDOORSHEET.png')
				doorno = int(sprite['model'][7])
				door = doors.crop((0, doorno*32, 16, (doorno+1)*32))
				paste(map, door, sprite['x'], sprite['y'], h=2)
			elif sprite['model'][:4] == 'DOOR':
				doors = Image.open('sprites/DOORSHEET.png')
				doorno = int(sprite['model'][4])
				door = doors.crop((0, doorno*16, 16, (doorno+1)*16))
				paste(map, door, sprite['x'], sprite['y'])
		if debug:
			map.show()

if __name__ == '__main__':
	main()
