import pandas
from typing import Optional

from wordle_state import WordleGameState 

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

def get_word_score_df(words_df: pandas.DataFrame) -> pandas.DataFrame:
    letter_counts_df = get_letter_counts_per_column(words_df)

    def score_fn(word):
        return sum(letter_counts_df.at[word[i], i] for i in range(5))

    word_score_df = pandas.DataFrame({ 
        'word': words_df.apply(lambda row: ''.join(row), axis=1),
        'score': words_df.apply(lambda row: ''.join(row), axis=1).apply(score_fn).astype(int)
    })

    return word_score_df


def get_best_word_accordind_to_the_state(state: WordleGameState,
                                         word_score_df: pandas.DataFrame
                                         ) -> Optional[str]:
    green = state.get_green_letters()
    yellow_positions = state.get_yellow_positions()
    absent_letters = state.get_absent_letters()

    def is_valid(word):
        word = word.upper()
 
        for i, g in enumerate(green):
            if g is not None and word[i] != g:
                return False
 
        for i, letters in enumerate(yellow_positions):
            for y in letters:
                if word[i] == y:
                    return False
                if y not in word:
                    return False
 
        for letter in absent_letters:
            if letter in [letter if green[i] == None else None for i, letter in enumerate(word)]:
                return False

        return True

    filtered = word_score_df[word_score_df['word'].apply(is_valid)]

    if filtered.empty:
        return None
    
    best_index = filtered['score'].idxmax()
    
    return filtered.at[best_index, 'word']
