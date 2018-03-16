# Attempts to predict whether comments will have a reply that states "Yes." based
# on the parent comment's language, using a manually trained set of comments.
# I am not very experienced with NLTK, so this is not very good at classifying.
# Additionally, the sample size/training set are too small, further hindering this
# from being of any use.

#################################
# TODO:
# 1. Setup error analysis
# 	- use mistakes made by the classifier to improve itself (this sounds like machine learning)
# 2. Get a larger sample size
# 3. Get a larger training set (requires completing #2)
#	- http://www.nltk.org/book/ch06.html#error_analysis_index_term

import nltk, random, string, re
import pandas as pd
from nltk.classify import apply_features

table = str.maketrans({key: None for key in string.punctuation})

re_question = re.compile(r"^.(?=(?:.+?\?)).*$", re.M).search
re_or = re.compile(r"^.(?=(?:.*\sor\s)).*$", re.I | re.M).search
re_and_which = re.compile(r"^.* and (?=.* which ).*$", re.I | re.M).search
re_how_and = re.compile(r"^.(?=(?:.*\show\s.*\sand\s)).*$", re.I | re.M).search

# https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
def stripped(s):
    return s.translate(table)

def match_features(comment):
	comment_words = set(stripped(comment).split())
	features = {}
	features["has_or"] = bool(re_or(comment))
	features["has_question"] = bool(re_question(comment))
	#print(features["has_or"])
	#features["and&which"] = bool(re_and_which(comment))
	#features["how&and"] = bool(re_how_and(comment))
	features["post_length"] = len(comment)
	for word in word_features:
		features['contains({})'.format(word)] = (word in comment_words)
	return features

df1 = pd.read_excel("assets/excel/comment_data.xlsx", "Sheet1", converters={'Matched': bool})
# df1.dropna(axis=0, how='any', inplace=True)

# not sure the following 3 items are still needed..
# cols = ['Body', 'Matched']
# df3 = df1[cols]
# comment_matches = {k:v for k,v in  zip(df3.index,df3.to_dict('records'))}

all_comments = df1['Body'].tolist()

bool_list = df1['Matched'].tolist()

labeled_comments = list(zip(all_comments, bool_list))

# https://stackoverflow.com/questions/31845482/iterating-through-a-string-word-by-word
x = (' '.join(all_comments)).split()
all_words = nltk.FreqDist(word.lower() for word in x)

word_features = list(all_words)[:2000]

size = int(len(labeled_comments)*0.9)
train_comments = labeled_comments[:size]
test_comments = labeled_comments[size:]

train_set = apply_features(match_features, train_comments)
test_set = apply_features(match_features, test_comments)

# full_set = apply_features(match_features, labeled_comments)
# classifier = nltk.NaiveBayesClassifier.train(full_set)

classifier = nltk.NaiveBayesClassifier.train(train_set)

print(nltk.classify.accuracy(classifier, test_set))

classifier.show_most_informative_features(15)
