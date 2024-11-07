import unittest
import solitaire as sol

class RussianRevolverTestCase(unittest.TestCase):
    # TODO: Write a lot more tests

    def test_deal_cards(self):
        # TODO: realized these tests are wrong, as they don't account for column 1 priority
        self.check_breadth_first_columns(6, 1)
        self.check_breadth_first_columns(12, 2)


    def check_breadth_first_columns(self, deck_size, expected_col_len):
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
