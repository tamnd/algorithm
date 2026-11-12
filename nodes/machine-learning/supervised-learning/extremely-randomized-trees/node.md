---
tag: ZH6FA9
kind: algorithm
slug: extremely-randomized-trees
name: Extremely randomized trees
aliases:
- extra trees
area: machine-learning/supervised-learning
level: advanced
summary: "An ensemble of trees grown on the whole sample, where each node draws K attributes and one random cut point for each, and keeps the best of these K splits by score."
solves: [classification, regression]
model: real-ram
complexity:
  vars: {n: the number of training examples, d: the number of attributes, M: the number of trees}
  time: {worst: "O(M d n^2)"}
  space: {extra: "Θ(M n)"}
properties: {deterministic: false, exact: false, online: false, recursive: true}
history:
  year: 2006
  people: [Pierre Geurts, Damien Ernst, Louis Wehenkel]
  note: Geurts, Ernst and Wehenkel described the Extra-Trees algorithm in Machine Learning in 2006.
prereqs: [random-forest, decision-tree-learning]
see_also: [bagging, cart, decision-tree, information-gain, shannon-entropy, bias-variance-tradeoff, ensemble-learning]
sources:
  - paper: doi:10.1007/s10994-006-6226-1
    title: Pierre Geurts, Damien Ernst and Louis Wehenkel, Extremely randomized trees, Machine Learning 63(1), 2006
    locator: Section 2 (the Extra-Trees algorithm and its pseudocode, the parameters K, n_min and M, the default values, the score measures and the complexity), the experiments on the effect of the parameters, and the bias and variance analysis
  - paper: doi:10.1023/A:1010933404324
    title: Leo Breiman, Random forests, Machine Learning 45(1), 2001
    locator: Section 4 (random input selection at each node, the method that Extra-Trees randomizes further)
  - paper: doi:10.1023/A:1007607513941
    title: Thomas G. Dietterich, An experimental comparison of three methods for constructing ensembles of decision trees, bagging, boosting, and randomization, Machine Learning 40(2), 2000
    locator: randomized split selection among the best candidate splits
  - paper: doi:10.1109/34.709601
    title: Tin Kam Ho, The random subspace method for constructing decision forests, IEEE Transactions on Pattern Analysis and Machine Intelligence 20(8), 1998
    locator: trees grown on all the examples, each in a random subspace of the attributes
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 15.2 (Eq. 15.1, the variance of an average of correlated predictions)
---

Extremely randomized trees, or Extra-Trees, is a tree ensemble method for classification and regression by Geurts, Ernst and Wehenkel (2006). Like a [random forest](/random-forest/), it averages many unpruned trees and draws $K$ attributes at random at each node. It differs in two ways. First, for each drawn attribute it draws one cut point uniformly at random between the smallest and largest value in the node, instead of searching for the best cut point, and then keeps the best of these $K$ random splits by a score. Second, by default each tree is grown on the whole training set, with no bootstrap sample. The random cut points make the trees less alike and faster to grow; the averaging over $M$ trees removes the extra variance.

## In plain words

Grow many decision trees on all the data. At each question a tree asks, pick a few features at random. For each of them, do not search for the best place to cut; pick a cut point at random between the smallest and the largest value of that feature in the current group. Then keep the cut that separates the labels best among these few. Stop when a group is very small or has only one label. Each tree is rough and different from the others, but the vote or the average of many such trees is smooth and accurate, and the trees are fast to build because no feature needs to be sorted.

## The problem

The data model is a training set $S = \{(x_1, y_1), \ldots, (x_n, y_n)\}$ with $x_i \in \mathbb{R}^d$ (numerical attributes) and $y_i$ in a finite set of classes or in $\mathbb{R}$. The parameters are the number of trees $M$, the number $K$ of attributes drawn at each node, and the least node size $n_{\min}$ for a split. The defaults of the paper are $K = \sqrt d$ and $n_{\min} = 2$ for classification, and $K = d$ and $n_{\min} = 5$ for regression. With $n_{\min} = 2$ the trees are fully grown. The output is $M$ trees, combined by a majority vote for classification and by the average for regression.

The score of a split is the normalized information gain for classification,

$$\mathrm{Score}(s, S) = \frac{2\, I_c^s(S)}{H_c(S) + H_s(S)},$$

where $H_c(S)$ is the [entropy](/shannon-entropy/) of the classes in $S$, $H_s(S)$ is the entropy of the split (the sizes of the two sides), and $I_c^s(S)$ is their mutual information, the [information gain](/information-gain/) of the split. For regression it is the relative reduction of the variance of the output, $(\mathrm{var}(S) - \frac{|S_l|}{|S|}\mathrm{var}(S_l) - \frac{|S_r|}{|S|}\mathrm{var}(S_r))/\mathrm{var}(S)$.

## The algorithm

```pseudo id=main
EXTRA-TREES(S, M, K, n_min)
L1  for i ← 1 to M do
L2      t_i ← BUILD(S)                         ▷ the whole training set, no bootstrap
L3  predict x by the majority vote of t_1(x), ..., t_M(x), or by their average for regression

BUILD(S)
L4  if |S| < n_min or all attributes are constant in S or the output is constant in S then return a leaf with the majority class (or the mean output) of S
L5  A ← K attributes drawn without replacement among the attributes that are not constant in S (all of them if there are fewer than K)
L6  for each a ∈ A: draw a cut point c_a uniformly between min_S a and max_S a, and let s_a be the split [x_a < c_a]
L7  s* ← the split s_a with the largest Score(s_a, S)
L8  return the node (s*, BUILD(the examples of S with x_a < c_a), BUILD(the other examples of S)) for s* = s_a
```

The parameter $K$ sets the strength of the randomization. With $K = 1$, the split does not depend on the outputs at all; Geurts et al. call these totally randomized trees. With larger $K$, the score filters out bad random splits. Line L5 skips constant attributes, so each drawn attribute gives a split with two nonempty sides.

## Example

Take one node with six examples, two attributes and $K = 2$:

| row | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $x_1$ | 1 | 2 | 3 | 4 | 5 | 6 |
| $x_2$ | 5 | 1 | 4 | 2 | 6 | 3 |
| $y$ | A | A | A | B | B | B |

Both attributes are not constant, so line L5 takes both. Suppose line L6 draws $c_1 = 4.2$ in $[1, 6]$ and $c_2 = 2.5$ in $[1, 6]$.

- The split $[x_1 < 4.2]$ sends rows 1 to 4 (A, A, A, B) left and rows 5 and 6 (B, B) right. In bits, $H_c = 1$, $H_s = H(4/6, 2/6) = 0.9183$ and $H(C \mid s) = \frac46 H(3/4, 1/4) = 0.5409$, so $I = 0.4591$ and the score is $2 \cdot 0.4591 / 1.9183 = 0.4787$.
- The split $[x_2 < 2.5]$ sends rows 2 and 4 (A, B) left and the other four (A, A, B, B) right. Both sides have the class proportions of the node, so $I = 0$ and the score is $0$.

Line L7 keeps $[x_1 < 4.2]$. The best CART split, $x_1 < 3.5$, has score $1$, but the random cut on $x_1$ finds a split with the same left set only when $c_1$ falls in $(3, 4]$, which has probability $1/5$. The left child $\{1, 2, 3, 4\}$ is split again; the right child has a constant output and becomes a leaf.

## Correctness

Extra-Trees is a heuristic, and the paper supports its accuracy by experiments and by a bias and variance analysis. The facts below are proved on the proof page.

- Each split puts at least one example on each side, so BUILD terminates and each tree has at most $n$ leaves.
- For an attribute with distinct values $v_1 < \ldots < v_r$ in the node, the split puts $v_1, \ldots, v_j$ on the left with probability $(v_{j+1} - v_j)/(v_r - v_1)$, whatever the outputs.
- The classification score is in $[0, 1]$, since the mutual information is at most each of the two entropies; it is 1 exactly when the split and the class determine each other. The regression score is in $[0, 1]$ by the law of total variance.
- With $n_{\min} = 2$ and distinct inputs, each tree has zero training error.
- Given the training set, the trees are independent and identically distributed, so the variance due to the random draws falls like $1/M$.

The tests check that each node keeps the best of its $K$ recorded random splits, that each cut lies between the smallest and largest value of the node, the distribution of the cut, the stopping rule at $n_{\min}$, and that each root holds all $n$ examples.

## Complexity

At a node with $n'$ examples, line L6 finds the minimum and maximum of $K$ attributes and line L7 scores $K$ splits, in $O(K n')$ time, with no sorting. Finding the attributes that are not constant costs $O(d n')$ in the worst case, but drawing an attribute and testing it, and drawing again if it is constant, is cheaper when few attributes are constant. The nodes of one level hold at most $n$ examples, so a level costs $O(d n)$, and $O(K n)$ with lazy draws. The depth is $O(\log n)$ for balanced trees and at most $n - 1$, so the worst case for $M$ trees is $O(M d n^2)$, and the balanced case is $O(M K n \log n)$, the cost given in the paper. Each tree has at most $n$ leaves, so the ensemble takes $\Theta(M n)$ space.

## Properties

- **Randomized.** The trees depend on the random draws. Two runs with different seeds give different ensembles.
- **Faster than a random forest.** No attribute is sorted at any node, so the trees are cheaper to grow than CART trees on the same data.
- **Whole sample.** With no bootstrap, each tree sees every example, which lowers the bias of each tree. The randomness of the cut points alone keeps the trees apart.
- **Smooth average.** Averages of many trees with random cut points give a response that changes more gradually than a single tree or a forest of trees with optimized cut points.
- **Scale-dependent cut points.** The cut is uniform in value, so a monotone transform of an attribute changes the distribution of the splits, unlike in CART.

## Variants and improvements

- **Totally randomized trees.** With $K = 1$ the trees do not look at the outputs to choose splits, and the ensemble behaves like a kernel method whose kernel depends only on the inputs.
- **Bootstrap.** Extra-Trees can be combined with bootstrap samples. The paper uses the whole sample by default, to keep the bias of each tree small.
- **Random forests.** A [random forest](/random-forest/) optimizes the cut point of each drawn attribute and uses bootstrap samples.
- **Random subspaces.** Ho (1998) grew each tree in one random subset of the attributes, on all the examples.
- **Randomized C4.5.** Dietterich (2000) chose at random among the best candidate splits.

## When to use it

Use Extra-Trees as an alternative to a random forest on numerical data, when the training time matters or when the target changes smoothly. It is often as accurate as a random forest, and the defaults of $K$ and $n_{\min}$ work well. When attributes have strong outliers or very uneven scales, the uniform cut point wastes many splits, and a random forest or a rank transform of the attributes helps.

## Pitfalls

- **Searching for the best cut point.** Line L6 draws one cut point per attribute. Searching over all cut points of each drawn attribute gives a random forest without bootstrap, not Extra-Trees.
- **Adding a bootstrap by default.** Line L2 grows each tree on all of $S$. Bootstrap samples are an option, not the default.
- **Using too few trees.** A single extremely randomized tree is a poor predictor. The method relies on $M$ being large.
- **Drawing constant attributes.** A constant attribute gives no split with two nonempty sides. Line L5 draws only among the attributes that are not constant in the node.
- **Ignoring the scale of attributes.** A heavy tail puts most of the interval $[\min, \max]$ where few examples lie, so most random cuts are nearly useless.

## Implementations

## History

Breiman's [bagging](/bagging/) (1996) and [random forests](/random-forest/) (2001), Ho's random subspaces (1998) and Dietterich's randomized C4.5 (2000) showed that randomization of trees helps the ensemble. Geurts, Ernst and Wehenkel (2006) pushed the randomization to the cut points and dropped the bootstrap, compared the result with these methods on many data sets, and analyzed its bias and variance and its link to kernel methods.

## References
