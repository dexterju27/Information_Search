from features.Feature import *
class FeatureIdfSum(Feature):
    def __init__(self, weighter):
        self.IdfSum = dict()
        self.weighter = weighter #weighter idf

    def getIdfSum(self, doc):
        words = self.weighter.getDocWeightsForDoc(doc)
        length = 0
        for (k, v) in words.iteritems():
            length += v
        return length

    def getFeatures(self, idDoc, query):
        if not self.IdfSum.has_key(idDoc):
            self.IdfSum[idDoc] = self.getIdfSum(idDoc)
        return self.IdfSum[idDoc]