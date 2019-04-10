import subprocess
import argparse
import time

cur_core = 0
nb_cores = 1
server = "127.0.0.1"

class client(object):
    def __init__(self, k, https_port, nb_requests, core, client_port):
        self.https_port = https_port

        self.args = ["taskset"]
        self.args.extend(["-c", str(core)])
        self.args.extend(["./ab"])
        if k:
            self.args.extend(["-k"])
        self.args.extend(["-D", str(client_port)])
        self.args.extend(["-n", str(nb_requests)])
        self.args.extend(["https://{}:{}/".format(server, https_port)])

        self.log_file_path, log_file = self.create_log()
        print self.args
        
        self.p = subprocess.Popen(self.args, stdout=log_file)
        log_file.close()

    def stop(self):
        while self.process.poll() is None:
            time.sleep(1)
        self.log_file_path.close()

    def create_log(self):
        file_path = "logs/ab_{}".format(self.https_port)
        f = open(file_path, "w+")
        f.write("ab arguments: {}\n\nSTDOUT:\n".format(str(self.args)))
        f.flush()
        return file_path, f

    def parse_result(self):
        with open(self.log_file_path, "r") as f:

            for line in f:
                if line.startswith("Requests per second:"):
                    print line
                    self.request_per_sec = line.split()[3].strip();
                    print self.request_per_sec
                    break

        return self.request_per_sec

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
    p = core + cur_core
    cur_core = (cur_core + 1) % nb_cores
    return p

def start_clients(k, https_port, nb_requests, nb_clients, client_port):
    client_list=[]
    for _ in range(nb_clients):
        nc = increment_core_num(0)
        client_list.append(client(k, https_port, nb_requests, nc, client_port))
        """
        if https_port > 0:
            https_port += 1
        """
        if client_port > 0:
            client_port += 1
    return client_list

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="server port number", type=int)
    parser.add_argument("-k", help="turn on Keep-Alive feature", action='store_true')
    parser.add_argument("--nb_clients", help="number of clients to create", type=int)
    parser.add_argument("--nb_requests", help="number of requests to make", type=int)
    parser.add_argument("--nb_cores", help="number of cores", type=int)
    return parser.parse_args()

if __name__ == '__main__':

    args = parse_args()
    server = "127.0.0.1"
    client_port = 11211
    https_port = args.p if args.p else 443
    k = args.k
    nb_clients = args.nb_clients if args.nb_clients else 1
    nb_requests = args.nb_requests if args.nb_requests else 1
    nb_cores = args.nb_cores if args.nb_cores else 1

    client_list = start_clients(k, https_port, nb_requests, nb_clients, client_port)

    time.sleep(10)
    total_result = 0

    for client in client_list:
        total_result += float(client.parse_result())

    print total_result
