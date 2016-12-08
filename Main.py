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
from Index import *
from QueryParser import *
from evaluation.EvalMeasure import *
from models.IRmodel import  *
from models.Weighter import  *
from models.LanguageModel import *
from models.Okapi import  *
import numpy as np
from evaluation.GridSearch import *
from models.RandomModel import *
from collection.PageRank import *
from collection.Hits import *
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import sys
from pylab import *
from features.FeatureIRmodel import *
from features.FeatureList import *
from models.MetaModelLinear import *
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
    lams = np.linspace(0, 0.99, 5)
    for lam in lams:
        models.append(LanguageModel(weighter1, lam))
    search = GridSearch(models, irlists, 10)
    print (search.optimisation())
    return


def test7(irlists, index):
    weighter1 = WeighterVector1(index)
    models = []
    page_rank = PageRank(0.1, 100, index)
    random_model = RandomModel(IRmodelVector(weighter1), page_rank, 10, 10)
    models.append(IRmodelVector(weighter1))
    models.append(random_model)
    eval = EvalIRModel(models, irlists, 10)
    scores_mean, scores_std = eval.evalModels()
    return scores_mean, scores_std


def test8(irlists, index):
    weighter1 = WeighterVector1(index)
    models = []
    hits = Hits(100, index)
    random_model = RandomModel(IRmodelVector(weighter1), hits, 10, 10, )
    models.append(IRmodelVector(weighter1))
    models.append(random_model)
    eval = EvalIRModel(models, irlists, 10)
    scores_mean, scores_std = eval.evalModels()
    return scores_mean, scores_std
# scores, scores_std = test4(irlists, index)
# the best parameters are 0.2475
weighter1 = WeighterVector1(index)
weighter2 = WeighterVector2(index)
weighter3 = WeighterVector3(index)
weighter4 = WeighterVector4(index)
weighter5 = WeighterVector5(index)

features = Fearurelist()
features.addFeature(FeatureVectormodel(IRmodelVector(weighter1)))
features.addFeature(FeatureVectormodel(IRmodelVector(weighter2)))
features.addFeature(FeatureVectormodel(IRmodelVector(weighter3)))
# features.addFeature(FeatureVectormodel(IRmodelVector(weighter4)))
# features.addFeature(FeatureVectormodel(IRmodelVector(weighter5)))
meta_model = MetaModelLinear(index, features, 0.001, 0.001, 20, 3)
meta_model.trainModel(irlists)
models = []
models.append(meta_model)
models.append(IRmodelVector(weighter1))
models.append(IRmodelVector(weighter2))
models.append(IRmodelVector(weighter3))
eval = EvalIRModel(models, irlists, 20)
scores_mean_m, scores_std_m = eval.evalModels()
pdb.set_trace()