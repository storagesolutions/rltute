import libtcodpy as libtcod

def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
	if fov_recompute:
	#draw all tiles in the game_map
		for y in range(game_map.height):
			for x in range(game_map.width):
				visible = libtcod.map_is_in_fov(fov_map, x, y)
				wall = game_map.tiles[x][y].block_sight
				
				if visible:
					if wall:
						libtcod.console_put_char_ex(con, x, y, '#', libtcod.white, libtcod.black)
					
					else:
						libtcod.console_put_char_ex(con, x, y, '.', libtcod.white, libtcod.black)
					
					game_map.tiles[x][y].explored = True
				
				elif game_map.tiles[x][y].explored:
					if wall:
						
						libtcod.console_put_char_ex(con, x, y, '#', libtcod.grey, libtcod.black)
					
					else:
						libtcod.console_put_char_ex(con, x, y, '.', libtcod.grey, libtcod.black)
					
					
	#draw all entities in the list
	for entity in entities:
		draw_entity(con, entity, fov_map)
		

	libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
	for entity in entities:
		clear_entity(con, entity)
		
		
		
def draw_entity(con, entity, fov_map):
	if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
		libtcod.console_set_default_foreground(con, entity.color)
		libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)
	

def clear_entity(con, entity):
	#erase the character that represents this object
	libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
		
		
