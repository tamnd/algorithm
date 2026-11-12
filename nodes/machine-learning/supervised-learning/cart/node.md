---
tag: 6A3KDC
kind: algorithm
slug: cart
name: CART
aliases:
- classification and regression trees
- CART decision tree
- Breiman-Friedman-Olshen-Stone trees
area: machine-learning/supervised-learning
level: core
summary: "Breiman et al. 1984: grow a large binary tree by Gini or squared-error decrease, with surrogate splits, then prune it by cost-complexity with alpha chosen by cross-validation."
solves: [decision-tree-learning]
model: real-ram
complexity:
  vars: {n: the number of training cases, d: the number of features}
  time: {worst: O(d n^2 log n)}
  space: {extra: O(d n)}
properties: {deterministic: true, exact: false, online: false, recursive: true}
history:
  year: 1984
  people: [Leo Breiman, Jerome H. Friedman, Richard A. Olshen, Charles J. Stone]
  note: "The monograph Classification and Regression Trees (Wadsworth, 1984) gave binary tree growing, surrogate splits and minimal cost-complexity pruning with cross-validation."
prereqs: [decision-tree-learning, gini-impurity, cost-complexity-pruning]
see_also: [c4-5, id3, decision-tree, decision-stump, mean-squared-error, cross-validation, random-forest, gradient-boosting]
sources:
  - book: isbn:9780412048418
    title: L. Breiman, J. H. Friedman, R. A. Olshen and C. J. Stone, Classification and Regression Trees, Wadsworth 1984, reprinted by Chapman and Hall/CRC
    locator: Chapter 2 (growing a classification tree), Chapter 3 (minimal cost-complexity pruning, the weakest-link sequence, cross-validation and the 1-SE rule), Chapter 4 (splitting rules, the Gini index and twoing), Chapter 5 (surrogate splits, missing values, linear combination splits) and Chapter 8 (regression trees)
  - book: isbn:9780387848570
    title: T. Hastie, R. Tibshirani and J. Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 9.2 (tree-based methods; 9.2.2 regression trees and cost-complexity pruning, 9.2.3 classification trees and the Gini index, 9.2.4 categorical predictors, missing values and surrogate splits)
  - paper: doi:10.1016/0020-0190(76)90095-8
    title: L. Hyafil and R. L. Rivest, Constructing optimal binary decision trees is NP-complete, Information Processing Letters 5(1), 1976
    locator: pages 15 to 17; the hardness that makes greedy growth the standard
---

CART, for classification and regression trees, is the tree learner of the 1984 book by Leo Breiman, Jerome Friedman, Richard Olshen and Charles Stone. It grows a binary [decision tree](/decision-tree/) top-down, choosing at each node the split $x_j \le \theta$ that most decreases the [Gini impurity](/gini-impurity/) (classification) or the sum of squared errors (regression). It stores *surrogate splits* to route cases with missing values. It grows the tree large on purpose and then prunes it by [cost-complexity pruning](/cost-complexity-pruning/), choosing the size by [cross-validation](/cross-validation/).

## In plain words

CART asks only yes-or-no questions, such as "is the income at most 40,000?". At each node it tries every feature and every cut point, and keeps the question whose two answer groups are the most uniform: the most of one class, or numbers closest to their average.

It does not try to stop at the right moment. It grows the tree until the leaves are pure or tiny, which overfits, and then cuts it back. Cutting back trades errors against leaves: each leaf costs a price $\alpha$. As $\alpha$ grows, the best tree shrinks in a fixed nested order. CART picks the $\alpha$ that predicts best on held-out parts of the data.

For a case with a missing value at a node, CART asks a backup question on another feature that splits the cases almost the same way.

## The problem

The input is $n$ training cases $(x, y)$ with $x \in \mathbb{R}^d$, where a value may be missing, and $y$ a class (classification) or a real number (regression). The output is a binary tree whose internal nodes test $x_j \le \theta$ and whose leaves predict a class or a constant. The goal is a small expected loss on new cases: 0-1 loss or [mean squared error](/mean-squared-error/). CART is a heuristic: finding even an optimal tree for the training data is NP-hard (Hyafil and Rivest 1976).

## The algorithm

For a node $t$ with $N(t)$ cases, let $I(t) = N(t)\, i(t)$, where $i(t)$ is the Gini impurity $1 - \sum_k p_k^2$ of the classes at $t$, or the mean squared deviation of the $y$ at $t$ (so $I(t)$ is the sum of squared errors). A split $s$ sends $t$ to children $t_L$ and $t_R$, and its decrease is $\Delta I(s, t) = I(t) - I(t_L) - I(t_R) \ge 0$. As a leaf, $t$ predicts the majority class or the mean, and $R(t)$ is its resubstitution risk: the number of misclassified cases, or the sum of squared errors.

```pseudo id=main
CART(S)
L1  GROW(t): if t is pure, or N(t) < n_min, then t is a leaf
L2  for each feature j: s_j ← the cut x_j ≤ θ of largest ΔI on the cases with x_j known, θ a midpoint
L3  s* ← the s_j of largest decrease; if there is none, t is a leaf
L4  surrogates(t) ← for each other feature, the split that agrees most with s*, kept if its λ > 0, best first
L5  send each case by s*, or by its first surrogate with a known value, or to the larger side
L6  GROW(t_L); GROW(t_R)
L7  T_1 ← T_max with every node t collapsed where R(t) = R(T_t), bottom-up
L8  repeat: g(t) ← (R(t) − R(T_t)) / (|leaves(T_t)| − 1) for each internal t; α ← min g(t)
L9      collapse every t with g(t) = α; record (α_k, T_k)  until only the root is left
L10 choose T_k by V-fold cross-validation at α'_k = sqrt(α_k α_{k+1}), and return it
```

**Surrogates.** For the primary split $s^*$ at $t$ and another feature $j$, the surrogate on $j$ is the split $\tilde s$ on $x_j$, in either direction, that sends the most cases to the same side as $s^*$. With $p_L$ and $p_R$ the fractions that $s^*$ sends left and right, and agreement $a$, the *predictive measure of association* is $\lambda = (\min(p_L, p_R) - (1 - a)) / \min(p_L, p_R)$. It compares $\tilde s$ with the trivial rule "send every case to the larger side", whose error is $\min(p_L, p_R)$. Only surrogates with $\lambda > 0$ beat that rule.

**Pruning.** Lines L7 to L9 are the weakest-link algorithm of [cost-complexity pruning](/cost-complexity-pruning/). For $\alpha \in [\alpha_k, \alpha_{k+1})$, $T_k$ is the smallest subtree of $T_{\max}$ that minimizes $R_\alpha(T) = R(T) + \alpha |\text{leaves}(T)|$, and $T_1 \supset T_2 \supset \cdots \supset \{\text{root}\}$. That page proves this.

**Cross-validation.** Split the data into $V$ folds (Breiman et al. use $V = 10$). For each fold, grow and prune a tree on the other folds, and for each $k$ measure the loss of its subtree for $\alpha'_k$ on the held-out fold. Sum over the folds and pick the $k$ of least loss. The *1-SE rule* of the book picks instead the smallest $T_k$ whose cross-validated loss is within one standard error of the least; this implementation uses the plain minimum.

## Example

Regression on the six points $x = 1, \dots, 6$ with $y = 1, 3, 2, 8, 9, 15$. The root has mean $19/3$ and $R = 430/3 \approx 143.3$. The cuts at the root:

| cut | SSE left | SSE right | decrease |
|---|---|---|---|
| $x \le 1.5$ | 0 | 109.2 | 34.1 |
| $x \le 2.5$ | 2 | 85 | 56.3 |
| $x \le 3.5$ | 2 | 28.7 | **112.7** |
| $x \le 4.5$ | 29 | 18 | 96.3 |
| $x \le 5.5$ | 53.2 | 0 | 90.1 |

CART splits at $x \le 3.5$. Growing on to pure leaves gives $T_{\max}$ with 6 leaves: the left child $\{1, 3, 2\}$ splits at 1.5 and then 2.5, and the right child $\{8, 9, 15\}$ splits at 5.5 and then 4.5. The pruning sequence is:

| $k$ | $\alpha_k$ | collapsed at this step | leaves | $R(T_k)$ |
|---|---|---|---|---|
| 1 | 0 | nothing | 6 | 0 |
| 2 | 1/2 | $\{3, 2\}$ and $\{8, 9\}$, a tie, together | 4 | 1 |
| 3 | 3/2 | $\{1, 3, 2\}$ | 3 | 5/2 |
| 4 | 169/6 ≈ 28.2 | $\{8, 9, 15\}$ | 2 | 92/3 ≈ 30.7 |
| 5 | 338/3 ≈ 112.7 | the root | 1 | 430/3 ≈ 143.3 |

For example $g$ at the node $\{8, 9, 15\}$ in $T_3$ is $(86/3 - 1/2)/(2 - 1) = 169/6$: collapsing it costs 169/6 in squared error and saves one leaf. Cross-validation then picks one of these five trees.

## Correctness

CART is a heuristic for the tree it grows, but parts of it are exact.

- **Split search.** Line L2 finds the best cut on each feature exactly. Between two adjacent distinct values of $x_j$, every threshold induces the same partition, so the midpoints of adjacent distinct values cover all partitions by a cut on $x_j$. The tests compare the grown tree with a builder that tries every feature and every midpoint from the definitions.
- **Decrease is nonnegative.** Gini impurity and the variance are concave in the class proportions or the distribution, so $\Delta I \ge 0$ for every split; the [Gini impurity](/gini-impurity/) page proves it.
- **Termination.** Every split leaves at least one case on each side, so each child has fewer cases and the tree has at most $n$ leaves.
- **Pruning.** For each $\alpha$, the tree $T_k$ with $\alpha_k \le \alpha < \alpha_{k+1}$ is the smallest subtree minimizing $R_\alpha$, and it is contained in every minimizer (Breiman et al., Chapter 3). The proof is on the [cost-complexity pruning](/cost-complexity-pruning/) page, and the tests check it against all prunings of small trees.

The full proofs are below.

## Complexity

Costs are on the [real RAM](/real-ram/), for a bounded number of classes.

- **One node** with $n_t$ cases: sorting each feature costs $O(d\, n_t \log n_t)$, and the scan with running counts or sums costs $O(d\, n_t)$. Surrogates cost another $O(d\, n_t \log n_t)$.
- **One level** holds at most $n$ cases, so it costs $O(d\, n \log n)$. Presorting each feature once, and keeping the order in the children, removes the log factor after the first $O(d\, n \log n)$.
- **Depth.** A split may peel off a single case, so the depth can reach $n - 1$, and growth costs $O(d\, n^2 \log n)$ in the worst case. For balanced trees it is $O(d\, n \log^2 n)$.
- **Pruning.** This implementation recomputes $g(t)$ for all nodes at each step, so the sequence costs $O(|T|^2)$ for a tree of $|T| \le 2n$ nodes; one bottom-up pass per step suffices.
- **Cross-validation** repeats growing and pruning $V$ more times.
- **Space.** The data take $O(d n)$, the tree has at most $2n - 1$ nodes, and each node keeps at most $d - 1$ surrogates.

## Properties

- **Binary splits only.** A categorical feature with $L$ values is split into two subsets of values. For two classes or regression, sorting the values by the class proportion or the mean and cutting that order finds the best of the $2^{L-1} - 1$ subsets (ESL, Section 9.2.4).
- **Invariant to monotone transforms** of each feature: only the order of the values matters.
- **Handles missing values** by surrogates, at training and prediction time, without imputation.
- **High variance.** A small change in the data can change the top split and the whole tree. This is the weakness that [bagging](/bagging/) and [random forests](/random-forest/) exploit.
- **Deterministic**, with fixed tie rules; cross-validation uses a seeded fold assignment.

## Variants and improvements

- **Other splitting rules.** The book also gives the twoing rule and allows priors and unequal misclassification costs. Entropy works about as well as Gini (see [information gain](/information-gain/)).
- **Linear combination splits.** The book searches splits $\sum_j a_j x_j \le c$ by a local search. Such oblique trees can be much smaller.
- **Regression trees** with absolute deviation (least absolute deviation trees) and median leaves.
- **Ensembles.** [Bagging](/bagging/), [random forests](/random-forest/) and [gradient boosting](/gradient-boosting/) use CART-style trees as base learners; boosting often uses very small trees, down to [decision stumps](/decision-stump/).
- **rpart** in R and the tree module of scikit-learn implement CART; scikit-learn has cost-complexity pruning but no surrogate splits.

## When to use it

Use CART when you need one readable model, mixed or unscaled features, missing values, or a fast baseline. Use it for regression as well as classification. When accuracy matters more than one readable tree, use it as the base learner of an ensemble instead. For categorical data with many-way splits and no held-out data for pruning, [C4.5](/c4-5/) is the classical alternative.

## Pitfalls

- **Stopping early instead of pruning.** A rule like "stop when the best decrease is small" can stop before a split whose children split well, as in XOR. Grow large and prune.
- **Thresholds at data values.** A cut at a data value, not a midpoint, gives the same training partition but biases predictions for new values between the two.
- **Too many candidate cuts.** A feature with many distinct values gets many chances to fit noise, so the greedy choice favors it. Pruning reduces, but does not remove, this bias.
- **The pruning risk is not the growing criterion.** Classification trees grow by Gini but prune by the misclassification count $R(t)$. Mixing the two up changes the sequence.
- **Cross-validation noise.** The cross-validated loss is often flat near its minimum; the 1-SE rule gives smaller trees with little loss of accuracy.

## Implementations

## History

Morgan and Sonquist's AID program of 1963 grew regression trees by greedy binary splits and stopped by a threshold, and later work found such stopping rules unreliable. Breiman, Friedman, Olshen and Stone worked on tree methods from the 1970s, and their 1984 monograph replaced stopping rules by growing a large tree and pruning it with cost-complexity and cross-validation. It also introduced surrogate splits and gave consistency results for tree estimates. Commercial CART software by Salford Systems followed. CART trees became the base learners of bagging (Breiman 1996), random forests (Breiman 2001) and gradient boosting (Friedman 2001).

## References
