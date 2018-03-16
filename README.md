# downvote_bot

### Attempts to downvote any comment whose only contents are "Yes." or "Yes" (case insensitive)

#### This bot was inspired by my petpeeve of user's erroneously responding with "Yes". Example:

User 1: "Is the pen blue or red?"
User 2: "Yes"

It utilizes the [PRAW](https://praw.readthedocs.io/en/latest/) library to get information from Reddit and the [NLTK (Natural Language Toolkit)](http://www.nltk.org/) library (poorly) to analyze and attempt to predict whether the comment is a false positive or not

After downvoting the comment, it also attempts to record some information about the offender (username, subreddit, date), as well as some information about the parent comment (username, subreddit, comment body)

Information is recorded to/read from excel using the [Pandas](http://pandas.pydata.org/) library.

Currently, the main script attempts to predict whether the person is actually committing said pet peeve based on the language used in the parent comment using only regex. The prediction is recorded into excel under the "Proposed" collumn as boolean. This information is then used to train what is called a "classifier", one of NTLK's main features. In order for the classifier to be properly trained, it is required to manually enter whether or not the comment was in fact commiting said pet peeve under the "Actual" collumn in excel.

At present, the main issues are: 
- lack of sample size to train the classifier
- The method of training the classifier is very time consuming and seems innefficient 
- lack of familiarity with NLTK

A GUI for marking the comments as "TRUE" or "FALSE" would be helpful (regarding whether or not the comment commit's the petpeeve). Some simple program that shows each comment one at a time and then records the user's response ("TRUE" or "FALSE") into the "Actual" collumn -- for the purpose of building 

TODO: make the classifier learn from itself (this is likely possible, but would require a lot of time, effort, and research)

*Disclosure: I don't remember if this is in a working state, and don't have plans to work on it any time soon.*
