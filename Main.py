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
from Index import Index
import os
index = Index("text")
index.indexation('cacm/cacm.txt', './test/')

