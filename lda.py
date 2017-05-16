from __future__ import print_function
from time import time
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

n_samples = 2000
n_features = 1000
n_topics = 3
n_top_words = 20


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


def load_data_dir(data_dir_path):
    print("Loading dataset...")
    t0 = time()
    data_samples = []
    data_file_list = list((os.walk(data_dir_path)))[0][2]
    for item in data_file_list:
        with open(data_dir_path + "%s" % item, 'r') as f:
            data_list = f.readlines()
            data_file = "".join(data_list)
        data_samples.append(data_file)
    print("done in %0.3fs." % (time() - t0))
    return data_samples


def load_data_file(data_file_path):
    print("Loading dataset...")
    t0 = time()
    data_file = []
    with open(data_file_path, 'r') as f:
        data_list = f.readlines()
        data_file.append(data_list)
    print("done in %0.3fs." % (time() - t0))
    return data_file


def tf_lda(data):
    # Use tf (raw term count) features for LDA.
    print("Extracting tf features for LDA...")
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                    max_features=n_features)
    print("tf_vectorizer:")
    print(tf_vectorizer)

    t0 = time()

    tf = tf_vectorizer.fit_transform(data)
    print("tf(tf_vectorizer_transform)")
    print(tf)

    print("done in %0.3fs." % (time() - t0))
    print("Fitting LDA models with tf features, "
          "n_samples=%d and n_features=%d..."
          % (n_samples, n_features))
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    t0 = time()
    lda.fit(tf)
    print("done in %0.3fs." % (time() - t0))

    print("\nTopics in LDA model:")
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)

if __name__ == '__main__':
    data_set = load_data_dir("data\\6\\")
    # data_set = load_data_file("data\\1\\1.txt-1.txt")
    tf_lda(data_set)
