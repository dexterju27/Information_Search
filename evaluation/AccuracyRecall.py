from evaluation.EvalMeasure import *


class AccuracyRecall(EvalMeasure):
    def __init__(self, nbLevels):
        self.nbLevels = nbLevels
        return

    def CalPrecisionRecall(self, l):
        # query_id = l.query.identifier
        # query_file = l.query.get('from').split('.')[0] + '.rel'
        # f_rel = open(query_file, 'r')
        precision = []
        recall = []
        pertinent_docs = set()
        # record the pertinent doc ids
        # res = f_rel.readline()
        # while (len(res) != 0):
        #     qry_id, doc_id, _, _ = res.split()
        #     if int(qry_id) == int(query_id):
        #         pertinent_docs.append(doc_id)
        # #     res = f_rel.readline()
        # # f_rel.close()
        # s = set()
        # number_correct = 0
        # scores = dict()
        # index = 0
        # if l.list == None:
        #     scores[0] = 0
        #     return scores
        for each in l.query.relevants:
            pertinent_docs.add(each[0])
        # number_all_doc = len(s)

        # no pertinent doc
        if len(pertinent_docs) == 0:
            return -1, -1, -1

        # for every top k results in l.score_list, calculate precition and recall
        nb_pertinent_docs = 0.
        pertinent_idx_in_precision = []
        for i in range(len(l.list)):
            doc_score_pair = l.list[i]
            doc_id = doc_score_pair[0]
            if doc_id in pertinent_docs:
                nb_pertinent_docs += 1
                pertinent_idx_in_precision.append(i)
            recall.append(nb_pertinent_docs / len(pertinent_docs))
            precision.append(nb_pertinent_docs / (i + 1))
        return precision, recall, pertinent_idx_in_precision


    def eval(self, l):
        nbLevels = self.nbLevels
        precision, recall, _ = self.CalPrecisionRecall(l)
        if precision == -1: #no pertinent doc in the corpus
            return None;
        #calculate the interpolate precisions
        k_levels = np.linspace(0, 1, nbLevels)
        precision_k = np.zeros(nbLevels)

        max_precision = 0
        current_level = nbLevels - 1
        for i in range(len(recall)):
            if recall[-i-1] < k_levels[current_level]:
                precision_k[current_level] = max_precision
                current_level -= 1
                if current_level == 0:
                    max_precision = max(max(precision[:-i]), max_precision)
                    precision_k[0] = max_precision
                    return precision_k
            max_precision = max(precision[-i-1], max_precision)
        for i in range(current_level+1):
            precision_k[i] = max_precision
        return precision_k

    def eval_1(self, l):
        nbLevels = self.nbLevels
        s = set()
        number_correct = 0
        scores = dict()
        recall_array = []
        precision_array = []
        index = 0
        if l.list == None:
            return None
        for each in l.query.relevants:
            s.add(each[0])
        number_all_doc = len(s)
        for doc, score in l.list:
            if index >= self.nbLevels:
                break
            if doc in s:
                number_correct += 1
            precision = number_correct * 1. / (index + 1.)
            rappel = number_correct * 1. / number_all_doc * 1.
            recall_array.append(rappel)
            precision_array.append(precision)
            index += 1
        levels = np.linspace(0, 1, nbLevels)
        precision =  np.zeros(nbLevels)

        max_precision = 0
        current_level = nbLevels - 1
        for i in range(len(recall_array)):
            if recall_array[-i-1] < levels[current_level]:
                precision[current_level] = max_precision
                current_level -= 1
                if current_level == 0:
                    max_precision = max(max(precision_array[:-i]), max_precision)
                    precision[0] = max_precision
                    return precision
            max_precision = max(precision_array[-i-1], max_precision)
        for i in range(current_level+1):
            precision[i] = max_precision
            return precision




