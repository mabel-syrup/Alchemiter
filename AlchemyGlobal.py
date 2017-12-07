import pickle

items = []
components = []
mechanisms = {}
primitives = {}
abilities = {}


def get_seed(data):
    #print("Raw input data is in form {} : {}".format(type(data), data))
    raw_data = pickle.dumps(data)
    #print("Data is in form {} : {}".format(type(raw_data),raw_data))
    int_data = int.from_bytes(raw_data, byteorder='big')
    int_data -= int(len(raw_data) / 2)
    #print("Integer Data is in form {} : {}".format(type(int_data), int_data))
    return int_data


def get_one_from_list(list, seed=0):
    if seed == 0:
        seed = get_seed(list)
    index = seed % len(list)
    return list[index]


def get_item_from_name(name):
    for item in items:
        if item.name.lower() == name.lower():
            return item
    return None
