FROM python:3.9.13

WORKDIR /esy_shop_bot

COPY ./requirements.txt /esy_shop_bot/requirements.txt

RUN apt-get update 
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libnss3 lsb-release xdg-utils

#download and install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

RUN pip install --no-cache-dir --upgrade -r /esy_shop_bot/requirements.txt

COPY . /esy_shop_bot

CMD ["python", "app.py"]