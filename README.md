# Dave-BOT
A Discord bot based on Discord.py.  
For our server, but could work for other servers.  
## Quickstart  
The following is a quickstart guide to getting the bot running.  
### Using the instance on our server:  
You can use our copy of Dave-BOT. We take no responsibility for any issues arising out of your use of our service to the maximum legal extent, and there is no guarantee that it will be available.  
1. Make sure you can add bots to your discord.
2. Visit [this bot add link](https://discordapp.com/oauth2/authorize?client_id=321704542406443009&scope=bot&permissions=0).  
3. Select the server you want to add dave to.  
4. Enjoy!  

### Create your own instance:  

#### Docker:  
This app will build into a docker container:
- Get your [discord clientcode](https://discordapp.com/developers/applications/me) and [reddit client_id and _secret](https://reddit.com/prefs/apps/) (we recommend using a personal user script).  
- Download and install docker.  
- Clone the master branch of this repo.  
- cd into the top level of the repo (Usually ```cd Dave-BOT```).  
- Build with ```sudo docker build -t dave:master .```  
- Create a file called env.list and put your client_id, client_secret, and discord client code into it:  
```
client_id=ID HERE
client_secret=SECRET HERE
clientcode=CODE HERE
```
- Run with ```sudo docker run -d --env-file env.list dave:master```  
- Get your ID by running ```sudo docker logs <name>``` where <name> is the container name/id; insert it as ```ID``` into https://discordapp.com/oauth2/authorize?client_id=ID&scope=bot&permissions=0; this allows you to add it to any servers where you are allowed to do so.  
- To stop, ```sudo docker stop <name>```  

#### Raw python:  
*nb: commands presume debian/apt; if you're using rpm then use the relevant commands.*
1. Clone the master branch of the repo into your server.  
2. Setup a virtualenv and activate it:  
```
# if not already installed:
sudo apt install virtualenv
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
6. Create a ```praw.ini``` file and fill it in with the details; EG:
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

## Development  
### Contributing  
Create a fork of the master branch for your own personal development. If you think you've made a significant contribution to the main code, open a pull request.  
If the code in your pull request is *too* incompatible with the master branch - IE, you've modified the core too much from the original - then we'll close it and ask you to open an issue with details that we can then work around.  
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
    content
```   
where ```cmd``` is your command to put after !, and ```content``` is what to do when that happens.   
```content``` can be anything; try starting with ```await client.say(string)```.  
For example:  
```
@client.command(pass_context=True)
async def ping(ctx):
    await client.say("Pong!")
```  
Adding this makes the bot reply "Pong!" to !ping in chat.  
