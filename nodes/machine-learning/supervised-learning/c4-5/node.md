---
tag: MDWZEM
kind: algorithm
slug: c4-5
name: C4.5 algorithm
aliases:
- C4.5
- C4.5 decision tree
- J48
area: machine-learning/supervised-learning
level: advanced
summary: "Quinlan's 1993 successor of ID3: gain ratio with an average-gain filter, numeric thresholds, fractional cases for missing values, and pessimistic error-based pruning."
solves: [decision-tree-learning]
model: real-ram
complexity:
  vars: {n: the number of training cases, d: the number of attributes, v: the largest number of values of a categorical attribute}
  time: {worst: O(d n^2 log n)}
  space: {extra: O(n v)}
properties: {deterministic: true, exact: false, online: false, recursive: true}
history:
  year: 1993
  people: [J. Ross Quinlan]
  note: "Quinlan's book C4.5, Programs for Machine Learning (1993) gave the algorithm and its C source code; Release 8 (1996) changed the handling of numeric attributes."
prereqs: [id3, information-gain]
see_also: [cart, decision-tree, decision-tree-learning, reduced-error-pruning, cost-complexity-pruning, overfitting, binomial-distribution]
sources:
  - book: isbn:9781558602380
    title: J. Ross Quinlan, C4.5, Programs for Machine Learning, Morgan Kaufmann, 1993
    locator: Chapter 1 (the golf data), Chapter 2 (gain, gain ratio, the average-gain constraint, tests on continuous attributes and the threshold rule), Chapter 3 (unknown attribute values and fractional cases), Chapter 4 (error-based pruning, U_CF(E, N), CF = 25%, subtree raising)
  - paper: doi:10.1613/jair.279
    title: J. R. Quinlan, Improved use of continuous attributes in C4.5, Journal of Artificial Intelligence Research 4, 1996
    locator: pages 77 to 90; Release 8, the choice of the threshold by gain and the MDL-based penalty on numeric tests
  - paper: doi:10.1007/BF00116251
    title: J. R. Quinlan, Induction of decision trees, Machine Learning 1(1), 1986
    locator: pages 81 to 106; Section 7 (the gain ratio)
  - paper: doi:10.1007/s10115-007-0114-2
    title: X. Wu, V. Kumar, J. R. Quinlan, et al., Top 10 algorithms in data mining, Knowledge and Information Systems 14(1), 2008
    locator: pages 1 to 37; Section 1 (C4.5)
  - paper: doi:10.1109/34.589207
    title: F. Esposito, D. Malerba and G. Semeraro, A comparative analysis of methods for pruning decision trees, IEEE Transactions on Pattern Analysis and Machine Intelligence 19(5), 1997
    locator: pages 476 to 491; the analysis and experiments on error-based pruning
---

C4.5 is J. Ross Quinlan's decision tree learner of 1993, the successor of [ID3](/id3/). It keeps the top-down growth of ID3 and adds four things: it ranks tests by the gain ratio, but only among tests whose [information gain](/information-gain/) is at least average; it splits numeric attributes at a threshold; it handles missing values by sending fractions of a case down every branch; and it prunes the grown tree with a pessimistic estimate of the error, the upper limit $U_{\mathrm{CF}}(E, N)$ of a binomial confidence interval with $\mathrm{CF} = 0.25$.

## In plain words

C4.5 builds a tree of questions about a case, like ID3, and fixes the weak spots of ID3.

- ID3 likes attributes with many values, because many small groups look pure. C4.5 divides the gain by the information in the split itself, so a split into many small parts pays a price.
- A numeric attribute, such as a temperature, gets a question like "is it at most 75?".
- A case with no value for the tested attribute goes down every branch, with a part of its weight in each.
- After growth, C4.5 asks how many errors each part of the tree would make in a bad but plausible case, and replaces a subtree by a leaf when the leaf is not worse by that measure.

## The problem

The input is a set of $n$ training cases $(x, y, w)$, where $x$ gives each of $d$ attributes a value or "unknown", an attribute is categorical (at most $v$ values) or numeric, $y$ is a class and $w > 0$ is a weight (1 for an ordinary case). The output is a [decision tree](/decision-tree/) whose internal nodes test a categorical attribute (one branch per value) or a numeric attribute against a threshold (two branches), and whose leaves hold class distributions. C4.5 is a heuristic for the NP-hard problem of [decision tree learning](/decision-tree-learning/); it does not find an optimal tree.

## The algorithm

For a test with outcomes $o$ on cases $S$ of weight $W$, let $W_o$ be the weight of the cases with known outcome $o$, $S_K$ the cases with a known value, of weight $W_K$, and $F = W_K / W$. With $H$ the entropy of the class weights in bits, C4.5 uses

$$\mathrm{gain} = F \Big( H(S_K) - \sum_o \frac{W_o}{W_K} H(S_o) \Big), \qquad \mathrm{split\ info} = -\sum_{o \,\cup\, \{?\}} \frac{W_o}{W} \log_2 \frac{W_o}{W},$$

where the split info treats "unknown" as one more outcome of weight $W - W_K$, and the gain ratio is gain / split info. A test is *admissible* only if at least two of its outcomes have known weight at least $m$ (by default $m = 2$). For a numeric attribute, every cut between two adjacent distinct values with weight at least $m$ on each side is a candidate test, and the cut of largest gain is kept.

```pseudo id=main
GROW(S)                               ▷ S: weighted cases
L1  if S has one class, or weight(S) < 2m then return LEAF(S)
L2  for each attribute a: find its best admissible test, with its gain and split info
L3  avg ← the mean gain of the tests found in L2
L4  t ← the test of largest gain ratio among those with gain ≥ avg
L5  if there is no such test, or its gain is 0, then return LEAF(S)
L6  N ← a node for t; p_o ← W_o / W_K for each outcome o
L7  send each known case to its outcome, and each unknown case to every outcome o with weight w·p_o
L8  for each outcome o of t do
L9      child(N, o) ← GROW(S_o), or a leaf with the class of S if S_o has no weight
L10 return N

PRUNE(T, S)                           ▷ returns a tree and its estimated errors
L11 if T is a leaf then return (T, N·U_CF(E, N)) for the N cases of S and the E of them it misclassifies
L12 prune each branch T_o on S_o; E_tree ← the sum of their estimates
L13 E_branch ← the estimate of the largest branch on all of S (∞ without subtree raising)
L14 if E_leaf ≤ E_branch + 0.1 and E_leaf ≤ E_tree + 0.1 then return a leaf, with estimate E_leaf
L15 else if E_branch ≤ E_tree + 0.1 then return PRUNE(the largest branch, S)
L16 else return (T, E_tree)
```

**The threshold.** The test on a numeric attribute is $x \le \theta$, where $\theta$ is the largest value of the attribute in the whole training set that does not exceed the midpoint of the chosen cut. So every threshold that C4.5 prints is a value that occurs in the data. This implementation chooses the cut by gain, as Release 8 does (Quinlan 1996); Release 8 also subtracts a penalty of $\log_2(c)/W$ from the gain of a numeric test with $c$ candidate cuts, which this page leaves out.

**Classifying.** A case with a known value follows its branch. A case with an unknown value (or a categorical value with no branch) follows every branch $o$ with weight $p_o$, and the class distributions of the leaves it reaches are added with these weights. The prediction is the class of largest total.

**The upper limit.** $U_{\mathrm{CF}}(E, N)$ is the $p$ with $P(\mathrm{Bin}(N, p) \le E) = \mathrm{CF}$: if a leaf makes $E$ errors on $N$ cases, it is the largest error rate under which seeing at most $E$ errors still has probability $\mathrm{CF}$. With $\mathrm{CF} = 0.25$ it is the upper end of a one-sided 75% confidence interval for the error rate of the leaf. For $E = 0$ it is $1 - \mathrm{CF}^{1/N}$. A leaf predicts $N \cdot U_{\mathrm{CF}}(E, N)$ errors, and a subtree predicts the sum over its leaves. Quinlan calls this reasoning a heuristic himself: the errors are counted on the same cases that grew the tree, so they are not an independent sample, and CF is in practice a knob that sets how much the tree is pruned. Smaller CF prunes more.

## Example

**The golf data.** Quinlan's 14 cases (book, Chapter 1) have outlook (sunny, overcast, rain), temperature and humidity as numbers, windy (true, false) and the class Play (9) or Don't Play (5). At the root:

| attribute | best test | gain | split info | gain ratio | gain ≥ average 0.1106? |
|---|---|---|---|---|---|
| outlook | three branches | 0.2467 | 1.5774 | 0.1564 | yes |
| humidity | $\le 80$ | 0.1022 | 0.9403 | 0.1087 | no |
| windy | two branches | 0.0481 | 0.9852 | 0.0488 | no |
| temperature | $\le 70$ | 0.0453 | 0.9403 | 0.0482 | no |

C4.5 tests outlook. Under sunny, humidity $\le 75$ separates the 2 Play cases from the 3 Don't Play cases; 75 is the largest value in the data that does not exceed the midpoint $(70 + 85)/2 = 77.5$ of the cut. Under rain, windy separates the classes, and overcast is a pure leaf.

**Why the filter and the minimum count matter.** Add a case-number attribute with 14 values. Its gain is the full 0.940 bits, and its split info is $\log_2 14 = 3.807$, so its gain ratio 0.247 beats outlook. The gain ratio alone does not stop it on 14 cases. C4.5 rejects it because no value has 2 cases, so the test is not admissible. The average-gain filter guards the other end: a test that splits off a few cases has a split info near 0 and so a large gain ratio even when its gain is small, and the filter removes such tests.

**A missing value.** Make the outlook of the case (overcast, 72, 90, true, Play) unknown (book, Chapter 3). On the 13 known cases $H = 0.961$ and the weighted entropy after the split is 0.747, so the gain is $\frac{13}{14}(0.961 - 0.747) = 0.199$. The split info, with the unknown case as a fourth outcome of weight 1/14, is 1.809. Outlook still wins. The unknown case goes to sunny with weight 5/13, to overcast with 3/13 and to rain with 5/13. The leaf "sunny, humidity > 75" then holds 3 Don't Play cases and $5/13 \approx 0.4$ of a Play case, which the book prints as (3.4/0.4). A new case (sunny, 75, unknown, false) reaches both humidity leaves, with weights 2/5.4 and 3.4/5.4 of the sunny branch, and gets $P(\text{Play}) = (2 + 0.385)/5.385 = 0.44$, so C4.5 predicts Don't Play.

**Pruning.** A subtree has three leaves that cover 6, 9 and 1 training cases with no errors (book, Chapter 4). Its estimate is $6\,U(0, 6) + 9\,U(0, 9) + 1\,U(0, 1) = 6(0.206) + 9(0.143) + 0.750 = 3.273$. A single leaf in its place covers 16 cases with 1 error, and predicts $16\,U(1, 16)$ errors. The book uses $U_{25\%}(1, 16) = 0.157$, which gives 2.512; the exact binomial limit is 0.1596, which gives 2.554. Either way the leaf is better, so C4.5 prunes the subtree.

## Correctness

C4.5 is a heuristic, so the guarantees are invariants. The proofs are below.

- **Weights are conserved.** The child for outcome $o$ gets weight $W_o W / W_K$, and these add up to $W$; the copies of one case over all leaves keep its full weight.
- **Growth stops.** Each child of a node of weight $W$ has weight at most $W - m$, since another outcome holds at least $m$, so the depth is at most $W/m - 1$ for total weight $W$.
- **Class probabilities** of every case, also with missing values, are nonnegative and add up to 1.
- **The upper limit** $U_{\mathrm{CF}}(E, N)$ is unique and the bisection finds it.
- **Pruning** stops and returns the estimate of the tree that it returns. Without subtree raising, the estimate grows by at most 0.1 for each internal node of the original tree.

## Complexity

Costs are on the [real RAM](/real-ram/), with no missing values.

- **One node.** With $n_t$ cases, a categorical attribute costs $O(n_t)$ to count; a numeric attribute costs $O(n_t \log n_t)$ to sort and $O(n_t k)$ to scan all cuts, for $k$ classes, keeping running class counts on each side.
- **One level** holds at most $n$ cases, so it costs $O(d\, n \log n)$ for a bounded number of classes.
- **Depth.** Each child has at least $m$ fewer cases than its parent, so the depth is at most $n/m$, and growth costs $O(d\, n^2 \log n)$ in the worst case. Real trees are much shallower, and the cost is close to $O(d\, n \log n)$ times the depth.
- **Missing values** copy a case into every branch of a node, so the number of case copies at a level can exceed $n$.
- **Pruning** without raising sends every case through one path, costing $O(n h)$ for depth $h$ plus one evaluation of $U_{\mathrm{CF}}$ for each node. Subtree raising evaluates the largest branch on all the cases of the node, which can add another factor of the tree size in the worst case.
- **Space.** Each internal node has at least two outcomes with $m$ cases each, so there are fewer than $n$ internal nodes and $O(n v)$ nodes in all. The original C source reorders one index array in place, so the cases need $O(n)$ extra space.

## Properties

- **Greedy and deterministic.** It never revises a split, and fixed tie rules make the output a function of the data.
- **Handles mixed data.** Categorical and numeric attributes and missing values are all handled without preprocessing.
- **Prunes without a validation set.** Error-based pruning uses only the training data, unlike [reduced-error pruning](/reduced-error-pruning/) and the cross-validation step of [cost-complexity pruning](/cost-complexity-pruning/).
- **Readable output.** The book's program also turns trees into production rules (C4.5rules), which are often smaller.

## Variants and improvements

- **Release 8** (Quinlan 1996) chooses the threshold of a numeric attribute by gain instead of gain ratio, and subtracts an MDL-style penalty $\log_2(c)/W$ from the gain of a numeric test with $c$ candidate cuts. It improved accuracy on data sets with many numeric attributes.
- **Subset tests.** An option groups the values of a categorical attribute into subsets, found greedily, so a test has fewer branches.
- **C5.0 (See5)** is Quinlan's later commercial system, with boosting, smaller rule sets and much faster code.
- **J48** is the C4.5 Release 8 clone in the Weka toolkit.
- **Other pruning.** [Reduced-error pruning](/reduced-error-pruning/) uses a held-out set; [cost-complexity pruning](/cost-complexity-pruning/) from [CART](/cart/) uses cross-validation. Esposito, Malerba and Semeraro (1997) compare these methods.

## When to use it

Use C4.5 when you want one readable tree from tabular data with mixed attribute types and missing values, and you do not want to hold out data for pruning. It works well as a baseline. For the best accuracy, ensembles of trees such as [random forests](/random-forest/) and [gradient boosting](/gradient-boosting/) usually win, at the cost of readability. Binary trees with cross-validated pruning ([CART](/cart/)) are the main alternative for a single tree.

## Pitfalls

- **Gain ratio alone.** A test with a tiny split info gets a huge gain ratio from a small gain. Keep the average-gain filter.
- **Threshold not at the midpoint.** C4.5 puts the threshold at a value of the training set. Code that uses the midpoint gives the same partition of the training data but can classify new cases between the two values differently from C4.5.
- **Unknown values are not a value.** Treating "unknown" as an ordinary category lets the tree learn from the pattern of missing data, which C4.5 does not do. Its fractional cases assume values are missing at random.
- **The pessimistic bound is not a confidence bound.** The training cases at a leaf are not an independent test sample, so $N \cdot U_{\mathrm{CF}}(E, N)$ is not a real 75% bound on the future errors. Treat CF as a tuning parameter.
- **Approximations of $U_{\mathrm{CF}}$.** The C source uses an interpolated normal approximation, so its numbers differ a little from the exact binomial limit (0.157 against 0.1596 for $E = 1$, $N = 16$). Close pruning decisions can differ.

## Implementations

## History

Quinlan developed C4.5 from [ID3](/id3/) through the late 1980s. The gain ratio already appears in the 1986 ID3 paper, as a fix for the bias of the gain toward many-valued attributes. The 1993 book collected the full system with its C source code: the average-gain constraint, numeric thresholds, fractional cases and error-based pruning. Release 8 in 1996 changed the handling of numeric attributes. C4.5 became one of the most used machine learning programs; in the 2006 survey of the IEEE International Conference on Data Mining, reported by Wu et al. (2008), it was first in the list of the top 10 algorithms in data mining. Quinlan's commercial successor is C5.0.

## References
