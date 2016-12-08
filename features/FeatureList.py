from features.Feature import *
class Fearurelist:
    def __init__(self):
        self.features = list()

    def addFeature(self, feature):
        self.features.append(feature)

    def getFeatures(self, idDoc, query):
        features = list()
        for each in self.features:
            features.append(each.getFeatures(idDoc, query))
        return features


