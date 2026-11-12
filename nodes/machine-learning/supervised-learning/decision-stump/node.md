---
tag: H1E126
kind: model
slug: decision-stump
name: Decision stump
aliases:
- one-level decision tree
- one-rule classifier
area: machine-learning/supervised-learning
level: intro
summary: "A decision tree of depth one: one test x_j <= θ and two leaves. Exact weighted ERM over stumps takes O(d n log n) time; stumps are the classic AdaBoost weak learner."
prereqs: [decision-tree, empirical-risk-minimization]
see_also: [adaboost, boosting, decision-tree-learning, gini-impurity, vc-dimension, weak-learnability-equivalence, gradient-boosting, prefix-sums]
sources:
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, From Theory to Algorithms, Cambridge University Press, 2014
    locator: Chapter 10, Section 10.1.1 (an efficient implementation of ERM for decision stumps by sorting and one scan) and Chapter 6 (VC dimension)
  - paper: "Wayne Iba and Pat Langley, Induction of one-level decision trees, Proceedings of the Ninth International Conference on Machine Learning (ML92), Morgan Kaufmann, 1992"
    locator: pages 233 to 240 (one-level trees, their learning and their accuracy)
  - paper: doi:10.1023/A:1022631118932
    title: Robert C. Holte, Very simple classification rules perform well on most commonly used datasets, Machine Learning 11(1), 1993
    locator: pages 63 to 90 (the 1R learner of one-attribute rules)
  - book: isbn:9780262017183
    title: Robert E. Schapire and Yoav Freund, Boosting, Foundations and Algorithms, MIT Press, 2012
    locator: Chapter 1 (AdaBoost with decision stumps as base classifiers) and Chapter 3 (the training error bound)
---

A decision stump is a [decision tree](/decision-tree/) of depth one: a single test $x_j \le \theta$ on one feature, with one leaf for each outcome. Its hypothesis class is tiny, so it underfits most tasks on its own, but [empirical risk minimization](/empirical-risk-minimization/) over it is exact and fast: with weighted examples, one sort per feature and one prefix scan find a stump of least weighted error in $O(d n \log n)$ time. This makes stumps the classic weak learner of [AdaBoost](/adaboost/) and a common base learner of [gradient boosting](/gradient-boosting/).

## The machine

**Notation.** $n$ is the number of training examples, $d$ the number of features, $x_i \in \mathbb{R}^d$ and $y_i$ the $i$-th example and its label, $k$ the number of classes, and $w_i \ge 0$ the weight of example $i$, with $W = \sum_i w_i$.

**The hypothesis.** A stump is a tuple $(j, \theta, a, b)$ with a feature $j \in \{1, \ldots, d\}$, a threshold $\theta \in \mathbb{R}$ and two leaf values $a, b$:

$$ h_{j, \theta, a, b}(x) = \begin{cases} a & \text{if } x_j \le \theta, \\ b & \text{if } x_j > \theta. \end{cases} $$

For classification $a, b$ are class labels; with labels $\pm 1$ and $a = -b$ this is the sign of $\pm(x_j - \theta)$. The constant classifiers are stumps too (take $a = b$, or $\theta$ below all data). For regression $a, b \in \mathbb{R}$. For a categorical feature the test is $x_j = v$ against $x_j \ne v$, or a multiway leaf for each value, which is the one-attribute rule 1R of Holte (1993).

**The learning task.** The data model is a fixed weighted sample $S = ((x_i, y_i, w_i))_{i=1}^n$, for example the reweighted sample of a boosting round. The learner returns a stump that minimizes the weighted training error

$$ \widehat{L}_w(h) = \sum_{i=1}^{n} w_i \, [\, h(x_i) \ne y_i \,], $$

or, for a regression stump, the weighted squared error $\sum_i w_i (h(x_i) - y_i)^2$. In the learning-theory reading, the examples are drawn i.i.d. from an unknown distribution $D$, and the setting is agnostic: no stump needs to have zero error.

## What it counts

- **Prediction.** One comparison of a feature with the threshold: $O(1)$ time on the [real RAM](/real-ram/).
- **Learning.** Comparisons for sorting, and additions of weights in the scan. The exact learner below takes $O(d n \log n)$ comparisons and $O(d n k)$ arithmetic operations, or $O(d n)$ for two classes. With the $d$ sort orders computed once and kept, as in boosting where the data do not change between rounds, each later call costs only $O(d n)$.
- **Memory.** $O(n + k)$ words besides the data.
- **Number of distinct behaviours.** On a sample of $n$ points, a feature has at most $n - 1$ cut positions between distinct values. With two classes, the stumps produce at most $2 + 2d(n - 1)$ distinct labelings of the sample: the 2 constant labelings, and for each feature and cut the two non-constant ones. This count drives the VC bound below.

## Relation to other models

- **Decision trees.** A stump is a decision tree with one internal node. A [decision tree learning](/decision-tree-learning/) algorithm such as [CART](/cart/) finds its root test with the same scan, using an impurity such as the [Gini impurity](/gini-impurity/) instead of the 0-1 error.
- **Halfspaces.** A stump with $a \ne b$ on labels $\pm 1$ is a halfspace $\text{sign}(\pm(x_j - \theta))$ whose normal vector is a coordinate axis. So stumps are a subclass of linear threshold functions, with a far smaller VC dimension when $d$ is large ($O(\log d)$ instead of $d + 1$).
- **Boosting.** [AdaBoost](/adaboost/) calls a stump learner on reweighted data in each round and outputs a weighted vote $\text{sign}(\sum_t \alpha_t h_t(x))$. Each $h_t$ depends on one feature, so the vote is an additive model: a sum of step functions, one sum per feature. Boosted stumps cannot model interactions between features; deeper trees can. [Gradient boosting](/gradient-boosting/) with regression stumps gives the same additive form.
- **One-attribute rules.** Holte's 1R chooses the single attribute whose rule (one leaf per value, or per interval of a numeric attribute) has the least training error. It is a multiway stump. Iba and Langley (1992) studied one-level trees in the same spirit.

## Known results in the model

**Exact weighted ERM in $O(d n \log n)$ time (Shalev-Shwartz and Ben-David, Section 10.1.1).** For each feature, sort the examples by that feature, and move them one at a time from the right side to the left side, keeping the weight of each class on each side.

```pseudo id=main
BEST-STUMP(X, y, w)                      ▷ least weighted 0-1 error over all stumps
L1  best ← the constant stump of the heaviest class, error W − max_c W_c
L2  for j ← 1 to d do
L3      π ← the indices 1..n sorted by x_{i,j}
L4      L_c ← 0 and R_c ← W_c for each class c       ▷ class weights left and right of the cut
L5      for t ← 1 to n − 1 do
L6          i ← π[t]; L_{y_i} ← L_{y_i} + w_i; R_{y_i} ← R_{y_i} − w_i
L7          if x_{i,j} < x_{π[t+1],j} then           ▷ a cut only between distinct values
L8              e ← (Σ L − max_c L_c) + (Σ R − max_c R_c)
L9              if e < best.error then best ← (e, j, θ = x_{i,j}, argmax L, argmax R)
L10 return best
```

*Why it is exact.* On the sample, a threshold $\theta$ on feature $j$ only matters through the set $\{i : x_{i,j} \le \theta\}$. These sets are prefixes of the sorted order that end between two distinct values (or are empty, which gives a constant stump), and line L7 visits each such prefix once, with the right class weights by the invariant "$L$ and $R$ hold the class weights of $\pi[1..t]$ and of the rest". For a fixed cut, the leaves are independent: the weighted error of a leaf that predicts $c$ is the weight of the other classes on its side, which is least for the heaviest class, so line L8 is the least error for that cut. Line L9 keeps the minimum over all cuts and features. The cost is $d$ sorts of $O(n \log n)$ and $d(n-1)$ updates of $O(k)$ each. The same scan with running sums $\sum w_i$, $\sum w_i y_i$ and $\sum w_i y_i^2$ on each side finds the least squared-error regression stump, with leaf values equal to the weighted means of the two sides.

**Example.** Six points in $\mathbb{R}^2$ with labels: $(1, 5){:}+$, $(2, 3){:}+$, $(3, 6){:}-$, $(4, 1){:}+$, $(5, 4){:}-$, $(6, 2){:}-$, all of weight 1. The scan on feature 1:

| cut after $x_1 =$ | left $(+, -)$ | right $(+, -)$ | error |
|---|---|---|---|
| 1 | (1, 0) | (2, 3) | 2 |
| 2 | (2, 0) | (1, 3) | 1 |
| 3 | (2, 1) | (1, 2) | 2 |
| 4 | (3, 1) | (0, 2) | 1 |
| 5 | (3, 2) | (0, 1) | 2 |

Feature 2 gives errors 2, 3, 2, 3, 2 at its five cuts. The constant stump has error 3. The first stump of least error is $x_1 \le 2 \Rightarrow +$, else $-$, with error 1 (the point $(4, 1)$). If the point $(4, 1)$ gets weight 0.4 and the others 0.1, the same scan returns $x_1 \le 4 \Rightarrow +$, else $-$, with error 0.1: reweighting moves the best stump, which is what boosting uses.

**VC dimension.** Let $H_d$ be the stumps on $\mathbb{R}^d$ with labels $\pm 1$.

- For $d = 1$, $VC(H_1) = 2$. Two points $u < v$ get all four labelings: the two constants, and the cut between them with either orientation. Three points $u < v < w$ cannot get $(+, -, +)$, because a stump changes its label at most once along the line.
- For each $d$, $\lfloor \log_2 d \rfloor \le VC(H_d) \le m^*$, where $m^*$ is the largest $m$ with $2^m \le 2 + 2d(m - 1)$. *Upper bound:* to shatter $m$ points the class needs $2^m$ labelings, and it has at most $2 + 2d(m-1)$ by the count above. *Lower bound:* take $m = \lfloor \log_2 d \rfloor$ points and give feature $j$ the values $x_{i,j} = $ bit $i$ of the number $j$; each of the $2^m \le d$ labelings is the stump $x_j > 1/2$ on the feature $j$ that encodes it. So $VC(H_d) = \Theta(\log d)$. For example $d = 1000$ gives $9 \le VC(H_d) \le 14$.

By the [fundamental theorem of statistical learning](/fundamental-theorem-of-statistical-learning/), ERM over stumps is then an agnostic PAC learner with sample complexity $O((\log d + \log(1/\delta)) / \varepsilon^2)$, up to constants. The [VC dimension](/vc-dimension/) page gives the bound with its constants.

**Stumps as weak learners.** The [weak learnability equivalence](/weak-learnability-equivalence/) needs a base learner whose weighted error is at most $1/2 - \gamma$ on every reweighting. Stumps do not always give this. On the four points of $\{0, 1\}^2$ labeled by $x_1 \oplus x_2$ with equal weights, every stump has error exactly $1/2$: each cut leaves one point of each label on each side. So boosted stumps cannot fit XOR, in line with the additive form above. When stumps do have an edge $\gamma_t$ in round $t$, AdaBoost's training error is at most $\prod_t \sqrt{1 - 4\gamma_t^2}$ (Schapire and Freund, Chapter 3).

**Empirical results.** Holte (1993) found that one-attribute rules were often only a few points of accuracy below C4.5 trees on the benchmark data sets of the time. This is an observation on those data sets, not a theorem, and it shows how simple many of those tasks were.

## References
