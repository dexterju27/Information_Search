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

from EvalMeasure import *
from Index import Index
from QueryParser import QueryParser
from models.IRmodel import  *
from models.Weighter import  *

index = Index("text")
index.indexation('cacm/cacm.txt', './test/')
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


parser = QueryParser()
parser.initFile('cacm/cacm.qry', 'cacm/cacm.rel')

irlists = []
query = parser.nextQuery()
while query != None:
    irlists.append(IRList(query))
    query = parser.nextQuery()

eval = EvalIRModel(models, irlists, 10)
scores_mean, scores_std = eval.evalModels()
pdb.set_trace()

