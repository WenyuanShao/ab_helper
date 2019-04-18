import os
import sys

path = "logs/"
files = os.listdir(path)
s = []
num = 0
total_result = 0
req_per_sec_min = sys.maxint
req_per_sec_max = 0
time_taken_avg = 0
time_taken_min = sys.maxint
time_taken_max = 0
failed_request_tot = 0
HTML_transferred_min = sys.maxint
HTML_transferred_max = 0
time_per_req_min = sys.maxint
time_per_req_max = 0
time_per_req_avg = 0
tail_latency_min = sys.maxint
tail_latency_max = 0
tail_latency_avg = 0
temp = 0
flag = 1
failure=[]


for file in files:
    with open(path+"/"+file, "r") as f:
        for line in f:
            if line.startswith("Requests per second:"):
#                print line
                temp = float(line.split()[3].strip())
                req_per_sec_min = min(req_per_sec_min, temp)
                req_per_sec_max = max(req_per_sec_max, temp)
                total_result += temp
            elif line.startswith("Time taken for tests:"):
                temp = float(line.split()[4].strip())
		time_taken_min = min(temp, time_taken_min)
		time_taken_max = max(temp, time_taken_max)
		time_taken_avg += temp
            elif line.startswith("Failed requests:"):
                temp = (int)(line.split()[2].strip())
                if temp > 0:
                    failure.append(11211+num+1)
                    failed_request_tot += temp
#                    print "found err"
                    break
            elif line.startswith("HTML transferred:"):
                temp = (int)(line.split()[2].strip())
                HTML_transferred_min = min(temp, HTML_transferred_min)
                HTML_transferred_max = max(temp, HTML_transferred_max)
            elif (line.startswith("Time per request:") and flag):
                temp = float(line.split()[3].strip())
                time_per_req_min = min(time_per_req_min, temp)
                time_per_req_max = max(time_per_req_max, temp)
                time_per_req_avg += temp
                flag = 0
            elif line.startswith("  99%"):
                temp = (int)(line.split()[1].strip())
                tail_latency_min = min(tail_latency_min, temp)
                tail_latency_max = max(tail_latency_max, temp)
                tail_latency_avg += temp
            flag = 1
#        print "------------"
        num += 1

print("Request per second:              tot: {}, max: {}, min: {}".format(total_result, req_per_sec_max, req_per_sec_min))
print("Number of success clients:       {}".format(num))
print("Time taken for tests:            min: {}, max: {}, avg: {:.3f}".format(time_taken_min, time_taken_max, time_taken_avg/num))
print("Failed requests:                 {}".format(failed_request_tot))
print("HTML transferred:                min: {}, max: {}".format(HTML_transferred_min, HTML_transferred_max))
print("Time per request:                min: {}, max: {}, avg: {:.3f}".format(time_per_req_min, time_per_req_max, time_per_req_avg/num))
print("Tail lantency:                   min: {}, max: {}, avg: {}".format(tail_latency_min, tail_latency_max, tail_latency_avg/num))
print("Possible failed client logfile: ")
for i in failure:
    print("    log/ab_{}".format(i))
