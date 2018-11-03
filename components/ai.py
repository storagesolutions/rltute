
import libtcodpy as libtcod
from random import randint
from game_messages import Message


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
		return results	
		
class ConfusedMonster:
	def __init__(self, previous_ai, number_of_turns=10):
		self.previous_ai = previous_ai
		self.number_of_turns = number_of_turns

	def take_turn(self, target, fov_map, game_map, entities):
		results = []
		if self.number_of_turns > 0:
			random_x = self.owner.x + randint(0, 2) - 1
			random_y = self.owner.y + randint(0, 2) - 1

			if random_x != self.owner.x and random_y != self.owner.y:
				self.owner.move_towards(random_x, random_y, game_map, entities)

				self.number_of_turns -= 1
		else:
			self.owner.ai = self.previous_ai
			results.append({'message': Message('The {0} is no longer full of worms'.format(self.owner.name), libtcod.red)})

		return results

class CunningMonster:
	def take_turn(self, target, fov_map, game_map, entities):
		results = []
		
		monster = self.owner

		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			turn = randint(1,10)
			
			if monster.distance_to(target) >=2:
				if turn <= 5:
					monster.move_astar(target, entities, game_map)
				elif turn <= 7:
					attack_results = monster.fighter.attack(target)
					results.extend(attack_results)
				else:
					results.append({'message': Message('The {0} stands and shivers in place, watching you'.format(self.owner.name),libtcod.silver)})

				
			elif target.fighter.hp > 0:
				attack_results = monster.fighter.attack(target)
				results.extend(attack_results)
				
				
		return results
		
		
class WanderingMonster:
	def take_turn(self, target, fov_map, game_map, entities):
		results = []
		
		random_x = self.owner.x + randint(0, 2) - 1
		random_y = self.owner.y + randint(0, 2) - 1

		if random_x != self.owner.x and random_y != self.owner.y:
			self.owner.move_towards(random_x, random_y, game_map, entities)
						
		else:
			random_x = self.owner.x + randint(0, 2) - 1
			random_y = self.owner.y + randint(0, 2) - 1
			if random_x != self.owner.x and random_y != self.owner.y:
				self.owner.move_towards(random_x, random_y, game_map, entities)
			else:
				random_x = self.owner.x + randint(0, 2) - 1
				random_y = self.owner.y + randint(0, 2) - 1
				if random_x != self.owner.x and random_y != self.owner.y:
					self.owner.move_towards(random_x, random_y, game_map, entities)



		return results
		


class CautiousMonster:
	def take_turn(self, target, fov_map, game_map, entities):
		results = []
		
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			
			if monster.distance_to(target) >=4:
				monster.move_astar(target, entities, game_map)
				if target.fighter.hp > 0:
					attack_results = monster.fighter.attack(target)
					results.extend(attack_results)

			elif monster.distance_to(target) <=2:
				monster.move_away(target.x, target.y, game_map, entities)

				if target.fighter.hp > 0:
					attack_results = monster.fighter.attack(target)
					results.extend(attack_results)
				
				
		return results

class StalkingMonster:
	def take_turn(self, target, fov_map, game_map, entities):
		results = []
		
		monster = self.owner
		
		if monster.distance_to(target) >=15:
			print('where are you?')
			
		elif monster.distance_to(target) >=2:
			print("found you!")
			monster.move_astar(target, entities, game_map)
				
		elif target.fighter.hp > 0:
			attack_results = monster.fighter.attack(target)
			results.extend(attack_results)
				
				
		return results