---
tag: H57VVG
kind: model
slug: vector-space-model
name: Vector space model
aliases:
- VSM
- term vector model
area: information-retrieval-and-ai-reasoning/ranking-models
level: intro
summary: Represents documents and queries as weighted term vectors and ranks documents by the cosine of the angle to the query.
prereqs: [tf-idf, cosine-similarity]
see_also: [boolean-retrieval-model, pivoted-length-normalization, bm25, latent-semantic-analysis, rocchio-algorithm, sparse-vector, term-at-a-time-evaluation, maximum-inner-product-search]
sources:
  - paper: doi:10.1145/361219.361220
    title: Gerard Salton, Anita Wong and Chung-Shu Yang, A vector space model for automatic indexing, Communications of the ACM 18(11), 613 to 620, 1975
    locator: documents as vectors of term weights, similarity of vectors, and the density of the document space as a measure of the quality of an indexing vocabulary
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 6 (Section 6.3 on the vector space model and cosine similarity, Section 6.4 on variant weighting functions and the SMART notation)
  - book: isbn:9780321416919
    title: Ricardo Baeza-Yates and Berthier Ribeiro-Neto, Modern Information Retrieval, second edition, Addison-Wesley, 2011
    locator: Chapter 3 (modeling, the vector model)
  - paper: doi:10.1145/243199.243206
    title: Amit Singhal, Chris Buckley and Mandar Mitra, Pivoted document length normalization, Proceedings of SIGIR 1996, 21 to 29
    locator: cosine normalization favors short documents over their probability of relevance
---

The vector space model represents each document and each query as a vector with one coordinate for each term of the vocabulary, whose value is a weight of the term, most often a [tf-idf](/tf-idf/) weight. It ranks the documents by the [cosine similarity](/cosine-similarity/) of their vectors to the query vector. A document that contains only some of the query terms still gets a score, so the model ranks partial matches, which the [Boolean model](/boolean-retrieval-model/) cannot do. The model comes from the SMART system of Gerard Salton, and the paper of Salton, Wong and Yang (1975) is its usual reference.

## The machine

**Vectors.** Let $V$ be the vocabulary of a collection of $N$ documents. A document $d$ is the vector $\vec d \in \mathbb{R}^{|V|}$ with coordinate $w(t, d) \ge 0$ for each term $t$, and $w(t, d) = 0$ when $t$ does not occur in $d$. A query $q$ is a vector $\vec q$ of the same kind. Each vector is sparse: a document has a nonzero coordinate only for its own terms.

**Score.** The score of $d$ for $q$ is the cosine of the angle between the two vectors,

$$s(q, d) = \cos(\vec q, \vec d) = \frac{\vec q \cdot \vec d}{\lVert \vec q \rVert \, \lVert \vec d \rVert} = \sum_{t \in q} \frac{w(t, q)}{\lVert \vec q \rVert} \cdot \frac{w(t, d)}{\lVert \vec d \rVert},$$

and the answer is the list of documents with $s(q, d) > 0$ in decreasing order of score, ties broken by increasing document id. Only the terms of the query contribute to the sum.

**Weights.** The SMART notation names a weighting by three letters for the document and three for the query: term frequency, document frequency and normalization (see [tf-idf](/tf-idf/)). The standard scheme lnc.ltc uses, with $\log_{10}$:

- document: $w(t, d) = 1 + \log_{10} \mathrm{tf}(t, d)$ for $\mathrm{tf} > 0$, no idf, cosine normalization;
- query: $w(t, q) = (1 + \log_{10} \mathrm{qtf}(t, q)) \cdot \log_{10}(N / \mathrm{df}(t))$, cosine normalization.

**Evaluation.** An engine stores $w(t, d)$, or $\mathrm{tf}(t, d)$, in each posting and the norm $\lVert \vec d \rVert$ once for each document. It reads the posting lists of the query terms, adds the products into one accumulator for each document, divides by the norms and keeps the $k$ best scores. This is [term-at-a-time evaluation](/term-at-a-time-evaluation/). The cost is $O(\sum_{t \in q} \mathrm{df}(t))$ for the sums and $O(n \log_2 k)$ to select the top $k$ of $n$ scored documents with a heap.

**Example.** Take query q1 = "sorted array search" on the toy collection of the information retrieval pages, with $N = 8$ and lnc.ltc weights. The document frequencies are 4 for sorted, 3 for array and 2 for search. The query weights are $\log_{10} 2 = 0.301$, $\log_{10}(8/3) = 0.426$ and $\log_{10} 4 = 0.6021$, the query norm is $\sqrt{0.301^2 + 0.426^2 + 0.6021^2} = 0.7966$, and the normalized weights are 0.3779 for sorted, 0.5347 for array and 0.7558 for search.

Document $d_1$ is "binary search finds a key in a sorted array". It has 8 distinct terms, "a" twice and the others once, so its weights are $1 + \log_{10} 2 = 1.301$ for "a" and 1 for the other seven. Its norm is $\sqrt{7 + 1.301^2} = 2.9483$. It holds all three query terms once, so

$$s(q_1, d_1) = \frac{0.3779 + 0.5347 + 0.7558}{2.9483} = 0.5659.$$

| rank | document | query terms in it | norm | score |
|---|---|---|---|---|
| 1 | $d_1$ | sorted, array, search | 2.9483 | 0.5659 |
| 2 | $d_2$ | sorted (twice), array | 3.1133 | 0.3297 |
| 3 | $d_8$ | sorted, array | 3.1623 | 0.2886 |
| 4 | $d_7$ | search | 3.1623 | 0.2390 |
| 5 | $d_4$ | sorted | 3.0636 | 0.1234 |

For $d_2$ the numerator is $1.301 \cdot 0.3779 + 0.5347 = 1.0264$. Document $d_7$ holds only "search" and still ranks above $d_4$, which holds only "sorted", because "search" is in fewer documents and so has a higher idf. On q2 = "posting list merge" the order is $d_4$ (0.4146), then $d_3$ and $d_5$ with the same score 0.3415, so $d_3$ comes first by id, then $d_2$ (0.2031).

## What it counts

- **A ranked list.** The output is an order of the documents, measured by ranked measures such as [precision at k](/precision-at-k/), [mean average precision](/mean-average-precision/) and [nDCG](/normalized-discounted-cumulative-gain/).
- **Postings and accumulators.** The time is the number of postings of the query terms that are read, plus the cost of selecting the top $k$. The extra memory is one accumulator for each document that has a nonzero score.
- **Index space.** One weight, or one term frequency, for each posting, and one norm for each document.

## Relation to other models

- **Boolean model.** With 0-1 weights and a threshold in place of a ranking, the score says only which query terms a document contains. The extended Boolean $p$-norm model of Salton, Fox and Wu sits between the two.
- **Probabilistic models.** A [BM25](/bm25/) score is also a sum over the query terms of a query weight times a document weight, so it is an inner product of two sparse vectors. Its document weight is a saturating function of $\mathrm{tf}$ with its own length correction, and it has no cosine normalization. The vector space model has no notion of relevance as a random event; its weights come from practice.
- **Length normalization.** Cosine normalization makes long documents score too low compared with their rate of relevance. [Pivoted length normalization](/pivoted-length-normalization/) tilts the normalization to correct this.
- **Relevance feedback.** The [Rocchio algorithm](/rocchio-algorithm/) moves the query vector toward the mean vector of the relevant documents and away from the non-relevant ones. It needs the vector view.
- **Latent semantic analysis.** In the term space the vectors of "car" and "automobile" are orthogonal, so a query with one word gives a score of 0 to a document with only the other. [Latent semantic analysis](/latent-semantic-analysis/) maps the vectors into a low-rank space where such terms are close.
- **Dense vectors.** Neural retrieval keeps the geometry and replaces the sparse term vectors by learned dense vectors, as in [dual-encoder retrieval](/dual-encoder-retrieval/). Finding the top $k$ by inner product is then [maximum inner product search](/maximum-inner-product-search/).

## Known results in the model

- **The query norm does not change the order.** $\lVert \vec q \rVert$ is the same positive number for every document, so dividing by it changes all scores by one factor. Engines often skip it.
- **Cosine and distance agree on unit vectors.** If $\lVert \vec q \rVert = \lVert \vec d \rVert = 1$, then $\lVert \vec q - \vec d \rVert^2 = 2 - 2 \cos(\vec q, \vec d)$, so ranking by decreasing cosine is ranking by increasing Euclidean distance.
- **Sums of term scores allow pruning.** The score is a sum of contributions of single terms, each with an upper bound that can be stored with its posting list. This is what lets [WAND](/wand/), [MaxScore](/maxscore/) and the [threshold algorithm](/threshold-algorithm/) find the exact top $k$ without scoring every document.
- **Space density.** Salton, Wong and Yang (1975) observed that an indexing vocabulary works better when it spreads the document vectors apart, and they used the change in the average similarity of documents to judge the value of a term for indexing.
- **Bias of the cosine.** Singhal, Buckley and Mitra (1996) showed on TREC data that the probability of retrieval under cosine normalization falls faster with document length than the probability of relevance does, which is the reason for pivoting.

## References
