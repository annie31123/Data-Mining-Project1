import csv
import sys
from itertools import chain, combinations
from collections import OrderedDict
import time
import operator
import arff

class sset(set):
    def __str__(self):
        return ', '.join([str(i) for i in self])

def data_to_c1(data):
    c1 = set()
    for t in data:
        for item in t:
            c1.add(frozenset([item]))
    return c1
       
def create_ci(item_set, data):
    can_set = dict()
    for item in item_set:
        for transcation in data:
            if item.issubset(transcation):
                can_set[item] = can_set.get(item, 0) + 1
    return can_set


def create_li(item_set, min_support):
    fre_set = dict()
    for key, value in list(item_set.items()):
        if value >= min_support:
            fre_set[key] = value
    return fre_set
        
def join(fre_set, level):
    join_set = set()
    for f1 in fre_set:
        for f2 in fre_set:
            if f1 != f2:
                join = f1.union(f2)
                if len(join) == level:
                    join_set.add(join)
    return join_set

def ibm_data():
    arff_data = list()
    data =list()
    pat_data = open('./data/pat.ntrans_5.tlen_10.nitems_0.02', 'rU')
    
    for line in pat_data:
        line = line.strip().rstrip(',')
        split_item_set = line.split('  ')
        if len(split_item_set) == 3:
            data_list = list()
            arff_list = list()
            trans_list = split_item_set[2].split(' ')
            for i in range(0, 20): 
                if str(i) in trans_list:
                    data_list.append(str(i)+'=t')
                    arff_list.append('t')
                else:
                    arff_list.append('?')

            data.append(set(data_list))
            arff_data.append(arff_list)
            
    attr = list()
    for i in range(0,20):
        attr.append((str(i),['?','t']))
    obj = {
        'description': u'',
        'relation': 'ibm',
        'attributes': attr,
        'data': arff_data,
    }
    arff.dump(obj,open('ibm.arff', 'w'))

    return data

def mushroom_data():
    data = list() 
    with open('./data/mushrooms.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for index, value in enumerate(spamreader):
            if index == 0:
                attribute = value
            else:
                for v_index, element in enumerate(value):
                    value[v_index] = attribute[v_index] + ':' + element
                data.append(set(value))
    return data

def powerset(iterable):
    xs = list(iterable)
    return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

def rule(fre_set, min_confidence):
    cnt = 0
    print('Best rules:')
    for f in list(fre_set.items()):
        
        if len(f[0]) <= 1:
            continue
        subsets = list(map(frozenset, powerset(f[0])))
        
        for subset in subsets[1:]:
            set1 = f[0]-subset
            if len(set1) != 0:
                num = round(float(f[1] / fre_set[subset]),3)
                if num >= min_confidence:
                    cnt+=1
                    stri = str(cnt) + '. ' + str(sset(subset)) + ' -> ' + str(sset(set1)) + '   [ conf: ' + str('%.3f'%num) + ' ]'
                    print(stri)


def apriori(data, min_support, min_confidence):
    c1 = data_to_c1(data)
    c = create_ci(c1, data)
    level_set = create_li(c, min_support)
    fre_set = level_set

    level = 1
    while len(level_set) != 0:
        level += 1
        join_set = join(fre_set, level)
        can_set = create_ci(join_set, data)
        level_set = create_li(can_set, min_support)
        fre_set = {**fre_set, **level_set}

    rule(fre_set, min_confidence)

if __name__ == '__main__':
    start = time.time()
   
    data = list()
    if sys.argv[1] == '0':
        data = mushroom_data()
    elif sys.argv[1] == '1':
        data = ibm_data()
    

    print('Min Support: ' + sys.argv[2])
    print('Min Confidence: ' + sys.argv[3])
    print('')
    min_support = int(len(data) * float(sys.argv[2]))
    min_confidence = float(sys.argv[3])
    
    apriori(data, min_support, min_confidence)
    print('')
    print('Process time: %s seconds' % (time.time() - start))
    
