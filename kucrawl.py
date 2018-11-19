from bs4 import BeautifulSoup
import requests


def find_table(year, hakgi):

    #학사일정 페이지 크롤링
    url = 'https://registrar.korea.ac.kr/registrar/college/schedule_new.do?cYear=' + year + '&hakGi='+ hakgi
    res = requests.get(url)
    tables = BeautifulSoup(res.text, 'html.parser').find("table")
    rows = tables.find_all('tr')

    return rows


def event_search(year, hakgi, search_month, search_date):

    rows = find_table(year, hakgi)
    calendar = []

    #월, 일, 이벤트 갖고오기
    for row in rows:
        monthrow = row.find_all('th')

        if len(monthrow) > 0:
            month = monthrow[0].get_text(strip=True)
            month = month.split("월")[0]

        date = row.find_all('td')[0].get_text(strip=True)
        event = row.find_all('td')[1].get_text(strip=True)

        if "~" in date:
            days = date.split("~")
            former = days[0].split("(")[0]
            latter = days[1].split("(")[0]

            calendar.append([month, former, latter, event])

        else:
            day = date.split("(")[0]
            calendar.append([month, day, day, event])

    #날짜 검색
    tmp = [calendar[i] for i in range(len(calendar)) if int(calendar[i][0]) == int(search_month)
           and int(calendar[i][1]) <= int(search_date) <= int(calendar[i][2])]

    if len(tmp) == 0:
        result = str(search_month) + '월 ' + str(search_date) + '일의 일정을 찾지 못했습니다.'
    else:
        result = str(search_month) + '월 ' + str(search_date) + "일의 날짜 검색 결과입니다. \n\n"
        for i in range(len(tmp)):
            if i == len(tmp) - 1:
                result += tmp[i][3] + '(' + tmp[i][0] + '/' + tmp[i][1] + " ~ " + tmp[i][0] + '/' + tmp[i][2] + ")"
            else:
                result += tmp[i][3] + '(' + tmp[i][0] + '/' + tmp[i][1] + " ~ " + tmp[i][0] + '/' + tmp[i][2] + ")" +'\n'

    return result


def date_search(year, hakgi, search_event):
    
    rows = find_table(year, hakgi)
    calendar = []

    #캘린더 그대로 갖고와서 일정 찾기
    for row in rows:
        monthrow = row.find_all('th')

        if len(monthrow) > 0:
            month = monthrow[0].get_text(strip=True)

        date = row.find_all('td')[0].get_text(strip=True)
        event = row.find_all('td')[1].get_text(strip=True)

        calendar.append([month, date, event])

    dates = [calendar[i][:3] for i in range(len(calendar)) if all(letter in calendar[i][2] for letter in search_event)]
    if len(dates) == 0:
        result = '\'' + search_event + '\'' + ' 의 날짜를 찾지 못했습니다.'
    else:
        tmp = [dates[i][2] + ": " + dates[i][0] + ' ' + dates[i][1] for i in range(len(dates))]
        result = '\'' + search_event + '\'' + "의 날짜 검색 결과입니다. \n\n"
        for i in range(len(tmp)):

            if i == len(tmp) - 1:
                result += tmp[i]
            else:
                result += tmp[i] + '\n'

    return result