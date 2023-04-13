import re
from operator import itemgetter
from collections import Counter
from django.db.models import Q
from django.shortcuts import get_object_or_404
from webapp.models import Country, Player, Tournament, Club, Game
from webapp.views.GoR_calculator import get_new_rank_from_rating


# Функция считает средний ранг игроков одного клуба. Возвращает список, в котором словарь с ключами club
# (содержит pk клуба) и average (посчитанное значение). На доработке
def average_go_level():
    # Здесь нужно будет привязать фильтр через страну клуба, чтобы выводил только по Кыргызстану
    clubs = Club.objects.all()
    club_list = []
    for club in clubs:
        new_dict = dict()
        total_rating = 0
        num_players = club.players.count()
        for player in club.players.all():
            total_rating += player.current_rating
        if num_players > 0:
            result = total_rating // num_players
            average_num = get_new_rank_from_rating(result)
            new_dict['club'] = club.pk
            new_dict['average'] = average_num
        else:
            new_dict['club'] = club.pk
            new_dict['average'] = 0
        club_list.append(new_dict)
    return club_list


def get_total_wins(data):
    new_list = []
    for club in data:
        new_dict = dict()
        total_wins = 0
        for player in club.players.all():
            player_wins = 0
            games = Game.objects.filter(Q(black=player) | Q(white=player))
            for game in games:
                if game.result is not None:
                    if game.result.startswith('1'):
                        if game.black == player:
                            player_wins += 1
                    elif game.result.startswith('0'):
                        if game.white == player:
                            player_wins += 1
            total_wins += player_wins
        new_dict['club'] = club.pk
        new_dict['total'] = total_wins
        new_list.append(new_dict)
    return new_list


def get_position_in_kgf():
    country = Country.objects.get(country_code='kg')
    players = Player.objects.filter(country=country)
    new_list = []
    for player in players:
        new_dict = dict()
        new_dict['player'] = player
        new_dict['rating'] = player.current_rating
        new_dict['rank'] = player.current_rank
        new_list.append(new_dict)
    new_list.sort(key=itemgetter('rating'))
    new_list.reverse()
    position = 1
    for element in new_list:
        element['position'] = position
        position += 1
    return new_list


# Функция принимает pk турнира и возвращает список из словарей с ключами - player, wins (победы в этом турнире), losses
# (поражения в рамках турнира)
def get_wins_losses(pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    players = tournament.player_set.all()
    games = Game.objects.filter(tournament=tournament)
    new_list = []
    for player in players:
        new_dict = dict()
        wins = 0
        losses = 0
        for game in games:
            if game.result:
                if game.black == player and game.black_score > 0:
                    wins += game.black_score
                elif game.white == player and game.white_score > 0:
                    wins += game.white_score
                elif game.black == player and game.white_score > 0:
                    losses += 1
                elif game.white == player and game.black_score > 0:
                    losses += 1
            new_dict['player'] = player.pk
            new_dict['wins'] = wins
            new_dict['losses'] = losses
        new_list.append(new_dict)
    return new_list


def get_rank_for_json(data):
    tournaments = Tournament.objects.order_by("-date")
    new_list = []
    for player in data:
        new_dict = dict()
        for tournament in tournaments:
            for el in tournament.playerintournament_set.all():
                if player.pk == el.player_id:
                    if player not in new_dict:
                        new_dict['last_name'] = player.last_name
                        new_dict['first_name'] = player.first_name
                        new_dict['patronymic'] = player.patronymic
                        new_dict['GoLevel'] = el.GoLevel
        new_list.append(new_dict)
    return new_list


def get_data_for_table_games(pk):
    player = Player.objects.get(pk=pk)
    tournaments = player.playerintournament_set.all()
    new_list = []
    for element in tournaments:
        tournament = Tournament.objects.get(pk=element.tournament_id)
        games = Game.objects.filter(tournament=tournament)
        for game in games:
            new_dict = dict()
            new_dict['tournament'] = tournament
            if game.black == player:
                new_dict['round'] = game.round_num
                opponent = game.white
                if opponent:
                    data = opponent.playerintournament_set.filter(tournament=tournament)
                    for el in data:
                        new_dict['rank'] = el.GoLevel
                        if el.club is not None:
                            new_dict['club'] = el.club.name
                new_dict['opponent'] = game.white
                if game.result is not None:
                    if game.black_score == 0:
                        new_dict['result'] = '-'
                    elif game.black_score == 1:
                        new_dict['result'] = '+'
                new_dict['color'] = 'b'
                new_list.append(new_dict)
            elif game.white == player:
                new_dict['round'] = game.round_num
                opponent = game.black
                if opponent:
                    data = opponent.playerintournament_set.filter(tournament=tournament)
                    for el in data:
                        new_dict['rank'] = el.GoLevel
                        if el.club is not None:
                            new_dict['club'] = el.club.name
                new_dict['opponent'] = game.black
                if game.result is not None:
                    if game.white_score == 0:
                        new_dict['result'] = '-'
                    elif game.white_score == 1:
                        new_dict['result'] = '+'
                new_dict['color'] = 'w'
                new_list.append(new_dict)
    for item in new_list:
        if item['opponent'] is None:
            new_list.remove(item)
    return new_list


def get_data_for_gor_evolution(pk):
    player = Player.objects.get(pk=pk)
    tournaments = player.playerintournament_set.all()
    new_list = []
    for element in tournaments:
        tournament = Tournament.objects.get(pk=element.tournament_id)
        games = Game.objects.filter(tournament=tournament)
        for game in games:
            new_dict = dict()
            if game.black == player and game.black_gor_change:
                new_dict['tournament'] = tournament
                new_dict['round'] = game.round_num
                new_dict['gor_change'] = game.black_gor_change
                opponent = game.white
                if opponent:
                    data = opponent.playerintournament_set.filter(tournament=tournament)
                    for el in data:
                        new_dict['opponent_rank'] = el.GoLevel
                        new_dict['opponent_rating'] = el.rating
                new_dict['opponent'] = game.white
                new_dict['opponent_gor_change'] = game.white_gor_change
                if game.result is not None:
                    if game.black_score == 0:
                        new_dict['result'] = 'Loss'
                    elif game.black_score == 1:
                        new_dict['result'] = 'Win'
                new_dict['color'] = 'b'
                new_list.append(new_dict)
            elif game.white == player and game.white_gor_change:
                new_dict['tournament'] = tournament
                new_dict['round'] = game.round_num
                new_dict['gor_change'] = game.white_gor_change
                opponent = game.black
                if opponent:
                    data = opponent.playerintournament_set.filter(tournament=tournament)
                    for el in data:
                        new_dict['opponent_rank'] = el.GoLevel
                        new_dict['opponent_rating'] = el.rating
                new_dict['opponent'] = game.black
                new_dict['opponent_gor_change'] = game.black_gor_change
                if game.result is not None:
                    if game.white_score == 0:
                        new_dict['result'] = 'Loss'
                    elif game.white_score == 1:
                        new_dict['result'] = 'Win'
                new_dict['color'] = 'w'
                new_list.append(new_dict)
            else:
                pass
    for item in new_list:
        if item['opponent'] is None:
            new_list.remove(item)
    print(new_list)
    return new_list


def get_tournaments_list_for_gor_evolution(pk):
    player = Player.objects.get(pk=pk)
    tournaments = player.playerintournament_set.all()
    new_list = []
    for element in tournaments:
        new_dict = dict()
        tournament = Tournament.objects.get(pk=element.tournament_id)
        new_dict['tournament'] = tournament
        new_dict['rating_before'] = element.rating
        new_dict['rating_after'] = element.rating_after
        new_dict['rank_after'] = element.GoLevel_after
        new_list.append(new_dict)
    return new_list


def player_wins_loses(pk):
    player = Player.objects.get(pk=pk)
    games = Game.objects.filter(Q(black=player) | Q(white=player))
    wl = []
    for game in games:
        new_dict = dict()
        wins = 0
        losses = 0
        if game.result:
            if game.black == player and game.black_score > 0:
                wins += game.black_score
            elif game.white == player and game.white_score > 0:
                wins += game.white_score
            elif game.black == player and game.white_score > 0:
                losses += 1
            elif game.white == player and game.black_score > 0:
                losses += 1
        new_dict['player'] = player.pk
        new_dict['wins'] = wins
        new_dict['losses'] = losses
        wl.append(new_dict)
    c = Counter()
    for d in wl:
        c.update(d)
    statistics = dict(c)
    return statistics
