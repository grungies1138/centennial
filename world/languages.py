from evennia.contrib import rplanguage


def setup_languages():
    add_binary()


def add_binary():
    phonemes = "w b d t io, oi, ii, oe, ee, oo, ie, ei"
    vowels = "oei"
    grammar = "cvvv cvv cvvcv cvvcvv cvvvc cvvvcvv cvvc"
    word_length_variance = 4
    rplanguage.add_language(key='Binary', phonemes=phonemes, grammar=grammar,
                            word_length_variance=word_length_variance, vowels=vowels)
