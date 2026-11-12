---
tag: 4YYHCQ
kind: data-structure
slug: decision-tree
name: Decision tree
aliases:
- classification tree
- regression tree
- axis-aligned decision tree
area: machine-learning/supervised-learning
level: intro
summary: A rooted tree that predicts. Each internal node tests one feature, each leaf holds a label or a value, and a prediction follows one root-to-leaf path in O(depth) tests.
model: real-ram
complexity:
  vars: {h: the depth of the tree, m: the number of nodes}
  time: {worst: O(h)}
  space: {extra: Θ(m)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1963
  people: [James N. Morgan, John A. Sonquist]
  note: "Morgan and Sonquist's Automatic Interaction Detection (1963) grew regression trees on survey data. CART (Breiman et al. 1984) and ID3 (Quinlan 1986) made trees a standard learner."
prereqs: [binary-tree, classification, regression]
see_also: [decision-tree-learning, cart, id3, c4-5, random-forest, decision-stump, decision-tree-model, kd-tree]
sources:
  - book: isbn:9780412048418
    title: Leo Breiman, Jerome H. Friedman, Richard A. Olshen and Charles J. Stone, Classification and Regression Trees, Wadsworth, 1984 (reprinted by Chapman and Hall/CRC)
    locator: Chapter 2 (the tree classifier, its nodes, splits and terminal nodes) and Chapter 8 (regression trees)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 9.2 (tree-based methods; 9.2.4 on categorical predictors, missing values, linear combination splits and instability)
  - book: isbn:9780070428072
    title: Tom M. Mitchell, Machine Learning, McGraw-Hill, 1997
    locator: Chapter 3, Sections 3.2 and 3.3 (the representation of decision trees and the problems they fit)
  - paper: doi:10.1007/BF00116251
    title: J. R. Quinlan, Induction of decision trees, Machine Learning 1(1), 1986
    locator: pages 81 to 106, Section 3 (the tree as a classification rule) and Figure 2
  - paper: "James N. Morgan and John A. Sonquist, Problems in the analysis of survey data, and a proposal, Journal of the American Statistical Association 58(302), 1963"
    locator: pages 415 to 434 (the AID procedure, a binary regression tree grown by sum-of-squares splits)
---

A decision tree is a rooted tree that predicts: each internal node holds a test on one feature of the input, each edge out of it holds one outcome of the test, and each leaf holds a prediction, a class label for a [classification](/classification/) tree or a number for a [regression](/regression/) tree. To predict for an input, start at the root, follow the edge of each test outcome, and return the value at the leaf you reach, so a prediction costs $O(h)$ tests on a tree of depth $h$. This page treats the tree as a data structure, with axis-aligned tests $x_j \le \theta$ unless it says otherwise; how to choose the tests from data is [decision tree learning](/decision-tree-learning/).

## In plain words

A decision tree is a flow chart of questions. Each question looks at one property of the thing you want to judge, such as "is the age at most 30?" The answer sends you left or right to the next question. When there are no more questions, you are at an end box, and the end box holds the answer, for example "approve" or a price.

Each end box stands for the set of all inputs that give the same answers on the way to it. These sets do not overlap, and together they cover all inputs. So the tree cuts the input space into boxes and gives one answer to each box. A shallow tree answers fast, because one input meets only the questions on its own path.

## The abstract type

The tree stores a function $f : \mathcal{X} \to \mathcal{Y}$ from inputs $x = (x_1, \ldots, x_d) \in \mathbb{R}^d$ to outputs. Here $d$ is the number of features, $\mathcal{Y}$ is a finite set of $k$ classes for a classifier or $\mathbb{R}$ for a regressor. The operations are:

| operation | result |
|---|---|
| PREDICT$(T, x)$ | $f(x)$, the value of the leaf whose cell holds $x$ |
| SPLIT-LEAF$(T, v, j, \theta, a, b)$ | leaf $v$ becomes the test $x_j \le \theta$ with new leaves of values $a$ and $b$ |
| PRUNE$(T, v, c)$ | the subtree at $v$ becomes one leaf of value $c$ |
| DEPTH$(T)$, SIZE$(T)$, LEAVES$(T)$ | the depth $h$, the number of nodes $m$, the list of leaves |
| CELL$(T, v)$ | the box of inputs that reach $v$ |

A learner calls SPLIT-LEAF while it grows the tree (see [CART](/cart/), [ID3](/id3/) and [C4.5](/c4-5/)) and PRUNE when it simplifies it (see [cost-complexity pruning](/cost-complexity-pruning/) and [reduced-error pruning](/reduced-error-pruning/)).

## Representation

Each node $v$ has a parent pointer and is either

- a **leaf**, with a value $c(v) \in \mathcal{Y}$ (often also the class counts or the mean of the training examples that reach it), or
- an **internal node**, with a feature index $j(v) \in \{1, \ldots, d\}$, a threshold $\theta(v) \in \mathbb{R}$, a left child for $x_{j(v)} \le \theta(v)$ and a right child for $x_{j(v)} > \theta(v)$.

The invariant is: (R1) each internal node has exactly two children, whose parent pointer is that node; (R2) the nodes form one finite tree under the root. The *cell* $C(v)$ of a node is the set of inputs that satisfy all tests on the path from the root to $v$. For an axis-aligned tree, each cell is a box $\prod_j (lo_j, hi_j]$, with $lo_j = -\infty$ or $hi_j = +\infty$ allowed. The implementation stores the nodes in parallel arrays indexed by node id, so a child is an integer and no recursion is needed.

A tree over categorical features uses a *multiway* node instead: it tests $x_j$ and has one child for each value of feature $j$. [ID3](/id3/) and [C4.5](/c4-5/) use multiway nodes; [CART](/cart/) uses only binary nodes, with a test $x_j \in S$ for a subset $S$ of the values.

## Operations

```pseudo id=main
PREDICT(T, x)                         ▷ the value f(x) of the leaf whose cell holds x
L1  v ← root(T)
L2  while v is not a leaf do
L3      if x[j(v)] ≤ θ(v) then v ← left(v)
L4      else v ← right(v)
L5  return c(v)
```

PREDICT walks one path. Each iteration does one comparison and moves one level down, so it does at most $h$ comparisons.

```pseudo id=split
SPLIT-LEAF(T, v, j, θ, a, b)          ▷ v is a leaf
L6  j(v) ← j, θ(v) ← θ
L7  left(v) ← a new leaf with value a and parent v
L8  right(v) ← a new leaf with value b and parent v
```

SPLIT-LEAF takes $O(1)$ time. It refines the cell $C(v)$ into the two halves $C(v) \cap \{x_j \le \theta\}$ and $C(v) \cap \{x_j > \theta\}$ and leaves the other cells alone.

```pseudo id=prune
PRUNE(T, v, c)
L9  remove all descendants of v       ▷ with an explicit stack
L10 make v a leaf with value c
```

PRUNE takes time linear in the size of the removed subtree. It merges all the cells below $v$ back into $C(v)$.

DEPTH, SIZE and LEAVES are one traversal each, $O(m)$ time, or $O(1)$ for SIZE and the number of leaves if the counts are kept up to date as the implementation does. CELL$(T, v)$ walks from $v$ to the root and intersects the tests, in $O(h)$ time.

## Example

Start from one leaf of value A on inputs $x = (x_1, x_2)$, and apply these operations.

| step | operation | the leaves and their cells | $h$ | $m$ |
|---|---|---|---|---|
| 0 | the new tree | A: all of $\mathbb{R}^2$ | 0 | 1 |
| 1 | SPLIT-LEAF(root, 1, 2.5, A, B) | A: $x_1 \le 2.5$; B: $x_1 > 2.5$ | 1 | 3 |
| 2 | SPLIT-LEAF(leaf B, 2, 1.0, B, C) | A: $x_1 \le 2.5$; B: $x_1 > 2.5, x_2 \le 1.0$; C: $x_1 > 2.5, x_2 > 1.0$ | 2 | 5 |
| 3 | PREDICT$((3.0, 0.5))$ | root: $3.0 > 2.5$, go right; $0.5 \le 1.0$, go left; return B | 2 | 5 |
| 4 | PREDICT$((2.5, 9.0))$ | root: $2.5 \le 2.5$, go left; return A | 2 | 5 |
| 5 | PRUNE(the node $x_2 \le 1.0$, B) | A: $x_1 \le 2.5$; B: $x_1 > 2.5$ | 1 | 3 |

Step 4 shows the tie rule: an input exactly on the threshold goes left.

**A function that needs a full tree.** The parity of $d$ bits, $f(x) = x_1 \oplus \cdots \oplus x_d$ on $\{0, 1\}^d$, has a tree of depth $d$ with $2^d$ leaves, and no tree with fewer leaves computes it. Suppose a leaf $\ell$ is reached by an input $x$ and the path to $\ell$ never tests $x_i$. Flip bit $i$ of $x$: the new input passes the same tests, so it reaches $\ell$ too, but its parity differs. So each path tests all $d$ features, each leaf cell holds exactly one point of $\{0, 1\}^d$, and there are $2^d$ leaves. The same argument shows why trees learn additive and parity-like structure poorly.

## Correctness

The invariant (R1) gives the key fact: the leaf cells partition the input space, so each input reaches exactly one leaf and the tree is a well defined function. The proof is by induction on the height: the two children of an internal node $v$ split $C(v)$ by a test and its negation, which partition $C(v)$. PREDICT keeps the loop invariant $x \in C(v)$; it moves one level down per iteration, so it stops at a leaf whose cell holds $x$, which is the unique such leaf. SPLIT-LEAF and PRUNE keep (R1) and (R2), change $f$ only on $C(v)$, and change the counts by exactly one leaf and one internal node. The full proofs are below.

## Complexity

The table is for a binary tree with $m$ nodes, $L$ leaves and depth $h$, on the [real RAM](/real-ram/), where a comparison of two reals costs one step.

| operation | worst case time |
|---|---|
| PREDICT | $O(h)$ comparisons |
| SPLIT-LEAF | $O(1)$ |
| PRUNE at $v$ | $O(\text{size of the subtree at } v)$ |
| CELL | $O(h)$ |
| DEPTH, LEAVES | $O(m)$ |
| SIZE, number of leaves | $O(1)$ with stored counts |

The space is $\Theta(m)$ words.

- **Size.** Each internal node has two children, so $L = m_{\text{int}} + 1$ and $m = 2L - 1$. Proof: each tree arises from one leaf by SPLIT-LEAF calls, and each call adds one internal node and one leaf.
- **Depth.** Level $i$ holds at most $2^i$ nodes, so $L \le 2^h$ and $h \ge \lceil \lg L \rceil$. A path tree (a "caterpillar") has $h = L - 1$. So $\lceil \lg L \rceil \le h \le L - 1$.
- **Trees fitted to data.** If each leaf of a learned tree holds at least one of the $n$ training examples, the leaf cells are disjoint and nonempty on the data, so $L \le n$ and $h \le n - 1$. A balanced tree gives a prediction in $O(\log n)$ tests; a learned tree can be far from balanced, so libraries cap the depth.
- **Multiway nodes.** A node with one child for each of $v$ values finds its child in $O(1)$ time with an array indexed by the value, so PREDICT stays $O(h)$.

## Variants

- **Classification and regression trees.** A classification leaf stores the majority class, or the class counts so that PREDICT can return class probabilities. A regression leaf stores the mean of its training targets, which minimizes the squared error in the cell (see [CART](/cart/)).
- **Multiway and subset splits.** For a categorical feature, a node has one child per value ([ID3](/id3/), [C4.5](/c4-5/)) or two children for a subset of values and its complement ([CART](/cart/)).
- **Oblique trees.** A node tests $w^\top x \le \theta$, a linear combination of features, so the cells are convex polytopes instead of boxes. Breiman et al. 1984 (Chapter 5) gave such splits. A test then costs $O(d)$, and PREDICT costs $O(h d)$.
- **Model trees.** A leaf holds a small model, for example a linear regression, instead of a constant.
- **Stumps and ensembles.** A tree of depth one is a [decision stump](/decision-stump/). Many trees combined give a [random forest](/random-forest/) or [gradient boosting](/gradient-boosting/).
- **Comparison trees.** The [decision tree model](/decision-tree-model/) of computation uses the same shape for a different purpose: its nodes compare input items, and its depth is a lower bound on the number of comparisons of an algorithm. A [k-d tree](/kd-tree/) also cuts space into axis-aligned boxes, but to search for points, not to predict.

## When to use it

Use a decision tree when you need a model that a person can read and check, when the features mix numbers and categories with different scales, or when prediction must be fast and simple. Trees need no feature scaling, because each test compares one feature with a threshold, and they can model interactions between features. They are a poor choice for smooth or additive targets, such as a sum of many small effects, and for oblique boundaries such as $x_1 = x_2$, which a tree can only approximate with a staircase of many leaves. A single deep tree has high variance: a small change in the data can change the root test and so the whole tree (Hastie, Tibshirani and Friedman, Section 9.2.4). When accuracy matters more than readability, use an ensemble of trees.

## Pitfalls

- **Ties at the threshold.** Line L3 sends $x_j = \theta$ to the left. A learner that chose $\theta$ with a strict test $x_j < \theta$ and a predictor that uses $\le$ disagree on the examples at the threshold. Use one rule in both, or put thresholds at midpoints between distinct training values.
- **Deep recursion.** A learned tree can have depth close to $n$. A recursive PREDICT or PRUNE can then overflow the call stack. Use a loop as in lines L2 to L4 and an explicit stack in PRUNE.
- **Missing feature values.** Line L3 needs $x_{j(v)}$. If the input lacks it, the tree must say what to do: follow a surrogate test ([CART](/cart/)), send the input down all branches with weights ([C4.5](/c4-5/)), or use a default branch. A tree without such a rule fails on missing values.
- **Reading the tree as causal.** A test near the root is a good predictor in this data, not a cause, and a correlated feature could have taken its place.

## Implementations

## History

Morgan and Sonquist (1963) proposed Automatic Interaction Detection, which grew binary regression trees on survey data by splits that reduce the sum of squares. Breiman, Friedman, Olshen and Stone published Classification and Regression Trees in 1984, with binary trees for both tasks and a theory of pruning. Quinlan published ID3 in 1986 in the first issue of Machine Learning, with multiway trees chosen by information gain, and its successor C4.5 in 1993.

## References
