import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import random

# all same length
totalacc = 0
tests = 10
test_same = 61140 * 0.1
tsv_title = 'soc-redditHyperlinks-title.tsv'
for R in range(tests):

    #tsv_body = 'soc-redditHyperlinks-body.tsv'
    train_table = pd.read_table(tsv_title, sep='\t', header="infer")

    #test_table = pd.read_table(tsv_body, sep='\t', header="infer")
    train_labels = train_table['LINK_SENTIMENT'].astype(int)
    train = train_table['PROPERTIES']
    #test_labels = test_table['LINK_SENTIMENT'].astype(int)
    #test = test_table['PROPERTIES']

    plist = []
    i = 0
    counter = 0
    test_same_data = []
    maxright = 61140
    train_label = []
    count = 0
    test_same_label = []

    ilist = []

    for p in train:
        hatred = (train_labels[i], p.split(','))
        ilist.append(hatred)
        i += 1

    counter2 = 0
    random.shuffle(ilist)
    i = 0
    for r in ilist:

        i = r[0]
        p = r[1]

        if i == 1 and counter < maxright:
            plist.append(p)#.split(','))
            counter += 1
            train_label.append(1)
        elif i == 1 and counter2 < maxright:
            test_same_data.append(p)
            test_same_label.append(1)
            counter2 += 1
        elif i == -1:
            if count < test_same:
                test_same_data.append(p)#.split(','))
                test_same_label.append(0)
                count += 1
            else:
                plist.append(p)#.split(','))
                count += 1
                train_label.append(0)



    train = np.asarray(plist, dtype=float)
    # test = np.asarray(tlist, dtype=float)
    # test_labels = np.asarray(labels)
    train_labels = np.asarray(train_label)
    test_same_data = np.asarray(test_same_data, dtype=float)

    test_same_label = np.asarray(test_same_label)

    model = tf.keras.Sequential([
        layers.Dense(86, activation='sigmoid'),
        layers.Dense(43, activation='relu'),
        layers.Softmax(),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss=tf.keras.losses.binary_crossentropy, metrics=['accuracy'])

    model.fit(train, train_labels, epochs=10, batch_size=32, shuffle=True, verbose=1)
    loss, acc = model.evaluate(test_same_data, test_same_label)
    print(acc)
    totalacc += (acc*100)
    #print(acc)

print(totalacc/tests)