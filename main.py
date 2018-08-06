import argparse
import logging
import logging.handlers
import os

from DaveBOT import core


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
    logger.warning("Logging is setup in main.py")

    parser = argparse.ArgumentParser()
    parser.add_argument("-cc",
                        "--clientcode",
                        help="client code for discord.py",
                        type=str)
    parser.add_argument("-a",
                        "--adminid",
                        help="discord admin id",
                        type=str)
    parser.add_argument("-l",
                        "--loglevel",
                        help="change loglevel; valid levels are: debug,"
                             " info, warning, error, critical.",
                        type=str)
    parser.add_argument("-rid",
                        "--reddit_id",
                        help="reddit client id",
                        type=str)
    parser.add_argument("-rsc",
                        "--reddit_sc",
                        help="reddit client secret",
                        type=str)
    parser.add_argument("-w",
                        "--weather",
                        help="api key for openweathermap.org",
                        type=str)
    args = parser.parse_args()

    if args.clientcode:
        logger.info(f"clientcode found: {args.clientcode}")
        cc = args.clientcode
    else:
        cc = os.environ.get("clientcode")
        if cc:
            logger.info(f"clientcode found: {cc}")
        else:
            logger.critical("Empty clientcode: Not passed by env or cli.")
            parser.print_help()
            raise RuntimeError("Empty clientcode: Not passed by env or cli.")

    if args.adminid:
        logger.info(f"adminid found: {args.adminid}")
        adid = args.adminid
    else:
        adid = os.environ.get("adminid")
        if adid:
            logger.info("adminid")
        else:
            logger.warning("Adminid not found; loading all cogs by default.")

    if args.loglevel:
        logger.info("Loglevel found, working out what it is...")
        ll = findLogLevel(args.loglevel)
        if ll:
            logger.info(f"Loglevel is {str(ll)}")
        else:
            logger.error("Loglevel invalid, using default.")
            ll = logging.WARNING
    else:
        ll = os.environ.get("loglevel")
        if ll:
            logger.info("Loglevel found, working out what it is...")
            ll = findLogLevel(ll)
            if ll:
                logger.info(f"Loglevel is {str(ll)}")
            else:
                logger.error("Loglevel invalid, using default.")
                ll = logging.WARNING
        else:
            logger.warning("Loglevel not passed or in env, using default.")
            ll = logging.WARNING

    if args.reddit_id:
        logger.info(f"reddit_id found: {args.reddit_id}")
        rid = args.reddit_id
    else:
        rid = os.environ.get("reddit_id")
        if rid:
            logger.info(f"reddit_id found: {rid}")
        else:
            logger.warning("reddit_id not found, not enabling reddit.")
            rid = False
            rsc = False

    if rid:
        if args.reddit_sc:
            logger.warning(f"reddit_sc found: {args.reddit_sc} , enabling reddit.")
            rsc = args.reddit_sc
        else:
            rsc = os.environ.get("reddit_sc")
            if rsc:
                logger.info(f"reddit_sc found: {args.reddit_sc} , enabling reddit.")
            else:
                logger.warning("reddit_sc not found, not enabling reddit.")
                rid = False
                rsc = False

    if args.weather:
        logger.info(f"Weather found: {args.weather} , enabling weather.")
        wk = args.weather
    else:
        wk = os.environ.get("weather")
        if wk:
            logger.info(f"Weather found: {wk} , enabling weather.")
        else:
            logger.warning("Weather not found, not enabling.")
            wk = False

    bot = core.Dave(cc, adid, ll, rid, rsc, wk)
    bot.discout()


if __name__ == "__main__":
    main()
