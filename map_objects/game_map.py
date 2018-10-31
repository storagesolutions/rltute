from random import randint

from map_objects.tile import Tile
from map_objects.rectangle import Rect


class GameMap:

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.tiles = self.initialize_tiles()
		
		
	def initialize_tiles(self):
		tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
		
		return tiles
	
	def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
	
		rooms = []
		num_rooms = 0
		
		
		for r in range(max_rooms):
			#random width and height
			w = randint(room_min_size, room_max_size)
			h = randint(room_min_size, room_max_size)
			#random position without leaving map boundries
			x = randint(0, map_width - w -1)
			y = randint(0, map_height - h -1)
			
			# Rect class makes rectangles easier to work with
			new_room = Rect(x, y, w, h)
			
			#run through the other rooms and see if they interessct with this one
			for other_room in rooms:
				if new_room.intersect(other_room):
					break
					
			else:
				
			#this means there are no intersections, so this room is valid
				
			#paint it to the map's tiles
				self.create_room(new_room)
				self.make_lumps(new_room)
				
			#center coordinates of new room, useful later
				(new_x, new_y) = new_room.center()
				
				if num_rooms == 0:
					# this is first room, for the player
					player.x = new_x
					player.y = new_y
					
				else:
					#all rooms after the first
					#connect it to the previous room with a tunnel
					
					#center coordinates of previous room
					(prev_x, prev_y) = rooms[num_rooms - 1].center()
					
					#flip a coin randint 0 or 1
					if randint(0, 1) == 1:
						#first move horzontally, then vertically
						self.create_h_tunnel(prev_x, new_x, prev_y)
						self.create_v_tunnel(prev_y, new_y, new_x)
						
					else:
						#first move verticall, then horzontally
						self.create_v_tunnel(prev_y, new_y, new_x)
						self.create_h_tunnel(prev_x, new_x, prev_y)
						
				#finally, append the new room to the list
				rooms.append(new_room)
				num_rooms += 1
					
	
		
				
			
		
	
	def create_room(self, room):
		#go through the tiles in the rectangle and make them passable
		for x in range(room.x1 + 1, room.x2):
			for y in range(room.y1 + 1, room.y2):
				self.tiles[x][y].blocked = False
				self.tiles[x][y].block_sight = False
				
	
	def create_h_tunnel(self, x1, x2, y):
		for x in range(min(x1, x2), max (x1, x2) + 1):
			self.tiles[x][y].blocked = False
			self.tiles[x][y].block_sight = False
			
	
	def create_v_tunnel(self, y1, y2, x):
		for y in range(min(y1, y2), max(y1, y2) + 1):
			self.tiles[x][y].blocked = False
			self.tiles[x][y].block_sight = False
	
	def make_lumps(self, room):
		for x in range(room.x1 + 1, room.x2):
			for y in range(room.y1 + 1, room.y2):
					if randint(1, 7) == 1:	
						self.tiles[x][y].blocked = True
						self.tiles[x][y].block_sight = True
				
	
	def is_blocked(self, x, y):
		if self.tiles[x][y].blocked:
			return True
			
		return False
		
		
