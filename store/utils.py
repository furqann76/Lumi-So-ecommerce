from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Product
import numpy as np


def get_ai_related_products(current_product, top_n=4):
    all_products = list(Product.objects.exclude(id=current_product.id))

    # If there are no other products, return empty
    if not all_products:
        return []

    descriptions = [current_product.description] + [p.description for p in all_products]

    # Create TF-IDF matrix
    tfidf = TfidfVectorizer(stop_words="english").fit_transform(descriptions)

    # Compute cosine similarity between the current product and all others
    cosine_sim = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

    # Get top N similar products
    top_indices = np.argsort(cosine_sim)[::-1][:top_n]

    return [all_products[i] for i in top_indices]
