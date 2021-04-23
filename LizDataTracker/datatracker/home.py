from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
import json, requests
from types import SimpleNamespace
import urllib.request
from flask_table import Table, Col, ButtonCol

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
    platform_names = []

    for g in lst2013:
        h = g['platform']
        i = str(h)
        platform_names.append(i)

    u_plt = []

    for n in platform_names:
        if n not in u_plt:
            u_plt.append(n)

    ct_gms_by_plt = []
    for p in u_plt:
        ndict = {
            'count': 0,
            'platform': p
        }
        ct_gms_by_plt.append(ndict)

    for p in ct_gms_by_plt:
        for g in lst2013:
            if g['platform'] == p['platform']:
                p['count'] += 1

    s_ct_gms_by_plt = sorted(ct_gms_by_plt, key=lambda a: a['count'])

    # create array for charting
    values = []
    labels = []
    for c in s_ct_gms_by_plt:
        number_of_games = c['count']
        values.append(number_of_games)
    for d in s_ct_gms_by_plt:
        label = d['platform']
        labels.append(label)

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
    elif request.form['search'] == 'see all':
        return redirect(url_for('home.index'))
    else:
        return render_template('home/gamedetails.html')
    # else:
    # return 'hi'
    # render_template('sample/postform.html', page_title="PostForm from Module Function")


@bp.route('/equestion')
def equestion():
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
    platform_names = []

    for g in lst2013:
        h = g['platform']
        i = str(h)
        platform_names.append(i)

    u_plt = []

    for n in platform_names:
        if n not in u_plt:
            u_plt.append(n)

    ct_gms_by_plt = []
    for p in u_plt:
        ndict = {
            'count': 0,
            'platform': p
        }
        ct_gms_by_plt.append(ndict)

    for p in ct_gms_by_plt: # ct_gms_by_plt is a list of dictionaries
        for g in lst2013:
            if g['platform'] == p['platform']:
                p['count'] += 1 # p is the dictionary.

    s_ct_gms_by_plt = sorted(ct_gms_by_plt, key=lambda a: a['count'])

    # create array for charting
    values = []
    labels = []
    for c in s_ct_gms_by_plt:
        number_of_games = c['count']
        values.append(number_of_games)
    for d in s_ct_gms_by_plt:
        label = d['platform']
        st_label = str(label)
        labels.append(st_label)

    return render_template("home/equestion.html", labels=labels, values=values)


@bp.route('/play')
def play():
    a = 'hello'
    b = 'world'
    d = 'play'
    c = []
    c.append(a)
    c.append(b)
    c.append(d)
    values = []
    v = 2
    values.append(v)
    v = 4
    values.append(v)
    v = 6
    values.append(v)
    v = 9
    values.append(v)

    return render_template('home/play.html', labels=c, values=values)


@bp.route('/search')
def presearch():
    error = "Search for a game by title"
    return render_template('home/search.html', error=error)


@bp.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        game = request.form['search']
        if game is not None:
            url = 'https://api.dccresource.com/api/games'
            data = urllib.request.urlopen(url).read().decode()
            obj = json.loads(data)

            found_items = []
            for s in obj:
                if s['name'] == game:
                    found_items.append(s)

            if len(found_items) == 0:
                error = "No games matched your search. Please try again."
                flash(error)
                return render_template('home/search.html', error=error)
            if len(found_items) == 1:
                for item in found_items:
                    # game_id = item['_id']
                    # game_id_st = str(game_id)
                    # url = ('https://api.dccresource.com/api/games' + game_id_st)
                    # data = urllib.request.urlopen(url).read().decode()
                    game_for_details = item
                    id_of_game = "Game Id:" + game_for_details['_id']
                    game_rank = "Rank:" + str(game_for_details['rank'])
                    page_title_game_name = "Game name: " + game_for_details['name']
                    game_platform = "Platform: " + game_for_details['platform']
                    year_game = "Year: " + str(game_for_details['year'])
                    genre_game = "Genre: " + game_for_details['genre']
                    game_publisher = "Publisher: " + game_for_details['publisher']
                    na_sales_game = "North America Sales in millions: " + str(game_for_details['naSales'])
                    game_eu_sales = "European Sales in millions: " + str(game_for_details['euSales'])
                    game_japan_sales = "Japan Sales in Millions: " + str(game_for_details['jpSales'])
                    other_game_sales = "Other Sales: " + str(game_for_details['otherSales'])
                    global_game_sales = "Global Sales: " + str(game_for_details['globalSales'])
                    game_version = "Version: " + str(game_for_details['__v'])
                    game_details_list = [id_of_game, game_rank, game_platform, year_game, genre_game, game_publisher,
                                         na_sales_game, game_eu_sales, game_japan_sales, other_game_sales,
                                         global_game_sales, game_version]
                    return render_template('home/search.html', data=game_details_list, title=page_title_game_name)
            else:
                item = found_items[0]
                game_id = item['_id']
                url = 'https://api.dccresource.com/api/games' + game_id
                data = urllib.request.urlopen(url).read().decode()
                game_for_details = json.loads(data)
                id_of_game = "Game Id:" + game_for_details['_id']
                game_rank = "Rank:" + str(game_for_details['rank'])
                page_title_game_name = "Game name: " + game_for_details['name']
                game_platform = "Platform: " + game_for_details['platform']
                year_game = "Year: " + str(game_for_details['year'])
                genre_game = "Genre: " + game_for_details['genre']
                game_publisher = "Publisher: " + game_for_details['publisher']
                na_sales_game = "North America Sales in millions: " + str(game_for_details['naSales'])
                game_eu_sales = "European Sales in millions: " + str(game_for_details['euSales'])
                game_japan_sales = "Japan Sales in Millions: " + str(game_for_details['jpSales'])
                other_game_sales = "Other Sales: " + str(game_for_details['otherSales'])
                global_game_sales = "Global Sales: " + str(game_for_details['globalSales'])
                game_version = "Version: " + str(game_for_details['__v'])
                game_details_list = [id_of_game, game_rank, game_platform, year_game, genre_game, game_publisher,
                                     na_sales_game, game_eu_sales, game_japan_sales, other_game_sales,
                                     global_game_sales, game_version]
                return render_template('home/search.html', data=game_details_list, title=page_title_game_name)

    else:
        error = "GoDebug"
        return render_template('home/search.html', error=error)


@bp.route('/globalsalesbyconsole')
def globalsalesbyconsole():
    url = 'https://api.dccresource.com/api/games'
    data = urllib.request.urlopen(url).read().decode()
    game_objects = json.loads(data)
    games_after2013_year = []

    # scrub data without year info
    for game in game_objects:
        if game['year'] is not None:
            if game['year'] >= 2013:
                games_after2013_year.append(game)

    # get platform names
    platform_names = []

    for g in games_after2013_year:
        h = g['platform']
        i = str(h)
        platform_names.append(i)

    # get unique platform names
    unique_platform_names = []
    for p in platform_names:
        if p not in unique_platform_names:
            unique_platform_names.append(p)

    # create dictionary for each unique console name
    platform_dictionary_list = []
    # for each platform name, sort games into list
    # for each list, iterate through list and edit global sales on platform dictionary in platform_dictionary_li
    game_list = []

    for name in unique_platform_names:
        game_list.clear()
        for game in games_after2013_year:
            if name == game['platform']:
                game_list.append(game)
        global_sales_count = 0
        game_list_count = len(game_list)
        for game in game_list:
            global_sales_count += game['globalSales']
            game_list_count -= 1
            int_glob = int(global_sales_count)
            if game_list_count == 0:
                platform_dictionary = dict(platform=name, globalSales=int_glob)
                platform_dictionary_list.append(platform_dictionary)

    # sort dictionaries by sales numbers for pretty graphs :).
    platform_dictionary_li_s = sorted(platform_dictionary_list, key=lambda f: f['globalSales'])

    # assign keys to a list
    # assign data count to list
    labels = []
    data = []
    for platform in platform_dictionary_li_s:
        labels.append(platform['platform'])
        data.append(platform['globalSales'])

    # return labels and data to html for chart making

    return render_template('home/globalsalesbyconsole.html', labels=labels, values=data)


@bp.route('/search', methods=('GET', 'POST'))
def searchgame():
    if request.method == 'POST':
        page_title = request.form['title']
        error = None

        if not page_title:
            error = 'You must enter a title'

        if error is not None:
            flash(error)
        elif request.form['title'] == "go home":
            return redirect(url_for('sample.index'))
        else:
            return render_template('sample/postform.html', page_title=page_title)

    else:
        return render_template('sample/postform.html', page_title="PostForm from Module Function")


@bp.route('/searchchart')
def presearchchart():
    return render_template('home/searchchart.html')


@bp.route('/searchchart', methods=('GET', 'POST'))
def searchchart():
    if request.method == 'POST':
        game = request.form['searchchart']
        if game is None:
            render_template('home/searchchart.html')
        if game is not None:
            url = 'https://api.dccresource.com/api/games'
            data = urllib.request.urlopen(url).read().decode()
            obj = json.loads(data)
            found_items = []
            for s in obj:
                if s['name'] == game:
                    found_items.append(s)

            if len(found_items) == 0:
                return render_template('home/search.html')
            if len(found_items) == 1:
                for item in found_items:
                    game_for_details = item
                first_console = game_for_details['platform']
                second_console = "na"
                sales = game_for_details['globalSales']
                global_sales = int(sales)
                global_sales2 = 0
                consoles = []
                sales = []
                consoles.append(second_console)
                consoles.append(first_console)
                sales.append(global_sales2)
                sales.append(global_sales)

                return render_template("home/globalsalesbyconsole.html", labels=consoles, values=sales)
