import hashlib

import numpy as np

sizes = [25, 50, 75, 100]


def gen_rand_sizes(qty):
    assets = []

    for _ in range(qty):
        assets.append((np.random.choice(sizes),
                       np.random.choice(sizes)))

    return assets


def gen_rand_size():
    return np.random.choice(sizes)


# https://www.geeksforgeeks.org/python-merge-two-lists-into-list-of-tuples/
def merge(list1, list2):
    merged_list = []
    for i in range(max((len(list1), len(list2)))):

        while True:
            try:
                tup = (list1[i], list2[i])
            except IndexError:
                if len(list1) > len(list2):
                    list2.append('')
                    tup = (list1[i], list2[i])
                elif len(list1) < len(list2):
                    list1.append('')
                    tup = (list1[i], list2[i])
                continue

            merged_list.append(tup)
            break
    return merged_list


# https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists
def flatten(t):
    return [item for sublist in t for item in sublist]