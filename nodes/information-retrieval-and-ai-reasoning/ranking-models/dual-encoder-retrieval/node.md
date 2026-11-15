---
tag: FHA02A
kind: model
slug: dual-encoder-retrieval
name: Dual encoder retrieval model
aliases:
- bi-encoder
- two-tower model
area: information-retrieval-and-ai-reasoning/ranking-models
level: advanced
summary: Encodes queries and items separately into one vector space, so item vectors are precomputed and retrieval is a nearest neighbor search.
prereqs: [embedding, maximum-inner-product-search]
see_also: [dense-passage-retrieval, colbert, splade, cross-encoder-reranking, hnsw, approximate-nearest-neighbor-search, vector-space-model, cosine-similarity]
sources:
  - paper: doi:10.1145/2505515.2505665
    title: Po-Sen Huang, Xiaodong He, Jianfeng Gao, Li Deng, Alex Acero and Larry Heck, Learning deep structured semantic models for web search using clickthrough data, Proceedings of the 22nd ACM CIKM, 2013
    locator: pp. 2333-2338 (an early neural model that maps queries and documents separately to vectors and scores them by their similarity)
  - paper: doi:10.18653/v1/2020.emnlp-main.550
    title: Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen and Wen-tau Yih, Dense passage retrieval for open-domain question answering, Proceedings of EMNLP 2020
    locator: pp. 6769-6781; Section 3.1 and Equation (1) (the inner product of a question vector and a passage vector), Section 5.4 (an index over precomputed passage vectors)
---

A dual encoder scores a query $q$ and an item $d$ by $s(q, d) = \langle E_Q(q), E_D(d) \rangle$, where $E_Q$ and $E_D$ are two encoders into $\mathbb R^k$ that never see each other's input. Because $E_D(d)$ does not depend on the query, all item vectors are computed once, offline, and answering a query is one call of $E_Q$ followed by a [maximum inner product search](/maximum-inner-product-search/) over the stored vectors. The maximum-inner-product-search and [HNSW](/hnsw/) pages are about that search; this page is about the scoring model that produces the vectors: what it costs, what scores it can and cannot express, and how it relates to the other neural ranking models. [Dense passage retrieval](/dense-passage-retrieval/) is one way to train a dual encoder. The encoders themselves, and how good their vectors are, lie outside this model.

## The machine

The model has three parts.

- **Two encoders.** $E_Q$ maps a query and $E_D$ maps an item to a vector in $\mathbb R^k$. They may share weights (a Siamese encoder) or not. Any function is allowed, but it sees only its own input.
- **A similarity.** Usually the inner product $\langle u, v \rangle$; the [cosine similarity](/cosine-similarity/) is the inner product of the normalized vectors. Some systems divide by a temperature during training, which does not change the order of the scores.
- **An index.** The $N$ item vectors are stored, and a query asks for the $K$ items of largest score. An exact search scans all $N$ vectors; an [approximate nearest neighbor](/approximate-nearest-neighbor-search/) index such as HNSW or [product quantization](/product-quantization/) answers faster with some recall loss.

The model splits the work into an offline phase, encoding all items and building the index, and an online phase, encoding one query and searching.

## What it counts

The model counts encoder calls, vector operations and stored numbers.

- **Offline:** $N$ calls of $E_D$, and $N k$ stored numbers, plus the index.
- **Per query:** one call of $E_Q$, and the search, which costs $O(N k)$ for an exact scan plus $O(N \log K)$ to keep the top $K$, or less with an index.
- **Per new item:** one call of $E_D$ and one insertion into the index. Nothing else changes.

A [cross-encoder](/cross-encoder-reranking/), which reads the query and the item together, needs $N$ encoder calls per query for the same full ranking, since nothing can be computed before the query arrives. This gap, one call against $N$, is what makes dual encoders the standard first stage of neural retrieval.

**A worked case.** Take $E_Q(q) = (1, 0.5)$ and three items with $E_D(a) = (2, 0)$, $E_D(b) = (1, 1)$, $E_D(c) = (0, 2)$.

| item | inner product | cosine |
|---|---|---|
| a | 2.0 | 0.8944 |
| b | 1.5 | 0.9487 |
| c | 1.0 | 0.4472 |

By inner product the order is a, b, c; by cosine it is b, a, c. The norm of an item vector acts as a query-independent prior on the item, which the inner product keeps and the cosine removes. A system must train and search with the same similarity.

## Relation to other models

- **[Vector space model](/vector-space-model/) and [BM25](/bm25/).** Classic lexical retrieval is a dual encoder with hand-made sparse vectors: a query vector with one entry per query term and a document vector of term weights, and the [inverted index](/inverted-index/) is its search structure. BM25 is the inner product of a query vector of IDF weights and a document vector of saturated term frequencies.
- **[SPLADE](/splade/).** A learned sparse dual encoder: both encoders output vectors over the vocabulary, most entries zero, scored by the inner product on an inverted index.
- **[ColBERT](/colbert/).** Keeps the separate encoders but outputs one vector per token and scores by a sum of maxima. This is late interaction: more expressive than one inner product, at the cost of storing one vector per token.
- **Cross-encoder.** Reads query and item together and can use any interaction between them. It is more expressive and cannot precompute anything, so it is used to rerank a short list from a dual encoder.
- **[Knowledge distillation](/knowledge-distillation/).** Dual encoders are often trained to match the scores of a cross-encoder, which links the two models in practice.

## Known results in the model

**Low rank.** For $m$ queries and $N$ items, the matrix of scores $S = Q D^\top$ has rank at most $k$. Conversely, any $m \times N$ matrix of rank at most $k$ is the score matrix of some dual encoder of dimension $k$ on these queries and items: factor it as $S = U V^\top$, for example by the singular value decomposition, and let the encoders output the rows of $U$ and $V$. So the dimension $k$ bounds exactly which score tables a dual encoder can reproduce on a fixed set of inputs.

**Few orders of the items.** Fix $N$ item vectors in $\mathbb R^k$. The order of the items for a query vector $u$ changes only when $u$ crosses one of the $M = N(N - 1)/2$ hyperplanes $\{u : \langle u, d_i - d_j \rangle = 0\}$, all through the origin. So the number of distinct orders is at most the number of regions of this arrangement. For $k = 1$ there are at most 2 orders: the items sorted by their single coordinate, upward or downward. For $k = 2$, the direction of $u$ moves on a circle, which the $M$ lines cut into at most $2M$ arcs, so there are at most $N(N - 1)$ orders. For $N = 4$ items that is at most 12 of the 24 orders, and 4 random points in the plane give exactly 12. For general $k$, the standard count of regions of $M$ hyperplanes through the origin bounds the number of orders by $2 \sum_{i=0}^{k-1} \binom{M - 1}{i}$, which is polynomial in $N$ for fixed $k$, while $N!$ is not. A dual encoder of small dimension therefore cannot give every query its own arbitrary order of the items, whatever the encoders are. A query-dependent model such as a cross-encoder has no such limit.

**Exact search is a reduction.** Retrieval under the model is exactly maximum inner product search over $N$ fixed vectors; any guarantee of the search structure, exact or approximate, carries over to the retrieval step and no further, since the vectors may rank relevant items low.

**Measured effectiveness.** How well trained dual encoders retrieve relevant items is an empirical matter. For example, Karpukhin et al. (2020), Table 2, measured a top-20 retrieval accuracy of 78.4 for their dual encoder against 59.1 for BM25 on the Natural Questions test set.

## References
