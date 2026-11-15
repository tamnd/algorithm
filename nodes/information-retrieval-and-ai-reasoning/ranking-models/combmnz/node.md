---
tag: HTFVCS
kind: algorithm
slug: combmnz
name: CombSUM and CombMNZ
aliases:
- CombMNZ
- CombSUM
area: information-retrieval-and-ai-reasoning/ranking-models
level: core
summary: Fuses result lists by summing normalized scores (CombSUM), and in CombMNZ multiplies the sum by the number of lists that retrieved the document.
solves: [rank-aggregation]
model: word-ram
complexity:
  vars: {N: the total number of entries in the input runs, n: the number of distinct documents in them}
  time: {worst: O(N + n log n)}
  space: {extra: O(N)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1994
  people: [Edward A. Fox, Joseph A. Shaw]
  note: Fox and Shaw defined CombSUM, CombMNZ and four related rules in their TREC-2 paper; Lee later studied them with min-max normalized scores and found CombMNZ the best.
prereqs: [rank-aggregation]
see_also: [reciprocal-rank-fusion, borda-count, markov-chain-rank-aggregation, federated-search, bm25]
sources:
  - paper: "Edward A. Fox and Joseph A. Shaw, Combination of multiple searches, The Second Text REtrieval Conference (TREC-2), NIST Special Publication 500-215 (1994), 243-252"
    locator: the six combination rules CombMAX, CombMIN, CombMED, CombSUM, CombANZ and CombMNZ, with CombMNZ defined as the sum of the similarities times the number of nonzero similarities
  - paper: doi:10.1145/278459.258587
    title: Joon Ho Lee, Analyses of multiple evidence combination, Proceedings of the 20th Annual International ACM SIGIR Conference (SIGIR 1997), 267-276
    locator: the min-max normalization of each run and the comparison of the combination rules on TREC runs, in which CombMNZ did best
  - paper: doi:10.1145/1571941.1572114
    title: Gordon V. Cormack, Charles L. A. Clarke and Stefan Büttcher, Reciprocal rank fusion outperforms Condorcet and individual rank learning methods, Proceedings of the 32nd Annual International ACM SIGIR Conference (SIGIR 2009), 758-759
    locator: Tables 2 and 3, where CombMNZ is compared with reciprocal rank fusion and Condorcet fusion on TREC and LETOR 3
---

CombSUM and CombMNZ merge the result lists of several retrieval systems by their scores. CombSUM gives each document the sum of its normalized scores over the lists that retrieved it. CombMNZ multiplies that sum by the number of lists that retrieved the document, so documents that many systems agree on get an extra reward. Edward Fox and Joseph Shaw defined both rules, with four others, for the second TREC conference, and they are the classic score-based methods of [rank aggregation](/rank-aggregation/), also called data fusion. They need comparable scores, so each list is first normalized, most often by min-max scaling.

## In plain words

Several search systems each return a list of documents with scores. The scores of different systems mean different things: one system may give scores from 0 to 1 and another from 5 to 30. So first we rescale each list, for example so that its best document gets 1 and its worst gets 0. Then each document gets the sum of its rescaled scores from all systems that returned it; that is CombSUM. CombMNZ goes one step further and multiplies the sum by the number of systems that returned the document. The idea is that a document found by many different systems is more likely to be relevant than one that only a single system likes, even if that system likes it a lot.

## The problem

The input is $m$ runs $S_1, \ldots, S_m$ for one query. Each run maps the documents that it retrieved to real scores, higher is better, and usually holds only the top few hundred or thousand documents. A document that a run did not retrieve has no score in it. The output is one ranking of the union of the runs. The scores of different runs need not be on the same scale, and the method does not know how they were made.

## The algorithm

```pseudo id=main
COMB(S1, ..., Sm, rule, ν)
L1  for each run l: Ŝl ← ν(Sl)                 ▷ min-max: (s - min) / (max - min)
L2  for each run l and each document d of Ŝl: append Ŝl(d) to the list of d
L3  for each document d: SUM(d) ← the sum of its list; h(d) ← the length of its list
L4      if rule = MNZ: score(d) ← h(d) · SUM(d) else score(d) ← SUM(d)
L5  return the documents sorted by score, highest first, ties to the smaller id
```

Line L1 is the normalization. Min-max scaling maps the best document of each run to 1 and the worst retrieved document to 0. Two other common choices are the sum normalization, which shifts the scores so that the lowest is 0 and divides by their sum, and the z-score, which subtracts the mean and divides by the standard deviation. Line L3 counts $h(d)$, the number of runs that retrieved $d$. Fox and Shaw also defined CombMAX, CombMIN and CombMED (the largest, smallest and median score) and CombANZ (the sum divided by $h(d)$, the average of the nonzero scores); the code supports all six.

## Example

Take query "sorted array search" on the toy collection. Run $A$ is [BM25](/bm25/), which retrieves five documents. Run $B$ is the second run that the collection supplies for this query. The table shows each step for each document, with scores to 4 places.

| document | 1 | 2 | 8 | 7 | 4 | 6 |
|---|---|---|---|---|---|---|
| $A$, raw | 3.0283 | 1.8893 | 1.6292 | 1.2743 | 0.6896 | none |
| $A$, min-max | 1 | 0.5130 | 0.4018 | 0.2500 | 0 | none |
| $B$, raw | 2.0 | 1.0 | 1.5 | none | 1.0 | 2.0 |
| $B$, min-max | 1 | 0 | 0.5 | none | 0 | 1 |
| $h(d)$ | 2 | 2 | 2 | 1 | 2 | 1 |
| CombSUM | 2 | 0.5130 | 0.9018 | 0.2500 | 0 | 1 |
| CombMNZ | 4 | 1.0260 | 1.8035 | 0.2500 | 0 | 1 |

CombSUM returns $1, 6, 8, 2, 7, 4$. CombMNZ returns $1, 8, 2, 6, 7, 4$: documents 8 and 2 double their sums because both runs found them, and they pass document 6, which only run $B$ found. Document 4 is in both runs but gets 0 from each, because min-max gives 0 to the lowest document of a run, and so it ends last even under CombMNZ. Without normalization, CombSUM gives $1, 8, 2, 6, 4, 7$, because run $A$ has the larger raw scores and decides more of the order. With z-scores, document 4 has a negative sum, and CombMNZ doubles it to the lowest score of all.

## Correctness

Lines L1 to L5 compute $\mathrm{SUM}(d) = \sum_{l : d \in S_l} \hat S_l(d)$ and $\mathrm{MNZ}(d) = h(d) \cdot \mathrm{SUM}(d)$; the invariant of line L2 is that after each run, the list of each document holds one normalized score for each run seen so far that retrieved it. The file proofs/correctness.md proves this and three further facts. With min-max, sum or z-score normalization, replacing a run's scores by $a s + b$ with $a > 0$ does not change the result, so the method does not depend on the scale of any system. With one run, both rules return that run's order. With nonnegative normalized scores, a further run that retrieves $d$ never lowers $d$'s score; with z-scores this fails, which is the reason for the pitfall below.

That the rules give good rankings is a measured claim, not a proved one. Fox and Shaw found CombSUM the best of their six rules on their TREC-2 runs. Lee found CombMNZ the best on his runs with min-max scores, and argued that systems tend to retrieve the same relevant documents but different nonrelevant ones, which is what the factor $h(d)$ rewards. Cormack, Clarke and Büttcher found [reciprocal rank fusion](/reciprocal-rank-fusion/) better than CombMNZ on three of four TREC tasks, and CombMNZ slightly better on LETOR 3.

## Complexity

Line L1 reads each run twice, once for the minimum and maximum and once to rescale. Lines L2 to L4 touch each entry once with a hash map. So with $N = \sum_l |S_l|$ entries and $n$ distinct documents, the time is $O(N + n \log n)$, where the last term is the sort of line L5, and the extra space is $O(N)$ for the lists of scores. SUM and MNZ need only a running sum and a count per document, which brings the extra space to $O(n)$; only CombMED needs all the values.

## Properties

- **Uses the scores.** Unlike rank-only methods, CombSUM keeps the size of the gaps between documents. A document far ahead in one run keeps that lead.
- **Scale free after normalization.** With min-max, sum or z-score normalization, a positive affine change of one run's scores changes nothing.
- **Rewards overlap.** CombMNZ multiplies by $h(d)$, so with $m$ runs a document in all of them can gain up to a factor $m$ over a document in one.
- **Separable.** Each run adds its part independently, so runs can be added one at a time, and per-run weights are a one-line change.
- **One run is kept.** With a single run both rules return its order.

## Variants and improvements

- **Weighted CombSUM.** Multiply each run's normalized scores by a weight learned on training queries. This is a linear combination of systems, the most common form of score fusion in practice.
- **Other normalizations.** Montague and Aslam compared min-max, sum and z-score normalizations for metasearch. Scores can also be mapped to estimated probabilities of relevance, using training queries, which makes the sum more meaningful.
- **Rank-based fusion.** When the scores are not available or not trusted, [reciprocal rank fusion](/reciprocal-rank-fusion/) or the [Borda count](/borda-count/) use the ranks only. A Borda score is CombSUM on scores that are linear in the rank.
- **Pairwise fusion.** Condorcet fusion and [Markov chain rank aggregation](/markov-chain-rank-aggregation/) use pairwise majorities in place of sums.
- **Federated search.** When the runs come from different collections, not from different systems on the same collection, the overlap that CombMNZ rewards is rare, and [federated search](/federated-search/) needs other merging methods.

## When to use it

Use CombSUM or CombMNZ when the runs search the same collection, their scores carry information beyond the order, and the runs overlap enough that $h(d)$ varies. CombMNZ suits a set of runs of similar quality whose relevant documents overlap. Weighted CombSUM suits a case with training queries, where weights can favour the better systems. If the scores are on very different scales, or one run's scores have a long tail that normalization handles badly, a rank-based method such as reciprocal rank fusion is safer.

## Pitfalls

- **Min-max gives 0 to the bottom.** Line L1 with min-max sets the lowest retrieved document of each run to 0, so it adds nothing, and under CombMNZ $h(d)$ counts it but multiplies 0. Document 4 in the example is in both runs and still ends last. If being retrieved should count, normalize with the minimum over the whole collection, or add a small constant to every retrieved score.
- **Negative scores and the multiplier.** With z-scores, line L4 multiplies a negative sum by $h(d)$ and so punishes a document for being found by more runs. Use a normalization with nonnegative values for CombMNZ, or shift the z-scores so that the lowest is 0.
- **No normalization.** If line L1 is skipped, the run with the largest scores decides the order, as the unnormalized example shows. Always state the normalization; results in papers with different choices are not comparable.
- **Outliers in min-max.** One very high score in a run compresses all other scores of that run toward 0. A robust choice, such as dividing by a high percentile, or the z-score with a shift, can help.
- **Counting nonzero scores.** Fox and Shaw count the nonzero similarities, while the code counts the retrieved documents. The two differ when a retrieved document has the score 0 after normalization, as the bottom document under min-max does. Say which count you use.

## Implementations

## History

Fox and Shaw described the six combination rules in their paper for TREC-2, which NIST published in 1994; the conference took place in 1993. They combined the runs of several retrieval methods on the same collection and found CombSUM the most effective. Lee, in 1997, normalized each run by min-max scaling, compared the rules again on TREC runs, and found CombMNZ the best; his analysis of overlap, that different systems retrieve similar relevant documents but different nonrelevant ones, became the usual explanation for why CombMNZ works. CombMNZ became the standard baseline for data fusion and was the main score-based method that later rank-based methods, such as reciprocal rank fusion in 2009, were measured against.

## References
