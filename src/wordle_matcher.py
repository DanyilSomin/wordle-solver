class WordleMatcher:
    def __init__(self, secret_word):
        self.secret = secret_word.lower()


    def match(self, guess_word):
        guess = guess_word.lower()
        result = ['B'] * 5
        secret_letters = list(self.secret)
        guess_letters = list(guess)

        for i in range(5):
            if guess_letters[i] == secret_letters[i]:
                result[i] = 'G'
                secret_letters[i] = None

        for i in range(5):
            if result[i] == 'B' and guess_letters[i] in secret_letters:
                result[i] = 'Y'
                secret_letters[secret_letters.index(guess_letters[i])] = None

        return result
