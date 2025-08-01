import time
from select_region import select_screen_region, crop_region_to_tiles
from select_region import extract_tile_colors, type_word_at_center
from functions import load_words, get_word_score_df, get_best_word_according_to_the_state
from conservativechoseoptimisticordiscoveryguessstrategy import ConservativeChoseOptmisticOrDiscoveryStrategy
from wordle_state import WordleGameState


if __name__ == '__main__':
    answers_df = load_words('res/wordle-answers.txt')
    guesses_df = load_words('res/wordle-guesses.txt')

    guesses_score_df, answers_score_df = get_word_score_df(guesses_df, answers_df)

    state = WordleGameState()

    region = select_screen_region()
    region = crop_region_to_tiles(region)

    while True:
        guess = get_best_word_according_to_the_state(state,
                                                    guesses_score_df,
                                                    answers_score_df,
                                                    ConservativeChoseOptmisticOrDiscoveryStrategy())
        if not guess:
            print('Error: program failed to produce a guess word.')
            break

        print(f'Guess: {guess}.')
        type_word_at_center(region, guess)
        time.sleep(2)

        feedbacks = extract_tile_colors(region)
        feedback = next((row for row in reversed(feedbacks) if row), '')
        assert(len(feedback) and 'Failed to read feedback')
        
        print(f'Feedback: {feedback}.')

        if feedback == 'GGGGG':
            print('Win!')
            exit(0)

        if len(feedback) != 5 or any(ch not in "BYG" for ch in feedback):
            assert(False and 'Wrong feedback!')

        state.add_guess(guess, list(feedback))
