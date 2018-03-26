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
        logger.info("clientcode found: {}".format(args.clientcode))
        cc = args.clientcode
    else:
        cc = os.environ.get("clientcode")
        if cc:
            logger.info("clientcode found: {}".format(cc))
        else:
            logger.critical("Empty clientcode: Not passed by env or cli.")
            parser.print_help()
            raise RuntimeError("Empty clientcode: Not passed by env or cli.")

    if args.loglevel:
        logger.info("Loglevel found, working out what it is...")
        ll = findLogLevel(args.loglevel)
        if ll:
            logger.info("Loglevel is {}".format(str(ll)))
        else:
            logger.error("Loglevel invalid, using default.")
            ll = logging.WARNING
    else:
        ll = os.environ.get("loglevel")
        if ll:
            logger.info("Loglevel found, working out what it is...")
            ll = findLogLevel(ll)
            if ll:
                logger.info("Loglevel is {}".format(str(ll)))
            else:
                logger.error("Loglevel invalid, using default.")
                ll = logging.WARNING
        else:
            logger.warning("Loglevel not passed or in env, using default.")
            ll = logging.WARNING

    if args.reddit_id:
        logger.info("reddit_id found: {}".format(args.reddit_id))
        rid = args.reddit_id
    else:
        rid = os.environ.get("reddit_id")
        if rid:
            logger.info("reddit_id found: {}".format(rid))
        else:
            logger.warning("reddit_id not found, not enabling reddit.")
            rid = False
            rsc = False

    if rid:
        if args.reddit_sc:
            logger.warning("reddit_sc found: {} , "
                           "enabling reddit.".format(args.reddit_sc))
            rsc = args.reddit_sc
        else:
            rsc = os.environ.get("reddit_sc")
            if rsc:
                logger.info("reddit_sc found {} , "
                            "enabling reddit.".format(args.reddit_sc))
            else:
                logger.warning("reddit_sc not found, not enabling reddit.")
                rsc = False

    if args.weather:
        logger.info("Weather found: {} , "
                    "enabling weather.".format(args.weather))
        wk = args.weather
    else:
        wk = os.environ.get("weather")
        if wk:
            logger.info("Weather found: {} , "
                        "enabling weather.".format(wk))
        else:
            logger.warning("Weather not found, not enabling.")
            wk = False

    bot = core.Dave(cc, ll, rid, rsc, wk)
    bot.discout()


if __name__ == "__main__":
    main()
