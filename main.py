import argparse
import os

from DaveBOT import core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t",
                        "--token",
                        help="client token for discord",
                        type=str)
    parser.add_argument("-id",
                        "--adminid",
                        help="Discord userid of the bot's admin.")
    parser.add_argument("-v4",
                        help="force ipv4 (instead of v6)",
                        action="store_true")
    args = parser.parse_args()

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
