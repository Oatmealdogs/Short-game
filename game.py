# Simple Text-Based Adventure Game

from companion import Companion

def show_instructions():
    print("""
    Adventure Game
    ==============
    Commands:
      go [direction] (e.g., 'go right', 'go left', 'go forward', 'go back')
      get [item]
      cast [spell]
      attack
      run
      talk
      summon (activate your companion)
      dismiss (deactivate your companion)
    """)

def show_status():
    print("---------------------------")
    print(f"You are in the {current_room}")
    print(f"Inventory: {inventory}")
    print(f"Spells: {spells}")
    print(f"Health: {health}")
    if companion.is_active:
        print(f"Your companion {companion.name} is with you.")
    if "item" in rooms[current_room]:
        if rooms[current_room]['item'] == 'npc':
            print("You see a wise old wizard here.")
        else:
            print(f"You see a {rooms[current_room]['item']}")
    
    # Display available directions
    available_directions = [k for k, v in direction_mapping.items() if v in rooms[current_room]]
    print(f"You can go: {', '.join(available_directions)}")
    print("---------------------------")

import sys
import os
import random  # Add this import

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from game_maps import rooms, get_starting_room

# Initialize player's health and attack
health = 100
attack = 10  # Dagger attack

# An inventory, which is initially empty
inventory = []
spells = []

# Monster stats
monster_health = 20  # Changed from 100 to 20
monster_stunned = False

# Create a companion
companion = Companion("Fluffy", 5)  # Name: Fluffy, Attack Power: 5

show_instructions()

# Start the player in the Hall
current_room = get_starting_room()

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
        direction = ' '.join(move[1:])  # Join all words after 'go'
        if direction in direction_mapping:
            cardinal_direction = direction_mapping[direction]
            if cardinal_direction in rooms[current_room]:
                current_room = rooms[current_room][cardinal_direction]
                print(f"You move {direction}.")
            else:
                print(f"You can't go {direction}!")
        else:
            print("I don't understand that direction!")

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

    # If they type 'attack' first
    if move[0] == 'attack':
        if 'item' in rooms[current_room] and rooms[current_room]['item'] == 'monster':
            if 'dagger' in inventory:
                damage = attack + companion.attack()  # Add companion's attack
                if random.random() < 0.2:  # 20% chance of critical hit
                    damage *= 2
                    monster_stunned = True
                    print("Critical hit! The monster is stunned!")
                monster_health -= damage
                print(f"You and your companion attack the monster for {damage} damage!")
                if monster_health <= 0:
                    print("You defeated the monster!")
                    del rooms[current_room]['item']
                    monster_health = 20  # Reset to 20 for next monster
                else:
                    print(f"The monster has {monster_health} health remaining.")
                    if not monster_stunned:
                        health -= 10  # Reduced monster damage to balance the game
                        print("The monster attacks you! You lose 10 health.")
                    else:
                        monster_stunned = False
                        print("The monster is stunned and can't attack!")
            else:
                print("You need a weapon to attack!")
        else:
            print("There's nothing to attack here!")

    # If they type 'run' first
    if move[0] == 'run':
        if 'item' in rooms[current_room] and rooms[current_room]['item'] == 'monster':
            possible_rooms = [dir for dir in rooms[current_room] if dir != 'item']
            if possible_rooms:
                escape_room = random.choice(possible_rooms)
                current_room = rooms[current_room][escape_room]
                print(f"You managed to escape to the {current_room}!")
                monster_health = 20  # Reset to 20 when running away
                monster_stunned = False
            else:
                print("There's nowhere to run!")
                health -= 10  # Reduced damage when failing to run
                print("The monster attacks you as you fail to escape! You lose 10 health.")
        else:
            print("There's nothing to run from here!")

    # If a player enters a room with a monster
    if 'item' in rooms[current_room] and rooms[current_room]['item'] == 'monster':
        print("A monster attacks you!")
        health -= 10  # Changed from 30 to 10
        if health <= 0:
            print("You have been defeated... GAME OVER!")
            break
        else:
            print(f"You lost 10 health. Current health: {health}")

    # If a player enters the Garden with a key and a potion
    if current_room == 'Garden' and 'key' in inventory and 'potion' in inventory:
        if companion.is_active:
            print("You escaped with all the treasures and your loyal companion... YOU WIN THE SECRET ENDING!")
        else:
            print("You escaped with all the treasures... YOU WIN!")
        break

    if current_room == 'Dining Room' and 'key' not in inventory:
        print("The door is locked! You need a key.")
        current_room = 'Hall'  # Send them back

    # Random events that can affect health
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

    if random.random() < 0.05 and companion.is_active:  # 5% chance when companion is active
        heal = random.randint(5, 10)
        health = min(100, health + heal)
        print(f"{companion.name} found some herbs and healed you for {heal} health!")

    if current_room == 'Garden' and 'key' in inventory and 'potion' in inventory:
        print("You escaped with all the treasures... YOU WIN!")
        break

    # Add new commands to activate/deactivate companion
    if move[0] == 'summon':
        if not companion.is_active:
            companion.activate()
        else:
            print(f"{companion.name} is already with you.")

    if move[0] == 'dismiss':
        if companion.is_active:
            companion.deactivate()
        else:
            print("You don't have an active companion.")

    # If they type 'talk' first
    if move[0] == 'talk':
        if 'item' in rooms[current_room] and rooms[current_room]['item'] == 'npc':
            talk_to_npc()
        else:
            print("There's no one here to talk to!")

    # ... rest of the game logic ...

# Add this near the top of your file, after imports
direction_mapping = {
    'right': 'east',
    'left': 'west',
    'forward': 'north',
    'back': 'south',
    # Keep the original directions as well
    'east': 'east',
    'west': 'west',
    'north': 'north',
    'south': 'south'
}

def talk_to_npc():
    print("You meet a wise old wizard in the library.")
    print("Wizard: 'Greetings, adventurer! I can teach you a spell for 5 gold pieces.'")
    if companion.is_active:
        print(f"Wizard: 'Ah, I see you have {companion.name} with you. A fine companion indeed!'")
    if 'gold' in inventory and inventory.count('gold') >= 5:
        choice = input("Do you want to learn the spell? (yes/no) ").lower()
        if choice == 'yes':
            for _ in range(5):
                inventory.remove('gold')
            spells.append('fireball')
            print("You learned the fireball spell!")
        else:
            print("Maybe next time then.")
    else:
        print("Wizard: 'Come back when you have enough gold, adventurer.'")
