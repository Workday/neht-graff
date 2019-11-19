from neo4j import GraphDatabase, basic_auth
from datetime import datetime

from config import *

# Build a connection to the DB
driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_CREDS[0], NEO4J_CREDS[1]))


def create_host_constraints():
    """
    Make sure the host IP address is unique in the data base (may need to change this to the domain name, but not
    all hosts have a domain name
    :return:
    """
    cypher_query = "CREATE CONSTRAINT ON (n:Host) ASSERT n.address IS UNIQUE;"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


def create_conn_constraints():
    """
    build constraints in the neo4j data base
    :return: none
    """
    # Make sure connection IDs are unique in the data base
    cypher_query = "CREATE CONSTRAINT ON (c:Conn) ASSERT c.uid IS UNIQUE;"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


def create_dns_constraints():
    """
    build constriints in the neo4j data base
    :return: none
    """
    cypher_query = "CREATE CONSTRAINT ON (d:DNS) ASSERT d.uid IS UNIQUE;"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


def create_file_constraints():
    """
    build constriints in the neo4j data base
    :return: none
    """
    cypher_query = "CREATE CONSTRAINT ON (f:File) ASSERT f.fuid IS UNIQUE;"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


def create_ftp_constraints():
    """
    build constriints in the neo4j data base
    :return: none
    """
    cypher_query = "CREATE CONSTRAINT ON (f:FTP) ASSERT f.uid IS UNIQUE;"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


def create_smtp_constraints():
    """
    build constriints in the neo4j data base
    :return: none
    """
    cypher_query = "CREATE CONSTRAINT ON (s:SMTP) ASSERT s.uid IS UNIQUE;"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)

def create_http_constraints():
    """
    build constriints in the neo4j data base
    :return: none
    """
    cypher_query = "CREATE CONSTRAINT ON (h:HTTP) ASSERT h.uid IS UNIQUE;"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)

def create_weird_constraints():
    """
    build constriints in the neo4j data base
    :return: none
    """
    cypher_query = "CREATE CONSTRAINT ON (w:Weird) ASSERT w.uid IS UNIQUE;"

    print(cypher_query)

    with driver.session() as session:
        session.run(cypher_query)


if __name__ == "__main__":
    start = datetime.now()
    create_host_constraints()
    create_conn_constraints()
    # create_dns_constraints() not needed according to my data set there can be many of these
    create_ftp_constraints()
    create_smtp_constraints()
    create_http_constraints()
    create_weird_constraints()
    driver.close()
    print("time taken: ", end="")
    print(datetime.now() - start)
