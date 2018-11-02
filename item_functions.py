import libtcodpy as libtcod

from game_messages import Message

def heal(*args, **kwargs):
	entity = args[0]
	amount = kwargs.get('amount')
	
	
	results = []
	
	
	if entity.fighter.hp == entity.fighter.max_hp:
		results.append({'consumed': False, 'message': Message('Your body is perfect, the meat goes straight through you.')})
		
	else:
		entity.fighter.heal(amount)
		results.append({'consumed': True, 'message': Message('The meat slides into you bringing you closer to perfect')})
		
	return results