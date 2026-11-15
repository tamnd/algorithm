---
tag: 26Y1DV
kind: algorithm
slug: colbert
name: ColBERT late interaction
aliases:
- ColBERT
area: information-retrieval-and-ai-reasoning/ranking-models
level: research
summary: Keeps one embedding per token and scores a document by summing, over query tokens, the maximum similarity to any document token.
solves: [learning-to-rank]
model: word-ram
complexity:
  vars: {n: the number of query vectors, t: the number of token vectors in the collection, c: the number of candidate documents, L: the largest number of tokens in a document, e: the vector dimension}
  time: {stage_one: O(n t e), stage_two: O(c L n e + c log c)}
  space: {extra: O(t e)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2020
  people: [Omar Khattab, Matei Zaharia]
  note: Khattab and Zaharia proposed in 2020 to encode query and document separately with BERT, keep one vector per token, and delay the interaction to a cheap sum of maxima, so that document vectors can be computed offline.
prereqs: [dual-encoder-retrieval]
see_also: [dense-passage-retrieval, cross-encoder-reranking, splade, maximum-inner-product-search, approximate-nearest-neighbor-search, product-quantization, inverted-file-index, top-k-selection]
sources:
  - paper: doi:10.1145/3397271.3401075
    title: Omar Khattab and Matei Zaharia, ColBERT, efficient and effective passage search via contextualized late interaction over BERT, Proceedings of the 43rd ACM SIGIR Conference, 2020
    locator: pp. 39-48; Section 3 and Equation (3) (the sum of maximum similarities, the encoders with [mask] padding of queries and the [Q] and [D] markers, and training with a pairwise softmax loss), Sections 3.6 and 4.1.2 (end-to-end retrieval with a faiss index over token vectors and exact reranking of the candidates), and the experimental evaluation (measured effectiveness and latency)
---

ColBERT scores a query against a document by late interaction. Each side is encoded separately into one vector per token, $q_1, \ldots, q_n$ for the query and $e_{d,1}, \ldots, e_{d,m}$ for document $d$, and the score is

$$S(q, d) = \sum_{i=1}^{n} \max_{j} \, q_i \cdot e_{d,j},$$

the sum over query tokens of their best match in the document. A [dual encoder](/dual-encoder-retrieval/) compresses each side into one vector and scores by one inner product; ColBERT keeps all token vectors, which makes the score more expressive and the index much larger. A [cross-encoder](/cross-encoder-reranking/) lets the query and document tokens attend to each other and cannot precompute anything; ColBERT precomputes all document vectors. This page gives the score, the two-stage retrieval with a token index and exact reranking, when the two stages give the exhaustive answer, a certificate for it, and the training gradient. Search inside the token index is the topic of [maximum inner product search](/maximum-inner-product-search/). The BERT encoders and the quality of their vectors are outside the code here.

## In plain words

We break the question and each document into words and give every word a list of numbers that describes its meaning in context. To score a document, we take each word of the question and find the word of the document that matches it best. We add up these best matches. A document that matches every part of the question well gets a high score. Because the documents are processed once, ahead of time, a search only needs to process the question. To search a large collection, we first find, for each question word, the stored document words that match it best, collect their documents, and then score only those documents exactly.

## The problem

The input is a query, given as $n$ unit vectors $q_1, \ldots, q_n \in \mathbb R^e$, and a collection of $N$ documents, each a list of $m_d \ge 1$ unit vectors, with $t = \sum_d m_d$ token vectors in all. The output is the $k$ documents with the largest $S(q, d)$, highest first, ties to the smaller document id. In the paper, the vectors come from BERT with a linear layer to a smaller dimension and normalization, the query is padded with [mask] tokens to a fixed length $N_q = 32$, and the inner product of unit vectors is the cosine similarity. Exhaustive scoring of all documents costs $O(t n e)$, which is too slow for millions of documents, so retrieval uses two stages.

## The algorithm

```pseudo id=main
COLBERT-RETRIEVE(q_1..q_n, docs, k', k)
L1  index ← every document token vector, with its document id and position
L2  C ← ∅
L3  for each query vector q_i:
L4      add to C the documents of the k' token vectors with the largest q_i · e
L5  for each d ∈ C: S(q, d) ← Σ_i max_j q_i · e_{d,j}
L6  return the k documents of C with the largest S, ties to the smaller id
```

Line L1 is offline. Line L4 is a top-$k'$ inner product search for each query vector; the code does it exactly, and the paper uses an approximate faiss index over the token vectors. Lines L5 and L6 score the candidates exactly. The paper also uses the same score alone to rerank the top 1000 documents of BM25, which is lines L5 and L6 with a given $C$.

## Example

The query has $q_1 = (1, 0)$ and $q_2 = (0, 1)$. Document 0 has the tokens $(0.8, 0.6)$ and $(0.6, 0.8)$, document 1 has $(1, 0)$, and document 2 has $(0, 1)$.

| document | best match for $q_1$ | best match for $q_2$ | $S(q, d)$ |
|---|---|---|---|
| 0 | 0.8 | 0.8 | 1.6 |
| 1 | 1.0 | 0.0 | 1.0 |
| 2 | 0.0 | 1.0 | 1.0 |

The exhaustive top 1 is document 0. With $k' = 1$, line L4 keeps the token $(1, 0)$ of document 1 for $q_1$ and the token $(0, 1)$ of document 2 for $q_2$, so $C = \{1, 2\}$ and line L6 returns document 1: stage 1 misses the best document, because it is good for both query vectors and best for neither. With $k' = 2$, every document is a candidate and the result is document 0. For $k' = 1$, the certificate of the proof file is $\tau_1 + \tau_2 = 1 + 1 = 2$, and the returned score 1.0 is below it, so the result is correctly not certified. In training, the pairwise loss of document 0 as the positive and document 1 as the negative is $\log(1 + e^{1.0 - 1.6}) = 0.4375$.

## Correctness

The proof in proofs/correctness.md shows:

- **Score.** The code computes $S$, and $-n \le S \le n$ for unit vectors. The tests compare it with a plain double loop.
- **A superset is enough.** If the candidate set $C$ contains the exhaustive top $k$, lines L5 and L6 return it in the exhaustive order. In particular, when $k'$ is at least the number of tokens, $C$ is the whole collection and end-to-end retrieval equals exhaustive late interaction. The tests check both on random collections.
- **Stage 1 can miss.** For smaller $k'$ this fails in general, as in the example.
- **A certificate.** With $\tau_i$ the $k'$-th largest $q_i \cdot e$ over all tokens, every document outside $C$ has $S \le \sum_i \tau_i$. So if the $k$-th returned score exceeds $\sum_i \tau_i$, the result is exactly the exhaustive top $k$.
- **Training gradient.** For the pairwise softmax loss, the gradient in $q_i$ flows only to the winning token of each document, $\partial \ell / \partial q_i = (p^+ - 1) e_{d^+, j^+(i)} + (1 - p^+) e_{d^-, j^-(i)}$, where the maxima are unique. The tests check it by finite differences.

These are statements about the given vectors and an exact stage 1. The quality of the ranking is measured: Khattab and Zaharia (2020) report MRR@10 on the MS MARCO passage development set of 34.9 when reranking the BM25 top 1000 and 36.0 for end-to-end retrieval, against 16.7 for BM25, and much lower latency than reranking with a BERT cross-encoder. These are measurements.

## Complexity

Line L1 stores $t$ vectors of dimension $e$, $O(t e)$ space, which is the main cost of the method: one vector per token rather than one per document. Stage 1 with an exact scan costs $O(n t e)$, plus the selection of the top $k'$ for each query vector; an approximate index makes it sublinear in $t$. Stage 2 scores $c = |C| \le n k'$ documents of at most $L$ tokens each, $O(c L n e)$, and sorts them in $O(c \log c)$. A cross-encoder over the same $c$ documents needs $c$ full transformer passes over the joined text, which is much more expensive per document than $L n$ inner products.

## Properties

- **Decomposable.** The score is a sum over query tokens, so one strong match cannot make up for a missing query term, and each query token adds at most 1.
- **Precomputable.** Document vectors do not depend on the query; adding a document needs one encoder pass and an index update.
- **Order-free inside the document.** The maximum ignores where in the document the match is, except through the contextual vectors.
- **Exact given the candidates.** Stage 2 is exact, so all error of end-to-end retrieval comes from stage 1 and from the encoders.
- **Sparse gradient.** Each query vector trains only the winning token of each document in the pair.

## Variants and improvements

- **Compressed token vectors.** Later versions store each token vector as a centroid id plus a quantized residual, which cuts the index size several times; see [product quantization](/product-quantization/).
- **Centroid-based candidate generation.** Group token vectors by cluster, as in an [inverted file index](/inverted-file-index/), and gather candidates by the clusters nearest each query vector.
- **Distillation.** Train the late interaction scores to match a cross-encoder.
- **Single-vector reduction.** Mean pooling of the token vectors gives a plain dual encoder, with the cost and expressiveness of one inner product.
- **Learned sparse alternative.** [SPLADE](/splade/) keeps one sparse vector per document and runs on an inverted index.

## When to use it

Use ColBERT when a single vector per document loses too much, for example for long or multi-aspect queries, and the index can afford one vector per token. It sits between a dual encoder and a cross-encoder in both cost and expressiveness, and it can be the first stage or a reranker. When storage is tight, a single-vector dual encoder or a sparse model is cheaper. Whether its accuracy gain is worth the index size on a given collection is a matter of measurement.

## Pitfalls

- **Too small $k'$.** Line L4 with a small $k'$ misses documents that are good for every query vector and best for none, as in the example. Use the certificate, or a larger $k'$, to detect it.
- **Unnormalized vectors.** The bounds and the cosine reading need unit vectors. Long, unnormalized token vectors in line L1 let a single token dominate the maximum.
- **Ties in the maximum.** At a tie between two document tokens, the gradient of line L5 is not unique. Fix a rule, such as the first token, so that training is reproducible.
- **Mixing exact and approximate.** Line L4 with an approximate index can miss tokens even for large $k'$; the superset argument then does not hold. Compare against exact search when testing.
- **Punctuation and padding.** The paper filters punctuation from documents and pads queries with [mask] tokens. Changing either changes the set of vectors in lines L1 and L3 and the scores.

## Implementations

## History

Khattab and Zaharia (2020) introduced ColBERT to close the gap between fast dual encoders and accurate but slow BERT rerankers. They kept the independence of the two encoders, so that documents can be encoded offline, and moved the interaction to a cheap sum of maxima over token vectors, with a faiss index for end-to-end retrieval. Later work compressed the token vectors and replaced the candidate stage with centroid search, which made late interaction practical on larger collections.

## References
