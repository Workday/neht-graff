from neo4j import GraphDatabase, basic_auth
from datetime import datetime

from config import *

# Build a connection to the DB
driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_CREDS[0], NEO4J_CREDS[1]))


# TODO modify the headers on the log data to not have . on the id sections

def upload_smtp(path="file:///smtp.csv"):
    """
    bulk upload the data into the data base
    :param path: either file path on local server (neo4j upload point) or url to data
    :return: none
    """
    cypher_query = "USING PERIODIC COMMIT\n"
    cypher_query += "LOAD CSV WITH HEADERS FROM '" + path + "' AS row WITH row \n"
    cypher_query += "MERGE (c:SMTP{uid: row.uid})\n" \
                    "ON CREATE SET\n" \
                    "\tc.ts = row.ts,\n" \
                    "\tc.uid = row.uid,\n" \
                    "\tc.id_orig_h = row.id_orig_h,\n" \
                    "\tc.id_orig_p = row.id_orig_p,\n" \
                    "\tc.id_resp_h = row.id_resp_h,\n" \
                    "\tc.id_resp_p = row.id_resp_p,\n" \
                    "\tc.proto = row.proto,\n" \
                    "\tc.trans_depth = row.trans_depth,\n" \
                    "\tc.helo = row.helo,\n" \
                    "\tc.mailfrom = row.mailfrom,\n" \
                    "\tc.rcptto = row.rcptto,\n" \
                    "\tc.from = row.from,\n" \
                    "\tc.to = row.to,\n" \
                    "\tc.in_reply_to = row.in_reply_to,\n" \
                    "\tc.subject = row.subject,\n" \
                    "\tc.x_originating_ip = row.x_originating_ip,\n" \
                    "\tc.first_received = row.first_received,\n" \
                    "\tc.second_received = row.second_received,\n" \
                    "\tc.last_reply = row.last_reply,\n" \
                    "\tc.path = row.path,\n" \
                    "\tc.user_agent = row.user_agent,\n" \
                    "\tc.fuids = row.fuids,\n" \
                    "\tc.is_webmail = row.is_webmail\n" \


    """
         "ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "proto", "trans_depth", "helo",
                 "mailfrom", "rcptto", "date", "from", "to", "in_reply_to", "subject", "x_originating_ip",
                 "first_received", "second_received", "last_reply", "path", "user_agent", "tls", "fuids",
                 "is_webmail"
    """

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


if __name__ == "__main__":
    start = datetime.now()
    upload_smtp()
    driver.close()
    print("time taken: ", end="")
    print(datetime.now() - start)
