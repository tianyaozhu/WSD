java_path = "C:/Program Files/Java/jre1.8.0_131/bin/java.exe"
parser_path = "D:/stanford-parser-full-2016-10-31/stanford-parser.jar"
models_path = "D:/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar"
engPCFG_path = "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz"

import os
os.environ['JAVA_HOME'] = java_path

import cPickle as pickle

import nltk

from nltk.corpus import senseval

from nltk.tokenize import StanfordTokenizer
tokenizer = StanfordTokenizer(parser_path)

from nltk.parse.stanford import StanfordDependencyParser
parser = StanfordDependencyParser(parser_path, models_path, engPCFG_path)

interest = set(['interest', 'interests', 'Interest', 'Interests'])

sense = {'interest_1':0, 'interest_2':1, 'interest_3':2, 'interest_4': 3, 'interest_5': 4, 'interest_6':5}

bayes = [[],[],[],[],[],[]]

count = [0, 0, 0, 0, 0, 0]

n = 0

for instance in senseval.instances('interest.pos')[0:1599]:
    count[sense[instance.senses[0]]] += 1
    sentence = ' '.join(w for (w,p) in instance.context)
    parsed = list(parser.parse(tokenizer.tokenize(sentence)))
    for triple in parsed[0].triples():
        related = 0
        if triple[0][0] in interest:
            word = triple[2][0]
            related = 1
        if triple[2][0] in interest:
            word = triple[0][0]
            related = 1
        if related == 1:
            exist = 0
            for item in bayes[sense[instance.senses[0]]]:
                if item[0] == word:
                    item[1] += 1
                    exist = 1
            if exist == 0:
                bayes[sense[instance.senses[0]]].append(list([word, 1]))
    n += 1
    print n
                
pickle.dump(bayes, open('bayes_parse.txt', 'w'))
pickle.dump(count, open('count.txt', 'w'))

    
 
