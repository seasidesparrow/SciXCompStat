import argparse
import datetime
import os
import compstat.utils as utils
import compstat.database as database

from SciXPipelineUtils.utils import load_config, setup_logging

proj_home = os.path.realpath(os.path.dirname(__file__))
config = load_config(proj_home=proj_home)
logger = setup_logging("run.py", proj_home=proj_home,
                       level=config.get("LOGGING_LEVEL", "INFO"),
                       attach_stdout=config.get("LOG_STDOUT", False))

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-l",
                        "--load-sets",
                        dest="load_sets",
                        action="store_true",
                        default=False,
                        help="Load stem2set.tab into postgres setidents table.")

    return parser.parse_args()

                       
def main():
    args = get_args()
    if args.load_sets:
        local_stem2set = "./tests/stubdata/input/stem2set.tab"
        stem2set_dict = utils.read_stem2set(local_stem2set)
        print("I have this many bibstems to write: %s" % len(stem2set_dict.keys()))
        try:
            database.write_stem2set_setidents(stem2set_dict)
        except Exception as err:
            logger.error("Well, shit: %s" % err)

if __name__ == "__main__":
    main()
