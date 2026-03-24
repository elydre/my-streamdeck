import psutil

psutil_history = {
    "cpu": [],
    "mem": [],
}

def get_memory_usage():
    return round(psutil.virtual_memory().used / psutil.virtual_memory().total * 100, 2)

def get_memory_usage_go():
    return psutil.virtual_memory().used / 1024 ** 3

def get_cpu_temp():
    try:
        return round(psutil.sensors_temperatures()['coretemp'][0].current)
    except:
        return 0

def get_cpu_usage():
    return psutil.cpu_percent()

def to_graph(args, in_list, in_max=None, in_min=0):
    max_len = args["info"]["resolution"][0]
    max_val = args["info"]["resolution"][1]

    out_list = in_list.copy()

    # remove values
    while len(out_list) > max_len:
        out_list.pop(0)

    # scale values
    if in_max is None: in_max = max(out_list) + max(out_list) / 10 + 1
    out_list = [int((i - in_min) * (max_val - 0) / (in_max - in_min)) for i in out_list]

    for i in range(len(out_list)):
        out_list[i] = max(0, min(out_list[i], max_val))

    # add values
    while len(out_list) < max_len:
        out_list.insert(0, 0)

    return out_list

def graph_psutil(args, thing):
    max_len = args["info"]["resolution"][0]

    if len(psutil_history[thing]) > max_len:
        psutil_history[thing].pop(0)
    
    if thing == "cpu":
        psutil_history[thing].append(psutil.cpu_percent())
    elif thing == "mem":
        psutil_history[thing].append(get_memory_usage())

    return to_graph(args, psutil_history[thing], 100)

def graph_streamdeck(args, in_list):
    new_list = []
    for i in range(0, len(in_list) - 4, 4):
        new_list.append(max(in_list[i], in_list[i+1], in_list[i+2], in_list[i+3]))

    return to_graph(args, new_list, 100)


def get_linux_version():
    # return linux kernel version
    with open("/proc/version", "r") as f:
        return f.read().split(" ")[2].split("-")[0]
