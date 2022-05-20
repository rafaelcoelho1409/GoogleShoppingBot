# Web Scraping with Selenium to collect product prices on Google Shopping

## Purpose:
- Store into a data table products, prices, shops and links from each item displayed in a search on Google Shopping. For example, if you want to search smartphone prices, it's enough to type 'smartphones' as a search term on command terminal after executing Python script.

## Resources:
- Webdriver: ChromeDriver (Chrome)
- Visual Studio Code
- python3.8
- pip3: python3.x packages manager

## Python packages used to build the bot:
- Selenium Webdriver (selenium)
- Webdriver Manager (webdriver_manager)
- time
- pandas
- datetime
- os

## Running this bot on a local machine:
- clone this repo in your machine:  
> git clone https://github.com/rafaelcoelho1409/GoogleShoppingBot.git

- choose a Python interpreter (python3.x)

- execute the following commands (for Linux):
> cd GoogleShoppingBot  
> python3 GoogleShoppingBot.py

## Running this bot on Docker (for Linux):
- Install Docker in your local machine. Installation tutorial in the link below:
> https://docs.docker.com/engine/install/

<h2> Execute the following commands in your terminal: </h2>  
  
- Build a Docker image from Dockerfile in this repo:  
> sudo docker build -t gsbot:v1 .

- Run a new container from the created image:
> sudo docker container run -it --name gsbot gsbot:v1

- Type the search term you want to do (example: samsung galaxy s21) and click ENTER

- Type the number of pages from google search you want to the bot collecting products and prices

- Copy the file name created in the end of the running (CSV_FILE)

- After, to open files in your local machine:
> sudo docker container ls -a #copy the CONTAINER_ID from container called 'gsbot'  
> sudo docker cp CONTAINER_ID:/home/seluser/'CSV_FILE' .  
> #(ex: sudo docker cp d5f466d18766:/home/seluser/'smartphone-2021-11-08 21:35:55.679724.csv' .)  
> sudo -s #open root mode to access files  
> cd seluser  
> ls #list 'seluser' folder files to see files into  
Copy the csv file name (CSV_FILE) that is in the list from 'ls' command  
> libreoffice CSV_FILE (example: smartphone.csv) #Open the CSV table on LibreOffice  
> #Type CTRL-D to exit root mode

- In the case you need to delete the CSV file extracted from 'gsbot' container:
> sudo -s #root mode  
> rm -r CSV_FILE #deletes the csv file from the container
> #Type CTRL-D to exit root mode

- To run this bot again in the same container:
> sudo docker container start gsbot  
> sudo docker container exec -it gsbot python3 GoogleShoppingBot.py

- To delete this container:
> sudo docker container stop gsbot  
> sudo docker container rm gsbot





