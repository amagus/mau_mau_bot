#!/usr/bin/env python3
#
# Telegram bot to play UNO in group chats
# Copyright (c) 2016 Jannes Höke <uno@jhoeke.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from telegram.emoji import Emoji

# Colors
RED = 'r'
BLUE = 'b'
GREEN = 'g'
YELLOW = 'y'
BLACK = 'x'

COLORS = (RED,BLUE,GREEN,YELLOW)

COLOR_ICONS = {
    RED: Emoji.HEAVY_BLACK_HEART,
    BLUE: Emoji.BLUE_HEART,
    GREEN: Emoji.GREEN_HEART,
    YELLOW: Emoji.YELLOW_HEART,
    BLACK: '⬛️'
}

# Values
ZERO = '0'
ONE = '1'
TWO = '2'
THREE = '3'
FOUR = '4'
FIVE = '5'
SIX = '6'
SEVEN = '7'
EIGHT = '8'
NINE = '9'
DRAW_TWO = 'draw'
REVERSE = 'reverse'
SKIP = 'skip'

VALUES = (ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, DRAW_TWO,
          REVERSE, SKIP)

# Special cards
CHOOSE = 'colorchooser'
DRAW_FOUR = 'draw_four'

SPECIALS = (CHOOSE, DRAW_FOUR)

STICKERS = {
    'b_0': 'BQADAQADLQEAAj4q6QABpUDVqBfXmCgC',
    'b_1': 'BQADAQADLwEAAj4q6QABHCpbYT4zdgsC',
    'b_2': 'BQADAQADMQEAAj4q6QABSPKXlMe1r-YC',
    'b_3': 'BQADAQADMwEAAj4q6QABZD8hbMmWokUC',
    'b_4': 'BQADAQADNQEAAj4q6QABFdqVPZ3Z5RgC',
    'b_5': 'BQADAQADNwEAAj4q6QABDC32UoSoXc8C',
    'b_6': 'BQADAQADOQEAAj4q6QABZiIePrDNZE4C',
    'b_7': 'BQADAQADOwEAAj4q6QABhFx3R6Deja0C',
    'b_8': 'BQADAQADPQEAAj4q6QABRR3lLkWw6pIC',
    'b_9': 'BQADAQADPwEAAj4q6QABjcnjfLVblmkC',
    'b_draw': 'BQADAQADQQEAAj4q6QABNHYNbzYZW68C',
    'b_skip': 'BQADAQADRQEAAj4q6QABAxLqDyVvm8AC',
    'b_reverse': 'BQADAQADQwEAAj4q6QABM4cEz6kMZnUC',
    'g_0': 'BQADAQADSwEAAj4q6QABNM17kTWMHm8C',
    'g_1': 'BQADAQADTQEAAj4q6QAB9OEXIHQSwekC',
    'g_2': 'BQADAQADTwEAAj4q6QABN1m0W38BvxIC',
    'g_3': 'BQADAQADUQEAAj4q6QABrn-S4CkoyzYC',
    'g_4': 'BQADAQADmgEAAj4q6QAByfSD9CebR6IC',
    'g_5': 'BQADAQADUwEAAj4q6QABp2t-0ISLVjQC',
    'g_6': 'BQADAQADVQEAAj4q6QABGIhSxfGkgqgC',
    'g_7': 'BQADAQADVwEAAj4q6QABAspuHEDEBpEC',
    'g_8': 'BQADAQADWQEAAj4q6QABNJEEbTzO9FgC',
    'g_9': 'BQADAQADWwEAAj4q6QABOAVXnBtA3_EC',
    'g_draw': 'BQADAQADXQEAAj4q6QABFvifXJm5MCsC',
    'g_skip': 'BQADAQADYQEAAj4q6QABBRIiR88Z4H0C',
    'g_reverse': 'BQADAQADXwEAAj4q6QAB97WGS17VbfMC',
    'r_0': 'BQADAQADZQEAAj4q6QABQhliM-_XxgYC',
    'r_1': 'BQADAQADZwEAAj4q6QAB_gRXNybGX2gC',
    'r_2': 'BQADAQADaQEAAj4q6QABBriT6hpnI-oC',
    'r_3': 'BQADAQADawEAAj4q6QABFTxp2zrnqLgC',
    'r_4': 'BQADAQADbgEAAj4q6QABeIFCqtl393gC',
    'r_5': 'BQADAQADcAEAAj4q6QABNxmXrv0nN-oC',
    'r_6': 'BQADAQADcgEAAj4q6QABXT3dHtMStAEC',
    'r_7': 'BQADAQADdAEAAj4q6QAB3MEAAeZUY2GgAg',
    'r_8': 'BQADAQADdgEAAj4q6QAB0YNVKBa2cokC',
    'r_9': 'BQADAQADeAEAAj4q6QABHSAcQZeN6t4C',
    'r_draw': 'BQADAQADegEAAj4q6QABJhKBhiiTZFAC',
    'r_skip': 'BQADAQADfgEAAj4q6QABRJ1C8H3305wC',
    'r_reverse': 'BQADAQADfAEAAj4q6QACJR8b31hU2AI',
    'y_0': 'BQADAQADgAEAAj4q6QABvvSFDSGrn50C',
    'y_1': 'BQADAQADggEAAj4q6QABQCkZz7fnDOYC',
    'y_2': 'BQADAQADhAEAAj4q6QABw7_kWmXjEPQC',
    'y_3': 'BQADAQADhgEAAj4q6QABE3l00hFD2AIC',
    'y_4': 'BQADAQADiAEAAj4q6QABtJ_TW0cjU-8C',
    'y_5': 'BQADAQADigEAAj4q6QABp57eeeuw24kC',
    'y_6': 'BQADAQADjAEAAj4q6QABMdwKMHcFLK8C',
    'y_7': 'BQADAQADjgEAAj4q6QAB07QEi-Ic6D4C',
    'y_8': 'BQADAQADkAEAAj4q6QABkKbOapGWBw8C',
    'y_9': 'BQADAQADkgEAAj4q6QABulpxLPlEXJYC',
    'y_draw': 'BQADAQADlAEAAj4q6QABuQ5_f0Xh-YYC',
    'y_skip': 'BQADAQADmAEAAj4q6QABbJUclt5ytyEC',
    'y_reverse': 'BQADAQADlgEAAj4q6QABtbL0U2X1sK0C',
    'draw_four': 'BQADAQADSQEAAj4q6QAB4TMkTHt5lQEC',
    'colorchooser': 'BQADAQADRwEAAj4q6QABpAK25wNGjsIC',
    'option_draw': 'BQADAQADCgIAAj4q6QABiQaKgZR8tmsC',
    'option_pass': 'BQADAQADEAIAAj4q6QABI1-uJHk89vAC',
    'option_bluff': 'BQADAQADCAIAAj4q6QABSaTiGgxxIpgC',
    'option_info': 'BQADAQADDgIAAj4q6QABPCXOnpmWeKsC'
}

STICKERS_GREY = {
    'b_0': 'BQADAQADnAEAAj4q6QAByYCtgbrNMa8C',
    'b_1': 'BQADAQADngEAAj4q6QABkfPiIRrHh8UC',
    'b_2': 'BQADAQADoAEAAj4q6QABHci5rhnzcH0C',
    'b_3': 'BQADAQADogEAAj4q6QAB45RNjLGe5gsC',
    'b_4': 'BQADAQADpAEAAj4q6QAB6sswXV_X8EYC',
    'b_5': 'BQADAQADpgEAAj4q6QABpeAcGkmgifoC',
    'b_6': 'BQADAQADqAEAAj4q6QABxUj1UdwRBOYC',
    'b_7': 'BQADAQADqgEAAj4q6QABUqXNCOScj80C',
    'b_8': 'BQADAQADrAEAAj4q6QAByNwuN7Ep-D4C',
    'b_9': 'BQADAQADrgEAAj4q6QAB2qWJz8sNkp8C',
    'b_draw': 'BQADAQADsAEAAj4q6QABmN4K7CsR-UoC',
    'b_skip': 'BQADAQADtAEAAj4q6QABJFKbIxaKF4oC',
    'b_reverse': 'BQADAQADsgEAAj4q6QABCfz8sWF-WjAC',
    'g_0': 'BQADAQADugEAAj4q6QABhrHgp2qRoZsC',
    'g_1': 'BQADAQADvAEAAj4q6QABj9kps0CgaUgC',
    'g_2': 'BQADAQADvgEAAj4q6QABgDFfdqcq5X4C',
    'g_3': 'BQADAQADwAEAAj4q6QABGBpH4rp-l1EC',
    'g_4': 'BQADAQADwgEAAj4q6QABoLWWWEBjvh8C',
    'g_5': 'BQADAQADxAEAAj4q6QABOyDeS1_wLwIC',
    'g_6': 'BQADAQADxgEAAj4q6QAB96IjTnkj3BEC',
    'g_7': 'BQADAQADyAEAAj4q6QABkZnPQPowL8YC',
    'g_8': 'BQADAQADygEAAj4q6QABald8BX6SRxsC',
    'g_9': 'BQADAQADzAEAAj4q6QABtoMIjJmFqGIC',
    'g_draw': 'BQADAQADzgEAAj4q6QAB1xJsyCjiJm8C',
    'g_skip': 'BQADAQAD0gEAAj4q6QABoZt1xRj9QaMC',
    'g_reverse': 'BQADAQAD0AEAAj4q6QABz0CqhZvhVcYC',
    'r_0': 'BQADAQAD1AEAAj4q6QABsEm_32dfn6MC',
    'r_1': 'BQADAQAD1gEAAj4q6QABwMVv8-_QaFQC',
    'r_2': 'BQADAQAD2AEAAj4q6QABmky5HxtMt_gC',
    'r_3': 'BQADAQAD2gEAAj4q6QABd7MQKRDrOhYC',
    'r_4': 'BQADAQAD3AEAAj4q6QAB4nXnkxzq8-sC',
    'r_5': 'BQADAQAD3gEAAj4q6QABqw0SKUjr0hgC',
    'r_6': 'BQADAQAD4AEAAj4q6QABO_lW0ULETb8C',
    'r_7': 'BQADAQAD4gEAAj4q6QABEtbBCPJK1pQC',
    'r_8': 'BQADAQAD5AEAAj4q6QABuwmYVIflE7IC',
    'r_9': 'BQADAQAD5gEAAj4q6QABLM29e5GSruUC',
    'r_draw': 'BQADAQAD6AEAAj4q6QAB18-DUkJdoMkC',
    'r_skip': 'BQADAQAD7AEAAj4q6QABqFZXBpbxprQC',
    'r_reverse': 'BQADAQAD6gEAAj4q6QABvCGWkQ8U1TsC',
    'y_0': 'BQADAQAD7gEAAj4q6QABYCgcllwRZS4C',
    'y_1': 'BQADAQAD8AEAAj4q6QAB5qgBiD9zeokC',
    'y_2': 'BQADAQAD8gEAAj4q6QAB6xdh8qHT7-wC',
    'y_3': 'BQADAQAD9AEAAj4q6QABDcg0uQ6G-OAC',
    'y_4': 'BQADAQAD9gEAAj4q6QABkFmb6RYFOR0C',
    'y_5': 'BQADAQAD-AEAAj4q6QAB_pldsK0bfA0C',
    'y_6': 'BQADAQAD-gEAAj4q6QAB1akqGmCG2QIC',
    'y_7': 'BQADAQAD_AEAAj4q6QABkIE5gnMeX_gC',
    'y_8': 'BQADAQAD_gEAAj4q6QABvsRXuDu_nF0C',
    'y_9': 'BQADAQAEAgACPirpAAE24GZw4xhr7AI',
    'y_draw': 'BQADAQADAgIAAj4q6QABU-49KEbCGpQC',
    'y_skip': 'BQADAQADBgIAAj4q6QABUSLVjTlTo2kC',
    'y_reverse': 'BQADAQADBAIAAj4q6QAB0MP1a7QzAb0C',
    'draw_four': 'BQADAQADuAEAAj4q6QABb-d7RlSPslEC',
    'colorchooser': 'BQADAQADtgEAAj4q6QABumVyzfivOBIC'
}


class Card(object):
    """
    This class represents a card.
    """

    def __init__(self, color, value, special=None):
        self.color = color
        self.value = value
        self.special = special

    def __str__(self):
        if self.special:
            return self.special
        else:
            return '%s_%s' % (self.color, self.value)

    def __repr__(self):
        if self.special:
            return '%s%s%s' % (COLOR_ICONS.get(self.color, ''),
                               COLOR_ICONS[BLACK],
                               ' '.join([s.capitalize()
                                         for s in self.special.split('_')]))
        else:
            return '%s%s' % (COLOR_ICONS[self.color], self.value.capitalize())

    def __eq__(self, other):
        """ Needed for sorting the cards """
        return str(self) == str(other)

    def __lt__(self, other):
        """ Needed for sorting the cards """
        return str(self) < str(other)


def from_str(string):
    """ Decode a Card object from a string """
    if string not in SPECIALS:
        color, value = string.split('_')
        return Card(color, value)
    else:
        return Card(None, None, string)