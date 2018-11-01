import libtcodpy as libtcod

class BasicMonster:
	def take_turn(self, target, fov_map, game_map, entities):
		results = []
		
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			
			if monster.distance_to(target) >=2:
				monster.move_astar(target, entities, game_map)
				
			elif target.fighter.hp > 0:
				attack_results = monster.fighter.attack(target)
				results.extend(attack_results)
				
				
		return results
			
class BlockingMonster:
	def take_turn(self, target, fov_map, game_map, entities):
		results = []
		
		monster = self.owner
		
		
				
				
		return results	
		
		
		
class DrudgeMonster:
	def take_turn(self, target, fov_map, game_map, entities):
		
		results = []
		
		monster = self.owner
		
			
		if monster.distance_to(target) >=1:
				monster.move_astar(target, entities, game_map)
				
		else: 
			target = None
			
			while target is None:
				x = randint(map_width - 1)
				y = rantint(map_height - 1)
					
				if not tiles[x][y].blocked:
					target = tiles[x][y]
					print ('got target')
				
		return results
		
		
		
	
		