---
tag: TRPVZ8
kind: algorithm
slug: listnet
name: ListNet
aliases:
- listwise top-one probability loss
area: information-retrieval-and-ai-reasoning/ranking-models
level: advanced
summary: Trains a scorer by minimizing the cross-entropy between top-one probability distributions induced by predicted and true scores.
solves: [learning-to-rank]
model: word-ram
complexity:
  vars: {N: the number of documents, d: the number of features, T: the number of steps}
  time: {per_step: O(N d), total: O(T N d)}
  space: {extra: O(N + d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2007
  people: [Zhe Cao, Tao Qin, Tie-Yan Liu, Ming-Feng Tsai, Hang Li]
  note: Cao, Qin, Liu, Tsai and Li proposed in 2007 to define the loss on whole lists rather than on pairs, using probability distributions over permutations and their top-one marginals.
prereqs: [learning-to-rank, cross-entropy-loss]
see_also: [softmax-regression, ranknet, lambdarank, lambdamart, ranking-svm, normalized-discounted-cumulative-gain, gradient-descent, dense-passage-retrieval]
sources:
  - paper: doi:10.1145/1273496.1273513
    title: Zhe Cao, Tao Qin, Tie-Yan Liu, Ming-Feng Tsai and Hang Li, Learning to rank, from pairwise approach to listwise approach, Proceedings of the 24th International Conference on Machine Learning (ICML 2007)
    locator: pp. 129-136 (the permutation probability, the top-one probability, the cross-entropy loss and its gradient, and training of a neural network scorer by gradient descent)
---

ListNet trains a scoring function for [learning to rank](/learning-to-rank/) with a loss on the whole list of a query. It turns the scores into a probability distribution over the documents with a softmax, does the same with the labels, and minimizes the [cross-entropy](/cross-entropy-loss/) between the two. The cross-entropy-loss page treats a fixed target class; here the target is itself a distribution made from graded labels, and the classes are the documents of one query, so the number of classes changes from query to query. Unlike [RankNet](/ranknet/) and the Ranking SVM, no pairs are formed. This page gives the loss, the reason the softmax is the probability of being ranked first, the gradient $P_s - P_y$, a safe step for the linear model, and its known limits.

## In plain words

For one search request, we turn the scores of the results into shares that add up to 1. A result with a much higher score gets a much larger share. We also turn the true labels into shares in the same way. The method changes the scoring rule so that the two sets of shares agree. The share of a result can be read as the chance that it comes out first if we draw the results one by one at random, with better results more likely. The method looks at the whole list at once, and its cost grows with the number of results, not with the number of pairs.

## The problem

The input is a set of queries; query $q$ has documents $x_1, \ldots, x_n \in \mathbb R^d$ and labels $y_1, \ldots, y_n$. The code uses the linear scorer $s_j = w \cdot x_j$; Cao et al. (2007) train a neural network scorer, which changes only how $\partial s_j / \partial w$ is computed. With $\varphi = \exp$, the top-one probabilities of the scores and of the labels are

$$P_s(j) = \frac{e^{s_j}}{\sum_{l=1}^{n} e^{s_l}}, \qquad P_y(j) = \frac{e^{y_j}}{\sum_{l=1}^{n} e^{y_l}},$$

and the loss is

$$L(w) = \sum_{\text{queries}} -\sum_{j=1}^{n} P_y(j) \log P_s(j).$$

$P_s(j)$ is the probability that $j$ comes first under the Plackett-Luce model, which draws document $j$ first with probability proportional to $e^{s_j}$, then the next one among those left in the same way. So the loss compares the first-place marginals of two distributions over the $n!$ permutations, at the cost of $n$ numbers instead of $n!$.

## The algorithm

```pseudo id=main
LISTNET(queries, T)
L1  w ← 0;  η ← 1 / M,  where M = Σ_queries max_j ‖x_j‖²
L2  repeat T times:
L3      for each query: s_j ← w · x_j
L4          P_s ← softmax(s),  P_y ← softmax(y)
L5      g ← Σ_queries Σ_j (P_s(j) - P_y(j)) x_j
L6      w ← w - η g
L7  return w
```

Line L4 is the whole loss computation. The gradient in the scores is $P_s - P_y$, so line L5 is one pass over the documents. Cao et al. (2007) train with a fixed learning rate; the step $1/M$ of line L1 is the one for which the proof shows that the loss never increases.

## Example

One query has three documents with labels $y = (2, 0, 1)$ and current scores $s = (1, 0, 0.5)$.

| document | $y_j$ | $s_j$ | $P_y(j)$ | $P_s(j)$ | $P_s(j) - P_y(j)$ |
|---|---|---|---|---|---|
| 0 | 2 | 1.0 | 0.6652 | 0.5065 | -0.1588 |
| 1 | 0 | 0.0 | 0.0900 | 0.1863 | 0.0963 |
| 2 | 1 | 0.5 | 0.2447 | 0.3072 | 0.0625 |

The loss is $0.8927$. The scores already rank the documents in the label order, so NDCG is 1, but the loss is not at its minimum: document 0 should have a larger share, and the gradient asks for a higher $s_0$ and lower $s_1$ and $s_2$. The minimum of the loss for this query is the entropy of $P_y$, $0.8324$, reached exactly when $s - y$ is a constant vector. At $s = 0$ the loss is $\ln 3 = 1.0986$ and the score gradient is $(-0.3319, 0.2433, 0.0886)$.

## Correctness

The proof in proofs/correctness.md shows:

- **Top-one probability.** Under the Plackett-Luce model with weights $e^{s_j}$, the probability that $j$ is ranked first is $P_s(j)$. The tests check it by a sum over the 24 permutations of 4 documents.
- **Gradient.** $\partial L / \partial s_j = P_s(j) - P_y(j)$ and $\nabla_w L = \sum_j (P_s(j) - P_y(j)) x_j$. The tests check both by central finite differences.
- **Convex and smooth.** For the linear model, $L$ is convex and its Hessian is at most $M I$, because the Hessian of one query is a covariance of $u \cdot x_j$ under $P_s$.
- **Descent.** With the step $1/M$, $L(w_{t+1}) \le L(w_t) - \frac{1}{2M}\lVert \nabla L(w_t) \rVert^2$.
- **Minimum.** For each query, $L \ge H(P_y)$, with equality exactly when $s - y$ is constant.

On the planted set of the tests (6 queries of 5 documents), 200 steps lower the loss from 9.657 to 8.410, against the bound $\sum H(P_y) = 7.997$, and the mean NDCG on the training queries rises from 0.713 at $w = 0$ to 1.0. The NDCG figures are measured, not proved: a lower loss does not imply a higher NDCG.

## Complexity

Each step computes $N$ scores in $O(N d)$, one softmax per query in $O(n_q)$, and the gradient in $O(N d)$. So a step costs $O(N d)$, and $T$ steps $O(T N d)$. A pairwise loss on the same data costs $O(P + N d)$ per step with the lambda factorization and $O(P d)$ without it, with $P$ up to $\sum n_q^2 / 2$. The extra space is $O(N + d)$. The full permutation distribution would cost $n!$ terms per query, which the top-one form avoids.

## Properties

- **Shift invariant per query.** Adding a constant to all scores of a query does not change $P_s$.
- **Depends on label values, not only their order.** The labels $(2, 0, 1)$ and $(4, 0, 2)$ give different $P_y$ and different minimizers. A rescaling of the label grades is a modeling choice.
- **Nonzero minimum.** The loss at its minimum is $\sum H(P_y)$, so its value alone does not show how close the model is to the best possible.
- **Not position aware.** The loss does not use a discount by rank; errors at the top and errors at the bottom count through the shares only.
- **Bounded gradient.** Each entry of $P_s - P_y$ is in $(-1, 1)$.

## Variants and improvements

- **Top-$k$ probabilities.** Cao et al. (2007) define the probability of the first $k$ positions in general and use $k = 1$ for cost reasons.
- **ListMLE.** Maximizes the Plackett-Luce likelihood of the label order itself, which fixes one permutation instead of matching marginals.
- **Softmax cross-entropy with one positive.** If $P_y$ puts all mass on one relevant document, the loss is the softmax loss used to train retrieval models such as [dense passage retrieval](/dense-passage-retrieval/), with the other documents as negatives.
- **Other transforms.** A different increasing $\varphi$ in place of $\exp$, or a temperature on $y$, changes how much the top label dominates $P_y$.

## When to use it

Use ListNet when the scorer is trained by gradients and the data have graded labels for every document of a query, and when the cost per step must be linear in the number of documents. Its loss is smooth, convex for a linear model, and simple to implement. If the target metric is NDCG@$k$ with a small $k$, [LambdaRank](/lambdarank/) or [LambdaMART](/lambdamart/) weight the top positions more directly; which works better on a given data set is a matter of measurement.

## Pitfalls

- **Overflow.** Line L4 must subtract the largest entry before exponentiating, or large scores or labels overflow. Use a log-softmax for the loss.
- **Softmax across queries.** Line L4 must normalize within one query. A softmax over all documents of all queries compares documents that never compete.
- **Large label scales.** Labels on a scale of 0 to 100 make $P_y$ almost one-hot. Rescale the labels before line L4, or the loss ignores all but the top document.
- **Reading the loss as quality.** The loss stays above $\sum H(P_y)$ even for a perfect ranking, as in the example, where NDCG is 1 but the loss is 0.8927. Monitor NDCG on held-out queries.
- **Step size.** A fixed step much larger than $1/M$ in line L6 can make the loss oscillate. $M$ grows with the number of queries in the batch.

## Implementations

## History

Cao, Qin, Liu, Tsai and Li (2007) argued that pairwise methods such as the Ranking SVM, RankBoost and RankNet optimize a loss on pairs, while ranking quality is a property of whole lists. They defined permutation probabilities by the Plackett-Luce model, showed that the top-one marginals are a softmax of the scores, and trained a neural network scorer with the resulting cross-entropy. ListNet started the listwise family of losses, which includes ListMLE and many later softmax losses.

## References
