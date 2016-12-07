from features.Feature import *
class FeatureLengthQuery(Feature):
    def __init__(self, weighter):
        self.weighter = weighter #weighter tf

    def getFeatures(self, idDoc, query):
        length = 0
        for (k, v) in self.weighter.getWeightsForQuery(query):
            length += v
        return length