from neo4j import GraphDatabase, basic_auth
from datetime import datetime
from config import *

# Build a connection to the DB
driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_CREDS[0], NEO4J_CREDS[1]))


# TODO modify the headers on the log data to not have . on the id sections


def create_conn_relationships():
    """
    build the relationships in the data base
    :return: none
    # TODO test if these queries can be crammed into one and if the improves performance
    """
    cypher_query = "match (n:Conn), (h:Host) where h.address = n.id_orig_h\n" \
                   "merge (h)<-[r:ORIG]-(n)\n"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)

    cypher_query = "match (n:Conn), (h:Host) where h.address = n.id_resp_h\n" \
                   "merge (h)<-[r:DEST]-(n)\n"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


def create_dns_relationships():
    """
    build the relationships in the data base
    :return: none
    # TODO test if these queries can be crammed into one and if the improves performance
    """
    cypher_query = "match (n:DNS), (h:Host) where h.address = n.id_orig_h\n" \
                   "merge (h)<-[r:REQUEST]-(n)\n"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)

    cypher_query = "match (n:DNS), (h:Host) where h.address = n.id_resp_h\n" \
                   "merge (h)<-[r:ANSWER]-(n)\n"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


def create_ftp_relationships():
    """
    build the relationships in the data base
    :return: none
    # TODO test if these queries can be crammed into one and if the improves performance
    """
    cypher_query = "match (n:FTP), (h:Host) where h.address = n.id_orig_h\n" \
                   "merge (h)<-[r:SENT]-(n)\n"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)

    cypher_query = "match (n:FTP), (h:Host) where h.address = n.id_resp_h\n" \
                   "merge (h)<-[r:RECEIVED]-(n)\n"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


def create_smtp_relationships():
    """
    build the relationships in the data base
    :return: none
    # TODO test if these queries can be crammed into one and if the improves performance
    """
    cypher_query = "match (n:SMTP), (h:Host) where h.address = n.id_orig_h\n" \
                   "merge (h)<-[r:SENT_MAIL]-(n)\n"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)

    cypher_query = "match (n:SMTP), (h:Host) where h.address = n.id_resp_h\n" \
                   "merge (h)<-[r:RECEIVED_MAIL]-(n)\n"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


def create_http_relationships():
    """
    build the relationships in the data base
    :return: none
    # TODO test if these queries can be crammed into one and if the improves performance
    """
    cypher_query = "match (n:HTTP), (h:Host) where h.address = n.id_orig_h\n" \
                   "merge (h)<-[r:REQUEST]-(n)\n"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)

    cypher_query = "match (n:HTTP), (h:Host) where h.address = n.id_resp_h\n" \
                   "merge (h)<-[r:PROVIDED]-(n)\n"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


def create_direct_conns():
    cypher_query = "match (n:Host)-[:ORIG]-(c:Conn)-[:DEST]-(b:Host) where c.id_orig_h = n.address " \
                   "and c.id_resp_h = b.address " \
                   "and not n.address = b.address\n" \
                   "merge (n)-[r:SPOKE]->(b)\n"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


def create_weird_conns():
    cypher_query = "match (n:Weird), (h:Host) where h.address = n.id_orig_h\n" \
                   "merge (h)<-[r:WEIRD_ORIG]-(n)\n"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)

    cypher_query = "match (n:Weird), (h:Host) where h.address = n.id_resp_h\n" \
                   "merge (h)<-[r:WEIRD_DEST]-(n)\n"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


if __name__ == "__main__":
    start = datetime.now()
    create_conn_relationships()
    create_dns_relationships()
    create_ftp_relationships()
    create_http_relationships()
    create_smtp_relationships()
    create_weird_conns()
    create_direct_conns()
    driver.close()
    print("time taken: ", end="")
    print(datetime.now() - start)
