import pandas as pd
import re, requests, time

""" This reads through a csv of users from Argos and checks to see who needs to be moved to 'Unlicensed' group """

start = time.time()

def check_status(name):
    """ Checking names against the Corgan Locator to check if they are still employed here """
    url='http://corganinet.com/_applications/whois_V1/view_list_01.cfm'
    payload={'MySearch_01': name} # Searching employee name
    r=requests.post(url, data=payload)
    try:
        re.findall('EMID=([0-9]+)', r.text)[0]
        return True # Still employed if we get a result
    except IndexError:
        return False # No info raises an IndexError, no longer employed

file='C:\\Users\\00015\\Desktop\\argos_user.csv'
df = pd.read_csv(file)

emp_list = set()
for x in df.iterrows():
    if type(x[1]['FirstName']) != float and type(x[1]['LastName']) != float: # Weed out the random auto-created accounts
        n, p, g = x[1]['FirstName']+' '+x[1]['LastName'], x[1]['UserName'], x[1]['GroupName']
        if g != 'Unlicensed' and not check_status(n): # Don't want users who are already unlicensed
            emp_list.add((p, n))


flag=0
with open('C:\\Users\\00015\\Desktop\\removal_list_test.txt', 'w') as f:
    for person in sorted(emp_list):
        if flag == 2:
            f.write('\n')
            print('')
            flag=0
        f.write(str(person).ljust(37))
        print(str(person).ljust(37), end='')
        flag+=1

end = time.time() - start

print(f'Finished in {int(end//60)} minutes and {round(end%60)} seconds')

