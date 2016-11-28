from IRmodel import *
from Weighter import *
import math

class LanguageModel(IRmodel):
    # 1-gram language model
    def __init__(self, weighter, lam):
        self.weighter = weighter
        self.lam = lam
        return

    def getLength(self, doc):
        words = self.weighter.getDocWeightsForDoc(doc)
        length = 0
        for (k, v) in words.iteritems():
            length += v
        return length

    def generate_Pmc(self, query):
        # get tf for each stem in all corpus
        query = self.weighter.getWeightsForQuery(query)
        # query is the term frequency of query
        docs_with_query_count = dict()
        for each_stem in query:
            sum_count = 0.
            docs = self.weighter.getDocWeightsForStem(each_stem)
            for v in docs.values():
                sum += v
            docs_with_query_count[each_stem] = sum_count
        # get length of the whole corpus
        length_of_document = dict()
        length_of_corpus = 0
        for k in self.weighter.index.doc:
            length_of_document[k] = self.getLength(k)
            length_of_corpus += length_of_document[k]
        return docs_with_query_count, length_of_document,length_of_corpus




    def getScores(self,query):
        query = self.weighter.getWeightsForQuery()
        scores = dict()
        docs_with_query_count, length_of_document, length_of_corpus= self.generate_Pmc(query)
        for each_stem in query.keys():
            for doc in self.weighter.getDocWeightsForStem(each_stem):
                scores[doc] = 0.0
        # get the id of all the documents that we need to compute
        for each_stem in query.keys():
            weight_stem = query[each_stem]
            docs = self.weighter.getDocWeightsForStem(each_stem)
            if docs == None:
                continue
            # never appears
            for (k, v) in scores.iteritems():
                # normal case
                docs = dict()
                pmd = 0.0
                pmc = docs_with_query_count[each_stem] / (1. * length_of_corpus)
                if docs != None and docs.has_key(k):
                    pmd = docs[k] / (length_of_document[k] * 1.)
                scores[k] = v + query[each_stem] * math.log(self.lam * pmd + (1 - self.lam)* pmc)
        return scores

    def getRanking(self, query):
        scores = self.getScores(query)
        sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
        sorted_scores.reverse()
        return sorted_scores
