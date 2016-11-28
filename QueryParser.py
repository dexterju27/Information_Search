import ParserCACM
from TextRepresenter import PorterStemmer

class Query:
    def __init__(self, id, text, relevants):
        self.id = id
        self.text = text
        self.relevants = relevants

class QueryParser():
# input: the .qry file
# output: the document reader, Quert object
    def __init__(self):
        self.parser =  ParserCACM.ParserCACM()
        self.r_file = None
        self.r_position = 0
        self.PorterStemmer = PorterStemmer()

    def initFile(self, input_file_qry, input_file_r):
        self.parser.initFile(input_file_qry)
        self.r_file = open(input_file_r, "rb")

    def nextQuery(self):
        docs = self.parser.nextDocument()
        if docs == None:
            return None
        relevants = []
        if self.r_file is None:
            return
        while True:
            self.r_file.seek(self.r_position)
            text = self.r_file.readline()
            id = int (docs.getId())
            if (text == None):
                break
            text = text.split()
            if len(text) < 3:
                return None
            if int(text[0]) == id:
                self.r_position = self.r_file.tell()
                item = tuple((int(text[1]) ,int(text[2]), int(text[3])))
                relevants.append(item)
            else:
                break
        query = Query(id, self.PorterStemmer.getTextRepresentation(docs.getText()), relevants)
        return query
