---
tag: CDFW0E
kind: concept
slug: search-tree
name: Search tree
aliases:
- state tree
- game tree
area: techniques/search-strategies
level: intro
summary: The tree of paths unfolded from the start state of a search, with repeated states kept as separate nodes.
prereqs: [state-space, rooted-tree]
see_also: [search-strategy, search-frontier, graph-search-vs-tree-search, state-space-tree, game-tree, branching-factor, effective-branching-factor, geometric-series]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.3 (search trees, nodes versus states, expansion, and redundant paths) and Section 3.4.1 (the count of nodes of a uniform tree)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 1 (state-space graphs and the trees that search explores)
  - paper: doi:10.1016/0004-3702(85)90084-0
    title: Richard E. Korf, Depth-first iterative-deepening, an optimal admissible tree search, Artificial Intelligence 27(1) (1985)
    locator: pp. 97 to 109 (the uniform tree of branching factor b and depth d as the model of the analysis)
---

A search tree is the rooted tree whose nodes are the paths that a [state-space search](/state-space-search/) can follow from the start state. The root is the empty path at the start state, and the children of a node are the paths one action longer. A state that can be reached by several paths appears in several nodes, so the search tree can be much larger than the [state space](/state-space/), and it is infinite when the space has a cycle. Each [search strategy](/search-strategy/) is an order in which to visit this tree.

## In plain words

Write down every way to walk from the start. Each walk is a separate entry, even when two walks end at the same place. Put the walks in a family tree: the empty walk is the root, and each walk has a child for each way to take one more step.

This is the search tree. A search program builds a part of it. The entries that the program has finished with are inside the part, and the entries that wait to be looked at are on its edge.

Places that you can reach in several ways appear many times in the tree. So the tree can be very large even when there are few places. If you can walk in a circle, the tree never ends.

## The idea

### Definition

Let a search problem have the initial state $s_0$, a finite set of actions $\mathrm{ACTIONS}(s)$ for each state $s$, the transition model $\mathrm{RESULT}(s, a)$ and action costs $c(s, a, s') \ge 0$. The search tree $T$ is the rooted tree with these nodes and edges.

- The root is a node with state $s_0$, no parent, path cost $g = 0$ and depth $0$.
- A node $n$ with state $s$ has one child $n_a$ for each $a \in \mathrm{ACTIONS}(s)$. The child has state $s' = \mathrm{RESULT}(s, a)$, parent $n$, action $a$, path cost $g(n_a) = g(n) + c(s, a, s')$ and depth one more than $n$.

A node is the same thing as a path from $s_0$: follow the parent pointers to the root and read the actions in reverse. So the nodes of $T$ and the action sequences that can be done from $s_0$ are in one-to-one correspondence. The map from a node to its state is onto the states that can be reached from $s_0$, but it is not one-to-one when a state has two paths.

### Nodes are not states

A *state* is a configuration of the problem, for example a position of a puzzle. A *node* is a record of the search: a state, a parent, an action, a cost and a depth. Two nodes with the same state differ in their path and often in their cost. This difference is the base of the comparison [graph search versus tree search](/graph-search-vs-tree-search/). Tree-like search treats each node as new. Graph search keeps one node, or one cheapest node, for each state, so it walks a subtree of $T$ that has at most one node per state.

### The partial search tree

A search never builds all of $T$. At each moment it holds a partial tree. Its interior nodes are the nodes already expanded, and the leaves that wait to be expanded are the [frontier](/search-frontier/). Each path from the root to an unexplored node of $T$ passes through a frontier node. This is the *separation property* of the frontier, and it is why the frontier is enough to continue the search.

### Size

The *branching factor* $b$ is the largest number of children of a node. If each node at depth less than $d$ has exactly $b$ children, the tree has $b^i$ nodes at depth $i$, and up to depth $d$ it has

$$ N(b, d) = \sum_{i=0}^{d} b^i = \frac{b^{d+1} - 1}{b - 1} \qquad (b \ge 2) $$

nodes. This is a [geometric series](/geometric-series/): multiply the sum by $b$ and subtract the sum, which leaves $b^{d+1} - 1$. The last level has $b^d$ nodes, which is more than $(b - 1)/b$ of the total. So in a uniform tree most nodes are at the deepest level. Iterative deepening relies on this fact: running the search again on the upper levels costs a fraction of the total, a constant factor of at most $b/(b-1)$, see [iterative deepening search](/iterative-deepening-search/).

| $b$ | $N(b, 2)$ | $N(b, 5)$ | $N(b, 10)$ |
| --- | --- | --- | --- |
| 2 | 7 | 63 | 2,047 |
| 3 | 13 | 364 | 88,573 |
| 10 | 111 | 111,111 | 11,111,111,111 |

Real trees are not uniform. The [effective branching factor](/effective-branching-factor/) is the $b^*$ for which a uniform tree of the depth of the solution has as many nodes as the search generated.

### Finite and infinite trees

Let the branching factor be finite. Then each level of $T$ is finite, so $T$ is infinite if and only if it has nodes at every depth. By König's lemma, this holds if and only if $T$ has an infinite path, that is, an infinite sequence of actions from $s_0$. A finite state space with a cycle that can be reached from $s_0$ has an infinite path, so its tree is infinite. A state space that is a finite directed acyclic graph has a finite tree, but the tree can still have exponentially many nodes in the number of states.

## Examples

### A small graph and its tree

The graph has states S, A, B, C, D, G and the directed edges S→A 1, S→G 12, A→B 4, A→C 1, B→D 3, C→D 1, C→G 2, D→G 3. It has no cycle, so its search tree is finite. The tree has 10 nodes, one for each path from S:

| depth | nodes, as paths, with path cost |
| --- | --- |
| 0 | S:0 |
| 1 | S-A:1, S-G:12 |
| 2 | S-A-B:5, S-A-C:2 |
| 3 | S-A-B-D:8, S-A-C-D:3, S-A-C-G:4 |
| 4 | S-A-B-D-G:11, S-A-C-D-G:6 |

The 6 states give 10 nodes. The state G is in 4 nodes with 4 different costs, and D is in 2 nodes. A tree-like search can expand D twice. A graph search expands D at most once.

### A grid, where the tree explodes

A robot walks on the integer grid with the four moves up, down, left and right, from $(0, 0)$. The cells at distance at most $d$ in moves are the $(x, y)$ with $|x| + |y| \le d$. For a fixed $x$ with $|x| \le d$, there are $2(d - |x|) + 1$ values of $y$, and the sum over $x$ is $2d^2 + 2d + 1$. The search tree has $4^i$ nodes at depth $i$, one for each sequence of moves.

| depth $d$ | cells at distance at most $d$ | tree nodes at depth $d$ | tree nodes up to depth $d$ |
| --- | --- | --- | --- |
| 1 | 5 | 4 | 5 |
| 5 | 61 | 1,024 | 1,365 |
| 10 | 221 | 1,048,576 | 1,398,101 |

At depth 10 there are 221 cells but more than a million nodes. A tree-like search that does not undo its last move still has $4 \cdot 3^{d-1}$ nodes at depth $d \ge 1$, which is 78,732 at depth 10. Only graph search, or [duplicate detection](/duplicate-detection/) of another kind, brings the work down to the number of cells.

### A cycle, where the tree is infinite

Two states $u$ and $v$ with the actions $u \to v$ and $v \to u$ give the infinite search tree $u, uv, uvu, uvuv, \ldots$, a single infinite path. A [depth-first](/depth-first-search/) tree-like search from $u$ for a goal that cannot be reached never stops on it. [Depth-limited search](/depth-limited-search/) cuts the tree at a fixed depth and so always stops.

## Where it is used

The search tree is the object that the analysis of each uninformed strategy counts: the bounds $O(b^d)$ and $O(bm)$ of the [search strategy](/search-strategy/) table are counts of its nodes. [Backtracking](/generic-backtracking-algorithm/) walks the [state-space tree](/state-space-tree/) of partial solutions, which is a search tree whose states are partial assignments. In two-player games, the [game tree](/game-tree/) is the search tree of the positions, and [minimax](/minimax/) evaluates it from the leaves up. The difference between the tree and the graph of states is the subject of [graph search versus tree search](/graph-search-vs-tree-search/), and the frontier of a partial tree is the [search frontier](/search-frontier/).

## References
