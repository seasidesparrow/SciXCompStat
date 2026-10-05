import argparse
import datetime
import os

from SciXPipelineUtils.utils import load_config, setup_logging

proj_home = os.path.realpath(os.path.dirname(__file__))
config = load_config(proj_home=proj_home)
logger = setup_logging("run.py", proj_home=proj_home,
                       level=config.get("LOGGING_LEVEL", "INFO"),
                       attach_stdout=config.get("LOG_STDOUT", False))

def get_args():
    parser = ArgumentParser()

    parser.add_argument("-l",
                        "--load-sets",
                        dest="load_sets",
                        action="store",
                        default=None,
                        help="Load stem2set.tab into postgres setidents table.")

    return parser.parse_args()

                       
def main():
    logger.info("I'm a logging statement, hoopty doo...")

if __name__ == "__main__":
    main()
