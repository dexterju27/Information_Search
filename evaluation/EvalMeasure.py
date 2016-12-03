from QueryParser import Query
import numpy as np
class IRList:
    def __init__(self, query):
        self.query = query
        self.list =  []

class EvalMeasure:
    def eval(l):
        return

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
            if index >= self.nbLevels or index >= len(l.query.relevants) :
                break
            if doc in s:
                number_correct += 1
            precision = number_correct * 1. / (index + 1.)
            rappel = number_correct * 1. / number_all_doc * 1.
            scores[rappel] = precision
            index += 1
        return scores

    def ap(self, l):
        scores = self.eval(l)
        score = 0.
        count = 0
        for (key, value) in scores.iteritems():
            score += value
            count += 1
        if count == 0:
            return 0.
        return score / count * 1.


class EvalIRModel:
    def __init__(self, models, irLists, nbLevels):
        self.models = models
        self.irLists = irLists
        self.nbLevels = nbLevels

    def evalModels(self):
        scores_mean = []
        socres_std  = []
        for model in self.models:
            print ("evaluation of the first model")
            score = []
            for l in self.irLists:
                l.list = model.getRanking(l.query.text)
                rater = PresitionRappel(self.nbLevels)
                score.append(rater.ap(l))
                print ("evaluation of querry is %f", score[-1])
            scores_mean.append(np.mean(score))
            socres_std.append(np.std(score))
        return scores_mean, socres_std







