import os
from SciXPipelineUtils.utils import load_config, setup_logging

from compstat.models import CompStatMaster as master
from compstat.models import CompStatSummary as summary
from compstat.models import CompStatSetIDs as setidents

proj_home = os.path.realpath(os.path.join(os.path.dirname(__file__), "../"))
config = load_config(proj_home=proj_home)
logger = setup_logging(
    __name__,
    proj_home=proj_home,
    level=config.get("LOGGING_LEVEL", "INFO"),
    attach_stdout=config.get("LOG_STDOUT", False),
)

def write_stem2set_setidents(cls, stem2set):
    output_rows = []
    for k, v in stem2set.items():
        output_rows.append(setidents(bibstem=k, crossrefid=v))

    with cls.session_scope() as session:
        try:
            session.bulk_insert_mappings(setidents, output_rows)
            session.commit()
        except Exception as err:
            session.rollback()
            session.flush()
            logger.error("Failed to write stem2set to db: %s" % err)
