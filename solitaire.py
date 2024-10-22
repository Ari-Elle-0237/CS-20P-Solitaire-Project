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
    # TODO:
    # - Store the deck
    # - Store State of board
    # - Functions for Different game actions
    # - Win detection
    def __init__(self):
        self.deck = [Card(rank, suit) for rank, suit in Card.get_varieties()]
        self.tableaus = [[] for _ in range(4)]
        self.columns =  [[] for _ in range(6)]
        cards.shuffle(self.deck)


    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):



class Card:
    def __init__(self, rank, suit):
        pass

    @classmethod
    def get_varieties(cls):
        return []

