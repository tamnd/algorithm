---
tag: 669YF6
kind: model
slug: splade
name: SPLADE
aliases:
- sparse lexical and expansion model
area: information-retrieval-and-ai-reasoning/ranking-models
level: research
summary: Learns sparse term weights over the whole vocabulary from a masked language model, so learned expansions run on an inverted index.
prereqs: [inverted-index, dual-encoder-retrieval]
see_also: [bm25, sparse-vector, posting-list, wand, block-max-wand, pseudo-relevance-feedback, colbert, dense-passage-retrieval]
sources:
  - paper: doi:10.1145/3404835.3463098
    title: Thibault Formal, Benjamin Piwowarski and Stéphane Clinchant, SPLADE, sparse lexical and expansion model for first stage ranking, Proceedings of the 44th ACM SIGIR Conference, 2021
    locator: pp. 2288-2292; Equation (1) (the importance of vocabulary term j for input token i, from the masked language model head), Equation (4) (the document weight as a sum over tokens of log(1 + ReLU)), the dot product score, the FLOPS regularizer as a sum of squared mean weights, Equation (6) (the ranking loss plus the query and document regularizers), Table 1 (measured effectiveness)
  - paper: "Thibault Formal, Carlos Lassance, Benjamin Piwowarski and Stéphane Clinchant, SPLADE v2, sparse lexical and expansion model for information retrieval, arXiv:2109.10086, 2021"
    locator: the change from sum pooling to max pooling over the input tokens
---

SPLADE is a [dual encoder](/dual-encoder-retrieval/) whose vectors live in the vocabulary of a masked language model, about 30,000 terms, and are mostly zero. For each input token $i$ and each vocabulary term $j$, the masked language model head gives a logit $w_{ij}$; SPLADE turns these into one nonnegative weight per term, $w_j = \sum_i \log(1 + \mathrm{ReLU}(w_{ij}))$, and scores a query against a document by the inner product of their weight vectors. A term can get weight even if it does not occur in the text, which is a learned expansion, and the weights are learned, unlike the hand-made weights of [BM25](/bm25/). Because the vectors are sparse and nonnegative, retrieval runs on an ordinary [inverted index](/inverted-index/). The dual-encoder page covers dense vectors and nearest neighbor search; this page covers the sparse model: its weights, its cost on an inverted index, the regularizer that controls that cost, and a worked case. The language model and the quality of its weights are outside this page.

## The machine

The model has four parts.

- **An encoder with a vocabulary head.** A masked language model reads the text and, for every input position $i$, gives a logit $w_{ij}$ for every vocabulary term $j$, with $|V| = 30522$ for the BERT vocabulary used in the paper. In Equation (1) of Formal, Piwowarski and Clinchant (2021), $w_{ij} = \mathrm{transform}(h_i)^\top E_j + b_j$, with $h_i$ the hidden state of token $i$ and $E_j$ the input embedding of term $j$.
- **Pooling.** The weight of term $j$ for the text is $w_j = \sum_i \log(1 + \mathrm{ReLU}(w_{ij}))$, Equation (4). The ReLU makes most weights exactly 0, and the logarithm damps large logits. SPLADE v2 replaces the sum over $i$ by a maximum.
- **A score.** $s(q, d) = \sum_j w_j^{q} w_j^{d}$, the inner product of the two sparse vectors.
- **An index.** Each term with a nonzero document weight gets a [posting list](/posting-list/) of (document, weight) entries. A query reads only the posting lists of its own nonzero terms.

Training minimizes $L = L_{\text{rank}} + \lambda_q L^{q}_{\text{reg}} + \lambda_d L^{d}_{\text{reg}}$, Equation (6): a softmax ranking loss over a positive and negatives, as in [dense passage retrieval](/dense-passage-retrieval/), plus a sparsity regularizer for each side. The regularizer is the FLOPS loss $\sum_j \bar a_j^2$, where $\bar a_j$ is the mean weight of term $j$ over the documents of a batch. The paper raises $\lambda$ from 0 quadratically over the first 50,000 steps.

## What it counts

The model counts the work of an inverted index: the number of postings read and multiplied for a query. If $Q$ is the set of terms with nonzero query weight and $n_j$ is the number of documents with nonzero weight for term $j$, an exact query by term-at-a-time accumulation reads $\sum_{j \in Q} n_j$ postings. Dynamic pruning such as [WAND](/wand/) and [block-max WAND](/block-max-wand/) can skip postings that cannot reach the top $k$, since all weights are nonnegative and each list has a known maximum.

Expansion has a cost: every extra term in a document lengthens one posting list, and every extra term in a query adds one list to read. A term that is active in a large fraction $p_j$ of the documents costs about $p_j N$ postings each time a query uses it. The FLOPS regularizer pushes down $\bar a_j$, which is large exactly for such terms, more than a plain L1 penalty would. This is why it penalizes the mean weight squared rather than the sum.

**A worked case.** Take a vocabulary of five terms, cat, dog, pet, car and the, with the logits of all other terms negative. Document A has two tokens with the logits $(2.0, 0.5, 1.2, -1.0, -0.5)$ and $(0.3, -0.2, 0.8, -2.0, 1.5)$ over the five terms; document B has one token with $(-1, -1, -0.3, 2.5, 0.2)$; the query has one token with $(0.4, 0.9, 1.5, -1, -1)$.

| | cat | dog | pet | car | the |
|---|---|---|---|---|---|
| document A | 1.3610 | 0.4055 | 1.3762 | 0 | 0.9163 |
| document B | 0 | 0 | 0 | 1.2528 | 0.1823 |
| query | 0.3365 | 0.6419 | 0.9163 | 0 | 0 |

Each entry is the sum of $\log(1 + \max(0, w_{ij}))$ over the tokens; for example, cat in document A is $\log 3 + \log 1.3 = 1.3610$. The scores are $s(q, A) = 0.3365 \cdot 1.3610 + 0.6419 \cdot 0.4055 + 0.9163 \cdot 1.3762 = 1.9792$ and $s(q, B) = 0$. Document A gets weight on "pet" and "dog" from its context, so the query matches it through the expanded terms. With max pooling, as in SPLADE v2, $s(q, A) = 1.3524$. For the batch $\{A, B\}$, the FLOPS loss is $\sum_j \bar a_j^2 = 1.6718$, while the L1 norm of the two documents is $5.4941$. The query reads three posting lists, cat, dog and pet, each with one entry here; the list of "the" has two entries and is not read, since its query weight is 0. The softmax loss with A as the positive and B as the negative is $\log(1 + e^{0 - 1.9792}) = 0.1294$.

## Relation to other models

- **BM25 and the [vector space model](/vector-space-model/).** Also inner products of sparse vectors over terms, with weights from term frequencies and IDF. SPLADE learns the weights and can activate terms that the text does not contain.
- **[Pseudo-relevance feedback](/pseudo-relevance-feedback/) and document expansion.** Classic expansion adds terms from retrieved documents at query time or from predicted queries at indexing time. SPLADE learns expansion inside the encoder, for both sides at once.
- **Dense dual encoders.** Same factorization of the score, but dense vectors of a few hundred dimensions need nearest neighbor indexes, while SPLADE vectors use an inverted index and have one interpretable dimension per term.
- **[ColBERT](/colbert/).** Keeps many dense vectors per document; SPLADE keeps one sparse vector.
- **Weighting without expansion.** Restricting $w_j$ to the terms of the text gives a learned term weighting model; SPLADE is that plus expansion over the whole vocabulary.

## Known results in the model

**Exact retrieval on an inverted index.** The score is $\sum_{j \in Q} w^q_j w^d_j$, so it depends only on the posting lists of the query's nonzero terms. Accumulating over those lists gives the exact score of every document with at least one shared term, and every other document has score 0. Since all weights are nonnegative, the maximum of each list bounds its contribution, which is what WAND and block-max WAND need to skip documents and still return the exact top $k$.

**Saturation.** Each token adds $\log(1 + \mathrm{ReLU}(w_{ij}))$ to term $j$, which grows only logarithmically in the logit, so one confident token cannot give a term an unbounded weight. With sum pooling, a term that many tokens support grows with the number of tokens, like a term frequency; with max pooling it does not.

**Sparsity is a trained property, not a guarantee.** The ReLU gives exact zeros, but the number of nonzero entries depends on the weights and on $\lambda_q$ and $\lambda_d$. Nothing in the model bounds the posting list lengths, so query cost must be measured on the collection.

**Measured effectiveness.** Formal, Piwowarski and Clinchant (2021), Table 1, report MRR@10 of 0.322 on the MS MARCO passage development set, against 0.184 for BM25 in their table. These are measurements.

## References
