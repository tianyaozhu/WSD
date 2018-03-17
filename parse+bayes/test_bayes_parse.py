java_path = "C:/Program Files/Java/jre1.8.0_131/bin/java.exe"
parser_path = "D:/stanford-parser-full-2016-10-31/stanford-parser.jar"
models_path = "D:/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar"
engPCFG_path = "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz"

import os
os.environ['JAVA_HOME'] = java_path

import cPickle as pickle

import math

import nltk

from nltk.corpus import senseval

from nltk.tokenize import StanfordTokenizer
tokenizer = StanfordTokenizer(parser_path)

from nltk.parse.stanford import StanfordDependencyParser
parser = StanfordDependencyParser(parser_path, models_path, engPCFG_path)

interest = set(['interest', 'interests', 'Interest', 'Interests'])

sense = {'interest_1':0, 'interest_2':1, 'interest_3':2, 'interest_4': 3, 'interest_5': 4, 'interest_6':5}


bayes = pickle.load(open('bayes_parse.txt', 'r'))

count = pickle.load(open('count.txt', 'r'))

correct = 0

n = 0

for instance in senseval.instances('interest.pos')[1600:2000]:
    sentence = ' '.join(w for (w,p) in instance.context)
    parsed = list(parser.parse(tokenizer.tokenize(sentence)))
    score = []
    for num in count[0:6]:
        score.append(math.log(num / 1600.0))
    for triple in parsed[0].triples():
        related = 0
        if triple[0][0] in interest:
            word = triple[2][0]
            related = 1
        if triple[2][0] in interest:
            word = triple[0][0]
            related = 1
        if related == 1:
            i = 0
            for pdf in bayes[0:6]:
                s = 0
                for item in pdf:
                    if item[0] == word:
                        s = item[1]
                score[i] += math.log((s + 0.000000001) * 1.0 / count[i])
                i += 1

    maxscore = -2147483648
    ans = -1
    i = 0
    for num in score[0:6]:
        if num > maxscore:
            ans = i
            maxscore = num
        i += 1

    if ans == sense[instance.senses[0]]:
        correct += 1

    n += 1

    print ans, sense[instance.senses[0]]
    print correct, '/', n, correct * 1.0 / n
                
                
            
    
