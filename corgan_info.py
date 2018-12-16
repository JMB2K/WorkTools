import requests, lxml, re, time
from bs4 import BeautifulSoup as BS
from collections import OrderedDict as OD


class Corgan():
    floors = OD([('First Floor', [10000, 10025, 10029]),('Second Floor', [10026]),('Third Floor',[10002, 10027, 10031]), ('Fourth Floor', [10028]), ('Corgan East', [10019, 10032])])

    def __init__(self, to_file=True, names_only=False):
        self.to_file = to_file
        self.names_only = names_only

    def seating_chart(self):

        url = 'http://corganinet.com/_applications/locator_v1/view_officemap_01.cfm'
        for k, v in self.floors.items():
            file = f'C:\\Users\\00015\\Desktop\\{k}_SeatingChart.txt'
            emps = []
            for map_id in v:
                params = {'MAPID':map_id, 'EMID':'00015'}
                r = requests.get(url, params=params)
                soup = BS(r.content, 'lxml')
                [emps.append(x['title'].split(' | ')[::-1]) for x in soup.find_all(attrs={'class': 'color_48'})]

            if not self.names_only:
                for emp in emps:
                    name = emp[0].split()[-1] + ', ' + emp[0].split()[0]
                    emp[0] = name
                    #print(emp[0])

            self.floors[k] = [x[0] for x in emps]

            if self.to_file:
                with open(file, 'w') as f:
                    f.write(f'----->{k}<-----\n')
                    flag, side, space = 0, 'L', 0
                    for p in sorted(emps):
                        if flag == 2:
                            f.write('\n')
                            flag = 0
                        p = f'{p[0]} - ({p[1]})'
                        if side == 'L':
                            space = 40-len(p)
                            side = 'R'
                        elif side == 'R':
                            f.write(' '*space)
                            side = 'L'
                        f.write(f'\t{p}')
                        flag += 1
                    f.close()
        return self.floors

start = time.time()
corgan = Corgan(to_file=True)
floor_list = corgan.seating_chart()
two = floor_list['Second Floor']
end = time.time() - start
print(f'Finished in {end} seconds')