from conservativechoseoptimisticordiscoveryguessstrategy import ConservativeChoseOptmisticOrDiscoveryStrategy
from wordle_state import WordleGameState
from functions import load_words, get_word_score_df, get_best_word_according_to_the_state

answers_df = load_words('res/wordle-answers.txt')
guesses_df = load_words('res/wordle-guesses.txt')

guesses_score_df, answers_score_df = get_word_score_df(guesses_df, answers_df)

state = WordleGameState()

while True:
    guess = get_best_word_according_to_the_state(state,
                                                guesses_score_df,
                                                answers_score_df,
                                                ConservativeChoseOptmisticOrDiscoveryStrategy())
    if not guess:
        print('Error: program failed to produce a guess word.')
        break

    print('Guess: ' + guess)
    feedback = input('Feedback 5x(B/Y/G) ("exit" to exit): ')

    if feedback == 'exit':
        break

    if feedback == 'GGGGG':
        print('Win!')

    if len(feedback) != 5 or any(ch not in "BYG" for ch in feedback):
        continue

    state.add_guess(guess, list(feedback))