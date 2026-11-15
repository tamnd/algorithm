---
tag: 47WHK1
kind: algorithm
slug: cori-resource-selection
name: CORI resource selection
aliases:
- collection retrieval inference network
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: advanced
summary: Ranks the collections of a federated search system for a query by a tf-idf style belief computed from each collection's document frequencies and size.
solves: [federated-search]
model: word-ram
complexity:
  vars: {K: the number of collections, m: the number of query terms}
  time: {expected: O(K m + K log K)}
  space: {extra: O(K)}
properties: {deterministic: true, recursive: false}
history:
  year: 1995
  people: [James P. Callan, Zhihong Lu, W. Bruce Croft]
  note: Callan, Lu and Croft introduced CORI at SIGIR 1995; Callan gave the form with the constants 50, 150 and 0.4 in his 2000 survey chapter.
prereqs: [federated-search, tf-idf, bm25]
see_also: [inverted-index, query-likelihood-model, rank-aggregation, combmnz, reciprocal-rank-fusion, ranked-retrieval]
sources:
  - paper: doi:10.1007/0-306-47019-5_5
    title: Jamie Callan, Distributed information retrieval, in W. Bruce Croft (ed), Advances in Information Retrieval, Kluwer Academic Publishers, 2000, Chapter 5, 127-150
    locator: Section 4 (resource selection with the CORI belief, equations 5.1 to 5.4, with b = 0.4) and Section 5 (merging of the result lists); the page uses the formula in this form
  - paper: doi:10.1145/215206.215328
    title: James P. Callan, Zhihong Lu and W. Bruce Croft, Searching distributed collections with inference networks, Proceedings of the 18th Annual International ACM SIGIR Conference (SIGIR 1995), 21-28
    locator: the inference network over collections, with collections in place of documents and document frequency in place of term frequency, and the first experiments on TREC data
  - paper: "Daryl D'Souza, Justin Zobel and James A. Thom, Is CORI effective for collection selection? An exploration of parameters, queries, and data, Proceedings of the 9th Australasian Document Computing Symposium (ADCS 2004)"
    locator: the history of the CORI formula and of its constants (fitted on TREC disk 1 split into collections), and the experiments in which a plain inner product often matched or beat CORI
  - paper: doi:10.1561/1500000010
    title: Milad Shokouhi and Luo Si, Federated search, Foundations and Trends in Information Retrieval 5(1), 1-102 (2011)
    locator: the chapter on collection selection, where CORI is one of the methods that treat each collection as one big document
---

CORI resource selection is a method that ranks the collections of a [federated search](/federated-search/) system for a query, so that the broker sends the query only to the best few. James Callan, Zhihong Lu and Bruce Croft introduced it in 1995 as the collection retrieval inference network. It treats each collection as one large document: the document frequency of a term in the collection plays the part of the term frequency, and the number of collections that contain the term plays the part of the document frequency of [tf-idf](/tf-idf/). The belief formula has three constants, 50, 150 and $b = 0.4$, that were fitted on test data and not derived.

## In plain words

A search broker can send a query to many separate search engines, but asking all of them is slow and costly. So it keeps a short summary of each engine: how many documents it has with each word, and how big it is. For a new query, it gives each engine a score. An engine scores high for a word when many of its documents contain the word, after a correction for the size of the engine. A word that only a few engines have counts more than a word that every engine has. The score of an engine is the average over the query words, and every word adds at least a fixed base amount. The broker then asks only the few engines with the best scores.

## The problem

There are $K$ collections $C_1, \ldots, C_K$, each behind its own search engine. The broker has a description of each collection: $df_i(t)$, the number of documents of $C_i$ that contain the term $t$, and $cw_i$, the number of tokens in $C_i$ (the papers call it the number of words). Let $\overline{cw}$ be the mean of the $cw_i$, and let $c(t)$ be the number of collections that contain $t$. The CORI papers call $c(t)$ the collection frequency, but on this site $cf(t)$ means the number of occurrences of $t$ in a collection, so this page writes $c(t)$. A query $q$ is a bag of $m$ terms. The task is to rank the collections by their expected value for $q$ and return the top $n$, with ties broken by the smaller collection number.

This is the resource selection step of federated search. Building the descriptions (by cooperation, or by query-based sampling when the engines do not cooperate) and merging the result lists are separate steps.

## The algorithm

For a term $t$ with $c(t) \ge 1$, the belief that collection $i$ satisfies $t$ is

$$T = \frac{df_i(t)}{df_i(t) + 50 + 150 \cdot cw_i / \overline{cw}}, \qquad I = \frac{\log\left(\frac{K + 0.5}{c(t)}\right)}{\log(K + 1.0)}, \qquad p(t \mid C_i) = b + (1 - b) \cdot T \cdot I,$$

with $b = 0.4$, the default belief. $I$ is a ratio of two logarithms, so the base does not matter. The score of the collection is the mean belief over the query terms, the #sum operator of the inference network:

```pseudo id=main
CORI-SELECT(q, C_1, ..., C_K, n)            ▷ b = 0.4
L1  for each collection i: cw_i ← number of tokens in C_i
L2  avg ← (cw_1 + ... + cw_K) / K
L3  for each distinct query term t: c(t) ← number of i with df_i(t) > 0
L4  for each collection i:
L5      s_i ← 0
L6      for each query term t, repeats included:
L7          if c(t) = 0 then s_i ← s_i + b; continue
L8          T ← df_i(t) / (df_i(t) + 50 + 150 · cw_i / avg)
L9          I ← log((K + 0.5) / c(t)) / log(K + 1.0)
L10         s_i ← s_i + b + (1 - b) · T · I
L11     s_i ← s_i / m
L12 return the n collections with the largest s_i, ties to the smaller i
```

A term that no collection contains adds $b$ to every score, so it does not change the ranking; line L7 states this rule, which the formula leaves open because $I$ is undefined when $c(t) = 0$. Lines L1 to L3 depend only on the descriptions and the query terms, so a broker computes $cw_i$ and $\overline{cw}$ once and $c(t)$ from a term dictionary.

## Example

Split the eight documents of the shared toy collection of the information retrieval pages into three collections: $C_1 = \{d_1, d_2, d_8\}$ (searching and sorting arrays), $C_2 = \{d_3, d_4, d_5\}$ (posting lists) and $C_3 = \{d_6, d_7\}$. Tokens are the lower-case words. Then $cw = (29, 30, 20)$, $\overline{cw} = 79/3 \approx 26.33$ and $K = 3$.

Take q1, "sorted array search". The term "array" is in the three documents of $C_1$ and in no other collection, so $c = 1$ and $I = \log 3.5 / \log 4 \approx 0.9037$. For $C_1$, $150 \cdot 29 / 26.33 \approx 165.19$, so $T = 3 / (3 + 50 + 165.19) \approx 0.01375$ and $p = 0.4 + 0.6 \cdot 0.01375 \cdot 0.9037 \approx 0.407455$. The term "sorted" is in $C_1$ (3 documents) and $C_2$ (1 document), and "search" in $C_1$ and $C_3$ (1 document each), so for both $c = 2$ and $I = \log 1.75 / \log 4 \approx 0.4037$.

| collection | sorted | array | search | score for q1 |
|---|---|---|---|---|
| $C_1$ | 0.403330 | 0.407455 | 0.401120 | 0.403969 |
| $C_2$ | 0.401092 | 0.400000 | 0.400000 | 0.400364 |
| $C_3$ | 0.400000 | 0.400000 | 0.401469 | 0.400490 |

The ranking is $C_1$, $C_3$, $C_2$. $C_3$ beats $C_2$ because it is smaller: each has one document with one of the rarer query terms, and the size correction favours $C_3$. For q2, "posting list merge", the scores are $0.400373$, $0.404407$ and $0.4$, so $C_2$ comes first. For q4, "quantum circuit", no collection has a query term, every score is $0.4$, and the tie rule gives $C_1$, $C_2$, $C_3$.

All the scores stay close to $b$, because the constants 50 and 150 assume collections with thousands of documents: here $df_i(t) \le 3$ is small next to them. If each collection holds 1000 copies of its documents, the scores for q1 become about $0.7104$, $0.4661$ and $0.4694$, with the same order.

## Correctness

CORI is a scoring formula, so correctness means that the procedure computes the formula and that the formula behaves as its authors intend. The file proofs/correctness.md proves both. Each belief lies in $[b, 1)$, because $0 \le T < 1$ and $0 < I < 1$ when $1 \le c(t) \le K$. The belief grows strictly with $df_i(t)$, falls with the size $cw_i$, and the factor $I$ falls as more collections contain the term. For a one-term query, $I$ and $b$ are the same for every collection, so the ranking depends only on $df_i(t)$ and $cw_i$. The factor $T$ is the term frequency part of [BM25](/bm25/) with $k_1 = 200$ and $b = 0.75$, because $200 \cdot (0.25 + 0.75 \cdot cw_i / \overline{cw}) = 50 + 150 \cdot cw_i / \overline{cw}$. Whether the top collections hold the most relevant documents is a measured property, not a theorem.

## Complexity

Line L3 takes $O(Km)$ lookups in the descriptions, and lines L4 to L11 take $O(Km)$ arithmetic operations and lookups. Line L12 sorts $K$ scores in $O(K \log K)$; a heap gives the top $n$ in $O(K + n \log K)$. With hash tables for the descriptions, a query costs $O(Km + K \log K)$ expected time on the word RAM, and $O(K)$ extra space. The descriptions need one entry for each distinct term of each collection. They are much smaller than the collections, which is the reason to rank collections and not documents at the broker.

## Properties

- **Bounded.** Every score lies in $[0.4, 1)$, and a collection with none of the query terms scores exactly $0.4$.
- **Size-aware.** For the same $df_i(t)$, a larger collection gets a smaller $T$. This keeps a huge collection from winning only because it is huge.
- **Not a probability of relevance.** The beliefs come from an inference network with fitted constants. They rank collections; their values have no direct meaning, and the scores of two queries cannot be compared.
- **Deterministic.** With the tie rule of line L12, equal descriptions give equal output.

## Variants and improvements

- **Sampled descriptions.** When the engines do not export their statistics, the broker estimates $df_i(t)$ and $cw_i$ from documents that it gets back for probe queries. CORI then runs on the estimates. The sampled counts are much smaller than the true counts, so for rare terms $df_i(t)$ is small next to the constants even in large collections, which flattens the scores as in the example.
- **Other constants.** D'Souza, Zobel and Thom explored other values of the constants on other test data, and in their experiments a plain inner product often did as well as CORI or better. They write the size term as $k((1 - b) + b \cdot cw_i/\overline{cw})$ with $k = 200$ and $b = 0.75$, the values fitted on TREC disk 1.
- **Other operators.** The inference network also allows weighted sums and Boolean operators over the term beliefs, in place of the plain mean.
- **Methods that estimate relevant documents.** Later selection methods estimate the number of relevant documents in each collection from a central sample index, which helps when the collections differ much in size. See [federated search](/federated-search/) for these methods.

## When to use it

Use CORI as a cheap and well-known baseline for resource selection when you have term statistics (or samples) for each collection and the collections are of moderate and similar size. Check it against a plain inner product or a sample-based method on your own queries, since the constants were fitted on one test setting and later studies found that CORI is not always the best choice.

## Pitfalls

- **The constants are fitted, not derived.** The values 50, 150 and 0.4 come from experiments on TREC data split into collections. With very small or very unequal collections, they can be a poor fit.
- **Small collections give flat scores.** When $df_i(t)$ is much less than 50, $T$ is close to 0 and all scores stay near $b$, as in the example. Rankings still follow the formula, but the differences are tiny and easily lost to rounding in later steps.
- **The meaning of cw.** The papers define $cw_i$ as the number of words in the collection. Implementations differ on whether that counts tokens or distinct terms. The two choices give different scores; state which one you use.
- **Two meanings of cf.** In the CORI papers, cf is the number of collections that contain a term. In most of information retrieval, cf is the number of occurrences of a term. Mixing them up breaks $I$.
- **An unknown term.** If no collection contains a query term, $I$ is undefined. Give the default belief $b$ to every collection, or drop the term; both keep the ranking.
- **Several published forms.** The 1995 paper used another form of $T$, with a logarithm of $df$ and a default of 0.4 inside $T$. Name the form you use; this page uses the form of Callan's 2000 chapter.

## Implementations

## History

Callan, Lu and Croft presented the method at SIGIR 1995. They built an inference network, as in the INQUERY retrieval system, in which collections take the place of documents. The form of the belief changed over the next years: D'Souza, Zobel and Thom trace an early form with $T = d_t + (1 - d_t) \cdot \log(df + 0.5) / \log(\max df + 1.0)$ and a default $d_t = 0.4$, which was later set to 0, and they report that the constants were fitted on TREC disk 1 split into collections and were not tuned again in later work. Callan's 2000 chapter "Distributed information retrieval" gives the form with 50 and 150 that most later work cites, together with a result merging heuristic. CORI then became the standard baseline of resource selection, and Shokouhi and Si describe it in their 2011 survey of federated search.

## References
