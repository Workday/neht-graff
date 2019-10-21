from bat.log_to_dataframe import LogToDataFrame
from neo4j import GraphDatabase, basic_auth

from config import *

# Build a connection to the DB
driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_CREDS[0], NEO4J_CREDS[1]))

# Read the conn.log file into a data frame
conn = LogToDataFrame('your/path')  # Log path

# Read the dns.log file into a data frame
dns = LogToDataFrame('your/path')  # Log path

# Read the files.log
files = LogToDataFrame('your/path')  # Log path

# TODO update imports to be taken from the configuration file


def construct_files_query(index, zeek_line):
    query = "MERGE(host_o: Host{{address: \"{tx_hosts}\"}})\n\n" \
            "MERGE(host_r: Host{{address: \"{rx_hosts}\"}})\n\n" \
            "MERGE (file:File  {{\n" \
            "\tfuid: \"{fuid}\",\n" \
            "\tuid: \"{conn_uids}\",\n" \
            "\tts: \"{ts}\",\n" \
            "\tsource: \"{source}\",\n" \
            "\tdepth: \"{depth}\",\n" \
            "\tanalyzers: \"{analyzers}\",\n" \
            "\tmime_type: \"{mime_type}\",\n" \
            "\tfilename: \"{filename}\",\n" \
            "\tduration: \"{duration}\",\n" \
            "\tlocal_orig: \"{local_orig}\",\n" \
            "\tis_orig: \"{is_orig}\",\n" \
            "\tseen_bytes: \"{seen_bytes}\",\n" \
            "\ttotal_bytes: \"{total_bytes}\",\n" \
            "\tmissing_bytes: \"{missing_bytes}\",\n" \
            "\toverflow_bytes: \"{overflow_bytes}\",\n" \
            "\ttimedout: \"{timedout}\",\n" \
            "\tparent_fuid: \"{parent_fuid}\",\n" \
            "\tmd5: \"{md5}\",\n" \
            "\tsha1: \"{sha1}\",\n" \
            "\tsha256: \"{sha256}\",\n" \
            "\textracted: \"{extracted}\",\n" \
            "\textracted_cutoff: \"{extracted_cutoff}\",\n" \
            "\textracted_size: \"{extracted_size}\" }})\n\n" \
            "CREATE (host_o)-[:ORIG]->(file)<-[:RESP]-(host_r)"

    query = query.format(tx_hosts=zeek_line['tx_hosts'],
                         rx_hosts=zeek_line['rx_hosts'],
                         fuid=zeek_line['fuid'],
                         conn_uids=zeek_line['conn_uids'],
                         ts=index,
                         source=zeek_line['source'],
                         depth=zeek_line['depth'],
                         analyzers=zeek_line['analyzers'],
                         mime_type=zeek_line['mime_type'],
                         filename=zeek_line['filename'],
                         duration=zeek_line['duration'],
                         local_orig=zeek_line['local_orig'],
                         is_orig=zeek_line['is_orig'],
                         seen_bytes=zeek_line['seen_bytes'],
                         total_bytes=zeek_line['total_bytes'],
                         missing_bytes=zeek_line['missing_bytes'],
                         overflow_bytes=zeek_line['overflow_bytes'],
                         timedout=zeek_line['timedout'],
                         parent_fuid=zeek_line['parent_fuid'],
                         md5=zeek_line['md5'],
                         sha1=zeek_line['sha1'],
                         sha256=zeek_line['sha256'],
                         extracted=zeek_line['extracted'],
                         extracted_cutoff=zeek_line['extracted_cutoff'],
                         extracted_size=zeek_line['extracted_size'],
                         )
    return query


def construct_dns_query(index, zeek_line):
    query = "MERGE(host_o: Host{{address: \"{id_orig_h}\"}})\n\n" \
            "MERGE(host_r: Host{{address: \"{id_resp_h}\"}})\n\n" \
            "MERGE (dns:DNS  {{\n" \
            "\tuid: \"{uid}\",\n" \
            "\tts: \"{ts}\",\n" \
            "\tsport: \"{id_orig_p}\",\n" \
            "\tdport: \"{id_resp_p}\",\n" \
            "\tproto: \"{proto}\",\n" \
            "\ttrans_id: \"{trans_id}\",\n" \
            "\trtt: \"{rtt}\",\n" \
            "\tquery: \"{query}\",\n" \
            "\tqclass_name: \"{qclass_name}\",\n" \
            "\tqtype_name: \"{qtype_name}\",\n" \
            "\trcode: \"{rcode}\",\n" \
            "\trcode_name: \"{rcode_name}\",\n" \
            "\taa: \"{aa}\",\n" \
            "\ttc: \"{tc}\",\n" \
            "\trd: \"{rd}\",\n" \
            "\tra: \"{ra}\",\n" \
            "\tz: \"{z}\",\n" \
            "\tanswers: \"{answers}\",\n" \
            "\tttls: \"{ttls}\",\n" \
            "\trejected: \"{rejected}\" }})\n\n" \
            "CREATE (host_o)-[:ORIG]->(dns)<-[:RESP]-(host_r)"

    query = query.format(id_orig_h=zeek_line['id.orig_h'],
                         id_resp_h=zeek_line['id.resp_h'],
                         uid=zeek_line['uid'],
                         ts=index,
                         id_orig_p=zeek_line['id.orig_p'],
                         id_resp_p=zeek_line['id.resp_p'],
                         proto=zeek_line['proto'],
                         trans_id=zeek_line['trans_id'],
                         rtt=zeek_line['rtt'],
                         query=zeek_line['query'],
                         qclass=zeek_line['qclass'],
                         qclass_name=zeek_line['qclass_name'],
                         qtype=zeek_line['qtype'],
                         qtype_name=zeek_line['qtype_name'],
                         rcode=zeek_line['rcode'],
                         rcode_name=zeek_line['rcode_name'],
                         aa=zeek_line['AA'],
                         tc=zeek_line['TC'],
                         rd=zeek_line['RD'],
                         ra=zeek_line['RA'],
                         z=zeek_line['Z'],
                         answers=zeek_line['answers'],
                         ttls=zeek_line['TTLs'],
                         rejected=zeek_line['rejected'])
    return query


def construct_conn_query(index, zeek_line):
    query = "MERGE(host_o: Host{{address: \"{id_orig_h}\"}})\n\n" \
            "MERGE(host_r: Host{{address: \"{id_resp_h}\"}})\n\n" \
            "MERGE (conn:Connection  {{\n" \
            "\tuid: \"{uid}\",\n" \
            "\tsport: \"{id_orig_p}\",\n" \
            "\tts: \"{ts}\",\n" \
            "\tdport: \"{id_resp_p}\",\n" \
            "\tproto: \"{proto}\",\n" \
            "\tservice: \"{service}\",\n" \
            "\tdur: \"{duration}\",\n" \
            "\tconn_state: \"{conn_state}\",\n" \
            "\ttunnel_parents: \"{tunnel_parents}\",\n" \
            "\tvlan: \"{vlan}\",\n" \
            "\tinner_vlan: \"{inner_vlan}\",\n" \
            "\torig_l2_addr: \"{orig_l2_addr}\",\n" \
            "\tresp_l2_addr: \"{resp_l2_addr}\",\n" \
            "\tlocal_orig: \"{local_orig}\",\n" \
            "\tmissed_bytes: \"{missed_bytes}\",\n" \
            "\thistory: \"{history}\",\n" \
            "\torig_pkts: \"{orig_pkts}\",\n" \
            "\tresp_pkts: \"{resp_pkts}\",\n" \
            "\torig_ip_bytes: \"{orig_ip_bytes}\",\n" \
            "\tresp_ip_bytes: \"{resp_ip_bytes}\",\n" \
            "\torig_bytes: \"{orig_bytes}\",\n" \
            "\tresp_bytes: \"{resp_bytes}\" }})\n\n" \
            "CREATE (host_o)-[:ORIG]->(conn)<-[:RESP]-(host_r)"

    query = query.format(id_orig_h=zeek_line['id.orig_h'],
                         id_resp_h=zeek_line['id.resp_h'],
                         uid=zeek_line['uid'],
                         ts=index,
                         id_orig_p=zeek_line['id.orig_p'],
                         id_resp_p=zeek_line['id.resp_p'],
                         proto=zeek_line['proto'],
                         service=zeek_line['service'],
                         duration=zeek_line['duration'],
                         conn_state=zeek_line['conn_state'],
                         tunnel_parents=zeek_line['tunnel_parents'],
                         vlan=zeek_line['vlan'],
                         inner_vlan=zeek_line['inner_vlan'],
                         orig_l2_addr=zeek_line['orig_l2_addr'],
                         resp_l2_addr=zeek_line['resp_l2_addr'],
                         local_orig=zeek_line['local_orig'],
                         missed_bytes=zeek_line['missed_bytes'],
                         history=zeek_line['history'],
                         orig_pkts=zeek_line['orig_pkts'],
                         resp_pkts=zeek_line['resp_pkts'],
                         orig_ip_bytes=zeek_line['orig_ip_bytes'],
                         resp_ip_bytes=zeek_line['resp_ip_bytes'],
                         orig_bytes=zeek_line['orig_ip_bytes'],
                         resp_bytes=zeek_line['resp_ip_bytes'])

    return query


def create_constraint(node_label="Host", node_attribute="address"):
    query = "CREATE CONSTRAINT ON (n:{label}) ASSERT n.{property} IS UNIQUE;"
    query = query.format(label=node_label, property=node_attribute)

    with driver.session() as session:
        session.run(query)

    print("Created IP Constraint")


def upload_conn():
    print("Data Frame Dimensions: Conn")
    print(conn.shape)
    print(conn.size)
    print(conn.columns)

    for index, row in conn.iterrows():
        with driver.session() as session:
            session.run(construct_conn_query(index, row))

    print("Uploaded Conn Log")


def upload_dns():
    print("Data Frame Dimensions: DNS")
    print(dns.shape)
    print(dns.size)
    print(dns.columns)

    for index, row in dns.iterrows():
        with driver.session() as session:
            session.run(construct_dns_query(index, row))

    print("Uploaded DNS Log")


def upload_files():
    print("Data Frame Dimensions: Files")
    print(files.shape)
    print(files.size)
    print(files.columns)

    for index, row in files.iterrows():
        with driver.session() as session:
            session.run(construct_files_query(index, row))

    print("Uploaded Files")


def clean():
    driver.close()


if __name__ == "__main__":
    upload_conn()
    clean()
