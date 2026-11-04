---
tag: FA43QR
kind: concept
slug: state-space-tree
name: State space tree
aliases:
- backtracking tree
- search tree of partial solutions
area: techniques/backtracking
level: intro
summary: The tree whose nodes are partial solutions and whose leaves are complete candidates.
prereqs: [partial-solution, rooted-tree]
see_also: [generic-backtracking-algorithm, search-tree-pruning, state-space-search, search-tree, branching-factor, depth-first-branch-and-bound, best-first-branch-and-bound]
sources:
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 7, Backtracking (state space tree, problem states, solution states, answer states, live and dead nodes)
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2
    locator: Section 7.2.2, Backtrack programming
  - paper: doi:10.1090/S0025-5718-1975-0373371-6
    title: Donald E. Knuth, Estimating the efficiency of backtrack programs, Mathematics of Computation 29(129), 1975
    locator: pp. 122 to 136
---

The state space tree of a search problem is the [rooted tree](/rooted-tree/) whose root is the empty [partial solution](/partial-solution/), whose children of a node are the partial solutions with one more decision, and whose leaves are complete candidates or dead ends. [Backtracking](/generic-backtracking-algorithm/) and branch and bound are traversals of this tree, and their running time is the number of tree nodes they visit times the work per node. The tree is almost never built in memory: the search generates each node from its parent when it needs it.

## In plain words

Think of a problem as a row of decisions: which column for the first queen, which column for the second, and so on. Draw the start, with no decision made, at the top. Below it, draw one branch for each possible first decision. Below each of those, draw one branch for each possible second decision, and so on. Each path from the top to the bottom is one complete way to make all the decisions.

This drawing is the state space tree. A search walks through it. The tree has a fixed shape for the problem, but a search does not need to walk all of it: when a point in the tree shows that no good answer is below it, the search skips that whole part.

## The idea

Fix a problem whose candidates are sequences of decisions $x_1, x_2, \ldots$, with a set $D_{k+1}(x_1 \ldots x_k)$ of allowed next decisions for each prefix. The state space tree $\mathcal{T}$ has:

- one node for each sequence $x_1 \ldots x_k$ with $x_j \in D_j(x_1 \ldots x_{j-1})$ for each $j \le k$, including the empty sequence at the root;
- an edge from $x_1 \ldots x_k$ to $x_1 \ldots x_k x_{k+1}$ for each $x_{k+1} \in D_{k+1}(x_1 \ldots x_k)$.

The depth of a node is the number of decisions it fixes. The children of a node are ordered by the order of $D_{k+1}$. A preorder walk of $\mathcal{T}$ visits the sequences in lexicographic order.

Horowitz and Sahni name the nodes by their role. Each node is a *problem state*. A node that stands for a complete candidate is a *solution state*, and a solution state that satisfies all the constraints is an *answer state*. During a search, a node that has been generated but whose children are not all generated is *live*; the node whose children are being generated is the *E-node*; a node that is fully expanded or cut off is *dead*.

Three trees should be kept apart.

1. **The full tree** $\mathcal{T}$: all prefixes allowed by the domains.
2. **The pruned tree** $\mathcal{T}_P$: the prefixes $x_1 \ldots x_k$ such that the test $P_j(x_1 \ldots x_j)$ holds for each $j \le k$. When the tests are prefix-closed, this is a subtree of $\mathcal{T}$ that contains the root, and [backtracking](/generic-backtracking-algorithm/) visits exactly its nodes.
3. **The tree a branch-and-bound run visits**: a subtree of $\mathcal{T}_P$ that also depends on the incumbent values found during the run, so on the order of the search.

The same problem has several state space trees, one for each way to write a candidate as a sequence of decisions. The choice changes the size of the tree, not the set of solutions.

**Fixed-tuple and variable-tuple trees.** For the subsets of $\{1, \ldots, n\}$, a *fixed-tuple* tree decides $x_i \in \{0, 1\}$ for item $i$ at depth $i$. It is a complete binary tree with $2^{n+1} - 1$ nodes, and its $2^n$ leaves are the subsets. A *variable-tuple* tree writes a subset as its increasing list of items $i_1 < i_2 < \cdots < i_k$. Each node is a subset, and the children of $i_1 \ldots i_k$ add one item larger than $i_k$. This tree has exactly $2^n$ nodes, and each node, not only each leaf, is a candidate.

**Trees and graphs.** Two different nodes of the tree can stand for the same state of the problem. In a search for a tour of cities, the partial paths $1, 2, 3$ and $1, 3, 2$ have visited the same set and end at different cities, while $1, 2, 3, 4$ and $1, 3, 2, 4$ have visited the same set and end at the same city: what remains to be done is the same. A [state space search](/state-space-search/) on the graph of states merges such nodes; the tree keeps them apart. Merging them is the step from backtracking to [memoization](/memoization/), as in the [Held-Karp algorithm](/held-karp-algorithm/).

## Examples

### Queens

For $n$ queens with one queen in each row, $x_k$ is the column of the queen in row $k$. Three formulations give three trees:

- columns from $\{1, \ldots, n\}$ with no test: the full tree has $\sum_{k=0}^{n} n^k$ nodes;
- columns that are not used yet: a permutation tree with $\sum_{k=0}^{n} n!/(n-k)!$ nodes;
- the tree pruned by the test "the new queen attacks no earlier queen".

| $n$ | full tree | permutation tree | pruned tree | solutions |
|---|---|---|---|---|
| 4 | 341 | 65 | 17 | 2 |
| 5 | 3906 | 326 | 54 | 10 |
| 6 | 55987 | 1957 | 153 | 4 |
| 7 | 960800 | 13700 | 552 | 40 |
| 8 | 19173961 | 109601 | 2057 | 92 |

For $n = 4$ the pruned tree has 1, 4, 6, 4 and 2 nodes at depths 0 to 4. Its two leaves at depth 4 are the solutions $(2, 4, 1, 3)$ and $(3, 1, 4, 2)$. The other leaves are dead ends at depth 2 or 3. For example, the node $(1, 3)$ has no child, because each column of row 3 is attacked by the queen at column 1 or the queen at column 3.

### Subset sum

Take the items $3, 5, 6, 7$, in this order, and the target 15. The fixed-tuple tree has 31 nodes. The only subset with sum 15 is $\{3, 5, 7\}$.

- With the test "the chosen items sum to at most 15", the pruned tree keeps 28 nodes: 1, 2, 4, 8 and 13 at depths 0 to 4. The test cuts only 3 leaves.
- With the second test "the chosen sum plus the sum of the items not yet decided is at least 15", the pruned tree keeps 11 nodes: 1, 2, 3, 4 and 1 at depths 0 to 4. Its only leaf is the solution.

The second test does not change the full tree or the solutions. It changes only the pruned tree, which is the tree that the search pays for.

### Estimating the size

The size of the pruned tree decides the running time, and it is hard to predict. Knuth (1975) estimates it from random root-to-leaf paths: if the nodes on a random path have $c_0, c_1, \ldots$ children, and each child is picked with equal probability, then $1 + c_0 + c_0 c_1 + \cdots$ has expected value equal to the number of nodes. The [generic backtracking algorithm](/generic-backtracking-algorithm/) page proves this.

## Where it is used

The state space tree is the object behind each algorithm of this area. [Backtracking](/generic-backtracking-algorithm/) walks it depth first and cuts it with feasibility tests, which is [search tree pruning](/search-tree-pruning/). Branch and bound walks it in an order given by a [node selection rule](/node-selection-rule/): [depth-first](/depth-first-branch-and-bound/), [breadth-first](/breadth-first-branch-and-bound/) or [best-first](/best-first-branch-and-bound/), and cuts it with a [bounding function](/bounding-function/). A [game tree](/game-tree/) is a state space tree with two players, cut by [alpha-beta pruning](/alpha-beta-pruning/). The [branching factor](/branching-factor/) and the depth bound the size of the full tree, and [variable ordering heuristics](/variable-ordering-heuristics/) change the shape of the pruned tree.

## References
