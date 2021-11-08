FROM selenium/standalone-chrome
WORKDIR /home/seluser
COPY ./GoogleShoppingBot.py /home/seluser
USER root
RUN sudo apt-get -y update \
&& sudo apt-get install -y python3-pip \
&& sudo pip3 install selenium webdriver-manager pandas datetime
# set display port to avoid crash
ENV DISPLAY=:99
CMD ["python3.8", "GoogleShoppingBot.py"]