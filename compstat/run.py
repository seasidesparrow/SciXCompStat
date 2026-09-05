import argparse
import datetime
import os

from adsputils import load_config, setup_logging

from adscompstat import tasks, utils
from adscompstat.exceptions import (
    DBClearException,
    DBWriteException,
    GetLogException,
    LoadClassicDataException,
)
from adscompstat.models import CompStatAltIdents as alt_identifiers
from adscompstat.models import CompStatIdentDoi as identifier_doi
from adscompstat.models import CompStatIssnBibstem as issn_bibstem

proj_home = os.path.realpath(os.path.join(os.path.dirname(__file__), "./"))
conf = load_config(proj_home=proj_home)
logger = setup_logging(
    "run.py",
    proj_home=proj_home,
    level=conf.get("LOGGING_LEVEL", "INFO"),
    attach_stdout=conf.get("LOG_STDOUT", False),
)


def get_arguments():
    parser = argparse.ArgumentParser(description="Command line options.")

    parser.add_argument(
        "-p",
        "--publisher-prefix",
        dest="do_pub",
        action="store",
        default=None,
        help="Parse only logs for one publisher DOI prefix",
    )

    parser.add_argument(
        "-l",
        "--latest",
        dest="do_latest",
        action="store_true",
        default=False,
        help="Do only records from the most recent harvest",
    )

    parser.add_argument(
        "-m",
        "--completeness",
        dest="do_completeness",
        action="store_true",
        default=False,
        help="Calculate completeness summary for all harvested bibstems",
    )

    parser.add_argument(
        "-j",
        "--json",
        dest="do_json_export",
        action="store_true",
        default=False,
        help="Export completeness summary to JSON file",
    )

    parser.add_argument(
        "-r",
        "--retry",
        dest="do_retry",
        action="store_true",
        default=False,
        help="Retry all mismatched and unmatched records",
    )

    args = parser.parse_args()
    return args


def get_logs(args):
    logfiles = utils.get_updateagent_logs(conf.get("HARVEST_LOG_DIR", "/"))
    if logfiles:
        logfiles.sort()
        (dates, pubdois) = utils.parse_pub_and_date_from_logs(logfiles)
        if args.do_pub:
            if args.do_pub in pubdois:
                newlogs = list()
                try:
                    for logfile in logfiles:
                        if args.do_pub in logfile:
                            newlogs.append(logfile)
                except Exception as err:
                    raise GetLogException(
                        "Problem selecting publisher (%s): %s" % (args.do_pub, err)
                    )
                logfiles = newlogs
            else:
                raise GetLogException("No log files available for publisher %s" % args.do_pub)
        if args.do_latest:
            today = datetime.datetime.today()
            newlogs = list()
            for ff in logfiles:
                age = today - datetime.datetime.fromtimestamp(os.path.getmtime(ff))
                if age.days < 7:
                    newlogs.append(ff)
            logfiles = newlogs
    return logfiles


def main():
    try:
        args = get_arguments()

        if args.do_completeness:
            tasks.task_do_all_completeness()
        elif args.do_json_export:
            tasks.task_export_completeness_to_json()
        elif args.do_retry:
            for result_type in ["mismatch", "unmatched", "failed"]:
                tasks.task_retry_records.delay(result_type)
        else:
            logfiles = get_logs(args)
            if not logfiles:
                logger.warning("No logfiles found! Nothing to do -- stopping.")
            else:
                for logfile in logfiles:
                    tasks.task_process_logfile.delay(logfile)
    except Exception as err:
        logger.error("Process failed: %s" % err)


if __name__ == "__main__":
    main()
