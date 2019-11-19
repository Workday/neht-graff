from neo4j import GraphDatabase, basic_auth
from datetime import datetime

from config import *

# Build a connection to the DB
driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_CREDS[0], NEO4J_CREDS[1]))


# TODO modify the headers on the log data to not have . on the id sections

def upload_files(path="file:///files.csv"):
    """
    bulk upload the data into the data base
    :param path: either file path on local server (neo4j upload point) or url to data
    :return: none
    """
    cypher_query = "USING PERIODIC COMMIT\n"
    cypher_query += "LOAD CSV WITH HEADERS FROM '" + path + "' AS row WITH row \n"
    cypher_query += "MERGE (c:File{fuid: row.fuid})\n" \
                    "ON CREATE SET\n" \
                    "\tc.ts = row.ts,\n" \
                    "\tc.fuid = row.fuid,\n" \
                    "\tc.tx_hosts = row.tx_hosts,\n" \
                    "\tc.rx_hosts = row.rx_hosts,\n" \
                    "\tc.conn_uids = row.conn_uids,\n" \
                    "\tc.depth = row.depth,\n" \
                    "\tc.analyzers = row.analyzers,\n" \
                    "\tc.mime_type = row.mime_type,\n" \
                    "\tc.filename = row.filename,\n" \
                    "\tc.duration = row.duration,\n" \
                    "\tc.local_orig = row.local_orig,\n" \
                    "\tc.is_orig = row.is_orig,\n" \
                    "\tc.seen_bytes = row.seen_bytes,\n" \
                    "\tc.total_bytes = row.total_bytes,\n" \
                    "\tc.missing_bytes = row.missing_bytes,\n" \
                    "\tc.overflow_bytes = row.overflow_bytes,\n" \
                    "\tc.timedout = row.timedout,\n" \
                    "\tc.md5_sha1_sha256 = row.md5_sha1_sha256,\n" \
                    "\tc.extracted = row.extracted\n" \


    """
    "ts", "fuid", "tx_hosts", "rx_hosts", "conn_uids", "source", "depth", "analyzers", "mime_type",
                  "filename", "duration", "local_orig", "is_orig", "seen_bytes", "total_bytes", "missing_bytes",
                  "overflow_bytes", "timedout", "parent_fuid", "md5/sha1/sha256", "extracted"
    """

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


if __name__ == "__main__":
    start = datetime.now()
    upload_files()
    driver.close()
    print("time taken: ", end="")
    print(datetime.now() - start)
