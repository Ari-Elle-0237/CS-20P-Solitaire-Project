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

    def help_message(self):
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
        try:
            with open(filename, 'rb') as file:
                pickle.dump(self.game_board, file)
            print("Gamestate saved successfully.")
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_game(self):
        filename = input("Enter filename to load the gamestate from: ")
        try:
            with open(filename, 'rb') as file:
                self.game_board = pickle.load(file)
            print("Game loaded.")
        except Exception as e:
            print(f"Error loading game: {e}")

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

        Could use regex? Would make it very resilient to typos, but it's definitely overkill.
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
        if user_input in commands:
            commands[user_input]()
        else:
            print("Invalid Command.")

class GameBoard:
    """
    A class defining a solitaire board
    """
    TAB_COUNT = 4 # Tableau Count
    COL_COUNT = 6 # Column Count
    def __init__(self):
        if self.COL_COUNT <= 0:
            raise ValueError("Column count must be greater than 0.")

        self.deck = Card.new_deal() # Previously [Card(rank, suit) for rank, suit in Card.get_varieties()]
        cards.shuffle(self.deck)
        self.tableaus = [[] for _ in range(self.TAB_COUNT)]
        self.columns =  [[] for _ in range(self.COL_COUNT)]
        self.deals = 6
        self.history = []
        self.deal_cards()


    def update_card_visibility(self):
        for column in self.columns:
            for i, card in enumerate(column):
                card.visible = i == len(column) - 1


    def check_winstate(self):
        """
        Check if the game has been won
        Specifically, checks to see if all cards
        are in piles.
        :return: bool representing whether the game has been won
        """
        if all(len(column) == 0 for column in self.columns) and len(self.deck) == 0: # w3schools
            print("Congratulations, you win!")
            '''
            columns_empty = True
        else:
            columns_empty = False
        if len(self.deck) == 0: # If the deck = []
            deck_empty = True
        else:
            deck_empty = False

        return columns_empty and deck_empty
        '''

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

            '''
            if col == 0 and len(self.columns[0]) >= 2: # TODO: Rephrase this to comply with class style guides
                continue
            self.columns[col].append(self.deck.pop()) # TODO: Need to test how pop() works
            col += 1
            col %= self.COL_COUNT
             self.update_board()
            '''




    def gather_deck(self):
        for col in self.columns:
            self.deck += col
            col.clear()
        cards.shuffle(self.deck)
    # </editor-fold>

    # <editor-fold: Updates and misc helper functions>


    def update_card_visibility(self):
        """Updates the board to make sure cards are facing up according to solitaire rules"""
        # TODO: See if this can be shortened or given improved readability with some list comprehensions
        # TODO: Write a unittest for this function
        # Flip all cards face up
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

    # </editor-fold>

    # <editor-fold: move() and move() helper functions>
    def move(self, target, destination):
        """

        :param target: The card to be moved as specified by the user
        :param destination: The destination column as specified by to user
        :return: None
        """
        card = Card.from_string(target)
        '''
        if card is None:
            print(f"invalid card: {target}.")
            return
        if destination is None:
            print("No destination.")
            return
        if destination < 0 or destination >= len(self.columns) + >= len(self.tableaus):
            print("Invalid destination.")
            return
        if not self.valid_move(card, destination):
            print(f"invalid move: {target} to {destination}")
            return
        self.columns[destination].append(card)
        self.update_board()
        '''
        if not card:
            print("invalid card.")
            return False

        source_column = next((col for col in self.columns if card in col), None)
        if not source_column or not card.visible:
            print("Card not available for move.")
            return False

        if destination < len(self.columns):
            column_top = self.columns[destination][-1] if self.columns[destination] else None
            if column_top is None:
                if card.rank == 'K':
                    self.save_board_state()
                    source_column.remove(card)
                    self.columns[destination].append(card)
                    self.update_board()
                    return True
            elif card.suit == column_top.suit and Card.PIPS.index(card.rank) == Card.PIPS.index(column_top.rank) - 1:
                self.save_board_state()
                source_column.remove(card)
                self.columns[destination].append(card)
                self.update_board()
                return True
        print("Invalid move.")
        return False

    def valid_move(self, card, destination):
        if destination in range(len(self.tableaus)):
            tableau_top = self.tableaus[destination][-1] if self.tableaus[destination] else None
            if tableau_top is None:
                return card.rank == 'A'
            return card.suit == tableau_top.suit and card.rank == card.PIPS[Card.PIPS.index(tableau_top.rank) + 1]

        elif destination in range(len(self.columns)):
            column = self.columns[destination]
            column_top = column[-1] if column else None
            if not column_top:
                return card.rank == 'K'
            return card.suit == column_top.suit and Card.PIPS.index(card.rank) == Card.PIPS.index(column_top.rank) - 1
        else:
            return False


    def check_destination(self, destination=None):
        """
        Helper function for move()
        :param destination: Target column, if None, the destination is assumed to be a tableau
        :return: bool
        """
        return NotImplemented

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

    # <editor-fold: Properties>
    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._board = value
    # </editor-fold>

    # <editor-fold: Magic Methods>
    def __str__(self):
        strbrd = f"Russian Revolver Solitaire\nShuffles left: {self.deals}\n"
        for i, col in enumerate(self.columns):
            strbrd += f"Column {i+1}: {[str(card) for card in col]}\n"
        for i, tab in enumerate(self.tableaus):
            strbrd += f"Tableau {i+1}: {tab}\n"
        return strbrd


    def __repr__(self):
        return NotImplemented
    # </editor-fold>


class Card:
    # TODO:
    #  - Sanitize inputs
    PIPS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    SUIT = ['♠', '♦', '♥', '♣']


    def __init__(self, rank, suit):
        self.rank = rank # Some number between 1 and 13.
        self.suit = suit
        self.visible = True

    def flip(self):
        """Flips the card over"""
        self.visible = not self.visible

    def __str__(self):
        # returns the rank and suit as a string hopefully
        if self.visible:
            color.fgcolor(color.RED if self.suit in {'♦', '♥'} else color.BLACK)
            return f"{self.rank}{self.suit}"
        else:
            color.fgcolor(color.BLACK)
            return "[X]"

    def __repr__(self):
        # returns the rank and suit as a string hopefully
        return str(self)

    @classmethod
    def new_deal(cls):
        # Creates a new deck
        return [cls(rank, suit) for suit in cls.SUIT for rank in cls.PIPS]

    @classmethod
    def get_varieties(cls):
        """Returns all possible combinations of suits and rank."""
        return [(rank, suit) for rank in cls.PIPS for suit in cls.SUIT]

    @classmethod
    def from_string(cls, target):
        try:
            rank, suit = target[:-1], target[-1]
            if rank in cls.PIPS and suit in cls.SUIT:
                return cls(rank,suit)
        except:
            pass
        return None

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        if value in Card.PIPS:
            self._rank = value
        else:
            raise ValueError("Invalid Rank.")

    @property
    def suit(self):
        # TODO: implement input sanitization
        return self._suit

    @suit.setter
    def suit(self, value):
        # TODO: sanitize inputs and translate synonyms to the appropriate unicode

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

if __name__ == "__main__":
    try:
        SolitaireUI()
    except Exception as e:
        print(f"An error occurred: {e}")