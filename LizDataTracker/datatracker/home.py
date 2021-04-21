from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
import json, requests
from types import SimpleNamespace
import urllib.request

bp = Blueprint('home', __name__)


@bp.route('/home')
def index():
    return "liz"


@bp.route('/chart')
def chart():
    url = 'https://api.dccresource.com/api/games'
    data = urllib.request.urlopen(url).read().decode()
    obj = json.loads(data)
    # get only games released 2013 or later
    lst2013 = []
    list_unknown_year = []
    for ob in obj:
        if ob['year'] is None:
            list_unknown_year.append(ob)
        elif ob['year'] >= 2013:
            lst2013.append(ob)
    # find unique platforms
    unique_platforms = []
    first_console = lst2013[0]
    first_console1 = first_console['platform']
    first_console_str = str(first_console1)
    my_platform_dictionary = {
        'platform': first_console_str,
        'games': 1
    }
    unique_platforms.append(my_platform_dictionary)
    for game in lst2013:
        platform = game['platform']
        for gme in unique_platforms:
            if gme['platform'] == platform:
                f = 1
            elif gme['platform'] != platform:
                f = 0
            if f == 0:
                 pltform_string = str(platform)
                 my_platform_dictionary = {
                     'platform': pltform_string,
                     'games': 0
                 }
                 unique_platforms.append(my_platform_dictionary)
    # get count of games for each platform fro post 2013 list
    games_per_platform = []
    for pl in unique_platforms:
        x = pl['platform']
        for g in lst2013:
            if g['platform'] == x:
                pl['games'] += 1

    # create array for charting
    chart_array_game_count = []
    label = []
    for d in unique_platforms:
        val = d['platform']
        label.append(val)
        number_of_games = d['games']
        chart_array_game_count.append(number_of_games)

    labels = label
    values = chart_array_game_count

    return render_template("home/chart.html", labels=labels, values=values)


@bp.route('/games')
def games():
    url = 'https://api.dccresource.com/api/games'
    # response = requests.get('https://api.dccresource.com/api/games').json(
    resp = requests.get(url)
    game_list = json.loads(resp.content, object_hook=lambda d: SimpleNamespace(**d))
    game_titles = []
    for gamess in game_list:
        game_titles.append(gamess.name)
    game_names = []
    for t in game_titles:
        u = t.__str__()
        game_names.append(u)
    game_count = 0
    for t in game_titles:
        game_count += 1
    gsc = str(game_count)
    # game count is 16598
    game_consoles = []
    unique_game_consoles = []
    for game in game_list:
        game_consoles.append(game.platform)
    for cons in game_consoles:
        if cons not in unique_game_consoles:
            unique_game_consoles.append(cons)
    game_consoles_count = len(unique_game_consoles)
    u_g_c_str = str(game_consoles_count)
    # 31 unique game consoles
    game_and_console_data = []
    for platform in unique_game_consoles:
        pltform_string = str(platform)
        my_dictionary = {
            'games': 0,
            'platform': pltform_string
        }
        game_and_console_data.append(my_dictionary)
    # my_len = len(game_and_console_data)
    # my_len_st = str(my_len)
    # return my_len_st
    # result = 31

    # data_one = game_and_console_data[2]
    # data_one['games'] = 10
    # data_one_string = str(data_one['games'])
    # return data_one_string
    # returns 10

    for console_dict in game_and_console_data:
        for game in game_list:
            game_release = int(game.year)
            if game_release >= 2013:
                if console_dict['platform'] == game.platform:
                    console_dict['games'] += 1

    data_two = game_and_console_data[25]
    data_two_ct = data_two['games']
    str_data_two = str(data_two_ct)
    return str_data_two


@bp.route('/yearsort')
def yearsort():
    url = 'https://api.dccresource.com/api/games'
    data = urllib.request.urlopen(url).read().decode()
    obj = json.loads(data)
    obj_zero = obj[0]
    yr_fame = obj_zero['year']
    yr_fame_str = str(yr_fame)
    return yr_fame_str

@bp.route('/gamedetails')
def gamedetails():
    if request.method == 'POST':
        search = request.form['search']
        error = None

    if not search:
        error = 'You must enter a game title'
    if error is not None:
        flash(error)
    elif request.form['search'] == 'see all' :
        return  redirect(url_for('home.index'))
    else:
        return render_template('home/gamedetails.html')
    # else:
    # return 'hi'
            # render_template('sample/postform.html', page_title="PostForm from Module Function")

