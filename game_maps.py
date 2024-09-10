# Game maps and room data

rooms = {
    'Hall': {
        'south': 'Kitchen',
        'east': 'Dining Room',
        'item': 'key'
    },
    'Kitchen': {
        'north': 'Hall',
        'item': 'monster'
    },
    'Dining Room': {
        'west': 'Hall',
        'south': 'Garden',
        'east': 'Library',
        'item': 'potion'
    },
    'Garden': {
        'north': 'Dining Room'
    },
    'Library': {
        'west': 'Dining Room',
        'item': 'npc'
    }
}

def get_starting_room():
    return 'Hall'