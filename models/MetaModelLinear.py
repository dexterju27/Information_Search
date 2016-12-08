from models.MetaModel import *
import numpy as np
from evaluation.EvalMeasure import *
import random
import pdb

class MetaModelLinear(MetaModel):
    def __init__(self, index, FeaturersList, alpha, lam, maxIter, n):
        self.FeaturersList = FeaturersList
        self.theta = np.ones([n , 1])
        self.alpha = alpha
        self.lam = lam
        self.index = index
        self.maxIter = maxIter
        self.n = n
        return

    def trainModel(self, irLists):
        loss = 0.
        #  random choose a query
        l = random.choice(irLists)
        if len(l.query.relevants) != 0 and len(l.query.relevants) != len(self.index.doc):
            s = set()
            for each in l.query.relevants:
                s.add(each[0])
            accuracy_doc = random.choice(tuple(s))
            non_accuracy_doc = random.choice(self.index.doc.keys())
            while non_accuracy_doc in s:
                non_accuracy_doc = random.choice(self.index.doc.keys())
            # find the two docs
            accuracy_doc_feature = np.array(self.FeaturersList.getFeatures(accuracy_doc, l.query.text)).reshape([1, self.n])
            non_accuracy_doc_feature = np.array(self.FeaturersList.getFeatures(non_accuracy_doc, l.query.text)).reshape([1, self.n])
            score_a = accuracy_doc_feature.dot(self.theta)
            score_na = non_accuracy_doc_feature.dot(self.theta)
            # pdb.set_trace()
            if (1. - score_a + score_na)  > 0:
                self.theta += self.alpha * (accuracy_doc_feature - non_accuracy_doc_feature).T
            self.theta = (1. - 2.* self.alpha * self.lam) * self.theta

    def getScores(self, query):
        scores = dict()
        for idDoc in self.index.doc:
            features = np.array(self.FeaturersList.getFeatures(idDoc, query))
            scores[idDoc] = features.dot(self.theta)
        return scores

    def getRanking(self, query):
        scores = self.getScores(query)
        sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
        sorted_scores.reverse()
        return sorted_scores



