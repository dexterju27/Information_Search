import pdb

from collection.RandomWalker import *
import numpy as np
class PageRank(RandomWalker):
    def __init__(self, d, max_iter, index):
        self.d = d
        self.max_iter = max_iter
        self.index = index
        return

    def compute(self, successuers, predecesseurs):
        N = len(successuers)
        # vector
        u = np.ones([N, 1])
        u = u * 1. / N
        A = np.zeros([N, N])
        mapping_element_to_index = dict()
        i = 0
        for (i, each) in enumerate(successuers):
            mapping_element_to_index[each] = i
        mapping_index_to_element = successuers.keys()
        for i in range(N):
            for j in range(N):
                i_element = mapping_index_to_element[i]
                j_element = mapping_index_to_element[j]
                if j_element not in predecesseurs[i_element]:
                    continue
                l = len(successuers[j_element])
                A[i][j] = 1. / l
        # pdb.set_trace()
        for i in range(self.max_iter):
            u = (1. - self.d) / N * np.ones([N, 1]) + self.d * A.dot(u)
        return u

