---
tag: 6YEMD5
kind: algorithm
slug: lambdarank
name: LambdaRank
aliases:
- lambda gradients for ranking
area: information-retrieval-and-ai-reasoning/ranking-models
level: advanced
summary: Scales each pairwise RankNet gradient by the change in nDCG that swapping the pair would cause, to optimize the metric directly.
solves: [learning-to-rank]
model: word-ram
complexity:
  vars: {N: the number of documents, P: the number of preferred pairs, d: the number of features, T: the number of steps}
  time: {per_step: O(N log N + P + N d), total: O(T (N log N + P + N d))}
  space: {extra: O(N + d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2006
  people: [Chris Burges, Robert Ragno, Quoc Viet Le]
  note: Burges, Ragno and Le proposed in 2006 (NIPS 19, printed 2007) to define the gradients of a ranking cost directly, since NDCG itself has no useful gradient. The lambdas of RankNet scaled by the NDCG change of a swap became the standard choice.
prereqs: [ranknet, normalized-discounted-cumulative-gain]
see_also: [lambdamart, learning-to-rank, ranking-svm, listnet, expected-reciprocal-rank, mean-reciprocal-rank, gradient-descent, top-k-selection]
sources:
  - paper: "Christopher J. C. Burges, Robert Ragno and Quoc Viet Le, Learning to rank with nonsmooth cost functions, Advances in Neural Information Processing Systems 19 (NIPS 2006), MIT Press, 2007"
    locator: pp. 193-200 (defining the gradients of a nonsmooth ranking cost directly, with NDCG as the main case)
  - paper: "Christopher J. C. Burges, From RankNet to LambdaRank to LambdaMART: an overview, Microsoft Research Technical Report MSR-TR-2010-82, 2010"
    locator: Section 4.1 and Equation (6) (the lambdas scaled by the NDCG change of a swap, called empirically optimizing NDCG) and Section 4.3 (when the lambdas are a gradient)
  - paper: doi:10.1145/3269206.3271784
    title: Xuanhui Wang, Cheng Li, Nadav Golbandi, Michael Bendersky and Marc Najork, The LambdaLoss framework for ranking metric optimization, Proceedings of the 27th ACM CIKM, 2018
    locator: pp. 1313-1322 (a loss framework in which LambdaRank is a special case)
---

LambdaRank trains a scoring function for [learning to rank](/learning-to-rank/) by gradient steps whose direction is defined directly, not derived from a cost. It starts from the per-pair gradients of [RankNet](/ranknet/) and multiplies each one by $|\Delta Z_{ij}|$, the absolute change of [NDCG](/normalized-discounted-cumulative-gain/) if documents $i$ and $j$ swapped their ranks. Pairs near the top of the list, where NDCG is sensitive, get large pushes, and pairs deep in the list get small ones or none. The learning-to-rank page shows one such step on three documents; this page gives the algorithm with a cutoff $k$, the closed form of $|\Delta Z_{ij}|$, the exact sense in which the lambdas are a gradient, and why they are not the gradient of NDCG. Fitting trees to the same lambdas gives [LambdaMART](/lambdamart/).

## In plain words

RankNet treats every wrongly ordered pair of results the same. But users look mostly at the top of a result list, so a mistake at the top costs much more than a mistake near the bottom. LambdaRank keeps the pushes of RankNet and makes each one bigger or smaller. For each pair, it asks how much the quality score of the whole list would change if the two results traded places. A pair whose swap would change the list quality a lot gets a strong push. A pair whose swap changes little gets a weak push. The method never needs the quality score to be smooth, because it only uses these pushes.

## The problem

The input is a set of queries; query $q$ has documents with features $x_1, \ldots, x_n$ and graded labels $y_i \in \{0, 1, \ldots\}$. The scorer is $s_i = f(x_i)$; the code uses $f(x) = w \cdot x$. The ranking sorts by score, highest first, ties to the smaller index, and $r_i$ is the rank of document $i$. NDCG@$k$ uses the gain $G_i = 2^{y_i} - 1$ and the discount $D(r) = 1/\log_2(r + 1)$ for $r \le k$ and 0 beyond. The goal is a high mean NDCG@$k$ over the queries. NDCG depends on the scores only through the ranking, so it is piecewise constant in $s$ and its gradient is zero wherever it exists. Gradient methods cannot use it directly.

For a pair with $y_i > y_j$, the swap change has the closed form

$$|\Delta Z_{ij}| = \frac{|(G_i - G_j)(D(r_i) - D(r_j))|}{\mathrm{IDCG@}k}.$$

## The algorithm

With $\rho_{ij} = 1/(1 + e^{\sigma(s_i - s_j)})$, the RankNet gradient of a pair in $s_i$ is $-\sigma \rho_{ij}$. LambdaRank uses

$$\lambda_{ij} = -\sigma \rho_{ij} |\Delta Z_{ij}|, \qquad \lambda_i = \sum_{j : y_i > y_j} \lambda_{ij} - \sum_{j : y_j > y_i} \lambda_{ji},$$

and moves $w$ against $\sum_i \lambda_i x_i$.

```pseudo id=main
LAMBDARANK(queries, σ, k, η, T)
L1  w ← 0
L2  repeat T times:
L3      for each query: s_i ← w · x_i, sort to get the ranks r_i and IDCG@k
L4          for each pair with y_i > y_j: λ_ij ← -σ |ΔZ_ij| / (1 + e^{σ (s_i - s_j)})
L5          λ_i ← Σ_j λ_ij - Σ_j λ_ji
L6      w ← w - η Σ_queries Σ_i λ_i x_i
L7  return w
```

Line L3 is the only place where the ranking enters. Line L4 is the RankNet gradient times the swap change. Lines L5 and L6 are the factorization of RankNet: one sum per document, then one gradient per document.

## Example

One query has four documents with scores $s = (0.5, 1.5, 1.0, 2.0)$ and labels $y = (2, 1, 0, 0)$, with $\sigma = 1$ and no cutoff. The ranking is $3, 1, 2, 0$ (document 3 first), so the best document is last. NDCG is $0.5296$, with IDCG $= 3.6309$.

| pair $(i, j)$ | $s_i - s_j$ | RankNet $-\sigma \rho_{ij}$ | $\lvert \Delta Z_{ij} \rvert$ | $\lambda_{ij}$ |
|---|---|---|---|---|
| (0, 1) | -1.0 | -0.7311 | 0.1103 | -0.0806 |
| (0, 2) | -0.5 | -0.6225 | 0.0573 | -0.0357 |
| (0, 3) | -1.5 | -0.8176 | 0.4704 | -0.3846 |
| (1, 2) | 0.5 | -0.3775 | 0.0361 | -0.0136 |
| (1, 3) | -0.5 | -0.6225 | 0.1016 | -0.0633 |

The pair (0, 3) holds the best document at rank 4 and a document of label 0 at rank 1, so its swap change is by far the largest. The lambdas are $\lambda = (-0.5009, 0.0038, 0.0493, 0.4479)$. Plain RankNet gives $(-2.1711, -0.2689, 1.0, 1.44)$ on the same scores; it pushes document 1 up, while LambdaRank pushes it slightly down, because its pairs matter little for NDCG compared with the push that document 0 needs. With the cutoff $k = 2$ the lambdas are $(-0.9296, 0.1252, 0.0656, 0.7388)$: they are larger, because IDCG@2 is smaller, and they act mainly on the two documents that are or should be in the top 2.

## Correctness

LambdaRank has no cost that it provably decreases, and the proof in proofs/correctness.md states what does hold.

- **The swap change.** The closed form above equals the change of NDCG@$k$ computed by swapping the two documents and recomputing. Pairs with both ranks beyond $k$ get $\lambda_{ij} = 0$.
- **A gradient on each region.** On each open region of score vectors with one fixed ranking, the weights $|\Delta Z_{ij}|$ are constant, and the lambdas are the exact gradient of the weighted RankNet cost $C_Z(s) = \sum |\Delta Z_{ij}| \log(1 + e^{-\sigma(s_i - s_j)})$, a convex function of $s$. This is the observation of Burges (2010), Section 4.3. Across region boundaries the weights jump.
- **Not the gradient of NDCG.** NDCG is constant on each region, so the lambdas are not its gradient. That steps along the lambdas raise NDCG is an experimental finding, which Burges (2010), Section 4.1, calls empirical.

The tests check each $\lambda_{ij}$ against a finite-difference RankNet gradient times the NDCG change of the swap computed by sorting, on 200 random queries. The rise of NDCG during training on a planted set is measured, not proved.

## Complexity

One step sorts each query, $O(n_q \log n_q)$, and computes IDCG. Each pair then costs $O(1)$ by the closed form, so the lambdas cost $O(P)$ for $P$ pairs, and line L6 costs $O(N d)$ for $N$ documents. The total per step is $O(N \log N + P + N d)$. Recomputing NDCG for each swap would cost $O(n_q)$ per pair, $O(P n)$ in total, which the closed form avoids. With a cutoff $k$, only pairs with at least one rank at most $k$ have nonzero lambdas, which leaves $O(k n_q)$ pairs per query. The extra space is $O(N + d)$.

## Properties

- **Zero sum.** The lambdas of a query sum to zero, as in RankNet.
- **Local to the top.** With a cutoff $k$, documents whose pairs all lie below rank $k$ get no push.
- **Scale.** Each $|\Delta Z_{ij}| \le 1$, so every $|\lambda_{ij}| < \sigma$.
- **Any metric with a swap change.** The same recipe works with the swap change of [ERR](/expected-reciprocal-rank/), [MRR](/mean-reciprocal-rank/) or MAP in place of NDCG.
- **No cost function in general.** The lambdas are a gradient only inside each region of fixed ranking. Line searches and convergence tests that need a cost value use $C_Z$ of the current region, which changes when the ranking changes.

## Variants and improvements

- **LambdaMART** fits gradient-boosted regression trees to the lambdas, with a Newton step in each leaf, and is the most used form.
- **LambdaLoss.** Wang et al. (2018) give a family of well-defined losses that contains LambdaRank as one case, and propose new losses inside the family.
- **Other metrics.** Replace $|\Delta Z_{ij}|$ by the swap change of the metric that matters, for example ERR when a user is likely to stop at the first very good result.
- **Neural scorers.** The original setting: line L6 becomes back-propagation of $\lambda_i$ through the network.

## When to use it

Use LambdaRank when the target metric weights the top of the list, such as NDCG@10, and the scorer is trained by gradients, for example a neural network. With hand-made features and tree models, use LambdaMART. If the metric weights all pairs equally, as AUC does, RankNet or the Ranking SVM is simpler and the weights add nothing. The advantage of LambdaRank over RankNet on NDCG is a measured result.

## Pitfalls

- **The ranks come from the current scores.** Line L3 must sort by the current $s$, not by the labels or by stale scores. With the ideal ranks, every pair of the closed form is computed at the wrong positions.
- **Ties in the scores.** At the start, all scores are 0. Line L3 needs a fixed tie rule, such as the smaller index first, or the ranks and the lambdas change from run to run.
- **Queries with no relevant document.** IDCG@$k$ is 0 when every label in the top $k$ of the ideal order is 0. Line L4 must skip such queries rather than divide by zero.
- **Treating the lambdas as a cost.** Monitoring $\sum \lambda_i^2$ or a RankNet cost does not track NDCG. Monitor NDCG@$k$ on validation queries.
- **The sign.** Line L4 gives the gradient of a cost to minimize, so line L6 subtracts it. Adding it moves every pair the wrong way. Texts that write the lambdas as the direction to move up use the opposite sign, so check the convention before mixing code.

## Implementations

## History

Burges, Ragno and Le (2006) observed that one does not need a smooth cost to train a ranker by gradient descent: it is enough to specify the gradient of each document's score, and they chose the RankNet gradient times the NDCG change of a swap. Burges (2010) reviewed the method together with RankNet and LambdaMART, stated when the lambdas are the gradient of a cost, and called the optimization of NDCG empirical. Wang et al. (2018) later embedded LambdaRank in a framework of well-defined losses.

## References
