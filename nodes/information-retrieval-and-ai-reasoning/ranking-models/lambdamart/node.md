---
tag: HY1P4E
kind: algorithm
slug: lambdamart
name: LambdaMART
aliases:
- lambda-gradient boosted trees
area: information-retrieval-and-ai-reasoning/ranking-models
level: advanced
summary: Fits gradient-boosted regression trees to LambdaRank gradients, a strong standard ranker on feature-based benchmarks.
solves: [learning-to-rank]
model: word-ram
complexity:
  vars: {N: the number of documents, P: the number of preferred pairs, d: the number of features, D: the tree depth, M: the number of rounds}
  time: {per_round: O(N log N + P + D d N log N), total: O(M (N log N + P + D d N log N))}
  space: {extra: O(N + M 2^D)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2010
  people: [Qiang Wu, Chris Burges, Krysta Svore, Jianfeng Gao]
  note: Wu, Burges, Svore and Gao combined the lambdas of LambdaRank with the boosted regression trees of MART. Burges (2010) states that an ensemble of LambdaMART rankers won Track 1 of the 2010 Yahoo! Learning to Rank Challenge.
prereqs: [lambdarank, gradient-boosting]
see_also: [ranknet, learning-to-rank, decision-tree-learning, cart, normalized-discounted-cumulative-gain, rankboost, listnet, unbiased-learning-to-rank]
sources:
  - paper: doi:10.1007/s10791-009-9112-1
    title: Qiang Wu, Christopher J. C. Burges, Krysta M. Svore and Jianfeng Gao, Adapting boosting for information retrieval measures, Information Retrieval 13(3), 2010
    locator: pp. 254-270 (LambdaMART as boosted trees fitted to the lambdas, and its comparison with LambdaRank)
  - paper: "Christopher J. C. Burges, From RankNet to LambdaRank to LambdaMART: an overview, Microsoft Research Technical Report MSR-TR-2010-82, 2010"
    locator: Sections 5 and 6 (MART and its Newton step in each leaf) and Section 7 (the LambdaMART algorithm, with targets y_i = lambda_i, weights w_i = dy_i/dF and leaf values sum y over sum w)
---

LambdaMART is a [gradient boosting](/gradient-boosting/) machine for [learning to rank](/learning-to-rank/): each round fits a small regression tree to the [LambdaRank](/lambdarank/) lambdas of the current scores and sets each leaf by one Newton step. The gradient-boosting page explains boosting for a fixed differentiable loss; here there is no fixed loss, because the lambdas change with the ranking, and the Newton weights come from the second derivatives of a frozen pairwise cost. The learning-to-rank page lists LambdaMART among the methods and mentions the 2010 Yahoo! challenge; this page gives the targets, the weights, the leaf formula of Burges (2010) and what it is a Newton step of, and a worked round.

## In plain words

We build the scoring rule as a sum of many small decision trees, one tree at a time. Before each new tree, we score every result with the trees so far and sort each list. For every result, we work out how strongly it should move up or down to improve the list, using the same pushes as LambdaRank. The new tree groups results with similar features and similar pushes. Each group gets one number, which says how far to move every result in the group. That number takes into account both the push and how sure we are about it. We add a small part of the new tree to the scores and repeat.

## The problem

The input is a set of queries, each with documents $x_1, \ldots, x_n \in \mathbb R^d$ and graded labels $y_i$. The model is $F(x) = \eta \sum_{m=1}^{M} f_m(x)$, a sum of regression trees $f_m$ of depth at most $D$, with shrinkage $\eta \in (0, 1]$. The goal is a high mean [NDCG](/normalized-discounted-cumulative-gain/)@$k$. At the current scores $s = F(x)$ of a query, let $|\Delta Z_{ij}|$ be the NDCG@$k$ change of swapping $i$ and $j$ and $\rho_{ij} = 1/(1 + e^{\sigma(s_i - s_j)})$. Freeze the weights $|\Delta Z_{ij}|$ and define the cost

$$C(s) = \sum_{(i,j) : y_i > y_j} |\Delta Z_{ij}| \log\left(1 + e^{-\sigma (s_i - s_j)}\right).$$

The round targets and weights are the negative first and the second derivatives of $C$:

$$g_i = -\frac{\partial C}{\partial s_i} = -\lambda_i, \qquad h_i = \frac{\partial^2 C}{\partial s_i^2} = \sum_{\text{pairs } p \ni i} \sigma^2 |\Delta Z_p|\, \rho_p (1 - \rho_p).$$

## The algorithm

```pseudo id=main
LAMBDAMART(queries, M, D, η, σ, k)
L1  F(x_i) ← 0 for every document
L2  for m ← 1 to M:
L3      for each query: sort by F, get |ΔZ_ij| and ρ_ij for each pair with y_i > y_j
L4          g_i ← Σ σ |ΔZ| ρ over pairs where i is better, minus over pairs where i is worse;  h_i ← Σ σ² |ΔZ| ρ (1 - ρ)
L5      fit a regression tree of depth D to the targets g by least squares, over all documents
L6      for each leaf R: γ_R ← Σ_{i ∈ R} g_i / Σ_{i ∈ R} h_i   (0 if the sum of h is 0)
L7      F(x) ← F(x) + η γ_{leaf(x)}
L8  return the trees and their leaf values
```

Line L4 is the LambdaRank computation with the sign of a cost. Line L5 chooses the shape of the tree by least squares on $g$, as in MART. Line L6 then replaces the least-squares means of the leaves by Newton steps, which is the difference between MART for ranking and plain gradient boosting on the lambdas. In the notation of Burges (2010), Section 7, $y_i = \lambda_i$, $w_i = \partial y_i / \partial F$ and $\gamma = \sum y_i / \sum w_i$, with the sign of a utility.

## Example

One query has four documents with the current scores $s = (0.5, 1.5, 1.0, 2.0)$, labels $(2, 1, 0, 0)$, $\sigma = 1$, no cutoff, and one binary feature that is 1 for documents 0 and 1 and 0 for documents 2 and 3. The ranking is $3, 1, 2, 0$ and NDCG is $0.5296$. The pairs and their $\rho$ and $|\Delta Z|$ are those of the LambdaRank example.

| document | label | $s$ | $g_i$ | $h_i$ | leaf | $\gamma$ | new $s$ |
|---|---|---|---|---|---|---|---|
| 0 | 2 | 0.5 | 0.5009 | 0.1053 | $\{0, 1\}$ | 3.1196 | 0.8120 |
| 1 | 1 | 1.5 | -0.0038 | 0.0540 | $\{0, 1\}$ | 3.1196 | 1.8120 |
| 2 | 0 | 1.0 | -0.0493 | 0.0219 | $\{2, 3\}$ | -4.2863 | 0.5714 |
| 3 | 0 | 2.0 | -0.4479 | 0.0940 | $\{2, 3\}$ | -4.2863 | 1.5714 |

The only split is on the feature, so the depth-1 tree has the leaves $\{0, 1\}$ and $\{2, 3\}$. Leaf $\{0, 1\}$ has $\sum g = 0.4971$ and $\sum h = 0.1594$, so $\gamma = 3.1196$; leaf $\{2, 3\}$ has $\sum g = -0.4971$ and $\sum h = 0.1160$, so $\gamma = -4.2863$. With $\eta = 0.1$ the new scores rank the documents $1, 3, 0, 2$, and NDCG rises to $0.6885$. The pair (0, 1) lies inside one leaf, so moving the leaf does not change its score difference; the exact one-dimensional Newton step for that leaf would be $4.2863$, not $3.1196$ (see the proof file).

## Correctness

The proof in proofs/correctness.md shows:

- **Targets and weights.** $g_i = -\partial C / \partial s_i$ and $h_i = \partial^2 C / \partial s_i^2$ for the frozen cost $C$. The tests check both by central finite differences on 100 random queries.
- **Leaf values.** $\gamma_R$ of line L6 minimizes the second-order model of $C$ along the move of all documents of the leaf, with the mixed second derivatives dropped. It is a diagonal Newton step, not the exact Newton step: pairs inside one leaf are counted in $\sum h$ but do not change. The tests check each leaf of a fitted depth-2 tree against the ratio of finite-difference derivatives.
- **The split.** Line L5 finds the least-squares split over all features and thresholds; the tests compare it with a brute force.
- **Scale.** At $s = 0$, multiplying $\sigma$ by $c$ divides every leaf value by $c$, the $1/\sigma$ scaling that Burges (2010) mentions.

No round provably lowers $C$ or raises NDCG, since the tree shape comes from least squares, the step is diagonal and shrunk, and the weights change with the ranking. On the planted set of the tests, where the label depends on whether both $x_0 > 0$ and $x_1 > 0$, 30 rounds of depth-2 trees raise the mean NDCG from 0.6916 to 1.0. That is a measurement on one data set.

## Complexity

Each round sorts each query and computes the lambdas in $O(N \log N + P)$ for $N$ documents and $P$ pairs. A depth-$D$ tree on $N$ points and $d$ features costs $O(D\, d\, N \log N)$ with sorting at each level, or $O(D\, d\, N)$ with presorted features or histograms of binned feature values, as production libraries use. Line L7 costs $O(N D)$. The model has $M$ trees of at most $2^D$ leaves, and predicting one document costs $O(M D)$. The code is a simple reference and tries every midpoint with a fresh sum, which is quadratic in the node size.

## Properties

- **Invariant to monotone feature transforms.** Trees split on thresholds, so rescaling or taking the logarithm of a feature changes nothing. Linear scorers do not have this property.
- **Interactions.** A depth-$D$ tree models interactions of up to $D$ features. The planted rule of the tests needs depth 2.
- **Uses the second derivative.** The leaf step is larger where the frozen cost is flat ($h$ small) and smaller where it is curved, unlike plain gradient boosting with a fixed step.
- **Query-local targets.** The targets and weights of each query depend only on that query, but the trees are shared by all queries.
- **Deterministic.** With a fixed tie rule for scores and splits, the output depends only on the data and the parameters.

## Variants and improvements

- **Histogram split finding.** Binning features and summing $g$ and $h$ per bin makes split search linear in $N$, as in LightGBM and XGBoost.
- **Second-order split gain.** Choose the split by the Newton gain $(\sum g)^2 / \sum h$ of each child, with a regularizer, rather than by least squares on $g$. This is common in later libraries and differs from Burges (2010), Section 7.
- **Other metrics.** Replace $|\Delta Z|$ by the swap change of ERR or MAP, as in LambdaRank.
- **Unbiased versions.** Weight the pairs by inverse examination propensities when the labels are clicks; see [unbiased learning to rank](/unbiased-learning-to-rank/).
- **Ensembles.** Average several LambdaMART models trained with different seeds or subsamples; the winning 2010 Yahoo! entry was such an ensemble.

## When to use it

Use LambdaMART when each query-document pair is described by a few hundred hand-made features such as [BM25](/bm25/) scores, click counts and page quality signals, and the metric is NDCG@$k$ or similar. It is the usual baseline on feature-based ranking benchmarks, and its strong results there are measured, not proved. When the inputs are raw text, a neural scorer such as a [cross-encoder](/cross-encoder-reranking/) usually does better, at a much higher cost per document.

## Pitfalls

- **Recompute the ranks every round.** Line L3 must sort by the current $F$. Reusing the ranks of round 1 fits every later tree to stale weights.
- **Zero weights.** A leaf whose documents are in no pair with nonzero weight has $\sum h = 0$. Line L6 must return 0 there, not divide by zero.
- **Exact Newton by mistake.** Computing the leaf value from the full Hessian of the leaf gives a different step from line L6. Both are defensible, but only line L6 is the formula of Burges (2010), and they differ whenever a pair lies inside a leaf.
- **No shrinkage.** With $\eta = 1$ in line L7, the Newton step of a nearly flat leaf can be huge, as in the example, and overshoot. Use $\eta$ around 0.1 and more rounds.
- **The sign convention.** Line L4 uses $g = -\lambda$ for a cost. Mixing it with the utility convention $y = \lambda$ without also flipping the weights moves every leaf the wrong way.

## Implementations

## History

Friedman's MART is the gradient boosting machine with regression trees and a Newton step per leaf. Burges and colleagues had defined the LambdaRank gradients for neural networks, and Wu, Burges, Svore and Gao (2010) fitted MART to those gradients, which gave LambdaMART. In his 2010 overview, Burges described the algorithm in full and noted that an ensemble of LambdaMART rankers won Track 1 of the 2010 Yahoo! Learning to Rank Challenge. Boosted tree libraries later added LambdaMART objectives, and it became the common reference model for feature-based ranking.

## References
