import subprocess
import argparse

nserver = 0
cur_core = 0
ncores = 1
filelen = 0

class SSL(object):
    def __init__(self, http_port, https_port, core):
        self.http_port = http_port
        self.https_port = https_port

        self.args = ["taskset"]
        self.args.extend(["-c", str(core)])
        self.args.extend(["./axhttpd"])
        self.args.extend(["-l", filelen])
        if http_port > 0:
            self.args.extend(["-p", str(http_port)])
        if https_port > 0:
            self.args.extend(["-s", str(https_port)])
        print self.args
        self.p = subprocess.Popen(self.args)

    def stop(self):
        self.p.terminate()

def increment_core_num(core):
    global cur_core
    p = core + cur_core
    cur_core = (cur_core + 1) % ncores
    return p

def start_server(http_port, https_port, nb_servers):
    ws_list = []

    for _ in range(nb_servers):
        nc = increment_core_num(0)
        ws_list.append(SSL(http_port, https_port, nc))
        if http_port > 0:
            http_port += 1
        if https_port > 0:
            https_port += 1
    return ws_list

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="http port number", type=int)
    parser.add_argument("-s", help="https port number", type=int)
    parser.add_argument("-c", help="number of cores", type=int)
    parser.add_argument("--nb_servers", help="number of instances to create", type=int)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    http_port = args.p
    https_port = args.s
    ncores = args.c if args.c else 1
    nb_servers = args.nb_servers if args.nb_servers else 1

    ws_list = start_server(http_port, https_port, nb_servers)
    while True:
        quit = raw_input("quit? y/n")
        if "y" in quit:
            break

    for ws in ws_list:
        ws.stop()
