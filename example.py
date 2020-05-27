from collections import Counter

l = [[0, 'fi\nfz'], [1, 'ft\nyu'], [-1, 'gh\ngh'], [-1, 'fi\nfg'], [-1, 'gh\ngh']]
k = sorted(l, key=lambda x: x[0])

d = {}
for i in l:
    key = i[1].split('\n')[0]
    if d.get(key) is None:
        d[key] = [i]
    else:
        d[key].append(i)
for key in d:
    d[key] = sorted(d[key], key=lambda x: x[0])
    result = []
for key in d:
    group = d[key]
    print(group)
    i = 0
    while i < len(group):
        counter = group.count(group[i])
        result.append((counter, group[i]))
        # print(group[i], '-', counter)
        i += counter
print(result)
# print(list(d.values()))
