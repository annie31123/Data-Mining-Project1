import arff
import csv
import sys
from itertools import chain, combinations
from collections import OrderedDict, defaultdict
import time

arff_attr = [
            ('class=p',['?','t']),('class=e',['?','t']),
            ('cap-shape=b',['?','t']),('cap-shape=c',['?','t']),('cap-shape=x',['?','t']),('cap-shape=f',['?','t']),('cap-shape=k',['?','t']),('cap-shape=s',['?','t']),
            ('cap-surface=f',['?','t']),('cap-surface=g',['?','t']),('cap-surface=y',['?','t']),('cap-surface=s',['?','t']),
            ('cap-color=n',['?','t']),('cap-color=b',['?','t']),('cap-color=c',['?','t']),('cap-color=g',['?','t']),('cap-color=r',['?','t']),('cap-color=p',['?','t']),('cap-color=u',['?','t']),('cap-color=e',['?','t']),('cap-color=w',['?','t']),('cap-color=y',['?','t']),
            ('bruises=t',['?','t']),('bruises=f',['?','t']),
            ('oder=a',['?','t']),('oder=l',['?','t']),('oder=c',['?','t']),('oder=y',['?','t']),('oder=f',['?','t']),('oder=m',['?','t']),('oder=n',['?','t']),('oder=p',['?','t']),('oder=s',['?','t']),
            ('gill-attachment=a',['?','t']),('gill-attachment=d',['?','t']),('gill-attachment=f',['?','t']),('gill-attachment=n',['?','t']),
            ('gill-spacing=c',['?','t']),('gill-spacing=w',['?','t']),('gill-spacing=d',['?','t']),
            ('gill-size=b',['?','t']),('gill-size=n',['?','t']),
            ('gill-color=b',['?','t']),('gill-color=n',['?','t']),('gill-color=k',['?','t']),('gill-color=h',['?','t']),('gill-color=g',['?','t']),('gill-color=r',['?','t']),('gill-color=o',['?','t']),('gill-color=p',['?','t']),('gill-color=u',['?','t']),('gill-color=e',['?','t']),('gill-color=w',['?','t']),('gill-color=y',['?','t']),
            ('stalk-shape=e',['?','t']),('stalk-shape=t',['?','t']),
            ('stalk-root=e',['?','t']),('stalk-root=b',['?','t']),('stalk-root=c',['?','t']),('stalk-root=u',['?','t']),('stalk-root=z',['?','t']),('stalk-root=r',['?','t']),('stalk-root=f',['?','t']),
            ('stalk-surface-above-ring=f',['?','t']),('stalk-surface-above-ring=y',['?','t']),('stalk-surface-above-ring=k',['?','t']),('stalk-surface-above-ring=s',['?','t']),
            ('stalk-surface-below-ring=f',['?','t']),('stalk-surface-below-ring=y',['?','t']),('stalk-surface-below-ring=k',['?','t']),('stalk-surface-below-ring=s',['?','t']),
            ('stalk-color-above-ring=n',['?','t']),('stalk-color-above-ring=b',['?','t']),('stalk-color-above-ring=c',['?','t']),('stalk-color-above-ring=g',['?','t']),('stalk-color-above-ring=o',['?','t']),('stalk-color-above-ring=p',['?','t']),('stalk-color-above-ring=e',['?','t']),('stalk-color-above-ring=w',['?','t']),('stalk-color-above-ring=y',['?','t']),
            ('stalk-color-below-ring=n',['?','t']),('stalk-color-below-ring=b',['?','t']),('stalk-color-below-ring=c',['?','t']),('stalk-color-below-ring=g',['?','t']),('stalk-color-below-ring=o',['?','t']),('stalk-color-below-ring=p',['?','t']),('stalk-color-below-ring=e',['?','t']),('stalk-color-below-ring=w',['?','t']),('stalk-color-below-ring=y',['?','t']),
            ('veil-type=p',['?','t']),('veil-type=u',['?','t']),
            ('veil-color=n',['?','t']),('veil-color=o',['?','t']),('veil-color=w',['?','t']),('veil-color=y',['?','t']),
            ('ring-number=n',['?','t']),('ring-number=o',['?','t']),('ring-number=t',['?','t']),
            ('ring-type=c',['?','t']),('ring-type=e',['?','t']),('ring-type=f',['?','t']),('ring-type=l',['?','t']),('ring-type=n',['?','t']),('ring-type=p',['?','t']),('ring-type=s',['?','t']),('ring-type=z',['?','t']),
            ('spore-print-color=k',['?','t']),('spore-print-color=n',['?','t']),('spore-print-color=b',['?','t']),('spore-print-color=h',['?','t']),('spore-print-color=r',['?','t']),('spore-print-color=o',['?','t']),('spore-print-color=u',['?','t']),('spore-print-color=w',['?','t']),('spore-print-color=y',['?','t']),
            ('population=a',['?','t']),('population=c',['?','t']),('population=n',['?','t']),('population=s',['?','t']),('population=v',['?','t']),('population=y',['?','t']),
            ('habitat=g',['?','t']),('habitat=l',['?','t']),('habitat=m',['?','t']),('habitat=p',['?','t']),('habitat=u',['?','t']),('habitat=w',['?','t']),('habitat=d',['?','t']),
        ]

start= time.time()
data = list()  # transaction
arff_data = list()

with open('./data/mushrooms.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            
    for index, value in enumerate(spamreader):   # get transcation list and process the origin data 
        if index == 0:
            attribute = value[0].split(',')
        else:
            value_split = value[0].split(',')
            for index1, element in enumerate(value_split):
                value_split[index1] = attribute[index1] + '=' + element

            attr_value = list()
            for attr in arff_attr:
                if attr[0] in value_split:
                    attr_value.append('t')
                else:
                    attr_value.append('?')
            arff_data.append(attr_value)

obj = {
        'description': u'',
        'relation': 'mushrooms',
        'attributes': arff_attr,
        'data': arff_data,
    }
arff.dump(obj,open('mushrooms.arff', 'w'))

#print(arff_data)

           

print('Process time: %s seconds' % (time.time() - start))