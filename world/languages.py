from evennia.contrib import rplanguage


def setup_languages():
    add_binary()


def add_binary():
    phonemes = "w b d p t ooo eee ee oo e o a aa aaa wh dw bw E EE O OO A AA B"
    vowels = "oea"
    grammar = "cvvv cvv cvvcv cvvcvv cvvvc cvvvcvv cvvc c v cc vv ccvvc ccvvccvv "
    word_length_variance = 4
    rplanguage.add_language(key='Binary', phonemes=phonemes, grammar=grammar,
                            word_length_variance=word_length_variance, vowels=vowels, force=True)
