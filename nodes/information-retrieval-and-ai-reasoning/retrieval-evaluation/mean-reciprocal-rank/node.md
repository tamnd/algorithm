---
tag: 52K6S3
kind: definition
slug: mean-reciprocal-rank
name: Mean reciprocal rank
aliases:
- MRR
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: intro
summary: The mean over queries of 1/r, where r is the rank of the first relevant result.
prereqs: [precision-at-k, test-collection]
see_also: [mean-average-precision, expected-reciprocal-rank, normalized-discounted-cumulative-gain, reciprocal-rank-fusion, rank-biased-precision]
sources:
  - paper: "Ellen M. Voorhees, The TREC-8 Question Answering Track Report, in Proceedings of the Eighth Text REtrieval Conference (TREC-8), NIST Special Publication 500-246, 1999, pp. 77-82"
    title: The TREC-8 Question Answering Track Report
    locator: section on evaluation (five ranked responses per question, score is the reciprocal of the rank of the first correct response, 0 if none of the five is correct)
  - url: https://github.com/usnistgov/trec_eval
    title: trec_eval, the TREC evaluation program by Chris Buckley, maintained by NIST
    locator: file m_recip_rank.c (1/(i+1) for the first relevant retrieved document at index i, no cutoff, no value set when no relevant document is retrieved)
  - paper: doi:10.1007/978-3-540-78646-7_38
    title: Frank McSherry and Marc Najork, Computing information retrieval performance measures efficiently in the presence of tied scores, ECIR 2008, LNCS 4956, pp. 414-421
    locator: tie-aware reciprocal rank
  - book: isbn:9780136072249
    title: W. Bruce Croft, Donald Metzler and Trevor Strohman, Search Engines, Information Retrieval in Practice, Addison-Wesley, 2010
    locator: Chapter 8 (reciprocal rank and mean reciprocal rank)
---

Reciprocal rank (RR) scores a ranking by the rank $r$ of its first relevant document: the value is $1/r$, and 0 when the ranking holds no relevant document. Mean reciprocal rank (MRR) is the arithmetic mean of RR over the queries. It models a user who wants one good answer and stops at the first one, so it fits known-item search and question answering. It ignores every relevant document after the first.

## Definition

**Input.** A ranking $d_{(1)}, \ldots, d_{(n)}$ of $n$ distinct document ids, with ranks starting at 1, and graded judgments $g(d) \in \{0, 1, 2, \ldots\}$, where a document that is not judged has $g(d) = 0$. A document is relevant when $g(d) \ge 1$. $R$ is the number of relevant documents in the judgments. An optional cutoff $k$ limits the ranking to its first $k$ ranks.

**Value.** When $R \ge 1$, let $i_1$ be the smallest rank $i \le \min(k, n)$ whose document is relevant. Then

$$\mathrm{RR} = \begin{cases} 1/i_1 & \text{if } i_1 \text{ exists,} \\ 0 & \text{otherwise.} \end{cases}$$

- Gain: binary, with the threshold $g \ge 1$.
- Discount: $1/i$ at the rank of the first relevant document. Every later rank has weight 0, whatever it holds.
- Normalization: none is needed. The best value is 1, reached when rank 1 is relevant.
- Cutoff: trec_eval uses the whole run (file m_recip_rank.c). The TREC-8 question answering track took 5 responses per question, so its score was RR at $k = 5$, with the possible values 0, 1/5, 1/4, 1/3, 1/2 and 1 (Voorhees 1999). Say which $k$ a reported MRR uses.
- Ties: RR changes when a tie group holds the first relevant document and a nonrelevant one. This area orders by score descending, then by document id ascending. trec_eval orders tied documents by document number in reverse lexical order.
- No relevant documents ($R = 0$): undefined. No ranking can do better than 0, so the value says nothing about the system. Return None and leave the query out of the mean. trec_eval sets no value for a query in its judgments file with no relevant document retrieved, so the query counts as 0 in its mean.

**MRR** over $m$ queries with $R \ge 1$ is the arithmetic mean $\frac{1}{m}\sum_q \mathrm{RR}_q$.

**Claim 1.** If every query has a relevant document in its ranking, at ranks $i^{(1)}, \ldots, i^{(m)}$, then MRR is the reciprocal of the harmonic mean of these ranks.

*Proof.* The harmonic mean of $i^{(1)}, \ldots, i^{(m)}$ is $H = m / \sum_q (1/i^{(q)})$. Its reciprocal is $\frac{1}{m}\sum_q 1/i^{(q)}$, which is MRR. $\square$

So MRR is not the reciprocal of the mean rank. For two queries with first relevant ranks 1 and 10, MRR is $(1 + 1/10)/2 = 0.55$, while $1/\text{(mean rank)} = 1/5.5 \approx 0.18$. A single query with a good rank pulls MRR up much more than a bad rank pulls it down.

**Claim 2.** If $R = 1$, RR equals [average precision](/mean-average-precision/).

*Proof.* With one relevant document at rank $i_1$, AP is $\mathrm{P@}i_1 / 1 = 1/i_1$, and both are 0 when that document is not retrieved. $\square$

When $R \ge 2$ the two are not ordered. Relevant documents at ranks 1 and 10 with $R = 2$ give RR 1 and AP $(1 + 2/10)/2 = 0.6$. Relevant documents at ranks 2 and 3 give RR $1/2$ and AP $(1/2 + 2/3)/2 = 7/12$, which is larger.

## Examples and non-examples

### The toy collection

The toy collection of this area has four queries.

| Query | Ranking | First relevant | RR |
|---|---|---|---|
| q1 "sorted array search" | 1, 6, 8, 2, 4 | d1 at rank 1 | 1 |
| q2 "posting list merge" | 8, 5, 1, 4, 2 | d5 at rank 2 | 1/2 |
| q3 "rank documents" | 2, 6, 7, 1, 5 | d7 at rank 3 | 1/3 |
| q4 "quantum circuit" | 1, 2, 3, 4, 5 | none, $R = 0$ | None |

MRR $= (1 + 1/2 + 1/3)/3 = (11/6)/3 = 11/18 \approx 0.6111$. If q4 is kept with the value 0, the mean becomes $11/24 \approx 0.4583$.

On q1, RR is 1 although only one of the three relevant documents is near the top. Average precision on the same ranking is $29/36$, and it would fall if d8 and d2 moved down. RR would not change.

### Ties on q1

The fixed run gives d1 and d6 the same score 2.0. With this area's rule d1 comes first and $\mathrm{RR} = 1$. trec_eval puts d6 first and gets $\mathrm{RR} = 1/2$. The tie-aware value of McSherry and Najork (2008), the mean over both orders, is $(1 + 1/2)/2 = 3/4$.

### Non-examples

- $1/\text{(mean rank of the first relevant document)}$. For the three toy queries the mean rank is $(1 + 2 + 3)/3 = 2$, which gives $1/2$, not $11/18$.
- [Reciprocal rank fusion](/reciprocal-rank-fusion/). It also uses $1/\text{rank}$, but it is a method to merge several rankings into one, with a constant added to each rank. It does not score a ranking against judgments.
- [Expected reciprocal rank](/expected-reciprocal-rank/). It uses graded judgments and a user who may stop at any relevant document with a probability that grows with the grade. With binary grades and certain stopping at the first relevant document it reduces to RR.
- Success at $k$, which is 1 if the first $k$ ranks hold a relevant document and 0 otherwise. It does not separate rank 1 from rank $k$.

## Related definitions

- [Precision at k](/precision-at-k/) counts all relevant documents in the first $k$ ranks; RR looks only at the first one.
- [Average precision](/mean-average-precision/) looks at every relevant document and equals RR when $R = 1$.
- [Normalized discounted cumulative gain](/normalized-discounted-cumulative-gain/) and [rank-biased precision](/rank-biased-precision/) also discount by rank, but sum over all ranks.

RR takes few values, and on a single query a move of the first relevant document from rank 1 to rank 2 halves it. A difference in MRR between two systems is therefore noisy on a small query set. To claim that one system is better, use a paired test over the queries, such as the [sign test](/sign-test/) or a [permutation test](/permutation-test/), and give the number of queries.

## References
