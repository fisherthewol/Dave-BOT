import sys
if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        import DaveBOT.core as bot
        clientcode = args[1]
        if clientcode:
            print("Main File; discout is being called.")
            client = bot.Dave(clientcode)
            client.discout()
        else:
            raise SystemExit("Error: Empty client code. Try again.")
    else:
        raise SystemExit("Usage:\npython3 main.py clientcode\nwhere "
                         "clientcode is the discord bot clientcode")
