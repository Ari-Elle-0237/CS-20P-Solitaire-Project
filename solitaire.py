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

class GameBoard:
    TAB_COUNT = 4 # Tableau Count
    COL_COUNT = 6 # Column Count
    # TODO:
    # - Store the deck
    # - Store State of board
    # - Functions for Different game actions
    # - Win detection
    def __init__(self):
        self.deck = [Card(rank, suit) for rank, suit in Card.get_varieties()]
        cards.shuffle(self.deck)
        self.tableaus = [[] for _ in range(self.TAB_COUNT)]
        self.columns =  [[] for _ in range(self.COL_COUNT)]

    def __str__(self):
        print()

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._board = value

    def deal_cards(self):
        col = 0
        while self.deck:
            if col == 0 and len(self.columns[0]) >= 2: # TODO: Rephrase this to comply with class style guides
                continue
            self.columns[col].append(self.deck.pop()) # TODO: Need to test this
            col += 1 % self.COL_COUNT # TODO: This is definitely not right but something like this probably is
        self. update_flipped_cards()

    def update_flipped_cards(self):
        """
        Helper function for flipping cards on the board, works by modifying attributes inplace
        :return: None
        """
        return NotImplemented
    
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



class Card:
    def __init__(self, rank, suit):
        pass

    @classmethod
    def get_varieties(cls):
        return []

