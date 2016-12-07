import evaluation.EvalMeasure
from Index import *
from QueryParser import QueryParser
from evaluation.EvalMeasure import *
from models.IRmodel import  *
from models.Weighter import  *
from models.LanguageModel import *
from models.Okapi import  *
import numpy as np


class GridSearch(object):
    def __init__(self, models, irlists, nbLevel):
        self.models = models
        self.irlists = irlists
        self.nbLevel = nbLevel
        self.scores_mean = []
        self.scores_std = []

    def optimisation(self):
        eval = EvalIRModel(self.models, self.irlists,  self.nbLevel)
        self.scores_mean, self.scores_std = eval.evalModels()
        scores_mean = np.array(self.scores_mean)
        return self.models[scores_mean.argmax()].getParams()