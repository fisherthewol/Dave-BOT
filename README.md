# Dave-BOT
A Discord bot based on Discord.py.  
For our server, but could work for other servers.  
## Quickstart  
The following is a quickstart guide to getting the bot running.  
### Using the instance on our server.  
You can use our copy of Dave-BOT. We take no responsibility for any issues arising out of your use of our service to the maximum legal extent.  
1. Make sure you can add bots to your discord.
2. Visit [the bot add link](https://discordapp.com/oauth2/authorize?client_id=321704542406443009&scope=bot&permissions=0).  
3. Select the server you want to add dave to.  
4. Enjoy!  

### Create your own instance.
1. Clone the master banch of the repo into your server.  
2. Generate a new app at the [discord website](https://discordapp.com/developers/applications/me), and create a user on it. Copy the  user token and set it as a string inside ```client.run("")``` in dave.py  
3. Visit [reddit's dev centre](https://reddit.com/prefs/apps/) to create an app (we recommend using personal use script) and grab the client_id and client_secret.  
4. Create a ```praw.ini``` file and fill it in with the details; EG:
```
[prequelbot]
client_id=ID
client_secret=secret
```
You can see https://praw.readthedocs.io/en/latest/ for more details.  
5. Run the file. When it starts, it should output
```
Login Successful
Name: **
ID: **
```  
6. Insert the ```ID``` it gices you as ID in https://discordapp.com/oauth2/authorize?client_id=ID&scope=bot&permissions=0  
7. That will allow you to add the bot to any servers where you have permission to.

## Development  
### Contributing  
Create a fork of the master branch for your own personal development. If you think you've made a significant contribution to the main code, open a pull request.  
If the code in your pull request is **too** incompatible with the master branch, we'll close it and ask you to open an issue with details that we can then work around.  
If you want to add a (singular) command, open an issue with the title beginning in !command. If you want to add a group of commands, use !group.  
Incentive to contribute: we'll add you to the contributors on the repo.  
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
