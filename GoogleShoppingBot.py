import os, sys
if sys.platform in ['linux', 'linux2']:
    os.system('pip3 install selenium webdriver-manager pandas datetime > /dev/null') #Linux
elif sys.platform in ['win32', 'cygwin', 'msys']:
    os.system('pip3 install selenium webdriver-manager pandas datetime > NUL') #Windows
else:
    raise('Sistema operacional não encontrado.')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pandas as pd, datetime

class GSBot:
    """
    Argumentos:
    headless (True/False): executar ou não em modo 'headless' (navegador sem cabeçalho, oculto)
    os (Linux/Windows): sistema operacional

    Funções:
    _options: solicita que você escolha um nome para sua planilha de dados, o que você irá pesquisar no Google Shopping, e quantas páginas de pesquisa você deseja para coletar dados
    _get_url: acessa o site do Google Shopping. Se headless = True, o bot funcionará em modo oculto. Para visualizar o bot funcionando no navegador, troque para headless = False.
    _search: executa a pesquisa dentro do Google Shopping
    _create_folder: cria uma pasta para armazenar o arquivo final em excel dentro
    _leave_folder: sai da pasta onde é armazenado o arquivo csv com os dados
    _scraping_top_and_bottom: coleta os dados dos produtos nas barras de rolagem horizontal no topo e no final da página
    _scraping_body_*: coleta os dados dos produtos que estão no corpo da página
    _to_dataframe_*: importa os dados para dentro de dataframes
    _next_page: passa para a próxima pagina da pesquisa
    _concat_df: junta novas informações para dentro do dataframe a cada coleta de dados feita
    _save_to_excel: salva o dataframe em formato xlsx
    main: executa todas as funções construídas dentro da lógica da raspagem de dados
    """
    def __init__(self, headless = True):
        self.headless = headless
        self.options = Options()
        self.service = Service(ChromeDriverManager().install())
        self.dataframe = pd.DataFrame()

    def _options(self):
        print('\n\n\n\n\n')
        print('Digite abaixo o produto que você deseja pesquisar:')
        self.search_words = input()
        self.excel_filename = self.search_words.replace(' ', '_') + '.xlsx'
        print('Digite o número de páginas que você deseja para coletar dados:')
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
    
    def _create_folder(self):
        self.now = str(datetime.datetime.now())
        os.system('mkdir "' + self.now + '"')
        os.chdir(self.now)

    def _leave_folder(self):
        os.chdir('..')

    def _scraping_top_and_bottom(self):
        try:
            sleep(1)
            self.products = self.driver.find_elements(By.XPATH, '//div[starts-with(@class, "sh-np__product-title")]')
            self.prices = self.driver.find_elements(By.XPATH, '//span[@class = "T14wmb"]')
            self.sellers = self.driver.find_elements(By.XPATH, '//div[@class = "sh-np__seller-container"]')
            self.links = self.driver.find_elements(By.XPATH, '//a[@class = "shntl sh-np__click-target"]')
            self.df1 = pd.DataFrame() #dataframe com os preços dos itens nas barras de rolagem superior e inferior
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
            self.df2 = pd.DataFrame() #dataframe com os preços dos itens no corpo da página
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
            self.df3 = pd.DataFrame() #dataframe com os preços dos itens no corpo da página
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

    def _save_to_excel(self):
        self.dataframe = self.dataframe[~self.dataframe.duplicated()]
        self.dataframe.to_excel(self.excel_filename, engine = 'xlsxwriter', index = False)

    def _quit(self):
        self.driver.quit()

    def main(self):
        self._options()
        self._get_url()
        self._search()
        self._create_folder()
        i = 0
        while i < self.num_pages:
            print('Coletando dados da página {}'.format(i + 1))
            self._scraping_top_and_bottom()
            self._scraping_body()
            self._to_dataframe()
            self._scraping_body_2()
            self._to_dataframe_2()
            self._concat_df()
            try:
                self._next_page()
            except:
                print('Dados coletados.')
                break
            i += 1
        print('Dados coletados.')
        self._save_to_excel()
        self._leave_folder()
        self._quit()

bot = GSBot()
bot.main()

#from selenium import webdriver; from selenium.webdriver.common.by import By; driver = webdriver.Chrome(executable_path = './chromedriver')

    
