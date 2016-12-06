from  models.IRmodel import *
class RandomModel(IRmodel):
    def __init__(self, sub_model, random_walker, n, k):
        # the parameters for the models
        self.n = n
        self.k = k
        self.sub_model = sub_model
        self.random_walker = random_walker
        self.successors = self.random_walker.index.getSuccessors()
        self.presuccessors = self.random_walker.index.getPresuccessors()
        return

    def getScores(self,query):
        # work with vector model
        scores = self.sub_model.getScores(query, False)
        #initial seeds
        seeds = set()
        count = 0
        for each in scores.keys():
            if count < self.n:
                count += 1
                seeds.add(each)

        # add all the documents pointed by d
        v = set()
        for each in seeds:
            v.add(each)
            v.union(self.successors[each])
            count = 0
            for parent in self.presuccessors[each] :
                if parent not in v and count < self.k:
                    v.add(parent)
        # regreante its successors and presuccessors
        v_successors = dict()
        v_presucessors = dict()
        for each in v:
            v_successors[each] = v.intersection(self.successors[each])
            v_presucessors[each] = v.intersection(self.presuccessors[each])
        # get sub graph
        u = self.random_walker.compute(v_successors, v_presucessors)
        for (i, key) in enumerate(v_successors.keys()):
            if key not in seeds:
                continue
            scores[key] = u[i]
        return scores

    def getRanking(self, query):
        scores = self.getScores(query)
        sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
        sorted_scores.reverse()
        return sorted_scores