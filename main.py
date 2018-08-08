import argparse
import configparser
import os

from DaveBOT import core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-co",
                        "--configobject",
                        help="specify where to find config file; "
                             "uses environ if not specified",
                        type=str)
    parser.add_argument("-tk",
                        "--token",
                        help="client token for discord",
                        type=str)
    parser.add_argument("-id",
                        "--adminid",
                        help="Discord userid of the bot's admin.",
                        type=str)
    parser.add_argument("-v4",
                        help="force ipv4 (instead of v4/v6)",
                        action="store_true")
    args = parser.parse_args()

    if args.configobject:
        config = configparser.ConfigParser()
        config.read(args.configobject)
        print(config["DaveBOT"])
        return
    else:
        if args.token:
            os.environ["token"] = args.token
        elif not os.environ.get("token"):
            raise RuntimeError("No discord token found.")

        if args.adminid:
            os.environ["adminid"] = args.admin

    bot = core.Dave(cc, adid, ll, rid, rsc, wk)
    bot.discout()


if __name__ == "__main__":
    main()
