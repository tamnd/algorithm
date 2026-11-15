---
tag: TRVGYD
kind: technique
slug: tf-idf
name: tf-idf weighting
aliases:
- term frequency-inverse document frequency
- tf.idf
area: information-retrieval-and-ai-reasoning/ranking-models
level: intro
summary: Weights a term in a document by its frequency there times the log of the inverse fraction of documents that contain it.
prereqs: [term-document-incidence-matrix, logarithms]
see_also: [vector-space-model, bm25, pivoted-length-normalization, binary-independence-model, zipfs-law, stop-word-removal, latent-semantic-analysis, inverted-index]
sources:
  - paper: doi:10.1108/eb026526
    title: Karen Sparck Jones, A statistical interpretation of term specificity and its application in retrieval, Journal of Documentation 28(1), 11 to 21, 1972
    locator: the weighting of a query term by a function of the number of documents that contain it, the origin of idf
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 6 (Section 6.2 on term frequency and inverse document frequency, Section 6.4 on sublinear tf scaling, maximum tf normalization and the SMART notation of Section 6.4.3)
  - paper: doi:10.1016/0306-4573(88)90021-0
    title: Gerard Salton and Christopher Buckley, Term-weighting approaches in automatic text retrieval, Information Processing and Management 24(5), 513 to 523, 1988
    locator: the comparison of many combinations of tf, collection frequency and normalization components on several test collections
  - paper: doi:10.1108/00220410410560582
    title: Stephen Robertson, Understanding inverse document frequency, on theoretical arguments for IDF, Journal of Documentation 60(5), 503 to 520, 2004
    locator: idf as an information measure and as the relevance weight of the probabilistic model with no relevance information
---

Tf-idf weighting gives a term $t$ in a document $d$ the weight $\mathrm{tf}(t, d) \cdot \log(N / \mathrm{df}(t))$, where $\mathrm{tf}$ counts the occurrences of $t$ in $d$, $N$ is the number of documents and $\mathrm{df}(t)$ is the number of documents that contain $t$. A term counts more when it occurs often in the document and less when it occurs in many documents of the collection. The idf factor is due to Sparck Jones (1972), and the weights are the coordinates of the [vector space model](/vector-space-model/) and the starting point of [BM25](/bm25/).

## In plain words

A word tells more about a document when the document uses it many times. A word tells less when almost every document uses it, like "the" or "a", because it does not separate one document from the others. Tf-idf multiplies the two effects: how often the word occurs in this document, and a factor that grows as the word gets rarer in the whole collection. The factor is a logarithm, so a word in half of the documents gets a small factor and a word in only one document gets the largest one.

Most systems also damp the count, so that ten uses of a word do not count ten times as much as one use. The weights then go into a sum over the query words, or into a vector for a cosine.

## When it applies

Use tf-idf when:

- documents and queries are bags of words, and the order of words does not matter for the task;
- the score of a document for a query can be a sum over the query terms of a weight for each term;
- there is no information about which documents are relevant, so the weight must come from statistics of the collection;
- the statistics $\mathrm{tf}$ and $\mathrm{df}$ are cheap to get, as they are from an [inverted index](/inverted-index/), which stores $\mathrm{tf}$ in each posting and $\mathrm{df}$ as the length of each list.

Notation: $N$ documents, $\mathrm{tf}(t, d)$ occurrences of $t$ in $d$, $\mathrm{df}(t)$ documents that contain $t$, $\mathrm{qtf}(t, q)$ occurrences of $t$ in the query.

## The template

```pseudo id=main
TFIDF-VECTOR(d, N, df)
L1  for each distinct term t of d do
L2      a ← TF(tf(t, d))                ▷ hole: the term frequency part
L3      g ← IDF(N, df(t))               ▷ hole: the document frequency part
L4      w[t] ← a · g
L5  return NORM(w)                      ▷ hole: the normalization
```

The score of $d$ for $q$ is then $s(q, d) = \sum_{t} w_q[t] \cdot w_d[t]$, where $w_q$ comes from the same template applied to the query, possibly with other choices for the holes. The SMART notation names a choice by one letter for each hole, written for the document and then for the query, as in lnc.ltc (Manning, Raghavan and Schuetze, Section 6.4.3). With $\log$ to one fixed base:

| letter | TF (L2) | letter | IDF (L3) | letter | NORM (L5) |
|---|---|---|---|---|---|
| n | $\mathrm{tf}$ | n | $1$ | n | none |
| l | $1 + \log \mathrm{tf}$ for $\mathrm{tf} > 0$, else 0 | t | $\log(N / \mathrm{df})$ | c | divide by $\sqrt{\sum_t w[t]^2}$ |
| a | $0.5 + 0.5\,\mathrm{tf} / \max_u \mathrm{tf}(u, d)$ | p | $\max(0, \log((N - \mathrm{df}) / \mathrm{df}))$ | u | pivoted unique |
| b | 1 if $\mathrm{tf} > 0$, else 0 | | | b | byte size |
| L | $(1 + \log \mathrm{tf}) / (1 + \log \mathrm{ave}_u \mathrm{tf}(u, d))$ | | | | |

**Walk-through on the toy collection.** The toy collection of the information retrieval pages has $N = 8$. With $\log_{10}$, the idf is $\log_{10}(8/4) = 0.301$ for "sorted", $\log_{10}(8/3) = 0.426$ for "array", $\log_{10}(8/2) = 0.6021$ for "search" and $\log_{10}(8/5) = 0.2041$ for "a". Document $d_2$, "merge sort merges two sorted runs into one sorted array", holds "sorted" twice. Its weight for "sorted" is $2 \cdot 0.301 = 0.602$ in the n-t scheme and $(1 + \log_{10} 2) \cdot 0.301 = 1.301 \cdot 0.301 = 0.3916$ in the l-t scheme.

Score q1 = "sorted array search" with ntn weights for the documents and the weight 1 for each query term, so that $s(q, d) = \sum_{t \in q} \mathrm{tf}(t, d) \log_{10}(N / \mathrm{df}(t))$:

| rank | document | sum | score |
|---|---|---|---|
| 1 | $d_1$ | $0.301 + 0.426 + 0.6021$ | 1.329 |
| 2 | $d_2$ | $2 \cdot 0.301 + 0.426$ | 1.028 |
| 3 | $d_8$ | $0.301 + 0.426$ | 0.727 |
| 4 | $d_7$ | $0.6021$ | 0.602 |
| 5 | $d_4$ | $0.301$ | 0.301 |

The cosine-normalized lnc.ltc scores of the same query are worked out on the [vector space model](/vector-space-model/) page. They give the same order on this query.

## Classic examples

- **[Vector space model](/vector-space-model/).** The tf-idf weights are the coordinates of the document and query vectors, and the cosine is the score. The standard choice is lnc.ltc.
- **[Binary independence model](/binary-independence-model/).** With no relevance information, the relevance weight of a term becomes $\log((N - \mathrm{df}) / \mathrm{df})$, the p letter above, so idf comes out of a probabilistic derivation (Croft and Harper 1979, Robertson 2004).
- **[Pivoted length normalization](/pivoted-length-normalization/).** It replaces the cosine normalization at L5 by a normalization tilted around the average, which is the u letter.
- **[BM25](/bm25/).** It keeps an idf at L3 and replaces the linear tf at L2 by a function that saturates and depends on the length of the document.
- **[Latent semantic analysis](/latent-semantic-analysis/).** It takes the term-document matrix of tf-idf weights and replaces it by a low-rank approximation.

## Variations

- **Sublinear tf.** $1 + \log \mathrm{tf}$ (the l letter) stops a word that occurs 20 times from counting 20 times as much as a word that occurs once. BM25 uses the saturating form $\mathrm{tf}(k_1 + 1)/(\mathrm{tf} + k_1)$, which has a bound.
- **Smoothed idf.** Forms such as $\log((N + 1)/\mathrm{df})$, $\log(1 + N / \mathrm{df})$ and $\ln(1 + (N - \mathrm{df} + 0.5)/(\mathrm{df} + 0.5))$, the last one in Lucene's BM25, stay positive for a term that occurs in every document.
- **Probabilistic idf.** $\log((N - \mathrm{df})/\mathrm{df})$, or $\ln((N - \mathrm{df} + 0.5)/(\mathrm{df} + 0.5))$ with the 0.5 corrections, is 0 for a term in half of the documents and negative above.
- **Maximum tf normalization.** The a letter divides by the largest tf in the document, so that long documents do not get higher weights only because they repeat all their words.
- **Collection frequency.** Some weights use the total count $\mathrm{cf}(t)$ in place of $\mathrm{df}(t)$, as the basic models of [divergence from randomness](/divergence-from-randomness/) do.

## Pitfalls

- **The log base.** With the n letter for tf on both sides, a change of base multiplies every score by one constant and does not change the order. With the l letter it does change the weights, because $1 + \log_{10} \mathrm{tf}$ and $1 + \ln \mathrm{tf}$ are not proportional. Always say which base is used.
- **Terms in every document.** With $\log(N / \mathrm{df})$, a term with $\mathrm{df} = N$ gets weight 0 and disappears from the score. With the p letter, every term in at least half of the documents gets 0, because of the clamp at 0. In the toy collection these are "sorted" ($\mathrm{df} = 4$) and "a" ($\mathrm{df} = 5$).
- **Unknown query terms.** A query term with $\mathrm{df} = 0$ makes $\log(N / \mathrm{df})$ infinite. Drop such terms or smooth the df.
- **Statistics from the wrong collection.** On an index split into shards, each shard has its own $N$ and $\mathrm{df}$, so the same document can get different scores on different shards. Use global statistics, or accept the difference.
- **Raw tf and spam.** With the n letter, a page that repeats a word many times can push itself to the top of the ranking. A sublinear or saturating tf limits this.

## Exercises

1. Compute the ltc weight of "array" in $d_8$ = "the sorted array of ids is compressed with gap encoding", before normalization, with $\log_{10}$. *Answer:* $(1 + \log_{10} 1) \cdot \log_{10}(8/3) = 0.426$.
2. Show that with the scheme ntn.ntn a change of the log base from 10 to $e$ multiplies every score by $(\ln 10)^2$, so the ranking does not change. *Hint:* each score is a sum of terms $\mathrm{qtf} \cdot \mathrm{idf} \cdot \mathrm{tf} \cdot \mathrm{idf}$.
3. Let $d'$ be the document made of two copies of $d_1$. Show that the ntc vectors of $d'$ and $d_1$ are equal, but their ltc vectors are not. *Hint:* the n letter doubles every coordinate, and the l letter maps 1 to 1 and 2 to 1.301.
4. Which terms of the toy collection have a p idf of 0? *Answer:* those with $\mathrm{df} \ge 4$, which are "a" and "sorted".

## References
