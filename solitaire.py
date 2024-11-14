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
        self.running = True # To be used in exit function - not yet implemented
        self.main_ui_loop()

    def main_ui_loop(self):
        while True: # What does this do??
        # Also oh god do we have to index each command manually? I mean thats not hard but
        while self.running = True:
            user_input = input("") # What do we wanna prompt the player with?
            self.process_command(user_input)

    def process_command(self, user_input):
        """
        Breaks a string input into a command and arguments and sends that data to the appropriate function
        Or if the command is malformed, enters a UI loop and returns an appropriate error

        Could use regex? Would make it very resilient to typos, but it's definitely overkill.
        """
        user_input = user_input.lower
        if user_input == "exit":
            self.exit

    def exit(self):
        """exits the ui loop"""
        self.running = False

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
        self.deals = 4
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
        for col in self.columns:
            self.deck += col
            col = []
        cards.shuffle(self.deck)
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
                card.visible = True
        # Ignoring column 1
        for column in self.columns[1:]:
            # Flip the first 3 rows face down
            for card in column[0:2]:
                card.visible = False
            # Then, flip the last card in each row face up
            column[-1].visible = True


    def check_winstate(self):
        """
        Check if the game has been won
        Specifically, checks to see if all cards
        are in piles.
        :return: bool representing whether the game has been won
        """
        if all(len(column) == 0 for column in self.columns): # we love w3schools
            # uses
            columns_empty = True
        else:
            columns_empty = False
        if len(self.deck) == 0: # If the deck = []
            deck_empty = True
        else:
            deck_empty = False
            """
            I have a feeling this should not be all that's in the argument checklist;
            But the logic checks out - columns and deck are empty, where else could the cards be?
            """
        return columns_empty and deck_empty



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
        # TODO: Make this actually like, look right, add colors, print in the right orientation etc.
        s = f"Russian Revolver Solitaire {self.deals=}"
        for tab in self.tableaus:
            s += f"{tab[-1]}"
        for col in self.columns:
            s += str(col) + '\n'
        return s


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
        self.visible = True
        pass

    def flip(self):
        """Flips the card over"""
        self.visible = not self.visible

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