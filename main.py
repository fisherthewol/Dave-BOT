import os, sys, logging


if __name__ == "__main__":
    args = sys.argv
    numberofargs = len(args)
    if numberofargs == 1:
        if (os.environ.get("clientcode") is None) or \
           (os.environ.get("client_id") is None) or \
           (os.environ.get("client_secret") is None):
            raise SystemExit("Error, environvar(s) not set")
        else:
            import DaveBOT.core as bot
            client = bot.Dave(os.environ.get("clientcode"))
            client.discout()
    elif numberofargs == 2:
        import DaveBOT.core as bot
        clientcode = args[1]
        if clientcode:
            print("Main File; discout is being called.")
            client = bot.Dave(clientcode)
            client.discout()
        else:
            raise SystemExit("Error: Empty client code. Try again.")
    elif numberofargs == 3:
        import DaveBOT.core as bot
        clientcode = args[1]
        loglevels = {"debug": logging.DEBUG,
                     "info": logging.INFO,
                     "warning": logging.WARNING,
                     "error": logging.ERROR,
                     "critical": logging.CRITICAL}
        loglevelcli = args[2].lower()
        if loglevelcli in loglevels:
            logginglevel = loglevels[loglevelcli]
        else:
            raise SystemExit("Invalid logging level.")
        print("Main File; discout is being called.")
        client = bot.Dave(clientcode, logginglevel)
        client.discout()
    else:
        raise SystemExit("Usage:\npython3 main.py clientcode loglevel\nwhere "
                         "clientcode is the discord bot clientcode, and\n"
                         "loglevel is a valid log level (default is INFO).")
