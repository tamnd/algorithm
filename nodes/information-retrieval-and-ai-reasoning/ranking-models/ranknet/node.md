---
tag: DHZW3Q
kind: algorithm
slug: ranknet
name: RankNet
aliases:
- Burges RankNet
area: information-retrieval-and-ai-reasoning/ranking-models
level: advanced
summary: Trains a neural scoring function with a cross-entropy loss on the logistic probability that one document ranks above another.
solves: [learning-to-rank]
model: word-ram
complexity:
  vars: {N: the number of documents, P: the number of preferred pairs, d: the number of features, T: the number of steps}
  time: {per_step: O(P + N d), total: O(T (P + N d))}
  space: {extra: O(N + d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2005
  people: [Chris Burges, Tal Shaked, Erin Renshaw, Ari Lazier, Matt Deeds, Nicole Hamilton, Greg Hullender]
  note: Burges and colleagues at Microsoft Research proposed the pairwise logistic cost for a neural scorer in 2005. The factorization into lambdas, described in the 2010 overview by Burges, led to LambdaRank and LambdaMART.
prereqs: [logistic-loss, learning-to-rank]
see_also: [lambdarank, lambdamart, ranking-svm, listnet, rankboost, backpropagation, gradient-descent, normalized-discounted-cumulative-gain]
sources:
  - paper: doi:10.1145/1102351.1102363
    title: Chris Burges, Tal Shaked, Erin Renshaw, Ari Lazier, Matt Deeds, Nicole Hamilton and Greg Hullender, Learning to rank using gradient descent, Proceedings of the 22nd International Conference on Machine Learning (ICML 2005)
    locator: pp. 89-96 (the logistic model of the pair probability, the cross-entropy cost, and its training by back-propagation)
  - paper: "Christopher J. C. Burges, From RankNet to LambdaRank to LambdaMART: an overview, Microsoft Research Technical Report MSR-TR-2010-82, 2010"
    locator: Section 2 (the cost with a target probability) and Section 2.1 (the factorization of the gradient into lambdas)
---

RankNet trains a scoring function $s = f(x)$ for [learning to rank](/learning-to-rank/) from pairs of documents of one query. It models the probability that document $i$ should rank above document $j$ as a $\sigma$-scaled [logistic](/logistic-loss/) function of the score difference $s_i - s_j$ and minimizes the cross-entropy of that probability against the label order. The logistic-loss page treats one example with one label; here the "example" is a pair, and the useful step is the factorization of the gradient into one number $\lambda_i$ per document, so that one pass over the documents replaces one pass over the pairs. The learning-to-rank page shows one RankNet step on three documents; this page gives the algorithm, the factorization, a safe step size for the linear model, and a full training trace. The code uses a linear scorer $s = w \cdot x$; the original paper uses neural networks, which change only how $\partial s / \partial w$ is computed.

## In plain words

For one search request, take two results where we know which one is better. The model gives each result a score. A large score gap in the right direction means the model is confident and right, and costs almost nothing. A gap in the wrong direction costs a lot. We add these costs over all such pairs. To improve the model, we work out how much each result should move up or down, by adding the pushes from all its pairs. Then we change the model so that each result moves by that amount. Results that sit below many worse results get a strong push up.

## The problem

The input is a set of queries. Query $q$ has documents with feature vectors $x_1, \ldots, x_n \in \mathbb R^d$ and integer labels $y_1, \ldots, y_n$. The preferred pairs $\mathcal P$ of the query are the pairs $(i, j)$ with $y_i > y_j$. For a scale $\sigma > 0$ and scores $s_i = f(x_i)$, the model probability that $i$ ranks above $j$ is

$$P_{ij} = \frac{1}{1 + e^{-\sigma (s_i - s_j)}},$$

and the cost of a preferred pair is the cross-entropy against the target probability 1:

$$C_{ij} = -\log P_{ij} = \log\left(1 + e^{-\sigma (s_i - s_j)}\right), \qquad C = \sum_{\text{queries}} \sum_{(i,j) \in \mathcal P} C_{ij}.$$

Burges (2010), Section 2, allows a general target $\bar P_{ij} = \frac{1}{2}(1 + S_{ij})$ with $S_{ij} \in \{-1, 0, 1\}$; for a preferred pair $\bar P_{ij} = 1$ and the cost is the one above, and pairs with equal labels add a cost that pulls their scores together. The code keeps only the preferred pairs. The output is the scorer, and a query is ranked by sorting its documents by score, ties to the smaller id.

## The algorithm

For each pair, $\partial C_{ij} / \partial s_i = -\sigma / (1 + e^{\sigma(s_i - s_j)}) = -\partial C_{ij} / \partial s_j$. Call this number $\lambda_{ij}$. Summing the pairs that touch each document gives $\lambda_i = \partial C / \partial s_i$, and by the chain rule $\nabla_w C = \sum_i \lambda_i \nabla_w s_i$. For the linear scorer, $\nabla_w s_i = x_i$.

```pseudo id=main
RANKNET(queries, σ, T)
L1  w ← 0;  η ← 1 / L,  where L = (σ² / 4) Σ_{(i,j) ∈ P} ‖x_i - x_j‖²
L2  repeat T times:
L3      for each query: s_i ← w · x_i
L4          for each (i, j) ∈ P: λ_ij ← -σ / (1 + e^{σ (s_i - s_j)})
L5          λ_i ← Σ_j λ_ij - Σ_j λ_ji
L6      g ← Σ_queries Σ_i λ_i x_i
L7      w ← w - η g
L8  return w
```

Line L4 is the only work per pair, and it is a scalar. Line L6 is the only work per feature, and it is done once per document, not once per pair. With a neural scorer, line L6 becomes one back-propagation per document with the output gradient $\lambda_i$, and line L7 any gradient method.

## Example

One query has three documents with features A $= (1, 0)$, B $= (0, 1)$, C $= (1, 1)$ and labels 1, 0, 2, and $\sigma = 1$. The preferred pairs are (A, B), (C, A) and (C, B), with the differences $(1, -1)$, $(0, 1)$ and $(1, 0)$. So $L = \frac{1}{4}(2 + 1 + 1) = 1$ and $\eta = 1$.

At $w = 0$ every score is 0 and every $\lambda_{ij} = -0.5$. Document A is the better one of (A, B) and the worse one of (C, A), so $\lambda_A = -0.5 + 0.5 = 0$; B is the worse one twice, so $\lambda_B = 1$; C is the better one twice, so $\lambda_C = -1$. Then $g = 0 \cdot A + 1 \cdot B - 1 \cdot C = (-1, 0)$, and line L7 gives $w = (1, 0)$.

| step | $w$ | scores (A, B, C) | $\lambda$ (A, B, C) | $g$ | $C$ |
|---|---|---|---|---|---|
| 0 | $(0, 0)$ | $(0, 0, 0)$ | $(0, 1, -1)$ | $(-1, 0)$ | 2.0794 |
| 1 | $(1, 0)$ | $(1, 0, 1)$ | $(0.2311, 0.5379, -0.7689)$ | $(-0.5379, -0.2311)$ | 1.3197 |

The cost at step 0 is $3 \ln 2$. After step 1 the pair (C, A) is a tie and still has the push $-0.5$ on C, while A gets $-0.2689$ from (A, B) and $+0.5$ from (C, A). The cost after 0, 10, 20, 30, 40 and 50 steps is 2.0794, 0.3707, 0.2100, 0.1471, 0.1133 and 0.0922, and $w$ after 50 steps is about $(6.201, 2.874)$, which orders the documents C, A, B. The cost keeps falling but never reaches 0, because every pair can be ordered correctly and a larger $w$ always helps (see the remark in the proof file).

## Correctness

The proof in proofs/correctness.md shows:

- **The factorization.** $\nabla_w C = \sum_i \lambda_i x_i$ with $\lambda_i$ from lines L4 and L5. The tests check it against the sum over pairs and against finite differences of $C$.
- **Zero sum.** The lambdas of one query sum to 0, since each pair adds $\lambda_{ij}$ to one document and subtracts it from the other.
- **Convex and smooth.** For the linear scorer, $C$ is convex in $w$ and its Hessian is at most $L I$, because $P_{ij}(1 - P_{ij}) \le 1/4$.
- **Descent.** With $\eta = 1/L$, $C(w_{t+1}) \le C(w_t) - \frac{1}{2L}\lVert \nabla C(w_t) \rVert^2$, so the cost never increases.

These are statements about the pairwise cost. A smaller cost does not imply a larger [NDCG](/normalized-discounted-cumulative-gain/), and the rise of NDCG in the tests is measured on one planted data set, not proved.

## Complexity

Let $N$ be the number of documents and $P$ the number of preferred pairs, at most $\sum_q n_q^2 / 2$. One step computes the scores in $O(N d)$, the pair lambdas in $O(P)$ and the gradient in $O(N d)$, so it costs $O(P + N d)$. Without the factorization, summing $\lambda_{ij}(x_i - x_j)$ over the pairs costs $O(P d)$. The extra space is $O(N + d)$ for the scores, the lambdas and the gradient. With a neural scorer, the factorization replaces $P$ back-propagations by $N$.

## Properties

- **Shift invariant.** Adding the same constant to all scores of a query changes nothing, because only differences enter.
- **Smooth surrogate of the pair order.** $C_{ij} \ge \log 2$ when $s_i \le s_j$, so $C / \log 2$ bounds the number of misordered pairs, as the hinge loss does for the [Ranking SVM](/ranking-svm/).
- **Equal weight per pair.** A pair at ranks 1 and 2 counts the same as a pair at ranks 50 and 51. This is the property that [LambdaRank](/lambdarank/) changes.
- **No minimizer on separable data.** If a linear $w$ orders all pairs, $C(t w) \to 0$ as $t \to \infty$ and the weights grow without bound. A weight penalty or a target $\bar P_{ij} < 1$ fixes it.
- **Bounded pushes.** $|\lambda_{ij}| < \sigma$, so one badly ordered pair cannot dominate the gradient, unlike a squared loss on the score difference.

## Variants and improvements

- **LambdaRank** multiplies each $\lambda_{ij}$ by the change of NDCG from swapping $i$ and $j$.
- **LambdaMART** fits [gradient-boosted](/gradient-boosting/) trees to the lambdas instead of a neural network.
- **Neural scorers.** The original paper trains neural networks with [back-propagation](/backpropagation/). With the factorization, one query is a natural mini-batch: one forward pass per document, then one backward pass per document with the output gradient $\lambda_i$.
- **Ties and soft targets.** The target $\bar P_{ij} = \frac{1}{2}(1 + S_{ij})$ of Burges (2010) puts a cost on pairs of equal label.
- **Listwise costs.** [ListNet](/listnet/) replaces the sum over pairs by a cross-entropy between distributions over the whole list.

## When to use it

Use RankNet when the scorer is a neural network and the training signal is pairwise preferences, for example from graded labels or from clicks. It is the base of the LambdaRank family, and its lambdas are the right first step to understand LambdaMART. If the metric weights the top of the list heavily, LambdaRank or LambdaMART usually do better on feature-based benchmarks, which is a measured result. For a linear scorer with a margin, the Ranking SVM gives a similar problem with a unique solution.

## Pitfalls

- **Overflow in the cost.** Computing $\log(1 + e^{-\sigma o})$ directly overflows for large $-\sigma o$. Use the stable softplus for $C_{ij}$, and in line L4 compute $1/(1 + e^{\sigma o})$ through a stable sigmoid.
- **The sign of the update.** Line L5 adds $\lambda_{ij}$ to the better document and subtracts it from the worse one. Swapping the two signs trains the model to reverse the order.
- **Pairs across queries.** Line L4 must loop over pairs of one query. Pairs from two queries ask for one score scale that the problem does not need.
- **Step size.** A fixed step much larger than $1/L$ in line L7 can make the cost oscillate. The bound $L$ of line L1 grows with the number of pairs, so a query set with many pairs needs a smaller step.
- **No stopping point on separable data.** Running line L2 longer always lowers the cost and grows $w$. Stop by validation NDCG, or add a penalty.

## Implementations

## History

Burges, Shaked, Renshaw, Lazier, Deeds, Hamilton and Hullender (2005) introduced the probabilistic pairwise cost and trained neural network scorers with it on web search data. In his 2010 overview, Burges wrote the gradient as a sum over documents of the lambdas, which made training faster and suggested changing the lambdas directly. That idea gave LambdaRank, and fitting boosted trees to the same lambdas gave LambdaMART.

## References
