import pandas
import string
from typing import Optional
from collections import Counter
from wordle_state import WordleGameState
from choseoptimisticordiscoveryguessstrategy import ChoseOptmisticOrDiscoveryStrategy

def load_words(filepath: str) -> pandas.DataFrame:
    answers_df = pandas.read_csv(filepath, header=None, names=['words'])

    answers_df = pandas.DataFrame(answers_df['words'].apply(
        lambda word: pandas.Series(list(word))
    ))

    return answers_df


def get_letter_counts_per_column(df: pandas.DataFrame) -> pandas.DataFrame:
    letter_counts_df = pandas.DataFrame({
        col: df[col].value_counts()
        for col in df.columns
    }).fillna(0).astype(int)

    return letter_counts_df


def get_word_score_df(guesses_df: pandas.DataFrame,
                      answers_df: pandas.DataFrame) -> tuple[pandas.DataFrame, pandas.DataFrame]:
    letter_counts_df = get_letter_counts_per_column(answers_df)

    def score_fn(word: str) -> int:
        def get_word_score(word, i):
            score = letter_counts_df.at[word[i], i]
            
            if word[i] in word[:i]:
                score = 0
            
            return score

        return sum(get_word_score(word, i) for i in range(5))

    def form_score_df(df: pandas.DataFrame) -> pandas.DataFrame:
        return pandas.DataFrame({ 
            'word': df.apply(lambda row: ''.join(row), axis=1),
            'score': df.apply(lambda row: ''.join(row), axis=1).apply(score_fn).astype(int)
        })

    return form_score_df(guesses_df), form_score_df(answers_df)


def is_valid_discower_guess(word: str,
                              green_positions,
                              yellow_positions,
                              absent_letters,
                              yellow_map,
                              green_map):
    word = word.lower()

    # check satisfy greens
    for letter in green_positions:
        if letter is not None and letter in word:
            return False

    # remove if yellows match 
    for i, letters in enumerate(yellow_positions):
        for y in letters:
            if word[i] == y:
                return False
            
    letter_counts = Counter(word)

    # check for yellows present and absent letters not present
    for letter in string.ascii_lowercase:
        minimum_amount = yellow_map[letter] + green_map[letter]
        strict = letter in absent_letters

        if strict and letter_counts[letter] != minimum_amount:
            return False
        elif letter_counts[letter] < minimum_amount:
            return False

    return True

    return True


def is_valid_optimistic_guess(word: str,
                              green_positions,
                              yellow_positions,
                              absent_letters,
                              yellow_map,
                              green_map):
    word = word.lower()

    if word == 'liege':
        erwerg = 0

    # remove if greens do not match
    for i, letter in enumerate(green_positions):
        if letter != None and word[i] != letter:
            return False

    # remove if yellows match 
    for i, letters in enumerate(yellow_positions):
        for y in letters:
            if word[i] == y:
                return False

    letter_counts = Counter(word)

    # check for yellows present and absent letters not present
    for letter in string.ascii_lowercase:
        minimum_amount = yellow_map[letter] + green_map[letter]
        strict = letter in absent_letters

        if strict and letter_counts[letter] != minimum_amount:
            return False
        elif letter_counts[letter] < minimum_amount:
            return False

    return True


def get_best_word_according_to_the_state(state: WordleGameState,
                                         guesses_score_df: pandas.DataFrame,
                                         answers_score_df: pandas.DataFrame,
                                         chose_optmistic_or_discovery_strategy: ChoseOptmisticOrDiscoveryStrategy
                                         ) -> Optional[str]:
    green_positions = state.get_green_letters()
    yellow_positions = state.get_yellow_positions()
    absent_letters = state.get_absent_letters()
    green_map = state.green_map()
    yellow_map = state.yellow_map()


    filtered_discovery = guesses_score_df[guesses_score_df['word'].apply(
            lambda word: is_valid_discower_guess(word,
                                                 green_positions,
                                                 yellow_positions,
                                                 absent_letters,
                                                 yellow_map,
                                                 green_map)
        )]
    
    filtered_optimistic = answers_score_df[answers_score_df['word'].apply(
            lambda word: is_valid_optimistic_guess(word,
                                                   green_positions,
                                                   yellow_positions,
                                                   absent_letters,
                                                   yellow_map,
                                                   green_map)
        )]

    optimistic = chose_optmistic_or_discovery_strategy.go_optimistic(
                    state, len(filtered_optimistic), len(filtered_discovery))

    filtered = filtered_optimistic if optimistic else filtered_discovery

    if filtered.empty:
        return None
    
    best_index = filtered['score'].idxmax()
    
    return filtered.at[best_index, 'word']
