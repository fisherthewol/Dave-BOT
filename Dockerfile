FROM python:3

WORKDIR /usr/src/DaveBOT

RUN pip3 install --no-cache-dir discord.py requests praw feedparser

ADD . /usr/src/DaveBOT

CMD ["python3", "main.py"]
