# -*- coding: utf-8 -*-

from kucrawl import *
from utils import *
from flask import Flask, request, jsonify


URL_OPEN_TIME_OUT = 10

app = Flask(__name__)

# Dialogflow fullfillment 처리
@app.route('/', methods=['POST'])
def webhook():

    req = request.get_json(force=True)
    action = req['result']['action']

    if action == 'event_search':
        year = req['result']['parameters']['year']
        hakgi = req['result']['parameters']['hakgi']
        month = req['result']['parameters']['month']
        date = req['result']['parameters']['date']
        answer = event_search(year, hakgi, month, date)
    elif action == 'date_search':
        year = req['result']['parameters']['year']
        hakgi = req['result']['parameters']['hakgi']
        search_event = req['result']['parameters']['search_event']
        answer = date_search(year, hakgi, search_event)
    else:
        answer = 'error'

    res = {'speech': answer}
        
    return jsonify(res)


@app.route("/keyboard")
def keyboard():

    res = {
        'type': 'buttons',
        'buttons': ['대화하기']
    }

    return jsonify(res)

@app.route('/message', methods=['POST'])
def message():

    req = request.get_json()
    user_key = req['user_key']
    content = req['content']
    
    if len(user_key) <= 0 or len(content) <= 0:
        answer = ERROR_MESSAGE


    if content == u'대화하기':
        answer = '안녕하세요! 고려대학교 학사일정봇입니다. \n 검색을 원하시는 시기를 골라주세요. 1. 2018학년도 1학기 2. 2018학년도 2학기 3. 2019학년도 1학기 4. 2019학년도 2학기'
    else:
        answer = get_answer(content, user_key)

    answer, menu = get_menu(answer)

    res = {
        'message': {
            'text': answer
        }                    
    }

    menu_button = get_menu_button(menu)
    
    if menu_button != None:
        res['keyboard'] = menu_button 

    return jsonify(res)


if __name__ == '__main__':

    app.run(host='0.0.0.0', threaded=True)    