import unittest
import solitaire as sol

class MyTestCase(unittest.TestCase): # add assertion here
    def test_deal_cards(self):
        self.test_breadth_first_columns(6, 1)
        self.test_breadth_first_columns(12, 2)


    def test_breadth_first_columns(self, deck_size, expected_col_len):
        gb = sol.GameBoard() # gb: GameBoard
        gb.deck = [sol.Card('A','♣') for _ in range(deck_size)]
        print(f"{len(gb.deck)=}")
        print(f"{gb.columns=}")
        print("Dealing...")
        gb.deal_cards()
        print(f"{gb.columns=}")
        for col in gb.columns:
            self.assertEqual(expected_col_len, len(col))


    def test_can_flip_cards(self):
        pass


if __name__ == '__main__':
    unittest.main()
