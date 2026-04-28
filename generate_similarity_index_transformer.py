import pickle

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MOVIES_PKL = "movies.pkl"
OUTPUT_FILE = "similarity_index_transformer.pkl"


def load_movie_tags(path):
    movies = pickle.load(open(path, "rb"))
    tags = movies.get("tags") if isinstance(movies, dict) else movies["tags"]
    return [str(tag) if tag is not None else "" for tag in tags]


def build_similarity_matrix(texts, model_name=MODEL_NAME):
    model = SentenceTransformer(model_name, device="cpu")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    similarity_matrix = cosine_similarity(embeddings)
    return similarity_matrix


def main():
    print(f"Loading movie tags from {MOVIES_PKL}...")
    texts = load_movie_tags(MOVIES_PKL)
    print(f"Encoding {len(texts)} movie tag texts with {MODEL_NAME}...")
    similarity_matrix = build_similarity_matrix(texts)
    print(f"Saving transformer similarity matrix to {OUTPUT_FILE}...")
    pickle.dump(similarity_matrix, open(OUTPUT_FILE, "wb"))
    print("Done.")


if __name__ == "__main__":
    main()
