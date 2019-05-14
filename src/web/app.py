# -*- encoding: utf-8 -*-
#
# flask app

from flask import Flask, render_template, jsonify, request
from utils.database_utils import get_tweet_rate, get_aurin_data
from utils.geo_utils import get_state_list
import json
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

app = Flask(__name__, instance_relative_config=True)

# load json file to get options data
with open(os.path.join(APP_STATIC, 'home_page_options.json')) as file:
    options_json = json.load(file)
    option_list = options_json["option_list"]


@app.route('/')
def home():
    """
    home page
    :return: html template
    """
    return render_template("home.html", option_list=option_list, state_list=get_state_list())


@app.route('/search', methods=['POST'])
def search():
    result = {
        "Wrath": {},
        "Lust": {},
        "Sloth": {},
        "Greed": {},
    }

    try:
        keyword_list = request.json["keywords"]
        sin = request.json["sin"]
        state = request.json["state"]
        database = request.json["database"]
        print(database)
        if state == 'All':
            for state in get_state_list():
                tweet_rate, aurin_data = search_database(keyword_list, state, database)
                result[sin][state] = {
                    "tweet_rate": tweet_rate,
                    "aurin_data": aurin_data,
                }
        else:
            tweet_rate, aurin_data = search_database(keyword_list, state, database)
            result[sin][state] = {
                "tweet_rate": tweet_rate,
                "aurin_data": aurin_data,
            }
    except Exception as e:
        print(e)
    print(result)
    return jsonify(result)


def search_database(keyword_list, state, database):
    """
    call database utils to do the searching by specifying the factor
    :param keyword_list: list of words
    :param state: state name
    :param database: database name
    :return: (tweet rate, aurin data rate)
    """

    # if keyword is not provided, use the default word list
    if len(keyword_list) > 0:
        tweet_rate = get_tweet_rate(keyword_list, state)
    else:
        tweet_rate = 0.2

    aurin_data = get_aurin_data(database, state)

    return tweet_rate, aurin_data


if __name__ == '__main__':
    app.run()
