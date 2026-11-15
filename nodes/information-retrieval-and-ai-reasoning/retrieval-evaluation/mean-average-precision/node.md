---
tag: WP8DJA
kind: definition
slug: mean-average-precision
name: Mean average precision
aliases:
- MAP metric
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: core
summary: The mean over queries of average precision, the mean of the precision values at the ranks of the relevant documents.
prereqs: [precision-at-k, precision-and-recall]
see_also: [r-precision, interpolated-precision-recall-curve, mean-reciprocal-rank, normalized-discounted-cumulative-gain, bpref, inferred-average-precision, detection-mean-average-precision, test-collection]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 8, Section 8.4 (mean average precision, and the remark that it approximates the area under the uninterpolated precision-recall curve)
  - url: https://trec.nist.gov/pubs/trec15/appendices/CE.MEASURES06.pdf
    title: Common Evaluation Measures, appendix to the TREC 2006 proceedings, NIST
    locator: sections on average precision (worked example with relevant documents at ranks 1, 2, 4 and 7) and on geometric MAP
  - url: https://github.com/usnistgov/trec_eval
    title: trec_eval, the TREC evaluation program by Chris Buckley, maintained by NIST
    locator: file m_map.c (sum of precision at each relevant retrieved document, divided by num_rel), file m_gm_map.c (log of MAX(AP, MIN_GEO_MEAN)), file form_res_rels.c (order of tied scores)
  - paper: doi:10.1007/978-3-540-78646-7_38
    title: Frank McSherry and Marc Najork, Computing information retrieval performance measures efficiently in the presence of tied scores, ECIR 2008, LNCS 4956, pp. 414-421
    locator: tie-aware average precision, equal to the mean over all orders of the tied documents
  - paper: doi:10.1145/1008992.1009000
    title: Chris Buckley and Ellen M. Voorhees, Retrieval evaluation with incomplete information, SIGIR 2004, pp. 25-32
    locator: Sections 3 and 4 (MAP is not robust when the judgments become much less complete)
  - book: isbn:9780262220736
    title: Ellen M. Voorhees and Donna K. Harman (editors), TREC, Experiment and Evaluation in Information Retrieval, MIT Press, 2005
    locator: Chapter 3, Chris Buckley and Ellen M. Voorhees, Retrieval system evaluation, pp. 53-75
---

Average precision (AP) scores one ranking for one query. It takes the [precision](/precision-and-recall/) at the rank of each relevant document, counts 0 for each relevant document that the ranking does not return, and divides the sum by the number of relevant documents. Mean average precision (MAP) is the arithmetic mean of AP over the queries of a [test collection](/test-collection/). AP is the area under the uninterpolated precision-recall curve, so one number rewards both early precision and high recall.

## Definition

**Input.** A ranking $d_{(1)}, \ldots, d_{(n)}$ of $n$ distinct document ids, with ranks starting at 1, and graded judgments $g(d) \in \{0, 1, 2, \ldots\}$, where a document that is not judged has $g(d) = 0$. A document is relevant when $g(d) \ge 1$. $\mathrm{rel}_i = 1$ when $d_{(i)}$ is relevant, and $\mathrm{P@}i$ is the [precision at](/precision-at-k/) rank $i$. $R$ is the number of relevant documents in the judgments.

**Value.** When $R \ge 1$,

$$\mathrm{AP} = \frac{1}{R} \sum_{i=1}^{n} \mathrm{rel}_i \, \mathrm{P@}i .$$

- Gain: binary, with the threshold $g \ge 1$. A grade 2 document counts the same as a grade 1 document.
- Discount: there is no fixed discount per rank. The relevant document at rank $i$ adds $\mathrm{P@}i / R$, which is smaller when more nonrelevant documents come before it.
- Normalization: division by $R$, the number of relevant documents in the judgments. It is not the number of relevant documents retrieved. A relevant document that is not in the ranking adds 0 to the sum and still counts in $R$.
- Cutoff: none. The whole ranking counts. TREC runs return at most 1000 documents per topic, so the TREC value is in effect AP over the first 1000 ranks.
- Ties: AP depends on the order of tied scores. This area orders by score descending, then by document id ascending. trec_eval orders tied documents by document number in reverse lexical order, and the toy example below shows that this changes AP from 0.8056 to 0.5889.
- No relevant documents ($R = 0$): undefined, because the sum is empty and the divisor is 0. Return None and leave the query out of the mean. trec_eval evaluates only the queries that are in its judgments file. For such a query with no relevant document it reports 0 and counts it in the mean.

**MAP** is the arithmetic mean of AP over the queries with $R \ge 1$. **GMAP**, the geometric mean, is $\exp\big(\frac{1}{m}\sum_{q} \ln \mathrm{AP}_q\big)$ over the same $m$ queries. An AP of 0 makes the logarithm undefined, so implementations put a small floor under AP first; trec_eval takes the log of $\max(\mathrm{AP}, \mathrm{MIN\_GEO\_MEAN})$ (file m_gm_map.c). GMAP gives more weight to the queries where a system does badly. The NIST appendix says that it came from the TREC 2004 robust track.

**Claim 1 (area).** For $r \in (0, 1]$, let $p(r)$ be the precision at the smallest rank whose recall is at least $r$, and let $p(r) = 0$ if no rank of the ranking reaches recall $r$. Then $\mathrm{AP} = \int_0^1 p(r)\,dr$.

*Proof.* Let $i_1 < i_2 < \cdots < i_m$ be the ranks of the relevant documents in the ranking, so $m \le R$. Recall at rank $k$ is (number of relevant documents in the first $k$ ranks)$/R$. It changes only at the ranks $i_j$, where it goes from $(j-1)/R$ to $j/R$. Take $r$ in the interval $((j-1)/R, j/R]$ with $j \le m$. The first rank with recall at least $r$ is the first rank with recall at least $j/R$, which is $i_j$. So $p(r) = \mathrm{P@}i_j = j/i_j$ on that interval. For $j > m$, no rank reaches recall $j/R$, so $p(r) = 0$ on the interval. Each interval has length $1/R$, so

$$\int_0^1 p(r)\,dr = \sum_{j=1}^{m} \frac{1}{R}\,\mathrm{P@}i_j + \sum_{j=m+1}^{R} \frac{1}{R}\cdot 0 = \mathrm{AP}. \quad \square$$

Manning, Raghavan and Schuetze (Section 8.4) state this as an approximation to the area under the uninterpolated curve. With $p$ defined as above, a step function, the equality is exact.

**Claim 2 (range).** $0 \le \mathrm{AP} \le 1$, and $\mathrm{AP} = 1$ exactly when the first $R$ ranks hold all the relevant documents.

*Proof.* With the notation of Claim 1, the $j$-th relevant document is at rank $i_j \ge j$, so $\mathrm{P@}i_j = j/i_j \le 1$. The sum has $m \le R$ terms, each at most 1, so $\mathrm{AP} \le m/R \le 1$. Equality needs $m = R$ and $i_j = j$ for every $j$, that is, the relevant documents fill ranks 1 to $R$. Conversely, such a ranking has every term equal to 1. $\square$

**Claim 3.** If $R = 1$, AP equals the reciprocal rank of the one relevant document, or 0 if it is not retrieved.

*Proof.* The sum has at most one term, $\mathrm{P@}i_1 = 1/i_1$, and $R = 1$. $\square$

So [mean reciprocal rank](/mean-reciprocal-rank/) and MAP agree on a query set where every query has exactly one relevant document.

## Examples and non-examples

### The fixed run on the toy collection

Query q1 "sorted array search" has the relevant documents d1 (grade 2), d2 and d8 (grade 1), so $R = 3$. The fixed run ranks 1, 6, 8, 2, 4 with the tie rule of this area. The relevant documents are at ranks 1, 3 and 4.

| Rank of relevant document | 1 | 3 | 4 |
|---|---|---|---|
| Relevant so far | 1 | 2 | 3 |
| Precision at that rank | 1 | 2/3 | 3/4 |

$$\mathrm{AP} = \frac{1}{3}\left(1 + \frac{2}{3} + \frac{3}{4}\right) = \frac{1}{3}\cdot\frac{29}{12} = \frac{29}{36} \approx 0.8056.$$

By Claim 1, the same number is the area under the step function that is 1 for recall in $(0, 1/3]$, $2/3$ on $(1/3, 2/3]$ and $3/4$ on $(2/3, 1]$: $(1 + 2/3 + 3/4)/3 = 29/36$.

### Ties change AP

The scores tie d1 with d6 at 2.0 and d2 with d4 at 1.0. There are four orders of the tied documents.

| Order | Relevant at ranks | AP |
|---|---|---|
| 1, 6, 8, 2, 4 (this area) | 1, 3, 4 | 29/36 = 0.8056 |
| 1, 6, 8, 4, 2 | 1, 3, 5 | 34/45 = 0.7556 |
| 6, 1, 8, 2, 4 | 2, 3, 4 | 23/36 = 0.6389 |
| 6, 1, 8, 4, 2 (trec_eval) | 2, 3, 5 | 53/90 = 0.5889 |

For the trec_eval order, $\mathrm{AP} = (1/2 + 2/3 + 3/5)/3 = (53/30)/3 = 53/90$. One run file thus gives 0.8056 or 0.5889, depending only on the tie rule. The tie-aware AP of McSherry and Najork (2008) is the mean over the four orders: $(290 + 272 + 230 + 212)/(4 \cdot 360) = 1004/1440 = 251/360 \approx 0.6972$. Their paper shows how to get this mean without listing the orders, which matters when a tie group is large.

### MAP over several queries

| Query | $R$ | Ranking | Relevant at ranks | AP |
|---|---|---|---|---|
| q1 | 3 | 1, 6, 8, 2, 4 | 1, 3, 4 | 29/36 |
| q2 "posting list merge" | 3 | 8, 5, 1, 4, 2 | 2, 4 (d3 missing) | 1/3 |
| q3 "rank documents" | 1 | 2, 6, 7, 1, 5 | 3 | 1/3 |
| q4 "quantum circuit" | 0 | 1, 2, 3, 4, 5 | none | None |

For q2, $\mathrm{AP} = (1/2 + 2/4 + 0)/3 = 1/3$; the 0 is for d3, which the run does not return. For q3 the only relevant document is at rank 3, so $\mathrm{AP} = 1/3$ (Claim 3). q4 is left out.

- MAP $= (29/36 + 1/3 + 1/3)/3 = (53/36)/3 = 53/108 \approx 0.4907$.
- If q4 is wrongly kept with the value 0, the mean becomes $53/144 \approx 0.3681$. The same run file gives two different MAP values, so a report must say how it handles queries with $R = 0$.
- GMAP $= (29/36 \cdot 1/3 \cdot 1/3)^{1/3} \approx 0.4473$, lower than MAP because two of the three values are low.

### Non-examples

- Dividing by the number of relevant documents retrieved. For q2 that gives $(1/2 + 2/4)/2 = 1/2$ instead of $1/3$, so a run that stops early is not punished for the relevant document it never found.
- [Detection mean average precision](/detection-mean-average-precision/) in object detection. It matches predicted boxes to ground-truth boxes by overlap, computes an interpolated precision-recall area per class, and averages over classes. It shares the name but not the input or the formula.
- The 11-point average of the [interpolated precision-recall curve](/interpolated-precision-recall-curve/). For the fixed run on q1 it is $37/44 \approx 0.8409$, not $29/36$, because interpolation takes the maximum precision over later ranks.
- [Normalized discounted cumulative gain](/normalized-discounted-cumulative-gain/), which uses the grades. AP gives d1 (grade 2) and d8 (grade 1) the same weight.

## Related definitions

- [R-precision](/r-precision/) and AP are both normalized by $R$ and both reach 1 only on a ranking with all relevant documents first.
- [Mean reciprocal rank](/mean-reciprocal-rank/) uses only the first relevant document, and equals MAP when $R = 1$ on every query.
- [Bpref](/bpref/) and [inferred average precision](/inferred-average-precision/) are built for judgments that are far from complete. AP counts every unjudged document as nonrelevant.
- AP and MAP are standard targets in [learning to rank](/learning-to-rank/).

What is proved here: Claims 1 to 3, which hold for every ranking. What is only measured: how stable MAP is as a way to order systems, and how it behaves with incomplete judgments. Buckley and Voorhees (2004) report that MAP, P(10) and R-precision become unreliable when the judgments are made much less complete, while bpref stays closer to the ranking of systems under full judgments. A claim that one system has a higher MAP than another needs a paired test over the queries, such as the [sign test](/sign-test/), the [Wilcoxon signed-rank test](/wilcoxon-signed-rank-test/), a [permutation test](/permutation-test/) or a [bootstrap interval](/bootstrap-percentile-interval/), with the number of queries and the p-value.

## References
