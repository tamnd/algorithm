---
tag: 6EK8VP
kind: problem
slug: sentiment-analysis
name: Sentiment analysis
aliases:
- opinion mining
- sentiment classification
area: natural-language-and-speech/tagging-and-information-extraction
level: intro
summary: "Decide whether a text, sentence or aspect expresses a positive, negative or neutral opinion, or score its polarity."
prereqs: [naive-bayes-classifier, logistic-regression]
see_also: [pointwise-mutual-information, min-cut-problem, support-vector-machine, bert, tf-idf, word-embedding, named-entity-recognition, confusion-matrix]
sources:
  - paper: "Bo Pang, Lillian Lee and Shivakumar Vaithyanathan, Thumbs up? Sentiment classification using machine learning techniques, Proceedings of EMNLP 2002, pages 79 to 86"
    title: Pang, Lee and Vaithyanathan 2002
    locator: the movie review data, the comparison of naive Bayes, maximum entropy and support vector machines on word features, and the discussion of why sentiment is harder than topic
  - paper: "Peter D. Turney, Thumbs up or thumbs down? Semantic orientation applied to unsupervised classification of reviews, Proceedings of ACL 2002, pages 417 to 424"
    title: Turney 2002
    locator: the semantic orientation of a phrase from its pointwise mutual information with excellent and with poor, and the review classification by the mean orientation
  - paper: "Minqing Hu and Bing Liu, Mining and summarizing customer reviews, Proceedings of KDD 2004"
    title: Hu and Liu 2004
    locator: product features found in reviews and the opinion about each feature
  - paper: "Bo Pang and Lillian Lee, Opinion mining and sentiment analysis, Foundations and Trends in Information Retrieval 2(1-2), 2008"
    title: Pang and Lee 2008
    locator: the survey of the problems, the methods and the data sets
---

Sentiment analysis decides what opinion a piece of text expresses: whether a review is positive or negative, how many stars it would get, or how the writer feels about each feature of a product. It became a research area around 2002, when Pang, Lee and Vaithyanathan applied standard classifiers to movie reviews and Turney classified reviews with no labeled data, and it is now one of the most used kinds of text classification. The words carry much of the signal ("superb", "boring"), but negation, contrast, irony and the target of each opinion make it harder than sorting texts by topic.

## In plain words

Read a review and say whether the writer liked the thing or not. Words like "great" and "awful" are strong clues, but not enough: "not great" flips the meaning, and "I expected a great film" may be negative. A review can like one part and dislike another: "the screen is sharp but the battery dies fast". So the question can be asked about a whole review, about each sentence, or about each feature named in it. The answer can be a class (positive, negative, neutral) or a number, such as a star rating.

## Definition

**Input.** A text $x$, which can be a document, a sentence or a short message; for aspect-based analysis, also an aspect $a$ (a feature or entity that the text talks about).

**Output.** A polarity $y$ from a fixed set of classes, usually {positive, negative} or {positive, negative, neutral}, or a score on an ordered scale, such as 1 to 5 stars. For aspect-based analysis, the polarity of the opinion about $a$.

**Learning form.** Given labeled examples $(x, y)$, find a classifier $f$ with low error on new texts. Labels often come for free from star ratings in reviews.

**Score.** Accuracy for balanced binary data; macro-averaged F1 over the classes when the classes are unbalanced or neutral is included; mean absolute error or correlation for ratings. A [confusion matrix](/confusion-matrix/) shows which classes are mixed up.

## Variants

- Document-level polarity: one label per review (Pang, Lee and Vaithyanathan 2002).
- Sentence-level polarity, and subjectivity detection: first decide whether a sentence states an opinion or a fact.
- Rating prediction: predict the number of stars, an ordinal regression problem.
- Aspect-based sentiment: find the aspects of a product or service named in the text and the opinion about each (Hu and Liu 2004).
- Target-dependent and stance detection: the opinion about a given entity, or for or against a given claim.
- Emotion classification: classes such as joy, anger and fear instead of polarity.
- Lexicon building: give each word or phrase a polarity score, as in Turney (2002).

## Examples

"The plot was predictable, but the acting was superb." At the aspect level, plot is negative and acting is positive. At the sentence level the label depends on the guidelines; many annotators mark it positive, because the clause after "but" usually carries the main point.

Negation: "This is not a good film" contains "good" and is negative. A model that counts words without their context misreads it.

Words that depend on the domain: "unpredictable" is good for a film plot and bad for a car's steering.

Turney's orientation: the semantic orientation of a phrase is $\mathrm{SO}(p) = \mathrm{PMI}(p, \text{excellent}) - \mathrm{PMI}(p, \text{poor})$, from [pointwise mutual information](/pointwise-mutual-information/) estimated with search engine counts, and a review is classified by the mean orientation of its phrases (Turney 2002).

## Known algorithms

- Lexicon methods: sum the polarity scores of the words from a lexicon, with rules for negation and intensifiers. No training data needed.
- Unsupervised orientation: Turney (2002), as in the example.
- Linear classifiers on word features: the [naive Bayes classifier](/naive-bayes-classifier/), [logistic regression](/logistic-regression/) and the [support vector machine](/support-vector-machine/) on unigram and bigram features, or [tf-idf](/tf-idf/) weights. Pang, Lee and Vaithyanathan (2002) found that these beat word lists chosen by people on movie reviews, and that sentiment was harder than topic classification for them (measurements).
- Subjectivity extraction by minimum cut: Pang and Lee (2004) first removed objective sentences, choosing the subjective ones by a [minimum cut](/min-cut-problem/) in a graph whose edges reward giving nearby sentences the same label, then classified the rest.
- Neural models: average [word embeddings](/word-embedding/), or use convolutional, recurrent or tree-structured networks over the sentence.
- Pretrained transformers: fine-tune [BERT](/bert/) or a similar encoder with a classifier on the sentence representation. This is the usual method today when labeled data exist.

## Bounds

- A linear classifier over the words of a text of $n$ tokens, with a hash map from words to weights, takes $O(n)$ time to classify (a theorem, by counting); training naive Bayes is one pass over the data.
- A transformer encoder takes $O(n^2 d)$ time for $n$ tokens and width $d$.
- The minimum-cut formulation of subjectivity detection is solved exactly in polynomial time by a max-flow algorithm (a theorem), because it has two labels and the pair terms reward agreement.
- Human agreement limits measured accuracy: annotators disagree on many neutral and mixed texts, so scores near perfect are not expected on such data (a measurement, depending on the data set).

## Reductions

- Sentiment classification is text classification with polarity classes, so any [multiclass classification](/multiclass-classification/) method applies.
- Rating prediction reduces to ordinal regression, or to classification with ordered classes.
- Aspect-based analysis reduces to finding aspect spans, a [sequence labeling](/sequence-labeling/) task with [BIO encoding](/bio-encoding/), followed by classification of each (text, aspect) pair.
- Sentence subjectivity with neighbor agreement reduces to [minimum cut](/min-cut-problem/), as in Pang and Lee (2004).

## Applications

- Product and service reviews: summarize opinions per feature, find complaints.
- Social media monitoring: track the opinion about a brand, a product or a politician over time.
- Finance: measure the tone of news and reports.
- Customer support: route angry messages first.

## References
