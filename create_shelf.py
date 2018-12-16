import shelve
import pandas as pd
import make_seat_dict

file = 'emp_list.csv'
df = pd.read_csv(file)
emp_dict = make_seat_dict.make_dict()

with shelve.open('Employees') as emps:
    for row in [x[1] for x in df.iterrows()]:
        try:
            name = ' '.join(row['Name'].split(', ')[::-1])
            emps[name] = {'seat': emp_dict[name], 'team': make_seat_dict.get_team(row)}
        except KeyError as k:
            continue
    for emp in list(emps.keys()):
        print(emps[emp])

