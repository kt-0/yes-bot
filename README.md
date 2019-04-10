# downvote_bot

### Attempts to downvote any comment whose only contents are "Yes." or "Yes" (case insensitive)

User 1: "Is the pen blue or red?"
User 2: "Yes"

Uses [PRAW](https://praw.readthedocs.io/en/latest/) to pull information from Reddit and the [NLTK (Natural Language Toolkit)](http://www.nltk.org/) library (poorly) to analyze and attempt to predict whether the comment is a false positive or not

After downvoting the comment (not supposed to do this), it also attempts to record some information about the offender (username, subreddit, date), as well as some information about the parent comment (username, subreddit, comment body)

Information is recorded to/read from excel using the [Pandas](http://pandas.pydata.org/) library.

Currently, the main script uses regex in an attempt to predict whether the comment is violating. The prediction is recorded into excel under the "Proposed" column. This is needed to train a classifier, which is something NLTK uses to make predictions(paraphrasing(badly*)). A decent sample size is needed to properly train said classifier.

*Disclosure: probably doesn't even work*
