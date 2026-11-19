---
tag: YD1B0W
kind: technique
slug: cross-domain-similarity-local-scaling
name: Cross-domain similarity local scaling
aliases:
- CSLS
area: natural-language-and-speech/word-and-sentence-embeddings
level: research
summary: Retrieve translations by cosine similarity minus the mean similarity of each word to its k nearest neighbours, which reduces hubness.
model: real-ram
complexity:
  vars: {n: "the number of source words", m: "the number of target words", d: "the dimension of the vectors", K: "the size of the neighbourhood"}
  time: {worst: "O(n m (d + log K))"}
  space: {extra: "O((n + m) K)"}
history:
  year: 2018
  people: [Alexis Conneau, Guillaume Lample, Marc'Aurelio Ranzato, Ludovic Denoyer, Hervé Jégou]
  note: "Conneau, Lample, Ranzato, Denoyer and Jégou introduced CSLS in 2018 for word translation with mapped embeddings, as a correction for hubness that needs no tuned parameter, after the reverse ranks of Dinu, Lazaridou and Baroni (2015) and the inverted softmax of Smith et al. (2017)."
prereqs: [cross-lingual-embedding-mapping, cosine-similarity, hubness]
see_also: [k-nearest-neighbor-search, nearest-neighbor-search, curse-of-dimensionality, word-analogy, sentence-embedding, k-nearest-neighbors]
sources:
  - paper: "Alexis Conneau, Guillaume Lample, Marc'Aurelio Ranzato, Ludovic Denoyer and Hervé Jégou, Word translation without parallel data, ICLR 2018, arXiv:1710.04087"
    title: Conneau, Lample, Ranzato, Denoyer and Jégou 2018
    locator: "Section 2.3 (equations 5 and 6, the definition of r_T, r_S and CSLS), Section 3.4 (mutual nearest neighbours under CSLS for the dictionary), Section 4 and Table 1 (K = 10, and Procrustes with NN, ISF and CSLS retrieval)"
  - paper: "Miloš Radovanović, Alexandros Nanopoulos and Mirjana Ivanović, Hubs in space: popular nearest neighbors in high-dimensional data, Journal of Machine Learning Research 11, 2010, pages 2487 to 2531"
    title: Radovanović, Nanopoulos and Ivanović 2010
    locator: the hubness phenomenon, some points are nearest neighbours of many points in high dimension
  - paper: "Georgiana Dinu, Angeliki Lazaridou and Marco Baroni, Improving zero-shot learning by mitigating the hubness problem, ICLR 2015 workshop track, arXiv:1412.6568"
    title: Dinu, Lazaridou and Baroni 2015
    locator: the hubness of mapped vectors and the retrieval rule based on reverse ranks
  - paper: "Samuel L. Smith, David H. P. Turban, Steven Hamblin and Nils Y. Hammerla, Offline bilingual word vectors, orthogonal transformations and the inverted softmax, ICLR 2017, arXiv:1702.03859"
    title: Smith, Turban, Hamblin and Hammerla 2017
    locator: the inverted softmax, which normalizes the similarity of each target word over the source words
---

Cross-domain similarity local scaling (CSLS) is a similarity score for nearest neighbour retrieval between two sets of vectors, such as mapped source words and target words in [cross-lingual embedding mapping](/cross-lingual-embedding-mapping/). In high dimension, a few target vectors, called hubs, are the nearest neighbours of many queries, and plain [cosine](/cosine-similarity/) retrieval returns them too often ([hubness](/hubness/)). CSLS subtracts from twice the cosine the mean similarity of each of the two vectors to its $K$ nearest neighbours in the other set:

$$\mathrm{CSLS}(\vec x, \vec y) = 2\cos(\vec x, \vec y) - r_T(\vec x) - r_S(\vec y).$$

A hub has a high $r_S$, so its scores go down. Conneau, Lample, Ranzato, Denoyer and Jégou (2018) introduced it with $K = 10$. On their English to Spanish test, it raised the precision at 1 of a supervised Procrustes map from 77.4 with plain nearest neighbour to 81.4.

## In plain words

When you translate a word by finding the closest word in the other language, some words are close to almost everything. They sit in a crowded middle part of the space, and they keep winning, even when they are wrong.

CSLS makes the contest fairer. For every word, it measures how close the word usually is to its nearest few neighbours on the other side. A word that is close to everything has a high usual closeness. The score of a pair is its closeness, counted twice, minus the usual closeness of each of the two words.

A pair now scores high only when the two words are closer to each other than they are to their other neighbours. Crowded words lose their advantage, and isolated words get a fair chance.

## When it applies

Use it when you retrieve, for each query from one set, its best match in a second set by cosine similarity, the vectors have a high dimension, and you can afford to compute the neighbourhoods of both sets once. The signals are retrieval between two domains (two languages, or images and text), the same few targets appearing as the answer to many queries, and a wish for a fixed rule without a tuned temperature. For retrieval inside one set, the same idea applies with both neighbourhoods in that set.

## The template

The holes are the source vectors $\vec x_s$ (already mapped into the target space), the target vectors $\vec y_t$, the similarity (cosine) and the size $K$ of the neighbourhoods. Let $N_T(\vec x)$ be the $K$ target vectors nearest to $\vec x$ and $N_S(\vec y)$ the $K$ source vectors nearest to $\vec y$. Then

$$r_T(\vec x) = \frac{1}{K}\sum_{\vec y_t \in N_T(\vec x)} \cos(\vec x, \vec y_t), \qquad r_S(\vec y) = \frac{1}{K}\sum_{\vec x_s \in N_S(\vec y)} \cos(\vec x_s, \vec y).$$

```pseudo id=main
CSLS-RETRIEVE(sources x_1..x_n, targets y_1..y_m, K)
L1  for each source s do r_T(s) ← mean of the K largest cos(x_s, y_t) over the targets t
L2  for each target t do r_S(t) ← mean of the K largest cos(x_s, y_t) over the sources s
L3  for each source s do
L4      answer(s) ← argmax over t of 2 cos(x_s, y_t) - r_T(s) - r_S(t)
L5  return answer
```

Lines L1 and L2 compute the two mean similarities, with the cosines of the same $n \times m$ matrix read by rows and by columns. Line L4 ranks the targets of one source. For a fixed source, $r_T(s)$ is the same for every target, so the ranking of line L4 is the ranking by $2\cos(\vec x_s, \vec y_t) - r_S(t)$. The term $r_T$ matters when scores of different sources are compared, for example to keep the most confident pairs or to test whether two words are mutual nearest neighbours.

With brute force, lines L1 to L4 cost $O(nmd)$ for the cosines and $O(nm \log K)$ for the heaps of the $K$ best values, and the heaps take $O((n + m)K)$ space. In practice the neighbourhoods are found with a fast [nearest neighbour index](/k-nearest-neighbor-search/), often on the most frequent words only.

**Example.** Take three sources and three targets with the cosines below, and $K = 2$.

| | $t_1$ | $t_2$ | $t_3$ | $r_T$ |
|---|---|---|---|---|
| $s_1$ | 0.60 | 0.20 | 0.65 | 0.625 |
| $s_2$ | 0.10 | 0.55 | 0.60 | 0.575 |
| $s_3$ | 0.20 | 0.15 | 0.70 | 0.450 |
| $r_S$ | 0.400 | 0.375 | 0.675 | |

Every row has its largest cosine at $t_3$, so plain nearest neighbour retrieval sends all three sources to the hub $t_3$. Its $r_S$ is high, $(0.70 + 0.65)/2 = 0.675$. The CSLS scores are

| | $t_1$ | $t_2$ | $t_3$ | answer |
|---|---|---|---|---|
| $s_1$ | 0.175 | -0.600 | 0.000 | $t_1$ |
| $s_2$ | -0.775 | 0.150 | -0.050 | $t_2$ |
| $s_3$ | -0.450 | -0.525 | 0.275 | $t_3$ |

For example, $\mathrm{CSLS}(s_1, t_1) = 2(0.60) - 0.625 - 0.400 = 0.175$. Each target is now chosen once, and each pair is a mutual best match under CSLS.

## Classic examples

- **Word translation.** After a [cross-lingual embedding mapping](/cross-lingual-embedding-mapping/) by Procrustes, each source word is translated to the target word with the highest CSLS score. This is the use in Conneau et al., where it beat plain cosine and the inverted softmax in most language pairs of their Table 1.
- **Dictionary induction for refinement.** The Procrustes refinement of Conneau et al. builds each new seed dictionary from the pairs that are mutual nearest neighbours under CSLS, so that the next map is fitted on more reliable pairs.
- **Analogy and similarity search.** The same correction applies to any [k-nearest neighbor search](/k-nearest-neighbor-search/) in a high-dimensional embedding space where [hubness](/hubness/) appears, such as the retrieval step of a [word analogy](/word-analogy/) query.
- **Cross-lingual sentence retrieval.** With multilingual [sentence embeddings](/sentence-embedding/), the same kind of score, the cosine corrected by the mean similarity to the nearest neighbours, is used to find sentences that are translations of each other.

## Variations

- **The size of the neighbourhood.** Conneau et al. report that the results are about the same for $K = 5$, 10 and 50, and use $K = 10$ in all their tests.
- **Inverted softmax.** Smith et al. (2017) normalize the similarities of each target over all sources with a softmax at a temperature, which also lowers the scores of hubs. The temperature must be tuned, which is hard without a validation dictionary.
- **Reverse ranks.** Dinu, Lazaridou and Baroni (2015) rank the candidates by how highly the query ranks among the neighbours of each candidate, instead of by the similarity itself.
- **Ratio form.** Dividing the cosine by the mean neighbourhood similarity, instead of subtracting it, gives a margin of a related form.
- **One domain.** For retrieval in one set, both means are taken in that set. Conneau et al. note that this kind of correction resembles the preprocessing of some spectral clustering methods.

## Pitfalls

- **Neighbourhoods on the wrong side.** $r_T(\vec x)$ uses the target neighbours of a source vector and $r_S(\vec y)$ the source neighbours of a target vector. Computing $r_S(\vec y)$ from the other target vectors measures density in the wrong set and does not correct cross-domain hubs.
- **Unmapped sources.** $r_S$ must use the mapped source vectors $W\vec x_s$. Using the source vectors before the map gives meaningless cosines.
- **Reading the score as a cosine.** CSLS values are not in $[-1, 1]$ and can be negative for the best match. Use them to rank, not as a similarity with a fixed threshold.
- **The cost of $r_S$.** Line L2 needs the $K$ nearest sources of every target, which is a search over the whole source vocabulary for each target. Restrict both vocabularies to the frequent words, or use an index.
- **Different sets at test time.** $r_S$ and $r_T$ depend on which words are in the two sets. Adding or removing words changes the scores of all pairs, so compare results only with the same vocabularies.

## Exercises

1. Show that for a fixed source $s$, ranking the targets by CSLS gives the same order as ranking them by $2\cos(\vec x_s, \vec y_t) - r_S(t)$.
2. In the example, change the cosine of $s_1$ and $t_3$ from 0.65 to 0.75. Recompute $r_T(s_1)$, $r_S(t_3)$ and the CSLS answers.
3. Show that if every target has the same $r_S$, CSLS retrieval returns the same answers as plain nearest neighbour retrieval.

## References
