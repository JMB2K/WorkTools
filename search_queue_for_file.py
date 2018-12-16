import os

location = '\\\\dal-01-data02\\REPRO\\PLP-Polling\\Client'

while True:
    directory = os.walk(location)
    search_term = input('Enter "q" to quit, or enter search term: ')
    if search_term.lower() == 'q':
        break
    for p, d, f in directory:
        if p.endswith('PREPROC'):
            continue
        for file in f:
            if search_term.lower() in file.lower():
                print(p)
                continue

