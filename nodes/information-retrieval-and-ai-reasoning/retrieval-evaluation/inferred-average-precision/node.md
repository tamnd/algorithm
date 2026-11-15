---
tag: A8X4ZP
kind: definition
slug: inferred-average-precision
name: Inferred average precision
aliases:
- infAP
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: research
summary: Estimates average precision from a uniform random sample of the judgment pool. It equals AP under complete judgments and is close to it in expectation, but not exactly unbiased.
prereqs: [mean-average-precision, pooling, random-sampling]
see_also: [bpref, minimal-test-collection, stratified-sampling, estimator-bias, horvitz-thompson-estimator, rank-biased-precision, test-collection]
sources:
  - paper: doi:10.1145/1183614.1183633
    title: Emine Yilmaz and Javed A. Aslam, Estimating average precision with incomplete and imperfect judgments, CIKM 2006, pp. 102-111
    locator: average precision as the expected outcome of a random experiment, and the estimate of the expected precision at each relevant document from a random sample of the pool (inferred AP)
  - paper: doi:10.1007/s10115-007-0101-7
    title: Emine Yilmaz and Javed A. Aslam, Estimating average precision when judgments are incomplete, Knowledge and Information Systems 16(2), 2008, pp. 173-211
    locator: induced AP, subcollection AP and inferred AP, which equal AP under complete judgments and are statistical estimates when a random subset of the pool is judged
  - paper: doi:10.1145/1390334.1390437
    title: Emine Yilmaz, Evangelos Kanoulas and Javed A. Aslam, A simple and efficient sampling method for estimating AP and NDCG, SIGIR 2008
    locator: the extension of inferred AP from uniform samples to stratified samples with different sampling rates (xinfAP), and the inferred form of NDCG
  - url: https://github.com/usnistgov/trec_eval
    title: trec_eval, the TREC evaluation program by Chris Buckley, maintained by NIST
    locator: file m_infap.c (the measure infAP; documents are unpooled, pooled but not judged, judged relevant or judged not relevant; the term of each judged relevant document, with a small constant INFAP_EPSILON, and the division by the number of relevant documents)
---

Inferred average precision (infAP) estimates the [average precision](/mean-average-precision/) of a run when only a random sample of the judgment [pool](/pooling/) has been judged. It reads AP as an expected value: pick a relevant document at random, then pick a document at or above it at random, and ask whether that document is relevant. For each judged relevant document, infAP estimates the precision at its rank from the judged documents above it, counts documents outside the pool as not relevant, and averages the estimates. Yilmaz and Aslam proposed it in 2006. With complete judgments it equals AP. With a sample it is built to be close to AP in expectation when the judged documents are a uniform random sample of the pool, but it is a ratio of random quantities and is not exactly unbiased.

## Definition

**Input.** A ranking $d_1, \ldots, d_n$ for a query, a pool $P$ of documents, and a set $S \subseteq P$ of judged documents, each judged relevant or not relevant. The sample $S$ is drawn uniformly at random from $P$. Every ranked document is in one of four classes: not in the pool, in the pool but not judged, judged relevant, judged not relevant.

**Counts above rank $k$.** For a judged relevant document at rank $k$, let $p_k$ be the number of pool documents above rank $k$, and $r_k$ and $u_k$ the numbers of documents above rank $k$ judged relevant and judged not relevant.

**Estimated precision at rank $k$.** For $k = 1$ the estimate is 1. For $k \ge 2$,

$$\hat{P}_k = \frac{1}{k} + \frac{k - 1}{k} \cdot \frac{p_k}{k - 1} \cdot \frac{r_k + \varepsilon}{r_k + u_k + 2\varepsilon} ,$$

where $\varepsilon$ is a small positive constant. Read it as the random experiment: with probability $1/k$ the picked document is the relevant document itself; otherwise it is one of the $k - 1$ above. Of those, a document outside the pool counts as not relevant, and a document in the pool is relevant with the rate seen among the judged documents above, $r_k/(r_k + u_k)$. The constant $\varepsilon$ keeps the ratio defined when nothing above is judged, and then the ratio is $1/2$.

**The measure.** Let $R_S$ be the number of judged relevant documents of the query. Then

$$\mathrm{infAP} = \frac{1}{R_S} \sum_{\text{judged relevant } d_k} \hat{P}_k .$$

Judged relevant documents that the run does not retrieve add 0 to the sum, as in AP. If no sampled document is relevant, $R_S = 0$ and infAP is undefined. trec_eval computes this formula in file m_infap.c, with the four classes of documents read from the judgments file.

### Properties

**Claim 1.** If every pool document is judged and every relevant document is in the pool, then infAP tends to AP as $\varepsilon \to 0$.

*Proof.* With $S = P$, every pool document above rank $k$ is judged, so $r_k + u_k = p_k$, and the ratio tends to $r_k/p_k$. Then $\hat{P}_k$ tends to $1/k + (1/k) r_k = (r_k + 1)/k$, which is the precision at rank $k$, since the documents outside the pool are not relevant. For $k = 1$ both are 1. $R_S$ is the number of relevant documents $R$. So infAP tends to the mean of the precisions at the relevant documents, with the unretrieved ones as 0, which is AP. $\square$

**Claim 2.** infAP is not an unbiased estimator of AP in general.

*Proof.* The example below has a pool of five documents and a sample of size 3. The mean of infAP over the ten equally likely samples is 0.7542, and AP is 0.8056. $\square$

The causes are easy to name. infAP divides by $R_S$, which is random, so it is a ratio of random sums. The rate $r_k/(r_k + u_k)$ is estimated from few documents near the top. A small sample can contain no relevant document, and then infAP is undefined. See [estimator bias](/estimator-bias/). Yilmaz and Aslam report experiments on TREC data in which the estimates stay close to AP at moderate sample rates; that is a measured property, not a theorem.

## Examples and non-examples

### The fixed run on the toy collection

Query q1 "sorted array search" has the relevant documents d1, d2 and d8. The fixed run ranks 1, 6, 8, 2, 4 with the tie rule of this area, and its AP is $29/36 = 0.8056$. Let the pool be the five ranked documents, and judge a uniform random sample of them.

With the sample $\{2, 4, 6\}$, the only judged relevant document is d2 at rank 4. Above it are the pool documents d1, d6 and d8, so $p_4 = 3$, and of them only d6 is judged, as not relevant, so $r_4 = 0$ and $u_4 = 1$. Then $\hat{P}_4 = 1/4 + (3/4)(3/3) \cdot \varepsilon/(1 + 2\varepsilon) \approx 0.25$, and infAP is 0.25. The sample happened to judge the one document above d2 that is not relevant.

With the sample $\{8\}$, d8 at rank 3 has two pool documents above, d1 and d6, neither judged. The ratio is $1/2$, and $\hat{P}_3 = 1/3 + (2/3)(2/2)(1/2) = 2/3$.

The values of infAP for all ten samples of size 3:

| Sample | {1,2,4} | {1,2,6} | {1,2,8} | {1,4,6} | {1,4,8} | {1,6,8} | {2,4,6} | {2,4,8} | {2,6,8} | {4,6,8} |
|---|---|---|---|---|---|---|---|---|---|---|
| infAP | 1 | 0.8125 | 1 | 1 | 1 | 0.8333 | 0.25 | 0.8333 | 0.4792 | 0.3333 |

The mean over the samples, for each sample size $m$, leaving out the samples with no relevant document:

| $m$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Undefined samples | 2 of 5 | 1 of 10 | 0 | 0 | 0 |
| Mean infAP | 0.7639 | 0.7454 | 0.7542 | 0.7861 | 0.8056 |

The mean is below AP for every partial sample, and it reaches AP only with full judgments.

### Documents outside the pool

Rank 3, 1, 9, 6, 8, 2, 4, 5 with the relevant documents 1, 8, 2 and 5, the pool {1, 2, 3, 4, 5, 6, 8} and d9 outside the pool, so d9 counts as not relevant. AP is 0.475. The mean infAP over all samples of size 2 to 7 is 0.4738, 0.4613, 0.4669, 0.4740, 0.4762 and 0.4750. Here the estimate is close to AP but not monotone in the sample size.

### Non-examples

- AP computed on the judged documents only, with the documents that are not judged removed from the ranking. That is condensed-list AP. It uses no model of the sample and tends to give higher values when many documents are not judged.
- AP with every document that is not judged counted as not relevant. That is the standard trec_eval measure map on incomplete judgments, which tends to fall as the sample gets smaller.
- infAP on a sample that is not uniform, such as the top documents of each run. The rate $r_k/(r_k + u_k)$ then estimates the wrong quantity. For a sample with known but different rates per part of the pool, use the stratified form xinfAP.

## Related definitions

- [Bpref](/bpref/) handles incomplete judgments by comparing judged relevant and judged not relevant documents, and estimates no other measure.
- xinfAP of Yilmaz, Kanoulas and Aslam extends infAP to [stratified samples](/stratified-sampling/), with each part of the pool sampled at its own rate, and the same paper gives an inferred form of NDCG. Weighting each judged document by the inverse of its sampling rate is the idea of the [Horvitz-Thompson estimator](/horvitz-thompson-estimator/).
- The [minimal test collection](/minimal-test-collection/) method picks the documents to judge in order to decide which of two runs is better, instead of sampling them at random.
- [Rank-biased precision](/rank-biased-precision/) reports a residual that bounds the effect of the documents that are not judged.

Claims 1 and 2 are proved. That infAP ranks systems in nearly the same order as AP with full judgments at moderate sample rates is a measured result on TREC collections, not a property that holds for every query.

## References
