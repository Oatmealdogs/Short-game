# Game maps and room data

rooms = {
    'Hall': {
        'south': 'Kitchen',
        'east': 'Dining Room',
        'item': 'dagger'
    },
    'Kitchen': {
        'north': 'Hall',
        'item': 'monster'
    },
    'Dining Room': {
        'west': 'Hall',
        'south': 'Garden',
        'item': 'potion'
    },
    'Garden': {
        'north': 'Dining Room',
        'item': 'fireball spellbook'
    }
}

def get_starting_room():
    return 'Hall'