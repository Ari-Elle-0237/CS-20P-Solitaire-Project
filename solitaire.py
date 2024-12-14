"""
Assignment #5: Solitaire
integer_set.py
by Ariel Zepezauer (arielzepezauer@gmail.com) and Aidan Raggio (Aidanpraggio@gmail.com)
Pengo: 'azepezau' & 'araggio'
Test Cases in unittest_.py
Repository at: https://github.com/Ari-Elle-0237/CS-20P-Solitaire-Project.git
Due: Nov 28th 2024
Exit Code: 0
"""
import re
import cards
import color
import pickle
import enum
import copy

class Card:
    """Class for a standard playing card, includes ability to set faceup/down and utils for generating cards"""
    PIPS = [' A', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', ' 9', '10', ' J', ' Q', ' K']
    SUIT = ['♠', '♦', '♥', '♣']
    BACK = "[_]"
    # Pattern Development at: https://regex101.com/r/vCMe6C/3
    # Matches a string like "As" or "10♦" into named capture groups for rank and suit (see: rank_suit_from_regex())
    CARD_REGEX = re.compile(r"\b(?P<rank>[23456789AJQK]|10)(?P<suit>[SCHD♠♦♥♣])\b", flags=re.IGNORECASE)
    def __init__(self, rank: str, suit: str=None):
        if suit is None: # Allow for instantiation with only one argument
            self.rank, self.suit = self.rank_suit_from_regex(rank)
        else:
            self.rank = rank
            self.suit = suit
        # Cards begin face up
        self.visible = True

    def flip(self):
        """Flips the card over by toggling self.visible"""
        self.visible = not self.visible

    # <editor-fold: magic methods>
    def __str__(self):
        """Prints rank/suit if visible otherwise prints Card.BACK, applying the correct color based on suit"""
        if self.visible:
            color.fgcolor(color.RED if self.suit in {'♦', '♥'} else color.BLACK)
            return f"{self.rank}{self.suit}"
        else:
            color.fgcolor(color.BLACK)
            return Card.BACK

    def __eq__(self, other):
        """Can Match other Card() objects, and autoapplies Card.from_string() for strings"""
        try:
            return (self.rank == other.rank and
                    self.suit == other.suit)
        except AttributeError:
            return self == Card.from_string(other)
    # </editor-fold>

    # <editor-fold: staticmethods>
    @staticmethod
    def new_deal() -> list:
        """Like get_varieties(), but creates Card() objects instead, thus generating a standard 52 card deck"""
        return [Card(rank, suit) for rank, suit in Card.get_varieties()]

    @staticmethod
    def get_varieties():
        """Returns all possible combinations of suits and rank."""
        return [(rank, suit) for rank in Card.PIPS for suit in Card.SUIT]

    @staticmethod
    def from_string(string: str):
        """Assembles a Card() object from a string"""
        return Card(*Card.rank_suit_from_regex(string))

    @staticmethod
    def rank_suit_from_regex(string:str)->tuple[str, str]:
        m = re.match(Card.CARD_REGEX, string)
        if not m:
            raise TypeError(f"Could not form card from user input {string}")
        return m.group("rank"), m.group("suit")
    #</editor-fold>

    # <editor-fold: Properties>
    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value: str):
        """Case and whitespace insensitive, will always set a value from self.PIPS,
           and can handle any output from rank_suit_from_regex()"""
        flattened_pips = [pip.strip().casefold() for pip in self.PIPS]
        value = value.strip().casefold()
        if value in flattened_pips:
            # I do not understand why there's a warn here on 'value' but it seems to work fine
            self._rank = self.PIPS[flattened_pips.index(value)]
        else:
            raise ValueError(f"Invalid Rank: {value}")

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, value: str):
        """Case and whitespace insensitive, will always set a value from self.SUITS
           and can handle any output from rank_suit_from_regex()"""
        value = value.strip().casefold()
        if value in ('s', '♠'):
            self._suit = '♠'
        elif value in ('d', '♦'):
            self._suit = '♦'
        elif value in ('h', '♥'):
            self._suit = '♥'
        elif value in ('c','♣'):
            self._suit = '♣'
        else:
            raise ValueError(f"Unrecognized suit: {value}")
    #</editor-fold>


class SolitaireUI:
    """A class for the UI and manual save/load features, should not handle any game logic"""
    def __init__(self):
        self.running = True
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
            # Can't tell why theres a warn here, seems to behave fine
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

    def process_command(self, user_input: str):
        """
        Breaks a string input into a command and arguments and sends that data to the appropriate function
        Acts only as a redirect, should not handle any actual logic
        (case/whitespace insensitive)
        """
        user_input = user_input.strip().casefold()
        # Simple command dict (commands without arguments)
        COMMANDS = {
            "exit": self.exit,
            "help": self.help_message,
            "shuf": self.shuffle,
            "cheat": self.cheat,
            "undo": self.undo,
            "save": self.save_game,
            "load": self.load_game,
        }
        # Check against our dict of simple commands to see if we can just execute it immediately and return early
        if user_input in COMMANDS:
            COMMANDS[user_input]()
            return
        # If not, assume we're moving a card and prepare to pass it along to move() using parse_command()
        arguments = self.parse_move_command(user_input)
        if arguments is None: # If malformed return early
            return
        # Otherwise send it ahead
        self.game_board.move(*arguments)

    def parse_move_command(self, user_input:str)-> tuple[Card, int|None]|None:
        """Sanitizes a user input to be passed to move(),
           returns None and prints an error message if malformed"""
        arguments = user_input.strip().casefold().split(" ")
        # First verify appropriate argument signature
        if len(arguments) == 0:
            print("No command given")
            return None
        if len(arguments) > 2:
            print(f"Malformed command, too many arguments given. Expected 1 or 2, "
                  f"Instead Got {len(arguments)}: {arguments}\n")
            return None
        # Then try to convert the first argument into a Card() object which represents the card to be moved
        target_card = arguments[0]
        try:
            target_card = Card(target_card)
        except TypeError as e: # Print an error if we fail and return None
            print(e)
            return None
        # If the second argument is not given, destination is set to None,
        if len(arguments) == 1:
            destination = None
            return target_card, destination
        # Otherwise check if it's an integer in the appropriate range representing a destination column
        destination = arguments[1]
        if destination.isdigit() and 1 <= int(destination) <= self.game_board.COL_COUNT:
            destination = int(destination) # If we succeed we can return and pass it along
            return target_card, destination - 1 # (Subtracting one to account for 0-indexing)
        else: # Otherwise error out
            print(f"Malformed command, Could not recognize user input, expected an integer between 1 and "
                  f"{self.game_board.COL_COUNT} or None.\n"
                  f"Instead got: {destination}")
            return None


class GameBoard:
    """
    A class defining a solitaire board, handles all game logic, but not the UI

    Note from Ari: I did not realize until far too late that Tableau is actually also meant to refer to
    "tableau columns", and what I'm using the term for here should actually be called "foundation piles"
    however the symmetry of tab and col both being 3 characters makes the code look neat so I have decided
    not to fix this.
    """
    TAB_COUNT = 4 # Tableau Count
    COL_COUNT = 6 # Column Count
    def __init__(self):
        # Generate a new 52 card deck
        self.deck = Card.new_deal()
        cards.shuffle(self.deck)
        # Set starting values
        self.tableaus = [[] for _ in range(self.TAB_COUNT)]
        self.columns =  [[] for _ in range(self.COL_COUNT)]
        self.deals = 6
        self.history = []
        # And begin
        self.deal_cards()

    # <editor-fold: Setup functions>
    def deal_cards(self):
        """Takes the contents of the deck and then deals them onto the board according to Russian Revolver rules"""
       # TODO: This seems to work fine, but it needs commenting
       # TODO: And a unittest to verify it handles smaller deck sizes according to the rules without error
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
        """Moves the contents of all columns on the board into the deck, and then shuffles it"""
        self.prune_array(self.columns)
        for col in self.columns:
            self.deck += col
            col.clear()
        cards.shuffle(self.deck)
    # </editor-fold>

    # <editor-fold: Updates and misc helper functions>
    def update_board(self):
        """Bundles checks that need to be regularly performed on the board"""
        self.update_card_visibility()
        self.check_winstate()

    def check_winstate(self) -> bool:
        """
        Check if the game has been won by checking if all cards are in piles.
        :return: bool representing whether the game has been won
        """
        if all(len(column) == 0 for column in self.columns) and len(self.deck) == 0: # w3schools
            print("Congratulations, you win!")
            # TODO: Make this end the game with something nicer than raising an Interrupt
            raise InterruptedError("You won!") # Temporary solution
            # return True
        return False

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
    def rotate_cw(array_2d: list[list]) -> list[list]:
        """Rectangularizes and rotates a 2 dimensional array 90 degrees clockwise, (gaps are filled with None)"""
        # First turn the array into a quadrilateral by filling in gaps with None
        array_2d = GameBoard.array_to_quad(array_2d)
        # Rotate the Array
        # (Source: https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python)
        array_2d = [list(r) for r in zip(*array_2d[::-1])]
        return array_2d

    @staticmethod
    def mirror_y_axis(array_2d: list[list]) -> list[list]:
        """Rectangularizes and mirrors a 2 dimensional array along the Y axis (gaps are filled with None)"""
        # First turn the array into a quadrilateral by filling in gaps with None
        array_2d = GameBoard.array_to_quad(array_2d)
        # Mirror the array
        array_2d = [i[::-1] for i in array_2d]
        return array_2d

    @staticmethod
    def array_to_quad(array_2d: list[list]) -> list[list]:
        """Converts an uneven 2d array into a quadrilateral by filling in gaps with none
        (helper function for mirror_y_axis, and rotate_cw)"""
        max_width = max([len(row) for row in array_2d])
        for row in array_2d:
            for _ in range(max_width - len(row)):
                row.append(None)
        return array_2d

    @staticmethod
    def prune_array(array_2d: list[list]) -> list[list]:
        """Removes trailing Nones from a 2d array (helper function for mirror_y_axis, and rotate_cw)"""
        # TODO: Check if there is a bug here when the entire list is Nones
        for row in array_2d:
            while len(row) > 0 and row[-1] is None:
               row.pop()
        return array_2d
    # </editor-fold>

    # <editor-fold: move() and move() helper functions>
    def move(self, target_card: Card, destination:int=None) -> bool:
        """
        Attempts to move a card stack from its current column to a specified
        destination column according to Russian Revolver rules
        :param destination: int: an integer from 0 to 5 (inclusive) representing
        :param target_card: Card: a Card() object determining the move
        :return bool: boolean representing whether the move was successful
        (Input sanitization can be found in Solitaire_UI.parse_move_command())
        """
        # First check if we are moving to a tableau and pass that off to the appropriate function
        if destination is None:
            return self.move_to_tableau(target_card)
        # Get the coordinates of the column where the card is located
        row, col = self.locate_card(target_card)
        # Then get the destination column
        destination_col = self.columns[destination]
        # And check if we can move
        if ((not destination_col # --------------------- If the destination is empty,
        and target_card.rank == Card.PIPS[-1]) or # ---- Only allow the move if the card is highest rank (K).
       (target_card.suit == destination_col[-1].suit # - Otherwise only allow the move is the suit matches,
        and Card.PIPS.index(target_card.rank) == # ----- And the rank is one less than the destination
        Card.PIPS.index(destination_col[-1].rank ) - 1)): # (As RR rules dictate)
            # TODO: Check for off by one errors here
            # If all our checks pass, go ahead and move the stack
            stack = self.columns[col][row::]
            self.columns[col] = self.columns[col][::row]
            self.columns[destination] += stack
            # Remembering to clean up afterwards.
            self.update_board()
            self.save_board_state()
            return True
        # If none of the above are met, return False.
        print("Could not find a valid move")
        return False

    def move_to_tableau(self, target_card: Card) -> bool:
        """Tries to move the first instance of target_card on the board to a tableau
           returns a bool value specifying if it is successful"""
        row, col = self.locate_card(target_card)
        if self.columns[col][row] != self.columns[col][-1]:
            print("Card is not at the end of a column!")
            return False
        for tab in self.tableaus:  # Then search the tableaus for a match
            # If tab is empty, check if we have an Ace
            if (not tab and target_card.rank == Card.PIPS[0] or # Otherwise check if rank is 1 less
            tab and Card.PIPS.index(target_card.rank) - 1 == Card.PIPS.index(tab[-1].rank)):
                # Move and return if we find a match
                tab.append(self.columns[col].pop())
                self.update_board()
                self.save_board_state()
                return True
        # Otherwise return False
        print("Card is not able to move to a tableau!")
        return False

    def locate_card(self, target_card: Card) -> tuple[int, int]:
        """Takes a Card() object and returns the coordinates of first
           column on the board to visibly contain that card in the format row, col"""
        self.prune_array(self.columns)
        for i, column in enumerate(self.columns):
            for j, card in enumerate(column):
                if card.visible and card == target_card:
                    return j, i
        raise ValueError(f"Card {target_card} not found or not available for move.")
    # </editor-fold>

    # <editor-fold: undo() and savestate functions>
    def undo(self):
        """Reverses the last move via pop() from self.history"""
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
        """Prints the board similar to assignment specs by rotating self.columns"""
        # TODO: Make this handle colors,
        #  also maybe see about using f-string alignment instead of the janky predefined spaces in PIPS
        # (I suspect that it may be necessary to use a separate print_board() method to handle colors,
        # but I have not studied how they work much, and I also can't get it to work at all on Windows,
        # I think this needs to be tested on Pengo)
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


if __name__ == "__main__":
    SolitaireUI()
