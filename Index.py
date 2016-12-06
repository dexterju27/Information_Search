from TextRepresenter import PorterStemmer
from ParserCACM import ParserCACM
import os
from tokenize import tokenize
import pdb
import copy
import ast


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
        self.successuers = {}
        self.presuccessors = {}

    def indexation(self, input, output):
        self.input = input
        self.output = output
        if not os.path.exists(output):
            os.makedirs(output)
        self.parser.initFile(input)
        doc = self.parser.nextDocument()
        statisticInversed = dict()
        offsetIndex = 0
        offsetDoc = 0
        fIndex = open(output + self.name +'_index.txt', 'w+')
        fIndexInv = open(output + self.name + '_inverted.txt', 'w+')
        while doc:
            statistic = self.PorterStemmer.getTextRepresentation(doc.getText())

            text = str(statistic)
            id = doc.getId()
            id = int(id)
            # print id
            # docFrom
            f = doc.get("from").split(';')
            self.docFrom[id] = Content(int(f[1]),int(f[2]))
            # Generate inverse statistic
            # first loop
            for eachStem in statistic.keys():
                inv = str(id) + ':' + str(statistic[eachStem]) + ','
                size = len(inv)
                if self.stems.has_key(eachStem):
                    self.stems[eachStem].length = self.stems[eachStem].length + size
                else:
                    self.stems[eachStem] = Content(-1, size)
            # output index
            self.doc[id] = Content(offsetIndex, len(text))
            fIndex.seek(offsetIndex)
            fIndex.write(text)
            offsetIndex = offsetIndex + self.doc[id].length
            doc = self.parser.nextDocument()
        fIndex.close()
        # # Generate output of inverted index file
        # second loop
        offsetInverted = 0
        # pdb.set_trace()
        for k, v in self.stems.iteritems():
            v.position = offsetInverted
            offsetInverted += v.length

        self.parser.initFile(input)
        doc = self.parser.nextDocument()

        tempPosition = copy.deepcopy(self.stems)
        while doc:
            statistic = self.PorterStemmer.getTextRepresentation(doc.getText())
            id = doc.getId()
            id = int(id)
            for eachStem in statistic.keys():
                inv = str(id) + ':' + str(statistic[eachStem]) + ','
                fIndexInv.seek(tempPosition[eachStem].position)
                fIndexInv.write(inv)
                tempPosition[eachStem].position += len(inv)
            # generate successors and presuccessors
            id = doc.getId()
            id = int(id)
            self.successuers[id] = set()
            if id not in self.presuccessors:
                self.presuccessors[id] = set()
            if doc.get('links') != '':
                for eachDoc in doc.get('links').split(";"):
                    # check if the id is valid
                    if eachDoc.isdigit():
                        id_eachDoc = int(eachDoc)
                        self.successuers[id].add(id_eachDoc)
                        if not self.presuccessors.has_key(id_eachDoc):
                            self.presuccessors[id_eachDoc] = set()
                        self.presuccessors[id_eachDoc].add(id)
            doc = self.parser.nextDocument()
        fIndexInv.close()
        # pdb.set_trace()



    def getTfsForDoc(self, id):
        if self.doc.has_key(id):
            content = self.doc[id]
            fIndex = open(self.output + self.name + '_index.txt', 'r')
            fIndex.seek(content.position)
            text = fIndex.read(content.length)
            fIndex.close()
            tfs4Doc = ast.literal_eval(text)
            return tfs4Doc
        else:
            return None

    def getTfsForStem(self, stem):
        if self.stems.has_key(stem):
            content = self.stems[stem]
            fIndexInv = open(self.output + self.name + '_inverted.txt', 'r')
            fIndexInv.seek(content.position)
            text = fIndexInv.read(content.length)
            fIndexInv.close()
            tfs4stem = dict()
            for each in text.split(','):
                if type(each) is not str:
                    continue
                if len(each) < 3:
                    continue
                tuple = each.split(':')
                tfs4stem[int(tuple[0])] = int(tuple[1])
            return tfs4stem
        else:
            return None

    def getStrDoc(self, id):
        if self.docFrom.has_key(id):
            content = self.docFrom[id]
            source = open(self.input, 'r')
            source.seek(content.position)
            text = source.read(content.length)
            source.close()
            return text
        else:
            return None

    def getSuccessors(self):
        return self.successuers

    def getPresuccessors(self):
        return self.presuccessors




