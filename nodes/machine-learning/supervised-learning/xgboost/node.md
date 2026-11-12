---
tag: 57E0E8
kind: algorithm
slug: xgboost
name: XGBoost
aliases:
- extreme gradient boosting
area: machine-learning/supervised-learning
level: advanced
summary: "Gradient tree boosting with a second-order objective, leaf weights -G/(H + λ), a split gain with penalties λ and γ, default directions for missing values and a weighted quantile sketch."
solves: [regression, classification]
model: real-ram
complexity:
  vars: {n: the number of training examples, T: the number of trees, D: the depth of each tree, z: the number of present entries of the data matrix}
  time: {worst: "O(T D z log n)"}
  space: {extra: "Θ(z + n + T 2^D)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2016
  people: [Tianqi Chen, Carlos Guestrin]
  note: Chen and Guestrin described the XGBoost system at KDD 2016.
prereqs: [gradient-boosting, decision-tree-learning]
see_also: [cart, newton-raphson-method, regularization, quantile-summary-problem, kll-sketch, logistic-loss, random-forest]
sources:
  - paper: doi:10.1145/2939672.2939785
    title: Tianqi Chen and Carlos Guestrin, XGBoost, a scalable tree boosting system, Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2016
    locator: Section 2 (the regularized objective, the second-order approximation, the leaf weight, the structure score and the split gain), Section 3 (Algorithm 1 exact greedy, Algorithm 2 approximate, the weighted quantile sketch, Algorithm 3 sparsity-aware split finding) and Section 4 (the column blocks)
  - paper: doi:10.1214/aos/1013203451
    title: Jerome H. Friedman, Greedy function approximation, a gradient boosting machine, Annals of Statistics 29(5), 2001
    locator: gradient boosting and TreeBoost, the method that XGBoost extends
  - paper: doi:10.1214/aos/1016218223
    title: Jerome Friedman, Trevor Hastie and Robert Tibshirani, Additive logistic regression, a statistical view of boosting, Annals of Statistics 28(2), 2000
    locator: boosting by Newton steps (LogitBoost)
  - paper: doi:10.1145/375663.375670
    title: Michael Greenwald and Sanjeev Khanna, Space-efficient online computation of quantile summaries, SIGMOD 2001
    locator: the unweighted quantile summary that the weighted sketch extends
  - paper: "Guolin Ke, Qi Meng, Thomas Finley, Taifeng Wang, Wei Chen, Weidong Ma, Qiwei Ye and Tie-Yan Liu, LightGBM, a highly efficient gradient boosting decision tree, Advances in Neural Information Processing Systems 30, 2017"
    locator: histogram-based split finding, gradient-based one-side sampling and exclusive feature bundling
  - paper: "Liudmila Prokhorenkova, Gleb Gusev, Aleksandr Vorobev, Anna Veronika Dorogush and Andrey Gulin, CatBoost, unbiased boosting with categorical features, Advances in Neural Information Processing Systems 31, 2018"
    locator: ordered boosting and ordered target statistics for categorical features
---

XGBoost is a system for [gradient tree boosting](/gradient-boosting/) by Chen and Guestrin (2016). In each round it fits a regression tree to the first and second derivatives $g_i$ and $h_i$ of the loss at the current predictions, so each tree is a Newton step, not only a gradient step. It adds a penalty $\gamma$ for each leaf and $\frac12 \lambda w^2$ for each leaf weight $w$. Then the best weight of a leaf is $w^* = -G/(H + \lambda)$, and a split is worth making when its gain, a closed form in the sums $G$ and $H$ of the two children, is positive. The system adds a split finder that learns a default direction for missing values, a weighted quantile sketch for large data, and a column layout for fast scans.

## In plain words

XGBoost builds trees one after another, like gradient boosting. For each example it looks at two numbers: how fast the loss changes when the prediction moves, and how fast that rate itself changes. With both numbers, it can say exactly how much each split of the data would help, and exactly what value each leaf should hold. It charges a fixed price for each new leaf, and it pulls leaf values toward zero, so it only makes a split that pays for itself. When a value is missing, it learns from the training data which side of each split such examples should go to. For very large data it tries only a short list of good split points per feature.

## The problem

The input is a training set $(x_1, y_1), \ldots, (x_n, y_n)$ with $x_i \in \mathbb{R}^d$, where some entries may be missing, a loss $\ell(y, \hat y)$ that is convex and twice differentiable in $\hat y$, the number of trees $T$, a learning rate $\eta$, a depth limit $D$ and the penalties $\lambda \ge 0$ and $\gamma \ge 0$. The model is $\hat y(x) = \hat y_0 + \eta \sum_{t=1}^{T} f_t(x)$, where each $f_t$ is a tree with $J$ leaves and leaf weights $w_1, \ldots, w_J$. The regularized objective is

$$\mathcal L = \sum_{i=1}^{n} \ell(y_i, \hat y(x_i)) + \sum_{t=1}^{T} \Omega(f_t), \qquad \Omega(f) = \gamma J + \tfrac12 \lambda \sum_{j=1}^{J} w_j^2.$$

Round $t$ minimizes a second-order Taylor approximation of $\mathcal L$ in the new tree, with $g_i = \partial \ell / \partial \hat y$ and $h_i = \partial^2 \ell / \partial \hat y^2$ at the current prediction $\hat y_i$:

$$\tilde{\mathcal L}(f) = \sum_{i=1}^{n} \left(g_i f(x_i) + \tfrac12 h_i f(x_i)^2\right) + \Omega(f).$$

For squared loss, $g_i = \hat y_i - y_i$ and $h_i = 1$. For log loss with $y_i \in \{0, 1\}$ and $\hat y$ the log-odds, $g_i = p_i - y_i$ and $h_i = p_i (1 - p_i)$. For a leaf with example set $I_j$, write $G_j = \sum_{i \in I_j} g_i$ and $H_j = \sum_{i \in I_j} h_i$.

## The algorithm

```pseudo id=main
XGBOOST(S, ℓ, T, η, λ, γ, D)
L1  for t ← 1 to T do
L2      g_i ← ∂ℓ(y_i, ŷ)/∂ŷ and h_i ← ∂²ℓ(y_i, ŷ)/∂ŷ² at ŷ = ŷ_i, for i = 1 .. n
L3      grow a tree f_t from a root that holds all examples; for each node I of depth < D:
L4          (gain, split) ← EXACT-GREEDY-SPLIT(I); if there is no split with gain > 0, I is a leaf, else split I
L5      for each leaf j: w_j ← −G_j / (H_j + λ)
L6      ŷ_i ← ŷ_i + η f_t(x_i), for i = 1 .. n

EXACT-GREEDY-SPLIT(I)
L7  G ← Σ_{i ∈ I} g_i, H ← Σ_{i ∈ I} h_i, best ← none
L8  for each feature k do
L9      P ← the examples of I with x_ik present, sorted by x_ik; G_M, H_M ← the sums over I \ P (the missing ones)
L10     G_L ← 0, H_L ← 0
L11     for j ← 0 to |P|, skipping cuts between equal values, do      ▷ cut after the first j elements of P
L12         if j > 0 then G_L ← G_L + g_{P[j]}, H_L ← H_L + h_{P[j]}
L13         for each default direction of the missing values (right, left) do
L14             (G'_L, H'_L) ← (G_L, H_L) if right, (G_L + G_M, H_L + H_M) if left
L15             gain ← ½ [G'_L²/(H'_L + λ) + (G − G'_L)²/(H − H'_L + λ) − G²/(H + λ)] − γ
L16             if both sides are nonempty and gain > best then best ← (gain, k, cut j, direction)
L17 return best
```

The leaf weight of line L5 and the gain of line L15 come from the closed form of $\tilde{\mathcal L}$ for a fixed tree shape. The objective splits into one quadratic per leaf, $G_j w_j + \frac12 (H_j + \lambda) w_j^2$, whose minimum is at $w_j^* = -G_j/(H_j + \lambda)$ with value $-G_j^2 / (2(H_j + \lambda))$. So the best objective of a tree shape is $-\frac12 \sum_j G_j^2/(H_j + \lambda) + \gamma J$, and splitting a leaf into two reduces it by

$$\mathcal L_{\text{split}} = \frac12\left(\frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - \frac{(G_L + G_R)^2}{H_L + H_R + \lambda}\right) - \gamma.$$

Lines L9 to L16 are the sparsity-aware form of the exact greedy algorithm: they scan only the present values of each feature, and they try the missing examples on each side. The direction of larger gain becomes the default direction of the node, and a prediction sends a missing value there. The code also stops a split when a child has $H$ below a minimum (the parameter min_child_weight), which keeps the denominators away from $\lambda$ alone.

### Approximate split finding and the weighted quantile sketch

The exact finder sorts every feature at every node, which is too slow when the data does not fit in memory or is spread over machines. The approximate algorithm first proposes a few candidate cut points $s_{k1} < s_{k2} < \ldots$ for each feature $k$, then puts each example into a bucket between two candidates, sums $g$ and $h$ per bucket, and scans only the buckets. The candidates are weighted quantiles with weight $h_i$. With the rank function

$$r_k(z) = \frac{1}{\sum_{i} h_i} \sum_{i : x_{ik} < z} h_i,$$

the candidates are chosen so that $|r_k(s_{k,j}) - r_k(s_{k,j+1})| < \epsilon$, which gives about $1/\epsilon$ candidates. The weights are $h_i$ because $\tilde{\mathcal L}$ equals $\sum_i \frac12 h_i (f(x_i) + g_i/h_i)^2 + \Omega(f)$ plus a constant: it is a weighted squared loss with weight $h_i$. Chen and Guestrin give a mergeable and prunable summary for weighted data with a proven error, which extends the unweighted [quantile summaries](/quantile-summary-problem/) of Greenwald and Khanna. Candidates can be proposed once per tree (global) or again after each split (local). The code of this page implements only the exact finder.

## Example

Take one node with six examples and one feature, squared loss, current prediction $\hat y_i = 0$, $\lambda = 1$ and $\gamma = 0$. Then $g_i = -y_i$ and $h_i = 1$.

| example | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $x$ | 1 | 2 | missing | 3 | 4 | missing |
| $y$ | $-3$ | $-1$ | 4 | 1 | 3 | 2 |
| $g$ | 3 | 1 | $-4$ | $-1$ | $-3$ | $-2$ |

The node has $G = -6$ and $H = 6$, so as a leaf it has weight $w^* = 6/7$ and $G^2/(H + \lambda) = 36/7 \approx 5.1429$. The finder tries each cut of the present values $1, 2, 3, 4$ with the missing examples 3 and 6 on each side:

| left side | missing go | $G_L$, $H_L$ | $G_R$, $H_R$ | gain |
|---|---|---|---|---|
| none of the present | left | $-6$, 2 | 0, 4 | 3.4286 |
| $x \le 1.5$ | right | 3, 1 | $-9$, 5 | 6.4286 |
| $x \le 1.5$ | left | $-3$, 3 | $-3$, 3 | $-0.3214$ |
| $x \le 2.5$ | right | 4, 2 | $-10$, 4 | **10.0952** |
| $x \le 2.5$ | left | $-2$, 4 | $-4$, 2 | 0.4952 |
| $x \le 3.5$ | right | 3, 3 | $-9$, 3 | 8.6786 |
| $x \le 3.5$ | left | $-3$, 5 | $-3$, 1 | 0.4286 |

The best split is $x \le 2.5$ with the missing values going right. Its gain is $\frac12(16/3 + 100/5 - 36/7) \approx 10.0952$. The leaf weights are $-4/3$ on the left, for targets $-3$ and $-1$, and $10/5 = 2$ on the right, for targets $4, 1, 3, 2$. Both are the leaf means shrunk toward 0 by $\lambda$. The row with gain $-0.3214$ shows that with $\lambda > 0$ a split can raise the objective even with $\gamma = 0$. With $\gamma > 10.0952$, no split has a positive gain and the node stays a leaf.

## Correctness

XGBoost, like [gradient boosting](/gradient-boosting/), is a greedy heuristic with no guarantee to find the best sum of $T$ trees. These steps are exact, and are proved below:

- For a fixed tree shape, $w_j^* = -G_j/(H_j + \lambda)$ is the unique minimizer of $\tilde{\mathcal L}$ when $H_j + \lambda > 0$, and the minimum is $-\frac12 \sum_j G_j^2/(H_j + \lambda) + \gamma J$.
- The split gain $\mathcal L_{\text{split}}$ equals the decrease of this minimum when one leaf is split in two.
- EXACT-GREEDY-SPLIT returns a threshold split with a default direction of largest gain at the node, by a scan with prefix sums.
- For squared loss the second-order objective is exact, so with $\lambda = 0$ the leaf weight is the mean residual of [gradient boosting](/gradient-boosting/).

The tests compare the leaf weight and the gain with a direct numerical minimization of the regularized second-order objective, for each partition of small random nodes with missing values.

## Complexity

Let $z$ be the number of present entries of the data matrix. In the code, each node sorts the present values of each feature, so a level of the tree costs $O(z \log n)$ and a tree of depth $D$ costs $O(D z \log n)$. The total for $T$ trees is $O(T D z \log n)$ in the worst case, and the gradients cost $O(n)$ per round. Chen and Guestrin store the data in column blocks sorted once, in $O(z \log n)$ time; then each level is a linear scan, and the total is $O(T D z + z \log n)$. The approximate algorithm with $b$ buckets per feature scans buckets, not examples, after one pass to fill them. Memory is $\Theta(z)$ for the data, $\Theta(n)$ for $g$, $h$ and the predictions, and $\Theta(T 2^D)$ for the trees.

## Properties

- **A Newton step per tree.** The leaf weight is one Newton step on the leaf loss, with $\lambda$ added to the curvature. The split choice also uses the curvature, where gradient boosting fits the gradient by least squares.
- **Regularized.** $\gamma$ prunes splits during growth. The paper also prunes after growth: it grows to the depth limit and then removes splits with negative gain from the bottom up. $\lambda$ shrinks the weights of leaves with small $H$.
- **Sparsity-aware.** The cost of a scan is linear in the present entries, not in $n d$. One-hot encoded and sparse data become cheap.
- **Shrinkage and column subsampling.** The learning rate $\eta$ shrinks each tree, as $\nu$ does in gradient boosting. Column subsampling, as in a [random forest](/random-forest/), draws a subset of the features for each tree or each level.
- **Deterministic.** Without subsampling, the exact algorithm is a function of the data and the tie rule.

## Variants and improvements

- **LightGBM** (Ke et al. 2017) bins features into histograms, grows the leaf of largest gain first instead of level by level, samples the examples with small gradients less often (GOSS), and bundles features that are rarely nonzero together.
- **CatBoost** (Prokhorenkova et al. 2018) computes the residuals of each example with a model that did not see that example (ordered boosting), to remove a bias that appears when the same data gives the gradients and the fit, and encodes categorical features with ordered target statistics.
- **Histogram method in XGBoost.** Later versions of XGBoost also offer a histogram-based tree method; its details are in the software documentation, not in the 2016 paper.

## When to use it

Use XGBoost or a similar library for tabular data with many examples, sparse or missing values, and a need for strong accuracy with tuned parameters. The second-order step matters most for losses whose curvature changes a lot, such as the log loss. For small data, plain [gradient boosting](/gradient-boosting/) or a [random forest](/random-forest/) gives similar results with fewer parameters.

## Pitfalls

- **Dropping $\lambda$ from the leaf weight.** Line L5 is $-G/(H + \lambda)$. With $-G/H$, a leaf with few examples and small $H$, as in a confident log loss leaf, gets a huge weight.
- **Treating a missing value as zero.** Line L9 must keep the missing examples apart. Filling them with 0 puts them among the present values, and the learned default direction is lost.
- **Taking the sketch weights as counts.** The candidate cuts of the approximate algorithm must be quantiles weighted by $h_i$. Equal-count quantiles put few candidates where the loss is most curved.
- **Setting $\gamma$ without the scale of the loss.** The gain is in units of the loss, and $H$ grows with $n$. A value of $\gamma$ that prunes well on one data size can prune nothing, or everything, on another.
- **Reading the gain as a measure of accuracy.** The gain is a decrease of a Taylor approximation. For log loss it is accurate only for small steps, which is one reason for a small $\eta$.

## Implementations

## History

Chen started XGBoost as a research project. Chen and Guestrin described the system, its regularized objective, the sparsity-aware split finder, the weighted quantile sketch and the cache-aware column blocks at KDD 2016. The Newton view of boosting goes back to LogitBoost of Friedman, Hastie and Tibshirani (2000), and the tree boosting it extends is Friedman's (2001). LightGBM (2017) and CatBoost (2018) followed with other ways to find splits and to handle categorical features.

## References
