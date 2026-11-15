---
tag: 6CDHT4
kind: definition
slug: precision-at-k
name: Precision at k
aliases:
- P@k
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: intro
summary: The fraction of the top k retrieved documents that are relevant.
prereqs: [precision-and-recall, test-collection]
see_also: [r-precision, mean-average-precision, mean-reciprocal-rank, normalized-discounted-cumulative-gain, interpolated-precision-recall-curve, cranfield-paradigm, rank-biased-precision]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 8, Section 8.4 (precision at k, and why it does not average well over queries)
  - url: https://github.com/usnistgov/trec_eval
    title: trec_eval, the TREC evaluation program by Chris Buckley, maintained by NIST
    locator: file m_P.c (P_k divides by k also when fewer than k documents are retrieved) and file form_res_rels.c (tied scores are ordered by document number in reverse lexical order)
  - paper: doi:10.1007/978-3-540-78646-7_38
    title: Frank McSherry and Marc Najork, Computing information retrieval performance measures efficiently in the presence of tied scores, ECIR 2008, LNCS 4956, pp. 414-421
    locator: tie-aware precision, equal to the mean over all orders of the tied documents
  - paper: doi:10.1145/1008992.1009000
    title: Chris Buckley and Ellen M. Voorhees, Retrieval evaluation with incomplete information, SIGIR 2004, pp. 25-32
    locator: Section 3, Table 3 (Kendall tau between the system rankings by MAP and by P(10) on TREC-8, TREC-10 and TREC-12)
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 12 (measuring effectiveness)
---

Precision at k, written P@k, is the number of relevant documents among the first k documents of a ranking, divided by k. It is the [precision](/precision-and-recall/) of the set that a user sees when the user reads the first k results and stops. It needs only the judgments of the top k documents, so it is cheap to measure, but it ignores the order inside the top k and every document below rank k. It is the simplest metric of ranked retrieval on a [test collection](/test-collection/).

## Definition

**Input.** A ranking $d_{(1)}, d_{(2)}, \ldots, d_{(n)}$ of $n$ distinct document ids for a query $q$, with rank $i$ starting at 1, and graded judgments: $g(d) \in \{0, 1, 2, \ldots\}$ for each document, with $g(d) = 0$ for a document that is not judged. A document is relevant when $g(d) \ge 1$. Write $\mathrm{rel}_i = 1$ when $d_{(i)}$ is relevant and $\mathrm{rel}_i = 0$ otherwise. $R$ is the number of relevant documents in the judgments.

**Value.** For an integer cutoff $k \ge 1$,

$$\mathrm{P@}k = \frac{1}{k} \sum_{i=1}^{\min(k, n)} \mathrm{rel}_i .$$

The parts of the definition, in the order of the metric pages of this area:

- Gain: binary. Grade 2 counts the same as grade 1. The threshold is a choice; trec_eval calls it the relevance level and sets it to 1 by default.
- Discount: none. Each of the first $k$ ranks has weight $1/k$, and ranks after $k$ have weight 0.
- Normalization: division by $k$. It is not division by $\min(k, n)$ and not by $\min(k, R)$.
- Fewer than $k$ results: the missing ranks count as nonrelevant, so the divisor stays $k$. This is the trec_eval rule (file m_P.c). A run that returns 4 documents of which 2 are relevant has P@10 = 2/10.
- Ties: the value depends on the order of documents with equal scores when a group of tied documents crosses rank $k$. This area orders by score descending, then by document id ascending. trec_eval orders tied documents by document number in reverse lexical order (file form_res_rels.c), so the two rules can give different values from the same run file.
- No relevant documents ($R = 0$): P@k = 0 for every ranking. The value is defined, but it says nothing about the system, so a mean over queries usually leaves such a query out together with the queries that the other metrics cannot score.

Over a set of queries, mean P@k is the arithmetic mean of the values per query.

**Bounds.** $0 \le \mathrm{P@}k \le \min(k, R)/k$. The upper bound holds because at most $R$ of the first $k$ documents are relevant, and it is reached by every ranking that puts $\min(k, R)$ relevant documents first. So when $R < k$, no system can reach P@k = 1. On a query with $R = 3$, the best possible P@10 is 0.3.

## Examples and non-examples

### The fixed run on the toy collection

The shared toy collection of this area has 8 short documents. Query q1 is "sorted array search", with judgments d1 grade 2, d2 grade 1 and d8 grade 1, so $R = 3$. The fixed run gives the scores d1 2.0, d6 2.0, d8 1.5, d2 1.0, d4 1.0. With the tie rule of this area the ranking is 1, 6, 8, 2, 4, and $\mathrm{rel} = 1, 0, 1, 1, 0$.

| $k$ | 1 | 2 | 3 | 4 | 5 | 10 |
|---|---|---|---|---|---|---|
| relevant in top $k$ | 1 | 1 | 2 | 3 | 3 | 3 |
| P@k | 1 | 1/2 | 2/3 | 3/4 | 3/5 | 3/10 |

P@1 = 1/1 = 1 and P@3 = 2/3. P@10 = 3/10, because the run returns only 5 documents and the divisor stays 10. P@k goes down from rank 1 to rank 2 and up again from rank 2 to rank 4. P@k is not monotone in $k$, but $k \cdot \mathrm{P@}k$, the count of relevant documents seen, never decreases.

### The same run with the other tie rule

d1 and d6 both score 2.0, and d2 and d4 both score 1.0. trec_eval puts the larger document number first inside each tie, so it reads the run as 6, 1, 8, 4, 2 with $\mathrm{rel} = 0, 1, 1, 0, 1$. Then P@1 = 0, P@2 = 1/2, P@3 = 2/3, P@4 = 2/4 = 1/2 and P@5 = 3/5. P@1 moves from 1 to 0 with no change in the scores. P@3 and P@5 do not change, because no tie group crosses rank 3 or rank 5.

The tie-aware value of McSherry and Najork (2008) is the mean of P@k over all orders of the tied documents. For P@1 the two orders of {d1, d6} give 1 and 0, so the tie-aware P@1 is 1/2. For P@3 the value is 2/3 in every order. They show that this mean has a closed form: inside a tie group that crosses rank $k$, each position counts the fraction of relevant documents in the group.

### Query q4

q4 is "quantum circuit". No query term occurs in the collection and $R = 0$. Every ranking has P@k = 0 for every $k$.

### Non-examples

- Precision of a set, $\mathrm{TP}/(\mathrm{TP} + \mathrm{FP})$, as on [precision and recall](/precision-and-recall/). It has no cutoff and no order. P@k is the precision of the set of the first $k$ ranks; it equals set precision only when the run returns exactly $k$ documents.
- "Precision over the documents retrieved", that is, the count of relevant documents in the top $k$ divided by $\min(k, n)$. For the run above with $k = 10$ it gives 3/5, not 3/10. It rewards a run for returning fewer documents. It is not P@k.
- [R-precision](/r-precision/). It is precision at the cutoff $k = R$, which differs from query to query. P@k uses one fixed $k$ for all queries.
- Recall at k, the count of relevant documents in the top $k$ divided by $R$. For q1 at $k = 2$ it is 1/3, while P@2 = 1/2.

## Related definitions

- [Average precision](/mean-average-precision/) is the mean of P@k over the ranks $k$ of the relevant documents, with 0 for each relevant document that is not retrieved. It is sensitive to the order inside the top $k$, which P@k is not.
- [R-precision](/r-precision/) is P@R. At rank $R$ precision equals recall.
- Success at k (also called hit rate at k) is 1 if the top $k$ holds at least one relevant document and 0 otherwise. Its mean over queries is close in spirit to [mean reciprocal rank](/mean-reciprocal-rank/).
- [Normalized discounted cumulative gain](/normalized-discounted-cumulative-gain/) uses the grades and a discount by rank, where P@k uses neither.
- [Rank-biased precision](/rank-biased-precision/) replaces the hard cutoff by a geometric weight on each rank.
- The [interpolated precision-recall curve](/interpolated-precision-recall-curve/) uses the precision at every rank, not only at one cutoff.

Mean P@10 is a common report, but it is a noisy summary. Manning, Raghavan and Schuetze (Section 8.4) point out that it averages badly, because the number of relevant documents differs a lot from query to query, and a query with $R = 3$ has a different scale from a query with $R = 300$. Buckley and Voorhees (2004, Table 3) measured the agreement between system rankings by MAP and by P(10) on three TREC collections with full judgments. The Kendall tau values were 0.813, 0.729 and 0.721, lower than for R-precision (0.916, 0.851 and 0.899). These are measurements on those collections. To claim that one system has a higher mean P@k than another, use a paired test over the queries, such as the [sign test](/sign-test/), the [Wilcoxon signed-rank test](/wilcoxon-signed-rank-test/) or a [permutation test](/permutation-test/), and give the number of queries and the p-value.

## References
