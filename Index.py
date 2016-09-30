from TextRepresenter import PorterStemmer
from ParserCACM import ParserCACM
import os
import pdb
class Content(object):
    def __init__(self, position, length):
        self.position = position
        self.length = length

class Index (object):
    def __init__(self, name):
        self.name = name
        self.doc = dict()
        self.stems = dict()
        self.parser = ParserCACM()
        self.PorterStemmer = PorterStemmer()
        self.docFrom = dict()
        self.input = ''
        self.output = ''

    def indexation(self, input, output):
        self.input = input
        self.output = output
        if not os.path.exists(output):
            os.makedirs(output)
        self.parser.initFile(input)
        doc = self.parser.nextDocument()
        statisticInversed = dict()
        offsetIndex = 0
        offsetInverted = 0
        offsetDoc = 0
        fIndex = open(output + self.name +'_index.txt', 'w+')
        fIndexInv = open(output + self.name + '_inverted.txt', 'w+')
        while doc:
            statistic = self.PorterStemmer.getTextRepresentation(doc.getText())
            text = str(statistic)
            id = doc.getId()
            # docFrom
            self.docFrom[id] = Content(offsetDoc,len(doc.getText()))
            offsetDoc = offsetDoc + self.docFrom[id].length - 1

            # Generate inverse statistic
            for eachStem in statistic.keys():
                if statisticInversed.has_key(eachStem):
                    statisticInversed[eachStem].append(id)
                else:
                    statisticInversed[eachStem] = [id]
            # output index
            self.doc[id] = Content(offsetIndex, len(text))
            fIndex.seek(offsetIndex)
            fIndex.write(text)
            offsetIndex = offsetIndex + self.doc[id].length - 1
            doc = self.parser.nextDocument()
        fIndex.close()
        # pdb.set_trace()
        # Generte output file
        for eachStem in statisticInversed.keys():
            text = str(statisticInversed[eachStem])
            self.stems[eachStem] = Content(offsetInverted, len(text))
            fIndexInv.seek(offsetInverted)
            fIndexInv.write(text)
            offsetInverted = offsetInverted + self.stems[eachStem].length - 1
        fIndexInv.close()

    def getTfsForFoc(self, id):
        if self.doc.has_key(id):
            content = self.doc[id]
            fIndex = open(self.output + self.name + '_index.txt', 'r')
            fIndex.seek(content.position)
            text = fIndex.read(content.length)
            fIndex.close()
            return text
        else:
            return None

    def getTfsForStem(self, stem):
        if self.stems.has_key(stem):
            content = self.doc[stem]
            fIndexInv = open(self.output + self.name + '_inverted.txt', 'r')
            fIndexInv.seek(content.position)
            text = fIndexInv.read(content.length)
            fIndexInv.close()
            return text
        else:
            return None

    def getStrDoc(self, id):
        if self.docFrom.has_key(id):
            content = self.doc[id]
            source = open(self.input, 'r')
            source.seek(content.position)
            text = source.read(content.length)
            source.close()
            return text
        else:
            return None






