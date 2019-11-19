from neo4j import GraphDatabase, basic_auth
from datetime import datetime

from config import *

# Build a connection to the DB
driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_CREDS[0], NEO4J_CREDS[1]))


# TODO modify the headers on the log data to not have . on the id sections

def upload_weird(path="file:///weird.csv"):
    """
    bulk upload the data into the data base
    :param path: either file path on local server (neo4j upload point) or url to data
    :return: none
    """
    cypher_query = "USING PERIODIC COMMIT\n"
    cypher_query += "LOAD CSV WITH HEADERS FROM '" + path + "' AS row WITH row \n"
    cypher_query += "MERGE (c:Weird{uid: row.uid})\n" \
                    "ON CREATE SET\n" \
                    "\tc.ts = row.ts,\n" \
                    "\tc.uid = row.uid,\n" \
                    "\tc.id_orig_h = row.id_orig_h,\n" \
                    "\tc.id_orig_p = row.id_orig_p,\n" \
                    "\tc.id_resp_h = row.id_resp_h,\n" \
                    "\tc.id_resp_p = row.id_resp_p,\n" \
                    "\tc.name = row.name,\n" \
                    "\tc.addl = row.addl,\n" \
                    "\tc.notice = row.notice,\n" \
                    "\tc.peer = row.peer\n" \

    """
         "ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "name", "addl", "notice", "peer"
    """

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


if __name__ == "__main__":
    start = datetime.now()
    upload_weird()
    driver.close()
    print("time taken: ", end="")
    print(datetime.now() - start)
