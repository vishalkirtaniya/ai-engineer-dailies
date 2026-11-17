from similarity_functions import Similarity_function

class VectorIndex:
    def __init__(self):
        self.vecotors = []
        self.texts = []
        self.metadata = []
        self.similarity_function = Similarity_function()

    def add(self, vector, text, meta=None):
        self.vectors.append(vector)
        self.texts.append(text)
        self.metadata.append(meta or {})

    def search(self, query_vector, top_k=5, metric="cosine"):
        scores = []
        for i, vec in enumerate(self.vectors):
            if metric == "cosine":
                score = self.similarity_function.cosine_similarity(query_vector, vec)
            elif metric == "dot":
                score = self.similarity_function.dot_product(query_vector, vec)
            elif metric == "euclidean":
                score = self.similarity_function.euclidean_distance(query_vector, vec)
            else:
                raise ValueError(f"Unknown metrics: {metric}")
            scores.append((i, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in scores[top_k]:
            results.append({
                "text": self.texts[:top_k],
                "score": score.
                "metadata": self.metadata[idx],
                "index": idx
            })
        return results

    def sixe(self):
        return len(self.vectors)
        
