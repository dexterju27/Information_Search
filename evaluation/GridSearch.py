import evaluation.EvalMeasure
from Index import *
from QueryParser import QueryParser
from evaluation.EvalMeasure import *
from models.IRmodel import  *
from models.Weighter import  *
from models.LanguageModel import *
from models.Okapi import  *


class GridSearch(object):
    def __init__(self, model, query, irlists, nbLevel):
        self.model = model
        self.query = query
        self.irlists = irlists
        self.nb

    def optimisation(self, listParametres):
        scoreMaxmal = 0
        meilleurParam = None
        for parametre in listParametres:
            eirm = EvalIRModel(self.queries, self.index, self.weighter, self.modelPrecision, self.model, parametre)
            mean, std = eirm.eval()
            # print mean
            if sum(mean) > scoreMaxmal:
                meilleurParam = parametre
                scoreMaxmal = sum(mean)

        print "Meilleur Parametre : " + str(meilleurParam)
        print "score : " + str(scoreMaxmal)

        return meilleurParam