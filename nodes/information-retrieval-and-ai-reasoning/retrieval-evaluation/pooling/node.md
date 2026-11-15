---
tag: HRM0F7
kind: technique
slug: pooling
name: Pooling
aliases:
- depth-k pooling
- TREC pooling
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: core
summary: Judges only the union of the top k documents of each participating system and treats unjudged documents as not relevant.
prereqs: [test-collection, precision-at-k]
see_also: [cranfield-paradigm, mean-average-precision, bpref, inferred-average-precision, minimal-test-collection, stratified-sampling, multi-armed-bandit]
sources:
  - paper: "Karen Sparck Jones and C. J. van Rijsbergen, Report on the need for and provision of an 'ideal' information retrieval test collection, British Library Research and Development Report 5266, Computer Laboratory, University of Cambridge, 1975"
    title: Report on the need for and provision of an 'ideal' information retrieval test collection
    locator: the proposal to judge a pool of documents found by several search strategies, made for a collection that was never built
  - book: isbn:9780262220736
    title: Ellen M. Voorhees and Donna K. Harman (editors), TREC, Experiment and Evaluation in Information Retrieval, MIT Press, 2005
    locator: Chapter 2, Donna K. Harman, The TREC test collections (how the TREC pools were built and judged)
  - paper: "Justin Zobel, How reliable are the results of large-scale information retrieval experiments?, Proceedings of the 21st Annual International ACM SIGIR Conference on Research and Development in Information Retrieval, Melbourne, 1998, pp. 307-314"
    title: How reliable are the results of large-scale information retrieval experiments?
    locator: abstract and the sections on pool depth and pool bias (relative system performance appears reliable, recall is overestimated, many relevant documents are not found; a new pooling strategy)
  - paper: doi:10.1145/290941.291009
    title: Gordon V. Cormack, Christopher R. Palmer and Charles L. A. Clarke, Efficient construction of large test collections, SIGIR 1998, pp. 282-289
    locator: move-to-front pooling and interactive searching and judging
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 8, Section 8.5 (assessing relevance, pooling)
  - paper: doi:10.1561/1500000009
    title: Mark Sanderson, Test collection based evaluation of information retrieval systems, Foundations and Trends in Information Retrieval 4(4), 2010, pp. 247-375
    locator: the sections on pooling, pool depth and pool bias
---

Pooling builds the judgments of a [test collection](/test-collection/) when the collection is too large to judge every document for every topic. Each participating system submits a ranking per topic, the top k documents of all rankings are merged into one pool, and only the pool is judged, while documents outside it count as not relevant. The method makes TREC-scale collections possible, but the judgments it gives are incomplete in a way that depends on which systems took part.

## In plain words

A large collection has far too many documents to judge for each topic. Pooling asks every system that takes part to submit its ranking. It takes the top documents of each ranking, merges them into one set with no repeats, and has people judge only that set. A document outside the set is treated as not relevant. The bet is that a document no system put near the top would change the scores of those systems very little. The set is chosen by the systems, not at random. So it can miss relevant documents that a new system finds, and then the new system looks worse than it is.

## When it applies

- The collection is too large to judge every document, but a few hundred judgments per topic are affordable.
- Several runs that differ in method are available for each topic. The more they differ, the more relevant documents the pool finds.
- The metrics of interest look mainly at the top ranks, such as [precision at k](/precision-at-k/) with $k$ at most the pool depth.
- The aim is to compare the systems that contributed to the pool. Scoring a new system later on the same judgments is possible, but less safe.

It does not apply when the pool must estimate the true number of relevant documents, for example for an absolute recall figure. A pool only gives a lower bound for that number.

## The template

Input: a set of topics, and runs $S_1, \ldots, S_m$, each a ranking of documents per topic. A pool depth $k$.

1. For each topic $q$, form the pool $P_q = \bigcup_{j=1}^{m} \mathrm{top}_k(S_j, q)$, the union of the first $k$ documents of each run.
2. Shuffle $P_q$, or sort it by document id, so that the assessor does not see which system found a document or at which rank.
3. Judge every document in $P_q$ for topic $q$, on a binary or graded scale.
4. Give every document outside $P_q$ the grade 0.
5. Score every run with the chosen metrics on these judgments.

**Cost.** $|P_q| \le mk$, with equality when the top $k$ sets of the runs do not overlap. When all runs have the same top $k$ set, $|P_q| = k$. Real runs overlap a lot, so the pool is much smaller than $mk$.

**Claim.** Let $S$ be a run that contributed to the pool. For any $j \le k$, the value of P@j for $S$ on the pooled judgments equals its value on complete judgments that agree with the pool on the pooled documents.

*Proof.* P@j depends only on the grades of the first $j$ documents of $S$. These are in $\mathrm{top}_k(S, q) \subseteq P_q$, so they are judged, and complete judgments give them the same grades. $\square$

The claim holds for every metric that depends only on the grades of the first $k$ ranks, such as DCG@k. It does not hold for metrics that use $R$, the number of relevant documents: [average precision](/mean-average-precision/), [R-precision](/r-precision/) and nDCG all use $R$ or the ideal ranking, and a pool can miss relevant documents below depth $k$ of every run. It also does not hold for a run that did not contribute to the pool.

## Classic examples

### The toy collection

On the toy collection of this area, query q1 "sorted array search" has the relevant documents d1 (grade 2), d2 and d8 (grade 1) under complete judgments. Two runs take part:

- run A ranks 1, 6, 8, 2, 4;
- run B ranks 1, 2, 8, 7, 4.

At depth $k = 2$ the pool is $\{d1, d6\} \cup \{d1, d2\} = \{d1, d2, d6\}$. The assessor finds d1 and d2 relevant and d6 not relevant. d8 is relevant but is at rank 3 in both runs, so it is not in the pool and counts as not relevant. The pool has $R = 2$, while the true value is 3.

| Run | AP, pooled at depth 2 | AP, complete judgments |
|---|---|---|
| A (in the pool) | $(1 + 2/4)/2 = 3/4$ | $29/36 \approx 0.8056$ |
| B (in the pool) | $(1 + 1)/2 = 1$ | 1 |
| C = 8, 3, 1, 5, 2 (not in the pool) | $(1/3 + 2/5)/2 = 11/30 \approx 0.3667$ | $34/45 \approx 0.7556$ |

P@1 and P@2 of A and B are the same under both judgments, as the claim says. Run C put d8 first, a relevant document that neither pooled run had in its top 2. On the pool its P@1 is 0 instead of 1, and its AP is less than half of its true value. Here the order of the three runs does not change, but the gap between A and C grows from 0.05 to 0.38.

At depth $k = 3$ the pool is $\{d1, d6, d8\} \cup \{d1, d2, d8\} = \{d1, d2, d6, d8\}$. It holds all three relevant documents, with 4 judgments instead of 8.

### TREC

TREC built its ad hoc collections in this way. Each participating group submitted runs, a depth was fixed, the pooled documents were judged by NIST assessors, and the judgments were then given to all groups, as Harman describes in Chapter 2 of the TREC book. The idea goes back to Sparck Jones and van Rijsbergen (1975), who proposed a pool built from several search strategies for an "ideal" test collection. That collection was never built.

## Variations

- **Move-to-front pooling.** Cormack, Palmer and Clarke (1998) judge documents in an order that favours the runs whose recent documents were relevant, so a fixed budget of judgments finds more relevant documents. The same paper describes interactive searching and judging, where an assessor searches for relevant documents directly.
- **Depth by topic.** Zobel (1998) proposed to vary the judging effort by topic and spend more of it on topics where the pool keeps finding relevant documents.
- **Choosing the next document as a bandit problem.** Later work treats each run as an arm of a [multi-armed bandit](/multi-armed-bandit/) and judges next from the run that looks most likely to give a relevant document.
- **Sampled pools.** The pool is split into strata by rank, and a random sample of each stratum is judged, as in [stratified sampling](/stratified-sampling/). [Inferred average precision](/inferred-average-precision/) then estimates the AP that complete judgments of the pool would give.
- **Judgments chosen for one comparison.** [Minimal test collections](/minimal-test-collection/) pick the documents whose judgments decide which of two systems is better.
- **Measures for incomplete pools.** [Bpref](/bpref/) uses only judged documents and ignores the others, so it does not count an unjudged document as not relevant.

## Pitfalls

- **Bias against new systems.** A run that was not in the pool can find relevant documents that nobody judged, and they count against it. Run C above shows the effect. Zobel (1998) measured it on TREC and reported that it did not appear to have a significant effect on the TREC results of his study. That is a measurement for those pools and those runs, not a guarantee for a new system that differs from all of them.
- **Recall that is too high.** The pool finds only part of the relevant documents, so $R$ is too small and recall is too high. Zobel (1998) estimated that the TREC pools found at best 50% to 70% of the relevant documents.
- **Metrics deeper than the pool.** AP over the top 1000 ranks on a pool of depth 100 treats every unjudged document below rank 100 as not relevant. The claim above holds only up to depth $k$.
- **Few or similar runs.** If all runs use the same method, their top $k$ sets overlap, the pool is small, and it misses what other methods would find.
- **Assessors who see the source.** If the assessor knows which system found a document, or its rank, the judgment can drift towards that system. Judge the pool in a shuffled or fixed order.
- **Unjudged versus not relevant.** Some tools keep a distinction between "judged not relevant" and "not judged". A metric that removes unjudged documents and one that counts them as not relevant give different values from the same judgments.

## Exercises

1. For runs A and B on q1, build the pool at depth 1 and compute the AP of run A on it.
   *Answer.* The pool is $\{d1\}$, so $R = 1$. Run A has d1 at rank 1, so its AP is 1.
2. For run C on q1, compute P@3 on the depth 2 pool and on complete judgments.
   *Answer.* The first three documents of C are d8, d3 and d1. On the pool only d1 is relevant, so P@3 is $1/3$. On complete judgments d8 and d1 are relevant, so P@3 is $2/3$.
3. Show that $|P_q| = k$ exactly when all runs have the same set of first $k$ documents, and that $|P_q| = mk$ exactly when these sets do not overlap.
   *Answer.* Each set has $k$ elements. The union of $m$ sets of size $k$ has at least $k$ elements, with equality when every set equals the union, and at most $mk$ elements, with equality when no element is in two sets.
4. Compute the bpref of run C on the depth 2 pool, and compare it with its value on complete judgments.
   *Answer.* On the pool, d8 is unjudged and bpref removes it. The judged documents of C in order are d1 and d2, both relevant with no judged nonrelevant document above them, so bpref is $2/2 = 1$. On complete judgments the relevant documents d8, d1 and d2 have 0, 1 and 2 judged nonrelevant documents above them, so bpref is $(1 + 2/3 + 1/3)/3 = 2/3$.

## References
