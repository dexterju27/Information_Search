import math
class Weighter:
    def __init__(self, index):
        self.index = index
        return
    def getDocWeightsForDoc(idDoc):
        return
    def  getDocWeightsForStem(stem):
        return
    def getWeightsForQuery(query):
        return

class WeighterVector1 (Weighter):
    def getDocWeightsForDoc(self, idDoc):
        return self.index.getTfsForDoc(idDoc)


    def getDocWeightsForStem(self, stem):
        return  self.index.getTfsForStem(stem)


    def getWeightsForQuery(self, query):
#       query is a list
        query_weight = dict()
        for each_word in query.keys():
            query_weight[each_word] = 1
        return  query_weight


class WeighterVector2(WeighterVector1):
    def getWeightsForQuery(self, query):
        return query


class WeighterVector3(WeighterVector1):
    def getWeightsForQuery(self, query):
        idf_query = dict()
        total_size = len(self.index.doc)
        for each_word in query.keys():
            res = self.index.getTfsForStem(each_word)
            size = 0
            if res != None:
                size = len(res)
            idf_query[each_word] = math.log((total_size + 1.0) / (1.0 + size) , 2)
        return idf_query

class  WeighterVector4(WeighterVector3):
    def getDocWeightsForDoc(self, idDoc):
        result = self.index.getTfsForDoc(idDoc)
        for (k, v) in result.iteritems():
            result[k] = 1. + math.log(v, 2.)
        return result

    def getDocWeightsForStem(self, stem):
        result = self.index.getTfsForStem(stem)
        if result == None:
            return None
        for (k, v) in result.iteritems():
            result[k] = 1. + math.log(v, 2.)
        return result

class WeighterVector5(Weighter):
    def getWeightsForQuery(self, query):
        idf_query = dict()
        total_size = len(self.index.doc)
        for each_word in query.keys():
            size = 0
            res = self.index.getTfsForStem(each_word)
            if res != None:
                size = len(res)
            idf_query[each_word] = math.log((total_size + 1.0) / (1.0 + size ), 2)
            idf_query[each_word] *= (1.0 + math.log(query[each_word], 2))
        return idf_query

    def getDocWeightsForDoc(self, idDoc):
        total_size = len(self.index.doc)
        result = self.index.getTfsForDoc(idDoc)
        if result == None:
            return None
        for (k, v) in result.iteritems():
            result[k] = math.log((total_size + 1.0) / (1.0 + len(self.index.getTfsForStem(k))), 2)
            result[k] *= (1.0 + math.log(v, 2))
        return result


    def getDocWeightsForStem(self, stem):
        total_size = len(self.index.doc)
        result = self.index.getTfsForStem(stem)
        if result == None:
            return None
        for (k, v) in result.iteritems():
            result[k] = math.log((total_size + 1.0) / (1.0 + len(self.index.getTfsForStem(stem))), 2)
            result[k] *= (1.0 + math.log(v, 2))
        return result










