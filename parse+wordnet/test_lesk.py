java_path = "C:/Program Files/Java/jre1.8.0_131/bin/java.exe"
parser_path = "D:/stanford-parser-full-2016-10-31/stanford-parser.jar"
models_path = "D:/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar"
engPCFG_path = "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz"

import os
os.environ['JAVA_HOME'] = java_path

import sys

from nltk.tokenize import StanfordTokenizer
tokenizer = StanfordTokenizer(parser_path)

from nltk.parse.stanford import StanfordDependencyParser
parser = StanfordDependencyParser(parser_path, models_path, engPCFG_path)

from nltk.corpus import wordnet

import nltk
from nltk.tree import Tree
from nltk.corpus.reader.wordnet import Synset
from nltk.corpus import semcor
from nltk.corpus import wordnet
from nltk.wsd import lesk

noun = set(['NN', 'NNS', 'NNP', 'NNPS'])
verb = set(['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'])
adjective = set(['JJ', 'JJR', 'JJS'])
adverb = set(['RB', 'RBR', 'RBS'])
substantive = noun | verb | adjective | adverb

corp = semcor.sents()

tags = semcor.tagged_sents(tag = 'sem')

n = 0

correct = 0
base = 0
total = 0

for sent in corp:

    sentence =  ' '.join(sent)

    print sentence

    for term in tags[n]:
        if len(term)==1 and isinstance(term[0], basestring) and isinstance(term, Tree) and len(wordnet.synsets(term[0])) > 1:
            if isinstance(term.label(), unicode):
                continue
            syn = term.label().synset()
            word = term[0]
            sense_standard = syn

            print word

            pos = syn.pos()
        
            sense_ans = lesk(sent, word, pos)

            total = total + 1

            if not sense_ans:
                continue

            if sense_ans == sense_standard:
                correct = correct + 1

            print sense_ans, sense_standard
            print correct, '/', total, correct*1.0/total

            if total == 2000:
                sys.exit()
                
    n = n + 1         


