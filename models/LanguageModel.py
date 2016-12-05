from IRmodel import *
from QueryParser import QueryParser
from Weighter import *
from evaluation.EvalMeasure import *


class LanguageModel(IRmodel):
    # 1-gram language model
    def __init__(self, weighter, lam):
        self.weighter = weighter
        self.lam = lam
        return

    def setParams(self, lam):
        self.lam = lam
        return

    def getParams(self):
        return self.lam

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
            if docs is not None:
                for v in docs.values():
                    sum_count += v
            docs_with_query_count[each_stem] = sum_count
        # get length of the whole corpus
        length_of_document = dict()
        length_of_corpus = 0
        for k in self.weighter.index.doc:
            length_of_document[k] = self.getLength(k)
            length_of_corpus += length_of_document[k]
        return docs_with_query_count, length_of_document,length_of_corpus


    def getScores(self,query):
        query = self.weighter.getWeightsForQuery(query)
        scores = dict()
        docs_with_query_count, length_of_document, length_of_corpus= self.generate_Pmc(query)
        for each_stem in query.keys():
            docs = self.weighter.getDocWeightsForStem(each_stem)
            if docs is None:
                continue
            for doc in docs.keys():
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
                # docs = dict()
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


if __name__ == '__main__':
    index = Index("text")
    index.indexation('../cacm/cacm.txt', '../test/')
    weighter1 = WeighterVector1(index)
    models = []
    models.append(LanguageModel(weighter1))


    parser = QueryParser()
    parser.initFile('cacm/cacm.qry', 'cacm/cacm.rel')

    irlists = []
    query = parser.nextQuery()
    while query != None:
        irlists.append(IRList(query))
        query = parser.nextQuery()

    eval = EvalIRModel(models, irlists, 10)
    scores_mean, scores_std = eval.evalModels()
