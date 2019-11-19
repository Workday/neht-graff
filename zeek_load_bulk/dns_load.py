from neo4j import GraphDatabase, basic_auth
from datetime import datetime

from config import *

# Build a connection to the DB
driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_CREDS[0], NEO4J_CREDS[1]))


# TODO modify the headers on the log data to not have . on the id sections

def upload_dns(path="file:///dns.csv"):
    """
    bulk upload the data into the data base
    :param path: either file path on local server (neo4j upload point) or url to data
    :return: none
    """
    cypher_query = "USING PERIODIC COMMIT\n"
    cypher_query += "LOAD CSV WITH HEADERS FROM '" + path + "' AS row WITH row \n"
    cypher_query += "CREATE (:DNS {\n" \
                    "\tts: row.ts,\n" \
                    "\tuid: row.uid,\n" \
                    "\tid_orig_h: row.id_orig_h,\n" \
                    "\tid_orig_p: row.id_orig_p,\n" \
                    "\tid_resp_h: row.id_resp_h,\n" \
                    "\tid_resp_p: row.id_resp_p,\n" \
                    "\tproto: row.proto,\n" \
                    "\tport: row.port,\n" \
                    "\tquery: row.query,\n" \
                    "\tqclass: row.qclass,\n" \
                    "\tqclass_name: row.qclass_name,\n" \
                    "\tqtype: row.qtype,\n" \
                    "\tqtype_name: row.qtype_name,\n" \
                    "\trcode: row.rcode,\n" \
                    "\trcode_name: row.rcode_name,\n" \
                    "\tqr: row.qr,\n" \
                    "\taa: row.aa,\n" \
                    "\ttc: row.tc,\n" \
                    "\trd: row.rd,\n" \
                    "\tz: row.z,\n" \
                    "\tanswers: row.answers,\n"\
                    "\tttls: row.ttls,\n"\
                    "\trejected: row.rejected})\n"\


    """
    "ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "proto", "port", "query", "qclass",
                "qclass_name", "qtype", "qtype_name", "rcode", "rcode_name", "QR", "AA", "TC", "RD", "Z", "answers",
                "TTLs", "rejected"
    """

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


if __name__ == "__main__":
    start = datetime.now()
    upload_dns()
    driver.close()
    print("time taken: ", end="")
    print(datetime.now() - start)
