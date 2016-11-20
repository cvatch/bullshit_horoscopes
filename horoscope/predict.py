import pandas as pd
import random

def get_first_word(first_word_probabilities):
    val = random.random()
    return first_word_probabilities.query('cumsum >= {}'.format(val)).iloc[0]['word1']

def get_next_word(previous_word, bigrams_probs):
    val = random.random()
    subset = bigrams_probs.query('word1 == "{}"'.format(previous_word))
    return subset.query('cumsum >= {}'.format(val)).iloc[0]['word2']


def create_sentence(first_word_probabilities, bigrams_probs):
    sentence = get_first_word(first_word_probabilities)
    previous_word = sentence
    size = 1
    while previous_word != '.':
        previous_word = get_next_word(previous_word, bigrams_probs)
        sentence += ' {}'.format(previous_word)
        size += 1
    return sentence.replace(r' .', '. ')


def create_horoscope(size, first_word_probabilities, bigrams_probs):
    horoscope = ''
    for _ in range(size):
        horoscope += create_sentence(first_word_probabilities, bigrams_probs)
    return horoscope


def load_frames(bigrams, first_words):
    bigrams_probs = pd.read_csv(bigrams, index_col=0)
    first_word_probabilities = pd.read_csv(first_words, index_col=0)
    return bigrams_probs, first_word_probabilities
