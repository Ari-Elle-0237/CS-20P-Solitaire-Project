"""
Assignment #5: Solitaire
integer_set.py
by Ariel Zepezauer (arielzepezauer@gmail.com) and Luna Raggio (Aidanpraggio@gmail.com)
Pengo: 'azepezau' & 'araggio'
Test Cases in unittest_.py
Repository at: https://github.com/Ari-Elle-0237/CS-20P-Solitaire-Project.git
Due: Nov 28th 2024
Exit Code: _
"""

import cards
import color

class SolitaireUI:
    """
    A class for the UI
    """
    def __init__(self):
        self.main_ui_loop()

    def main_ui_loop(self):
        while True:
            return NotImplemented

    def process_command(self, user_input):
        """
        Breaks a string input into a command and arguments and sends that data to the appropriate function
        Or if the command is malformed, enters a UI loop and returns an appropriate error

        Could use regex? Would make it very resilient to typos, but it's definitely overkill.
        """
        return NotImplemented

    def exit(self):
        """exits the ui loop"""
        return NotImplemented

class GameBoard:
    """
    A class defining a solitaire board
    TODO:
    - Decide if it makes sense to make the board and the game separate classes
    - Write unittests
    - Fill in unimplemented functions
    - Stretch goal: Add support for classic and spider solitaire rulesets
    """
    TAB_COUNT = 4 # Tableau Count
    COL_COUNT = 6 # Column Count
    def __init__(self):
        self.deck = [Card(rank, suit) for rank, suit in Card.get_varieties()]
        cards.shuffle(self.deck)
        self.tableaus = [[] for _ in range(self.TAB_COUNT)]
        self.columns =  [[] for _ in range(self.COL_COUNT)]
        self.history = []

    # <editor-fold: Setup functions>
    def deal_cards(self):
        # TODO: make the first column be dealt first
        col = 0
        while self.deck:
            if col == 0 and len(self.columns[0]) >= 2: # TODO: Rephrase this to comply with class style guides
                continue
            self.columns[col].append(self.deck.pop()) # TODO: Need to test how pop() works
            col += 1
            col %= self.COL_COUNT
        self.update_board()

    def gather_deck(self):
        """Function that collects all cards on the board not in a tableau and shuffles them into the deck"""
        """
        Loop over all the columns
        Copy their contents into self.deck
        Clear them
        Then Shuffle the deck
        """
        """
        Before:
        Columns = [[Card(),Card(),Card()],[Card(),...],[Card(),...],[]...]
        Deck = [a list of things]
        After:
        Columns = [[],[],[],[],[],[]]
        Deck = [a list of things, Card(),Card(),Card()...]
        """
        return NotImplemented
    # </editor-fold>

    # <editor-fold: Updates and misc helper functions>
    def update_board(self):
        self.update_flipped_cards()
        self.check_winstate()

    def update_card_visibility(self):
        """Updates the board to make sure cards are facing up according to solitaire rules"""
        # TODO: See if this can be shortened or given improved readability with some list comprehensions
        # TODO: Write a unittest for this function
        # Flip all cards face up
        for column in self.columns:
            for card in column:
                card.face_up = True
        # Ignoring column 1
        for column in self.columns[1:]:
            # Flip the first 3 rows face down
            for card in column[0:2]:
                card.face_up = False
            # Then, flip the last card in each row face up
            column[-1].face_up = True


    def check_winstate(self):
        """
        Check if the game has been won
        :return: bool representing whether the game has been won
        """
        return NotImplemented
    # </editor-fold>

    # <editor-fold: move() and move() helper functions>
    def move(self, target, destination=None):
        """

        :param target: The card to be moved as specified by the user
        :param destination: The destination column as specified by to user
        :return: None
        """
        return NotImplemented


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
        """Undo to the last move"""
        return NotImplemented

    def save_board_state(self):
        """Creates a savestate of the board and adds it to self.history"""
        return NotImplemented

    def load_board_state(self, boardstate):
        """
        Loads a boardstate
        :param boardstate: (structure of this not yet decided)
        :return: None
        """
        return NotImplemented
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
        return NotImplemented

    def __repr__(self):
        return NotImplemented
    # </editor-fold>


class Card:
    # TODO:
    #  - Implement card face up/ face down
    #  - Make it so suits will accept either the unicode or ascii representation
    #    (make it so the code treats '♣' as equivalent to 'c', this logic can be implemented in the setter function)
    #  - Make Cards print with color
    #  - Implement __repr__()
    #  - Sanitize inputs
    PIPS = ['A ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', 'J ', 'Q ', 'K ']
    SUIT = ['♠', '♦', '♥', '♣']
    def __init__(self, rank, suit):
        self.rank = rank # Some number between 1 and 13.
        self.suit = suit
        self.face_up = True
        pass

    def flip(self):
        """Flips the card over"""

    def __str__(self):
        # returns the rank and suit as a string hopefully
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        # returns the rank and suit as a string hopefully
        return f"{self.rank}{self.suit}"

    @classmethod
    def get_varieties(cls):
        """Returns all possible combinations of suits and rank."""
        return [(rank, suit) for rank in cls.PIPS for suit in cls.SUIT]

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        self._rank = value

    @property
    def suit(self):
        # TODO: implement input sanitization
        return self._suit

    @suit.setter
    def suit(self, value):
        # TODO: sanitize inputs and translate synonyms to the appropriate unicode
        self._suit = value

# This Comment here is a test lmk if you can see it after accepting the pull request
