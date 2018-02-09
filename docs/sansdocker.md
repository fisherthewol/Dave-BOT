# Running without docker:  

*nb: commands presume debian/apt; if you're using rpm then use the relevant commands.*
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
pip3 install praw
pip3 install -U discord.py
```
4. Generate a new app at the [discord website](https://discordapp.com/developers/applications/me). Copy the app id/token.
5. Visit [reddit's dev centre](https://reddit.com/prefs/apps/) to create an app (we recommend using personal use script) and grab the client_id and client_secret.  
6. Create a ```praw.ini``` file in the root directory and fill in the details:
```
[preqbot]
client_id=ID
client_secret=SECRET
```
You can see https://praw.readthedocs.io/en/latest/ for more details.  
7. Call the file using ```python3 main.py clientcode``` where clientcode is the token generated in step 3. It should produce the following output:
```
Login Successful
Name: **
ID: **
```  
8. Insert the ```ID``` it gives you as ID in https://discordapp.com/oauth2/authorize?client_id=ID&scope=bot&permissions=0  
9. That will allow you to add the bot to any servers where you have permission to do so.
