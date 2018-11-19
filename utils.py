import requests
import json


ERROR_MESSAGE = '네트워크 접속에 문제가 발생했습니다. 다시 시도해주세요.'

def get_menu(answer):
    menu = []
    index = answer.find(' 1. ')

    if index < 0:
        return answer, menu

    menu_string = answer[index + 1:]
    answer = answer[:index]

    number = 1

    while 1:
        number += 1
        search_string = ' %d. ' % number
        index = menu_string.find(search_string)

        if index < 0:
            menu.append(menu_string[3:].strip())
            break;

        menu.append(menu_string[3:index].strip())
        menu_string = menu_string[index + 1:]

    return answer, menu

def get_menu_button(menu):
    if len(menu) == 0:
        return None

    menu_button = {
        'type': 'buttons',
        'buttons': menu
    }

    return menu_button


def get_answer(text, user_key):
    data_send = {
        'lang': 'ko',
        'query': text,
        'sessionId': user_key,
        'timezone': 'Asia/Seoul'
    }

    data_header = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer TOKEN' #개인의 Client Access token 입력 
    }

    dialogflow_url = 'https://api.dialogflow.com/v1/query?v=20150910'

    res = requests.post(dialogflow_url,
                        data=json.dumps(data_send),
                        headers=data_header)

    if res.status_code != requests.codes.ok:
        return ERROR_MESSAGE

    data_receive = res.json()
    answer = data_receive['result']['fulfillment']['speech']

    return answer