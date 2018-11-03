import libtcodpy as libtcod

from game_messages import Message

from components.ai import ConfusedMonster

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

def cast_blood(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')
    
    results = []
    
    target = None
    closest_distance = maximum_range + 1
    
    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)
            
            if distance < closest_distance:
                target = entity
                closest_distance = distance
                
    if target:
        results.append({'consumed': True, 'target': target, 'message': Message('A stream of blood hammers the {0} in a thunderous rush! The damage is {1}'.format(target.name, damage), libtcod.crimson)})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('No enemy is close enough to strike.', libtcod.red)})
    
    return results

def cast_virus(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    results.append({'consumed': True, 'message': Message('The virus swarms forth,necrotizing everything within {0} tiles!'.format(radius), libtcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message('The {0} rots for {1} hit points.'.format(entity.name, damage), libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results  

def cast_mindworms(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message('The worms burrow deep into the {0} making it twitch and dance'.format(entity.name), libtcod.pink)})
            break
        else:
            results.append({'consumed': False, 'message': Message('There is nothing here into which the worms can burrow.')})
    return results