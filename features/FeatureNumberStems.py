from features.Feature import *
class FeatureNumberStems(Feature):
    def __init__(self, weighter):
        self.weighter = weighter #weighter tf

    def getFeatures(self, idDoc, query):
        return len(self.weighter.getDocWeightsForDoc(idDoc))
