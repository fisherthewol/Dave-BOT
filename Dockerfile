FROM python:3.6

WORKDIR /usr/src/DaveBOT

RUN pip3 install --no-cache-dir discord.py praw feedparser

ADD . /usr/src/DaveBOT

CMD ["python3", "main.py"]
