---
tag: VTCXN6
kind: algorithm
slug: ranking-svm
name: Ranking SVM
aliases:
- RankSVM
area: information-retrieval-and-ai-reasoning/ranking-models
level: core
summary: Learns a linear scoring function by solving an SVM on pairwise preferences between documents of the same query.
solves: [learning-to-rank]
model: word-ram
complexity:
  vars: {P: the number of preferred pairs, d: the number of features, T: the number of steps}
  time: {per_step: O(P d), total: O(T P d)}
  space: {extra: O(P d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2000
  people: [Ralf Herbrich, Thore Graepel, Klaus Obermayer, Thorsten Joachims]
  note: Herbrich, Graepel and Obermayer gave the large margin method for pairs in 2000, and Joachims applied it to web search in 2002, with preferences read from click logs.
prereqs: [support-vector-machine, learning-to-rank]
see_also: [hinge-loss, subgradient, kendall-tau-distance, ranknet, rankboost, roc-auc, click-model, unbiased-learning-to-rank]
sources:
  - paper: doi:10.7551/mitpress/1113.003.0010
    title: Ralf Herbrich, Thore Graepel and Klaus Obermayer, Large margin rank boundaries for ordinal regression, in Advances in Large Margin Classifiers, MIT Press, 2000
    locator: Chapter 7, pp. 115-132 (the reduction of ordinal regression to a large margin problem on pairs of objects)
  - paper: doi:10.1145/775047.775067
    title: Thorsten Joachims, Optimizing search engines using clickthrough data, Proceedings of the 8th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 2002
    locator: pp. 133-142 (preferences from clicks, the Ranking SVM on pair differences, and the bound of the number of discordant pairs by the slack sum)
  - paper: doi:10.1145/1273496.1273598
    title: Shai Shalev-Shwartz, Yoram Singer and Nathan Srebro, Pegasos, primal estimated sub-gradient solver for SVM, Proceedings of the 24th International Conference on Machine Learning (ICML 2007)
    locator: pp. 807-814 (the step 1/(lambda t), the projection onto a ball, and the log T over T rate for strongly convex objectives)
  - paper: doi:10.1145/1150402.1150429
    title: Thorsten Joachims, Training linear SVMs in linear time, Proceedings of the 12th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 2006
    locator: pp. 217-226 (cutting-plane training of linear SVMs, with a formulation for ordinal regression)
---

Ranking SVM learns a linear scoring function $f(x) = w \cdot x$ for [learning to rank](/learning-to-rank/). For each query and each two of its documents with different labels, it asks that the better document score at least 1 more than the worse one, and it pays the [hinge loss](/hinge-loss/) when it does not. With the norm penalty of a [support vector machine](/support-vector-machine/), this is an SVM on the difference vectors $x_i - x_j$. The learning-to-rank page states the problem and lists the methods; this page gives the objective, a solver with a proved rate, and what a low objective guarantees about the order of the training pairs. [RankNet](/ranknet/) uses the same pairs with the logistic loss in place of the hinge loss.

## In plain words

For each search request we know which results are better than which. Take two results of the same request, a better one and a worse one. We want a scoring rule that gives the better one a clearly higher score. Each such pair is a small test, and the rule loses points on every pair that it gets wrong or gets right by too little. We also keep the rule simple, so that it does not chase noise. The method finds the rule that balances these two costs. It never compares results of two different requests, because their scores do not need to match. When the cost is small enough, every training pair comes out in the right order.

## The problem

The input is a set of queries. Query $q$ has documents with feature vectors $x_{q,1}, \ldots, x_{q,n_q} \in \mathbb R^d$ and integer labels $y_{q,i}$. The preferred pairs are the $P$ pairs $(i, j)$ of one query with $y_{q,i} > y_{q,j}$, and $z = x_{q,i} - x_{q,j}$ is the pair vector. The output is $w \in \mathbb R^d$, and a new query is ranked by sorting its documents by $w \cdot x$, ties to the smaller id. For $\lambda > 0$, the objective is

$$J(w) = \frac{\lambda}{2} \lVert w \rVert^2 + \frac{1}{P} \sum_{k=1}^{P} \max(0, 1 - w \cdot z_k).$$

Joachims (2002) writes the same problem with slack variables $\xi_k \ge 1 - w \cdot z_k$, $\xi_k \ge 0$ and the constant $C$ in place of $1/(\lambda P)$. Pairs from different queries never form a pair, so the scores of different queries need not be on one scale.

## The algorithm

The code solves the objective with the projected [subgradient](/subgradient/) method of Pegasos, run on the full set of pairs.

```pseudo id=main
RANKING-SVM(queries, λ, T)
L1  Z ← the vectors x_i - x_j for all pairs of one query with y_i > y_j
L2  w ← 0, R ← sqrt(2 / λ), best ← w
L3  for t ← 1 to T:
L4      g ← λ w - (1 / P) Σ { z ∈ Z : w · z < 1 } z
L5      w ← w - g / (λ t)
L6      if ‖w‖ > R: w ← w R / ‖w‖
L7      if J(w) < J(best): best ← w
L8  return best
```

Line L4 is a subgradient of $J$ at $w$: the pairs with margin below 1 push $w$ toward their direction, and the penalty pulls it toward 0. Line L5 takes the step $1/(\lambda t)$, which suits a $\lambda$-strongly convex objective. Line L6 projects back onto the ball of radius $\sqrt{2/\lambda}$, which holds the minimizer because $\frac{\lambda}{2}\lVert w^* \rVert^2 \le J(w^*) \le J(0) = 1$. The subgradient method is not a descent method, so line L7 keeps the best iterate.

## Example

One query has three documents A, B and C with the features $(2, 0)$, $(1, 1)$, $(0, 1)$ and the labels 2, 1, 0. The pairs are A over B, A over C and B over C, with $z_1 = (1, -1)$, $z_2 = (2, -1)$, $z_3 = (1, 0)$, so $P = 3$. Take $\lambda = 0.1$, so $R = \sqrt{20} \approx 4.472$.

| $t$ | pairs with $w \cdot z < 1$ | $g$ | projected | $w$ after the step | $J(w)$ | best $J$ |
|---|---|---|---|---|---|---|
| 1 | all three | $(-1.3333, 0.6667)$ | yes | $(4, -2)$ | 1.0000 | 1.0000 |
| 2 | none | $(0.4, -0.2)$ | no | $(2, -1)$ | 0.2500 | 0.2500 |
| 3 | none | $(0.2, -0.1)$ | no | $(1.3333, -0.6667)$ | 0.1111 | 0.1111 |
| 4 | none | $(0.1333, -0.0667)$ | no | $(1, -0.5)$ | 0.0625 | 0.0625 |
| 5 | none | $(0.1, -0.05)$ | no | $(0.8, -0.4)$ | 0.1067 | 0.0625 |
| 6 | $z_3$ | $(-0.2533, -0.04)$ | no | $(1.2222, -0.3333)$ | 0.0802 | 0.0625 |

At step 5 the penalty has pulled $w$ so far that $w \cdot z_3 = 0.8 < 1$ and $J$ rises, which is why line L7 keeps the best iterate. The minimizer is $w^* = (1, 0)$ with $J^* = 0.05$: it gives the margins 1, 2 and 1, so every hinge term is 0. The dual point that puts the weight $0.3$ on $z_3$ and 0 on the other pairs has the dual value $0.05$, which proves that $0.05$ is optimal (see the proof file). After 100 steps the best $J$ is within $2.3 \cdot 10^{-5}$ of $J^*$, and after 1000 steps within $2.0 \cdot 10^{-7}$. The learned $w$ ranks A, B, C, the order of the labels.

## Correctness

The proof in proofs/correctness.md shows four things.

- **Rate.** With $G = \lambda R + \max_k \lVert z_k \rVert$, the best of the first $T$ iterates has $J - J^* \le G^2(1 + \ln T)/(2 \lambda T)$. The proof combines the strong convexity inequality of the subgradient with the step $1/(\lambda t)$, and the terms in the distance to $w^*$ telescope.
- **A dual lower bound.** For $\alpha \in [0, 1]^P$, $D(\alpha) = \frac{1}{P}\sum_k \alpha_k - \frac{1}{2\lambda P^2} \lVert \sum_k \alpha_k z_k \rVert^2 \le J(w)$ for every $w$. Exact coordinate ascent on $D$ gives the reference values that the tests use.
- **Pairs.** The number of training pairs that $w$ misorders is at most $P\, J(w)$, so $J(w) < 1/P$ means that every training pair is in the right order. This is the bound of Joachims (2002) that the slack sum bounds the number of discordant pairs, which is the [Kendall tau distance](/kendall-tau-distance/) to the label order over pairs with different labels.
- **Separable data.** If some $u$ has $u \cdot z_k \ge 1$ for all $k$ and $\frac{\lambda}{2}\lVert u \rVert^2 < 1/P$, the best iterate orders every training pair correctly after finitely many steps.

All four are statements about the training pairs. How well the learned $w$ ranks new queries is measured, not proved.

## Complexity

A query with $n$ documents gives at most $n(n - 1)/2$ pairs, so $P \le \sum_q n_q^2 / 2$. Line L1 costs $O(P d)$ time and stores $O(P d)$ numbers. Each step computes $w \cdot z$ for all pairs, adds the active ones and evaluates $J$, so it costs $O(P d)$ time; $T$ steps cost $O(T P d)$. The space beyond the input is $O(P d)$ for the pair vectors, or $O(d)$ if the pairs are formed on the fly from the documents. The rate bound shows that $T = O(G^2 / (\lambda \varepsilon) \log(1/\varepsilon))$ steps reach accuracy $\varepsilon$. A stochastic version, as in Pegasos, samples one pair per step and costs $O(d)$ per step.

## Properties

- **Convex.** The objective is $\lambda$-strongly convex and has one minimizer. Any solver that reaches it gives the same $w$.
- **Linear in the features.** The model is $w \cdot x$. The [kernel trick](/kernel-trick/) applies to the dual, with the kernel of a pair $\langle x_i - x_j, x_k - x_l \rangle$ expanded into four kernel values.
- **Only order within a query matters.** Adding the same vector to all documents of a query does not change any pair vector.
- **Few active pairs.** At the optimum, the pairs with margin above 1 have dual weight 0 and do not affect $w$. In the example only $z_3$ has a positive dual weight.
- **Equal weight per pair.** A misordered pair at ranks 1 and 2 costs the same as one at ranks 50 and 51. The objective does not know about the top of the list.

## Variants and improvements

- **Cutting planes.** Joachims (2006) trains linear SVMs, including a ranking formulation, with a cutting-plane method whose work grows linearly with the data.
- **Dual coordinate ascent.** The method of the proof file, one dual weight at a time, converges fast on small problems and gives a duality gap as a stopping test.
- **Stochastic subgradient.** Sample one pair per step. This is Pegasos with pairs as the examples, and it scales to very large $P$.
- **Bipartite labels.** With labels in $\{0, 1\}$, the fraction of pairs in the right order is the [area under the ROC curve](/roc-auc/), so the method maximizes a convex bound on AUC.
- **Query and position weights.** Weight each pair by its query or by a cost that grows near the top. [LambdaRank](/lambdarank/) weights by the change of NDCG; the propensity SVM-Rank of Joachims, Swaminathan and Schnabel (2017) weights by the inverse examination propensity (see [unbiased learning to rank](/unbiased-learning-to-rank/)).
- **Other losses on the same pairs.** The logistic loss gives RankNet, and the exponential loss gives [RankBoost](/rankboost/).

## When to use it

Use Ranking SVM when the features are good, the model can be linear, and you want a convex problem with a unique answer and a clean stopping test. It is a strong first baseline, and its pair data come directly from click logs in the way Joachims (2002) proposed. If the metric cares much more about the top positions than about the rest, [LambdaMART](/lambdamart/) usually ranks better on feature-based benchmarks, which is a measured result. If the model must be nonlinear, use trees or a neural scorer.

## Pitfalls

- **Pairs across queries.** Line L1 must form pairs only inside one query. Pairs across queries ask for one score scale for all queries, which the problem does not need and the data rarely support.
- **The best iterate.** The subgradient method can raise $J$, as at step 5 of the example. Returning the last $w$ of line L5 in place of the best of line L7 loses the guarantee of the theorem.
- **The radius.** Line L6 needs a radius that holds the minimizer. With the objective above, $\sqrt{2/\lambda}$ is safe. A different scale of the loss, for example $C \sum \xi$ without the $1/P$, needs a different radius.
- **Pair counts.** A query with many documents gives many more pairs than a short one and dominates the sum. Divide each query's pairs by their number if every query should count the same.
- **Ties in the labels.** Documents with the same label form no pair. Do not add pairs with a target of zero difference; the hinge loss would push them apart.

## Implementations

## History

Herbrich, Graepel and Obermayer (2000) treated ordinal regression as a large margin problem on pairs of objects, with the margin taken on the difference of their feature vectors. Joachims (2002) used the same pairwise SVM for web search and showed how click logs give the pairs: a clicked result is preferred to an unclicked result ranked above it. He also observed that the slack sum bounds the number of discordant pairs, which ties the objective to the Kendall tau measure. Faster solvers followed, among them the cutting-plane method of Joachims (2006) and the stochastic subgradient method of Shalev-Shwartz, Singer and Srebro (2007). The pairwise view also led to RankNet and RankBoost, and later to the propensity-weighted version for biased clicks.

## References
