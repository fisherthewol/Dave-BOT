import argparse
import logging
import os


def findLogLevel(leveltofind):
    loglevels = {"debug": logging.DEBUG,
                 "info": logging.INFO,
                 "warning": logging.WARNING,
                 "error": logging.ERROR,
                 "critical": logging.CRITICAL}
    if leveltofind.lower() in loglevels:
        return loglevels[leveltofind.lower()]
    else:
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-cc",
                        "--clientcode",
                        help="client code for discord code.",
                        type=str)
    parser.add_argument("-rid",
                        "--reddit_id",
                        help="reddit client id",
                        type=str)
    parser.add_argument("-rsc",
                        "--reddit_sc",
                        help="reddit client secret",
                        type=str)
    parser.add_argument("-l",
                        "--loglevel",
                        help="change loglevel",
                        type=str)
    args = parser.parse_args()

    if args.clientcode is None:
        cctopass = os.environ.get("clientcode")
        if cctopass is None:
            print("Empty clientcode: Not passed by env or cli.")
            parser.print_help()
            raise RuntimeError("Empty clientcode: Not passed by env or cli.")
        else:
            # import DaveBOT.core as core
            # davebot = core.Dave(cctopass)
            # davebot.discout()


if __name__ == "__main__":
    main()
