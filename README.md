# Dave-BOT
A Discord bot based on Discord.py.  
For our server, but could work for other servers.  
*****
# Quickstart  
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
