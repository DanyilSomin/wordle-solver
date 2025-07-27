import unittest

class WordleGameState:
    def __init__(self):
        self.rows = []

    def add_guess(self, guess: str, feedback: list):
        self.rows.append((guess.lower(), feedback))

    def display(self):
        color_codes = {'G': '\033[92m', 'Y': '\033[93m', 'B': '\033[90m'}
        reset = '\033[0m'
        for guess, fb in self.rows:
            line = ''.join(f"{color_codes[c]}{l}{reset}" for l, c in zip(guess, fb))
            print(line)

    def get_green_letters(self):
        green_slots = [None] * 5
        for guess, fb in self.rows:
            for i, code in enumerate(fb):
                if code == 'G':
                    green_slots[i] = guess[i]
        return green_slots

    def get_yellow_positions(self):
        yellow_positions = [set() for _ in range(5)]
        for guess, fb in self.rows:
            for i, code in enumerate(fb):
                if code == 'Y':
                    yellow_positions[i].add(guess[i])
        return yellow_positions

    def get_absent_letters(self):
        present_letters = set()
        absent_letters = set()
        for guess, fb in self.rows:
            for i, code in enumerate(fb):
                if code in ('G', 'Y'):
                    present_letters.add(guess[i])
        for guess, fb in self.rows:
            for i, code in enumerate(fb):
                if code == 'B' and guess[i] not in present_letters:
                    absent_letters.add(guess[i])
        return absent_letters


class TestWordleGameState(unittest.TestCase):
    def test_empty_state(self):
        state = WordleGameState()
        self.assertEqual(state.get_green_letters(), [None]*5)
        self.assertEqual(state.get_yellow_positions(), [set() for _ in range(5)])
        self.assertEqual(state.get_absent_letters(), set())

    def test_all_green(self):
        state = WordleGameState()
        state.add_guess("apple", ['G']*5)
        self.assertEqual(state.get_green_letters(), list("APPLE"))

    def test_all_yellow(self):
        state = WordleGameState()
        state.add_guess("crane", ['Y']*5)
        self.assertEqual(state.get_yellow_positions(), [{c} for c in "CRANE"])
        self.assertEqual(state.get_absent_letters(), set())

    def test_all_blank(self):
        state = WordleGameState()
        state.add_guess("brick", ['B']*5)
        self.assertEqual(state.get_absent_letters(), set("BRICK"))

    def test_mixed_case(self):
        state = WordleGameState()
        state.add_guess("slate", ['B', 'G', 'Y', 'B', 'B'])
        self.assertEqual(state.get_green_letters(), [None, 'L', None, None, None])
        self.assertIn('A', state.get_yellow_positions()[2])
        self.assertEqual(state.get_absent_letters(), {'S', 'T', 'E'})

    def test_duplicate_letters(self):
        state = WordleGameState()
        state.add_guess("sassy", ['B', 'G', 'Y', 'B', 'B'])
        self.assertEqual(state.get_green_letters(), [None, 'A', None, None, None])
        self.assertIn('S', state.get_yellow_positions()[2])
        self.assertIn('Y', state.get_absent_letters())

    def test_repeated_greens(self):
        state = WordleGameState()
        state.add_guess("crane", ['G', 'B', 'B', 'B', 'B'])
        state.add_guess("candy", ['G', 'B', 'G', 'B', 'B'])
        self.assertEqual(state.get_green_letters(), ['C', None, 'N', None, None])
        self.assertTrue({'R', 'A', 'D', 'Y'}.issubset(state.get_absent_letters()))

    def test_yellow_then_green(self):
        state = WordleGameState()
        state.add_guess("angle", ['Y', 'B', 'B', 'B', 'B'])
        state.add_guess("eagle", ['B', 'G', 'B', 'B', 'B'])
        self.assertEqual(state.get_green_letters(), [None, 'A', None, None, None])
        self.assertIn('A', state.get_yellow_positions()[0])
        self.assertIn('E', state.get_absent_letters())

    def test_absent_not_overlapping_yellow(self):
        state = WordleGameState()
        state.add_guess("blend", ['B', 'Y', 'B', 'B', 'B'])
        self.assertIn('L', state.get_yellow_positions()[1])
        self.assertTrue({'B', 'E', 'N', 'D'}.issubset(state.get_absent_letters()))

    def test_case_insensitivity(self):
        state = WordleGameState()
        state.add_guess("CrAnE", ['G', 'Y', 'B', 'B', 'B'])
        self.assertEqual(state.get_green_letters()[0], 'C')
        self.assertIn('R', state.get_yellow_positions()[1])
        self.assertIn('A', state.get_absent_letters())


if __name__ == '__main__':
    unittest.main()
