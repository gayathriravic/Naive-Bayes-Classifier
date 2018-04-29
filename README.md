# Naive-Bayes-Classifier

Deveoped a Naive Bayes classifier to identify hotel reviews and classify them as either True/Fake and Positive/Negative.
I used word tokens as features for classification and treated it as 4-class single classification problem.
nblearn3.py will learn a naive Bayes model from the training data, and nbclassify3.py will use the model to classify new data.

### Smoothing and Unknown Tokens: 
```
The classifier uses add-one smoothing on the training data, and will simply ignore unknown tokens in the test data.

```

### Tokenization: 

```
Mapped punctuations to space and lowercased all the letters.
Ignored stop words.
```
