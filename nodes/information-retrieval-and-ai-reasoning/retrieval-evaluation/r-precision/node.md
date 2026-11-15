---
tag: EJW2ZW
kind: definition
slug: r-precision
name: R-precision
aliases:
- R-prec
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: core
summary: Precision at rank R, where R is the number of relevant documents for the query; it equals recall at that rank.
prereqs: [precision-at-k, precision-and-recall]
see_also: [mean-average-precision, interpolated-precision-recall-curve, test-collection, bpref, pooling]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 8, Section 8.4 (R-precision, and its relation to the break-even point)
  - url: https://github.com/usnistgov/trec_eval
    title: trec_eval, the TREC evaluation program by Chris Buckley, maintained by NIST
    locator: file m_Rprec.c (counts the relevant documents in the first MIN(num_ret, num_rel) ranks and divides by num_rel; returns 0 when that minimum is 0)
  - url: https://trec.nist.gov/pubs/trec15/appendices/CE.MEASURES06.pdf
    title: Common Evaluation Measures, appendix to the TREC 2006 proceedings, NIST
    locator: section on R-precision
  - paper: doi:10.1145/1008992.1009000
    title: Chris Buckley and Ellen M. Voorhees, Retrieval evaluation with incomplete information, SIGIR 2004, pp. 25-32
    locator: Section 3, Table 3 (Kendall tau between the system rankings by MAP and by R-precision on TREC-8, TREC-10 and TREC-12)
  - book: isbn:9780262220736
    title: Ellen M. Voorhees and Donna K. Harman (editors), TREC, Experiment and Evaluation in Information Retrieval, MIT Press, 2005
    locator: Chapter 3, Chris Buckley and Ellen M. Voorhees, Retrieval system evaluation, pp. 53-75
---

R-precision is the [precision](/precision-and-recall/) of the first R documents of a ranking, where R is the number of relevant documents for the query. It is [precision at k](/precision-at-k/) with a cutoff that each query sets for itself. At that one rank precision and recall have the same value, so R-precision is also the recall at rank R. A perfect ranking scores 1 on every query, which P@k with a fixed k cannot promise.

## Definition

**Input.** A ranking $d_{(1)}, \ldots, d_{(n)}$ of $n$ distinct document ids for a query, with ranks starting at 1, and graded judgments $g(d) \in \{0, 1, 2, \ldots\}$, where a document that is not judged has $g(d) = 0$. A document is relevant when $g(d) \ge 1$, and $\mathrm{rel}_i = 1$ when $d_{(i)}$ is relevant. $R$ is the number of relevant documents in the judgments, retrieved or not.

**Value.** When $R \ge 1$,

$$\mathrm{Rprec} = \frac{1}{R} \sum_{i=1}^{\min(R, n)} \mathrm{rel}_i .$$

- Gain: binary, with the threshold $g \ge 1$. The grades above 1 are not used.
- Discount: none. The first $R$ ranks have weight $1/R$ each, and the ranks after $R$ have weight 0.
- Normalization: division by $R$. When the run has fewer than $R$ documents, the missing ranks count as nonrelevant and the divisor stays $R$. trec_eval does the same (file m_Rprec.c).
- Cutoff: $k = R$. The cutoff is a property of the query and its judgments, not a parameter of the metric.
- Ties: a group of tied scores that crosses rank $R$ can change the value. This area orders by score descending, then by document id ascending. trec_eval orders tied documents by document number in reverse lexical order, so the two can disagree on the same run file.
- No relevant documents ($R = 0$): undefined, because the cutoff and the divisor are both 0. Return None and leave the query out of the mean. trec_eval does not do this: for a query that is in its judgments file with no relevant document, it reports 0 and counts the query in the mean.

Mean R-precision over a set of queries is the arithmetic mean over the queries with $R \ge 1$.

**Claim 1.** R-precision equals recall at rank $R$.

*Proof.* Let $r$ be the number of relevant documents in the first $\min(R, n)$ ranks. Precision at rank $R$, with the missing ranks counted as nonrelevant, is $r/R$. Recall at rank $R$ is the number of relevant documents in the first $R$ ranks divided by the number of relevant documents, which is $r/R$. The two are the same number. $\square$

**Claim 2.** Let $r(k)$ be the number of relevant documents in the first $k$ ranks, $P(k) = r(k)/k$ and $\mathrm{rec}(k) = r(k)/R$. If $r(k) \ge 1$, then $P(k) = \mathrm{rec}(k)$ holds exactly when $k = R$.

*Proof.* With $r(k) \ge 1$, the equation $r(k)/k = r(k)/R$ divides through to $k = R$. $\square$

So rank $R$ is the only rank where the precision and the recall of a ranking can meet with a nonzero value. Manning, Raghavan and Schuetze (Section 8.4) relate R-precision to the break-even point of the precision-recall curve, where the two are equal.

**Claim 3.** $0 \le \mathrm{Rprec} \le 1$, and $\mathrm{Rprec} = 1$ exactly when the first $R$ ranks hold only relevant documents.

*Proof.* The sum has at most $R$ terms, each 0 or 1, so it lies between 0 and $R$. It equals $R$ exactly when $n \ge R$ and every one of the first $R$ documents is relevant. $\square$

P@k does not have this property: on a query with $R = 3$, no ranking reaches P@10 above 3/10, while every ranking that puts the 3 relevant documents first reaches R-precision 1.

## Examples and non-examples

### The fixed run on the toy collection

On the toy collection of this area, query q1 "sorted array search" has the relevant documents d1 (grade 2), d2 and d8 (grade 1), so $R = 3$. The fixed run, with the tie rule of this area, ranks 1, 6, 8, 2, 4. The first three ranks hold d1 and d8, which are relevant, and d6, which is not. So $\mathrm{Rprec} = 2/3$. Recall at rank 3 is also $2/3$: two of the three relevant documents are found.

The run has two tie groups, {d1, d6} at ranks 1 and 2 and {d2, d4} at ranks 4 and 5. Neither group crosses rank 3, so the trec_eval order 6, 1, 8, 4, 2 gives the same value $2/3$. P@1 on the same run changes from 1 to 0 under the other tie rule.

A run that ranks 1, 2, 8, 7, 4 puts all three relevant documents first and has $\mathrm{Rprec} = 1$.

### Several queries

| Query | $R$ | Ranking | First $R$ ranks | Rprec |
|---|---|---|---|---|
| q1 | 3 | 1, 6, 8, 2, 4 | d1, d6, d8 | 2/3 |
| q2 "posting list merge" | 3 | 8, 5, 1, 4, 2 | d8, d5, d1 | 1/3 |
| q3 "rank documents" | 1 | 2, 6, 7, 1, 5 | d2 | 0 |
| q4 "quantum circuit" | 0 | 1, 2, 3, 4, 5 | none | None |

For q2 the relevant documents are d5, d4 and d3. Only d5 is in the first 3 ranks, so the value is 1/3, though d4 comes at rank 4. For q3 the only relevant document is d7, at rank 3, which is after the cutoff $R = 1$, so the value is 0. q4 has no relevant document, so it is left out, and mean R-precision is $(2/3 + 1/3 + 0)/3 = 1/3$.

### A short run

If the run for q2 returns only d8 and d5, it has $n = 2 < R = 3$. The sum covers the first 2 ranks and finds one relevant document, so $\mathrm{Rprec} = 1/3$, the same as before.

### Non-examples

- Dividing by $\min(R, n)$ instead of $R$. For the short run above it gives 1/2, and it rewards a system for returning fewer documents. That is not R-precision.
- P@3 on all queries. On q1 it agrees with R-precision because $R = 3$, but on q3 ($R = 1$) P@3 is 1/3 and R-precision is 0.
- The break-even point read from an [interpolated precision-recall curve](/interpolated-precision-recall-curve/). Interpolation takes a maximum over later ranks, so the interpolated curve can meet the diagonal at a different value.

## Related definitions

- [Precision at k](/precision-at-k/) fixes one cutoff for all queries. R-precision is P@R.
- [Average precision](/mean-average-precision/) averages the precision at every relevant rank. Both are normalized by $R$, and a ranking scores 1 on both exactly when all relevant documents come first.
- [Bpref](/bpref/) also uses $R$ to bound how many nonrelevant documents it counts, and is built for incomplete judgments.
- The value of $R$ comes from the judgments, so it depends on how the [test collection](/test-collection/) was judged. With [pooling](/pooling/), $R$ counts only the relevant documents that some system found, and the cutoff moves when the pool grows.

Buckley and Voorhees (2004, Table 3) compared the system rankings by MAP with the rankings by other measures on TREC-8, TREC-10 and TREC-12 with full judgments. For R-precision the Kendall tau values were 0.916, 0.851 and 0.899, and for P(10) they were 0.813, 0.729 and 0.721. This is a measurement on those collections, not a property of the definition. A claim that one system has a higher mean R-precision than another needs a paired test over the queries, for example a [permutation test](/permutation-test/) or the [Wilcoxon signed-rank test](/wilcoxon-signed-rank-test/).

## References
