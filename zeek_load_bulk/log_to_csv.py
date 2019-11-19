import csv
from datetime import datetime

zeek_dict = {
    "dhcp.log": ["ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "mac", "assigned_ip", "lease_time",
                 "trans_id"],
    "dns.log": ["ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "proto", "port", "query", "qclass",
                "qclass_name", "qtype", "qtype_name", "rcode", "rcode_name", "QR", "AA", "TC", "RD", "Z", "answers",
                "TTLs", "rejected"],
    "ftp.log": ["ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "user", "password", "command",
                "arg", "mime_type", "file_size", "reply_code", "reply_msg", "passive", "orig_h", "resp_h", "resp_p",
                "fuid"],
    "ssh.log": ["ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "status", "direction", "client",
                "server", "resp_size"],
    "files.log": ["ts", "fuid", "tx_hosts", "rx_hosts", "conn_uids", "source", "depth", "analyzers", "mime_type",
                  "filename", "duration", "local_orig", "is_orig", "seen_bytes", "total_bytes", "missing_bytes",
                  "overflow_bytes", "timedout", "parent_fuid", "md5_sha1_sha256", "extracted"],
    "http.log": ["ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "trans_depth", "method", "host",
                 "uri", "referrer", "user_agent", "request_ body_len", "response_ body_len", "status_code",
                 "status_msg", "info_code", "info_msg", "filename", "tags", "username", "password", "proxied",
                 "orig_fuids", "orig_mime_types", "resp_fuids", "resp_mime_types"],
    "notice.log": ["ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "fuid", "file_mime_type",
                   "file_desc", "proto", "note", "msg", "sub", "src", "dst", "p", "n", "peer_descr", "actions",
                   "suppress_for", "dropped"],
    "smtp.log": ["ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "proto", "trans_depth", "helo",
                 "mailfrom", "rcptto", "date", "from", "to", "in_reply_to", "subject", "x_originating_ip",
                 "first_received", "second_received", "last_reply", "path", "user_agent", "tls", "fuids",
                 "is_webmail"],
    "ssl.log": ["ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "version", "cipher", "server_name",
                "session_id", "subject", "issuer_subject", "not_valid_before", "not_valid_after", "last_alert",
                "client_subject", "clnt_issuer_subject", "cer_hash", "validation_status"],
    "tunnel.log": ["ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "tunnel_type", "action"],
    "weird.log": ["ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "name", "addl", "notice", "peer"],
    "conn.log": ["ts", "uid", "id_orig_h", "id_orig_p", "id_resp_h", "id_resp_p", "proto", "service", "duration",
                 "orig_bytes", "resp_bytes", "conn_state", "local_orig", "local_resp", "missed_bytes", "history",
                 "orig_pkts", "orig_ip_bytes", "resp_pkts", "resp_ip_bytes", "tunnel_parents"]}


def zeek_to_csv(file_in_path, file_out_path, log_type):
    # TODO make this have error aware input
    # Create a log file into a csv file so we can manipulate it with pandas
    out = file_out_path + "/" + log_type + '.csv'
    print("SAVING TO: " + out)

    with open(out, 'w+', encoding='utf-8') as csv_file:
        w = csv.writer(csv_file, dialect='excel')
        with open(file_in_path, encoding="utf8") as file:
            lines = file.read().split('\n')

            # print("Adding Header for type: " + log_type + ".log")
            files = [zeek_dict[log_type + ".log"]]

            for line in lines:
                files.append(line.split('\t'))

            w.writerows(files)


if __name__ == "__main__":
    start = datetime.now()

    print("Starting conversion...")

    zeek_to_csv(file_in_path="/Users/max.hill/ghost/conn.log",
                file_out_path="/Users/max.hill/ghost/csv",
                log_type="conn")
    print("done")

    zeek_to_csv(file_in_path="/Users/max.hill/ghost/dns.log",
                file_out_path="/Users/max.hill/ghost/csv",
                log_type="dns")
    print("done")

    zeek_to_csv(file_in_path="/Users/max.hill/ghost/ftp.log",
                file_out_path="/Users/max.hill/ghost/csv",
                log_type="ftp")

    print("done")

    zeek_to_csv(file_in_path="/Users/max.hill/ghost/smtp.log",
                file_out_path="/Users/max.hill/ghost/csv",
                log_type="smtp")
    print("done")

    zeek_to_csv(file_in_path="/Users/max.hill/ghost/weird.log",
                file_out_path="/Users/max.hill/ghost/csv",
                log_type="weird")
    print("done")
    zeek_to_csv(file_in_path="/Users/max.hill/ghost/http.log",
                file_out_path="/Users/max.hill/ghost/csv",
                log_type="http")

    print("time taken: ", end="")
    print(datetime.now() - start)
