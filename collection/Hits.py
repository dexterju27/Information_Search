from collection.RandomWalker import *
import numpy as np

class Hits(RandomWalker):
    def __init__(self, max_iter, index):
        # type: (Int) -> object
        self.max_iter = max_iter
        self.index = index
        return

    def compute(self, successuers, predecesseurs):
        N = len(successuers)
        # vector
        a = np.ones([N, 1])
        h = np.ones([N, 1])
        mapping_element_to_index = dict()
        i = 0
        for (i, each) in enumerate(successuers):
            mapping_element_to_index[each] = i
        mapping_index_to_element = successuers.keys()

        for l in range(self.max_iter):
            # for regularization
            #update a
            a_next = np.zeros([N, 1])
            h_next = np.zeros([N, 1])

            for (i, key) in enumerate(successuers):
                for parent in predecesseurs[key]:
                    j = mapping_element_to_index[parent]
                    a_next[i] +=  h[j]
                for child in successuers[key]:
                    j = mapping_element_to_index[child]
                    h_next[i] += a[j]
                if np.linalg.norm(a_next) == 0:
                    a = a_next
                else:
                    a = a_next / np.linalg.norm(a_next)
                if np.linalg.norm(h_next) == 0:
                    h = h_next
                else:
                    h = h_next / np.linalg.norm(h_next)
        return a
