from concurrent.futures import ProcessPoolExecutor
from conservativechoseoptimisticordiscoveryguessstrategy import ConservativeChoseOptmisticOrDiscoveryStrategy
from wordle_state import WordleGameState
from wordle_matcher import WordleMatcher
from functions import load_words, get_word_score_df, get_best_word_according_to_the_state

answers_df = load_words('res/wordle-answers.txt')
guesses_df = load_words('res/wordle-guesses.txt')

# print(answers_df.head())

guesses_score_df, answers_score_df = get_word_score_df(guesses_df, answers_df)

# answers_score_df = answers_score_df.sort_values(by='score', ascending=False).reset_index(drop=True)
# print(answers_score_df.head(10))

# guesses_score_df = guesses_score_df.sort_values(by='score', ascending=False).reset_index(drop=True)
# print(guesses_score_df.head(10))

def play(answer: str) -> tuple[bool, int, str]:
    matcher = WordleMatcher(answer)
    state = WordleGameState()

    while True:
        guess = get_best_word_according_to_the_state(state,
                                                    guesses_score_df,
                                                    answers_score_df,
                                                    ConservativeChoseOptmisticOrDiscoveryStrategy())

        if not guess:
            print(answer)
            assert(False and 'Error: program failed to produce a guess word.')

        feedback = matcher.match(guess)
        state.add_guess(guess, list(feedback))

        if feedback == list('GGGGG'):
            return True, len(state.rows), answer

        if len(feedback) != 5 or any(ch not in 'BYG' for ch in feedback):
            assert(False and 'Wrong feedback!')

        if len(state.rows) > 5:
            break

    return False, len(state.rows), answer

words = answers_df.apply(lambda row: ''.join(row), axis=1).tolist()

total_words = len(words)
total_wins = 0
total_guesses = 0


def main():
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(play, words))

    total_wins = sum(1 for win, _, _ in results if win)
    total_guesses = sum(guesses for win, guesses, _ in results if win)
    failed_words = [word for win, _, word in results if not win]

    print('total_words: ' + str(len(words)))
    print('total_wins: ' + str(total_wins))
    print('%_wins: ' + str(total_wins / total_words))
    print('awerage_guesses_in_wins: ' + str(total_guesses / total_wins))
    print('Fails: ' + ' '.join(failed_words))


if __name__ == '__main__':
    main()