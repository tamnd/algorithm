---
tag: BGMRTX
kind: model
slug: relevance-model-rm3
name: Relevance model
aliases:
- RM3
- Lavrenko-Croft relevance model
area: information-retrieval-and-ai-reasoning/ranking-models
level: advanced
summary: Estimates a term distribution of the relevant class from top-ranked documents and mixes it with the query model for re-retrieval.
prereqs: [query-likelihood-model, pseudo-relevance-feedback, dirichlet-prior-smoothing]
see_also: [rocchio-algorithm, relevance-feedback, jelinek-mercer-smoothing, kullback-leibler-divergence, expectation-maximization, binary-independence-model, bm25, stop-word-removal]
sources:
  - paper: doi:10.1145/383952.383972
    title: Victor Lavrenko and W. Bruce Croft, Relevance-based language models, Proceedings of the 24th Annual International ACM SIGIR Conference (SIGIR 2001), 120-127
    locator: Section 3.2.1 (Method 1, independent and identical sampling), Section 3.2.2 (Method 2, conditional sampling, the method of the experiments) and Section 3.3 (the top 50 document models as the universe, Jelinek-Mercer smoothing with a constant lambda, and little variation for lambda between 0.4 and 0.8)
  - paper: "Nasreen Abdul-Jaleel, James Allan, W. Bruce Croft, Fernando Diaz, Leah Larkey, Xiaoyan Li, Mark D. Smucker and Courtney Wade, UMass at TREC 2004, novelty and HARD, Proceedings of the Thirteenth Text REtrieval Conference (TREC 2004)"
    locator: Section 3.1.4, the mixture P'(w|R) = lambda P(w|R) + (1 - lambda) P(w|Q) with 50 feedback documents, 200 terms, a weight of 0.6 on the original query and Dirichlet smoothing at mu equal to 1000
  - paper: doi:10.1145/984321.984322
    title: Chengxiang Zhai and John Lafferty, A study of smoothing methods for language models applied to information retrieval, ACM Transactions on Information Systems 22(2) (2004), 179-214
    locator: the Dirichlet prior smoothing of the document models used for the first retrieval
---

A relevance model is a probability distribution $P(w \mid R)$ over the words of the vocabulary that describes the documents relevant to a query. Victor Lavrenko and Bruce Croft introduced it in 2001 to bring the relevance class of the classical probabilistic models into the [query likelihood](/query-likelihood-model/) approach, which has no notion of relevance. With no judgments, they estimate it from the top documents of a first search: a mixture of their word distributions, each weighted by how likely it makes the query. RM3 mixes this estimate with the original query model and searches again, which makes it a method of [pseudo-relevance feedback](/pseudo-relevance-feedback/). The UMass group used it under the name RM3 in its runs at TREC 2004, and it is a standard feedback baseline in language modeling and in neural retrieval experiments.

## The machine

**The relevance model.** For a query $q = q_1 \ldots q_n$, Lavrenko and Croft approximate the probability of a word $w$ in the relevant documents by the probability of observing $w$ together with the query words, $P(w \mid R) \approx P(w \mid q_1, \ldots, q_n) = P(w, q_1, \ldots, q_n) / P(q_1, \ldots, q_n)$. The joint probability is computed over a universe $\mathcal{M}$ of language models, in practice the smoothed models of the top documents.

**Method 1, independent sampling (RM1).** Pick a model $M$ with probability $P(M)$, then draw $w$ and the query words from it independently:

$$P(w, q_1, \ldots, q_n) = \sum_{M \in \mathcal{M}} P(M) \, P(w \mid M) \prod_{i=1}^{n} P(q_i \mid M).$$

With a uniform $P(M)$, this gives $P(w \mid R) = \sum_{d} P(w \mid d) \, P(d \mid q)$, where $P(d \mid q) = P(q \mid d) / \sum_{d'} P(q \mid d')$. So RM1 is a mixture of the document models, each weighted by its normalized query likelihood.

**Method 2, conditional sampling (RM2).** Draw $w$ first, then each query word from a model chosen given $w$: $P(w, q_1, \ldots, q_n) = P(w) \prod_{i} \sum_{M} P(M \mid w) \, P(q_i \mid M)$. Lavrenko and Croft used this method in their experiments, with the top 50 documents as the universe and Jelinek-Mercer smoothing with a constant $\lambda$; they report little variation for $\lambda$ between 0.4 and 0.8.

**RM3.** Keep the $m$ words with the largest $P(w \mid R)$ under RM1, renormalize them to sum to 1, and mix with the maximum likelihood query model $P(w \mid Q) = c(w, q)/|q|$:

$$P'(w) = \lambda \, P(w \mid R) + (1 - \lambda) \, P(w \mid Q).$$

This is the form of the UMass runs at TREC 2004, which used 50 feedback documents, 200 terms and a weight of 0.6 on the original query, with [Dirichlet](/dirichlet-prior-smoothing/) smoothing at $\mu = 1000$.

**Ranking.** The second search ranks the documents by the negative cross entropy $\sum_w P'(w) \log p(w \mid d)$ with smoothed document models. This equals $-\mathrm{KL}(P' \,\|\, \theta_d)$ plus a constant, the [KL divergence](/kullback-leibler-divergence/) ranking, and with $P' = P(\cdot \mid Q)$ it is the query likelihood divided by $|q|$.

**Walk-through on the toy collection.** Take q1 = "sorted array search", Dirichlet smoothing with $\mu = 10$, $k = 2$ feedback documents, $m = 6$ words after the removal of the [stop words](/stop-word-removal/) "a", "an", "the", "in", "of", "is", "by", "for", "with", "to", "into", "up" and "each", and $\lambda = 0.5$.

1. The first search gives document 1, "binary search finds a key in a sorted array", the log likelihood -7.7954, and document 2, "merge sort merges two sorted runs into one sorted array", -9.0709. The likelihoods differ by a factor $e^{1.2755} = 3.5806$, so $P(d \mid q)$ is 0.7817 for document 1 and 0.2183 for document 2.
2. RM1 uses the maximum likelihood models $\mathrm{tf}/|d|$ of the two documents. "Sorted" gets $0.7817 \cdot 1/9 + 0.2183 \cdot 2/10 = 0.1305$, "array" 0.1087, "search", "binary", "finds" and "key" 0.0869 each (from document 1 only), and the six other words of document 2 get 0.0218 each.
3. The six best words have total mass 0.5866. Renormalized, "sorted" has 0.2225, "array" 0.1853 and the other four 0.1481 each.
4. With $\lambda = 0.5$ and $P(w \mid Q) = 1/3$ for each query word, $P'$ gives "sorted" 0.2779, "array" 0.2593, "search" 0.2407, and "binary", "finds" and "key" 0.0740 each.

| document | 1 | 2 | 8 | 7 | 4 | 6 | 3 | 5 |
|---|---|---|---|---|---|---|---|---|
| query model only | -2.5985 | -3.0236 | -3.1829 | -3.3957 | -3.6129 | -3.9289 | -3.9289 | -3.9289 |
| RM3 | -2.6281 | -3.3303 | -3.4630 | -3.6760 | -3.7976 | -3.8242 | -4.0610 | -4.0610 |

The top five keep their order, $1, 2, 8, 7, 4$. Document 6, "a hash table finds a key in constant expected time", leaves the tie with documents 3 and 5 and moves above them, because it holds "finds" and "key", two words that RM1 learned from document 1. Document 6 is not relevant to q1. The new words describe the top feedback document, not the information need, which is query drift.

## What it counts

- **The output.** A word distribution $P'$ with at most $m + |q|$ words, the expanded query, and the ranking that it gives.
- **Parameters.** The number $k$ of feedback documents, the number $m$ of words, the weight $\lambda$, and the smoothing of the first search; in the UMass setting $k = 50$, $m = 200$ and a query weight of 0.6.
- **Time.** One first search, then one pass over the $k$ feedback documents to accumulate $P(w \mid R)$ in $O(\sum_{d \in F} |d|)$ time with a hash map, a selection of the top $m$ words, and a second search over the posting lists of up to $m + |q|$ words. The second search dominates, which is why $m$ is cut.
- **Space.** A map from the words of the feedback documents to their mass, $O(\sum_{d \in F} |d|)$, plus the index.

## Relation to other models

- **Rocchio.** RM1 is a weighted centroid of the document models of the feedback set, with weights $P(d \mid q)$ in place of $1/k$, and RM3 adds the query with weight $1 - \lambda$. It is the [Rocchio](/rocchio-algorithm/) update with no negative part, in the space of word distributions.
- **Relevance feedback.** With documents that a user judged relevant in place of the top documents, the same estimate is [relevance feedback](/relevance-feedback/) in the language modeling approach.
- **Binary independence model.** The [binary independence model](/binary-independence-model/) needs a model of the relevant class, estimated from judged or assumed relevant documents. The relevance model plays the same part for language models, which is the motivation of Lavrenko and Croft.
- **Model-based feedback.** Another estimate of a feedback model fits a mixture of a topic model and the collection model to the feedback documents by [expectation-maximization](/expectation-maximization/), so that common words are explained by the collection and drop out of the topic model. RM1 has no such step and relies on stop word removal or on the cut to $m$ words.
- **Jelinek-Mercer smoothing.** The mixture of RM3 is an interpolation with a fixed weight, as in [Jelinek-Mercer smoothing](/jelinek-mercer-smoothing/), with the query model in the role of the sparse estimate and the relevance model in the role of the background.

## Known results in the model

- **Edge cases.** With $\lambda = 0$, $P'$ is the query model and the second search returns the first ranking. With $k = 1$, $P(d \mid q) = 1$ and RM1 is the model of the single top document.
- **Sharp weights.** The weights $P(d \mid q)$ are ratios of likelihoods, which are products over the query words, so they differ by large factors and the top few documents dominate RM1. In the walk-through, a difference of 1.28 in log likelihood gives document 1 78 percent of the weight.
- **Measured gains.** Lavrenko and Croft reported gains of the relevance model over the query likelihood baseline on TREC collections, and the UMass group used RM3 in its TREC 2004 runs. Its effectiveness relative to other feedback methods is a measured, collection-dependent property, not a theorem.
- **Drift.** As every pseudo-relevance feedback method, RM3 can hurt a query whose top documents are off topic. The weight $1 - \lambda$ on the original query limits this, as the small change in the walk-through shows.

## References
