---
tag: FQ86DQ
kind: algorithm
slug: rankboost
name: RankBoost
aliases:
- Freund-Iyer-Schapire-Singer RankBoost
area: information-retrieval-and-ai-reasoning/ranking-models
level: advanced
summary: Boosts weak rankers by reweighting the misordered document pairs at each round, minimizing an exponential pairwise loss.
solves: [learning-to-rank]
model: word-ram
complexity:
  vars: {N: the number of documents, P: the number of crucial pairs, d: the number of features, T: the number of rounds}
  time: {per_round: O(P + d N log N), total: O(T (P + d N log N))}
  space: {extra: O(P + N)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2003
  people: [Yoav Freund, Raj Iyer, Robert Schapire, Yoram Singer]
  note: Freund, Iyer, Schapire and Singer adapted AdaBoost to preferences over pairs. A conference version appeared at ICML 1998 and the journal version in JMLR in 2003.
prereqs: [adaboost, learning-to-rank]
see_also: [boosting, decision-stump, ranking-svm, ranknet, lambdamart, roc-auc, rank-aggregation, weak-learnability-equivalence]
sources:
  - paper: "Yoav Freund, Raj Iyer, Robert E. Schapire and Yoram Singer, An efficient boosting algorithm for combining preferences, Journal of Machine Learning Research 4, 2003"
    locator: pp. 933-969; Figure 1 (the algorithm), Section 3 and Theorem 1 (the ranking loss is at most the product of the Z_t), Section 3.2 (the choices of alpha), Section 3.3 and Figure 2 (RankBoost.B for bipartite feedback), Section 4 (threshold weak rankers)
---

RankBoost learns a ranking function $H(x) = \sum_t \alpha_t h_t(x)$ for [learning to rank](/learning-to-rank/) by [boosting](/boosting/) on pairs. It keeps a distribution $D$ over the crucial pairs, the pairs $(x_0, x_1)$ where $x_1$ should rank above $x_0$. Each round picks a weak ranker $h_t$ that orders the heavy pairs well, gives it a weight $\alpha_t$, and multiplies the weight of each pair by $e^{\alpha_t (h_t(x_0) - h_t(x_1))}$, so pairs that $h_t$ misorders get heavier. The [AdaBoost](/adaboost/) page does this for labeled examples; here the examples are pairs and a weak ranker is any real function, so the analysis bounds the fraction of misordered pairs, not a classification error. The learning-to-rank page lists RankBoost among the pairwise methods; this page gives the algorithm, the bound $\mathrm{rloss} \le \prod Z_t$, the choice of $\alpha$, the threshold weak learner, and a traced run.

## In plain words

We have pairs of results where we know which one should come first. We build the scoring rule from many very simple rules, each looking at one feature and asking whether it is above a cut. Every pair has a weight, and at the start all weights are equal. In each round we choose the simple rule that gets the most weight of pairs right, and we decide how much to trust it. Then we make the pairs it got wrong heavier and the pairs it got right lighter, so the next rule focuses on the hard pairs. The final score adds the simple rules with their trust values.

## The problem

The input is a set of queries with documents $x \in \mathbb R^d$ and labels. The crucial pairs are the pairs $(x_0, x_1)$ of one query with label of $x_1$ greater than label of $x_0$; there are $P$ of them, with the initial distribution $D_1$ uniform. A weak ranker is a function $h : \mathbb R^d \to [0, 1]$; the code uses the thresholds $h(x) = [x_f > \theta]$. The ranking loss of a scorer $H$ is the weighted fraction of crucial pairs that it does not order strictly right:

$$\mathrm{rloss}(H) = \sum_{(x_0, x_1)} D_1(x_0, x_1)\, [H(x_0) \ge H(x_1)].$$

A tie counts as an error. RankBoost minimizes the exponential upper bound $\sum D_1 e^{H(x_0) - H(x_1)}$ of this loss greedily, one weak ranker at a time.

## The algorithm

For a weak ranker $h$ under the distribution $D$, let $r = \sum D(x_0, x_1)(h(x_1) - h(x_0)) \in [-1, 1]$.

```pseudo id=main
RANKBOOST(pairs, T)
L1  D_1(p) ← 1 / P for each crucial pair p
L2  for t ← 1 to T:
L3      h_t ← the threshold ranker [x_f > θ] with the largest |r_t| under D_t
L4      α_t ← (1/2) ln((1 + r_t) / (1 - r_t))
L5      Z_t ← Σ_p D_t(p) e^{α_t (h_t(x_0) - h_t(x_1))}
L6      D_{t+1}(p) ← D_t(p) e^{α_t (h_t(x_0) - h_t(x_1))} / Z_t
L7  return H = Σ_t α_t h_t
```

Line L4 is method 3 of Freund et al. (2003), Section 3.2, which minimizes an upper bound on $Z_t$ and is the choice used in their experiments. Line L3 maximizes $|r|$, which minimizes that bound. A negative $r_t$ gives a negative $\alpha_t$, which reverses the weak ranker.

## Example

One query has four documents with features $(0, 1)$, $(1, 0)$, $(2, 2)$, $(3, 1)$ and labels 0, 1, 2, 1. The crucial pairs say that documents 1, 2 and 3 are above document 0, and document 2 is above documents 1 and 3: five pairs, each with weight $0.2$ at the start.

| round | weak ranker | $r_t$ | $\alpha_t$ | $Z_t$ | $\sqrt{1 - r_t^2}$ | $\prod Z$ | rloss after the round |
|---|---|---|---|---|---|---|---|
| 1 | $[x_0 > 0.5]$ | 0.6 | 0.6931 | 0.7000 | 0.8000 | 0.7000 | 0.4 |
| 2 | $[x_1 > 1.5]$ | 0.7143 | 0.8959 | 0.5773 | 0.6999 | 0.4041 | 0.0 |
| 3 | $[x_0 > 0.5]$ | 0.5959 | 0.6868 | 0.7039 | 0.8030 | 0.2845 | 0.0 |

In round 1, three thresholds tie at $r = 0.6$: $[x_0 > 0.5]$, $[x_0 > 1.5]$ and $[x_1 > 1.5]$; the code takes the first in the order of feature and threshold. $[x_0 > 0.5]$ orders the three pairs above document 0 and ties on the two pairs above documents 1 and 3, so $\alpha_1 = \frac{1}{2}\ln 4 = \ln 2$, and the two tied pairs are errors, $\mathrm{rloss} = 0.4$. Their weights grow from $0.2$ to $2/7$, and the other three fall to $1/7$. Round 2 picks $[x_1 > 1.5]$, which puts document 2 on top, with $r = 1/7 + 2/7 + 2/7 = 5/7$. After it, every pair is ordered right. At each round, $Z_t$ is below $\sqrt{1 - r_t^2}$ and the ranking loss is below $\prod Z$, as the proof requires.

## Correctness

The proof in proofs/correctness.md shows:

- **The bound.** Unrolling line L6 gives $D_{T+1} = D_1 e^{H(x_0) - H(x_1)} / \prod_t Z_t$. Since $D_{T+1}$ sums to 1 and $e^u \ge [u \ge 0]$, $\mathrm{rloss}(H) \le \prod_{t} Z_t$. This is the theorem of Freund et al. (2003), Section 3, and it holds after every round, for any choice of $\alpha_t$.
- **The choice of $\alpha$.** For $h$ with values in $[0, 1]$, convexity of $e^{\alpha u}$ gives $Z \le \frac{1 - r}{2} e^{\alpha} + \frac{1 + r}{2} e^{-\alpha}$, minimized by the $\alpha$ of line L4 at the value $\sqrt{1 - r^2}$. So $\mathrm{rloss}(H) \le \exp(-\frac{1}{2} \sum_t r_t^2)$.
- **Exact minimum for 0-1 rankers.** For $h \in \{0, 1\}$, $Z(\alpha) = W_{-1} e^{-\alpha} + W_0 + W_1 e^{\alpha}$ is minimized at $\alpha = \frac{1}{2}\ln(W_{-1}/W_1)$, method 2 of the paper. It can give a smaller $Z$ than line L4.
- **The weak learner.** Line L3 tries the midpoint between each two consecutive distinct values of each feature, which covers every distinct threshold ranker.

All of this is about the training pairs. How well $H$ orders the pairs of new queries is measured, not proved here.

## Complexity

Write $\pi(x) = \sum_{x_0} D(x_0, x) - \sum_{x_1} D(x, x_1)$ for each document, the weight of pairs where $x$ should be above minus the weight where it should be below. Then $r = \sum_x h(x)\, \pi(x)$, so after computing $\pi$ in $O(P)$, all thresholds of one feature are scored in one pass over the documents sorted by that feature. With the sorted orders kept from the start, a round costs $O(P + d N)$; sorting anew costs $O(P + d N \log N)$. Lines L5 and L6 cost $O(P)$. The space is $O(P + N)$. The code in this repository computes $r$ directly for each candidate, which is $O(d N P)$ per round and is meant only as a reference. Predicting a document costs $O(T)$.

## Properties

- **The bound needs no assumption.** $\mathrm{rloss} \le \prod Z_t$ holds for any weak rankers and any $\alpha_t$.
- **Fast training loss decay.** If every round has $|r_t| \ge \gamma$, the training ranking loss is at most $e^{-\gamma^2 T / 2}$.
- **Scale free features.** Threshold rankers depend only on the order of feature values, so monotone transforms of a feature change nothing.
- **Exponential weights.** Pairs that stay misordered gain weight exponentially, so label noise can dominate later rounds, as in AdaBoost.
- **Equal weight per pair.** The loss knows nothing about positions in the list, like the [Ranking SVM](/ranking-svm/) and [RankNet](/ranknet/).

## Variants and improvements

- **RankBoost.B.** For bipartite feedback, relevant against irrelevant, Freund et al. (2003), Section 3.3, keep one weight per document instead of one per pair, which reduces the cost from $O(P)$ to $O(N)$ per round. The ranking loss is then the fraction of relevant-irrelevant pairs in the wrong order, which is one minus the [area under the ROC curve](/roc-auc/) when ties count as errors.
- **Missing features.** The weak rankers of Freund et al. (2003), Section 4, give a default value $q_{\text{def}}$ to documents for which a feature is missing.
- **Method 2.** For 0-1 rankers, choose $\alpha$ by the exact minimum of $Z$ and the weak ranker by the smallest such $Z$.
- **Combining rankings.** Each feature can be the score of another ranker, which makes RankBoost a learned form of [rank aggregation](/rank-aggregation/), the setting the paper started from.
- **Boosted trees on pairwise losses.** [LambdaMART](/lambdamart/) also boosts, with regression trees and a position-aware gradient in place of exponential weights.

## When to use it

Use RankBoost when the features are scores or votes from several sources, the labels give preferences rather than grades, and a simple, interpretable additive model of thresholds is wanted. Its training bound is clean and needs no tuning of a step size. When the metric weights the top of the list or the data are large, LambdaMART is the usual choice today, which is a measured judgment.

## Pitfalls

- **Ties are errors.** The loss of line L7 counts $H(x_0) = H(x_1)$ as wrong. Counting ties as right, as some evaluations do, makes the bound look loose and hides weak rankers that do not separate pairs.
- **A perfect weak ranker.** If $|r_t| = 1$, line L4 divides by zero. Clip $|r|$ slightly below 1; the code uses $1 - 10^{-10}$, which gives $\alpha \approx 11.9$.
- **Pairs across queries.** The crucial pairs of line L1 must come from one query, or the model learns to order queries.
- **Normalizing.** Line L6 must divide by $Z_t$. Without it, the weights shrink or grow exponentially and the $r$ of later rounds is not on the scale that line L4 assumes.
- **Overfitting with many rounds.** The training loss can fall to 0 quickly, as in the example after two rounds. Choose $T$ by validation.

## Implementations

## History

Freund, Iyer, Schapire and Singer presented RankBoost at ICML in 1998, in the setting of combining the preferences of several experts, such as several search engines, and published the full version in JMLR in 2003. It carried the AdaBoost analysis to pairs: the bound on the training ranking loss, the choices of $\alpha$, an efficient bipartite version, and threshold weak rankers. It was one of the first learning-to-rank methods and is a standard baseline beside the Ranking SVM and RankNet.

## References
