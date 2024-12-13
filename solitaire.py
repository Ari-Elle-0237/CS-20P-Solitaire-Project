"""
Assignment #5: Solitaire
integer_set.py
by Ariel Zepezauer (arielzepezauer@gmail.com) and Aidan Raggio (Aidanpraggio@gmail.com)
Pengo: 'azepezau' & 'araggio'
Test Cases in unittest_.py
Repository at: https://github.com/Ari-Elle-0237/CS-20P-Solitaire-Project.git
Due: Nov 28th 2024
Exit Code: _
"""
import re

import cards
import color
import pickle
import copy


class SolitaireUI:
    """
    A class for the UI
    """
    def __init__(self):
        self.running = True # To be used in exit function - not yet implemented
        self.game_board = GameBoard()
        self.main_ui_loop()

    def main_ui_loop(self):
        while self.running:
            print(self.game_board)
            user_input = input("Enter A Command. (use 'help' for options.): ")
            self.process_command(user_input)

    @staticmethod
    def help_message():
        print("Commands:")
        print(" help: show this message.")
        print(" exit: quits the game.")
        print(" shuf: shuffle the cards.")
        print(" cheat: increase shuffle limit.")
        print(" undo: undo the last move.")
        print(" save: save the current game state. (One slot)")
        print(" load: load the saved game state.")
        print(" [card] [destination]: move a card to a destination (column or tableau).")

    def cheat(self):
        self.game_board.deals += 6
        print("Shuffle count increased.")

    def undo(self):
        if self.game_board.undo():
            print("Last move undone.")
        else:
            print("No moves to undo.")

    def save_game(self):
        filename = input("Enter filename to save the gamestate to: ")
        # Using pickle - taken mostly from Python Documentation
        with open(filename, 'wb') as file:
            pickle.dump(self.game_board, file)
        print("Gamestate saved successfully.")

    def load_game(self):
        filename = input("Enter filename to load the gamestate from: ")
        with open(filename, 'rb') as file:
            self.game_board = pickle.load(file)
        print("Game loaded.")

    def shuffle(self):
        if self.game_board.deals > 0:
            self.game_board.gather_deck()
            self.game_board.deal_cards()
            self.game_board.deals -= 1
        else:
            print("No shuffles remaining.")

    def exit(self):
        """exits the ui loop"""
        self.running = False

    def process_command(self, user_input):
        """
        Breaks a string input into a command and arguments and sends that data to the appropriate function
        Or if the command is malformed, enters a UI loop and returns an appropriate error
        """
        commands = {
            "exit": self.exit,
            "help": self.help_message,
            "shuf": self.shuffle,
            "cheat": self.cheat,
            "undo": self.undo,
            "save": self.save_game,
            "load": self.load_game,
        }
        # Check for simple commands
        if user_input in commands:
            commands[user_input]()
            return
        # Check for move commands: [card] [destination]
        parts = user_input.split()
        print(parts)
        if len(parts) == 2:
            card_input, destination = parts
            card = Card.from_string(self.normalize_card_input(card_input))
            if card is not None and destination.isdigit():
                if self.game_board.move(card, int(destination) - 1):  # Adjust for 0-based index
                    print("Move successful.")
                else:
                    print("Invalid move.")
            else:
                print("Invalid command format.")
        else:
            print("Invalid Command.")

    @staticmethod
    def normalize_card_input(card_input):
        """
        Converts input like '8 h' or '8h' into a proper card string (e.g., '8♥').
        """
        card_input = card_input.strip().replace(" ", "")
        if len(card_input) > 1:
            rank = card_input[:-1]
            suit = card_input[-1].lower()
            suit_map = {'s': '♠', 'h': '♥', 'd': '♦', 'c': '♣'}
            return f"{rank}{suit_map.get(suit, '')}"
        return card_input

    @staticmethod
    def parse_command(command):
        parts = command.strip().split()
        if len(parts) < 2:
            return "Invalid command format."

        # Extract card, destination type, and number
        card = parts[0]  # Card to move (e.g., 'ah' or '10c')
        destination = parts[1]  # Destination identifier

        if destination.startswith('t'):  # Tableau destination
            try:
                tableau_number = int(destination[1:])
                return "tableau", card, tableau_number
            except ValueError:
                return "Invalid tableau identifier."
        else:  # Assume column destination
            try:
                column_number = int(destination)
                return "column", card, column_number
            except ValueError:
                return "Invalid column identifier."


class GameBoard:
    """
    A class defining a solitaire board
    """
    TAB_COUNT = 4 # Tableau Count
    COL_COUNT = 6 # Column Count
    def __init__(self):
        self.deck = Card.new_deal() # Previously [Card(rank, suit) for rank, suit in Card.get_varieties()]
        cards.shuffle(self.deck)
        self.tableaus = [[] for _ in range(self.TAB_COUNT)]
        self.columns =  [[] for _ in range(self.COL_COUNT)]
        self.deals = 6
        self.history = []
        self.deal_cards()

    def update_board(self):
        self.update_card_visibility()
        self.check_winstate()

    # <editor-fold: Setup functions>
    def deal_cards(self):
        for _ in range(min(2, len(self.deck))):
            card = self.deck.pop()
            card.visible = True
            self.columns[0].append(card)
        col = 1
        while self.deck:
            card = self.deck.pop()
            card.visible = True if len(self.columns[col]) == 0 else False
            self.columns[col].append(card)
            col = (col + 1) % self.COL_COUNT if col < self.COL_COUNT - 1 else 1
        for column in self.columns[1:]:
            for i in range(max(0, len(column) - 3)):
                column[i].visible = False
        self.update_board()

    def gather_deck(self):
        for col in self.columns:
            self.deck += col
            col.clear()
        cards.shuffle(self.deck)
    # </editor-fold>

    # <editor-fold: Updates and misc helper functions>
    def check_winstate(self):
        """
        Check if the game has been won
        Specifically, checks to see if all cards
        are in piles.
        :return: bool representing whether the game has been won
        """
        if all(len(column) == 0 for column in self.columns) and len(self.deck) == 0: # w3schools
            print("Congratulations, you win!")

    def update_board(self):
        self.update_card_visibility()
        self.check_winstate()

    def update_card_visibility(self):
        """Updates the board to make sure cards are facing up according to solitaire rules"""
        # Flip all cards face up
        self.prune_array(self.columns)
        for column in self.columns:
            for card in column:
                card.visible = True
        # Ignoring column 1
        for column in self.columns[1:]:
            # Flip the first 3 rows face down
            for card in column[0:2]:
                card.visible = False
            # Then, flip the last card in each row face up
            column[-1].visible = True

    @staticmethod
    def rotate_cw(array_2d):
        """Rotates a 2 dimensional array 90 degrees clockwise, (gaps are filled with None)"""
        # First turn the array into a quadrilateral by filling in gaps with None
        array_2d = GameBoard.array_to_quad(array_2d)
        # Rotate the Array
        # (Source: https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python)
        array_2d = [list(r) for r in zip(*array_2d[::-1])]
        # Then Prune the extra Nones (Commented out bc found out this makes other things easier)
        # array_2d = GameBoard.prune_array(array_2d)
        return array_2d

    @staticmethod
    def mirror_y_axis(array_2d):
        """Mirrors a 2 dimensional array along the Y axis (gaps are filled with None)"""
        # First turn the array into a quadrilateral by filling in gaps with None
        array_2d = GameBoard.array_to_quad(array_2d)
        # Mirror the array
        array_2d = [i[::-1] for i in array_2d]
        # Then Prune the extra Nones (Commented out bc found out this makes other things easier)
        # array_2d = GameBoard.prune_array(array_2d)
        return array_2d

    @staticmethod
    def array_to_quad(array_2d):
        """Converts an uneven 2d array into a quadrilateral by filling in gaps with none
        (helper function for mirror_y_axis, and rotate_cw)"""
        max_width = max([len(row) for row in array_2d])
        for row in array_2d:
            for _ in range(max_width - len(row)):
                row.append(None)
        return array_2d

    @staticmethod
    def prune_array(array_2d):
        """Removes trailing Nones from a 2d array (helper function for mirror_y_axis, and rotate_cw)"""
        for row in array_2d:
            while row[-1] is None:
                row.pop()
        return array_2d
    # </editor-fold>

    # <editor-fold: move() and move() helper functions>
    def move(self, target: str, destination: int) -> bool:
        """
        # TODO: Add a better description
        :param target: The card to be moved as specified by the user
        :param destination: The destination column as specified by to user
        :return: None
        """
        card = Card.from_string(target)
        if not card:
            print("invalid card.")
            return False

        source_column = next((col for col in self.columns if card in col), None)
        if not source_column or not card.visible:
            print("Card not available for move.")
            return False

        # This looks like it has several issues
        # Does not seem to take the stack,
        # seems to have off by one errors,
        # order of operations errors,
        # and might crash in some scenarios
        # Needs to be investigated and unittested
        if destination < len(self.columns):
            column_top = self.columns[destination][-1] if self.columns[destination] else None
            if column_top is None:
                if card.rank == 'K':
                    self.save_board_state()
                    source_column.remove(card)
                    self.columns[destination].append(card)
                    self.update_board()
                    return True
            elif (card.suit == column_top.suit and
                  Card.PIPS.index(card.rank) == Card.PIPS.index(column_top.rank) - 1):
                self.save_board_state()
                source_column.remove(card)
                self.columns[destination].append(card)
                self.update_board()
                return True
        print("Invalid move.")
        return False
    # def valid_move(self, card, destination):
    #     # TODO: It seems like there's likely a bug in this function, need to investigate
    #       We actually don't need this function it seems but it should be kept
    #       in place as a safeguard if we ever need it.
    #     if destination in range(len(self.tableaus)):
    #         tableau_top = self.tableaus[destination][-1] if self.tableaus[destination] else None
    #         if tableau_top is None:
    #             return card.rank == 'A'
    #         return card.suit == tableau_top.suit and card.rank == card.PIPS[Card.PIPS.index(tableau_top.rank) + 1]
    #
    #     elif destination in range(len(self.columns)):
    #         column = self.columns[destination]
    #         column_top = column[-1] if column else None
    #         if not column_top:
    #             return card.rank == 'K'
    #         return card.suit == column_top.suit and Card.PIPS.index(card.rank) == Card.PIPS.index(column_top.rank) - 1
    #     else:
    #         return False
    # </editor-fold>

    # <editor-fold: undo() and savestate functions>
    def undo(self):
        if self.history:
            boardstate = self.history.pop()
            self.load_board_state(boardstate)
            return True
        return False

    def save_board_state(self):
        boardstate = {
            "deck": self.deck[:],
            "tableaus": [tab[:] for tab in self.tableaus],
            "columns": [col[:] for col in self.columns],
            "deals": self.deals,
        }
        self.history.append(boardstate)

    def load_board_state(self, boardstate):
        self.deck = boardstate["deck"][:]
        self.tableaus = [tab[:] for tab in boardstate["tableaus"]]
        self.columns = [col[:] for col in boardstate["columns"]]
        self.deals = boardstate["deals"]
    # </editor-fold>

    # <editor-fold: Magic Methods>
    def __str__(self):
        # TODO: Make this handle colors,
        #  also maybe see about using f-string alignment instead of the janky predefined spaces in PIPS
        self.update_card_visibility()
        # Header
        s = (f"Russian Revolver Solitaire  |  Deals:{self.deals}\n"
             f"    ")
        # Tableaus
        for tab in self.tableaus:
            s += f" {''.join([f'({tab[-1]})' if tab else f'(   )'])} "
        # Divider/Column labels
        s += f"\n---{'-----'.join([f'{i + 1}' for i,_ in enumerate(self.columns)])}---\n"
        # Columns
        columns = self.mirror_y_axis(self.rotate_cw(self.columns))
        for col in columns:
             s += f"|{'|'.join([f' {card} ' if card else f'     'for card in col])}|\n"
        return s
    # </editor-fold>


class Card:
    PIPS = [' A', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', ' 9', '10', ' J', ' Q', ' K']
    SUIT = ['♠', '♦', '♥', '♣']
    # Pattern Development at: https://regex101.com/r/vCMe6C/3
    CARD_REGEX = re.compile(r"\b(?P<rank>[23456789AJQK]|10)(?P<suit>[SCHD♠♦♥♣])\b", flags=re.IGNORECASE)
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.visible = True

    def flip(self):
        """Flips the card over"""
        self.visible = not self.visible

    # <editor-fold: magic methods>
    def __str__(self):
        # returns the rank and suit as a string hopefully
        if self.visible:
            color.fgcolor(color.RED if self.suit in {'♦', '♥'} else color.BLACK)
            return f"{self.rank}{self.suit}"
        else:
            color.fgcolor(color.BLACK)
            return "[_]"

    def __eq__(self, other):
        try:
            return (self.rank == other.rank and
                    self.suit == other.suit)
        except AttributeError:
            return self == Card.from_string(other)
    # </editor-fold>

    # <editor-fold: classmethods>
    @classmethod
    def new_deal(cls):
        # Creates a new deck
        return [cls(rank, suit) for suit in cls.SUIT for rank in cls.PIPS]

    @classmethod
    def get_varieties(cls):
        """Returns all possible combinations of suits and rank."""
        return [(rank, suit) for rank in cls.PIPS for suit in cls.SUIT]

    # @classmethod
    # def from_string(cls, target):
    #     try:
    #         rank, suit = target[:-1], target[-1]
    #         if rank in cls.PIPS and suit in cls.SUIT:
    #             return cls(rank, suit)
    #     except TypeError or IndexError:
    #         pass
    #     return None

    @staticmethod
    def from_string(string: str):
        """Assembles a Card() object from a string"""
        m = re.match(Card.CARD_REGEX, string)
        return Card(m.group("rank"), m.group("suit"))
    #</editor-fold>

    # <editor-fold: Properties>
    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        flattened_pips = [pip.strip().casefold() for pip in self.PIPS]
        value = value.casefold()
        if value in flattened_pips:
            self._rank = self.PIPS[flattened_pips.index(value)]
        else:
            raise ValueError("Invalid Rank.")

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, value):
        if value in ('S', 's', '♠'):
            self._suit = '♠'
        elif value in ('D', 'd', '♦'):
            self._suit = '♦'
        elif value in ('H', 'h', '♥'):
            self._suit = '♥'
        elif value in ('C','c','♣'):
            self._suit = '♣'
        else:
            raise ValueError("Unrecognized suit.")
    #</editor-fold>
if __name__ == "__main__":
    SolitaireUI()
