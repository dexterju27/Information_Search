from features.Feature import *
class FeatureIRmodel(Feature):
    def __init__(self, model):
        # type: (Index) -> object
        self.model = model
        self.scores = dict()

    def getFeatures(self, idDoc, query):
        scores = self.model.getScores(query)
        if scores.has_key(idDoc):
            return scores[idDoc]
        else :
            return 0.


class FeatureVectormodel(FeatureIRmodel):
    def __init__(self, model):
        # type: (Index) -> object
        self.model = model
        self.scores = dict()

    def getFeatures(self, idDoc, query):
        scores = self.model.getScores(query,True)
        if scores.has_key(idDoc):
            return scores[idDoc]
        else :
            return 0.