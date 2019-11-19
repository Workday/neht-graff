from neo4j import GraphDatabase, basic_auth
from datetime import datetime

from config import *

# Build a connection to the DB
driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_CREDS[0], NEO4J_CREDS[1]))


# TODO modify the headers on the log data to not have . on the id sections

def upload_http(path="file:///http.csv"):
    """
    bulk upload the data into the data base
    :param path: either file path on local server (neo4j upload point) or url to data
    :return: none
    """
    cypher_query = "USING PERIODIC COMMIT\n"
    cypher_query += "LOAD CSV WITH HEADERS FROM '" + path + "' AS row WITH row \n"
    cypher_query += "MERGE (c:HTTP{uid: row.uid})\n" \
                    "ON CREATE SET\n" \
                    "\tc.ts = row.ts,\n" \
                    "\tc.uid = row.uid,\n" \
                    "\tc.id_orig_h = row.id_orig_h,\n" \
                    "\tc.id_orig_p = row.id_orig_p,\n" \
                    "\tc.id_resp_h = row.id_resp_h,\n" \
                    "\tc.id_resp_p = row.id_resp_p,\n" \
                    "\tc.trans_depth = row.trans_depth,\n" \
                    "\tc.method = row.method,\n" \
                    "\tc.host = row.host,\n" \
                    "\tc.uri = row.uri,\n" \
                    "\tc.referrer = row.referrer,\n" \
                    "\tc.user_agent = row.user_agent,\n" \
                    "\tc.request_body_len = row.request_body_len,\n" \
                    "\tc.response_body_len = row.response_body_len,\n" \
                    "\tc.status_code = row.status_code,\n" \
                    "\tc.status_msg = row.status_msg,\n" \
                    "\tc.info_code = row.info_code,\n" \
                    "\tc.info_msg = row.info_msg,\n" \
                    "\tc.filename = row.filename,\n" \
                    "\tc.tags = row.tags,\n" \
                    "\tc.username = row.username,\n" \
                    "\tc.password = row.password,\n" \
                    "\tc.proxied = row.proxied,\n" \
                    "\tc.orig_fuids = row.orig_fuids,\n" \
                    "\tc.orig_mime_types = row.orig_mime_types,\n" \
                    "\tc.resp_fuids = row.resp_fuids,\n" \
                    "\tc.resp_mime_types = row.resp_mime_types\n" \


    """
         "ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "trans_depth", "method", "host",
                 "uri", "referrer", "user_agent", "request_ body_len", "response_ body_len", "status_code",
                 "status_msg", "info_code", "info_msg", "filename", "tags", "username", "password", "proxied",
                 "orig_fuids", "orig_mime_types", "resp_fuids", "resp_mime_types"
    """

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


if __name__ == "__main__":
    start = datetime.now()
    upload_http()
    driver.close()
    print("time taken: ", end="")
    print(datetime.now() - start)
