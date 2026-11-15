---
tag: ZHMAJD
kind: definition
slug: interpolated-precision-recall-curve
name: Interpolated precision-recall curve
aliases:
- 11-point interpolated average precision
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: core
summary: Plots, at each recall level r, the highest precision reached at any recall at least r, and averages it over standard recall points.
prereqs: [precision-and-recall, precision-at-k]
see_also: [mean-average-precision, r-precision, roc-auc, test-collection]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 8, Section 8.4 (interpolated precision, the sawtooth shape of the raw curve, and the 11-point average)
  - url: https://trec.nist.gov/pubs/trec15/appendices/CE.MEASURES06.pdf
    title: Common Evaluation Measures, appendix to the TREC 2006 proceedings, NIST
    locator: section on interpolated recall-precision averages (interpolated precision at recall level i is the maximum precision at any recall at least i, which also defines a value at recall 0.0)
  - url: https://github.com/usnistgov/trec_eval
    title: trec_eval, the TREC evaluation program by Chris Buckley, maintained by NIST
    locator: file m_iprec_at_recall.c (cutoffs 0.0 to 1.0, each turned into a count of relevant documents with lround(level times num_rel); v9 and earlier added 0.9 and truncated) and file m_11pt_avg.c
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 12 (measuring effectiveness, recall-precision curves)
---

A ranking gives one pair (recall, precision) at each rank. Plotted in order, the raw points make a sawtooth: precision drops at each nonrelevant document and jumps at each relevant one. The interpolated curve replaces the precision at recall level r by the highest precision at any rank whose recall is at least r. The result never goes up as recall grows, it can be read at fixed recall levels, and it can be averaged over queries level by level.

## Definition

**Input.** A ranking $d_{(1)}, \ldots, d_{(n)}$ of distinct document ids for one query, with ranks starting at 1, and graded judgments $g(d) \in \{0, 1, 2, \ldots\}$, where a document that is not judged has $g(d) = 0$. A document is relevant when $g(d) \ge 1$. $R$ is the number of relevant documents in the judgments. Let $r(k)$ be the number of relevant documents in the first $k$ ranks, $P(k) = r(k)/k$ the [precision at](/precision-at-k/) rank $k$, and $\mathrm{rec}(k) = r(k)/R$ the [recall](/precision-and-recall/) at rank $k$.

**Value.** For a recall level $\rho \in [0, 1]$,

$$P_{\mathrm{interp}}(\rho) = \max\,\{\, P(k) : 1 \le k \le n,\ \mathrm{rec}(k) \ge \rho \,\},$$

and $P_{\mathrm{interp}}(\rho) = 0$ when no rank reaches recall $\rho$. At $\rho = 0$ every rank qualifies, so $P_{\mathrm{interp}}(0)$ is the highest precision anywhere in the ranking.

- Gain: binary, with the threshold $g \ge 1$.
- Discount: none.
- Normalization: none beyond precision itself. Recall is normalized by $R$, the relevant documents in the judgments, not only the retrieved ones.
- Cutoff: the curve is read at chosen recall levels, not at ranks. The standard levels are $0, 0.1, 0.2, \ldots, 1.0$. The 11-point average is the arithmetic mean of $P_{\mathrm{interp}}$ at these 11 levels. It is a single number derived from the curve, and it is not the curve.
- Ties: tied scores change the points and so the curve. This area orders by score descending, then by document id ascending. trec_eval orders tied documents by document number in reverse lexical order.
- No relevant documents ($R = 0$): recall is undefined, so the curve is undefined. Return None and leave the query out of the average.

**Averaging over queries.** The curve of a query set is the arithmetic mean, at each recall level, of the values of the queries. The 11-point average of the set is the arithmetic mean of the 11 averaged values, which is the same as the mean of the 11-point averages of the queries.

**trec_eval.** trec_eval (file m_iprec_at_recall.c) does not compare recall with the level directly. It turns each level into a count of relevant documents, $c = \mathrm{lround}(\rho R)$, and takes the maximum precision over the ranks with at least $c$ relevant documents. A count of 0 gets the maximum precision over the whole run, and a count above the number of relevant documents retrieved gets 0. A comment in that file says that version 9 and earlier added 0.9 and truncated instead. Rounding can lower the count below the exact one, and then trec_eval reports a higher value than the definition above. The example below shows a case.

### Properties

**Claim 1.** $P_{\mathrm{interp}}$ is non-increasing on $[0, 1]$.

*Proof.* Let $\rho \le \rho'$. Every rank with $\mathrm{rec}(k) \ge \rho'$ also has $\mathrm{rec}(k) \ge \rho$, so the set for $\rho'$ is a subset of the set for $\rho$. A maximum over a subset is at most the maximum over the whole set. If the set for $\rho'$ is empty, the value at $\rho'$ is 0, which is at most any precision. $\square$

**Claim 2.** $P_{\mathrm{interp}}$ is the smallest function $f : [0, 1] \to [0, 1]$ that is non-increasing and lies on or above every raw point, that is, $f(\mathrm{rec}(k)) \ge P(k)$ for every rank $k$.

*Proof.* First, $P_{\mathrm{interp}}$ has both properties. It is non-increasing by Claim 1, and rank $k$ is in the set for $\rho = \mathrm{rec}(k)$, so $P_{\mathrm{interp}}(\mathrm{rec}(k)) \ge P(k)$.

Next, let $f$ have both properties and take any $\rho$. For each rank $k$ with $\mathrm{rec}(k) \ge \rho$, $f(\rho) \ge f(\mathrm{rec}(k)) \ge P(k)$, the first step because $f$ is non-increasing. Taking the maximum over these $k$ gives $f(\rho) \ge P_{\mathrm{interp}}(\rho)$. If there is no such $k$, then $P_{\mathrm{interp}}(\rho) = 0 \le f(\rho)$. $\square$

So interpolation is not a free choice of smoothing: it is the tightest non-increasing upper envelope of the points. One reading is that a user who wants recall at least $\rho$ can always read on to the rank where precision is highest among those that reach it.

**Claim 3.** The area under the interpolated curve is at least the [average precision](/mean-average-precision/) of the ranking.

*Proof.* On the page on average precision, AP is shown to be $\int_0^1 p(\rho)\,d\rho$, where $p(\rho)$ is the precision at the smallest rank with recall at least $\rho$, or 0 if there is none. That rank is in the set of the definition above, so $p(\rho) \le P_{\mathrm{interp}}(\rho)$ for every $\rho$. Integrate both sides. $\square$

## Examples and non-examples

### The fixed run on the toy collection

Query q1 "sorted array search" has the relevant documents d1, d2 and d8, so $R = 3$. The fixed run ranks 1, 6, 8, 2, 4 with the tie rule of this area.

| Rank $k$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Document | d1 | d6 | d8 | d2 | d4 |
| Recall | 1/3 | 1/3 | 2/3 | 1 | 1 |
| Precision | 1 | 1/2 | 2/3 | 3/4 | 3/5 |

The raw precision goes 1, 1/2, 2/3, 3/4, 3/5: down, up, up, down. The interpolated curve is 1 for $\rho \in [0, 1/3]$, because rank 1 qualifies, and $3/4$ for $\rho \in (1/3, 1]$, because the best rank with recall above $1/3$ is rank 4.

| Level $\rho$ | 0 to 0.3 | 0.4 to 1.0 |
|---|---|---|
| $P_{\mathrm{interp}}(\rho)$ | 1 | 3/4 |

The 11-point average is $(4 \cdot 1 + 7 \cdot 3/4)/11 = 9.25/11 = 37/44 \approx 0.8409$. The average precision of the same ranking is $29/36 \approx 0.8056$. The area under the interpolated curve is $1/3 + (2/3)(3/4) = 5/6 \approx 0.8333$, which is at least AP, as Claim 3 says.

### The same example in trec_eval

With $R = 3$, the level 0.4 gives $\mathrm{lround}(1.2) = 1$, so trec_eval takes the maximum precision over the ranks with at least one relevant document, which is 1 at rank 1. The exact definition needs recall at least 0.4, that is, at least 2 relevant documents, and gives $3/4$. The other ten levels agree. trec_eval's 11-point average is then $(5 \cdot 1 + 6 \cdot 3/4)/11 = 9.5/11 \approx 0.8636$, not $0.8409$.

### Ties

trec_eval reads the tied scores as the order 6, 1, 8, 4, 2. The precisions are 0, 1/2, 2/3, 1/2, 3/5 with recalls 0, 1/3, 2/3, 2/3, 1. The interpolated curve is $2/3$ for $\rho \in [0, 2/3]$ and $3/5$ above, so the levels 0 to 0.6 get $2/3$ and 0.7 to 1.0 get $3/5$. The 11-point average is $(7 \cdot 2/3 + 4 \cdot 3/5)/11 = 106/165 \approx 0.6424$.

### A run that misses a relevant document

For q2 "posting list merge" the relevant documents are d5, d4 and d3, and a run ranks 8, 5, 1, 4, 2. It finds d5 at rank 2 and d4 at rank 4, with precision $1/2$ at both, and never finds d3. The highest recall is $2/3$, so the levels 0.7 to 1.0 get 0. The levels 0 to 0.6 get $1/2$, and the 11-point average is $(7 \cdot 1/2)/11 = 7/22 \approx 0.3182$.

The mean curve of q1 and q2 is $3/4$ at the levels 0 to 0.3, $5/8$ at 0.4 to 0.6 and $3/8$ at 0.7 to 1.0. Its 11-point average is $51/88 \approx 0.5795$, which is also the mean of $37/44$ and $7/22$.

### Non-examples

- The raw points joined by straight lines. This curve is not monotone, and it is not defined at recall 0.
- Straight lines drawn between the points of the relevant ranks. Such a line rises when precision rises, so the curve is not non-increasing, and it is not the envelope of Claim 2.
- The ROC curve of [ROC AUC](/roc-auc/). It plots the true positive rate against the false positive rate, which depends on the number of nonrelevant documents. The precision-recall curve does not use that number.

## Related definitions

- [Average precision](/mean-average-precision/) is the area under the uninterpolated step curve. It is the usual single number today, while older TREC reports also gave the 11-point average.
- [R-precision](/r-precision/) is the point where precision and recall are equal, at rank $R$.
- [Precision at k](/precision-at-k/) reads precision at a rank, while the interpolated curve reads it at a recall level.

Claims 1 to 3 are proved for every ranking. A comparison of two systems by their mean curves at some recall level is a comparison of means over queries, and needs a paired test such as the [Wilcoxon signed-rank test](/wilcoxon-signed-rank-test/) or a [permutation test](/permutation-test/) before it is called significant.

## References
