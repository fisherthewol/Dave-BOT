import argparse
import logging
import logging.handlers
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
    streamhandle = logging.StreamHandler()
    streamhandle.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s"
        " [in %(pathname)s:%(lineno)d]"))
    logger = logging.getLogger(__name__)
    logger.addHandler(streamhandle)
    logger.warning("Logging has been setup.")

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
        cc = os.environ.get("clientcode")
        if cc is None:
            logger.critical("Empty clientcode: Not passed by env or cli.")
            parser.print_help()
            raise RuntimeError("Empty clientcode: Not passed by env or cli.")
        else:
            logger.warning("clientcode found")
    else:
        logger.warning("clientcode found")
        cc = args.clientcode

    if args.reddit_id is None:
        rid = os.environ.get("reddit_id")
        if rid is None:
            logger.warning("reddit_id not found, not enabling reddit")
            rid = False
        else:
            logger.warning("reddit_id found")
    else:
        logger.warning("reddit_id found")
        rid = args.reddit_id


if __name__ == "__main__":
    main()
