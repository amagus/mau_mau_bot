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


from telegram import Emoji


def list_subtract(list1, list2):
    """ Helper function to subtract two lists and return the sorted result """
    list1 = list1.copy()

    for x in list2:
        list1.remove(x)

    return list(sorted(list1))

def display_name(user,game):
    if game:
        return display_name_with_rank(user,game.ranking)
    else:
        return display_name_with_rank(user)


def display_name_with_rank(user,rank):
    """ Get the current players name including their username, if possible """
    user_name = ''
    if rank:
        most_wins = 0
        try:
            most_wins = int(rank['most'])
        except (IndexError, KeyError):
            most_wins = 0
            
        user_wins = 0
        try:
            user_wins = int(rank['players']["user_" + str(user['id'])]['wins'])
        except (IndexError, KeyError):
            user_wins = 0
        
        if user_wins >= most_wins:
            user_name += Emoji.TROPHY
    
    user_name += user['first_name']
    if user['username']:
        user_name += ' (@' + user['username'] + ')'
    return user_name


def display_color(color):
    """ Convert a color code to actual color name """
    if color == "r":
        return Emoji.HEAVY_BLACK_HEART + " Vermelho"
    if color == "b":
        return Emoji.BLUE_HEART + " Azul"
    if color == "g":
        return Emoji.GREEN_HEART + " Verde"
    if color == "y":
        return Emoji.YELLOW_HEART + " Amarelo"
