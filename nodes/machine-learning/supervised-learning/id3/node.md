---
tag: 3VDGHC
kind: algorithm
slug: id3
name: ID3 algorithm
aliases:
- Iterative Dichotomiser 3
- ID3 decision tree
area: machine-learning/supervised-learning
level: core
summary: "Quinlan's 1986 tree learner for categorical attributes: split each node on the attribute of largest information gain, one branch per value, until the nodes are pure."
solves: [decision-tree-learning]
model: real-ram
complexity:
  vars: {n: the number of examples, d: the number of attributes, v: the largest number of values of an attribute, k: the number of classes}
  time: {worst: O(d^2 n v k)}
  space: {extra: O(d n v)}
properties: {deterministic: true, exact: false, online: false, recursive: true}
history:
  year: 1986
  people: [J. Ross Quinlan]
  note: "Quinlan described ID3 in full in Induction of decision trees, in the first issue of the journal Machine Learning (1986)."
prereqs: [decision-tree-learning, information-gain]
see_also: [c4-5, cart, decision-tree, reduced-error-pruning, gini-impurity, overfitting]
sources:
  - paper: doi:10.1007/BF00116251
    title: J. R. Quinlan, Induction of decision trees, Machine Learning 1(1), 1986
    locator: pages 81 to 106; Section 2 (the TDIDT family and its origin in Hunt's CLS), Section 4 (ID3, the information-based criterion, windowing, Table 1 and Figure 2), Section 5 (noise and the chi-square test), Section 6 (unknown values) and Section 7 (the selection criterion and the gain ratio)
  - book: isbn:9780070428072
    title: Tom M. Mitchell, Machine Learning, McGraw-Hill, 1997
    locator: Chapter 3; Table 3.1 (the ID3 algorithm), Section 3.4 (Table 3.2 PlayTennis and the gains 0.246, 0.151, 0.048, 0.029), Section 3.5 (hypothesis space search) and Section 3.7 (overfitting and extensions)
  - book: isbn:9781558602380
    title: J. Ross Quinlan, C4.5, Programs for Machine Learning, Morgan Kaufmann, 1993
    locator: Chapter 1 (ID3 as the basis of C4.5) and Chapter 2 (the gain and gain ratio criteria)
---

ID3 is J. Ross Quinlan's algorithm for [decision tree learning](/decision-tree-learning/) on categorical attributes, published in full in 1986. It grows a [decision tree](/decision-tree/) top-down: at each node it tests the attribute of largest [information gain](/information-gain/) on the examples that reach the node, makes one branch for each value of that attribute, and recurses on each branch until the examples are pure or no attribute is left. The original has no pruning step, so it fits consistent training data exactly; its successor [C4.5](/c4-5/) added the gain ratio, numeric thresholds, missing values and pruning.

## In plain words

You have a table of past cases. Each case has a few properties with a small set of possible values, such as the weather being sunny, overcast or rainy, and a known outcome.

ID3 asks which property, if you sort the cases by it, makes the groups most pure in outcome. It measures purity with entropy from information theory. It puts that property at the top of the tree, with one branch for each value, and sorts the cases into the branches. Then it does the same inside each branch with the properties that are left. A branch whose cases all have the same outcome becomes an answer. A branch with no cases gets the most common outcome of its parent.

## The problem

The input is a sample $S$ of $n$ examples $(x, y)$, where $x$ gives a value to each of $d$ categorical attributes, attribute $a$ has a finite set of values $V_a$ with $|V_a| \le v$, and $y$ is one of $k$ classes. The output is a multiway decision tree whose internal nodes test one attribute and have one child for each value. ID3 does not solve an optimization problem exactly, since finding the smallest consistent tree is NP-hard (see [decision tree learning](/decision-tree-learning/)); it is a greedy heuristic with the guarantees proved below.

## The algorithm

The call ID3$(S, \mathcal{A}, \bot)$ grows the tree, where $\mathcal{A}$ is the set of all attributes.

```pseudo id=main
ID3(S, A, c)                          ▷ examples S, attributes A, default label c
L1  if S is empty then return LEAF(c)
L2  if all examples of S have the same label y then return LEAF(y)
L3  m ← the majority label of S
L4  if A is empty then return LEAF(m)
L5  a* ← the attribute a ∈ A of largest GAIN(S, a)
L6  N ← a node that tests a*, with default label m
L7  for each value u of a* do
L8      child(N, u) ← ID3({(x, y) ∈ S : x[a*] = u}, A − {a*}, m)
L9  return N
```

GAIN$(S, a) = H(S) - \sum_{u \in V_a} \frac{|S_u|}{|S|} H(S_u)$, with $H$ the entropy of the labels in bits and $S_u$ the examples of $S$ with $a = u$. Line L1 handles a value that no example at this node has: the branch gets the parent's majority $m$. Line L4 handles examples that agree on all attributes but differ in label. To predict, follow the branch of each tested value; a value never seen in training goes to the default label of the node.

**Windowing.** Quinlan's ID3 is iterative: for a large training set it grows a tree on a random subset, the *window*, then classifies the other examples, adds some of the misclassified ones to the window, and grows again, until the tree classifies all examples. The name refers to this loop of dichotomizers. The inner step is the procedure above, and the result on consistent data is a tree that fits all of it.

## Example

The 14 Saturday mornings of Quinlan (1986, Table 1), the PlayTennis table of Mitchell (1997, Table 3.2), have attributes outlook (sunny, overcast, rain), temperature (hot, mild, cool), humidity (high, normal) and windy (true, false), and class P (9 days) or N (5 days). So $H(S) = 0.9403$ bits.

| node | examples (P, N) | GAIN of each attribute, bits | chosen |
|---|---|---|---|
| root | (9, 5) | outlook 0.2467, humidity 0.1518, windy 0.0481, temperature 0.0292 | outlook |
| outlook = sunny | (2, 3) | humidity 0.9710, temperature 0.5710, windy 0.0200 | humidity |
| outlook = overcast | (4, 0) | pure | leaf P |
| outlook = rain | (3, 2) | windy 0.9710, temperature 0.0200, humidity 0.0200 | windy |
| sunny, humidity = high | (0, 3) | pure | leaf N |
| sunny, humidity = normal | (2, 0) | pure | leaf P |
| rain, windy = true | (0, 2) | pure | leaf N |
| rain, windy = false | (3, 0) | pure | leaf P |

The result is Quinlan's Figure 2: outlook at the root, humidity under sunny, windy under rain, with 5 leaves and no training error. Temperature is never used. Quinlan and Mitchell print the root gains as 0.246, 0.151, 0.048 and 0.029. The exact gain of outlook is $0.9403 - 0.6935 = 0.2467$ bits; the printed 0.246 comes from subtracting the rounded entropies $0.940 - 0.694$, and the same holds for humidity ($0.940 - 0.789 = 0.151$, exact 0.1518). The choice of each test is the same.

## Correctness

ID3 is a heuristic, so its correctness is a set of invariants, not optimality.

- **Termination and depth.** Each recursive call removes one attribute, so the recursion stops and the tree has depth at most $d$; each path tests an attribute at most once.
- **Greedy choice.** Each internal node tests an attribute of largest gain on the examples that reach it, among the attributes not tested above it.
- **Exact fit.** If no two training examples have the same attribute values and different labels, the tree classifies every training example correctly. The induction step: the examples that reach a child agree on the tested attribute, so they stay consistent on the remaining ones.
- **Windowing.** On consistent data, each round adds a new example to the window, so the loop stops after at most $n$ rounds with a tree that fits all the data.

The full proofs are below.

## Complexity

Costs are on the [real RAM](/real-ram/), with a logarithm counted as one operation.

- **One node.** With $n_t$ examples and $d_t$ attributes left, counting the (value, class) pairs of each attribute takes $O(d_t n_t)$ time, and computing the gains from the counts takes $O(d_t v k)$. Partitioning the examples by $a^*$ takes $O(n_t)$.
- **One level.** The nonempty nodes of one level hold disjoint subsets of the $n$ examples, and an internal node holds at least 2 examples, so a level has at most $n/2$ internal nodes and costs $O(d n + n d v k)$.
- **The tree.** The depth is at most $d$, so the total time is $O(d^2 n v k)$ in the worst case, which is $O(d^2 n)$ for a bounded number of values and classes.
- **Space.** At most $n/2$ internal nodes on each of at most $d$ levels, each with at most $v$ children, so the tree has $O(d n v)$ nodes. The recursion depth is at most $d + 1$.
- **Windowing** multiplies the cost by the number of rounds, at most $n$ on consistent data and usually few.

## Properties

- **Greedy, no backtracking.** A choice at a node is never revised. Mitchell (Section 3.5) calls this a hill-climbing search in the space of trees, which can end in a local optimum.
- **Fits consistent data.** Without pruning, the tree has zero training error whenever that is possible, so it overfits noisy data.
- **Multiway splits.** Each attribute is used at most once on a path, and the tree can fragment the data quickly when attributes have many values.
- **Categorical only.** The original handles numeric attributes only after discretization.
- **Deterministic.** With a fixed tie rule (this page: the first attribute in a fixed order, the smallest label for majority ties), the output is a function of the data.

## Variants and improvements

- **[C4.5](/c4-5/)** (Quinlan 1993) uses the gain ratio with an average-gain filter, binary thresholds on numeric attributes, fractional cases for missing values, and pessimistic error pruning.
- **Stopping on noise.** Quinlan (1986, Section 5) proposed a chi-square test that stops splitting when an attribute looks independent of the class.
- **Post-pruning.** [Reduced-error pruning](/reduced-error-pruning/) (Quinlan 1987) prunes an ID3 tree on a separate data set.
- **Other criteria.** Replacing the gain by the [Gini impurity](/gini-impurity/) decrease changes little; replacing multiway splits by binary ones leads toward [CART](/cart/).
- **Incremental versions.** ID4 and ID5R (Utgoff) update the tree one example at a time.

## When to use it

ID3 is mainly a teaching algorithm: it is the shortest complete tree learner and shows the information-gain idea clearly. Use it on small categorical data where a readable tree that fits the data is the goal. For real data with noise, numeric attributes or missing values, use [C4.5](/c4-5/) or [CART](/cart/) with pruning, or a tree ensemble when accuracy matters most.

## Pitfalls

- **Many-valued attributes.** An attribute such as a record number has the largest possible gain at line L5 and gives a useless tree. Drop such attributes, or use the gain ratio of C4.5.
- **Empty branches.** Line L8 makes a child for every value $u$, also for values that no example at this node has. Without line L1 the code fails or returns no label for them. Pass the majority of the parent, as line L8 does.
- **Values unseen in training.** At prediction time a value may have no branch at all. Use the node's default label, not an error.
- **Rounded gains.** Comparing gains computed from rounded entropies can change a close choice; compute the gain from counts in full precision.
- **No pruning.** The tree that fits the training data exactly is usually too large on noisy data. Prune it on held-out data.

## Implementations

## History

Quinlan (1986, Section 2) places ID3 in the TDIDT family that starts with Hunt's Concept Learning System of the 1960s. ID3 grew out of Quinlan's work on chess endgames in the late 1970s. The 1986 paper in the first issue of Machine Learning gave the algorithm with windowing, the information-based criterion and the PlayTennis example, and discussed noise, unknown values and the bias of the gain toward attributes with many values. Mitchell's textbook (1997, Chapter 3) made the same example the standard first lesson on decision trees.

## References
