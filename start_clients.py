import subprocess
import argparse
import time

cur_core = 0
nb_cores = 1
server = ""
offset = 0;
increment = 0

class client(object):
    def __init__(self, k, is_ssl, port_num, nb_requests, core, client_port):
        self.port_num    = port_num
	self.client_port = client_port

        self.args = ["taskset"]
        self.args.extend(["-c", str(core)])
        self.args.extend(["./ab"])
        if k:
            self.args.extend(["-k"])
        self.args.extend(["-D", str(client_port)])
        self.args.extend(["-n", str(nb_requests)])
        if is_ssl:
	    self.args.extend(["https://{}:{}/".format(server, port_num)])
        else:
            self.args.extend(["http://{}:{}/".format(server, port_num)])

        self.log_file_path, log_file = self.create_log()
        print self.args
        
        self.p = subprocess.Popen(self.args, stdout=log_file)
        log_file.close()

    def stop(self):
        while self.process.poll() is None:
            time.sleep(1)
        self.log_file_path.close()

    def create_log(self):
        file_path = "logs/ab_{}".format(self.client_port)
        f = open(file_path, "w+")
        f.write("ab arguments: {}\n\nSTDOUT:\n".format(str(self.args)))
        f.flush()
        return file_path, f

#    def parse_result(self):
#        with open(self.log_file_path, "r") as f:

#            for line in f:
#                if line.startswith("Requests per second:"):
#		    print line
#                    self.request_per_sec = line.split()[3].strip();
#                    print self.request_per_sec
#                    break

#        return self.request_per_sec

"""
def form_ab(
        k = True, 
        nb_requests = 1,
        core = 0
        ):
    args = ["taskset"]
    args.extend(["-c", str(core)])
    args.extend(["ab"])
    if k:
        args.extend(["-k"])
    args.extend(["-n", str(nb_requests)])
    print args
    return args
"""

def increment_core_num(core):
    global cur_core
    p = core + cur_core + offset
    cur_core = (cur_core + 1) % nb_cores
    return p

def start_clients(k, is_ssl, port_num, nb_requests, nb_clients, client_port):
    client_list=[]
    for _ in range(nb_clients):
        nc = increment_core_num(0)
        client_list.append(client(k, is_ssl, port_num, nb_requests, nc, client_port))
        if port_num > 0:
            port_num += increment
        if client_port > 0:
            client_port += 1
    return client_list

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", help="turn on Keep-Alive feature", action='store_true')
    parser.add_argument("-l", help="turn on ssl", action='store_true')
    parser.add_argument("-s", help="server ip address")
    parser.add_argument("--first_https_port", help="server https port number", type=int)
    parser.add_argument("--first_http_port", help="server http port number", type=int)
    parser.add_argument("--nb_clients", help="number of clients to create", type=int)
    parser.add_argument("--increment", help="the increment value of port", type=int)
    parser.add_argument("--nb_requests", help="number of requests to make", type=int)
    parser.add_argument("--nb_cores", help="number of cores", type=int)
    parser.add_argument("--first_client_port", help="client port num", type=int)
    return parser.parse_args()

if __name__ == '__main__':

    args = parse_args()
    server = args.s
    first_client_port = args.first_client_port if args.first_client_port else 11211
    first_https_port = args.first_https_port if args.first_https_port else 443
    first_http_port = args.first_http_port if args.first_http_port else 1500
    increment = args.increment if args.increment else 0
    k = args.k
    is_ssl = args.l
    nb_clients = args.nb_clients if args.nb_clients else 1
    nb_requests = args.nb_requests if args.nb_requests else 1
    nb_cores = args.nb_cores if args.nb_cores else 1

    if is_ssl == 1:
        client_list = start_clients(k, is_ssl, first_https_port, nb_requests, nb_clients, first_client_port)
    else:
        client_list = start_clients(k, is_ssl, first_http_port, nb_requests, nb_clients, first_client_port)

#    time.sleep(60)
#    total_result = 0

#    for client in client_list:
#        total_result += float(client.parse_result())

#    print total_result
