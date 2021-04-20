from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
import json, requests
from types import SimpleNamespace

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    data = [
        (1, 1999),
        (2, 1998),
        (3, 1957)
    ]
    # labels on x axis of chart, values on y axis of chart

    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template(games.html, labels=labels, values=values)

    return '/'


@bp.route('/home')
def index():
    return "liz"


@bp.route('/games')
def games():
    response = requests.get('https://api.dccresource.com/api/games').text
    return response


@bp.route('/chart')
def chart():
    response = requests.get('https://api.dccresource.com/api/games').json()
    platforms = []
    for line in response:
        platform = (x['platform'] for x in response)
        platforms.append(platform)

    unique_platforms = []

    for x in platforms:
        if x not in unique_platforms:
            unique_platforms.append(x)

    quantities = []
    game_sys_lists = []

    for line in unique_platforms:
        if game_sys_lists.count() != 0:
            quantities.append(game_sys_lists)
        game_sys_lists.clear()
        for game in response:
            platform = (x['platform'] for x in response == line)
            game_sys_lists.append(platform)
