from evennia.contrib import rplanguage


def setup_languages():
    add_binary()


def add_binary():
    phonemes = "w b d t oe, ee, oo"
    vowels = "oei"
    grammar = "cvvv cvv cvvcv cvvcvv cvvvc cvvvcvv cvvc c v cc vv"
    word_length_variance = 4
    rplanguage.add_language(key='Binary', phonemes=phonemes, grammar=grammar,
                            word_length_variance=word_length_variance, vowels=vowels, force=True)
