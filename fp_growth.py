import csv
import sys
from itertools import chain, combinations
from collections import OrderedDict, defaultdict
import time
import operator
import arff

class sset(set):
    def __str__(self):
        return ', '.join([str(i) for i in self])

class node:
    def __init__(self, name, parent):
        self.name = name
        self.count = 1
        self.link = None
        self.parent = parent
        self.children = {}

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
    arff.dump(obj,open('IBM.arff', 'w'))

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


def create_ordered_set(transactions, item_set): 
    ordered_item_set = list()
    sorted_itemset = sorted(item_set.items(), key=operator.itemgetter(1), reverse=True)

    for transaction in transactions:
        ordered_transaction = list()
        for item in sorted_itemset:
            if item[0] in transaction:
                ordered_transaction.append(item[0])
        ordered_item_set.append(ordered_transaction)

    return ordered_item_set


def create_item_set(data, min_support): 
    can_set = dict()
    
    for trans in data:
        for item in trans:
            can_set[item] = can_set.get(item, 0) + 1

    for key, value in list(can_set.items()): 
        if value < min_support:
            can_set.pop(key, None)
 
    return can_set

def construct_fptree(ordered_item_set, item_set):
    root = node('{}', None) 
    head = dict()

    if len(item_set) == 0:
        return root, head

    for item, value in item_set.items():  
        head[item] = [value, None] 

    for item_set in ordered_item_set:
        fptree_update(item_set, root, head) 

    return root, head


def fptree_update(item_set, current, head):
    if len(item_set) > 0:
        current_item = item_set[0]

        if current_item in current.children:  
            current.children[current_item].count += 1
        else:  
            current.children[current_item] = node(current_item, current) 
            
            if head[current_item][1] == None:  
                head[current_item][1] = current.children[current_item]
            else: 
                linked_node = head[current_item][1]
                while linked_node.link != None: 
                    linked_node = head[current_item][1].link
                linked_node.link = current.children[current_item] 

    if len(item_set) > 1:  
        fptree_update(item_set[1:], current.children[current_item], head)

def find_fre_patterns(in_tree, head, min_support, prefix, fre_pattern, item_set): 
    sorted_head = [v[0] for v in sorted(head.items(), key=lambda p: str(p[1]))]

    for base in sorted_head:
        new_prefix = prefix.copy()
        new_prefix.add(base)

        frozen_fre = list()
        for i in new_prefix:
            frozen_fre.append(i)

        condition_patterns, count = find_con_patterns(head[base][1])   
        fre_pattern[frozenset(frozen_fre)] = fre_pattern.get(frozenset(frozen_fre), 0) +  count 
        for i in condition_patterns:
            fre_pattern[frozenset(frozen_fre)] = fre_pattern.get(frozenset(frozen_fre), 0) + i[1]

        data = list() 
        for patterns in condition_patterns:
            pattern = list()
            for i in range(0, patterns[1]):
                data.append(patterns[0])
                for k in patterns[0]:
                    pattern.append(k)

        item_set = create_item_set(data, min_support)
        ordered_item_set = create_ordered_set(data, item_set)

        if len(ordered_item_set) != 0: 
            t, h = construct_fptree(ordered_item_set, item_set)
            if h != None: 
                find_fre_patterns(t, h, min_support, new_prefix, fre_pattern, item_set)


def find_con_patterns(node): 
    condition_patterns = list()
    count = 0

    while node != None:
        prefix = list()

        current = node        
        while current.parent != None:  
            prefix.append(current.name)
            current = current.parent

        if len(prefix) > 1:
            condition_patterns.append((set(prefix[1:]), node.count))
        else: 
            count = count + node.count
        node = node.link
    return condition_patterns, count



def level_append(fre_pattern):
    level_set = list()

    fre_copy = fre_pattern.copy()
    index = 0
    while len(fre_copy) != 0: 
        level = list()
        for item_set, count in list(fre_pattern.items()):
            if len(item_set) - 1 == index:
                level.append(item_set)
                fre_copy.pop(item_set, None)
        level_set.append(level)
        index += 1

    return level_set

def powerset(iterable):
    xs = list(iterable)
    return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

def rule(level_set, fre_pattern, min_confidence):
    cnt = 0
    print('Best rules:')
    for idx, level in enumerate(level_set[1:]):  
        for item_set in level:
            subsets = list(map(frozenset, powerset(item_set)))
            for subset in subsets[1:]: 
                if len(item_set) > len(subset):
                    num = round(float(fre_pattern.get(item_set, 0)) / float(fre_pattern.get(subset, 0)),3)
                    if  num >= min_confidence:  
                        cnt+=1
                        set1 = item_set - subset
                        stri = str(cnt) + '. ' + str(sset(subset)) + ' -> ' + str(sset(set1)) + '   [ conf: ' + str('%.3f'%num) + ' ]'
                        print(stri)

def fp_growth(data, min_support, min_confidence):
    item_set = create_item_set(data, min_support)  
    ordered_item_set = create_ordered_set(data, item_set)
    
    fptree, head = construct_fptree(ordered_item_set, item_set) 

    fre_pattern = dict()
    find_fre_patterns(fptree, head, min_support, set([]), fre_pattern, item_set)

    level_set = level_append(fre_pattern)
    rule(level_set, fre_pattern, min_confidence)
    


    

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
    fp_growth(data, min_support, min_confidence)
    
    print('')
    print('Process time: %s seconds' % (time.time() - start))