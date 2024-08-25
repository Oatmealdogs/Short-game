# Simple Text-Based Adventure Game

def show_instructions():
    print("""
    Adventure Game
    ==============
    Commands:
      go [direction]
      get [item]
    """)

def show_status():
    print("---------------------------")
    print(f"You are in the {current_room}")
    print(f"Inventory: {inventory}")
    if "item" in rooms[current_room]:
        print(f"You see a {rooms[current_room]['item']}")
    print("---------------------------")

# An inventory, which is initially empty
inventory = []

# A dictionary linking rooms to other rooms and items
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
        'item': 'potion'
    },
    'Garden': {
        'north': 'Dining Room'
    }
}

# Start the player in the Hall
current_room = 'Hall'

show_instructions()

# Loop until the player wins or loses
while True:
    show_status()

    # Get the player's next move
    move = input("> ").lower().split()

    # If they type 'go' first
    if move[0] == 'go':
        # Check that they are allowed to move in that direction
        if move[1] in rooms[current_room]:
            # Set the current room to the new room
            current_room = rooms[current_room][move[1]]
        else:
            print("try a different way!")

    # If they type 'get' first
    if move[0] == 'get':
        # If the item is in the room, add it to their inventory
        if "item" in rooms[current_room] and move[1] == rooms[current_room]['item']:
            inventory.append(move[1])
            print(f"{move[1]} got!")
            # Remove the item from the room
            del rooms[current_room]['item']
        else:
            print(f"Can't get {move[1]}!")

    # If a player enters a room with a monster
    if 'item' in rooms[current_room] and rooms[current_room]['item'] == 'monster':
        print("A monster ate you... GAME OVER!")
        break

    # If a player enters the Garden with a key and a potion
    if current_room == 'Garden' and 'key' in inventory and 'potion' in inventory:
        print("You escaped the house... YOU WIN!")
        break
if current_room == 'Dining Room' and 'key' not in inventory:
    print("The door is locked! You need a key.")
    current_room = 'Hall'  # Send them back
health = 100

if 'item' in rooms[current_room] and rooms[current_room]['item'] == 'monster':
    print("A monster attacks you!")
    health -= 30
    if health <= 0:
        print("You have been defeated... GAME OVER!")
   
if current_room == 'Garden' and 'key' in inventory and 'potion' in inventory:
    print("You escaped with all the treasures... YOU WIN THE SECRET ENDING!")
