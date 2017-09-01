# Dave-BOT
A Discord bot based on Discord.py.  
For our server, but could work for other servers.  
## Quickstart  
The following is a quickstart guide to getting the bot running.  
### Using the instance on our server.  
You can use our copy of Dave-BOT. We take no responsibility for any issues arising out of your use of our service to the maximum legal extent, and there is no guarantee that it will be available.  
1. Make sure you can add bots to your discord.
2. Visit [this bot add link](https://discordapp.com/oauth2/authorize?client_id=321704542406443009&scope=bot&permissions=0).  
3. Select the server you want to add dave to.  
4. Enjoy!  

### Create your own instance.
1. Clone the master branch of the repo into your server.  
2. Install packages:  
```
pip3 install feedparser
pip3 install praw
pip3 install -U discord.py
```
3. Generate a new app at the [discord website](https://discordapp.com/developers/applications/me). Copy it the app id/token.
4. Visit [reddit's dev centre](https://reddit.com/prefs/apps/) to create an app (we recommend using personal use script) and grab the client_id and client_secret.  
5. Create a ```praw.ini``` file and fill it in with the details; EG:
```
[prequelbot]
client_id=ID
client_secret=SECRET
```
You can see https://praw.readthedocs.io/en/latest/ for more details.  
6. Call the file using ```python3 clientcode``` where clientcode is the token generated in step 3. It should produce the following output:
```
Login Successful
Name: **
ID: **
```  
7. Insert the ```ID``` it gives you as ID in https://discordapp.com/oauth2/authorize?client_id=ID&scope=bot&permissions=0  
8. That will allow you to add the bot to any servers where you have permission to.

## Development  
### Contributing  
Create a fork of the master branch for your own personal development. If you think you've made a significant contribution to the main code, open a pull request.  
If the code in your pull request is **too** incompatible with the master branch - IE, you've modified the core too much from the original - then we'll close it and ask you to open an issue with details that we can then work around.  
If you want to add a (singular) command, open an issue with the title beginning in !command. If you want to add a group of commands, use !group.  
If you find a bug, check if there's not already an issue open for it, then open one with !bug, giving as much useful detail as possible - we'll want a traceback if you have one, but not what you had for lunch.  
Incentive to contribute: we'll add you to the contributors on the repo! Meaning you can contribute more!  
### Syntax  
We use soft tabs (4 spaces), and try to stick close to PEP8.  
### Adding commands  
Find the main file (currently dave.py), add a  
```
@client.command(pass_context=True)
async def cmd(ctx):
    stuff
```   
where ```cmd``` is your command to put after !, and ```stuff``` is what to do when that happens.   
```stuff``` can be anything, we recommend using ```await client.say(string)``` for a basic thing.  
For example:  
```
@client.command(pass_context=True)
async def ping(ctx):
    await client.say("Pong!")
```  
Adding this makes the bot reply "Pong!" to !ping in chat.  
