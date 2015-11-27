import os, ast, json
from PIL import Image
def main():
	for root, dirs, files in os.walk('maps'):
		for file in files:
			data = {}
			f = open(root+'/'+file, 'rb').read()
			for line in f.split(';\r\n'):
				if ' = ' in line:
					splits = line.split(' = ')
					if splits[1][0] == '"' and splits[1][-1] == '"':
						splits[1] = splits[1][1:-1]
					if splits[0] == 'map':
						data[splits[0]] = ast.literal_eval(splits[1])
					elif splits[0] == 'A_sprites':
						data[splits[0]] = json.loads(splits[1])
					else:
						data[splits[0]] = splits[1]
			tileset = Image.open('tilesets/'+data['tileset']+'.png')
			w, h = tileset.size
			w, h = w/16, h/16
			tiles = [None]*w*h
			for x in range(w):
				for y in range(h):
					tiles[x+y*w] = tileset.crop((x*16, y*16, (x+1)*16, (y+1)*16))
			map = Image.new('RGB', (len(data['map'][0])*16, len(data['map'])*16), 'white')
			for x in range(len(data['map'])):
				for y in range(len(data['map'][0])):
					map.paste(tiles[data['map'][x][y]+5], (y*16, x*16, (y+1)*16, (x+1)*16))
			for sprite in data['A_sprites']:
				if sprite['model'] == 'o_Crystal':
					crystal = Image.open('tilesets/obj_Crystal.png').crop((0, 0, 16, 16))
					x, y = sprite['x'], sprite['y']
					map.paste(crystal, (x*16, y*16, (x+1)*16, (y+1)*16), crystal)
				elif sprite['model'][:7] == 'BIGDOOR':
					doors = Image.open('tilesets/BIGDOORSHEET.png')
					doorno = int(sprite['model'][7])
					door = doors.crop((0, doorno*32, 16, (doorno+1)*32))
					x, y = sprite['x'], sprite['y']
					map.paste(door, (x*16, (y-1)*16, (x+1)*16, (y+1)*16), door)
			map.show()

			return

if __name__ == '__main__':
	main()
