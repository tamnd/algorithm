---
tag: 1G955M
kind: definition
slug: alpha-ndcg
name: "Alpha-nDCG"
aliases:
- alpha-normalized discounted cumulative gain
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: research
summary: An nDCG variant over the subtopics of a query that discounts the gain of a subtopic each time it has already been covered.
prereqs: [normalized-discounted-cumulative-gain, greedy-algorithm, np-hard]
see_also: [search-result-diversification, vertex-cover, max-coverage, submodular-function, nemhauser-wolsey-fisher-theorem, expected-reciprocal-rank, cwl-framework]
sources:
  - paper: "Charles L. A. Clarke, Maheedhar Kolla, Gordon V. Cormack, Olga Vechtomova, Azin Ashkan, Stefan Büttcher and Ian MacKinnon, Novelty and diversity in information retrieval evaluation, SIGIR 2008"
    locator: the model of documents and needs as sets of nuggets and the gain with parameter alpha; Section 5.1 (the ideal ordering, the proof that computing it is NP-complete by a reduction from vertex cover, and the greedy approximation with ties broken arbitrarily); Section 5.2 (alpha-nDCG, and the case alpha = 0); Section 6 (the TREC 2006 question answering data)
  - paper: "George L. Nemhauser, Laurence A. Wolsey and Marshall L. Fisher, An analysis of approximations for maximizing submodular set functions I, Mathematical Programming 14, 1978, pp. 265-294"
    locator: the greedy bound 1 - 1/e for monotone submodular maximization under a cardinality constraint
---

Alpha-nDCG is a version of [nDCG](/normalized-discounted-cumulative-gain/) for queries with several subtopics, or nuggets, such as the meanings of an ambiguous query. A document gains for each nugget it contains, but a nugget that documents higher in the ranking already contain is worth less each time it repeats: its gain is multiplied by $1 - \alpha$ for each earlier document that has it. So a ranking that covers many nuggets near the top scores higher than one that repeats the same nugget. Clarke, Kolla, Cormack, Vechtomova, Ashkan, Büttcher and MacKinnon defined it in 2008. Its normalizer, the DCG of the ideal ranking, is NP-hard to compute, so in practice it is computed by a greedy algorithm, and the result is then only an approximation of the ideal.

## Definition

**Input.** A ranking $d_1, d_2, \ldots$ of distinct documents for a query, a set of nuggets $1, \ldots, m$ of the query, judgments $J(d, t) \in \{0, 1\}$ that say whether document $d$ contains nugget $t$, a parameter $0 \le \alpha \le 1$ and a cutoff $k$. A document that is not judged contains no nugget.

**Gain.** Let $r_{t, j - 1} = \sum_{i < j} J(d_i, t)$ be the number of documents above rank $j$ that contain nugget $t$. The gain at rank $j$ is

$$G[j] = \sum_{t=1}^{m} J(d_j, t) \, (1 - \alpha)^{r_{t, j - 1}} .$$

The first document with nugget $t$ gets 1 for it, the second gets $1 - \alpha$, the third $(1 - \alpha)^2$, and so on. One reading: each earlier document with the nugget satisfies the need for it with probability $\alpha$, and the gain is the probability that the need is still open.

**Discounted gain.** $\mathrm{DCG}[k] = \sum_{j=1}^{k} G[j] / \log_2(1 + j)$, with the discount of nDCG.

**Ideal ranking.** Clarke et al. define the ideal ranking as one that maximizes the cumulative gain $\mathrm{CG}[j] = \sum_{i \le j} G[i]$ at every depth $j$, and $\mathrm{DCG}'[k]$ as its discounted gain. Computing it is NP-hard (see below), so they compute it greedily: at each rank, put the document with the largest gain $G$ given the documents already placed, and break ties arbitrarily.

**The measure.**

$$\alpha\text{-nDCG}[k] = \frac{\mathrm{DCG}[k]}{\mathrm{DCG}'[k]} .$$

It is undefined when no judged document contains a nugget, as nDCG is. With $\alpha = 0$ no repeat is discounted, every document gets one unit for each nugget it has, and alpha-nDCG is standard nDCG with the number of nuggets of a document as its grade. With $\alpha = 1$ only the first copy of each nugget counts, and $\mathrm{CG}[k]$ is the number of nuggets covered by the top $k$.

### The ideal ranking is NP-hard

**Claim 1.** For $\alpha = 1$, deciding whether some ranking reaches $\mathrm{CG}[k] = m$, that is, whether $k$ documents cover all nuggets, is NP-complete.

*Proof.* Clarke et al. reduce from [vertex cover](/vertex-cover/). Given a graph and a number $k$, make one document for each vertex and one nugget for each edge, and let a document contain the nuggets of the edges at its vertex. With $\alpha = 1$, $\mathrm{CG}[k]$ of a ranking is the number of edges touched by its top $k$ vertices, so it equals $m$ exactly when those vertices form a vertex cover of size $k$. Membership in NP is clear: a ranking is a certificate that can be checked in polynomial time. $\square$

So an algorithm that computes the ideal ranking of the definition in polynomial time would decide vertex cover, and the problem is [NP-hard](/np-hard/). An ordering that maximizes CG at every depth at once need not even exist: the counterexample below has a different best set at depth 1 and at depth 2.

### The greedy normalizer

**Claim 2.** Let $\mathrm{DCG}'[k]$ come from the greedy ranking, with any tie rule. Then for every ranking, $\mathrm{DCG}[k] \le \frac{e}{e - 1} \mathrm{DCG}'[k]$. So the reported alpha-nDCG is at most $e/(e - 1) \approx 1.582$, and it can be larger than 1.

*Proof.* $\mathrm{CG}[j]$ depends only on the set $S$ of the top $j$ documents: $f(S) = \sum_t \sum_{c=0}^{n_t(S) - 1} (1 - \alpha)^c$, where $n_t(S)$ is the number of documents of $S$ with nugget $t$. Adding $d$ to $S$ adds $\sum_{t \in d} (1 - \alpha)^{n_t(S)}$, which is the gain $G$ of $d$ at the next rank. This added value never grows as $S$ grows, so $f$ is monotone and [submodular](/submodular-function/). The greedy ranking adds at each rank the document of largest gain, so its top $j$ is the greedy solution for $j$ documents, and the [Nemhauser-Wolsey-Fisher theorem](/nemhauser-wolsey-fisher-theorem/) gives $\mathrm{CG}'[j] \ge (1 - 1/e) \, \mathrm{CG}^*[j]$, where $\mathrm{CG}^*[j]$ is the largest value of any ranking at depth $j$. Now write $w_j = 1/\log_2(1 + j)$ and $w_{k+1} = 0$. Summation by parts gives $\mathrm{DCG}[k] = \sum_{j=1}^{k} \mathrm{CG}[j] (w_j - w_{j+1})$, with coefficients at least 0 because $w$ decreases. So for every ranking, $\mathrm{DCG}[k] \le \sum_j \mathrm{CG}^*[j] (w_j - w_{j+1}) \le \frac{e}{e - 1} \sum_j \mathrm{CG}'[j] (w_j - w_{j+1}) = \frac{e}{e - 1} \mathrm{DCG}'[k]$. $\square$

Clarke et al. write that if no ties occur, the greedy approach computes the ideal gain vector, and that a run which beats the approximation when ties occur would be credited with an ideal result. The first part does not hold, as the second counterexample below shows. The greedy value is a good normalizer in practice, but a value above 1 is possible with or without ties.

## Examples and non-examples

### A worked example with $\alpha = 1/2$

This is the example of Clarke et al. Ten documents a to j are ranked in that order, and six nuggets 85.1 to 85.6 are judged:

| Rank $j$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Document | a | b | c | d | e | f | g | h |
| Nuggets | 85.2, 85.4 | 85.2 | 85.2 | none | 85.1, 85.6 | 85.1 | 85.3 | 85.1 |
| $G[j]$ | 2 | 0.5 | 0.25 | 0 | 2 | 0.5 | 1 | 0.25 |
| $\mathrm{DCG}[j]$ | 2 | 2.315 | 2.440 | 2.440 | 3.214 | 3.392 | 3.726 | 3.804 |
| $\mathrm{DCG}'[j]$ | 2 | 3.262 | 3.762 | 3.977 | 4.171 | 4.260 | 4.343 | 4.343 |
| $\alpha$-nDCG$[j]$ | 1 | 0.710 | 0.649 | 0.614 | 0.771 | 0.796 | 0.858 | 0.876 |

Documents i and j contain no nugget. Document b repeats 85.2 once, so it gets $1/2$, and c repeats it twice, so it gets $1/4$. The greedy ideal ranking is a, e, g, b, f, c, h, with gains 2, 2, 1, 0.5, 0.5, 0.25, 0.25. Here a and e tie at rank 1 and the tie is broken by name. For this example a search over all orders of the seven documents with nuggets shows that the greedy values are the best at every depth.

With $\alpha = 0$ the gains of the run are 2, 1, 1, 0, 2, 1, 1, 1, and $\alpha$-nDCG[8] is 0.932: the three copies of 85.2 in a row cost nothing. With $\alpha = 1$ the gains are 2, 0, 0, 0, 2, 0, 1, 0 and $\alpha$-nDCG[8] is 0.826.

### Ties broken badly

Let $\alpha = 1/2$, and let d1 contain t1 and t2, d2 contain t1 and t3, and d3 contain t2 and t4. All three tie with gain 2 at rank 1. If the tie rule picks d1, then d2 and d3 tie with gain 1.5 at rank 2, and the greedy $\mathrm{DCG}'[2] = 2 + 1.5 \cdot 0.6309 = 2.946$. The ranking d2, d3 covers four new nuggets and has $\mathrm{DCG}[2] = 2 + 2 \cdot 0.6309 = 3.262$, so its alpha-nDCG[2] is 1.107.

### No ties, and still not ideal

Let $\alpha = 1$, with nuggets 0 to 7, d1 containing 0, 2, 3, 5 and 7, d2 containing 0, 4, 6 and 7, and d3 containing 1, 2, 3 and 5. At rank 1 the gains are 5, 4 and 4, so greedy picks d1 with no tie. At rank 2 the new nuggets of d2 are 4 and 6 and those of d3 are 1, so greedy picks d2, again with no tie, and $\mathrm{DCG}'[2] = 5 + 2 \cdot 0.6309 = 6.262$. The ranking d2, d3 covers all eight nuggets: $\mathrm{DCG}[2] = 4 + 4 \cdot 0.6309 = 6.524$, and its alpha-nDCG[2] is 1.042. No ranking maximizes CG at both depths: depth 1 needs d1 first, and depth 2 needs d2 and d3.

### Non-examples

- nDCG with the number of nuggets as the grade. That is the case $\alpha = 0$, and it gives no credit for diversity.
- An intent-aware measure such as NDCG-IA of Agrawal et al., which computes nDCG for each subtopic and averages the values with the probability of each subtopic. It weights the subtopics but has no discount for repeats inside one subtopic list. See [search result diversification](/search-result-diversification/).
- Alpha-nDCG with the ideal taken from the run's own documents. As for nDCG, the ideal must come from all judged documents.

## Related definitions

- [nDCG](/normalized-discounted-cumulative-gain/) is the case $\alpha = 0$.
- The greedy ideal is the greedy algorithm for [maximum coverage](/max-coverage/) when $\alpha = 1$, and the hardness is the hardness of [vertex cover](/vertex-cover/) and [set cover](/set-cover/).
- [Expected reciprocal rank](/expected-reciprocal-rank/) also lets the documents above lower the worth of a document, through the probability that the user has already stopped. Averaged over subtopics it gives an intent-aware measure of diversity.
- [Search result diversification](/search-result-diversification/) is the ranking problem that alpha-nDCG evaluates.

Claims 1 and 2 are proved. That alpha-nDCG matches what users of ambiguous queries want is a question of measurement; Clarke et al. apply it to the question series of the TREC 2006 question answering track. The value of $\alpha$ must be reported with the results.

## References
