# Dave-BOT
A Discord bot based on Discord.py.
For our server, but could work for other servers.
*****
## Quickstart
The following is a quickstart guide to getting the bot running.
### Starting the bot as is.
Generate a new app at the [discord website](https://discordapp.com/developers/applications/me), and create a user on it. Copy the token and set it as a string inside ```client.run("")```.
When the program starts, it should output to console something like
```
Login Successful
Name: **
ID: **
```
Insert the number given as ```ID``` into https://discordapp.com/oauth2/authorize?client_id=ID&scope=bot&permissions=0, then open it in a browser
For the ~~reddit function~~ bot to work, you need to create a reddit app on reddit and create a praw.ini with the details from that; otherwise the file will fail on parsing.
See https://praw.readthedocs.io/en/latest/ for more details.
*****
### Adding Commands
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
