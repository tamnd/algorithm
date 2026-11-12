---
tag: NF9SRS
kind: problem
slug: decision-tree-learning
name: Decision tree learning
aliases:
- decision tree induction
- top-down induction of decision trees
- TDIDT
area: machine-learning/supervised-learning
level: core
summary: "Build a decision tree from labeled examples. Finding an optimal tree is NP-hard, so learners grow it greedily top-down by impurity, then stop or prune."
prereqs: [decision-tree, information-gain, gini-impurity, overfitting]
see_also: [id3, c4-5, cart, cost-complexity-pruning, reduced-error-pruning, decision-stump, random-forest, np-hard]
sources:
  - paper: doi:10.1016/0020-0190(76)90095-8
    title: Laurent Hyafil and Ronald L. Rivest, Constructing optimal binary decision trees is NP-complete, Information Processing Letters 5(1), 1976
    locator: pages 15 to 17 (the identification problem with binary tests and the external path length; the reduction from exact cover by 3-sets)
  - book: isbn:9780412048418
    title: Leo Breiman, Jerome H. Friedman, Richard A. Olshen and Charles J. Stone, Classification and Regression Trees, Wadsworth, 1984 (reprinted by Chapman and Hall/CRC)
    locator: Chapter 2 (growing a tree by splits), Chapter 3 (stopping rules against pruning) and Chapter 4 (splitting rules)
  - paper: doi:10.1007/BF00116251
    title: J. R. Quinlan, Induction of decision trees, Machine Learning 1(1), 1986
    locator: pages 81 to 106, Section 2 (the TDIDT family of learners) and Section 4 (ID3)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 9.2 (growing, stopping and pruning regression and classification trees)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, From Theory to Algorithms, Cambridge University Press, 2014
    locator: Chapter 18 (decision trees; sample complexity, the generic greedy algorithm, gain measures, pruning, threshold splits)
  - paper: doi:10.1007/s10994-017-5633-9
    title: Dimitris Bertsimas and Jack Dunn, Optimal classification trees, Machine Learning 106(7), 2017
    locator: pages 1039 to 1082 (optimal trees of bounded depth by mixed-integer optimization)
  - paper: "Manish Mehta, Rakesh Agrawal and Jorma Rissanen, SLIQ, a fast scalable classifier for data mining, Proceedings of the 5th International Conference on Extending Database Technology (EDBT), 1996"
    locator: pages 18 to 32 (presorted attribute lists that keep the sort order through the tree)
---

Decision tree learning is the problem of building a [decision tree](/decision-tree/) from labeled examples so that it predicts the labels of new examples well. The exact versions are hard: Hyafil and Rivest (1976) proved that finding a binary tree of least expected number of tests is NP-complete. So nearly all learners use top-down induction (TDIDT): choose at each node the test that most reduces an impurity such as [information gain](/information-gain/) or the [Gini impurity](/gini-impurity/), split the examples, recurse, and then stop or prune to avoid [overfitting](/overfitting/). [ID3](/id3/), [C4.5](/c4-5/) and [CART](/cart/) are the classic members of this family.

## In plain words

You have a table of past cases, each with some measured properties and a known outcome. You want a flow chart of yes or no questions that gives the right outcome for new cases.

The best possible flow chart is too hard to find for real data, so learners build it one question at a time. At the top, try every property and every cut point, and keep the question that makes the two groups of cases most pure, that is, most of one outcome each. Then do the same inside each group. Stop when a group is pure or too small.

A flow chart that fits every past case exactly usually learns the noise too. So learners stop early, or grow a big chart and then cut back the questions that do not help on new data.

## Definition

**Data model.** A sample $S = ((x_1, y_1), \ldots, (x_n, y_n))$ of $n$ examples, with $x_i \in \mathcal{X} = \mathcal{X}_1 \times \cdots \times \mathcal{X}_d$ over $d$ features (numeric, $\mathcal{X}_j = \mathbb{R}$, or categorical with finitely many values) and labels $y_i$ in a set of $k$ classes or in $\mathbb{R}$. In learning theory the examples are drawn i.i.d. from an unknown distribution $D$ over $\mathcal{X} \times \mathcal{Y}$, and the goal is a tree of small expected loss under $D$. A learner only sees $S$, so it solves one of the following optimization problems over the class $\mathcal{T}$ of trees whose internal nodes use allowed tests (axis-aligned thresholds $x_j \le \theta$, or one branch per value of a categorical feature).

- **Penalized empirical risk.** Given a loss $\ell$ and $\alpha \ge 0$, find
$$ T^* \in \arg\min_{T \in \mathcal{T}} \; \sum_{i=1}^{n} \ell(T(x_i), y_i) + \alpha \, |\widetilde{T}|, $$
where $|\widetilde{T}|$ is the number of leaves. With the 0-1 loss this is the cost-complexity criterion of CART; see [cost-complexity pruning](/cost-complexity-pruning/).
- **Bounded size.** Minimize the empirical risk among trees of depth at most $h$, or with at most $L$ leaves.
- **Smallest consistent tree.** If no two examples with the same $x$ have different labels, find a tree with zero training error and the fewest leaves (or nodes, or least depth).

The output is a tree $T$, which defines the predictor $x \mapsto T(x)$. The penalty or the size bound is the essential part: without it, a tree with one leaf for each distinct $x_i$ has zero training error and says nothing about new data.

## Variants

- **Classification and regression.** Classification trees use the 0-1 loss and an impurity (entropy, Gini) to grow; regression trees use the squared error, and a leaf predicts the mean of its examples.
- **Split types.** Binary threshold splits (CART), multiway splits on categorical values (ID3, C4.5), subset splits of categorical values, and oblique splits $w^\top x \le \theta$, whose split search is a much larger search than the $O(d n)$ thresholds of axis-aligned splits.
- **Identification (Hyafil and Rivest).** Each example is its own class, and the tree must identify every object; the cost is the total depth of the objects. This is the problem whose decision version they proved NP-complete.
- **Missing values, costs and weights.** Unknown feature values ([C4.5](/c4-5/) fractional cases, [CART](/cart/) surrogate splits), a loss matrix for unequal error costs, and example weights (as in boosting).

## Examples

**PlayTennis.** On the 14 days of Quinlan (1986, Table 1), top-down induction with information gain puts outlook at the root (gain 0.2467 bits), splits the sunny days on humidity and the rainy days on wind, and makes overcast a leaf. The tree has 5 leaves, depth 2 and no training error; the [ID3](/id3/) page traces it.

**Greedy splitting can be blind.** Take the four points of $\{0, 1\}^2$ with $y = x_1 \oplus x_2$. Each single split leaves one example of each label on each side, so its information gain and its Gini decrease are 0. A greedy learner that stops when no split helps returns one leaf with training error $2/4$, while a tree of depth 2 has error 0. A learner that splits anyway, as ID3 does until the nodes are pure, finds the depth 2 tree, but the root choice was a tie broken by chance. With more features of noise, the chance of choosing a useful root becomes small.

**Hyafil and Rivest's objective.** Four objects and the tests "is it in $\{1, 2\}$", "is it in $\{1, 3\}$" and "is it 1": a balanced tree with the first two tests identifies each object in 2 tests, total 8. A path that asks "is it 1" first costs $1 + 2 + 3 + 3 = 9$ with the other tests. The problem asks for the least total.

## Known algorithms

**Top-down induction (TDIDT).** The common template of [ID3](/id3/), [C4.5](/c4-5/) and [CART](/cart/):

```pseudo id=main
GROW(S)                                     ▷ S: the examples at this node
L1  if STOP(S) then return a leaf with the best constant for S
L2  for each feature j do
L3      for each candidate test t on feature j do
L4          score(t) ← impurity(S) − Σ_v (|S_v| / |S|) · impurity(S_v)
L5  t* ← a test of largest score              ▷ ID3: gain; C4.5: gain ratio; CART: Gini or squared error
L6  if score(t*) ≤ minimum gain then return a leaf for S
L7  partition S into S_1, ..., S_r by the outcome of t*
L8  return a node with test t* and children GROW(S_1), ..., GROW(S_r)
```

Then a pruning pass may replace subtrees by leaves. The parts are:

- **Impurity.** [Entropy](/information-gain/), [Gini](/gini-impurity/) or, for regression, the sum of squared deviations from the node mean. All are zero on pure nodes, and the concave ones never increase under a split.
- **Split search.** For a numeric feature, sort the $n_t$ examples of the node by the feature and scan the cut points between distinct values while updating the class counts (or the sums $\sum y$, $\sum y^2$) of the two sides: $O(n_t \log n_t)$ for the sort and $O(n_t k)$ for the scan, as in the [decision stump](/decision-stump/). For a categorical feature with $v$ values, one counting pass costs $O(n_t + v k)$.
- **Stopping rules.** A pure node; no remaining test; fewer than $n_{\min}$ examples; depth $h_{\max}$ reached; best decrease below a threshold; a significance test (Quinlan 1986 discussed a chi-square test). Stopping early is cheap but myopic, as the XOR example shows, so Breiman et al. (1984, Chapter 3) grow a large tree and prune it instead.
- **Pruning.** [Cost-complexity pruning](/cost-complexity-pruning/) (CART), [reduced-error pruning](/reduced-error-pruning/) on a held-out set (Quinlan 1987), and pessimistic error pruning by an upper confidence limit ([C4.5](/c4-5/)).

**Cost of the split search.** The nodes of one level hold disjoint subsets of the $n$ examples. If each node sorts its own examples, a level costs $\sum_t O(d\, n_t \log n_t) = O(d n \log n)$ for numeric features. With **presorting**, the $d$ sorted orders are computed once in $O(d n \log n)$ time, and a split passes each order to the children by a stable partition in $O(d n_t)$ time, which keeps the children's orders sorted (Mehta, Agrawal and Rissanen 1996). A level then costs $O(d n k)$, or $O(d n)$ for two classes. A tree of depth $h$ costs $O(d n \log n + d n k h)$ in total with presorting and $O(d n h \log n)$ without. The depth is at most $n - 1$, and is $O(\log n)$ when the splits are balanced.

**Exact algorithms.** For small depth bounds, optimal trees can be found by exhaustive search, by dynamic programming over subsets of the data, or by mixed-integer optimization (Bertsimas and Dunn 2017). These methods take exponential time in the worst case, in line with the hardness result below.

**Ensembles.** [Random forests](/random-forest/), [bagging](/bagging/) and [gradient boosting](/gradient-boosting/) avoid the search for one good tree: they average or add many greedy trees.

## Bounds

**NP-completeness (Hyafil and Rivest 1976).** The problem they prove hard is this. *Input:* a finite set $X$ of objects, a finite set $\mathcal{T}$ of tests, each a function $X \to \{\text{true}, \text{false}\}$, and an integer $w$. *Question:* is there a binary decision tree whose internal nodes are tests of $\mathcal{T}$ and whose leaves each identify exactly one object of $X$, such that the external path length $\sum_{x \in X} \text{depth}(x)$ is at most $w$? Here $\text{depth}(x)$ is the number of tests on the path to the leaf of $x$, so the objective is $|X|$ times the expected number of tests to identify an object drawn uniformly from $X$. They prove this decision problem NP-complete by a reduction from [exact cover by 3-sets](/exact-cover-by-3-sets/). So finding a tree of least expected cost is [NP-hard](/np-hard/). Their result is about this identification problem with arbitrary binary tests; the hardness of the smallest consistent tree over feature thresholds, and of approximating it, was proved later by other authors.

**Greedy has no general guarantee.** The greedy template finds the best split at each node exactly, but the tree as a whole can be far from optimal, as the XOR example shows: the greedy tree may have error $1/2$ while a tree of depth 2 has error 0.

**Cost lower bound for the split search.** A learner that considers every threshold on every feature must at least read the data, $\Omega(d n)$ per level. In the [comparison model](/comparison-model/), the sorting step costs $\Theta(n \log n)$ per feature in the worst case, so presorting is the dominant term for a shallow tree.

**Sample complexity.** Shalev-Shwartz and Ben-David (Chapter 18) bound the description length of a tree with $s$ nodes over $d$ binary features by $(s + 1) \log_2(d + 3)$ bits, and so, by an [MDL](/minimum-description-length/) argument, its generalization gap: with probability at least $1 - \delta$, for every such tree the gap is at most $\sqrt{((s + 1)\log_2(d + 3) + \log(2/\delta)) / (2n)}$ under the 0-1 loss. This is the formal reason to prefer small trees.

## Reductions

Hyafil and Rivest reduce exact cover by 3-sets to the identification problem: from an instance of X3C they build objects and tests such that a tree of external path length at most a computed bound exists if and only if an exact cover exists. The construction is polynomial. No reduction in the other direction is needed for the hardness claim.

Learning a tree of depth one is the [decision stump](/decision-stump/) problem, which a sort and a scan solve exactly. So the hardness needs trees of growing depth; for each fixed depth bound the search over all trees is polynomial in $n$, with a degree that grows with the depth.

## Applications

Decision tree learning gives readable models in medicine (triage rules), credit scoring and other settings where a person must check or explain a prediction. Greedy trees are the base learners of [random forests](/random-forest/) and [gradient boosting](/gradient-boosting/), the most used methods on tabular data. Trees also serve as quick feature screens, because the features near the root are the most informative under the chosen impurity.

## References
