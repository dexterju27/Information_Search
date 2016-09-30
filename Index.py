from TextRepresenter import PorterStemmer
from ParserCACM import ParserCACM
class Content:
    def __init__(self, position, length):
        self.position = position
        self.length = length


class Index:
    def __init__(self, name):
        self.name = name
        self.doc = dict()
        self.stems = dict()
        self.parser = ParserCACM()
        self.PorterStemmer = PorterStemmer()

    def readImputFile(self, input, output):
        self.parser(file)
        self.parser.initFile('cacm/cacm.txt')
        doc = self.parser.nextDocument()
        offsetIndex = 0
        offsetInverted = 0
        fIndex = open(output + self.name +'_index.txt', 'w+')
        fIndexInv = open(output + self.name + '_inverted.txt', 'w+')
        while doc:
            text = self.stems.getTextRepresentation(doc.getText())
            id = doc.getId()
            self.doc[id] = Content()







