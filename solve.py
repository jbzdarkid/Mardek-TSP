from Queue import Queue

def pprint(board):
	for row in board:
		line = ''
		for cell in row:
			if cell:
				cost, _, __ = cell
				cost = str(cost)
			else:
				cost = 'None'
			line += cost + ' '*(5-len(cost))
		print line

def is_valid(board, x, y):
	if x < 0 or x >= len(board):
		return False
	if y < 0 or y >= len(board[x]):
		return False
	return board[x][y] == 0

def calc_dist(board, start, end):
	x, y = start
	if board[x][y] != 0:
		return False
	board2 = [[None for _ in range(len(board[0]))] for __ in range(len(board))]
	q = Queue()
	board2[x][y] = (0, 'S', None)
	q.put((0, x, y, 'S'))
	while not q.empty():
		cost, x, y, dir = q.get()
		for newdir in ['N', 'E', 'S', 'W']:
			if newdir == 'N':
				_x, _y = x-1, y
			elif newdir == 'E':
				_x, _y = x, y-1
			elif newdir == 'S':
				_x, _y = x+1, y
			elif newdir == 'W':
				_x, _y = x, y+1
			if is_valid(board, _x, _y):
				cost2 = 99999
				if board2[_x][_y]:
					cost2, _, __ = board2[_x][_y]
				# It takes 6 frames to make a step, and 1 frame to change directions.
				newcost = cost + (6 if newdir == dir else 7)
				if newcost < cost2:
					board2[_x][_y] = (newcost, newdir, (x, y))
					q.put((newcost, _x, _y, newdir))
	path = [end]
	x, y = end
	if board2[x][y] == None:
		return False
	cost, _, __ = board2[x][y]
	prev = None
	while prev != start:
		_, dir, prev = board2[x][y]
		path.append(prev)
		x, y = prev
	return (cost, path)

data = [
[1, 1, 1, 0, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 1, 1],
[1, 0, 1, 1, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 0, 1, 0, 1],
[1, 0, 1, 1, 0, 0, 1, 0, 1],
[1, 0, 1, 0, 0, 1, 1, 0, 1],
[1, 0, 1, 1, 1, 1, 1, 1, 1]
]

start = (0, 3)
end = (6, 1)
chests = [(3, 3), (5, 3), (5, 7)]
n = len(chests)

# Step 1 - Make a board of every point to every other point.
# distances[0] represents start
# distances[1 .. n] represents chests
# distances[n+1] represents end
distances = [[None for _ in range(n+2)] for __ in range(n+2)]
distances[0][n+1] = calc_dist(data, start, end)
for i in range(n):
	distances[i+1][n+1] = calc_dist(data, chests[i], end)
	for j in range(i, n):
		if i == 0:
			distances[0][j+1] = calc_dist(data, start, chests[j])
		if i == j:
			continue
		distances[i+1][j+1] = calc_dist(data, chests[i], chests[j])

# NB start and end points, so n+2 elements.
# As far as TSP goes I see a 4-stage solution:
# Step 1. Make a board from every chest to every other, containing the shortest distance. This is simply done by an nxn array.
# Step 2. For each collection of chests, find the best route through. This is simply done with a 2^n array, where entry 5 = 0000101 which means chests 1 and 3. Build this iteratively, i.e. shortest path containing chest 1, chest 2, chest 3, then shortest path containing 1&2, 2&3, etc.
# Step 3. For each chest, find the difference (average? max? min?) between each collection that contains it and the same collection, less that chest.
# [Human] Step 4. Determine which chests should be grabbed or not.