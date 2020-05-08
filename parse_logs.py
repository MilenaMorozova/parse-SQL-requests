import re
from optparse import OptionParser


def create_options_for_option_parser(option_parser: OptionParser):
    option_parser.add_option("-c", "--count", action="store_true", dest='counter', help="display the total number of requests")
    option_parser.add_option("-t", "--time", action="store_true", dest='time',
                             help="display the total time of requests")
    option_parser.add_option("-g", "--group", action="store_true", dest='group',
                             help="group requests by first string")


def read_data_from_file(file_name):
    with open(file_name, 'r') as file:
        logs_data = file.read()

    logs_data = logs_data.strip('> \n')

    time = re.findall("\[\d*\.\d*ms\]", logs_data)
    time_ms = [float(i[1:-3]) for i in time]

    requests = re.split("\[\d*\.\d*ms\]", logs_data)
    result = [[time, request.strip()] for time, request in zip(time_ms, requests)]
    return result


def sort_logs(data, reverse=False):
    return sorted(data, reverse=reverse, key=lambda x: x[0])


def calc_total_time(data):
    return sum([i[0] for i in data])


def group_logs_by(data: list, sort_by=True, reverse=True):
    first_string_of_logs = {}
    for i in data:
        key = i[1].split('\n')[0]
        if first_string_of_logs.get(key) is None:
            first_string_of_logs[key] = [i]
        else:
            first_string_of_logs[key].append(i)
    if sort_by:
        for key in first_string_of_logs:
            first_string_of_logs[key] = sorted(first_string_of_logs[key], reverse=reverse, key=lambda x: x[0])

    return list(first_string_of_logs.values())


def write_to_file(data, file_name, options):
    with open(file_name, 'w') as output_file:
        if options.counter:
            output_file.write("Total requests: "+str(len(data))+'\n\n')

        if options.time:
            output_file.write("Total time: "+str(calc_total_time(data))+'\n\n')

        for item in data:
            output_file.write("[" + str(item[0]) + "ms] : \n" + item[1] + "\n\n")


def write_to_file_grouped_data(grouped_data, file_name, options):
    with open(file_name, 'w') as output_file:
        if options.group:
            for group in grouped_data:
                if options.counter:
                    output_file.write("Total requests in group: " + str(len(group)) + '\n\n')

                if options.time:
                    output_file.write("Total time: " + str(calc_total_time(group))+'\n\n')

                for item in group:
                    output_file.write("[" + str(item[0]) + "ms] : \n" + item[1] + "\n\n")
                output_file.write('-'*125+'\n\n')


if __name__ == '__main__':
    parser = OptionParser()
    create_options_for_option_parser(parser)

    options, args = parser.parse_args()
    name_of_original_file = args[0]

    data = read_data_from_file(name_of_original_file)

    write_to_file(data, 'unsort_'+name_of_original_file, options)

    sorted_data = sort_logs(data, True)
    write_to_file(sorted_data, 'sort_'+name_of_original_file, options)

    data_grouped = group_logs_by(data)
    write_to_file_grouped_data(data_grouped, 'grouped_'+name_of_original_file, options)
