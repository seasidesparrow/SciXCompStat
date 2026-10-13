import os
from time import sleep

import requests
from SciXPipelineUtils import utils
#from bs4 import BeautifulSoup

from lxml import etree
import io

proj_home = os.path.realpath(os.path.join(os.path.dirname(__file__), "../"))
conf = utils.load_config(proj_home=proj_home)
logger = utils.setup_logging(
    "harvester",
    level=conf.get("LOGGING_LEVEL", "WARN"),
    proj_home=proj_home,
    attach_stdout=conf.get("LOG_STDOUT", "FALSE"),
)


class OAIHarvest(object):
    def __init__(self, host="oai.crossref.org", verb="ListRecords", qparams={}, loop=True, verbose=False, sleep=1):
        self.protocol = "https"
        self.host = host
        self.verb = verb
        self.qparams = qparams
        self.loop = loop
        self.verbose = verbose
        self.allRecords = []
        self.sleep = sleep
        self.startToken = None
        self.lastToken = -1
        pass

    def _parse_response(self, response):
        logger.debug("Here is the status code: %s" % response.status_code)
        if response.status_code == 200:
            # fetch records from server and create bs4 object
            data = response._content
            """
            soup = BeautifulSoup(data, "lxml-xml")
            newRecords = soup.findAll("record")
            """
            # new parsing using lxml for speed
            newRecords = []
            OAI = "{http://www.openarchives.org/OAI/2.0/}"
            for _, rec in etree.iterparse(io.BytesIO(data) events=("end",), tag=OAI + "record"):
                doi = rec.findtext(f"{OAI}header/{OAI}identifier")
                newRecords.append(rec)
                rec.clear()
                while rec.getprevious() is not None:
                    del rec.getparent()[0]
            if self.verbose:
                logger.debug("Found %s records." % len(newRecords))
            self.allRecords.extend(newRecords)
            try:
                self.startToken = etree.fromstring(data).findtext(".//+OAI+"resumptionToken")
            except Exception as noop:
                self.startToken = None
                if self.verbose:
                    logger.debug("No resumption token found: %s" % noop)
            if self.startToken:
                if self.verbose:
                    logger.debug("resumptionToken found: %s" % self.startToken)
                if self.startToken == self.lastToken:
                    if self.verbose:
                        logger.info("Error: got the identical resumptionToken back, exiting.")
                    self.loop = False
                else:
                    self.lastToken = self.startToken
                    self.qparams = {"resumptionToken": self.startToken}
            else:
                if self.verbose:
                    logger.debug("No resumptionToken found, stopping.")
                self.loop = False
        elif response.status_code[0] == "5":
            logger.info("Transient error %s, sleeping % seconds" % (response.status_code, self.sleep))
        else:
            if self.verbose:
                logger.warning("Error: got unexpected HTTP response %s" % response.status_code)
                self.loop = False

    def do_harvest(self, headers={}):
        if not (self.host and self.verb):
            raise Exception("You need both a hostname and an action/verb for harvesting.")
        else:
            url_base = self.protocol + "://" + self.host + "/oai?" + "verb=%s" % self.verb
            count = 0
            logger.debug("Loop status is: %s" % self.loop)
            while self.loop:
                url_query = ""
                for k, v in self.qparams.items():
                    url_query = url_query + "&%s=%s" % (k, v)
                url = url_base + url_query
                logger.debug("Querying URL: %s" % url)
                response = requests.get(url, headers=headers)
                count += 1
                logger.debug("Finished loop # %s" % count)
                self._parse_response(response)
