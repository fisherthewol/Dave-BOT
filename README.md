# Dave-BOT
A Discord bot based on Discord.py.  
For our server, but could work for other servers.  
*****
# Quickstart  
The following is a quickstart guide to getting the bot running and adding commands.  
## Starting the bot as is.  
Generate a new app at the discord website, and create a user on it. Copy the token and set it as a string inside ```client.run("")```.  
## Adding Commands  
Find the main file (currently dave.py), add a  
```
@client.command(pass_context=True)
async def cmd(ctx):
    stuff
```   
where cmd is your command to put after !, and stuff is what to do when that happens.   
stuff can be anything, we recommend using ```await client.say(string)``` for a basic thing.  
For example:  
```
@client.command(pass_context=True)
async def ping(ctx):
    await client.say("Pong!")
```  
This replies "Pong!" to !ping in chat.  
