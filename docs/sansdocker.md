# Running without docker:  

*nb: commands presume debian/apt; if you're using rpm then please use the relevant commands.*
1. Clone the master branch of the repo into your server.  
2. Setup a virtualenv and activate it:  
```
# if not already installed:
sudo apt install virtualenv
# then:
virtualenv venv
. venv/bin/activate
```
3. Install packages:  
```
pip3 install feedparser
pip3 install -U discord.py
(optionally) pip3 install praw
```
4. Generate a new app at the [discord website](https://discordapp.com/developers/applications/me). Copy the app id/token.
5. Optionally, visit [reddit's dev centre](https://reddit.com/prefs/apps/) to create an app (we recommend using personal use script) and grab the client_id and client_secret. (Also optionally) Obtain an openweathermap [api key](https://home.openweathermap.org/api_keys).
6. Launch syntax is ```python3 main.py -cc clientcode [-l loglevel] [-rid reddit_id] [-rsc reddit_sc] [-w weather]``` where clientcode is the token generated in step 3. It should produce the following output:
```
Login Successful
Name: **
ID: **
```  
7. Insert the ```ID``` it gives you as ID in https://discordapp.com/oauth2/authorize?client_id=ID&scope=bot&permissions=0  
8. That will allow you to add the bot to any servers where you have permission to do so.
