---
tag: WX0HDK
kind: definition
slug: bpref
name: Bpref
aliases:
- binary preference measure
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: advanced
summary: Counts, for each relevant document, how many judged nonrelevant documents rank above it, so it is robust to incomplete judgments.
prereqs: [mean-average-precision, pooling]
see_also: [inferred-average-precision, minimal-test-collection, r-precision, test-collection, cranfield-paradigm]
sources:
  - paper: doi:10.1145/1008992.1009000
    title: Chris Buckley and Ellen M. Voorhees, Retrieval evaluation with incomplete information, SIGIR 2004, pp. 25-32
    locator: Section 2 (definitions of bpref and bpref-10), Section 3 and Table 3 (Kendall tau with MAP under complete judgments on TREC-8, TREC-10 and TREC-12), Section 4 (behaviour as judgments are removed)
  - url: https://github.com/usnistgov/trec_eval
    title: trec_eval, the TREC evaluation program by Chris Buckley, maintained by NIST
    locator: file m_bpref.c (1 minus MIN(nonrel_so_far, num_rel) over MIN(num_nonrel, num_rel), with the term 1 when nonrel_so_far is 0, divided by num_rel) and the file bpref_bug
  - url: https://trec.nist.gov/pubs/trec15/appendices/CE.MEASURES06.pdf
    title: Common Evaluation Measures, appendix to the TREC 2006 proceedings, NIST
    locator: section on bpref (the trec_eval 8.0 form differs from the form commonly cited)
---

Bpref scores a ranking by preferences between judged documents only. For each relevant document it counts how many judged nonrelevant documents the ranking puts above it, and documents that nobody judged play no part. Buckley and Voorhees (2004) designed it for test collections whose judgments are far from complete, where [average precision](/mean-average-precision/) counts every unjudged document as nonrelevant. The definition in the paper and the one in trec_eval differ when a query has fewer judged nonrelevant documents than relevant ones.

## Definition

**Input.** A ranking of distinct document ids for one query, with ranks starting at 1, and judgments on a set $J$ of documents. Each judged document has a grade $g(d) \in \{0, 1, 2, \ldots\}$, and it is relevant when $g(d) \ge 1$. $R$ is the number of judged relevant documents and $N$ the number of judged nonrelevant documents. Documents outside $J$ are unjudged, and bpref removes them from the ranking before it does anything else. For a relevant document $r$ in the ranking, let $n_r$ be the number of judged nonrelevant documents ranked above $r$.

**Value (Buckley and Voorhees 2004, Section 2).** When $R \ge 1$,

$$\mathrm{bpref} = \frac{1}{R} \sum_{r} \left( 1 - \frac{\min(n_r, R)}{R} \right),$$

where the sum runs over the relevant documents that the ranking retrieves. The paper says this in words: only the first $R$ judged nonrelevant documents retrieved count.

- Gain: binary, with the threshold $g \ge 1$.
- Discount: a relevant document loses $1/R$ of its credit for each judged nonrelevant document above it, up to $R$ of them. Unjudged documents cost nothing.
- Normalization: division by $R$. A relevant document that is not retrieved adds 0.
- Cutoff: there is no rank cutoff. The count of nonrelevant documents is capped at $R$.
- Ties: tied scores can change the order of a relevant and a judged nonrelevant document, and so the value. This area orders by score descending, then by document id ascending. trec_eval orders tied documents by document number in reverse lexical order.
- No relevant documents ($R = 0$): undefined. Return None and leave the query out of the mean. trec_eval skips the division in this case, reports 0 and counts the query in its mean.

Mean bpref over a set of queries is the arithmetic mean over the queries with $R \ge 1$.

**The trec_eval form.** trec_eval (file m_bpref.c) computes

$$\frac{1}{R} \sum_{r} \left( 1 - \frac{\min(n_r, R)}{\min(N, R)} \right),$$

with the term set to 1 when $n_r = 0$, which also avoids a division by 0 when $N = 0$. The NIST appendix on the TREC measures says that this form, from trec_eval 8.0, differs from the form commonly cited, and the trec_eval sources include a note on it (file bpref_bug).

**Bpref-10.** For queries with few relevant documents, Buckley and Voorhees also define

$$\mathrm{bpref\text{-}10} = \frac{1}{R} \sum_{r} \left( 1 - \frac{\min(n_r, 10 + R)}{10 + R} \right),$$

which counts up to $10 + R$ judged nonrelevant documents above each relevant one.

### Properties

**Claim 1.** If $N \ge R$, the paper form and the trec_eval form give the same value.

*Proof.* With $N \ge R$, $\min(N, R) = R$, so the two terms are equal for $n_r \ge 1$. For $n_r = 0$ both terms are 1. $\square$

When $N < R$, the trec_eval form divides by $N$ and can give a much lower value, as the example below shows.

**Claim 2.** Bpref does not change when unjudged documents are inserted into the ranking, removed from it or moved within it.

*Proof.* The value depends only on $R$, on which relevant documents are retrieved, and on each $n_r$. All of these are defined by the judged documents and their relative order, which those operations do not change. $\square$

Average precision does not have this property: an unjudged document inserted above a relevant one lowers the precision at that rank.

**Claim 3.** $0 \le \mathrm{bpref} \le 1$, and $\mathrm{bpref} = 1$ exactly when all $R$ relevant documents are retrieved and every one of them is above every judged nonrelevant document that is retrieved.

*Proof.* Each term lies in $[0, 1]$ and there are at most $R$ of them, so the value lies in $[0, 1]$. It is 1 exactly when there are $R$ terms and each is 1, that is, $n_r = 0$ for every relevant $r$. $\square$

**Claim 4.** If $N = 0$, bpref is the number of relevant documents retrieved divided by $R$, in both forms.

*Proof.* With no judged nonrelevant document, $n_r = 0$ for every $r$, so each term is 1. $\square$

## Examples and non-examples

### Complete judgments on the toy collection

On the toy collection of this area, query q1 "sorted array search" has the relevant documents d1, d2 and d8. Take all 8 documents as judged, so $R = 3$ and $N = 5$. By Claim 1 the two forms agree.

The fixed run ranks 1, 6, 8, 2, 4. d1 has no nonrelevant document above it, and d8 and d2 have one, d6. So

$$\mathrm{bpref} = \frac{1}{3}\left(1 + \left(1 - \tfrac{1}{3}\right) + \left(1 - \tfrac{1}{3}\right)\right) = \frac{7}{9} \approx 0.7778 .$$

Average precision on the same ranking is $29/36 \approx 0.8056$. The two measures are not equal even with complete judgments.

With the trec_eval order of the tied scores, 6, 1, 8, 4, 2, the counts are $n = 1$ for d1 and d8 and $n = 2$ for d2, so bpref is $(2/3 + 2/3 + 1/3)/3 = 5/9$. A run that ranks 8, 3, 1, 5, 2 has $n = 0, 1, 2$ and bpref $(1 + 2/3 + 1/3)/3 = 2/3$.

### An unjudged document

Suppose d6 was never judged. Bpref removes it, and then no judged nonrelevant document is above any relevant one, so the fixed run gets bpref 1. Average precision still counts d6 as nonrelevant at rank 2 and stays at $29/36$.

### The two forms disagree

Suppose only d1, d2, d8 and d6 are judged, so $R = 3$ and $N = 1$. The unjudged d4 is removed. d8 and d2 each have $n_r = 1$.

| Form | Term for d1 | Terms for d8 and d2 | bpref |
|---|---|---|---|
| Paper, divide by $R = 3$ | 1 | $1 - 1/3$ each | $7/9$ |
| trec_eval, divide by $\min(N, R) = 1$ | 1 | $1 - 1/1 = 0$ each | $1/3$ |

One nonrelevant document above a relevant one costs all of that document's credit in the trec_eval form, and a third of it in the paper form.

### Non-examples

- Average precision computed on the ranking with the unjudged documents removed. This is sometimes called condensed-list AP. It uses the same filtered ranking but weighs each relevant document by the precision at its condensed rank, not by the share of nonrelevant documents above it.
- [Inferred average precision](/inferred-average-precision/). It assumes the judged documents are a random sample of a pool and estimates the AP that complete judgments would give. Bpref does not estimate any other measure.
- A preference measure over all pairs of documents, such as the [Kendall tau distance](/kendall-tau-distance/). Bpref only counts pairs of one judged relevant and one judged nonrelevant document, and caps the count at $R$.

## Related definitions

- [R-precision](/r-precision/) also uses $R$ as the scale: R-precision looks at the first $R$ ranks, and bpref looks at the first $R$ judged nonrelevant documents.
- [Pooling](/pooling/) is the usual source of incomplete judgments. Bpref was built for pools that are too shallow, or for documents added to a collection after the pool was judged.
- [Minimal test collections](/minimal-test-collection/) choose which documents to judge so that a comparison of two systems can be decided with few judgments.

Claims 1 to 4 are proved and hold for every ranking. The claim that bpref is robust to incomplete judgments is a measured one, about how the order of systems changes. Buckley and Voorhees (2004) ran their experiments with bpref-10, because the plain form averages poorly over topics with few relevant documents. They made smaller and smaller random subsets of the judgments of TREC collections and found that the system rankings by bpref-10 stayed closer to the rankings with full judgments than the rankings by MAP, P(10) or R-precision did, whose values fell steadily as judgments were removed. With full judgments, the Kendall tau between the system rankings by bpref-10 and by MAP was 0.934, 0.895 and 0.942 on TREC-8, TREC-10 and TREC-12 (Table 3). These results are for those collections and that way of removing judgments, and they say nothing about one query. A claim that one system has a higher mean bpref than another needs a paired test over the queries, such as the [sign test](/sign-test/) or a [permutation test](/permutation-test/).

## References
