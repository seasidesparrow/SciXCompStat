from datetime import datetime
from dateutil import tz

from sqlalchemy import Column, Float, Integer, String, Text, JSON, Boolean, Index, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def get_date():
    return datetime.utcnow().replace(tzinfo=tz.tzutc())


class CompStatMaster(Base):
    __tablename__ = "master"

    masterid = Column(Integer, primary_key=True, unique=True)
    doi = Column(String, unique=True, index=True, nullable=False)
    journalid = Column(JSON, nullable=True)
    origin = Column(String, nullable=False)
    crmetadata = Column(JSON, nullable=False)
    bibcode = Column(Text, index=True, nullable=True)
    scix_id = Column(Text, index=True, nullable=True)
    is_valid = Column(Boolean, index=True, nullable=False)
    doi_found = Column(Boolean, index=True, nullable=False)
    meta_found = Column(Boolean, index=True, nullable=False)
    notes = Column(String, nullable=True)
    created = Column(DateTime(timezone=True), index=True, default=get_date())
    updated = Column(DateTime(timezone=True), index=True, onupdate=get_date())

    def __repr__(self):
        return "master.masterid='{self.masterid}', master.scix_id='{self.scix_id}', master.doi='{self.doi}'".format(
            self=self
        )

    def toJSON(self):
        return {
            "masterid": self.masterid,
            "doi": self.doi,
            "journalid": self.journalid,
            "origin": self.origin,
            "crmetadata": self.crmetadata,
            "bibcode": self.bibcode,
            "scix_id": self.scix_id,
            "is_valid": self.is_valid,
            "doi_found": self.doi_found,
            "meta_found": self.meta_found,
            "notes": self.notes,
            "created": self.created,
            "updated": self.updated
        }


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
    created = Column(DateTime(timezone=True), default=get_date)
    updated = Column(DateTime(timezone=True), onupdate=get_date)

    def __repr__(self):
        return "summary.summaryid='{self.summaryid}', summary.complete_fraction='{self.complete_fraction}'".format(
            self=self
        )

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

class CompStatSetIDs(Base):
    __tablename__ = "setidents"

    setidentid = Column(Integer, primary_key=True, unique=True)
    bibstem = Column(String, nullable=True)
    issn = Column(JSON, nullable=True)
    journal = Column(String, nullable=True)
    crossrefid = Column(String, nullable=False)
    created = Column(DateTime(timezone=True), default=get_date)
    updated = Column(DateTime(timezone=True), onupdate=get_date)

    def __repr__(self):
        return "setidents.setidentid='{self.setidentid}', setidents.bibstem='{self.bibstem}', setidents.crossrefid='{self.crossrefid}'".format(
            self=self
        )


class CompStatHarvesterLog(Base):
    __tablename__ = "harvestlog"

    harvestid = Column(Integer, primary_key=True, unique=True)
    crossrefid = Column(String, nullable=False)
    recordcount = Column(Integer, nullable=False)
    lastharvest = Column(DateTime(timezone=True), default="2026-01-01 00:00:00")
    currentharvest = Column(DateTime(timezone=True), default=get_date)

    def __repr__(self):
        return "harvestlog.harvestid='{self.harvestid}', harvestlog.crossrefid='{self.crossrefid}', harvestlog.currentharvest='{self.currentharvest}'".format(
            self=self
        )

