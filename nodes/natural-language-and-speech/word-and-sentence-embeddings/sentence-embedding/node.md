---
tag: 83BE7H
kind: problem
slug: sentence-embedding
name: Sentence embedding
aliases:
- sentence representation learning
area: natural-language-and-speech/word-and-sentence-embeddings
level: core
summary: Map a sentence or a short text to one fixed-size vector so that the cosine of two vectors reflects the semantic similarity of the two texts.
prereqs: [word-embedding, cosine-similarity]
see_also: [paragraph-vector, smooth-inverse-frequency-embedding, sentence-bert, simcse, word-movers-distance, tf-idf, nearest-neighbor-search, maximum-inner-product-search]
sources:
  - paper: doi:10.18653/v1/S17-2001
    title: Daniel Cer, Mona Diab, Eneko Agirre, Iñigo Lopez-Gazpio and Lucia Specia, SemEval-2017 Task 1, Semantic textual similarity multilingual and crosslingual focused evaluation, SemEval-2017, pages 1 to 14
    locator: the STS benchmark, its scale from 0 to 5, and the Pearson correlation used to score systems
  - paper: "Sanjeev Arora, Yingyu Liang and Tengyu Ma, A simple but tough-to-beat baseline for sentence embeddings, International Conference on Learning Representations (ICLR 2017), OpenReview SyK00v5xx"
    title: Arora, Liang and Ma 2017
    locator: the weighted average baseline and its comparison with trained encoders on the textual similarity tasks
  - paper: doi:10.18653/v1/D17-1070
    title: Alexis Conneau, Douwe Kiela, Holger Schwenk, Loïc Barrault and Antoine Bordes, Supervised learning of universal sentence representations from natural language inference data, EMNLP 2017, pages 670 to 680
    locator: the transfer evaluation of sentence vectors with a classifier on top, and the InferSent encoder
  - paper: doi:10.18653/v1/D19-1410
    title: Nils Reimers and Iryna Gurevych, Sentence-BERT, Sentence embeddings using siamese BERT-networks, EMNLP-IJCNLP 2019, pages 3982 to 3992
    locator: the STS comparison of average GloVe vectors, plain BERT vectors and SBERT, and the cost of the cross-encoder on all pairs
  - paper: "Quoc Le and Tomas Mikolov, Distributed representations of sentences and documents, Proceedings of the 31st International Conference on Machine Learning (ICML 2014), PMLR 32(2), pages 1188 to 1196"
    title: Le and Mikolov 2014
    locator: the paragraph vector models
  - paper: doi:10.18653/v1/2021.emnlp-main.552
    title: Tianyu Gao, Xingcheng Yao and Danqi Chen, SimCSE, Simple contrastive learning of sentence embeddings, EMNLP 2021, pages 6894 to 6910
    locator: the unsupervised and supervised contrastive objectives and the STS averages
---

Sentence embedding is the problem of mapping a sentence, or any short text, to one vector of fixed size, so that texts with similar meanings get vectors with a high [cosine](/cosine-similarity/), and so that the vectors serve as features for classification and as keys for retrieval. There is no single correct answer: a method is judged by measurement, mainly by the rank correlation of its cosines with human similarity scores. Averaging [word vectors](/word-embedding/) is a strong baseline, and trained encoders such as [Sentence-BERT](/sentence-bert/) and [SimCSE](/simcse/) measure best today.

## In plain words

Computers compare vectors easily, but they cannot compare the meaning of two sentences directly. A sentence embedding gives every sentence a list of numbers of the same length, for example 768 numbers. The goal is that "A man is playing a guitar" and "Someone plays an instrument" get lists that point in nearly the same direction, while "The stock market fell" points elsewhere. Once every sentence has such a list, finding similar sentences, grouping them, or training a classifier on them is fast and simple. The hard part is to find a method that makes the directions agree with what people judge as similar.

## Definition

**Input.** A set of texts, each a sequence of tokens, and possibly training data: a large unlabeled corpus, or labeled pairs (similar or not, entailment or contradiction).

**Output.** A function $f$ from texts to $\mathbb{R}^d$, for a fixed $d$, that does not depend on other texts at test time.

**The question.** The similarity of texts $a$ and $b$ is scored as $\cos(f(a), f(b))$. On a test set of pairs with human scores, for example from 0 (unrelated) to 5 (the same meaning) in the STS benchmark of Cer et al. 2017, the scores of $f$ should have a high rank correlation (Spearman) or linear correlation (Pearson) with the human scores. In the transfer form, a simple classifier, such as [logistic regression](/logistic-regression/), trained on $f(a)$ should predict labels such as sentiment well.

**Known complexity.** The question has no exact solution to compute; it is an empirical problem. What can be stated exactly is the cost of using a given $f$: $n$ evaluations of $f$ for $n$ texts, $O(d)$ per pair score, and $O(n d)$ per exact nearest neighbor query.

## Variants

- **Unsupervised or supervised.** Unsupervised methods use only raw text and word frequencies; supervised ones use labeled pairs, often [natural language inference](/natural-language-inference/) data.
- **Symmetric or asymmetric.** Similarity of two sentences is symmetric. Retrieval of passages for a question is asymmetric, and often uses two encoders, as in [dense passage retrieval](/dense-passage-retrieval/).
- **Length.** Sentences, paragraphs and whole documents. [Paragraph vectors](/paragraph-vector/) were designed for documents.
- **Cross-lingual.** Texts in different languages with the same meaning should get close vectors, which allows mining of parallel sentences (see [sentence alignment](/sentence-alignment/)).
- **Pair scorers.** A cross-encoder reads both texts at once and returns a score. It does not give a vector per text, so it is not a solution of this problem, but it is the usual upper reference for the quality of pair scores.

## Examples

Take the 2-dimensional word vectors dog $(1, 0)$, man $(0, 1)$ and bites $(1, 1)$, and let $f$ be the plain average. Then $f(\text{dog bites man}) = (\frac{2}{3}, \frac{2}{3})$ and $f(\text{man bites dog}) = (\frac{2}{3}, \frac{2}{3})$, so their cosine is 1, although the meanings differ. With cat $(1, 0.2)$, $f(\text{cat bites man}) = (\frac{2}{3}, 0.7333)$, whose cosine with $(\frac{2}{3}, \frac{2}{3})$ is $0.9989$. The average sees which words occur, not their order or roles.

A measured example (Reimers and Gurevych 2019): as the Spearman correlation times 100, averaged over seven STS data sets with no STS training, average GloVe vectors gave 61.32, mean-pooled BERT vectors 54.81, the BERT CLS vector 29.19, and Sentence-BERT trained on NLI 74.89. A large pretrained network used without training for this problem did worse than the average of static word vectors.

## Known algorithms

| method | training data | how $f$ is computed |
| --- | --- | --- |
| average of word vectors | none beyond the word vectors | mean of the word vectors |
| [tf-idf](/tf-idf/) weighted average | document frequencies | mean with IDF weights |
| [SIF](/smooth-inverse-frequency-embedding/) | word frequencies | mean with weights $a / (a + p(w))$, minus one common direction |
| [Paragraph vector](/paragraph-vector/) | unlabeled corpus | gradient steps per new text |
| Skip-thought (Kiros et al. 2015) | ordered sentences | an encoder trained to predict the neighbor sentences |
| InferSent (Conneau et al. 2017) | NLI pairs | a BiLSTM with max pooling |
| [Sentence-BERT](/sentence-bert/) | NLI pairs, then STS | a fine-tuned BERT with mean pooling |
| [SimCSE](/simcse/) | raw sentences, or NLI pairs | a BERT trained with a contrastive loss |

Measured results (all measurements): SIF beat many trained encoders of its time on STS. On the average of seven STS tasks, Gao et al. 2021 reported 76.25 for unsupervised SimCSE and 81.57 for supervised SimCSE, both with BERT-base, above the 74.89 of SBERT-NLI-base. [Word mover's distance](/word-movers-distance/) compares two texts without one vector per text, at a much higher cost per pair.

## Bounds

- **Order (theorem).** Any $f$ that is a function of the multiset of words, such as every weighted average, gives the same vector to two permutations of one sentence, so it cannot separate "dog bites man" from "man bites dog".
- **Rank (theorem).** For $n$ texts with unit vectors in $\mathbb{R}^d$, the matrix of all cosines is the Gram matrix $F F^T$ with $F \in \mathbb{R}^{n \times d}$. It is positive semidefinite, has 1 on the diagonal, and has rank at most $d$. A target similarity matrix that lacks these properties cannot be matched exactly in any dimension $d$, and a matrix of rank more than $d$ cannot be matched in dimension $d$.
- **Cost (theorem).** With an embedding, scoring all pairs of $n$ texts needs $n$ encoder passes and $n(n-1)/2$ dot products. A pair scorer needs $n(n-1)/2$ passes. For $n = 10{,}000$, Reimers and Gurevych estimated about 65 hours for BERT as a cross-encoder against about 5 seconds for SBERT (a measurement).

## Reductions

- **Most similar text to nearest neighbor search.** For unit vectors, $\|u - v\|^2 = 2 - 2\cos(u, v)$, so the text with the highest cosine is the nearest by Euclidean distance and the one with the largest dot product. Retrieval by cosine therefore reduces to [nearest neighbor search](/nearest-neighbor-search/) or [maximum inner product search](/maximum-inner-product-search/), and approximate indexes such as [HNSW](/hnsw/) and [product quantization](/product-quantization/) apply.
- **Clustering.** Grouping texts by meaning reduces to [k-means](/k-means/) or [agglomerative clustering](/agglomerative-clustering/) on the vectors.
- **Classification.** A text classification task reduces to a linear classifier on the vectors, which is how the transfer form of the problem is measured.

## Applications

- Semantic search: find the passages or questions closest to a query.
- Finding duplicate questions and paraphrases among many texts.
- Clustering of texts by topic.
- Mining parallel sentences from texts in two languages.
- Features for small classifiers when labeled data is scarce.
- The retrieval step of systems that answer questions from a collection of documents.

## References
