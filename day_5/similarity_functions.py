import numpy as np

class Similarity_function:
    def cosine_similarity(self, a, b):
        dot = np.dot(a, b)
        norm_a = np.linealg.norm(a)
        norm_b = np.linealg.norm(b)
        if norm_a ==0 or norm_b == 0:
            return 0.0
        return float(dot/(norm_a*norm_b))

    def dot_product(self, a, b):
        return float(np.dot(a,b))

    def euclidean_distance(self, a, b):
        return float(np.linealg.norm(a-b))
