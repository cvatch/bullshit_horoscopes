import pandas as pd
import random
import os
BASEDIR = os.path.dirname(os.path.realpath(__file__))


def get_first_word(first_word_probabilities):
    """Create first word of a sentence"""
    val = random.random()
    return first_word_probabilities.query(
        'cumsum >= {}'.format(val)).iloc[0]['word1']


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
    '''Acutally create the horoscope by adding n sentences

    Arguments:
        size (int): desired length of horoscope in sentences
        first_word_probabilties
    '''
    horoscope = ''
    for _ in range(size):
        horoscope += create_sentence(first_word_probabilities, bigrams_probs)
    return horoscope


def load_frames(
        bigrams=os.path.join(BASEDIR, 'bigrams_probs.csv'),
        first_words=os.path.join(BASEDIR, 'first_world_probabilities.csv')):
    '''Load dataframes containing probabilities of first words
    and all bigrams


    generally, the bigrams df has columns 'word1', 'word2', 'probabiltiy', 'cumsum'
    first_word_probabilties has columns 'word1', 'probabiltiy', 'cumsum'

    Arguments (in vanilla setup):
        bigrams (str): "bigram_probs.csv"
        first_words (str): "first_world_probabilities.csv"

    Retruns:
        pandas dataframes
    '''
    bigrams_probs = pd.read_csv(bigrams, index_col=0)
    first_word_probabilities = pd.read_csv(first_words, index_col=0)
    return bigrams_probs, first_word_probabilities
