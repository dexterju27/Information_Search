class Feature:
    def __init__(self, index):
        # type: (Index) -> object
        self.index = index
        self.scores = dict()

    def getFeatures(self, idDoc, query):
        return