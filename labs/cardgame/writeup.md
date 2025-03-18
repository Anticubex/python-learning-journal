# Homebrew Card Game - Documentation

## Overview

This homebrew card game is inspired by games like Magic: The Gathering and Hearthstone. It is a two-player game where each player has a deck of at least 25 cards, containing Unit Cards and Spell Cards. The goal is to reduce the opponent's HP to 0 through strategic card plays and attacks.

## Division of Labor

I worked alone because I have bad decision making skills.

## Game Rules

- Each player starts with 20 HP and 3 mana per turn.
- Players take turns drawing, playing cards, and attacking with units.
- Unit Cards remain on the board and can attack each turn.
- Spell Cards apply instant effects and are discarded after use.
- The deck is implemented as a linked list, ensuring dynamic card management.
- The game ends when a player’s HP reaches 0.

## UML Diagram

```plaintext
                +----------------+
                |      Card      |
                +----------------+
                | - name         |
                | - description  |
                | - cost         |
                +----------------+
                        |
          +-------------+-------------+
          |                           |
+-----------------+         +-----------------+
|   UnitCard      |         |   SpellCard    |
+-----------------+         +-----------------+
| - attack        |         | - effect        |
| - hp            |         | + cast()        |
+-----------------+         +-----------------+

+----------------+
|      Node      |
+----------------+
| - card         |
| - next         |
+----------------+

+----------------+
|  LinkedList    |
+----------------+
| - head         |
| + append()     |
| + draw()       |
| + shuffle()    |
+----------------+

+----------------+
|    Player      |
+----------------+
| - name         |
| - hp           |
| - mana         |
| - deck         |
| - hand         |
| - board        |
| + draw_card()  |
| + play_card()  |
| + attack()     |
| + is_defeated()|
+----------------+
```

## Class Descriptions

### Card (Base Class)

- Represents any card in the game.
- Attributes: `name`, `description`, `cost`.

### UnitCard (Derived from Card)

- Represents units that stay on the board and attack.
- Attributes: `attack`, `hp`.

### SpellCard (Derived from Card)

- Represents one-time-use cards that apply effects.
- Attributes: `effect` (a function to modify game state).
- Method: `cast(player, opponent)` to execute the effect.

### Node

- Represents a node in the linked list.
- Attributes: `card`, `next`.

### LinkedList (Deck Structure)

- Implements a linked list to hold cards dynamically.
- Methods:
     - `append(card)`: Adds a card to the deck.
     - `draw()`: Removes and returns the top card.
     - `shuffle()`: Shuffles the deck in place.

### Player

- Represents a player in the game.
- Attributes:
     - `name`, `hp`, `mana`.
     - `deck`, `hand`, `board` (as linked lists).
- Methods:
     - `draw_card()`: Draws a card from the deck.
     - `play_card(index, opponent)`: Plays a card from the hand.
     - `attack(opponent)`: Attacks the opponent using units.
     - `is_defeated()`: Checks if the player has lost.

## Conclusion

This game effectively uses object-oriented principles such as inheritance and polymorphism. The linked list structure provides efficient card management, while turn-based mechanics create engaging gameplay. This implementation provides a solid foundation for further enhancements, such as additional card types, more complex mechanics, and a graphical interface.
