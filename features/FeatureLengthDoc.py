from features.Feature import *
class FeatureLengthDoc(Feature):
    def __init__(self, weighter):
        self.docLength = dict()
        self.weighter = weighter #weighter tf

    def getLength(self, doc):
        words = self.weighter.getDocWeightsForDoc(doc)
        length = 0
        for (k, v) in words.iteritems():
            length += v
        return length

    def getFeatures(self, idDoc, query):
        if not self.docLength.has_key(idDoc):
            self.docLength[idDoc] = self.getLength(idDoc)
        return self.docLength[idDoc]