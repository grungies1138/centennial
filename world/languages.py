from evennia.contrib import rplanguage


def setup_languages():
    add_binary()
    add_ryl()
    add_shyriiwook()
    add_huttese()


def add_binary():
    phonemes = "w b d p t ooo eee ee oo e o a aa aaa wh dw bw E EE O OO A AA B"
    vowels = "oea"
    grammar = "cvvv cvv cvvcv cvvcvv cvvvc cvvvcvv cvvc c v cc vv ccvvc ccvvccvv "
    word_length_variance = 4
    rplanguage.add_language(key='Binary', phonemes=phonemes, grammar=grammar,
                            word_length_variance=word_length_variance, vowels=vowels, force=True)


def add_ryl():
    phonemes = "rhy rh ry mh a b c d e f g h i j k l m n o p q r s t u v w x y z th sh"
    vowels = "aeiouy"
    grammar = "ccv cvv ccvv cccv cv v cvvv ccvvv cvvcv ccvvcv ccvvccvv ccvcvvv"
    word_length_variance = 3
    rplanguage.add_language(key='Ryl', phonemes=phonemes, grammar=grammar, word_length_variance=word_length_variance,
                            vowels=vowels, force=True)


def add_shyriiwook():
    phonemes = "wh wrr wr grr gr ah aa oo ugh ee arr a e o"
    vowels = "aeo"
    grammar = "ccv ccvv ccvvv ccvvvv cccv cccvv cccvvv cccvvvv ccvcc ccvccc ccvvcc ccvvvcc ccvvvccc cccvvvcc " \
              "cccvvvccc cv cc c v"
    word_length_variance = 3
    rplanguage.add_language(key='Shyriiwook', phonemes=phonemes, vowels=vowels, grammar=grammar,
                            word_length_variance=word_length_variance, force=True)


def add_huttese():
    phonemes = "bh sh d b s wh w h a e i o u aa ao ou wh w"
    vowels = "aeiou"
    grammar = "cvv ccvv ccvvc ccvvcc ccvvccv cvvc cvvcv cvvcvcc ccvvcvcc cc vv c v"
    word_length_variance = 2
    rplanguage.add_language(key='Huttese', phonemes=phonemes, vowels=vowels, grammar=grammar,
                            word_length_variance=word_length_variance, force=True)
