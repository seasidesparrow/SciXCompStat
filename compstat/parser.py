import json
from ingestparser.parsers.crossref import CrossrefParser

def generate_simple_meta(idm_record):
    # idm_record is in ingest_data_model format
    simple_record = {}
    if idm_record:
        all_authors = idm_record.get("authors", [])
        title = idm_record.get("title", [])
        subtitle = idm_record.get("subtitle", [])
        publication = idm_record.get("publication", [])
        persistent_ids = idm_record.get("persistentIDs", [])
        pubdates = idm_record.get("pubDate", [])
        pagination = idm_record.get("pagination", None)

        if all_authors:
            simple_record["first_author"] = all_authors[0]

        if persistent_ids:
            for pid in persistent_ids:
                if pid.get("DOI", None):
                    simple_record["doi"] = pid.get("DOI", None)

        if title:
            simple_record["title"] = title.get("textEnglish", None)
        if subtitle:
            simple_record["subtitle"] = subtitle.get("textEnglish", None)

        if publication:
            simple_record["publication"] = publication.get("pubName", None)
            simple_record["issue"] = publication.get("issueNum", None)
            simple_record["volume"] = publication.get("volumeNum", None)
            simple_record["issn"] = publication.get("ISSN", None)

        if pagination:
            simple_record["pagination"] = pagination

        return simple_record
        
    else:
        raise EmptyRecordException("Null record passed to meta simplifier!")



def parse_record_to_simple_meta(record):
    # record is a harvested crossref metadata xml from Harvester
    if record:
        try:
            parser = CrossrefParser()
            output = parser.parse(record)
            return generate_simple_meta(output)
        except Exception as err:
            raise FailedParsingException("Failed to generate metadata: %s" % err)
    else:
        raise EmptyRecordException("Null record passed to the parser!")
