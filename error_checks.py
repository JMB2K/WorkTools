import time
import logging
from appJar import gui
from bs4 import BeautifulSoup as BS
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

logging.basicConfig(level=logging.DEBUG)
logging.disable(logging.CRITICAL)

class Printer():

    def __init__(self, url, name, params={'password':'00015', 'uri':'/rps/'}):
        self.params = params
        self.url = url
        self.name = name

    def check_errors(self):
        """ This remotes into the webUI of the copiers and pulls the data from the ongoing errors """
        global browser
        browser.get(self.url)
        result = f'{self.name}\n'
        wait = WebDriverWait(browser, 10)

        if self.params != None:
            try:
                browser.find_element_by_name('password').send_keys(self.params['password'])
                browser.find_element_by_xpath('//*[@id="main"]/form/p[2]/input[2]').click()
            except Exception:
                browser.find_element_by_name('pin').send_keys(self.params['password'])
                browser.find_element_by_xpath('//*[@id="main"]/form/p[2]/input[2]').click()
        try:
            wait.until(expected.presence_of_element_located((By.CLASS_NAME, 'ErrorInfoMessage')))
        except Exception as E:
            return None
        innerHTML=browser.execute_script('return document.body.innerHTML')
        soup=BS(innerHTML, 'lxml')
        errors = soup.find_all('span', attrs={'class':'ErrorInfoMessage'})
        if errors == []:
            return None
        for i in errors:
            result='{}\t{}\n'.format(result, i.text)
        result = result + '\n'
        return result


dal_a = Printer('http://10.21.20.104:8000', 'DAL-MFP-A ---> 55258')
dal_b = Printer('http://10.21.20.112:8000', 'DAL-MFP-B ---> 71156')
dal_c = Printer('http://10.21.20.108:8000', 'DAL-MFP-C ---> 55021')
dal_d = Printer('http://10.21.20.109:8000', 'DAL-MFP-D ---> 55259')
dal_f = Printer('http://10.21.20.105:8000', 'DAL-MFP-F ---> 55260')
dal_g = Printer('http://10.21.20.101:8000', 'DAL-MFP-G ---> 55215')
dal_h = Printer('http://10.21.20.106:8000', 'DAL-MFP-H ---> 55261', params={'password': '00015', 'originally-requested-url': '/rps/'})
dal_i = Printer('http://10.21.20.110:8000', 'DAL-MFP-I ---> 55262', params=None)
dal_j = Printer('http://10.21.20.102:8000', 'DAL-MFP-J ---> 39632')
dal_k = Printer('http://10.21.20.103:8000', 'DAL-MFP-K ---> 55253', params={'password': '00015', 'originally-requested-url': '/rps/'})
dal_m = Printer('http://10.21.20.107:8000', 'DAL-MFP-M ---> 39631')


copiers = [dal_a,
           dal_b,
           dal_c,
           #dal_d,
           dal_f,
           #dal_g,
           dal_h,
           #dal_i,
           dal_j,
           #dal_k,
           dal_m]

if __name__ == '__main__':

    logging.warning('Starting Program')
    start = time.time()
    app = gui('Errors')
    options = Options()
    options.headless = True
    logging.warning('About to start the browser...')
    browser = Firefox(options=options, executable_path="C:\\Program Files\\Mozilla Firefox\\geckodriver.exe")
    logging.warning('Browser started...')

    for_popup = ''
    for copier in copiers:
        logging.warning(f'Starting {copier}...')
        errs = copier.check_errors()
        if errs is not None:
            for_popup = for_popup+errs

    ending = time.time() - start
    for_popup = for_popup+'\n\n' + 'Finished in {:.2f} seconds'.format(ending)
    app.infoBox('Copier Errors', for_popup)
    browser.quit()
    app.stop()
