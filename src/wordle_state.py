import string
from collections import defaultdict

class WordleGameState:
    def __init__(self):
        self.rows = []

    def add_guess(self, guess: str, feedback: list):
        """feedback: list of 'G', 'Y', 'B' for green/yellow/black"""
        self.rows.append((guess.lower(), feedback))

    def display(self):
        color_codes = {
            'G': '\033[92m',  # Green
            'Y': '\033[93m',  # Yellow
            'B': '\033[90m',  # Gray (dim)
        }
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
        absent_letters = set()
 
        for guess, fb in self.rows:
            for i, code in enumerate(fb):
                if code == 'B':
                    absent_letters.add(guess[i])

        return absent_letters
    
    def green_map(self):
        green_map = defaultdict(int)
        for letter in self.get_green_letters():
            if letter != None:
                green_map[letter] += 1
        
        return green_map

    def yellow_map(self):
        green_map = self.green_map()
        yellow_map = defaultdict(int)

        for alphabet_letter in string.ascii_lowercase:
            for guess, feedback in self.rows:
                yellow_letter_count_in_a_guess = 0
                
                if guess == 'melle':
                    retwertwert=0

                for i, guess_letter in enumerate(guess):
                    if guess_letter == alphabet_letter and (feedback[i] == 'Y' or feedback[i] == 'G'):
                        yellow_letter_count_in_a_guess += 1
                
                yellow_map[alphabet_letter] = max(yellow_map[alphabet_letter], 
                                                  yellow_letter_count_in_a_guess
                                                  - green_map[alphabet_letter])
        
        return yellow_map