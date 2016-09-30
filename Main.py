from ParserCACM import ParserCACM
from TextRepresenter import PorterStemmer
parser = ParserCACM()
parser.initFile('cacm/cacm.txt')
stem = PorterStemmer()
doc = parser.nextDocument()
while doc:
    print (stem.getTextRepresentation(doc.getText()))
    doc = parser.nextDocument()