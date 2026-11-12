---
tag: N15Y9F
kind: algorithm
slug: random-forest
name: Random forest
aliases:
- random forests
- Forest-RI
area: machine-learning/supervised-learning
level: core
summary: "Bagged CART trees that choose each split among m features drawn at random, combined by vote or average. Out-of-bag examples give an error estimate and feature importances."
solves: [classification, regression]
model: real-ram
complexity:
  vars: {n: the number of training examples, m: the number of features drawn at each node, B: the number of trees}
  time: {worst: "O(B m n^2 log n)"}
  space: {extra: "Θ(B n)"}
properties: {deterministic: false, exact: false, online: false, recursive: true}
history:
  year: 2001
  people: [Leo Breiman]
  note: Breiman defined random forests and proved the strength and correlation bound in Machine Learning in 2001.
prereqs: [bagging, cart]
see_also: [extremely-randomized-trees, decision-tree, gini-impurity, bias-variance-tradeoff, feature-selection, gradient-boosting, xgboost, adaboost]
sources:
  - paper: doi:10.1023/A:1010933404324
    title: Leo Breiman, Random forests, Machine Learning 45(1), 2001
    locator: Section 1 (the definition), Section 2 (Theorem 1.2 on convergence and Theorem 2.3, the bound by strength and correlation), Section 3 (out-of-bag estimates), Section 4 (Forest-RI, random input selection), Section 10 (variable importance by noising up a variable) and Section 11 (regression)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Chapter 15 (Algorithm 15.1, the variance of an average of correlated trees, the defaults of floor(sqrt(p)) features with node size 1 for classification and floor(p/3) with node size 5 for regression, out-of-bag samples and variable importance)
  - paper: doi:10.1109/ICDAR.1995.598994
    title: Tin Kam Ho, Random decision forests, Proceedings of the 3rd International Conference on Document Analysis and Recognition, 1995
    locator: forests of trees built in randomly selected subspaces of the features
  - paper: doi:10.1109/34.709601
    title: Tin Kam Ho, The random subspace method for constructing decision forests, IEEE Transactions on Pattern Analysis and Machine Intelligence 20(8), 1998
    locator: each tree grown on one random subset of the features, without resampling the examples
  - paper: doi:10.1162/neco.1997.9.7.1545
    title: Yali Amit and Donald Geman, Shape quantization and recognition with randomized trees, Neural Computation 9(7), 1997
    locator: trees that choose each split among a random subset of the candidate questions
  - paper: doi:10.1023/A:1007607513941
    title: Thomas G. Dietterich, An experimental comparison of three methods for constructing ensembles of decision trees, bagging, boosting, and randomization, Machine Learning 40(2), 2000
    locator: randomized split selection among the best candidate splits
  - paper: "Andy Liaw and Matthew Wiener, Classification and regression by randomForest, R News 2(3), 2002"
    locator: the R package and its default number of features per split
  - paper: doi:10.1186/1471-2105-8-25
    title: Carolin Strobl, Anne-Laure Boulesteix, Achim Zeileis and Torsten Hothorn, Bias in random forest variable importance measures, illustrations, sources and a solution, BMC Bioinformatics 8, 2007
    locator: the bias of the impurity importance toward features with many cut points
---

A random forest is an ensemble of decision trees for classification and regression, defined by Breiman (2001). Each tree is a [CART](/cart/) tree grown on a bootstrap sample of the training set, as in [bagging](/bagging/), but at each node the split is chosen among only $m$ features drawn at random, not among all $d$. The trees are grown deep and not pruned, and the forest predicts by a majority vote or by the average of the trees. The random features make the trees less alike, so their average has a smaller variance than the average of bagged trees. The examples that a tree did not see give a free estimate of the error, the out-of-bag (OOB) error, and a measure of how much each feature matters.

## In plain words

Grow many decision trees, each a little different. Give each tree its own random sample of the data, drawn with repeats. At each question that a tree asks, let it look at only a few features picked at random, and ask the best question about those. Let each tree grow until its leaves are pure. To predict, let the trees vote, or take their average. One deep tree is very sensitive to the data, but the errors of many different trees partly cancel. Each tree did not see about a third of the data, so those left-out examples can test it, at no extra cost.

## The problem

The data model is a training set $S = \{(x_1, y_1), \ldots, (x_n, y_n)\}$ with $x_i \in \mathbb{R}^d$. For classification, $y_i$ is in a finite set of $k$ classes and the loss is the 0-1 loss; for regression, $y_i \in \mathbb{R}$ and the loss is the squared error. The parameters are the number of trees $B$, the number $m \le d$ of features to draw at each node, and the least leaf size $n_{\text{leaf}}$. The common defaults are $m = \lfloor \sqrt d \rfloor$ and $n_{\text{leaf}} = 1$ for classification, and $m = \lfloor d/3 \rfloor$ and $n_{\text{leaf}} = 5$ for regression (Hastie, Tibshirani and Friedman, Section 15.3). These are defaults to tune, not values that theory fixes. The output is the set of trees and, as by-products, the OOB error and a permutation importance for each feature.

## The algorithm

```pseudo id=main
RANDOM-FOREST(S, B, m, n_leaf)
L1  for b ← 1 to B do
L2      S_b ← n examples drawn from S uniformly with replacement      ▷ the bootstrap sample
L3      T_b ← GROW(S_b)
L4  predict x by the majority vote of T_1(x), ..., T_B(x), or by their average for regression

GROW(S')
L5  if |S'| < 2 n_leaf or all labels in S' are equal then return a leaf with the majority class (or the mean) of S'
L6  F ← m features drawn uniformly without replacement from {1, ..., d}
L7  (k, θ) ← the split x_k ≤ θ with k ∈ F and both sides of size ≥ n_leaf that has the largest decrease of Gini impurity (or of squared error)
L8  if there is no such split then return a leaf as in L5
L9  return the node (k, θ, GROW({(x, y) ∈ S' : x_k ≤ θ}), GROW({(x, y) ∈ S' : x_k > θ}))

OOB-ERROR-AND-IMPORTANCE
L10 for i ← 1 to n: ŷ_i ← the vote (or average) of the trees T_b with i ∉ S_b
L11 the OOB error ← the average loss of ŷ_i against y_i, over the i that have at least one such tree
L12 for each feature k and each tree T_b: e_b ← the error of T_b on its OOB examples; e_b^k ← that error after a random permutation of the values of feature k among those examples
L13 the importance of k ← the average over b of e_b^k − e_b
```

Line L7 is the [CART](/cart/) split search restricted to the features in $F$: for each $k \in F$, sort $S'$ by $x_k$ and scan the cut points between distinct values with running counts, as in [decision tree learning](/decision-tree-learning/). The impurity is the [Gini impurity](/gini-impurity/) for classification and the sum of squared errors for regression. A new set $F$ is drawn at each node, not once per tree. With $m = d$, line L6 draws all features and the forest is bagged CART trees.

## Example

Take $n = 8$ examples with $d = 2$ features and two classes, and grow $B = 3$ trees with $m = 1$ and $n_{\text{leaf}} = 1$.

| row | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $x_1$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| $x_2$ | 4 | 8 | 2 | 6 | 1 | 7 | 3 | 5 |
| $y$ | A | A | A | B | B | B | B | A |

The bootstrap samples, the feature draws at the nodes, and the trees that GROW returns are:

- $T_1$: sample rows $\{1, 1, 3, 4, 5, 6, 7, 8\}$. The root draws $x_1$ and splits at $x_1 \le 3.5$ into a pure leaf A. The right node draws $x_2$ and splits at $x_2 \le 4$ into a leaf B. Its right node draws $x_1$ and splits at $x_1 \le 7$ into B and A. Row 2 is out of bag.
- $T_2$: sample rows $\{2, 3, 3, 5, 6, 6, 7, 8\}$. The root draws $x_2$ and splits at $x_2 \le 1.5$ (leaf B), then $x_1 \le 4.5$ (leaf A), then $x_2 \le 6$ and $x_1 \le 7.5$. Rows 1 and 4 are out of bag.
- $T_3$: sample rows $\{1, 2, 4, 4, 5, 7, 8, 8\}$. The root draws $x_2$ and splits at $x_2 \le 3.5$ (leaf B), then $x_1 \le 3$ (leaf A), then $x_2 \le 5.5$ into A and B. Rows 3 and 6 are out of bag.

The OOB predictions use only the trees that did not see the row: row 2 gets A from $T_1$ (correct), rows 1 and 4 get A and A from $T_2$ (row 4 is wrong), and rows 3 and 6 get B and B from $T_3$ (row 3 is wrong). Rows 5, 7 and 8 are in every sample and get no OOB prediction. The OOB error is $2/5$. A new point $(2, 2)$ gets A from $T_1$, A from $T_2$ and B from $T_3$, so the forest predicts A. With so few trees the estimate is rough; with $B$ trees each row is out of bag for about $B/e$ of them.

## Correctness

A random forest has no guarantee to find the best classifier. Breiman proved two facts that explain its behavior, and the proof is below.

- **Convergence (Theorem 1.2).** As $B \to \infty$, the generalization error of the forest converges almost surely to a limit $PE^*$. Adding trees does not cause overfitting.
- **Strength and correlation (Theorem 2.3).** Let $mr(X, Y)$ be the margin of the limit forest: the fraction of trees that vote for the true class minus the largest fraction for another class. Let $s = \mathbb{E}\, mr$ be the strength and $\bar\rho$ the mean correlation of the raw margins of two trees. If $s > 0$, then

$$PE^* \le \frac{\bar\rho\,(1 - s^2)}{s^2}.$$

The proof writes the variance of the margin as $\bar\rho\,(\mathbb{E}\, sd)^2$, bounds it by $\bar\rho\,(1 - s^2)$ with two uses of Jensen's inequality, and ends with [Chebyshev's inequality](/chebyshev-inequality/). It uses no property of trees. The tests compute $s$, $\bar\rho$ and $PE^*$ exactly when the trees and the test examples are finite uniform distributions, and check each step. They also check that each OOB prediction uses exactly the trees whose sample excludes the row.

For regression, the same idea appears as the variance of an average of $B$ identically distributed predictions with variance $\sigma^2$ and pairwise correlation $\rho$ (Hastie, Tibshirani and Friedman, Eq. 15.1):

$$\rho\, \sigma^2 + \frac{1 - \rho}{B}\, \sigma^2.$$

More trees remove only the second term. Drawing $m < d$ features lowers $\rho$, which lowers the first.

## Complexity

At a node with $n'$ examples, line L7 sorts $n'$ values for each of the $m$ features, in $O(m\, n' \log n')$ time. The nodes of one level hold at most $n$ examples in total, so a level costs $O(m\, n \log n)$. A tree grown to pure leaves has depth $O(\log n)$ when the splits are balanced, and up to $n - 1$ in the worst case. So one tree costs $O(m\, n \log^2 n)$ when balanced and $O(m\, n^2 \log n)$ in the worst case, and the forest costs $B$ times that. Presorting each feature once removes one $\log n$ factor. Prediction costs one root-to-leaf path per tree. Each tree has at most $n$ leaves, so the forest takes $\Theta(B n)$ space. The OOB error costs one prediction per tree and OOB row, and the importance repeats it for each of the $d$ features.

## Properties

- **Randomized.** The forest depends on the bootstrap samples and the feature draws, so two runs with different seeds give different forests. The variance of the prediction from this source falls like $1/B$.
- **Embarrassingly parallel.** The trees are independent, so they can be grown on different processors, unlike the trees of [boosting](/boosting/).
- **Few parameters.** The defaults of $m$ and $n_{\text{leaf}}$ often work, and $B$ needs only to be large enough.
- **Invariant to monotone transforms.** The splits depend only on the order of each feature, so scaling or a monotone transform of a feature does not change the trees.
- **Built-in validation.** The OOB error is close to a cross-validation estimate and costs no extra training.
- **Interpretable importances.** The permutation importance of lines L12 and L13 measures how much the OOB error rises when a feature loses its link to the label. Breiman also proposed the total impurity decrease of a feature over all its splits, which is cheaper but biased toward features with many cut points (Strobl et al. 2007).

## Variants and improvements

- **Random subspaces (Ho 1998).** Each tree is grown on one random subset of the features, fixed for the whole tree, and on all the examples. A random forest instead draws new features at every node and resamples the examples. Ho's earlier random decision forests (1995) also built trees in random subspaces.
- **Randomized trees (Amit and Geman 1997, Dietterich 2000).** Amit and Geman chose each split among a random subset of the candidate questions; Dietterich chose at random among the 20 best splits of C4.5.
- **Forest-RC.** Breiman (2001, Section 5) also split on random linear combinations of a few features.
- **Extremely randomized trees.** [Extra trees](/extremely-randomized-trees/) draw the cut point at random as well, and use the whole sample instead of a bootstrap sample.
- **Quantile regression forests and survival forests** keep the full distribution of the labels in each leaf, not only its mean.
- **Gradient-boosted trees.** [Gradient boosting](/gradient-boosting/) and [XGBoost](/xgboost/) also use column subsampling, but grow small trees one after another.

## When to use it

Use a random forest as a strong first model for tabular data of moderate size, with mixed feature types and little tuning time. It needs no feature scaling, handles many features, and gives an error estimate and importances for free. When the best accuracy matters and there is time to tune, boosted trees often do better. On data with a few strong features and many noise features, a small $m$ makes many splits use only noise; then a larger $m$ helps.

## Pitfalls

- **Drawing the features once per tree.** Line L6 draws a new set at each node. One draw per tree is the random subspace method, a different algorithm.
- **Reading the OOB error from all the trees.** Line L10 must vote only with trees whose sample excludes the row. Using all trees gives the training error of deep trees, which is near 0.
- **Trusting impurity importance.** The mean decrease of impurity favors continuous features and categorical features with many levels. Use the permutation importance on OOB data, and remember that correlated features share their importance.
- **Pruning the trees.** The trees are grown deep on purpose. Their low bias is what the averaging keeps, and the averaging removes their variance.
- **Expecting the theorem to be tight.** The bound of Theorem 2.3 is often far above the real error. It explains the direction of the effects of $s$ and $\bar\rho$, not their size.
- **Extrapolating.** A regression forest predicts averages of training labels, so its predictions stay within the range of the training labels.

## Implementations

## History

Breiman introduced bagging in 1996. Ho built forests of trees in random subspaces in 1995 and described the random subspace method in 1998. Amit and Geman (1997) grew trees on random subsets of candidate questions for shape recognition, and Dietterich (2000) compared randomized C4.5 with bagging and boosting. Breiman (2001) joined bagging with random feature selection at each node, named the result random forests, proved the convergence theorem and the bound by strength and correlation, and gave the OOB estimates and permutation importance. Breiman and Cutler wrote the original software, and the R package of Liaw and Wiener (2002) made the method widely used.

## References
