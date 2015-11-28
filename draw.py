import os, re, ast, json, math
from PIL import Image
def main():
	for root, dirs, files in os.walk('maps'):
		for file in files:
			debug = False
			print file
			if file == '':
				debug = True
			data = {}
			f = open(root+'/'+file, 'rb').read()
			for line in re.split(';[\r\n]', f):
				if ' = ' in line:
					splits = line.strip().split(' = ')
					if splits[1][0] == '"' and splits[1][-1] == '"':
						splits[1] = splits[1][1:-1]
					if splits[0] == 'map':
						data[splits[0]] = ast.literal_eval(splits[1])
					elif splits[0] == 'A_sprites':
						if debug:
							print splits[1][2720:2740]
						data[splits[0]] = json.loads(splits[1])
					else:
						data[splits[0]] = splits[1]
			tileset = Image.open('tilesets/'+data['tileset']+'.png')
			w, h = tileset.size
			w, h = w/16, h/16
			tiles = [[None for _ in range(h)] for __ in range(w)]
			if data['tileset'] == 'rural':
				continue
				w -= 20
			# First, we parse the tileset.
			# All tiles in columns 0-9 are single-height
			# All tiles in columns 10-19 are double-height
			# All tiles in columns 20-29 are triple-height
			for x in range(10):
				for y in range(1, h, 1):
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
					_x = coords % 10 + (h-1) * 10
					_y = ((coords / 10) * h) + 1
					if debug:
						print h, coords, _x, _y
						print (x*16, y*16, (x+1)*16, (y+h)*16)
						print tiles[_x][_y]
					map.paste(tiles[_x][_y], (x*16, (y+3-h)*16, (x+1)*16, (y+3)*16), tiles[_x][_y])
			'''
			# Third, we add sprites
			for sprite in data['A_sprites']:
				if sprite['model'] == 'o_Crystal':
					crystal = Image.open('sprites/obj_Crystal.png').crop((0, 0, 16, 16))
					x, y = sprite['x'], sprite['y']
					map.paste(crystal, (x*16, y*16-4, (x+1)*16, (y+1)*16-4), crystal)
				elif sprite['model'][:7] == 'BIGDOOR':
					doors = Image.open('sprites/BIGDOORSHEET.png')
					doorno = int(sprite['model'][7])
					door = doors.crop((0, doorno*32, 16, (doorno+1)*32))
					x, y = sprite['x'], sprite['y']
					map.paste(door, (x*16, (y-1)*16, (x+1)*16, (y+1)*16), door)
				elif sprite['model'][:4] == 'DOOR':
					doors = Image.open('sprites/DOORSHEET.png')
					doorno = int(sprite['model'][4])
					door = doors.crop((0, doorno*16, 16, (doorno+1)*16))
					map.paste(door, (x*16, y*16, (x+1)*16, (y+1)*16), door)
			'''

if __name__ == '__main__':
	main()
