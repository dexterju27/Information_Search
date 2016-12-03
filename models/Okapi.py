from IRmodel import *
class Okapi(IRmodel):
    # requre a idf weighter for query while a tf weighter for
    def __init__(self, weighter,k1, b):
        # the parameters for the models
        self.weighter = weighter
        self.k1 = k1
        self.b = b
        self.length_of_document, self.average_length, self.N = self.get_average_length()
        return

    def setParams(self, k1, b):
        self.k1 = k1
        self.b = b
        return

    def getLength(self, doc):
        words = self.weighter.getDocWeightsForDoc(doc)
        length = 0
        for (k, v) in words.iteritems():
            length += v
        return length

    def get_average_length(self):
        # get tf for each stem in all corpus
        length_of_document = dict()
        length_of_corpus = 0
        count = 0
        for k in self.weighter.index.doc:
            length_of_document[k] = self.getLength(k)
            length_of_corpus += length_of_document[k]
            count+= 1
        average_length = length_of_corpus / (count * 1.)
        return length_of_document,average_length, count

    # N total number of documents,
    # dft number of documents contains dft
    def idf(self,dft):
        return max(0., math.log((self.N * 1. - dft + 0.5) / (dft + 0.5)))

    def getScores(self,query):
        # get the length of each document, average length of all documents and the number of all documents
        query = self.weighter.getWeightsForQuery(query)
        scores = dict()
        for each_stem in query.keys():
            docs = self.weighter.getDocWeightsForStem(each_stem)
            if docs is None:
                continue
            for doc in docs.keys():
                scores[doc] = 0.0
        # get the id of all the documents that we need to compute
        for each_stem in query.keys():
            docs = self.weighter.getDocWeightsForStem(each_stem)
            if docs is None:
                continue
            dft = len(docs)
            idf_prime = self.idf(dft)
            for (k, v) in docs.iteritems():
                scores[k] += idf_prime * (self.k1 + 1.) * 1. * v / (self.k1 * ((1. - self.b) + self.b * 1. * self.length_of_document[k]  / self.average_length) + docs[k])
        return scores

    def getRanking(self, query):
        scores = self.getScores(query)
        sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
        sorted_scores.reverse()
        return sorted_scores


