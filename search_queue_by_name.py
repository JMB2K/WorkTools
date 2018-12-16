import os

location = 'E:\\Job Queue'
finish = None

while finish != 'q':
    search_name = input('Name to search for: ').upper()
    directory = os.walk(location)
    for fpath, fdir, files in directory:
        for file in files:
            if file.endswith('.inf'):
                with open(os.path.join(fpath, file), 'r') as f:
                    r=f.read()
                    f.close()
                if search_name in r.upper():
                    print(fpath)
    finish = input('Press "q" and enter to quit, just press enter to search again: ')
