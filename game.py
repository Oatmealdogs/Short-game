# Simple Text-Based Adventure Game

def show_instructions():
    print("""
    Adventure Game
    ==============
    Commands:
      go [direction]
      get [item]
      cast [spell]
    """)

def show_status():
    print("---------------------------")
    print(f"You are in the {current_room}")
    print(f"Inventory: {inventory}")
    print(f"Spells: {spells}")
    print(f"Health: {health}")
    if "item" in rooms[current_room]:
        print(f"You see a {rooms[current_room]['item']}")
    print("---------------------------")

# An inventory, which is initially empty
inventory = []
spells = []

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
        'north': 'Dining Room',
        'item': 'fireball spellbook'
    }
}

# Start the player in the Hall
current_room = 'Hall'

# Initialize player's health
health = 100

show_instructions()

# Loop until the player wins or loses
while True:
    show_status()

    # Check if player's health is depleted
    if health <= 0:
        print("Your health has depleted... GAME OVER!")
        break

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
            # Use potion if picked up
            if move[1] == 'potion':
                health = min(100, health + 30)
                print("You drink the potion and restore 30 health!")
                inventory.remove('potion')
        else:
            print(f"Can't get {move[1]}!")

    # If they type 'cast' first
    if move[0] == 'cast':
        if move[1] in spells:
            if move[1] == 'fireball' and 'item' in rooms[current_room] and rooms[current_room]['item'] == 'monster':
                print("You cast fireball and defeat the monster!")
                del rooms[current_room]['item']
            else:
                print("Your spell has no effect here.")
        else:
            print("You don't know that spell!")

    # If they get a spellbook
    if 'item' in rooms[current_room] and 'spellbook' in rooms[current_room]['item']:
        spell = rooms[current_room]['item'].split()[0]
        if spell not in spells:
            spells.append(spell)
            print(f"You learned the {spell} spell!")

    # If a player enters a room with a monster
    if 'item' in rooms[current_room] and rooms[current_room]['item'] == 'monster':
        print("A monster attacks you!")
        health -= 30
        if health <= 0:
            print("You have been defeated... GAME OVER!")
            break
        else:
            print(f"You lost 30 health. Current health: {health}")

    # If a player enters the Garden with a key and a potion
    if current_room == 'Garden' and 'key' in inventory and 'potion' in inventory:
        print("You escaped the house... YOU WIN!")
        break

    if current_room == 'Dining Room' and 'key' not in inventory:
        print("The door is locked! You need a key.")
        current_room = 'Hall'  # Send them back

    # Random events that can affect health
    import random
    if random.random() < 0.1:  # 10% chance of a random event
        event = random.choice(['trap', 'blessing'])
        if event == 'trap':
            damage = random.randint(5, 15)
            health -= damage
            print(f"You triggered a trap! You lose {damage} health.")
        else:
            heal = random.randint(5, 15)
            health = min(100, health + heal)
            print(f"You feel a blessing! You gain {heal} health.")

    if current_room == 'Garden' and 'key' in inventory and 'potion' in inventory:
        print("You escaped with all the treasures... YOU WIN THE SECRET ENDING!")