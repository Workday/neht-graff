from neo4j import GraphDatabase, basic_auth
from datetime import datetime

from config import *

# Build a connection to the DB
driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_CREDS[0], NEO4J_CREDS[1]))


# TODO modify the headers on the log data to not have . on the id sections

def upload_ftp(path="file:///ftp.csv"):
    """
    bulk upload the data into the data base
    :param path: either file path on local server (neo4j upload point) or url to data
    :return: none
    """
    cypher_query = "USING PERIODIC COMMIT\n"
    cypher_query += "LOAD CSV WITH HEADERS FROM '" + path + "' AS row WITH row \n"
    cypher_query += "MERGE (c:FTP{uid: row.uid})\n" \
                    "ON CREATE SET\n" \
                    "\tc.ts = row.ts,\n" \
                    "\tc.fuid = row.fuid,\n" \
                    "\tc.id_orig_h = row.id_orig_h,\n" \
                    "\tc.id_orig_p = row.id_orig_p,\n" \
                    "\tc.id_resp_h = row.id_resp_h,\n" \
                    "\tc.id_resp_p = row.id_resp_p,\n" \
                    "\tc.user = row.user,\n" \
                    "\tc.password = row.password,\n" \
                    "\tc.command = row.command,\n" \
                    "\tc.arg = row.arg,\n" \
                    "\tc.mime_type = row.mime_type,\n" \
                    "\tc.file_size = row.file_size,\n" \
                    "\tc.reply_code = row.reply_code,\n" \
                    "\tc.reply_msg = row.reply_msg,\n" \
                    "\tc.passive = row.passive,\n" \
                    "\tc.orig_h = row.orig_h,\n" \
                    "\tc.resp_h = row.resp_h,\n" \
                    "\tc.resp_p = row.resp_p,\n" \
                    "\tc.fuid = row.fuid\n" \


    """
   "ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "user", "password", "command",
                "arg", "mime_type", "file_size", "reply_code", "reply_msg", "passive", "orig_h", "resp_h", "resp_p",
                "fuid"
    """

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


if __name__ == "__main__":
    start = datetime.now()
    upload_ftp()
    driver.close()
    print("time taken: ", end="")
    print(datetime.now() - start)
