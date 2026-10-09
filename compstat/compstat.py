import json
import time
from contextlib import contextmanager
from datetime import datetime

from SciXPipelineUtils import utils
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def init_pipeline(proj_home)
    app = CompStat_APP(proj_home)
    app.logger.debugging("Starting compstat pipeline")

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
        self.logger = utils.setup_logging()
        self.engine = create_engine(self.config.get("SQLALCHEMY_URL")
        self.Session = sessionmaker(self.engine)
