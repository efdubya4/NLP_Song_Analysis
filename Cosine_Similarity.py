import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

def calculate_cosine_similarity(file1_path, file2_path, text_column):
    # Read CSV files
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)
    
    # Combine all text from the specified column into single strings
    text1 = ' '.join(df1[text_column].astype(str))
    text2 = ' '.join(df2[text_column].astype(str))
    
    # Tokenization
    X_list = word_tokenize(text1.lower())
    Y_list = word_tokenize(text2.lower())
    
    # Remove stopwords
    sw = stopwords.words('english')
    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}
    
    # Create vector
    rvector = X_set.union(Y_set)
    l1 = []
    l2 = []
    
    for w in rvector:
        if w in X_set: 
            l1.append(1)
        else: 
            l1.append(0)
        if w in Y_set: 
            l2.append(1)
        else: 
            l2.append(0)
    
    # Calculate cosine similarity
    c = sum(l1[i] * l2[i] for i in range(len(rvector)))
    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
    
    return cosine

# Example usage
if __name__ == "__main__":
    file1_path = "one_star_reviews_sample.csv"
    file2_path = "four_star_reviews_sample.csv"
    text_column = "Reviews"  # Replace with your column name
    
    try:
        similarity = calculate_cosine_similarity(file1_path, file2_path, text_column)
        print(f"Cosine similarity between the files: {similarity:.4f}")
    except FileNotFoundError:
        print("Error: One or both CSV files not found")
    except KeyError:
        print(f"Error: Column '{text_column}' not found in one or both CSV files")