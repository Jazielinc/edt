import math

def _do_data(data):
    response = {
        'count' : len(data),
        'avg': None,
        'std': None
    }

    avg = {
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        }
    for row in data: 
        avg[str(row[1])] += 1
    
    final_avg = 0
    total_ = 0
    std_list = []
    for key in avg:
        final_avg = avg[key]*int(key)
        total_ += avg[key]
        std_list.append(avg[key])
    
    final_avg = final_avg/total_

    response['avg'] = final_avg

    mean = sum(std_list) / len(std_list)
    var = sum((l-mean)**2 for l in std_list) / len(std_list)
    st_dev = math.sqrt(var)

    response['std'] = st_dev

    return response