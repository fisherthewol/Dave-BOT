import sys

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        import lib.dave as bot
        clientcode = args[1]
        if clientcode:
            print("\nNote, regex checking hasn't been implemented - invalid "
                  "client codes error out one stage later.")
            print("\nMain File; discout is being called.")
            main = bot.Dave(clientcode)
            main.discout()
        else:
            raise SystemExit("Error: Errenous client code; "
                             "restart file and try again.")
    else:
        raise SystemExit("Usage:\npython3 main.py clientcode\nwhere "
                         "clientcode is the discord bot clientcode")
