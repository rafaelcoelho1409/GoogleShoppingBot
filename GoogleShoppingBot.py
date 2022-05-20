from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os, pandas as pd, datetime

#This bot was build to collect prices and products from Brazil, so some column names are maintained in Portuguese.

class GSBot:
    def __init__(self, headless = True):
        self.headless = headless
        self.options = Options()
        self.service = Service(ChromeDriverManager().install())
        self.dataframe = pd.DataFrame()

    def _options(self):
        self.current_path = os.getcwd()
        os.system('cd "{}"'.format(self.current_path))
        print('\n\n\n\n\n')
        print('Type below the product you want to search:')
        self.search_words = input()
        print('Type the number of pages you want to collect data from:')
        self.num_pages = int(input())

    def _get_url(self):
        if self.headless:
            self.options.add_argument('--headless')
            self.options.add_argument('--window-size=1920x1080')
        self.driver = webdriver.Chrome(options = self.options, service = self.service)
        self.driver.get('https://shopping.google.com')
        self.driver.maximize_window()

    def _search(self):
        try:
            self.search_box = self.driver.find_element(By.XPATH, '//input[@name = "q"]')
            self.search_box.send_keys(self.search_words)
            self.search_box.send_keys(Keys.ENTER)
        except:
            pass
    
    def _create_filename(self):
        self.now = '{}-'.format(self.search_words).replace(' ', '_') + str(datetime.datetime.now()) + '.csv'

    def _scraping_top_and_bottom(self):
        try:
            sleep(1)
            self.products = self.driver.find_elements(By.XPATH, '//div[starts-with(@class, "sh-np__product-title")]')
            self.prices = self.driver.find_elements(By.XPATH, '//span[@class = "T14wmb"]')
            self.sellers = self.driver.find_elements(By.XPATH, '//div[@class = "sh-np__seller-container"]')
            self.links = self.driver.find_elements(By.XPATH, '//a[@class = "shntl sh-np__click-target"]')
            self.df1 = pd.DataFrame() #dataframe with items prices on superior and inferior scroll bars on the page
            self.df1['Nome do produto'] = [self.products[i].text for i in range(len(self.products))]
            self.df1['Preço (R$)'] = [self.prices[i].text for i in range(len(self.prices))]
            self.df1[self.df1['Preço (R$)'] == 'Recondicionado por'] = '-'
            try:
                self.df1['Preço (R$)'] = self.df1['Preço (R$)'].str.split('R', expand = True)[1].apply(lambda x: x.replace('$', ''))
            except:
                pass
            self.df1['Seller'] = [self.sellers[i].text for i in range(len(self.sellers))]
            self.df1['Link'] = [self.links[i].get_attribute('href') for i in range(len(self.links))]
            self.df1 = self.df1[self.df1['Preço (R$)'] != '-']
        except:
            pass

    def _scraping_body(self):
        try:
            sleep(1)
            self.products2 = self.driver.find_elements(By.XPATH, '//h4[@class = "Xjkr3b"]')
            self.prices2 = self.driver.find_elements(By.XPATH, '//span[@class = "a8Pemb OFFNJ"]')
            self.sellers2 = self.driver.find_elements(By.XPATH, '//div[@class = "aULzUe IuHnof"]')
            self.links2 = self.driver.find_elements(By.XPATH, '//a[@class = "shntl"]')
            self.links2 = self.links2[::2]
        except:
            pass

    def _scraping_body_2(self):
        try:
            sleep(1)
            self.products3 = self.driver.find_elements(By.XPATH, '//h3[@class = "OzIAJc"]')
            self.prices3 = self.driver.find_elements(By.XPATH, '//span[@class = "a8Pemb OFFNJ"]')
            self.sellers3 = self.driver.find_elements(By.XPATH, '//div[@class = "b07ME mqQL1e"]')
            self.links3 = self.driver.find_elements(By.XPATH, '//a[@class = "LBbJwb shntl"]')
        except:
            pass

    def _to_dataframe(self):
        try:
            self.df2 = pd.DataFrame() #dataframe with items prices on page body
            self.df2['Nome do produto'] = [self.products2[i].text for i in range(len(self.products2))]
            self.df2['Preço (R$)'] = [self.prices2[i].text for i in range(len(self.prices2))]
            self.df2['Preço (R$)'] = self.df2['Preço (R$)'].apply(lambda x: x.replace('R$', ''))
            self.df2['Seller'] = [self.sellers2[i].text for i in range(len(self.sellers2))]
            self.df2['Link'] = [self.links2[i].get_attribute('href') for i in range(len(self.links2))]
        except:
            self.df2 = pd.DataFrame()
            pass

    def _to_dataframe_2(self):
        try:
            self.df3 = pd.DataFrame() #dataframe with items prices on page body
            self.df3['Nome do produto'] = [self.products3[i].text for i in range(len(self.products3))]
            self.df3['Preço (R$)'] = [self.prices3[i].text for i in range(len(self.prices3))]
            self.df3['Preço (R$)'] = self.df3['Preço (R$)'].apply(lambda x: x.replace('R$', ''))
            self.df3['Seller'] = [self.sellers3[i].text for i in range(len(self.sellers3))]
            self.df3['Link'] = [self.links3[i].get_attribute('href') for i in range(len(self.links3))]
        except:
            self.df3 = pd.DataFrame()
            pass

    def _next_page(self):
        ActionChains(self.driver).send_keys(Keys.END).perform()
        sleep(1)
        self.next_page = self.driver.find_element(By.XPATH, '//span[@class = "SJajHc NVbCr"]')
        self.next_page.click()

    def _concat_df(self):
        self.df_aux = pd.concat([self.df1, self.df2, self.df3])
        self.dataframe = pd.concat([self.dataframe, self.df_aux])

    def _save_to_csv(self):
        self.dataframe = self.dataframe[~self.dataframe.duplicated()]
        self.dataframe.to_csv(self.now, index = False)
    
    def _print(self):
        print(self.dataframe)
        print('Name of the file created: {}'.format(self.now))

    def _quit(self):
        self.driver.quit()

    def main(self):
        self._options()
        self._get_url()
        self._search()
        self._create_filename()
        i = 0
        while i < self.num_pages:
            print('Collecting data from page {}'.format(i + 1))
            self._scraping_top_and_bottom()
            self._scraping_body()
            self._to_dataframe()
            self._scraping_body_2()
            self._to_dataframe_2()
            self._concat_df()
            try:
                self._next_page()
            except:
                print('Data collected.')
                break
            i += 1
        print('Data collected.')
        self._save_to_csv()
        self._print()
        self._quit()

bot = GSBot()
bot.main()
