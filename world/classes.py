BASE_CLASSES = {'mechanic':{'business': 1, 'explosives': 2, 'heavy weapons': 2, 'intellect': 2, 'mechanical': 3, 'piloting': 1,
                            'salvage': 3, 'security': 3, 'streetwise': 1},
                'soldier': {'athletics': 2, 'command': 1, 'dodge': 1, 'explosives': 1, 'firearms':3, 'heavy weapons': 3, 'medicine': 2,
                            'melee': 3, 'quickdraw': 1, 'survival': 1},
                'scoundrel': {'athletics': 1, 'dodge': 2, 'firearms': 1, 'gambling': 2, 'influence': 1, 'mechanical': 1, 'perception':2,
                              'piloting': 2, 'quickdraw': 2, 'stealth': 2, 'streetwise': 2},
                'scout': {'athletics': 2, 'dodge': 2, 'explosives': 1, 'melee': 1, 'perception': 1, 'piloting': 1, 'quickdraw': 1,
                          'salvage': 2, 'stealth': 3, 'streetwise': 1, 'survival': 3},
                'noble': {'business': 3, 'command': 3, 'gambling': 2, 'influence': 3, 'intellect': 2, 'medicine': 2, 'perception': 2,
                          'security': 1}
                }


BASE_PRESTIGE = {'demolitionist':
                     {'explosives': 5, 'heavy weapons': 3, 'intellect': 4, 'perception': 3, 'salvage': 3},
                 'tinkerer':
                     {'explosives': 3, 'intellect': 4, 'mechanical': 5, 'perception': 3, 'salvage': 3},
                 'slicer':
                     {'business': 3, 'intellect': 4, 'security': 5, 'stealth': 3, 'streetwise': 3},
                 'repo man':
                     {'firearms': 3, 'gambling': 3, 'perception': 3, 'piloting': 4, 'salvage': 5},
                 'athlete':
                     {'athletics': 5, 'dodge': 4, 'medicine': 3, 'melee': 3, 'survival': 3},
                 'mogul':
                     {'business': 5, 'command': 3, 'influence': 4, 'intellect': 3, 'security': 3},
                 'officer':
                     {'command': 5, 'dodge': 3, 'firearms': 4, 'influence': 3, 'perception': 3},
                 'escape artist':
                     {'dodge': 5, 'firearms': 4, 'piloting': 3, 'streetwise': 3, 'survival': 3},
                 'trooper':
                     {'dodge': 3, 'firearms': 5, 'heavy weapons': 4, 'melee': 3, 'quickdraw': 3},
                 'hustler':
                     {'firearms': 3, 'gambling': 5, 'quickdraw': 4, 'security': 3, 'streetwise': 3},
                 'gunner':
                     {'dodge': 3, 'firearms': 4, 'heavy weapons': 5, 'melee': 3, 'perception': 3},
                 'politician':
                     {'business': 3, 'command': 3, 'influence': 5, 'intellect': 3, 'perception': 4},
                 'academic':
                     {'business': 3, 'intellect': 5, 'medicine': 3, 'piloting': 3, 'security': 4},
                 'physician':
                     {'command': 3, 'intellect': 4, 'medicine': 5, 'perception': 3, 'survival': 3},
                 'duelist':
                     {'athletics': 3, 'dodge': 4, 'melee': 5, 'perception': 3, 'quickdraw': 3},
                 'observer':
                     {'mechanical': 3, 'perception': 5, 'salvage': 3, 'streetwise': 3, 'survival': 4},
                 'ace':
                     {'command': 3, 'firearms': 3, 'heavy weapons': 3, 'piloting': 5, 'perception': 4},
                 'gunslinger':
                     {'dodge': 3, 'firearms': 4, 'heavy weapons': 3, 'quickdraw': 5, 'stealth': 3},
                 'ninja':
                     {'dodge': 3, 'perception': 3, 'security': 4, 'stealth': 5, 'survival': 3},
                 'thug':
                     {'business': 3, 'firearms': 3, 'perception': 4, 'quickdraw': 3, 'streetwise': 5},
                 'survivalist':
                     {'athletics': 3, 'gambling': 3, 'medicine': 4, 'salvage': 3, 'survival': 5}}


FORCE_BASE_CLASSES = {'knowledge':
                          {'attack': 1, 'defend': 1, 'neutral': 3},
                      'defense':
                          {'attack': 1, 'defend': 3, 'neutral': 1},
                      'aggression':
                          {'attack': 3, 'defend': 1, 'neutral': 1}}


FORCE_PRESTIGE_CLASSES = {'warrior':
                              {'attack': 4, 'defend': 3, 'neutral': 2},
                          'consular':
                              {'attack': 2, 'defend': 3, 'neutral': 4},
                          'guardian':
                              {'attack': 2, 'defend': 4, 'neutral': 3},
                          'sentinel':
                              {'attack': 4, 'defend': 2, 'neutral': 3},
                          'champion':
                              {'attack': 3, 'defend': 4, 'neutral': 2},
                          'shaman':
                              {'attack': 3, 'defend': 2, 'neutral': 4},
                          'adept':
                              {'attack': 3, 'defend': 3, 'neutral': 3},
                          }

FORCE_MASTER_CLASSES = {'justice':
                            {'attack': 2, 'defend': 4, 'neutral': 6},
                        'onslaught':
                            {'attack': 6, 'defend': 2, 'neutral': 4},
                        'bastion':
                            {'attack': 2, 'defend': 6, 'neutral': 4},
}