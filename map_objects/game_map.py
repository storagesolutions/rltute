import libtcodpy as libtcod
from random import randint
from components.fighter import Fighter
from components.ai import BasicMonster,BlockingMonster,CunningMonster,WanderingMonster,CautiousMonster,StalkingMonster
from components.item import Item
from item_functions import heal, cast_blood, cast_virus, cast_mindworms
from game_messages import Message
from entity import Entity
from render_functions import RenderOrder
from map_objects.tile import Tile
from map_objects.rectangle import Rect


class GameMap:

	def __init__(self, width, height,entities):
		self.width = width
		self.height = height
		self.tiles = self.initialize_tiles()
		self.entities = entities
		
	def initialize_tiles(self):
		tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
		
		return tiles
	
	def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room):
	
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
					

				self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)
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
					if randint(1, 5) == 1:	
						self.tiles[x][y].blocked = True
						self.tiles[x][y].block_sight = True
						
	
	def place_entities(self, room, entities, max_monsters_per_room, max_items_per_room):
		#get a random number of monseters
		number_of_monsters = randint(0, max_monsters_per_room)
		number_of_items = randint(0, max_items_per_room)
		
		
		for i in range(number_of_monsters):
			# Choose a random location in the room
			x = randint(room.x1 + 1, room.x2 -1)
			y = randint(room.y1 +1, room.y2 - 1)
			
			if not self.tiles[x][y].blocked:	
				if not any([entity for entity in entities if entity.x == x and entity.y == y]):
					monster_chance = randint(1,100)	
					if monster_chance <20:
						fighter_component = Fighter(hp = 10, defense = 1, power = 0)
						ai_component = BlockingMonster()
						monster = Entity(x, y, '&', libtcod.light_red,'meat pile', blocks=True, fighter=fighter_component, ai=ai_component, block_sight=True)

					elif monster_chance  < 30:
						fighter_component = Fighter(hp=2, defense=0, power=2)
						ai_component = WanderingMonster()
					
						monster = Entity(x, y, 'd', libtcod.purple, 'drudge', blocks=True, render_order = RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)


					elif monster_chance  < 45:
						fighter_component = Fighter(hp=8, defense=0, power=4)
						ai_component = BasicMonster()
					
						monster = Entity(x, y, 'm', libtcod.lighter_crimson, 'maw', blocks=True, render_order = RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
					
					elif monster_chance  < 55:
						fighter_component = Fighter(hp=8, defense=1, power=3)
						ai_component = CunningMonster()
						
						monster = Entity(x, y, 't', libtcod.turquoise, 'twitcher', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
					
					elif monster_chance  < 70:
						fighter_component = Fighter(hp=2, defense=0, power=2)
						ai_component = CautiousMonster()
					
						monster = Entity(x, y, 'w', libtcod.gold, 'warper', blocks=True, render_order = RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

					
					
					elif monster_chance  < 85:
						fighter_component = Fighter(hp=20, defense=0, power=10)
						ai_component = StalkingMonster()
					
						monster = Entity(x, y, 'A', libtcod.purple, 'amputatrix', blocks=True, render_order = RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
					
					

					else:
						fighter_component = Fighter(hp = 10, defense = 1, power = 0)
						ai_component = BlockingMonster()
						monster = Entity(x, y, '&', libtcod.light_red,'meat pile', blocks=True, fighter=fighter_component, ai=ai_component, block_sight=True)
							
					
					entities.append(monster)
		

		for i in range(number_of_items):
			x = randint(room.x1 + 1, room.x2 - 1)
			y = randint(room.y1 + 1, room.y2 - 1)
			
			if not self.tiles[x][y].blocked:
				if not any([entity for entity in entities if entity.x == x and entity.y == y]):
					item_chance = randint(0,100)

					if item_chance < 70:

						item_component = Item(use_function=heal, amount = 4)
						item = Entity(x, y, '!', libtcod.darker_amber, 'Meat Chunk', render_order=RenderOrder.ITEM, item=item_component)
					
					elif item_chance < 75:
						
						item_component = Item(use_function=cast_virus,targeting=True, targeting_message=Message(
																				'Left click a target tile to unleash the virus, or right-click to cancel.', libtcod.celadon),
																				damage=12, radius = 3)
						item = Entity(x, y, '*', libtcod.celadon, 'Virus Cluster', render_order=RenderOrder.ITEM, item=item_component)
					elif item_chance < 80:
						item_component =Item(use_function=cast_mindworms, targeting=True, targeting_message=Message(
									'Left click to fill a living being with burrowing worms, right click to cancel', libtcod.pink))
						item = Entity(x, y, '*', libtcod.pink, 'Mind-Worm Nest', render_order=RenderOrder.ITEM, item=item_component)
					
					else:
						item_component =Item(use_function=cast_blood, amount=4, damage = 20, maximum_range = 5)
						item = Entity(x, y, ')', libtcod.crimson, 'Blood Extruder', render_order=RenderOrder.ITEM,
													item=item_component)
					entities.append(item)
	
	def is_blocked(self, x, y):
		if self.tiles[x][y].blocked:
			return True
			
		return False
	

