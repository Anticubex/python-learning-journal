import random


# Base Card class
class Card:
    def __init__(self, name, description, cost):
        self.name = name
        self.description = description
        self.cost = cost

    def __str__(self):
        return f"{self.name} (Cost: {self.cost}) - {self.description}"


# Unit Card subclass
class UnitCard(Card):
    def __init__(self, name, description, cost, attack, hp):
        super().__init__(name, description, cost)
        self.attack = attack
        self.hp = hp

    def __str__(self):
        return f"{self.name} (Cost: {self.cost}, ATK: {self.attack}, HP: {self.hp}) - {self.description}"


# Spell Card subclass
class SpellCard(Card):
    def __init__(self, name, description, cost, effect):
        super().__init__(name, description, cost)
        self.effect = effect  # Function that modifies game state

    def cast(self, player, opponent):
        self.effect(player, opponent)

    def __str__(self):
        return f"{self.name} (Cost: {self.cost}) - {self.description}"


# Linked List Node for Deck
class Node:
    def __init__(self, card):
        self.card = card
        self.next = None


# Linked List for Deck
class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, card):
        if self.head is None:
            self.head = Node(card)
            return
        self.getTail().next = Node(card)

    def remove(self, index):
        ptr = self.head
        count = 1
        while count < index:
            if ptr is None:
                raise IndexError()
            count += 1
            ptr = ptr.next
        ptr.next = ptr.next.next

    def draw(self):
        ret = self.head.card
        self.head = self.head.next
        return ret

    def join(self, other):
        # Joins while copying
        anchor = Node("dummy")
        ptr = anchor
        for card in other:
            ptr.next = Node(card)
            ptr = ptr.next
        if self.head is None:
            self.head = anchor.next
        else:
            self.getTail.next = anchor.next

    def getTail(self):
        ptr = self.head
        if ptr is None:
            return None
        while ptr.next is not None:
            ptr = ptr.next
        return ptr

    def __iter__(self):
        ptr = self.head
        while ptr is not None:
            yield ptr.card

    def is_empty(self):
        return self.head is None

    def __len__(self):
        ptr = self.head
        count = 0
        while ptr is not None:
            ptr = ptr.next
            count += 1
        return count

    def shuffle(self):
        if self.head is None or self.head.next is None:
            return
        list1 = LinkedList()
        list2 = LinkedList()

        ptr = self.head
        while ptr is not None:
            list1.append(ptr.card)
            ptr = ptr.next
            if ptr is not None:
                list2.append(ptr.card)
                ptr = ptr.next

        list1.shuffle()
        list2.shuffle()
        anchor = Node(None)
        ptr = anchor

        while not list1.is_empty() or not list2.is_empty():
            l = random.choice([list1, list2])
            ptr.next = Node(l.head.card)
            ptr = ptr.next
            l.head = l.head.next
        self.head = anchor.next
        if list1.is_empty():
            self.join(list2)
        else:
            self.join(list1)


# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 20
        self.mana = 3  # Base mana each turn
        self.deck = LinkedList()
        self.hand = LinkedList()
        self.board = LinkedList()
        self.discard = LinkedList()

    def draw_card(self):
        card = self.deck.draw()
        if card:
            self.hand.append(card)
            print(f"{self.name} draws {card.name}")

    def play_card(self, index, opponent):
        if index < 0 or index >= len(self.hand):
            print("Invalid card index.")
            return False

        card_ptr = self.hand.head
        for _ in range(index):
            card_ptr = card_ptr.next
        card = card_ptr.card

        if card.cost > self.mana:
            print("Not enough mana!")
            return False

        self.mana -= card.cost
        self.hand.remove(index)

        if isinstance(card, UnitCard):
            self.board.append(card)
            print(f"{self.name} plays {card.name} onto the board!")
        elif isinstance(card, SpellCard):
            card.cast(self, opponent)
            print(f"{self.name} casts {card.name}!")
        return True

    def attack(self, opponent):
        for unit in self.board:
            if unit.hp > 0:
                print(f"{self.name}'s {unit.name} attacks for {unit.attack} damage!")
                opponent.take_damage(unit.attack)

    def take_damage(self, damage):
        behind = None
        ptr = self.board.head
        while True:
            if ptr is None:
                self.hp -= damage
                print(f"{self.name} loses {damage} hp!")
                return
            unit = ptr.card
            if damage >= unit.hp:
                damage -= unit.hp
                print(f"{self.name}'s {unit.name} dies!")
                if behind is None:
                    self.board.head = ptr.next
                else:
                    ptr.next = ptr.next.next
            else:
                print(f"{self.name}'s takes {damage} damage!")
                unit.hp -= damage

            behind = ptr
            ptr = ptr.next

    def is_defeated(self):
        return self.hp <= 0


# Game setup
def setup_game():
    player1 = Player("Player 1")
    player2 = Player("Player 2")

    def fullShuffle(player, _):
        # Join the
        player.deck.join(player.hand)
        player.hand = LinkedList()
        player.deck.join(player.discard)
        player.discard = LinkedList()

        player.deck.shuffle()

        for _ in range(7):
            player.draw_card()

    # Create sample cards
    cards = [
        UnitCard("Warrior", "A strong fighter", 2, 3, 2),
        UnitCard("Archer", "Ranged attack unit", 1, 2, 1),
        UnitCard("Knight", "A resilient defender", 3, 2, 5),
        UnitCard("Assassin", "A stealthy attacker", 2, 4, 1),
        SpellCard(
            "Full Shuffle",
            "Put your entire hand and discard pile into the deck. Shuffle the deck. Draw 7 cards",
            1,
            fullShuffle,
        ),
        SpellCard(
            "Fireball", "Deal 3 damage", 2, lambda p, o: setattr(o, "hp", o.hp - 3)
        ),
        SpellCard("Heal", "Restore 4 HP", 2, lambda p, o: setattr(p, "hp", p.hp + 4)),
    ]

    for _ in range(25):
        player1.deck.append(random.choice(cards))
        player2.deck.append(random.choice(cards))

    return player1, player2


def input_number(prompt, allowed_range):
    num = None
    while num is None:
        try:
            num = int(input(prompt))
        except ValueError:
            print("Not an integer value...")
        if num not in allowed_range:
            print("Not an option...")
            num = None
    return num


def print_board(player):
    print(
        "Board:"
        + "\t".join(
            f"{idx} {unit.name} {unit.attack}/{unit.hp}"
            for idx, unit in enumerate(player.board)
        )
    )


def print_hand(player):
    print(
        "Hand:"
        + "\t".join(
            f"{idx} {card.name} {card.cost}" for idx, card in enumerate(player.hand)
        )
    )


# Game loop
def play_game():
    player1, player2 = setup_game()
    turn = 1

    while not player1.is_defeated() and not player2.is_defeated():
        print(f"\nTurn {turn}")
        current_player = player1 if turn % 2 == 1 else player2
        opponent = player2 if turn % 2 == 1 else player1

        current_player.mana = 3  # Reset mana each turn
        if len(current_player.hand) < 7:
            current_player.draw_card()

        print(f"{current_player.name}'s turn:")
        print_board(current_player)
        print_hand(current_player)

        while True:
            print()
            print("Options:")
            print("1) Get more info on card on board")
            print("2) Get more info on card in hand")
            print("3) Play card")
            print("4) End turn")
            option = input_number("What option do you choose? ", [1, 2, 3, 4])

            match option:
                case 1:
                    print_board(current_player)
                    card_index = input_number(
                        "What card to describe?", range(len(current_player.board))
                    )
                    for idx, card in enumerate(current_player.board):
                        if idx == card_index:
                            print(str(card))
                case 2:
                    print_hand(current_player)
                    card_index = input_number(
                        "What card to describe?", range(len(current_player.hand))
                    )
                    for idx, card in enumerate(current_player.board):
                        if idx == card_index:
                            print(str(card))
                case 3:
                    print_hand(current_player)
                    card_index = input_number(
                        "What card to play?", range(len(current_player.hand))
                    )
                    current_player.play_card(card_index, opponent)
                case 4:
                    break

        current_player.attack(opponent)

        if opponent.is_defeated():
            print(f"{current_player.name} wins!")
            break

        turn += 1


# Run the game
play_game()
