import math
import operator

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
        query = self.weighter.getWeightsForQuery()
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
                sum_x = 0.
                xs  = self.weighter.getDocWeightsForDoc(k)
                for x in xs.value():
                    sum_x += x ** 2
                scores[k] = scores[k] / math.sqrt(sum_x * sum_y)
        return scores

    def getRanking(self, query):
        scores = self.getScores(query, False)
        sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
        sorted_scores.reverse()
        return sorted_scores



