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