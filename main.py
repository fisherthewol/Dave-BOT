import sys

if __name__ == "__main__":
    import lib.dave as bot
    args = sys.argv
    if len(args) == 3:
        import lib.dave as bot
        if args[1] == "nogui":
            print("nogui specified, running nogui.")
            clientcode = args[2]
            if clientcode:
                print("\nMain File; discout is being called.")
                main = bot.Dave(clientcode)
                main.discout()
            else:
                raise SystemExit("Error: Empty client code; "
                                 "restart file and try again.")
        elif args[1] == "gui":
            raise SystemExit("GUI not implemented yet; exiting.")
    elif len(args) == 2:
        import lib.dave as bot
        if args[1] == "nogui":
            print("nogui specified, running nogui.")
            clientcode = str(input("Input client code:\n"))
            if clientcode:
                print("\nMain File; discout is being called.")
                main = bot.Dave(clientcode)
                main.discout()
            else:
                raise SystemExit("Error: Empty client code; "
                                 "restart file and try again.")
        elif args[1] == "gui":
            raise SystemExit("GUI not implemented yet; exiting.")
    else:
        raise SystemExit("Usage:\npython3 main.py (no)gui clientcode\nwhere "
                         "gui/nogui is your selection and clientcode is "
                         "the discord bot clientcode")
