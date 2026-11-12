---
tag: QJH6MQ
kind: algorithm
slug: gradient-boosting
name: Gradient boosting
aliases:
- gradient boosting machine
- GBM
- gradient tree boosting
- TreeBoost
- stochastic gradient boosting
area: machine-learning/supervised-learning
level: core
summary: "Boosting as gradient descent in function space. Each new tree fits the negative gradient of the loss at the current scores, and its leaf values come from a line search."
solves: [regression, classification]
model: real-ram
complexity:
  vars: {n: the number of training examples, d: the number of features, T: the number of trees, D: the depth of each tree}
  time: {worst: "O(T D d n log n)"}
  space: {extra: "Θ(n + T 2^D)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2001
  people: [Jerome H. Friedman]
  note: Friedman published gradient boosting in the Annals of Statistics in 2001, and added subsampling in 2002.
prereqs: [boosting, gradient-descent, decision-tree-learning, loss-function]
see_also: [adaboost, xgboost, cart, logistic-loss, newton-raphson-method, random-forest, early-stopping, regularization]
sources:
  - paper: doi:10.1214/aos/1013203451
    title: Jerome H. Friedman, Greedy function approximation, a gradient boosting machine, Annals of Statistics 29(5), 2001
    locator: Section 3 (Algorithm 1, Gradient_Boost), Section 4 (LS_Boost, TreeBoost and L2_TreeBoost with the Newton step for the leaves) and Section 5 (shrinkage)
  - paper: doi:10.1016/S0167-9473(01)00065-2
    title: Jerome H. Friedman, Stochastic gradient boosting, Computational Statistics and Data Analysis 38(4), 2002
    locator: the subsample without replacement in each round
  - paper: doi:10.1214/aos/1016218223
    title: Jerome Friedman, Trevor Hastie and Robert Tibshirani, Additive logistic regression, a statistical view of boosting, Annals of Statistics 28(2), 2000
    locator: forward stagewise additive modeling and LogitBoost with Newton steps
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 10.10 (Algorithm 10.3, gradient tree boosting, and Table 10.2 of the gradients) and Section 10.12 (shrinkage and subsampling)
  - paper: "Llew Mason, Jonathan Baxter, Peter Bartlett and Marcus Frean, Boosting algorithms as gradient descent, Advances in Neural Information Processing Systems 12, 2000"
    locator: the AnyBoost view of boosting as gradient descent in function space
  - paper: "Guolin Ke, Qi Meng, Thomas Finley, Taifeng Wang, Wei Chen, Weidong Ma, Qiwei Ye and Tie-Yan Liu, LightGBM, a highly efficient gradient boosting decision tree, Advances in Neural Information Processing Systems 30, 2017"
    locator: histogram-based split finding and leaf-wise growth
  - paper: "Liudmila Prokhorenkova, Gleb Gusev, Aleksandr Vorobev, Anna Veronika Dorogush and Andrey Gulin, CatBoost, unbiased boosting with categorical features, Advances in Neural Information Processing Systems 31, 2018"
    locator: ordered boosting and the prediction shift
---

Gradient boosting builds an additive model $F_T(x) = F_0 + \nu \sum_{t=1}^{T} f_t(x)$ by [gradient descent](/gradient-descent/) in the space of functions. In each round it computes the pseudo-residuals, the negative gradient of the loss at the current scores of the training examples, and fits a small regression tree to them. Then it picks the value of each leaf by a line search on the true loss, and adds the tree times a shrinkage factor $\nu$. Friedman (2001) gave the method for any differentiable [loss](/loss-function/). With squared loss it fits residuals, with the exponential loss it is close to [AdaBoost](/adaboost/), and with the log loss it gives a boosted form of [logistic regression](/logistic-regression/).

## In plain words

Start with a guess that is the same number for every example, such as the average target. Now look at how wrong the guess is on each example. A small tree learns to predict these errors from the inputs. Add a small part of that tree to the guess, so that the guess moves toward the right answers. Then measure the errors again and train the next tree on them. Each tree fixes a bit of what the trees before it got wrong. For other kinds of loss, "the error" means the direction in which the loss falls fastest for each example. Taking only a small part of each tree is slower, but it usually gives a model that does better on new data.

## The problem

The input is a training set $(x_1, y_1), \ldots, (x_n, y_n)$ with $x_i \in \mathbb{R}^d$, a loss $\ell(y, F)$ that is differentiable in the score $F$, a number of rounds $T$, a tree depth $D$, a shrinkage factor $0 < \nu \le 1$ and a subsample fraction $0 < f \le 1$. The goal is a function $F$ with a small mean loss $L(F) = \frac1n \sum_i \ell(y_i, F(x_i))$ on the training set, and, when the examples are drawn i.i.d. from an unknown distribution $D$, a small expected loss on new data. This page uses two losses:

| loss | $\ell(y, F)$ | pseudo-residual $r = -\partial \ell / \partial F$ | leaf value |
|---|---|---|---|
| squared, $y \in \mathbb{R}$ | $\frac12 (y - F)^2$ | $y - F$ | mean of $r$ in the leaf (exact) |
| log loss, $y \in \{0, 1\}$ | $\log(1 + e^{F}) - yF$ | $y - p$, with $p = 1/(1 + e^{-F})$ | $\sum r / \sum p(1 - p)$ (one Newton step) |

With log loss the score $F$ is the log-odds. Friedman writes the same loss with $y \in \{-1, +1\}$ and $F$ equal to half the log-odds; his leaf value $\sum \tilde y_i / \sum |\tilde y_i|(2 - |\tilde y_i|)$ is the same Newton step in that scale.

## The algorithm

```pseudo id=main
GRADIENT-TREE-BOOST(S, ℓ, T, D, ν, f, rng)
L1  F_0 ← argmin_c Σ_i ℓ(y_i, c)
L2  for t ← 1 to T do
L3      r_i ← −∂ℓ(y_i, F)/∂F at F = F_{t−1}(x_i), for i = 1 .. n
L4      I_t ← all indices if f = 1, else ⌊f n⌋ indices drawn without replacement by rng
L5      fit a least squares tree of depth at most D to the pairs (x_i, r_i), i ∈ I_t; its leaves are R_1 .. R_J
L6      for j ← 1 to J do v_j ← argmin_v Σ_{i ∈ R_j} ℓ(y_i, F_{t−1}(x_i) + v)      ▷ exact, or one Newton step
L7      F_t(x) ← F_{t−1}(x) + ν · v_j, where R_j is the leaf of x
L8  return F_T
```

Line L1 is the best constant: $\bar y$ for squared loss, $\ln(\bar y/(1 - \bar y))$ for log loss. Line L3 is the gradient step: the vector $(r_1, \ldots, r_n)$ is the direction of steepest descent of $L$ over the $n$ training scores. A free vector does not give a function on new inputs, so line L5 projects it onto the trees by a least squares fit, as in [CART](/cart/) regression. Friedman's general Algorithm 1 then does one line search for a single step $\rho_t$. For trees he does better (TreeBoost): line L6 does a separate line search in each leaf, because a tree is a sum of $J$ indicator functions. Line L7 takes only the fraction $\nu$ of the step. This shrinkage is a form of [regularization](/regularization/). Line L4 is stochastic gradient boosting (Friedman 2002): each tree sees a random part of the data, often about half.

## Example

Squared loss, $\nu = 0.5$, trees of depth 1 (stumps), on six points:

| $x$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $y$ | 1 | 3 | 2 | 6 | 8 | 4 |

$F_0 = \bar y = 4$, and the mean loss is $17/6 \approx 2.8333$. Each row gives the residuals before the round, the stump fitted to them, and the mean loss after the round.

| round | residuals $r$ | split | leaf values | mean loss after |
|---|---|---|---|---|
| 1 | $-3, -1, -2, 2, 4, 0$ | $x \le 3.5$ | $-2$, $2$ | 1.3333 |
| 2 | $-2, 0, -1, 1, 3, -1$ | $x \le 3.5$ | $-1$, $1$ | 0.9583 |
| 3 | $-1.5, 0.5, -0.5, 0.5, 2.5, -1.5$ | $x \le 1.5$ | $-1.5$, $0.3$ | 0.7896 |

Round 1 fits the residuals $y_i - 4$. The best stump puts $x \le 3.5$ on the left, with mean residual $-2$, and the rest on the right, with mean $2$. Half of it moves the scores to $3$ and $5$. In round 2 the same split is still best. In round 3 the largest left part of the error is the point $x = 1$, so the split moves. After three rounds the scores are $1.75, 2.65, 2.65, 5.65, 5.65, 5.65$. The loss falls in each round, as it must for squared loss with $\nu \le 2$.

## Correctness

Gradient boosting is a greedy heuristic: it has no guarantee to reach the minimum training loss over sums of $T$ trees, and its error on new data depends on $T$, $\nu$ and $D$. These facts do hold, and are proved below.

- **The pseudo-residuals are the negative gradient.** For squared loss they are the residuals $y_i - F_{t-1}(x_i)$, so the first tree fits $y_i - \bar y$.
- **The leaf values are the line search.** For squared loss the mean residual of the leaf is the exact minimizer of the loss in the leaf. For log loss, $v_j = G_j / H_j$ with $G_j = \sum_{i \in R_j} r_i$ and $H_j = \sum_{i \in R_j} p_i(1 - p_i)$ minimizes the second-order Taylor expansion of the leaf loss, so it is one Newton step.
- **Squared loss never increases.** Without subsampling, the loss of leaf $R_j$ changes by $-\nu(1 - \nu/2) |R_j| v_j^2 \le 0$ for $0 < \nu \le 2$.
- **Log loss decreases for small steps.** Since $p(1 - p) \le \frac14$, a step $\nu \le 8H_j/|R_j|$ does not increase the loss of leaf $R_j$. No fixed $\nu$ is safe for all data, because $H_j/|R_j|$ is small in confident leaves.
- **Exact fit.** With distinct inputs, no depth limit and $\nu = 1$, the first tree with squared loss reaches zero training loss.

## Complexity

Count operations in $n$, $d$, $T$ and $D$. Lines L3 and L7 take $O(n)$ time per round, plus $O(D)$ per example to find its leaf. In line L5, a node with $m$ examples sorts them by each feature and sweeps the sorted order, keeping running sums of the residuals; this costs $O(d m \log m)$. The nodes at one depth hold at most $n$ examples in total, so one tree costs $O(D d n \log n)$. Line L6 costs $O(n)$. The total is $O(T D d n \log n)$ in the worst case. Presorting each feature once removes the log factor from each level, and histogram methods with $b$ bins cost $O(d n)$ per level to fill plus $O(d b)$ per node to scan. The model stores $T$ trees with at most $2^D$ leaves each, and the scores take $\Theta(n)$ memory. A prediction costs $O(T D)$.

## Properties

- **Any differentiable loss.** Only line L3 and line L6 depend on the loss. The absolute loss gives LAD regression (the leaf value is the median residual), the Huber loss gives a robust regression, and the multiclass log loss fits $k$ trees per round, one per class.
- **Shrinkage and the number of trees.** A smaller $\nu$ needs a larger $T$ for the same training loss. Friedman (2001) observed that small values such as $\nu \le 0.1$ gave lower test error in his experiments; this is an observation, not a theorem.
- **Subsampling.** With $f < 1$ the method is random, and each round costs less. Friedman (2002) observed better accuracy with subsampling on his test problems, and Hastie, Tibshirani and Friedman give $f = \frac12$ as a typical value. The proof of the monotone decrease of the squared loss does not apply, since the leaf values come from the subsample only.
- **Deterministic when $f = 1$.** With a fixed rule for ties between splits, as in the code, the output is a function of the data.
- **Sequential.** Round $t$ needs $F_{t-1}$, so the rounds do not run in parallel. The work inside one tree, over features and over examples, does.

## Variants and improvements

- **[XGBoost](/xgboost/).** Uses the second derivatives in the tree growth itself, not only in the leaf values, and adds penalties $\gamma$ per leaf and $\lambda$ on the squared leaf values.
- **Histogram-based boosting.** LightGBM (Ke et al. 2017) bins each feature and grows trees leaf by leaf. CatBoost (Prokhorenkova et al. 2018) uses ordered boosting to avoid a bias from using the same examples for the residuals and the fit.
- **[AdaBoost](/adaboost/).** Gradient boosting with the exponential loss and trees that return $\pm 1$ recovers the AdaBoost weights: the pseudo-residual of example $i$ is $y_i \exp(-y_i F(x_i))$.
- **Early stopping.** Stop when the loss on held-out data stops falling; see [early stopping](/early-stopping/).
- **Random forest as a contrast.** A [random forest](/random-forest/) grows deep trees independently and averages them, to reduce variance. Gradient boosting grows shallow trees in sequence, to reduce bias.

## When to use it

Use gradient boosting of trees for tabular data with mixed feature types, when you can tune $T$, $\nu$ and $D$ on held-out data. It handles regression, classification and ranking with one method. Prefer a [random forest](/random-forest/) when you want good results with almost no tuning, or when the rounds must run in parallel. For large data, use a histogram method such as XGBoost or LightGBM rather than the exact sort of this page.

## Pitfalls

- **Fitting the targets instead of the residuals.** Line L5 fits $r_i$, not $y_i$. Fitting $y_i$ in each round adds the same tree again and again.
- **Using the tree's least squares values for log loss.** For log loss the tree is grown on $r_i = y_i - p_i$, but line L6 must replace the leaf means by $G_j/H_j$. The mean of $r_i$ is a gradient step with no curvature, and it is far too small in confident leaves.
- **Forgetting the shrinkage in prediction.** The model is $F_0 + \nu \sum_t f_t$. A prediction without the factor $\nu$ is wrong by a large amount.
- **Choosing $T$ on the training loss.** The training loss falls in every round for squared loss, so it never says when to stop. Choose $T$ on held-out data or by [cross-validation](/cross-validation/).
- **Starting from $F_0 = 0$ with log loss on unbalanced classes.** It is not wrong, but the first trees then only learn the base rate. Line L1 starts from the log-odds of the base rate.

## Implementations

## History

Friedman, Hastie and Tibshirani (2000) read AdaBoost as stagewise fitting of an additive model with the exponential loss. Friedman's paper "Greedy function approximation: a gradient boosting machine" (2001) turned this into a method for any differentiable loss, with TreeBoost, the per-leaf line search and shrinkage. Mason, Baxter, Bartlett and Frean gave the same functional gradient view (AnyBoost) at NIPS 1999. Friedman added random subsampling in "Stochastic gradient boosting" (2002).

## References
