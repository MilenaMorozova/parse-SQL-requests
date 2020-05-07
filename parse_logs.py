import re
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-c", "--count", action="store_true", dest='counter', help="display the total number of requests")
options, args = parser.parse_args()

file_name = args[0]

with open(file_name, 'r') as file:
    data = file.read()

time = re.findall("\[\d*\.\d*ms\]", data)
time_ms = [float(i[1:-3]) for i in time]

requests = re.split("\[\d*\.\d*ms\]", data)
result = [[time, request.strip()] for time, request in zip(time_ms, requests)]

with open('unsort_'+file_name, 'w') as file_with_unsorted_logs:
    if options.counter:
        file_with_unsorted_logs.write("Total: "+str(len(result))+'\n\n')
    for item in result:
        file_with_unsorted_logs.write("[" + str(item[0]) + "ms] : \n" + item[1] + "\n\n")

sorted_result = sorted(result, reverse=True, key=lambda x: x[0])

with open('sort_'+file_name, 'w') as file_with_sorted_logs:
    if options.counter:
        file_with_sorted_logs.write("Total: "+str(len(result))+'\n\n')
    for item in sorted_result:
        file_with_sorted_logs.write("[" + str(item[0]) + "ms] : \n" + item[1] + "\n\n")
