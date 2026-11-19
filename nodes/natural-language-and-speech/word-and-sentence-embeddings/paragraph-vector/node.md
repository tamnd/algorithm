---
tag: ZV1QWA
kind: model
slug: paragraph-vector
name: Paragraph vector
aliases:
- doc2vec
area: natural-language-and-speech/word-and-sentence-embeddings
level: advanced
summary: Le and Mikolov's model that learns a vector per document jointly with word vectors, by predicting the words of the document from it.
history:
  year: 2014
  people: [Quoc Le, Tomas Mikolov]
  note: Le and Mikolov at Google added a vector per paragraph to the word2vec training objectives and reported state of the art results on two sentiment data sets. Mesnil et al. 2015 could not reproduce the IMDB result.
prereqs: [continuous-bag-of-words, skip-gram-model]
see_also: [sentence-embedding, smooth-inverse-frequency-embedding, hierarchical-softmax, negative-sampling, latent-dirichlet-allocation, latent-semantic-analysis, tf-idf, sentiment-analysis]
sources:
  - paper: "Quoc Le and Tomas Mikolov, Distributed representations of sentences and documents, Proceedings of the 31st International Conference on Machine Learning (ICML 2014), PMLR 32(2), pages 1188 to 1196"
    title: Le and Mikolov 2014
    locator: Section 2.2 (PV-DM), Section 2.3 (PV-DBOW), and the experiments on the Stanford Sentiment Treebank and IMDB
  - paper: "Grégoire Mesnil, Tomas Mikolov, Marc'Aurelio Ranzato and Yoshua Bengio, Ensemble of generative and discriminative techniques for sentiment analysis of movie reviews, ICLR 2015 workshop, arXiv:1412.5335"
    title: Mesnil et al. 2015
    locator: Table 2 (paragraph vectors alone at 88.73% accuracy on IMDB) and footnote 2 (the 92.6% result appears only without shuffling of the data)
---

The paragraph vector model, often called doc2vec, learns a vector for each document of a corpus together with the [word vectors](/word-embedding/). It extends the word2vec objectives: in PV-DM the document vector joins the context words that predict the next word, as in [continuous bag of words](/continuous-bag-of-words/), and in PV-DBOW the document vector alone predicts words sampled from the document, as in [skip-gram](/skip-gram-model/). A document not seen in training gets its vector by gradient steps with all other weights fixed. It is one answer to the [sentence embedding](/sentence-embedding/) problem, and the two pages overlap: that page states the task and compares the methods, this page defines the model.

## The machine

**Parameters.** There are $M$ paragraphs (any span of text: a sentence, a paragraph or a document), each with an id, and a vocabulary of $V$ words. The paragraph matrix $D$ has a column $d_p \in \mathbb{R}^{q}$ for each paragraph $p$. The word matrix $W$ has a column $e_w \in \mathbb{R}^{r}$ for each word. The output layer has weights $U$ and biases $b$, one row per word.

**PV-DM (distributed memory).** A training example is a window of $c$ words $w_{t-c}, \ldots, w_{t-1}$ of paragraph $p$ and the next word $w_t$. The input is the concatenation $z = [d_p; e_{w_{t-c}}; \ldots; e_{w_{t-1}}]$ of size $q + c r$ (a mean or a sum is the other choice, with $q = r$). The model is

$$y = U z + b, \qquad p(w_t \mid p, w_{t-c}, \ldots, w_{t-1}) = \frac{e^{y_{w_t}}}{\sum_{i=1}^{V} e^{y_i}}.$$

The paragraph vector is shared by all windows of the same paragraph, and the word vectors are shared by all paragraphs. It acts as a memory of what the context words leave out, the topic of the paragraph.

**PV-DBOW (distributed bag of words).** The input is $d_p$ alone. A training example samples a window of the paragraph and then a word $w$ from it, and the model is $p(w \mid p) = \operatorname{softmax}(U d_p + b)_w$. Word order inside the paragraph is ignored, and no word vectors are needed.

**Training.** [Stochastic gradient descent](/stochastic-gradient-descent/) with [backpropagation](/backpropagation/) maximizes the sum of the log probabilities of all training examples over $D$, $W$, $U$ and $b$. The full softmax over $V$ words is replaced by [hierarchical softmax](/hierarchical-softmax/) or [negative sampling](/negative-sampling/), as in word2vec.

**Inference.** For a new paragraph, a column $d_{\text{new}}$ is added to $D$ and trained by gradient steps on the windows of that paragraph, with $W$, $U$ and $b$ fixed. The vector then goes to a separate classifier, such as [logistic regression](/logistic-regression/).

**Standing assumptions.** Paragraphs are bags of windows; the model sees no order beyond the window in PV-DM and none in PV-DBOW. The vocabulary is fixed, and an unknown word is dropped.

## What it counts

The model assigns the probability of each target word given the paragraph id and, for PV-DM, the window. The vector it returns for a paragraph is the column $d_p$.

- **Parameters.** $M q$ for the paragraphs, $V r$ for the words in PV-DM, and about $V (q + c r)$ for the output layer with concatenation. The paragraph matrix grows with the corpus, unlike the other parameters.
- **One example.** With concatenation, the PV-DM input has size $q + c r$, and one example costs $O((q + c r) \log V)$ with hierarchical softmax, or $O((q + c r) k)$ with $k$ negative samples, against $O((q + c r) V)$ for the full softmax. PV-DBOW costs $O(q \log V)$ or $O(q k)$.
- **Inference.** A new paragraph of $\ell$ words costs the per-example cost times $\ell$ times the number of passes over it. This is more than one forward pass of an encoder, and the result depends on the learning rate, the number of passes and the random start.

## Relation to other models

- **Word2vec.** PV-DM is [continuous bag of words](/continuous-bag-of-words/) with one more context token, the paragraph id, which is the same for every window of the paragraph. PV-DBOW is [skip-gram](/skip-gram-model/) with the paragraph id as the input word. Many tools train word vectors by skip-gram at the same time as PV-DBOW, so that the two share one space.
- **Topic models and matrix factorization.** [Latent semantic analysis](/latent-semantic-analysis/) and [latent Dirichlet allocation](/latent-dirichlet-allocation/) also give each document a low-dimensional vector from its word counts. As a heuristic view, PV-DBOW fits a low-rank model of the matrix of paragraphs by words with a softmax link.
- **Bag of words.** A [tf-idf](/tf-idf/) vector of a document is a sparse vector of size $V$ with no training. With a linear classifier and word bigrams, it is a strong baseline for sentiment on long reviews (see the Mesnil et al. result below).
- **Weighted averages.** [SIF](/smooth-inverse-frequency-embedding/) builds a sentence vector from fixed word vectors with no gradient steps per sentence, and the same sentence always gets the same vector.
- **Trained encoders.** [Sentence-BERT](/sentence-bert/) and [SimCSE](/simcse/) compute a vector by one forward pass of a network, for any new text.

## Known results in the model

- **Inference is a concave problem (theorem).** With $W$, $U$ and $b$ fixed, the score $y = U z + b$ is an affine function of $d_{\text{new}}$, in PV-DM as in PV-DBOW. The log softmax $y_w - \log \sum_i e^{y_i}$ is concave in $y$, because the log-sum-exp function is convex (see the [log-sum-exp trick](/log-sum-exp-trick/)). An affine map keeps concavity, and a sum of concave functions is concave. So the inference objective is concave in $d_{\text{new}}$ and has no local maximum that is not global. The same holds for hierarchical softmax and negative sampling, whose terms are $\log \sigma(\pm u \cdot z)$, also concave. The maximum need not be reached at a finite point; for example, a paragraph of one word has the supremum 0 only in the limit. So the result depends on the number of steps, and practical tools stop after a fixed number of passes.
- **Reported sentiment results (measurement).** Le and Mikolov 2014 reported an error rate of 12.2% on the coarse and 51.3% on the fine-grained Stanford Sentiment Treebank task, and 7.42% on IMDB, with the PV-DM and PV-DBOW vectors concatenated, 400 dimensions each, and windows of 8 and 10 words. They recommended the combination of the two models.
- **The IMDB result was not reproduced (measurement).** Mesnil, Mikolov, Ranzato and Bengio 2015 trained paragraph vectors alone on IMDB and got 88.73% accuracy, an error of 11.27%. Their footnote 2 reports that, with hierarchical softmax, the 92.6% accuracy of the original result appears only when the training and test data are not shuffled, and they consider that result invalid. In the same paper, a bag of word n-grams with a linear model was better than paragraph vectors.
- **Vectors depend on the run (a property of the method).** Inference starts from a random vector and uses a finite number of stochastic steps, so two runs give different vectors for the same text. Test a downstream use with several runs.

## References
