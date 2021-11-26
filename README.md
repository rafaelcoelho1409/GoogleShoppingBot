# Web Scraping com Selenium para coletar preços de produtos no Google Shopping

## Objetivo deste bot:
- Armazenar em uma tabela os produtos, preços, lojas e links de cada item que aparece em uma pesquisa no Google Shopping. Por exemplo, se você deseja pesquisar preços de celulares, basta digitar 'celulares' como termo de pesquisa no terminal de comando após executar o script python.

## Recursos utilizados:
- Webdriver: ChromeDriver (Chrome)
- Visual Studio Code
- python3.8
- pip3: gerenciador de pacotes python3.x

## Pacotes do Python usados para construir o bot:
- Selenium Webdriver (selenium)
- Webdriver Manager (webdriver_manager)
- time
- pandas
- datetime
- os

## Para rodar este bot em sua máquina:
- baixe este repositório (pasta) em sua máquina. Você pode usar o seguinte comando no seu terminal de comando:
> git clone https://github.com/rafaelcoelho1409/GoogleShoppingBot.git

- escolha seu interpretador Python (python3, python3.x)

- execute os seguintes comandos (para Linux):
> cd GoogleShoppingBot  
> python3 GoogleShoppingBot.py

## Executando o bot em Docker (para Linux):
- Instale o docker em sua máquina local. Tutorial de instalação no site abaixo:
> https://docs.docker.com/engine/install/

<h2> Execute os seguintes comandos no seu terminal: </h2>
- Construa a imagem Docker a partir do Dockerfile desta pasta:
> sudo docker build -t gsbot:v1 .

- Execute um novo contâiner a partir da imagem criada com o volume criado anexado a este contâiner:
> sudo docker container run -it --name gsbot gsbot:v1

- Digite a pesquisa que você deseja fazer (exemplo: samsung galaxy s21) e dê ENTER

- Digite o número de páginas da pesquisa do google que você deseja que o bot faça a coleta dos produtos e preços

- Copie o nome do arquivo gerado ao fim da execução (ARQUIVO_CSV)

- Após isso, para poder abrir os arquivos em sua máquina local:
> sudo docker container ls -a #copie o CONTAINER_ID do contâiner chamado 'gsbot'  
> sudo docker cp CONTAINER_ID:/home/seluser/'ARQUIVO_CSV' .  
(ex: sudo docker cp d5f466d18766:/home/seluser/'pe_de_cabra-2021-11-08 21:35:55.679724.csv' .)  
> sudo -s #abre o modo root para acessar os arquivos  
> cd seluser  
> ls #liste a pasta seluser para visualizar os arquivos dentro  
Copie o nome do arquivo csv (ARQUIVO_CSV) que aparece nessa listagem  
> libreoffice ARQUIVO_CSV (ex: cama_elastica.csv) #Abre a tabela em csv no LibreOffice  
> #dê CTRL-D para sair do modo root

- Caso precise deletar o csv extraído do contâiner 'gsbot':
> sudo -s #modo root  
> rm -r ARQUIVO_CSV #deleta o arquivo csv vindo do contâiner
> #dê CTRL-D para sair do modo root

- Para executar o bot novamente no mesmo contâiner:
> sudo docker container start gsbot  
> sudo docker container exec -it gsbot python3 GoogleShoppingBot.py

- Para deletar o contâiner:
> sudo docker container stop gsbot  
> sudo docker container rm gsbot





