import os

path = "logs/"
files = os.listdir(path)
s = []
total_result = 0
request_per_sec = 0

for file in files:
    with open(path+"/"+file, "r") as f:
        for line in f:
            if line.startswith("Requests per second:"):
                print line
                request_per_sec = line.split()[3].strip();
                print request_per_sec
                break
        total_result += float(request_per_sec)
    
print total_result
