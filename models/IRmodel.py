import math
import operator
import numpy as np

class IRmodel:
    def getScores(self,query):
    # input : tf of query
        return

    def getRanking(self, query):
        return


class IRmodelVector(IRmodel):
    def __init__(self, weighter):
        self.weighter = weighter
        return

    def getScores(self, query, normalized) :
        query = self.weighter.getWeightsForQuery(query)
        scores = dict()
        sum_y = 0.
        for each_stem in query.keys():
            weight_stem = query[each_stem]
            sum_y += weight_stem ** 2
            docs = self.weighter.getDocWeightsForStem(each_stem)
            # never appears
            if docs == None:
                continue
            for each_doc in docs:
                if (scores.has_key(each_doc)):
                    scores[each_doc] += docs[each_doc] * weight_stem
                else :
                    scores[each_doc] = docs[each_doc] * weight_stem
        if normalized:
            for k in scores.keys():
                xs  = self.weighter.getDocWeightsForDoc(k).values()
                scores[k] = scores[k] / (np.linalg.norm(xs) * np.linalg.norm(query.values()))
        return scores

    def getRanking(self, query):
        scores = self.getScores(query, False)
        sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
        sorted_scores.reverse()
        return sorted_scores



