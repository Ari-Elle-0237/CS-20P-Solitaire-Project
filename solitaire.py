"""
Assignment #5: Solitaire
integer_set.py
by Ariel Zepezauer (arielzepezauer@gmail.com) and Luna Raggio (Aidanpraggio@gmail.com)
Pengo: 'azepezau' & 'araggio'
Test Cases in unittest_.py
Repository at: https://github.com/Ari-Elle-0237/CS-20P-Solitaire-Project.git
Due: Oct 28th 2024
Exit Code: _
"""

import cards
import color

class GameBoard:
<<<<<<< Updated upstream
    
=======
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

    pips = ['A ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', 'J ', 'Q ', 'K ']
    suit = ['♠', '♦', '♥', '♣']
    def __init__(self, rank, suit):
        self.rank = rank #Some number between 1 and 13.
        self.suit = suit
        pass

    def __str__(self):
        #returns the rank and suit as a string hopefully
        return f"{self.rank}{self.suit}"



    @classmethod
    def get_varieties(cls):
        return [(rank, suit) for rank in cls.pips for suit in cls.suit] #Returns all possible combinations for suits and rank.


>>>>>>> Stashed changes
