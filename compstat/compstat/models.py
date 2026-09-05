from datetime import datetime
from dateutil import tz

from SciXPipelineUtils.scix_uuid import scix_uuid as uuid
from sqlalchemy import Column, Float, Integer, String, Text, JSON, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def get_date():
    return datetime.utcnow().replace(tzinfo=tz.tzutc())

class CompStatXMLData(Base):
    __tablename__ = "xmldata"

    dataid = Column(Integer, primary_key=True, unique=True)
    record = Column(Text, nullable=True)
    doi = Column(String, index=True, nullable=False)
    indexed = Column(Boolean, nullable=False)
    created = Column(UTCDateTime, index=True, default=get_date)
    updated = Column(UTCDateTime, index=True, default=get_date)

    def __repr__(self):
        return "xmldata.dataid='{self.dataid}', xmldata.doi='{self.doi}', xmldata.indexed='{self.indexed}'".format(
            self=self
        )

    def toJSON(self):
        return {
            "dataid": self.dataid,
            "record": self.record,
            "doi": self.doi,
            "indexed": self.indexed,
            "created": self.created,
            "updated": self.updated
        }



class CompStatMaster(Base):
    __tablename__ = "master"

    masterid = Column(Integer, primary_key=True, unique=True)
    dataid = Column(Integer, ForeignKey('xmldata.dataid'),
                    primary_key=True, nullable=False)
    doi = Column(String, unique=True, index=True, nullable=False)
    journalid = Column(JSON, nullable=True)
    origin = Column(String, nullable=False)
    metadata = Column(JSON, nullable=False)
    bibcode = Column(Text, index=True, nullable=True)
    scix_id = Column(Text, index=True, nullable=True)
    is_valid = Column(Boolean, index=True, nullable=False)
    doi_found = Column(Boolean, index=True, nullable=False)
    meta_found = Column(Boolean, index=True, nullable=False)
    notes = Column(String, nullable=True)
    created = Column(UTCDateTime, index=True, default=get_date())
    updated = Column(UTCDateTime, index=True, onupdate=get_date())

    def __repr__(self):
        return "master.masterid='{self.masterid}', master.scix_id='{self.scix_id}', master.doi='{self.doi}'".format(
            self=self
        )

    def toJSON(self):
        return {
            "masterid": self.masterid,
            "dataid": self.dataid,
            "doi": self.doi,
            "journalid": self.journalid,
            "origin": self.origin,
            "metadata": self.metadata,
            "bibcode": self.bibcode,
            "scix_id": self.scix_id,
            "is_valid": self.is_valid,
            "doi_found": self.doi_found,
            "meta_found": self.meta_found,
            "notes": self.notes,
            "created": self.created,
            "updated": self.updated
        }

"""
    # THIS WILL DEPEND ON YOUR SELECT STATEMENT, SET UP LATER
    def toRow(rowdat):
        if len(rowdat) == 6:
            return {"inst_iso_country": rowdat[0],
                    "inst_country": rowdat[1],
                    "inst_parents": rowdat[2],
                    "inst_id": rowdat[3],
                    "inst_abbreviation": rowdat[4],
                    "inst_canonical": rowdat[5]}
        else:
            return {}
"""


class CompStatSummary(Base):
    __tablename__ = "summary"

    summaryid = Column(Integer, primary_key=True, unique=True)
    journalid = Column(String, nullable=False)
    volume = Column(Integer, nullable=False)
    volume_letter = Column(String, nullable=True)
    paper_count = Column(Integer, nullable=False)
    complete_fraction = Column(Float, nullable=True)
    complete_by_year = Column(Text, nullable=True)
    complete_details = Column(Text, nullable=True)
    created = Column(UTCDateTime, default=get_date)
    updated = Column(UTCDateTime, onupdate=get_date)

    def __repr__(self):
        return "summary.summaryid='{self.summaryid}', summary.complete_fraction='{self.summary.complete_fraction}'"

    def toJSON(self):
        return {
            "summaryid": self.summaryid,
            "journalid": self.journalid,
            "volume": self.volume,
            "volume_letter": self.volume_letter,
            "paper_count": self.paper_count,
            "complete_fraction": self.complete_fraction,
            "complete_by_year": self.complete_by_year,
            "complete_details": self.complete_details,
            "created": self.created,
            "updated": self.updated,
        }

