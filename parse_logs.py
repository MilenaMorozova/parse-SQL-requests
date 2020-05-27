import re
from optparse import OptionParser
import os


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

    result_with_counter = []

    for key in first_string_of_logs:
        group = first_string_of_logs[key]
        time_in_group = [i[0] for i in group]

        temp = []
        i = 0
        while i < len(time_in_group):
            number_of_item = time_in_group.count(time_in_group[i])
            temp.append((number_of_item, group[i]))
            i += number_of_item

        result_with_counter.append(temp)

    return result_with_counter


def write_to_file(data, file_name, options):
    with open(file_name, 'w') as output_file:
        if options.counter:
            output_file.write("Total requests: "+str(len(data))+'\n\n')

        if options.time:
            output_file.write("Total time: "+str(calc_total_time(data))+'\n\n')

        for item in data:
            output_file.write("[" + str(item[0]) + "ms] : \n" + item[1] + "\n\n")


def calc_len_of_group(group: list):
    return sum([i[0] for i in group])


def calc_time_in_group(group: list):
    return sum([i[0] * i[1][0] for i in group])


def write_to_file_grouped_data(grouped_data, file_name, options):
    with open(file_name, 'w') as output_file:
        if options.group:
            for group in grouped_data:
                if options.counter:
                    output_file.write("Total requests in group: " + str(calc_len_of_group(group)) + '\n\n')

                if options.time:
                    output_file.write("Total time: " + str(calc_time_in_group(group)) + '\n\n')

                for item in group:
                    output_file.write("[" + str(item[1][0]) + "ms] " + ("" if item[0] == 1 else "X "+str(item[0])) +
                                      ": \n" + item[1][1] + "\n\n")

                output_file.write('-' * 125 + '\n\n')


if __name__ == '__main__':
    parser = OptionParser()
    create_options_for_option_parser(parser)
    options, args = parser.parse_args()

    path_to_input_file = os.path.dirname(args[0])
    name_of_original_file = os.path.basename(args[0])

    data = read_data_from_file(args[0])

    write_to_file(data, os.path.join(path_to_input_file, 'unsort_'+name_of_original_file), options)

    sorted_data = sort_logs(data, True)
    write_to_file(sorted_data, os.path.join(path_to_input_file, 'sort_'+name_of_original_file), options)

    data_grouped = group_logs_by(data)
    write_to_file_grouped_data(data_grouped, os.path.join(path_to_input_file, 'grouped_'+name_of_original_file), options)
