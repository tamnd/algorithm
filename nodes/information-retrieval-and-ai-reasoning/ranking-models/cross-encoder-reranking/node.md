---
tag: 5X2N43
kind: model
slug: cross-encoder-reranking
name: Cross-encoder reranking
aliases:
- monoBERT reranker
area: information-retrieval-and-ai-reasoning/ranking-models
level: research
summary: Feeds the concatenated query and document to one transformer that outputs a relevance score, used to rerank a short candidate list.
prereqs: [learning-to-rank]
see_also: [dual-encoder-retrieval, colbert, bm25, dense-passage-retrieval, knowledge-distillation, mean-reciprocal-rank, logistic-regression, ranked-retrieval]
sources:
  - paper: "Rodrigo Nogueira and Kyunghyun Cho, Passage re-ranking with BERT, arXiv:1901.04085, 2019"
    locator: the method description (the query truncated to 64 tokens and the pair to 512 tokens, the [CLS] vector fed to a single-layer network that outputs the probability of relevance, the binary cross-entropy loss of Equation (1), and reranking of the BM25 top 1000), Table 1 (measured MRR@10 on MS MARCO)
---

A cross-encoder scores a query $q$ and a document $d$ by reading them together: the input is the joined text "[CLS] $q$ [SEP] $d$ [SEP]", one transformer encodes it so that every query token can attend to every document token, and a small output layer turns the final vector of the [CLS] token into a relevance score. Because the score depends on both texts at once, nothing can be computed before the query arrives, so a cross-encoder is used to rerank a short candidate list from a cheaper first stage such as [BM25](/bm25/) or a [dual encoder](/dual-encoder-retrieval/). The dual-encoder page covers models that encode the two sides separately; this page covers the joint model, what it costs, what reranking can and cannot achieve, and how it was trained in the setting of Nogueira and Cho (2019). The transformer and the quality of its scores are outside this page.

## The machine

The model has three parts.

- **An input pair.** The query, truncated to at most 64 tokens in Nogueira and Cho (2019), and the document, truncated so that the pair with its special tokens fits in 512 tokens.
- **A joint encoder.** A pretrained transformer, BERT in the paper, reads the whole pair. Every layer mixes information across the two texts.
- **An output layer.** The final [CLS] vector $h$ goes through one layer that gives $p(\text{relevant} \mid q, d)$, and the documents of the list are sorted by it. With a sigmoid output, $p = 1/(1 + e^{-(w \cdot h + b)})$.

Training uses labeled pairs and the binary cross-entropy of Equation (1) of the paper,

$$L = -\sum_{j \in J_{\text{pos}}} \log p_j - \sum_{j \in J_{\text{neg}}} \log(1 - p_j),$$

over relevant and nonrelevant candidates. This is [logistic regression](/logistic-regression/) on the [CLS] vector, trained together with the encoder. Reranking then takes the top $c$ candidates of a first stage, $c = 1000$ from BM25 in the paper, scores each pair, and sorts.

## What it counts

The model counts transformer passes. A query with $c$ candidates costs $c$ passes over inputs of up to $\ell = 512$ tokens, and each self-attention layer costs $O(\ell^2 h)$ for width $h$. A dual encoder costs one pass for the query and none for the documents, since their vectors are stored. For $c = 1000$, the cross-encoder runs 1000 passes per query where the dual encoder runs one; this is why it is a reranker and not a first stage.

**A worked case.** BM25 returns four candidates in the order $d_1, d_2, d_3, d_4$, and only $d_3$ is relevant. The cross-encoder gives the logits $(-1.2, 0.3, 2.1, -0.5)$.

| candidate | BM25 rank | logit | $p$ | label | new rank |
|---|---|---|---|---|---|
| $d_1$ | 1 | -1.2 | 0.2315 | 0 | 4 |
| $d_2$ | 2 | 0.3 | 0.5744 | 0 | 2 |
| $d_3$ | 3 | 2.1 | 0.8909 | 1 | 1 |
| $d_4$ | 4 | -0.5 | 0.3775 | 0 | 3 |

The reciprocal rank of the first relevant document rises from $1/3$ to 1, so for this query the [MRR](/mean-reciprocal-rank/) moves from $0.3333$ to $1$. The binary cross-entropy of the four pairs is $-\log(1 - 0.2315) - \log(1 - 0.5744) - \log 0.8909 - \log(1 - 0.3775) = 1.7072$, most of it from $d_2$, the nonrelevant candidate with the highest probability. The cost was four transformer passes for one query.

## Relation to other models

- **Dual encoders.** Encode each side alone and score by an inner product, with precomputed document vectors. The score of a dual encoder of dimension $k$ has rank at most $k$ over queries and documents; a cross-encoder has no such limit.
- **[ColBERT](/colbert/).** Encodes each side alone but keeps token vectors and interacts them late with a sum of maxima. It sits between the two in cost and expressiveness.
- **Feature-based rankers.** [LambdaMART](/lambdamart/) on hand-made features is another reranker of a candidate list; a cross-encoder learns its features from the text, at a far higher cost per pair.
- **[Knowledge distillation](/knowledge-distillation/).** The scores of a cross-encoder are often used as soft targets to train dual encoders and late interaction models.
- **Multi-stage ranking.** Pipelines use a cheap first stage over the collection, a cross-encoder over hundreds of candidates, and sometimes a pairwise or listwise cross-encoder over the top few.

## Known results in the model

**Reranking cannot add documents.** The final list is a permutation of the $c$ candidates. So the recall at depth $c$ of the first stage is an upper bound on the recall of the reranked list at any depth, and for a metric such as MRR@10 the best possible value is the one of the oracle order of the candidates. If no relevant document is among the $c$ candidates of a query, its reciprocal rank stays 0 whatever the cross-encoder does.

**Any order per query.** The score is a function of the pair, so for each query a cross-encoder can in principle give the candidates any order. This is the expressiveness that the low-rank limit of dual encoders lacks. In practice the order is only as good as the trained model, which is measured.

**Truncation.** The input holds at most 512 tokens, so the score of a document depends only on its first $512 - |q| - 3$ tokens, with $|q| \le 64$. Two documents that agree on that prefix get the same score. Long documents need passage splitting and an aggregation such as the maximum over passages.

**Measured effectiveness.** Nogueira and Cho (2019), Table 1, report MRR@10 on MS MARCO passage ranking of 36.5 on the development set and 35.8 on the evaluation set for their BERT Large reranker over the BM25 top 1000, against 16.7 and 16.5 for BM25. These are measurements.

## References
