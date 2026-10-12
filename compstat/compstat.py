import json
import os
import time
from contextlib import contextmanager
from datetime import datetime

import compstat.parser as simpleparser
from compstat.harvester import OAIHarvest

from SciXPipelineUtils import utils
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from compstat.models import CompStatMaster as master
from compstat.models import CompStatSummary as summary
from compstat.models import CompStatSetIDs as setidents


proj_home = os.path.realpath(os.path.join(os.path.dirname(__file__), "../"))
config = utils.load_config(proj_home=proj_home)
logger = utils.setup_logging(
    __name__,
    proj_home=proj_home,
    level=config.get("LOGGING_LEVEL", "INFO"),
    attach_stdout=config.get("LOG_STDOUT", False),
)


class CompStat_APP:
    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def __init__(self, proj_home):
        self.config = utils.load_config(proj_home)
        self.logger = logger
        self.engine = create_engine(self.config.get("SQLALCHEMY_URL"))
        self.Session = sessionmaker(self.engine)


def init_pipeline(proj_home):
    app = CompStat_APP(proj_home)
    app.logger.debugging("Starting compstat pipeline")

def write_stem2set_setidents(stem2set):
    output_rows = []
    app = CompStat_APP(proj_home)
    for k, v in stem2set.items():
        for row in v:
            row.update({"bibstem": k})
            output_rows.append(row)

    with app.session_scope() as session:
        try:
            session.bulk_insert_mappings(setidents, output_rows)
            session.commit()
        except Exception as err:
            session.rollback()
            session.flush()
            logger.error("Failed to write stem2set to db: %s" % err)

def harvest_one(bibstem):
    app = CompStat_APP(proj_home)
    with app.session_scope() as session:
        try:
            ident = session.query(setidents.doi_prefix, setidents.xr_journalid).filter(setidents.bibstem=bibstem).first()
            identifier = ":".join(ident)
            qparams = {
                "metadataPrefix": "cr_unixml",
                "set": identifier,
                "from": "2026-09-01"
            }

            harvester = OAIHarvest(qparams=qparams)
            harvester.do_harvest(config.get("HEADER", "{}"))
            write_records(harvester.allRecords)
        except Exception as err:
            logger.error("Unable to harvest %s: %s" % (bibstem, err))

def write_records(records):
    master_rows = []
    try:
        for rec in records:
            doi = rec.get("doi", None)
            origin = "CROSSREF"
            master_rows.append({"doi": doi, "origin": origin, "crmetadata": rec})
        if master_rows:
            with app.session_scope() as session:
            try:
                session.bulk_insert_mappings(master, master_rows)
                session.commit()
            except Exception as err:
                session.rollback()
                session.flush()
                logger.error("Failed to write records to master: %s" % err)
