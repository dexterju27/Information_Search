from QueryParser import Query
import numpy as np
class IRList:
    def __init__(self, query):
        self.query = query
        self.list =  []

class EvalMeasure:
    def eval(l):
        return


class AP(EvalMeasure):
    def __init__(self, nbLevels):
        self.nbLevels = nbLevels


    def eval(self, l):
        result = []
        lengthDoc = len(l.list)
        number_correct = 0.0
        s = set()
        for each in l.query.relevants:
            s.add(each[0])
        nbr_relevants = len(s)

        if nbr_relevants == 0:
            if len(l.list) == 0:
                return 1.
            return 0.

        i = 0
        presision = 0.
        for doc, score in l.list:
            if i >= self.nbLevels:
                break
            if doc in s:
                number_correct += 1.
                pre = number_correct * 1.0 / (i + 1)
                presision += pre
            i += 1
        return presision / nbr_relevants


class PresitionRappel(EvalMeasure):
    def __init__(self, nbLevels):
        self.nbLevels = nbLevels

    def eval(self, l):
        s = set()
        number_correct = 0
        scores = dict()
        index = 0
        if l.list == None:
            scores[0] = 0
            return scores
        for each in l.query.relevants:
            s.add(each[0])
        number_all_doc = len(s)
        for doc, score  in l.list:
            if index >= self.nbLevels:
                break
            if doc in s:
                number_correct += 1
            precision = number_correct * 1. / (index + 1.)
            rappel = number_correct * 1. / number_all_doc * 1.
            scores[rappel] = precision
            index += 1
        return scores



class EvalIRModel:
    def __init__(self, models, irLists, nbLevels):
        self.models = models
        self.irLists = irLists
        self.nbLevels = nbLevels

    def evalModels(self):
        scores_mean = []
        socres_std  = []
        for model in self.models:
            score = []
            for l in self.irLists:
                l.list = model.getRanking(l.query.text)
                rater = AP(self.nbLevels)
                score.append(rater.eval(l))
            scores_mean.append(np.mean(score))
            socres_std.append(np.std(score))
        return scores_mean, socres_std







