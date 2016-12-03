# from ParserCACM import ParserCACM
# from TextRepresenter import PorterStemmer
# parser = ParserCACM()
# parser.initFile('cacm/cacm.txt')
# stem = PorterStemmer()
# doc = parser.nextDocument()
# while doc:
#     text = stem.getTextRepresentation(doc.getText())
#     # doc = parser.nextDocument()
#     text.
import pdb

from Index import *
from QueryParser import QueryParser
from evaluation.EvalMeasure import *
from models.IRmodel import  *
from models.Weighter import  *
from models.LanguageModel import *
from models.Okapi import  *
import numpy as np
from evaluation.GridSearch import *

index = Index("text")
index.indexation('cacm/cacm.txt', './test/')
parser = QueryParser()
parser.initFile('cacm/cacm.qry', 'cacm/cacm.rel')
irlists = []
query = parser.nextQuery()
while query != None:
    irlists.append(IRList(query))
    query = parser.nextQuery()


def test1_3(irlists, index):
    weighter1 = WeighterVector1(index)
    weighter2 = WeighterVector2(index)
    weighter3 = WeighterVector3(index)
    weighter4 = WeighterVector4(index)
    weighter5 = WeighterVector5(index)
    models = []
    models.append(IRmodelVector(weighter1))
    models.append(IRmodelVector(weighter2))
    models.append(IRmodelVector(weighter3))
    models.append(IRmodelVector(weighter4))
    models.append(IRmodelVector(weighter5))


    # parser = QueryParser()
    # parser.initFile('cacm/cacm.qry', 'cacm/cacm.rel')
    #
    # irlists = []
    # query = parser.nextQuery()
    # while query != None:
    #     irlists.append(IRList(query))
    #     query = parser.nextQuery()

    eval = EvalIRModel(models, irlists, 10)
    scores_mean, scores_std = eval.evalModels()
    return scores_mean, scores_std


def test4(irlists, index):
    weighter1 = WeighterVector1(index)
    models = []
    models.append(LanguageModel(weighter1, 0.1))
    eval = EvalIRModel(models, irlists, 10)
    scores_mean, scores_std = eval.evalModels()
    return scores_mean, scores_std

def test5(irlists, index):
    weighter1 = WeighterVector1(index)
    models = []
    models.append(Okapi(weighter1, 1.5 ,0.75))
    eval = EvalIRModel(models, irlists, 10)
    scores_mean, scores_std = eval.evalModels()
    return scores_mean, scores_std

def test6(irlists, index):
    weighter1 = WeighterVector1(index)
    models = []
    lams = np.linspace(0, 1, 10)
    for lam in lams:
        models.append(LanguageModel(weighter1, lam))
    search = GridSearch(models, irlists, 10)
    search.optimisation()
    return

test6(irlists, index)
pdb.set_trace()