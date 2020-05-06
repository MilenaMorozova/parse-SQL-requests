import re
import sys

file_name = sys.argv[1]

with open(file_name, 'r') as file:
    data = file.read()

time = re.findall("\[\d*\.\d*ms\]", data)
time_ms = [float(i[1:-3]) for i in time]

requests = re.split("\[\d*\.\d*ms\]", data)
result = [[time, request.strip()] for time, request in zip(time_ms, requests)]
sorted_result = sorted(result, reverse=True, key=lambda x: x[0])

with open('sort_'+file_name, 'w') as file_with_sorted_logs:
    for item in sorted_result:
        file_with_sorted_logs.write("[" + str(item[0]) + "ms] : \n" + item[1] + "\n\n")
