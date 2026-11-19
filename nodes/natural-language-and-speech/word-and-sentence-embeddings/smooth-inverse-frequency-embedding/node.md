---
tag: V5GPPB
kind: algorithm
slug: smooth-inverse-frequency-embedding
name: Smooth inverse frequency embedding
aliases:
- SIF embedding
area: natural-language-and-speech/word-and-sentence-embeddings
level: advanced
summary: A sentence vector as the weighted mean of its word vectors with weights a / (a + p(w)), minus its projection on the first principal component.
model: real-ram
complexity:
  vars: {t: the total number of tokens, n: the number of sentences, d: the dimension of the word vectors, q: the number of power iteration steps}
  time: {worst: "O(t d + n d^2 + q d^2)"}
  space: {extra: "O(n d + d^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false, supervised: false}
history:
  year: 2017
  people: [Sanjeev Arora, Yingyu Liang, Tengyu Ma]
  note: Arora, Liang and Ma gave the weights from a random walk model of text and showed that a weighted average of word vectors with one direction removed beats many trained sentence encoders on similarity tasks.
prereqs: [sentence-embedding, word-embedding, principal-component-analysis]
see_also: [power-iteration, singular-value-decomposition, tf-idf, paragraph-vector, sentence-bert, simcse, glove, cosine-similarity]
sources:
  - paper: "Sanjeev Arora, Yingyu Liang and Tengyu Ma, A simple but tough-to-beat baseline for sentence embeddings, International Conference on Learning Representations (ICLR 2017), OpenReview SyK00v5xx"
    title: Arora, Liang and Ma 2017
    locator: Algorithm 1 (the weighted average and the removal of the common component), the random walk model that gives the weights, and the experiments on the textual similarity tasks
---

Smooth inverse frequency (SIF) embedding turns a sentence into a vector with no training beyond the [word vectors](/word-embedding/). It averages the word vectors of the sentence, each weighted by $a / (a + p(w))$, where $p(w)$ is the frequency of the word in a large corpus and $a$ is a small constant such as $10^{-3}$. Then it removes from every sentence vector its projection on one direction $u$, the first singular vector of the matrix of all sentence vectors. Arora, Liang and Ma 2017 measured that this simple method beats many trained [sentence embedding](/sentence-embedding/) models on textual similarity benchmarks.

## In plain words

A plain average of word vectors is pulled toward words like "the", "of" and "and", which appear in almost every sentence and say little. SIF gives each word a weight that is close to 1 for rare words and small for frequent words, so the content words decide where the sentence vector points. Even after the weighting, all sentence vectors still share one common part, which comes from syntax and from frequent words. SIF finds that shared direction from all the sentences together and cuts it away from each sentence. What is left shows how the sentences differ, which is what a similarity score needs.

## The problem

The input is a set of $n$ tokenized sentences, a word vector $v_w \in \mathbb{R}^d$ for each known word, a unigram probability $p(w)$ for each word, estimated on a large corpus, and a parameter $a > 0$. The output is a vector for each sentence. The cosine of two output vectors is used as the similarity of the two sentences.

## The algorithm

```pseudo id=main
SIF(S_1 .. S_n, v, p, a)
L1  for each sentence s do
L2      v_s ← (1 / |s|) Σ_{w ∈ s} a / (a + p(w)) · v_w
L3  X ← the n × d matrix with the rows v_s
L4  u ← the first right singular vector of X            ▷ no centering
L5  for each sentence s do
L6      v_s ← v_s - u u^T v_s
L7  return v_s for every s, and u
```

Line L4 needs only the top eigenvector of the $d \times d$ matrix $X^T X$, so [power iteration](/power-iteration/) is enough, and a truncated [singular value decomposition](/singular-value-decomposition/) gives the same vector. As in the code of the authors, $X$ is not centered, so $u$ is not the first principal component in the strict sense of [principal component analysis](/principal-component-analysis/), which centers the data first. To embed new sentences later, keep $u$ from the training sentences and apply lines L2 and L6 with it.

The weights come from a model. A latent discourse vector $c_s$ produces each word with probability $\alpha\, p(w) + (1 - \alpha) \exp(v_w \cdot \tilde c_s) / Z$, where $\tilde c_s = \beta c_0 + (1 - \beta) c_s$ mixes in a common discourse vector $c_0$. Under approximations, the maximum likelihood estimate of $\tilde c_s$ is proportional to the weighted sum of line L2 with $a = (1 - \alpha) / (\alpha Z)$, and line L6 estimates $c_0$ by $u$ and removes it. The derivation is a heuristic argument; the paper tests it by experiments.

## Example

The probabilities and the 3-dimensional vectors are written for this page. With $a = 10^{-3}$, "the" ($p = 0.05$) gets the weight $1/51 = 0.0196$, "a" ($p = 0.04$) gets 0.0244, "cat" and "dog" ($p = 10^{-4}$) get 0.9091, and "sat" and "ran" ($p = 5 \cdot 10^{-4}$) get 0.6667.

| word | vector |
| --- | --- |
| the | (1, 1, 0) |
| a | (1, 0.8, 0.2) |
| cat | (0.2, 0, 1) |
| dog | (0, 0.2, 1) |
| sat | (0.5, -1, 0) |
| ran | (0.3, -1, 0.3) |

| sentence | line L2 | line L6 |
| --- | --- | --- |
| the cat sat | (0.1783, -0.2157, 0.303) | (0.0495, -0.0326, -0.0364) |
| a dog ran | (0.0748, -0.1551, 0.3713) | (-0.053, 0.0266, 0.0345) |
| the dog sat | (0.1176, -0.1551, 0.303) | (0.0036, 0.007, 0.0024) |

The weighting moves the vectors away from "the": the plain average of "the cat sat" is (0.5667, 0, 0.3333), and the weighted one has its largest entry in the third coordinate, where "cat" points. The first singular vector is $u = (0.3168, -0.4503, 0.8348)$ with singular value 0.6766, and the projections on it are 0.4066, 0.4035 and 0.3601. Before line L6 the three cosines are 0.9436, 0.9845 and 0.9861, so the vectors hardly differ. After line L6 every vector is orthogonal to $u$, and the cosines are spread from -0.9945 to 0.1435. Three toy sentences cannot show that the new cosines are better; they show only what the steps do.

## Correctness

The proof below shows three facts, which are theorems. The weight $a / (a + p)$ is 1 at $p = 0$, $1/2$ at $p = a$, and strictly decreases in $p$. The first right singular vector $u$ of $X$ maximizes $\sum_s (v_s \cdot u)^2$ over unit vectors, and power iteration converges to it when the two largest singular values differ. Line L6 gives $v_s \cdot u = 0$, and it is the smallest change of $v_s$ along $u$ that does so. The tests check these facts and that a common direction planted in the word vectors is found and removed.

That SIF gives good sentence similarities is a measurement, not a theorem. The paper reports that the method, with GloVe or with PARAGRAM-SL999 word vectors, improves on the plain average by about 10% to 30% on textual similarity tasks and beats several trained models, including LSTM encoders.

## Complexity

The model is the [real-RAM](/real-ram/).

- **Weighted averages.** Line L2 touches each token once at $O(d)$ cost: $O(t d)$ for $t$ tokens.
- **First singular vector.** Forming $X^T X$ costs $O(n d^2)$, and each power iteration step costs $O(d^2)$, so $q$ steps cost $O(q d^2)$. Without forming $X^T X$, each step costs $O(n d)$ as two products with $X$.
- **Removal.** Line L6 costs $O(d)$ per sentence, $O(n d)$ in total.

The extra space is $O(n d)$ for $X$ and $O(d^2)$ for $X^T X$. With $d = 300$ the whole method is fast enough for millions of sentences.

## Properties

- **No training of its own.** The method needs word vectors and word frequencies. Its only parameters are $a$ and the one direction $u$.
- **Order is ignored.** "dog bites man" and "man bites dog" get the same vector, as with every weighted average.
- **Not online.** The direction $u$ depends on all sentences of the set. A fixed $u$ from a training set makes the embedding of new sentences independent of each other.
- **Deterministic.** With a fixed start vector for the power iteration the output is fixed up to the sign of $u$, and the sign does not change line L6.

## Variants and improvements

- **Weights only (W) or removal only (R).** The paper reports both parts separately; each helps, and the two together help most.
- **More directions.** Removing the top few singular directions instead of one is a common change. The same idea applied to word vectors is the "all-but-the-top" postprocessing of Mu and Viswanath 2018.
- **uSIF.** Ethayarajh 2018 derived the weights from a changed random walk model, which removes the need to tune $a$, and removed a few directions with weights.
- **Other weights.** IDF weights, as in [tf-idf](/tf-idf/), give a similar effect. Both down-weight frequent words, but SIF uses the corpus frequency and IDF uses the share of documents that contain the word.

## When to use it

Use SIF as a strong baseline for sentence similarity, clustering and retrieval when no labeled pairs exist, when the cost must be very low, or when a trained encoder is not allowed. Compare a new encoder against it. When labeled pairs or a pretrained transformer are available, trained encoders such as [Sentence-BERT](/sentence-bert/) and [SimCSE](/simcse/) usually measure better on the same benchmarks.

## Pitfalls

- **Frequencies from the wrong corpus.** The weights need $p(w)$ from a large general corpus. Frequencies from a small task set make rare but common words look important.
- **The value of a.** The paper measured good results for $a$ from about $10^{-4}$ to $10^{-3}$. Larger values bring back the weight of frequent words, and very small values make most words weigh about $a / p(w)$.
- **Centering.** Centering $X$ before line L4 gives a different direction. Both are used in practice; state which one you use.
- **A new u for every batch.** Computing $u$ on each small batch at test time makes the vector of a sentence depend on the other sentences of the batch. Fix $u$ on a training set.
- **Unknown words.** Words without a vector are skipped, and a sentence with no known word gives the zero vector, whose cosine is not defined.

## Implementations

The code takes the word vectors and the word probabilities as given and implements the weights, the weighted average, the first singular vector by power iteration on the uncentered $X^T X$, and the removal of the projection.

## History

Weighted averages of word vectors, often with IDF weights, were used as sentence vectors well before 2017. Wieting et al. 2016 showed that a plain average of word vectors trained on paraphrase pairs is hard to beat. Arora, Liang and Ma 2017 gave the SIF weights a basis in a random walk model of text, added the removal of the common direction, and titled the paper "a simple but tough-to-beat baseline". Later sentence encoders built on [BERT](/bert/), such as [Sentence-BERT](/sentence-bert/), compare against it.

## References
