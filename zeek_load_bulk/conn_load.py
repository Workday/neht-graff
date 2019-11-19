from neo4j import GraphDatabase, basic_auth
from datetime import datetime

from config import *

# Build a connection to the DB
driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_CREDS[0], NEO4J_CREDS[1]))


# TODO modify the headers on the log data to not have . on the id sections

def upload_conn(path="file:///conn.csv"):
    """
    bulk upload the data into the data base
    :param path: either file path on local server (neo4j upload point) or url to data
    :return: none
    """
    cypher_query = "USING PERIODIC COMMIT\n"

    cypher_query += "LOAD CSV WITH HEADERS FROM '" + path + "' AS row WITH row \n"
    cypher_query += "MERGE (c:Conn{uid: row.uid})\n" \
                    "ON CREATE SET\n" \
                    "\tc.ts = row.ts,\n" \
                    "\tc.uid = row.uid,\n" \
                    "\tc.id_orig_h = row.id_orig_h,\n" \
                    "\tc.id_orig_p = row.id_orig_p,\n" \
                    "\tc.id_resp_h = row.id_resp_h,\n" \
                    "\tc.id_resp_p = row.id_resp_p,\n" \
                    "\tc.proto = row.proto,\n" \
                    "\tc.service = row.service,\n" \
                    "\tc.duration = row.duration,\n" \
                    "\tc.orig_bytes = row.orig_bytes,\n" \
                    "\tc.resp_bytes = row.resp_bytes,\n" \
                    "\tc.conn_state = row.conn_state,\n" \
                    "\tc.local_orig = row.local_orig,\n" \
                    "\tc.local_resp = row.local_resp,\n" \
                    "\tc.missed_bytes = row.missed_bytes,\n" \
                    "\tc.history = row.history,\n" \
                    "\tc.orig_pkts = row.orig_pkts,\n" \
                    "\tc.orig_ip_bytes = row.orig_ip_bytes,\n" \
                    "\tc.resp_pkts = row.resp_pkts,\n" \
                    "\tc.resp_ip_bytes = row.resp_ip_bytes,\n" \
                    "\tc.tunnel_parents = row.tunnel_parents\n"

    print(cypher_query)

    """
          We have room for thought here on this. Above is the general query to upload a row of zeek conn
          as whole entire node in a graph. However i made a design choice with below to increase fidelity of the 
          graph to include host IP address. 
    """

    with driver.session() as session:
        session.run(cypher_query)


def create_hosts(path="file:///conn.csv"):
    cypher_query = ""  # empty the query since we are executing in chunks

    # Query for loading the source nodes
    cypher_query += "LOAD CSV WITH HEADERS FROM '" + path + "' AS row WITH row \n" \
                                                            "MERGE (h:Host{address: row.id_orig_h})\n"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)

    cypher_query = ""  # empty the query since we are executing in chunks

    # Query for loading the dest nodes
    cypher_query += "LOAD CSV WITH HEADERS FROM '" + path + "' AS row WITH row \n" \
                                                            "MERGE (h:Host{address: row.id_resp_h})\n"
    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)

    # One should close their sockets to make sure they dont leave ports floating around


if __name__ == "__main__":
    start = datetime.now()
    upload_conn()
    print("time taken: ", end="")
    print(datetime.now() - start)

    start = datetime.now()
    create_hosts()
    driver.close()
    print("time taken: ", end="")
    print(datetime.now() - start)
