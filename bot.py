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

import ast
import os.path
import json
from collections import namedtuple
import logging
from datetime import datetime
from random import randint
from random import choice

from telegram import ParseMode, Message, Chat, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import Updater, InlineQueryHandler, \
    ChosenInlineResultHandler, CommandHandler, MessageHandler, Filters, \
    CallbackQueryHandler
from telegram.ext.dispatcher import run_async
from telegram.utils.botan import Botan

from game_manager import GameManager
from credentials import TOKEN, BOTAN_TOKEN,WAIT_TIME,PEDALA_TIME,ALLOWED,API_TIMEOUT,RANKING_FILE
from start_bot import start_bot
from results import *
from utils import *
import card as c

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.DEBUG)
logger = logging.getLogger(__name__)

gm = GameManager()
u = Updater(token=TOKEN, workers=32)
dp = u.dispatcher

from threading import Lock

mutex = Lock()
ranking = {}

botan = False
if BOTAN_TOKEN:
    botan = Botan(BOTAN_TOKEN)

def _lambda(d): return namedtuple('X', d.keys())(*d.values())

help_text = ("Follow these steps:\n\n"
             "1. Add this bot to a group\n"
             "2. In the group, start a new game with /new or join an already"
             " running game with /join\n"
             "3. After at least two players have joined, start the game with"
             " /start\n"
             "4. Type <code>@mau_mau_bot</code> into your chat box and hit "
             "<b>space</b>, or click the <code>via @mau_mau_bot</code> text "
             "next to messages. You will see your cards (some greyed out), "
             "any extra options like drawing, and a <b>?</b> to see the "
             "current game state. The <b>greyed out cards</b> are those you "
             "<b>can not play</b> at the moment. Tap an option to execute "
             "the selected action.\n"
             "Players can join the game at any time. To leave a game, "
             "use /leave. If a player takes more than 90 seconds to play, "
             "you can use /skip to skip that player.\n\n"
             "Other commands (only game creator):\n"
             "/close - Close lobby\n"
             "/open - Open lobby\n\n"
             "<b>Experimental:</b> Play in multiple groups at the same time. "
             "Press the <code>Current game: ...</code> button and select the "
             "group you want to play a card in.\n"
             "If you enjoy this bot, "
             "<a href=\"https://telegram.me/storebot?start=mau_mau_bot\">"
             "rate me</a>, join the "
             "<a href=\"https://telegram.me/unobotupdates\">update channel</a>"
             " and buy an UNO card game.\n")

source_text = ("This bot is Free Software and licensed under the AGPL. "
               "The code is available here: \n"
               "https://github.com/jh0ker/mau_mau_bot")


@run_async
def send_async(bot, *args, **kwargs):
    if 'timeout' not in kwargs:
        kwargs['timeout'] = API_TIMEOUT

    try:
        bot.sendMessage(*args, **kwargs)
    except Exception as e:
        error(None, None, e)


@run_async
def answer_async(bot, *args, **kwargs):
    if 'timeout' not in kwargs:
        kwargs['timeout'] = API_TIMEOUT

    try:
        bot.answerInlineQuery(*args, **kwargs)
    except Exception as e:
        error(None, None, e)


def error(bot, update, error):
    """ Simple error handler """
    logger.exception(error)


def new_game(bot, update):
    """ Handler for the /new command """
    global ranking
    global mutex
    mutex.acquire()
    try:
        chat_id = update.message.chat_id
        
        if(not int(chat_id) in ALLOWED):
            send_async(bot, chat_id,
                       text="Esse chat/grupo não está autorizado a utilizar este bot. Peça para que o chat %d seja liberado." % chat_id)
            return
        try:
            game = gm.chatid_games[chat_id][-1]
            send_async(bot, chat_id,
                       text="Ô IMBECIL! Já tem jogo acontecendo aqui.")
            return
        except (KeyError, IndexError):
            pass

        if update.message.chat.type == 'private':
            help(bot, update)
        else:
            game = gm.new_game(update.message.chat)
            game.owner = update.message.from_user
            game.ranking = init_ranking(chat_id)
            send_async(bot, chat_id,
                       text="Jogo criado! Entre no jogo usando /join "
                            "e inicie o jogo com /start")
            if botan:
                botan.track(update.message, 'New games')
    finally:
        mutex.release()

def save_ranking():
    global ranking
    with open(RANKING_FILE, 'w') as f:
        json.dump(ranking, f, ensure_ascii=False)

def load_ranking():
    global ranking
    try:    
        if os.path.isfile(RANKING_FILE):
            with open(RANKING_FILE) as json_data:
                ranking = json.load(json_data)
                json_data.close()
    except:
        logger.debug("Unable to load ranking file, returning empty")
        ranking = {}
    

load_ranking()

def sort_ranking(chat_id):
    pass




def init_ranking(chat_id):
    global ranking
    try:
        return ranking['chat_' + str(chat_id)]
    except (IndexError, KeyError):
        ranking['chat_' + str(chat_id)] = {}
        ranking['chat_' + str(chat_id)]['most'] = 0;
        ranking['chat_' + str(chat_id)]['players'] = {};
        save_ranking()
        return ranking['chat_' + str(chat_id)]
       



def allow_handler(bot, update):
    """ Handler for the /allow command """
    chat_id = update.message.chat_id
    message_text = update.message.text.split(' ', 1 )
    if(not int(chat_id) in ALLOWED):
        send_async(bot, chat_id,
                   text="Esse chat/grupo não está autorizado a utilizar este bot. Peça para que o chat %d seja liberado." % chat_id,reply_to_message_id=update.message.message_id)
        return
    try:
        ALLOWED.append(int(message_text[1]))
        send_async(bot, chat_id,
                   text="Chat %d adicionado com sucesso a lista de permitidos.",
                   reply_to_message_id=update.message.message_id)
    except (KeyError, IndexError):
            send_async(bot, chat_id,
                   text="Erro ao adicionar novo chat a lista.",reply_to_message_id=update.message.message_id)
    

def join_game(bot, update):
    """ Handler for the /join command """
    global ranking
    message_text = update.message.text.split(' ', 1 )
    user_obj = ''
#     if(len(message_text) > 1):
#         user_obj = _lambda(ast.literal_eval(message_text[1]))
#         logger.debug("forçando a entrar: %d" % user_obj.id)
#     else:
    user_obj = update.message.from_user
    chat_id = update.message.chat_id
    if update.message.chat.type == 'private':
        help(bot, update)
    else:
        try:
            game = gm.chatid_games[chat_id][-1]
            if not game.open:
                send_async(bot, chat_id, text="Tem um monte de gente online, mas ninguém mais pode entrar no jogo. Fique aí triste e rejeitado.",reply_to_message_id=update.message.message_id)
                return
            try:
                delta = (datetime.now() - game.anti_pedalada[user_obj.id]).seconds;
                if(delta < PEDALA_TIME):
                    send_async(bot, chat_id, text="Tentando pedalar é?\nVocê só pode voltar a jogar em %d segundo(s)" % (PEDALA_TIME - delta),reply_to_message_id=update.message.message_id)
                    return
            except (KeyError, IndexError):
                pass
        except (KeyError, IndexError):
            pass

        joined = gm.join_game(chat_id, user_obj)
        if joined:
            try:
                user_rank_data = ranking['chat_' + str(chat_id)]['players']["user_" + str(user_obj.id)]
            except (IndexError, KeyError):
                user_rank_data = {}
                user_rank_data['wins'] = 0
                ranking['chat_' + str(chat_id)]['players']["user_" + str(user_obj.id)] = user_rank_data
            user_rank_data['user'] = {  'first_name': user_obj.first_name,
                                        'username': user_obj.username,
                                        'id': user_obj.id}
            save_ranking()
            if (update.message.from_user.id == user_obj.id):
                send_async(bot, chat_id,
                            text="Entrou no jogo.",
                            reply_to_message_id=update.message.message_id)
            else:
                send_async(bot, chat_id,
                            text="Forçou @%s a entrar no jogo" % user_obj.username,
                            reply_to_message_id=update.message.message_id)
        elif joined is None:
            send_async(bot, chat_id,
                       text="Não dá para dar join se não tem jogo acontecendo, né querida? "
                            "Crie um novo com /new",
                       reply_to_message_id=update.message.message_id)
        else:
            send_async(bot, chat_id,
                       text="Não tem como sentar na pica branca e preta aqui, querida. "
                            "Você já está dentro desse jogo, comece ele com /start ou /"
                            "startfouyer",
                       reply_to_message_id=update.message.message_id)


def uno_handler(bot, update):
    """ Handler for the /uno command """
    try:
        chat_id = update.message.chat_id
        user = update.message.from_user
        games = gm.chatid_games[chat_id]
        players = gm.userid_players.get(user.id, list())
        jogando = False
        for player in players:
            for game in games:
                if player in game.players:
                    jogando = True
                    if player.uno:
                        player.uno = False
                        send_async(bot, chat_id, text="OLHA ELE!",
                        reply_to_message_id=update.message.message_id)
                        break
                    else:
                        if(player.unoDrawn):
                            send_async(bot, chat_id, text="Burra! Nem tá com uma carta e tá gritando UNO...",
                                        reply_to_message_id=update.message.message_id)
                        else:
                            player.unoDrawn = True
                            player.cards.append(player.game.deck.draw())
                            send_async(bot, chat_id, text="Burra! Nem tá com uma carta e tá gritando UNO... Toma uma carta e vê se aprende!",
                                        reply_to_message_id=update.message.message_id)
                        break
        if not jogando:
            send_async(bot, chat_id, text="Você nem está jogando.",
            reply_to_message_id=update.message.message_id)
    except KeyError:
        send_async(bot, chat_id, text="Não tem jogo acontecendo neste chat.",
            reply_to_message_id=update.message.message_id)


def leave_game(bot, update):
    """ Handler for the /leave command """
    chat_id = update.message.chat_id
    user = update.message.from_user
    players = gm.userid_players.get(user.id, list())
    for player in players:
        if player.game.chat.id == chat_id:
            game = player.game
            break
    else:
        send_async(bot, chat_id, text="Para de tentar sair de jogo que você não tá jogando.",
                   reply_to_message_id=update.message.message_id)
        return

    user = update.message.from_user

    if game.started and len(game.players) < 3:
        player = gm.get_player_by_id(user, chat_id)
        w_user = player.prev.user
        wins = ranking['chat_' + str(chat_id)]['players']["user_" + str(w_user.id)]['wins'] + 1
        ranking['chat_' + str(chat_id)]['players']["user_" + str(w_user.id)]['wins'] = wins
        save_ranking()
        order_chat_rank(chat_id)
        gm.end_game(chat_id, user)
        send_async(bot, chat_id, text="Fim de jogo!\n%s ganhou por ser o último a sobrar. Deu sorte.\nTotal de vitórias: %d" % (display_name(w_user),wins))
    else:
        player = gm.get_player_by_id(user, chat_id);
        if game.playerWhichIsBluffing is player:
            game.playerWhichIsBluffing = None
        if(game.choosing_color):
            game.choosing_color = False
            result_id = choice(c.COLORS)
            game.choose_color(result_id)
            send_async(bot, chat_id, text="Nova cor: %s" % display_color(result_id))
        if not player is None:
            if(len(player.cards) < 15 and game.started):
                game.anti_pedalada[user.id] = datetime.now()
            gm.leave_game(user, chat_id)
            if(game.started):
                send_async(bot, chat_id,
                           text="Tchau, querida!\nPróximo jogador: " +
                                display_name(game.current_player.user,game),
                           reply_to_message_id=update.message.message_id)
            else:
                send_async(bot, chat_id,
                           text="Tchau, querida!",
                           reply_to_message_id=update.message.message_id)
        else:
            send_async(bot, chat_id, text="Para de tentar sair de jogo que você não tá jogando.",
                       reply_to_message_id=update.message.message_id)


def select_game(bot, update):

    chat_id = int(update.callback_query.data)
    user_id = update.callback_query.from_user.id
    players = gm.userid_players[user_id]
    for player in players:
        if player.game.chat.id == chat_id:
            gm.userid_current[user_id] = player
            break
    else:
        send_async(bot, update.callback_query.message.chat_id,
                   text="Jogo não encontrado :(")
        return

    back = [[InlineKeyboardButton(text='Volte ao último grupo',
                                  switch_inline_query='')]]

    bot.answerCallbackQuery(update.callback_query.id,
                            text="Vai jogar no grupo que você escolheu.",
                            show_alert=False,
                            timeout=API_TIMEOUT)
    bot.editMessageText(chat_id=update.callback_query.message.chat_id,
                        message_id=update.callback_query.message.message_id,
                        text="Grupo escolhido: %s\n"
                             "<b>Tenha certeza que foi para o grupo certo"
                             "</b>"
                             % gm.userid_current[user_id].game.chat.title,
                        reply_markup=InlineKeyboardMarkup(back),
                        parse_mode=ParseMode.HTML,
                        timeout=API_TIMEOUT)


def status_update(bot, update):
    """ Remove player from game if user leaves the group """
   
    
    if update.message.left_chat_member:
        try:
            chat_id = update.message.chat_id
            user = update.message.left_chat_member
            players = gm.userid_players.get(user.id, list())
            for player in players:
                if player.game.chat.id == chat_id:
                    game = player.game
                    break
        except (IndexError, KeyError):
            return

        if gm.leave_game(user, chat_id):
            send_async(bot, chat_id, text="Removendo %s do jogo." 
                                          % display_name(user,game))

def start_game_fouyer(bot, update, args):
    game = start_game(bot, update, args)
    game.fouyer = True


def start_game(bot, update, args):
    """ Handler for the /start command """

    if update.message.chat.type != 'private':
        # Show the first card
        chat_id = update.message.chat_id
        try:
            game = gm.chatid_games[chat_id][-1]
        except (KeyError, IndexError):
            send_async(bot, chat_id, text="Não tem jogo rodando neste chat.\n"
                                          "Crie um novo com /new")
            return

        if game.current_player is None or \
                game.current_player is game.current_player.next:
            send_async(bot, chat_id, text="Pelo menos dois jogadores precisam dar /join "
                                          "para começar o jogo")
        elif game.started:
            send_async(bot, chat_id, text="Lerda você, hein?\nJá tem um jogo rodando neste chat.")
        else:
            game.play_card(game.last_card)
            game.started = True
            bot.sendSticker(chat_id,
                            sticker=c.STICKERS[str(game.last_card)],
                            timeout=API_TIMEOUT)
            send_async(bot, chat_id, 
                       text="%s começa jogando.\n"
                            "Use /close para impedir que mais pessoas entrem no jogo."
                            % display_name(game.current_player.user,game))
            return game
    elif len(args) and args[0] == 'select':
        players = gm.userid_players[update.message.from_user.id]

        groups = list()
        for player in players:
            groups.append([InlineKeyboardButton(text=player.game.chat.title,
                                                callback_data=
                                                str(player.game.chat.id))])
        send_async(bot, update.message.chat_id,
                   text='Selecione o grupo que você quer jogar:',
                   reply_markup=InlineKeyboardMarkup(groups))
    else:
        help(bot, update)


def close_game(bot, update):
    """ Handler for the /close command """
    chat_id = update.message.chat_id
    user = update.message.from_user
    games = gm.chatid_games.get(chat_id)

    if not games:
        send_async(bot, chat_id, text="Não tem jogo rodando, não insista.")
        return

    game = games[-1]

    if game.owner.id == user.id:
        game.open = False
        send_async(bot, chat_id, text="Ninguém mais pode entrar no jogo.")
        return
    else:
        send_async(bot, chat_id,
                   text="Só o todo poderoso %s pode fazer isto. Foi ele quem criou o jogo."
                        % display_name(game.owner,game),
                   reply_to_message_id=update.message.message_id)
        return


def open_game(bot, update):
    """ Handler for the /open command """
    chat_id = update.message.chat_id
    user = update.message.from_user
    games = gm.chatid_games.get(chat_id)

    if not games:
        send_async(bot, chat_id, text="Vai abrir o que? Só se for seu cu, não tem jogo rodando.")
        return

    game = games[-1]

    if game.owner.id == user.id:
        game.open = True
        send_async(bot, chat_id, text="\o/ Tá aberto o jogo."
                                      "Novos jogadores podem usar o /join.")
        return
    else:
        send_async(bot, chat_id,
                   text="Só o todo poderoso %s pode fazer isto. Foi ele quem criou o jogo."
                        % display_name(game.owner,game),
                   reply_to_message_id=update.message.message_id)
        return


def skip_player(bot, update):
    """ Handler for the /skip command """
    chat_id = update.message.chat_id
    user = update.message.from_user
    games = gm.chatid_games.get(chat_id)
    players = gm.userid_players.get(user.id)

    if not games:
        send_async(bot, chat_id, text="Não tem jogo rodando, não insista.")
        return

    if not players:
        send_async(bot, chat_id, text="Deixa quem tá jogando palpitar, tá bom, querida?")
        return

    for game in games:
        for player in players:
            if player in game.players:
                started = game.current_player.turn_started
                now = datetime.now()
                delta = (now - started).seconds

                if delta < game.current_player.waiting_time:
                    send_async(bot, chat_id,
                               text="Ainda não, querida, só daqui %s segundos."
                                    % (game.current_player.waiting_time -
                                       delta),
                               reply_to_message_id=
                               update.message.message_id)
                    return

                elif game.current_player.waiting_time > 0:
                    game.current_player.anti_cheat += 1
                    game.current_player.waiting_time -= 30
                    if(game.choosing_color):
                        game.choosing_color = False
                        result_id = choice(c.COLORS)
                        game.choose_color(result_id)
                        send_async(bot, chat_id, text="Nova cor: %s" % display_color(result_id))
                    else:
                        game.current_player.cards.append(game.deck.draw())
                    send_async(bot, chat_id,
                               text="Na próxima vez, a espera será "
                                    "de %d seconds.\n"
                                    "Próximo jogador: %s"
                                    % (game.current_player.waiting_time,
                                       display_name(
                                           game.current_player.next.user,game)))
                    game.turn()
                    return

                elif len(game.players) > 2:
                    send_async(bot, chat_id,
                               text="%s ficou sem sinal, bateria ou morreu."
                                    "Ele foi removido do jogo.\n"
                                    "Próximo: %s"
                                    % (display_name(game.current_player.user),
                                       display_name(
                                           game.current_player.next.user,game)))

                    gm.leave_game(game.current_player.user, chat_id)
                    return
                else:
                    send_async(bot, chat_id,
                               text="%s ficou sem sinal, bateria ou morreu."
                                    "Ele foi removido do jogo e por isso o jogo acabou :(\n"
                                    % display_name(game.current_player.user,game))

                    gm.end_game(chat_id, game.current_player.user)
                    return


def help(bot, update):
    """ Handler for the /help command """
    send_async(bot, update.message.chat_id, text=help_text, 
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)


def source(bot, update):
    """ Handler for the /help command """
    send_async(bot, update.message.chat_id, text=source_text,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)

def order_chat_rank(chat_id):
    global ranking
    global mutex
    mutex.acquire()
    try:
        load_ranking()
        chat_rank = ranking['chat_' + str(chat_id)]['players']
        sorted_list = sorted(chat_rank, key=lambda x: chat_rank[x]['wins'], reverse=True)
        try:
            ranking['chat_' + str(chat_id)]['most'] = chat_rank[sorted_list[0]]['wins']
        except (KeyError,IndexError):
            ranking['chat_' + str(chat_id)]['most'] = 0
        save_ranking()
        return sorted_list
    finally:
        mutex.release()

def ranking_handler(bot,update):
    global ranking
    chat_id = update.message.chat_id
    
    try:
        chat_rank = ranking['chat_' + str(chat_id)]['players']
    except (KeyError,IndexError):
        init_ranking(chat_id)
        chat_rank = ranking['chat_' + str(chat_id)]['players']
    
    rank = ''

    sorted_list = order_chat_rank(chat_id)
    for p in sorted_list:
        user = chat_rank[p]
        rank += ("%s - %d vitória(s)\n" % (display_name_with_rank(user['user'],ranking['chat_' + str(chat_id)]),int(user['wins'])))
    send_async(bot, chat_id, text="Ranking:\n" + 
                rank,
                reply_to_message_id=update.message.message_id)


def stats(bot,update):
    chat_id = update.message.chat_id
    user = update.message.from_user
    games = gm.chatid_games.get(chat_id)
    if not games or len(games) < 1:
        send_async(bot, chat_id, text="Stats de que jogo? Não tem nada rodando aqui não.",
                    reply_to_message_id=update.message.message_id)
        return
    for game in games:
        if game.started:
            players = player_list(game)
            send_async(bot, chat_id, text="Jogando agora: " + 
                    display_name(game.current_player.user,game) +
                    "\n" +
                    "Última carta: " + repr(game.last_card) + "\n" +
                    "Jogadores: " + " -> ".join(players),
                    reply_to_message_id=update.message.message_id)
        else:
            send_async(bot, chat_id, text="Calma lá, o jogo ainda não começou.\nTente novamente mais tarde.",
                    reply_to_message_id=update.message.message_id)


def news(bot, update):
    """ Handler for the /news command """
    send_async(bot, update.message.chat_id, 
               text="All news here: https://telegram.me/unobotupdates",
               disable_web_page_preview=True)


def reply_to_query(bot, update):
    """ Builds the result list for inline queries and answers to the client """
    results = list()
    playable = list()
    switch = None

    try:
        user_id = update.inline_query.from_user.id
        players = gm.userid_players[user_id]
        player = gm.userid_current[user_id]
        game = player.game
    except KeyError:
        add_no_game(results)
    else:
        if not game.started:
            add_not_started(results)
        elif user_id == game.current_player.user.id:
            if game.choosing_color:
                add_choose_color(results)
            else:
                if not player.drew:
                    add_draw(player, results)

                else:
                    add_pass(results)

                if (game.last_card.special == c.DRAW_FOUR and game.draw_counter and not game.playerWhichIsBluffing is None) or (game.last_card.value == c.DRAW_TWO and game.draw_counter and not game.playerWhichIsBluffing is None) and not game.playerWhichIsBluffing is player:
                    add_call_bluff(results)

                playable = player.playable_cards()
                added_ids = list()

                for card in sorted(player.cards):
                    add_play_card(game, card, results,
                                  can_play=(card in playable and
                                            str(card) not in added_ids))
                    added_ids.append(str(card))

        if False or game.choosing_color:
            add_other_cards(playable, player, results, game)
        elif user_id != game.current_player.user.id or not game.started:
            for card in sorted(player.cards):
                add_play_card(game, card, results, can_play=False)
        else:
            add_gameinfo(game, results)

        for result in results:
            result.id += ':%d' % player.anti_cheat

        if players and game and len(players) > 1:
            switch = 'Current game: %s' % game.chat.title

    answer_async(bot, update.inline_query.id, results, cache_time=0,
                 switch_pm_text=switch, switch_pm_parameter='select')


def process_result(bot, update):
    """ Check the players actions and act accordingly """
    try:
        user = update.chosen_inline_result.from_user
        player = gm.userid_current[user.id]
        game = player.game
        result_id = update.chosen_inline_result.result_id
        chat_id = game.chat.id
    except KeyError:
        return

    logger.debug("Selected result: " + result_id)

    result_id, anti_cheat = result_id.split(':')
    last_anti_cheat = player.anti_cheat
    player.anti_cheat += 1

    if result_id in ('hand', 'gameinfo', 'nogame'):
        return
    elif len(result_id) == 36:  # UUID result
        return
    elif int(anti_cheat) != last_anti_cheat:
        send_async(bot, chat_id, 
                   text="Cheat attempt by %s" % display_name(player.user,player.game))
        return
    elif result_id == 'call_bluff':
        reset_waiting_time(bot, chat_id, player)
        check_uno(bot, chat_id, player.prev)
        do_call_bluff(bot, chat_id, game, player)
    elif result_id == 'draw':
        reset_waiting_time(bot, chat_id, player)
        check_uno(bot, chat_id, player.prev)
        do_draw(game, player)
    elif result_id == 'pass':
        game.turn()
    elif result_id in c.COLORS:
        game.choose_color(result_id)
    else:
        reset_waiting_time(bot, chat_id, player)
        check_uno(bot, chat_id, player.prev)
        do_play_card(bot, chat_id, game, player, result_id, user)

    if game in gm.chatid_games.get(chat_id, list()):
        send_async(bot, chat_id, text="Próximo: " +
                                      display_name(game.current_player.user,game))


def reset_waiting_time(bot, chat_id, player):
    if player.waiting_time < WAIT_TIME:
        player.waiting_time = WAIT_TIME
        send_async(bot, chat_id, text="Tempo de espera para %s voltou a ser de "
                                      "%d segundos." % (display_name(player.user,player.game),WAIT_TIME))

def check_uno(bot, chat_id, player):
    if player.uno:
        player.uno = False
        player.cards.append(player.game.deck.draw())
        send_async(bot, chat_id, text="%s se fudeu, esqueceu do /uno. Comeu uma carta pra ver se aprende." % display_name(player.user,player.game))


def do_play_card(bot, chat_id, game, player, result_id, user):
    global ranking
    game.ranking = init_ranking(chat_id)
    card = c.from_str(result_id)
    game.play_card(card)
    player.cards.remove(card)
    if len(player.cards) == 1:
        player.uno = True
        player.unoDrawn = False
        #send_async(bot, chat_id, text="UNO!")
    elif len(player.cards) == 0:
        if(game.playerWhichIsBluffing != None and game.playerWhichIsBluffing.user.id is player.user.id):
            game.playerWhichIsBluffing = None
        wins = ranking['chat_' + str(chat_id)]['players']["user_" + str(user.id)]['wins'] + 1
        ranking['chat_' + str(chat_id)]['players']["user_" + str(user.id)]['wins'] = wins
        save_ranking()
        order_chat_rank(chat_id)
        send_async(bot, chat_id, text="%s ganhou, esse prodígio!\nTotal de vitórias: %d" % (display_name(user,game),wins))
        if(game.choosing_color):
            game.choosing_color = False
            result_id = choice(c.COLORS)
            game.choose_color(result_id)
            send_async(bot, chat_id, text="Nova cor: %s" % display_color(result_id))
        if len(game.players) < 3:
            send_async(bot, chat_id, text="Fim de jogo!")
            gm.end_game(chat_id, user)
        else:
            gm.leave_game(user, chat_id)
            
    if game.choosing_color:
        send_async(bot, chat_id, text="Escolha uma cor!")
    if botan:
        botan.track(Message(randint(1, 1000000000), user, datetime.now(),
                            Chat(chat_id, 'group')),
                    'Cartas jogadas')

def do_draw(game, player):
    draw_counter_before = game.draw_counter
    for n in range(game.draw_counter or 1):
        player.cards.append(game.deck.draw())
    game.playerWhichIsBluffing = None
    game.draw_counter = 0
    player.drew = True
    if (game.last_card.value == c.DRAW_TWO or
        game.last_card.special == c.DRAW_FOUR) and \
            draw_counter_before > 0:
        game.turn()


def do_call_bluff(bot, chat_id, game, player):
    bluffer = game.playerWhichIsBluffing
    check_uno(bot, chat_id, player.prev)
    if game.playerIsBluffing:
        send_async(bot, chat_id, text="PEGO NO BLEFE! Dando %d cartas de brinde para o %s."
                                      % (game.draw_counter, display_name(bluffer.user,game)))
        for i in range(game.draw_counter):
            bluffer.cards.append(game.deck.draw())
    else:
        send_async(bot, chat_id, text="%s não blefou! %s se fudeu, ganhou %d cartas de brinde."
                                        % (display_name(bluffer.user,game),
                                        display_name(player.user,game),
                                         game.draw_counter + 2))
        for i in range(game.draw_counter + 2):
            player.cards.append(game.deck.draw())
    game.playerWhichIsBluffing = None
    game.draw_counter = 0
    game.turn()


# Add all handlers to the dispatcher and run the bot
dp.addHandler(InlineQueryHandler(reply_to_query))
dp.addHandler(ChosenInlineResultHandler(process_result))
dp.addHandler(CallbackQueryHandler(select_game))
dp.addHandler(CommandHandler('start', start_game, pass_args=True))
dp.addHandler(CommandHandler('startfouyer', start_game_fouyer, pass_args=True))
dp.addHandler(CommandHandler('new', new_game))
dp.addHandler(CommandHandler('join', join_game))
dp.addHandler(CommandHandler('leave', leave_game))
dp.addHandler(CommandHandler('open', open_game))
dp.addHandler(CommandHandler('close', close_game))
dp.addHandler(CommandHandler('skip', skip_player))
dp.addHandler(CommandHandler('help', help))
dp.addHandler(CommandHandler('source', source))
dp.addHandler(CommandHandler('news', news))
dp.addHandler(CommandHandler('uno', uno_handler))
dp.addHandler(CommandHandler('allow', allow_handler))
dp.addHandler(CommandHandler('stats', stats))
#dp.addHandler(CommandHandler('pedala', pedala))
dp.addHandler(CommandHandler('ranking', ranking_handler))
dp.addHandler(MessageHandler([Filters.status_update], status_update))
dp.addErrorHandler(error)

start_bot(u)
u.idle()
