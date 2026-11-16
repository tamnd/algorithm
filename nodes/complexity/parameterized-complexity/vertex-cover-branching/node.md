---
tag: XFZWRM
kind: algorithm
slug: vertex-cover-branching
name: Vertex cover branching
aliases:
- bounded search tree for vertex cover
area: complexity/parameterized-complexity
level: intro
summary: "Pick an uncovered edge and branch on its two endpoints, each with budget k - 1. The search tree has at most 2^k leaves, so vertex cover is decided in O(2^k (n + m)) time."
solves: [parameterized-vertex-cover]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the bound on the size of the cover}
  time: {worst: O(2^k (n + m))}
  space: {extra: O(n + m)}
properties: {deterministic: true, exact: true, search_tree_leaves: 2^k, search_tree_depth: k, recursive: true}
history:
  year: 1993
  people: [Jonathan F. Buss, Judy Goldsmith]
  note: The two-way branching on an edge is folklore. Surveys of the field trace the bounded search tree idea for vertex cover to the work of Buss and Goldsmith.
prereqs: [parameterized-vertex-cover, bounded-search-tree]
see_also: [buss-kernel, measure-and-conquer, kernelization, crown-reduction, parameterized-hitting-set, vertex-cover, vertex-cover-2-approximation]
sources:
  - paper: doi:10.1137/0222038
    title: "Jonathan F. Buss and Judy Goldsmith, Nondeterminism within P, SIAM Journal on Computing 22(3), 560-572 (1993)"
    locator: the treatment of vertex cover with a small parameter
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Section 3.1, Vertex Cover (the edge branching and the branching on a vertex of degree at least 3); Section 3.2, How to solve recursive relations
  - book: isbn:9781447155584
    title: Rodney G. Downey and Michael R. Fellows, Fundamentals of Parameterized Complexity, Springer, 2013
    locator: Chapter 3, Bounded Search Trees (Section 3.2, Vertex Cover)
  - book: isbn:9780198566076
    title: Rolf Niedermeier, Invitation to Fixed-Parameter Algorithms, Oxford University Press, 2006
    locator: Chapter 4, Vertex Cover, an illustrative example; Chapter 8, Depth-bounded search trees
  - paper: doi:10.1016/j.tcs.2010.06.026
    title: "Jianer Chen, Iyad A. Kanj and Ge Xia, Improved upper bounds for vertex cover, Theoretical Computer Science 411(40-42), 3736-3756 (2010)"
    locator: the main theorem, O(1.2738^k + kn) time
  - paper: doi:10.4230/LIPIcs.STACS.2024.40
    title: "David G. Harris and N. S. Narayanaswamy, A faster algorithm for vertex cover parameterized by solution size, 41st Symposium on Theoretical Aspects of Computer Science (STACS 2024), LIPIcs 289, 40:1-40:18"
    locator: the main theorem, time O*(1.25284^k)
---

Vertex cover branching decides [p-Vertex-Cover](/parameterized-vertex-cover/), the question whether a graph has a vertex cover of at most $k$ vertices, by a [bounded search tree](/bounded-search-tree/). Every edge $\{u, v\}$ needs $u$ or $v$ in the cover. So the algorithm picks an uncovered edge and tries both choices, each time with one vertex less of budget. The recursion stops when all edges are covered or the budget is used up. The search tree is binary and has depth at most $k$, so it has at most $2^k$ leaves, and each node costs $O(n + m)$ time. This gives $O(2^k (n + m))$ time, which is [fixed-parameter tractable](/fixed-parameter-tractable/): the exponential part depends on $k$ alone. It is the simplest FPT algorithm for vertex cover and the base of the faster ones.

## In plain words

You must put guards on at most $k$ crossings of a road network so that every road has a guard at one of its ends. Take any road with no guard yet. One of its two ends must get a guard. You do not know which one, so try both.

In the first try, put a guard at the first end and solve the rest with one guard fewer. If that fails, try the second end in the same way. Each try uses up one guard, so after at most $k$ choices you run out of guards and stop. The number of tries doubles at each level, so there are at most $2^k$ ways to go down. That number depends only on $k$, not on the size of the network.

## The problem

The input is a graph $G = (V, E)$ with $n$ vertices and $m$ edges, given by an edge list or adjacency lists, and an integer $k \ge 0$. The output is a vertex cover $S \subseteq V$ with $|S| \le k$, if one exists, and NONE otherwise. The decision form is [p-Vertex-Cover](/parameterized-vertex-cover/) with the parameter $k$.

## The algorithm

$G - u$ is the graph without $u$ and the edges at $u$.

```pseudo id=main
VC-BRANCH(G, k)                    ▷ a cover of size at most k, or NONE
L1  if G has no edge then return ∅
L2  if k = 0 then return NONE
L3  pick an edge {u, v} of G
L4  S ← VC-BRANCH(G - u, k - 1);  if S ≠ NONE then return S ∪ {u}
L5  S ← VC-BRANCH(G - v, k - 1);  if S ≠ NONE then return S ∪ {v}
L6  return NONE
```

The implementation does not copy the graph. It keeps the set of chosen vertices, and an edge is uncovered when neither end is chosen. The recursion is replaced by an explicit stack of at most $k$ frames, each holding the index of the branching edge and the side tried last, so a large $k$ cannot overflow the call stack. If line L3 always picks the first uncovered edge in a fixed order, the child can start its scan after the parent's edge, because all earlier edges are already covered.

## Example

Let $G$ have the vertices $a, b, c, d$ and the edges $\{a, b\}$, $\{b, c\}$, $\{c, d\}$, $\{b, d\}$, in this order: a triangle $b, c, d$ with a tail $a$. Line L3 picks the first uncovered edge. With $k = 2$:

| node | chosen | budget | first uncovered edge | action |
|---|---|---|---|---|
| 1 | $\emptyset$ | 2 | $\{a, b\}$ | L4: try $a$ |
| 2 | $\{a\}$ | 1 | $\{b, c\}$ | L4: try $b$ |
| 3 | $\{a, b\}$ | 0 | $\{c, d\}$ | L2: NONE |
| 4 | $\{a, c\}$ | 0 | $\{b, d\}$ | L2: NONE, so node 2 returns NONE at L6 |
| 5 | $\{b\}$ | 1 | $\{c, d\}$ | L4: try $c$ |
| 6 | $\{b, c\}$ | 0 | none | L1: return $\emptyset$ |

The search visits 6 nodes and returns the cover $\{b, c\}$. With $k = 1$ it visits 3 nodes: the root, $\{a\}$ with the uncovered edge $\{b, c\}$, and $\{b\}$ with the uncovered edge $\{c, d\}$. Both children fail at L2, so the answer is NONE. Indeed, the triangle alone needs two vertices.

## Correctness

The proof is by induction on $k$. If $G$ has no edge, $\emptyset$ is a cover. If $G$ has an edge and $k = 0$, no cover of size 0 exists. Otherwise, take the edge $\{u, v\}$ of line L3. Every cover of $G$ contains $u$ or $v$. If a cover $S$ with $|S| \le k$ contains $u$, then $S \setminus \{u\}$ covers $G - u$ with at most $k - 1$ vertices, so by induction line L4 finds a cover; the same holds for $v$ at line L5. Conversely, a cover $S'$ of $G - u$ plus $u$ covers $G$, because the only edges missing from $G - u$ are those at $u$. So the algorithm returns a cover of size at most $k$ exactly when one exists. The full proof is in the proof file of this page.

## Complexity

Each call either stops at L1 or L2 or makes at most two calls with budget $k - 1$. So the search tree is a binary tree of depth at most $k$, with at most $2^k$ leaves and $2^{k+1} - 1$ nodes. Each node finds an uncovered edge in $O(n + m)$ time. The running time follows $T(k) \le 2\,T(k - 1) + O(n + m)$, which gives $O(2^k (n + m))$. The bound is reached: on $k + 1$ disjoint edges every branch fails at depth $k$, and the tree has exactly $2^{k+1} - 1$ nodes.

The extra space is $O(n + m)$ for the graph and the chosen set, plus $O(k)$ for the stack.

The table compares the number of leaves $2^k$ with the bounds of the faster algorithms below, without their polynomial factors.

| $k$ | $2^k$ | $1.4656^k$ | $1.2738^k$ |
|---|---|---|---|
| 10 | 1024 | 46 | 11 |
| 20 | $1.0 \cdot 10^{6}$ | 2090 | 126 |
| 30 | $1.1 \cdot 10^{9}$ | $9.6 \cdot 10^{4}$ | 1422 |
| 40 | $1.1 \cdot 10^{12}$ | $4.4 \cdot 10^{6}$ | $1.6 \cdot 10^{4}$ |

## Properties

- **Exact.** It returns a cover of size at most $k$ whenever one exists. It does not return a least cover unless it is run with $k = 0, 1, 2, \ldots$ in turn.
- **Depth at most k.** Each level adds one vertex to the cover.
- **Polynomial space.** Only the current path of the tree is stored.
- **Order-dependent.** The answer is correct for every choice at L3, but the cover found and the number of nodes depend on it.

## Variants and improvements

- **Degree-3 branching.** Pick a vertex $v$ of largest degree. If $\deg(v) \le 2$, the graph is a union of paths and cycles, and a least cover is found in linear time: every second vertex of each path and cycle. Otherwise branch on "$v$ is in the cover" (budget $k - 1$) or "all of $N(v)$ is in the cover" (budget $k - \deg(v) \le k - 3$). The leaves follow $T(k) \le T(k - 1) + T(k - 3)$, whose root is about $1.4656$, so the time is $O^*(1.4656^k)$, where $O^*$ hides polynomial factors. The implementation of this page includes it.
- **Degree-2 branching.** Branching on $v$ or $N(v)$ for any vertex with $\deg(v) \ge 2$ gives $T(k) \le T(k - 1) + T(k - 2)$ and the golden ratio $1.618$; see [bounded search tree](/bounded-search-tree/).
- **Kernel first.** Run the [Buss kernel](/buss-kernel/) first. The search then runs on a graph with at most $k^2$ edges, and the time is $O(n + m + 2^k k^2)$.
- **Faster bounds.** Chen, Kanj and Xia (2010) gave $O(1.2738^k + kn)$ time with polynomial space. Harris and Narayanaswamy (STACS 2024) improved the base to $1.25284$.
- **Hitting set.** For sets of size $d$, branching on the $d$ elements of an unhit set gives $O^*(d^k)$ for [d-hitting set](/parameterized-hitting-set/).

## When to use it

Use it when the cover is small, say $k$ up to about 30, and when a simple and correct program matters more than speed. Run a kernel first, so that the exponential part runs on a small graph. For larger $k$, use the degree-based branching or a solver that combines many reduction rules with branching. If only an approximate cover is needed, the [2-approximation](/vertex-cover-2-approximation/) runs in linear time.

## Pitfalls

- **Branching on one vertex.** Writing "try $u$ in the cover, else stop" at L4 to L6 is wrong; the right algorithm tries $v$ at L5 when $u$ fails. A star with center $v$ and leaves $u_1, \ldots, u_5$ and $k = 1$ needs $v$.
- **A covered edge at L3.** Picking an edge whose end is already chosen wastes a level of budget on a vertex that is not needed. In the implementation, L3 must skip edges with a chosen end; the right test is that neither end is chosen.
- **Wrong order of the tests.** Testing $k = 0$ at L2 before the empty test at L1 is wrong: the instance $(G, 0)$ with no edge is a yes-instance. L1 must come first.
- **Undoing the wrong vertex.** In an implementation without copies, when L4 fails, remove $u$ from the chosen set before line L5 adds $v$. Leaving $u$ in place makes the second branch use budget $k$ for two vertices.
- **Recursion depth.** A recursive program with depth $k$ fails for large $k$ in languages with a small call stack. Use an explicit stack or bound $k$ by the kernel first.

## Implementations

## History

The branching on the two ends of an edge is the folklore algorithm for vertex cover. Surveys of the field trace the bounded search tree idea to the work of Buss and Goldsmith (1993), who also gave the kernel now named after Buss. Downey and Fellows made bounded search trees a central technique of parameterized complexity in the 1990s, and a long line of work improved the base of the exponent from 2 to $1.2738$ (Chen, Kanj and Xia, 2010) and then to $1.25284$ (Harris and Narayanaswamy, 2024).

## References
