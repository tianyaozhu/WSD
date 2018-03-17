java_path = "C:/Program Files/Java/jre1.8.0_131/bin/java.exe"
parser_path = "D:/stanford-parser-full-2016-10-31/stanford-parser.jar"
models_path = "D:/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar"
engPCFG_path = "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz"

import os
os.environ['JAVA_HOME'] = java_path

from nltk.tokenize import StanfordTokenizer
tokenizer = StanfordTokenizer(parser_path)

from nltk.parse.stanford import StanfordDependencyParser
parser = StanfordDependencyParser(parser_path, models_path, engPCFG_path)

from nltk.corpus import wordnet

import nltk
from nltk.tree import Tree
from nltk.corpus.reader.wordnet import Lemma
from nltk.corpus import semcor
from nltk.corpus import wordnet

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

    parsed = list(parser.parse(tokenizer.tokenize(sentence)))

    for term in tags[n]:
        if len(term)==1 and isinstance(term[0], basestring) and isinstance(term, Tree) and len(wordnet.synsets(term[0])) > 1:
            if isinstance(term.label(), unicode):
                continue
            syn = term.label().synset()
            word = term[0]
            sense_standard = syn

            print word
        
            for pair in parsed[0].triples():
                if pair[0][0] == word:
                    pos = pair[0][1]
                if pair[2][0] == word:
                    pos = pair[2][1]

            postag = 'none'

            if pos in noun:
                postag = 'n'
            if pos in verb:
                postag = 'v'
            if pos in adjective:
                postag = 's'
            if pos in adverb:
                postag = 'a'

            if postag == 'none':
                sense_list = wordnet.synsets(word)
            else:
                sense_list = wordnet.synsets(word, postag)

            if len(sense_list) == 0:
                sense_list = wordnet.synsets(word)
                   
            sense_ans = sense_list[0]

            maxscore = 0

            for sense in sense_list:

                bank = set()

                for synset in sense.hypernyms():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))

                for synset in sense.instance_hypernyms():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))
        
                for synset in sense.hyponyms():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))

                for synset in sense.instance_hyponyms():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))
        
                for synset in sense.member_holonyms():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))
    
                for synset in sense.substance_holonyms():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))
        
                for synset in sense.part_holonyms():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))

                for synset in sense.member_meronyms():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))
        
                for synset in sense.substance_meronyms():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))
        
                for synset in sense.part_meronyms():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))

                for synset in sense.attributes():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))

                for synset in sense.entailments():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))

                for synset in sense.causes():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))

                for synset in sense.also_sees():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))

                for synset in sense.verb_groups():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))

                for synset in sense.similar_tos():
                    for lemma in synset.lemmas():
                        bank.add(wordnet.morphy(lemma.name()))

                definition = nltk.word_tokenize(sense.definition())
                for tag in nltk.pos_tag(definition):
                    if tag[1] in substantive:
                        bank.add(wordnet.morphy(tag[0]))

                for example in sense.examples():
                    result = list(parser.parse(tokenizer.tokenize(example)))
                    name = set()
                    for lemma in sense.lemmas():
                        name.add(wordnet.morphy(lemma.name()))
                    for pair in result[0].triples():
                        if wordnet.morphy(pair[0][0]) in name and pair[0][1] in substantive:
                            bank.add(wordnet.morphy(pair[2][0]))
                        if wordnet.morphy(pair[2][0]) in name and pair[2][1] in substantive:
                            bank.add(wordnet.morphy(pair[0][0]))
                
                score = 0
    
                for pair in parsed[0].triples():
                    if wordnet.morphy(pair[0][0]) ==  wordnet.morphy(word) and pair[2][1] in substantive and wordnet.morphy(pair[2][0]) in bank:
                        score = score + 1
                    if wordnet.morphy(pair[2][0]) ==  wordnet.morphy(word) and pair[0][1] in substantive and wordnet.morphy(pair[0][0]) in bank:
                        score = score + 1
    
                if score > maxscore:
                    sense_ans = sense
                    maxscore = score

            total = total + 1
            if sense_ans == sense_standard:
                correct = correct + 1

            sense_base = wordnet.synsets(word)[0]
            if sense_base == sense_standard:
                base = base + 1

            print sense_ans, sense_standard
            print correct, '/', total, correct*1.0/total, '    ', base, '/', total, base*1.0/total

    n = n + 1         


