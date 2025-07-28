from conservativechoseoptimisticordiscoveryguessstrategy import ConservativeChoseOptmisticOrDiscoveryStrategy
from wordle_state import WordleGameState
from functions import load_words, get_word_score_df, get_best_word_according_to_the_state

answers_df = load_words('res/wordle-answers.txt')

# print(answers_df.head())

word_score_df = get_word_score_df(answers_df)

# word_score_df = word_score_df.sort_values(by='score', ascending=False).reset_index(drop=True)
# print(word_score_df.head(10))

game_state = WordleGameState()

while True:
    guess = get_best_word_according_to_the_state(game_state, word_score_df, ConservativeChoseOptmisticOrDiscoveryStrategy())

    if not guess:
        print('Error: program failed to produce a guess word.')
        break

    print('Guess: ' + guess)
    feedback = input('Feedback 5x(B/Y/G) ("exit" to exit): ')

    if feedback == 'exit':
        break

    if feedback == 'GGGGG':
        print('Win!')

    if len(feedback) != 5 and any(ch not in "BYG" for ch in feedback):
        continue

    game_state.add_guess(guess, list(feedback))