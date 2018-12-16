from requests_html import HTMLSession
from bs4 import BeautifulSoup as BS
import shelve
import pandas as pd
import pprint

session = HTMLSession()
url = 'http://corganinet.com/_applications/locator_v1/view_officemap_01.cfm'

def make_dict():
    emp_dict = dict()
    floors = dict([('First Floor', 10025),('Second Floor', 10026),('Third Floor',10027), ('Corgan East', 10019)])
    for v in floors.values():
        params = {'MAPID': v, 'EMID': '00015'}
        r = session.get(url, params=params)
        soup = BS(r.text, 'lxml')
        for emp in soup.find_all(attrs={'class': 'color_48'}):
            name, seat = emp['title'].split(' | ')[::-1]
            name = ' '.join(name.split(', ')[::-1])
            emp_dict[name] = seat
    return emp_dict

def get_team(row):
    if row['Sector'] == 'Critical Facilities':
        if row['Subsector'] == 'Red Studio':
            return 'CF Red'
        return 'CF Blue'
    if row['Sector'] == 'Shared Services':
        return row['Subsector']
    return row['Sector']

if __name__ == '__main__':
    #file = 'emp_list.csv'
    #df = pd.read_csv(file)
    emp_dict = make_dict()
    pprint.pprint(emp_dict)
"""
    with shelve.open(EnterName) as emps:
        for row in [x[1] for x in df.iterrows()]:
            try:
                name = ' '.join(row['Name'].split(', ')[::-1])
                emps[name] = {'seat': emp_dict[name], 'team': get_team(row)}
            except KeyError as k:
                continue
"""