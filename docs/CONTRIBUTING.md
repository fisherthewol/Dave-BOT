# Contributing  
Create a fork of the master branch for your own personal development. If you think you've made a significant contribution to the main code, open a pull request.  
If the code in your pull request is **too** incompatible with the master branch - IE, you've modified the core too much from the original - then we'll close it and ask you to open an issue with details that we can then work around.  
If you want to add a (singular) command, open an issue with the title beginning in !command. If you want to add a group of commands, use !group.  
If you find a bug, check if there's not already an issue open for it, then open one with !bug, giving as much useful detail as possible - we'll want a traceback, but not what you had for lunch.  
Incentive to contribute: we'll add you to the contributors on the repo! Meaning you can contribute more!  

# Syntax  
We use soft tabs (4 spaces), and try to stick close to PEP8.  

# Adding commands  
Find the main file (currently DaveBOT/core.py), add a  
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

Alternatively, you can create a cog. Create a file under /DaveBOT/cogs/, for example, /DaveBOT/cogs/test.py  
Then, inside of that, import discord.ext.commands (from discord.ext import commands), and write a class Test that takes one argument, bot, in the constructor:
```
from discord.ext import commands

class Test:
    def __init__(self, bot):
        self.client = bot
```
