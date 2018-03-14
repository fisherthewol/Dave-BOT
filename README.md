# Dave-BOT
A Discord bot based on [Discord.py](https://github.com/Rapptz/discord.py).   
## Quickstart  
The following is a quickstart guide to getting the bot running.  
### Using the instance on our server:  
You can use our copy of Dave-BOT. We take no responsibility for any issues arising out of your use of our service to the maximum legal extent, and there is no guarantee that it will be available.  
1. Make sure you can add bots to your discord.
2. Visit [this bot add link](https://discordapp.com/oauth2/authorize?client_id=321704542406443009&scope=bot&permissions=0).  
3. Select the server you want to add dave to.  
4. Enjoy!  

### Run your own: Docker:  
This app will build into a docker container:
- Get your [discord clientcode](https://discordapp.com/developers/applications/me).
- Optionally, get your [reddit client_id and _secret](https://reddit.com/prefs/apps/) (we recommend using a personal user script), and your [openweathermap api key](https://home.openweathermap.org/api_keys).  
- Download and install docker.  
- Clone the master branch/get the source of the latest release of the repo.  
- cd into the top level of the repo (Usually ```cd Dave-BOT```).  
- Build with ```sudo docker build -t dave:master .```  
- Create a file called env.list and put your discord clientcode (and optional keys) in it:  
```
clientcode=CODE HERE
client_id=ID HERE
client_secret=SECRET HERE
weather=KEY HERE
```
- Run with ```sudo docker run -d --env-file env.list dave:master```  
- Get your ID by running ```sudo docker logs <name>``` where <name> is the container name/id; insert it as ```ID``` into https://discordapp.com/oauth2/authorize?client_id=ID&scope=bot&permissions=0; this allows you to add it to any servers where you are allowed to do so.  
- To stop, ```sudo docker stop <name>```  

For running without docker, see docs/sansdocker.md  
For development and contributing, see docs/CONTRIBUTING.md  

DaveBOT/owmaw/cond.json is credited to [tbranyen](https://gist.github.com/tbranyen/62d974681dea8ee0caa1#file-icons-json)
