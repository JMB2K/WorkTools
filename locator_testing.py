from requests_html import HTMLSession
from bs4 import BeautifulSoup as BS
import pprint
import re



floors = {1 : '10025',
          2 : '10026',
          3 : '10027',
          'E': '10019'}

def get_seats(floor):
    temp = dict()
    session = HTMLSession()
    url = f'http://www.corganinet.com/_applications/locator_v1/view_officemap_01.cfm?MAPID={floors[floor]}'
    params = {'EMID': '00015'}
    data = session.get(url, params=params)
    soup = BS(data.text, 'lxml')
    for name in soup.find_all('div', attrs={'class': 'color_48'}):
        emp_name = name['title'].split(' | ')[1]
        temp[emp_name] = {'seat': name['title'].split(' | ')[0], 'emp_id': get_emid(emp_name), 'team': get_team(get_emid(emp_name))} 
    return temp

def get_emid(name):
    url = 'http://www.corganinet.com/_applications/whois_V1/view_list_01.cfm'
    params = {'MySearch_01': name}
    session = HTMLSession()
    data = session.post(url, data=params)
    try:
        emid = re.findall('EMID]([0-9]+)', data.text)[0]
    except Exception as E:
        emid = None
    return emid

def get_team(emid):
    url = 'http://www.corganinet.com/_applications/whois_V1/view_main_01.cfm'
    params = {'EMID': emid}
    session = HTMLSession()
    data = session.get(url, params=params)
    try:
        get_line = data.html.find('div', containing=' | Dallas Main')
        print(data.text)
        team_line = get_line[0].text
    except Exception as E:
        print(E)
        return None
    if team_line[1] == 'Critical Facilities':
        if team_line[2] == 'Red Studio':
            return 'CF Red'
        return 'CF Blue'
    elif team_line[1] == 'Shared Services':
        return team_line[2]
    return team_line[1]

for floor in floors:
    floors[floor] = get_seats(floor)

#pprint.pprint(floors)

for k in floors.keys():
    for name in sorted(floors[k]):
        print(name, floors[k][name])


    



