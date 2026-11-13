---
tag: AEGQ05
kind: algorithm
slug: pebble-game-rigidity
name: Pebble game for rigidity
aliases:
- Jacobs-Hendrickson pebble game
area: cad/geometric-constraint-solving
level: advanced
summary: Jacobs and Hendrickson's O(n^2) algorithm that tests Laman's condition by moving two pebbles per vertex along edges, and finds rigid components and redundant edges.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1997
  people: [Donald J. Jacobs, Bruce Hendrickson]
  note: Jacobs and Hendrickson published the pebble game in 1997 as a fast exact test of the Laman counts, for the rigidity analysis of large networks such as models of glass, and Lee and Streinu extended it to all (k, l) counts in 2008.
prereqs: [laman-theorem, generic-rigidity, depth-first-search]
see_also: [laman-theorem, henneberg-construction, maxwell-counting-rule, generic-rigidity, tay-theorem, degrees-of-freedom-analysis, matroid-greedy-algorithm, red-blue-pebble-game]
sources:
  - paper: doi:10.1006/jcph.1997.5809
    title: Donald J. Jacobs and Bruce Hendrickson, An algorithm for two-dimensional rigidity percolation, the pebble game, Journal of Computational Physics 137(2), 346 to 365, 1997
    locator: the pebble game for the Laman counts, the search for free pebbles, the rigid cluster decomposition, and the quadratic worst case bound
  - paper: doi:10.1016/j.disc.2007.07.104
    title: Audrey Lee and Ileana Streinu, Pebble game algorithms and sparse graphs, Discrete Mathematics 308(8), 1425 to 1437, 2008
    locator: the (k, l) pebble games, the proof that they accept exactly the (k, l)-sparse graphs, and the detection of components
  - paper: doi:10.1007/BF01534980
    title: G. Laman, On graphs and rigidity of plane skeletal structures, Journal of Engineering Mathematics 4(4), 331 to 340, 1970
    locator: the counts that the pebble game tests
  - paper: doi:10.1137/0221008
    title: Bruce Hendrickson, Conditions for unique graph realizations, SIAM Journal on Computing 21(1), 65 to 84, 1992
    locator: the earlier matching-based test of the Laman counts and of redundant rigidity
  - book: isbn:9780821838013
    title: Jack Graver, Brigitte Servatius and Herman Servatius, Combinatorial Rigidity, Graduate Studies in Mathematics 2, American Mathematical Society, 1993
    locator: Chapter 4, Linear and Planar Rigidity (the generic rigidity matroid in the plane)
---

The pebble game of Jacobs and Hendrickson decides the [Laman](/laman-theorem/) counts of a graph, and so [generic rigidity](/generic-rigidity/) in the plane, without any coordinates and without looking at the exponentially many vertex subsets. Each vertex holds two pebbles, and an edge is accepted when four pebbles can be brought to its two ends by moving pebbles back along accepted edges. The accepted edges form a largest set of independent bars, the rejected edges are redundant, and a second pass finds the rigid components. On a graph with $n$ vertices and $m$ edges it takes $O(nm)$ time, and $O(n^2)$ for the Laman test of a graph with $2n - 3$ edges.

## In plain words

Give every joint of a structure two tokens. A token stands for one way in which the joint can still move. When a new rod arrives between two joints, it can only take away a way of moving if the two joints, together, still have four free tokens: three of the four are the ways the pair can move as a whole, and only the fourth can be used up. If they do, one token is put on the rod. If they do not, the rod adds nothing new, and it is redundant.

The tokens can be moved. A joint can take a token from a neighbor if it hands its own token to the rod between them in return. So the search for four tokens is a search along the rods. In the end, the rods that got a token are the useful ones.

## The problem

The input is a graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$ and a list of $m$ edges $uv$ with $u \ne v$, in a fixed order. A repeated edge is allowed. The outputs are:

- for each edge, whether it is *independent* of the earlier accepted edges or *redundant*, where a set $F$ of edges is independent when every set $X$ of $k \ge 2$ vertices spans at most $2k - 3$ edges of $F$;
- the rank, the number of accepted edges, and from it the answers to "is $G$ generically rigid in the plane" (rank $2n - 3$) and "is $G$ a Laman graph" ($m = 2n - 3$ and every edge accepted);
- the *rigid components*: the maximal vertex sets $X$ with $|X| \ge 2$ whose induced subgraph is generically rigid in the plane. Each edge lies in exactly one of them.

By [Laman's theorem](/laman-theorem/), the independent sets are exactly the edge sets whose rows in the rigidity matrix are independent at a generic placement, so they are the independent sets of a [matroid](/matroid/), and the accepted edges are what the [matroid greedy algorithm](/matroid-greedy-algorithm/) keeps.

## The algorithm

The state is a directed graph $D$ on $V$, one arc for each accepted edge, and a count $\mathrm{peb}[v]$ of free pebbles at each vertex. An arc $u \to v$ means that a pebble of $u$ covers the edge $uv$, so $\mathrm{peb}[v] + \mathrm{outdeg}_D(v) = 2$ at all times.

```pseudo id=main
PEBBLE-GAME(n, E)
L1  for each vertex v do peb[v] ← 2;  D ← the directed graph on V with no arcs
L2  for each edge uv of E, in the given order do
L3      for (x, y) in ((u, v), (v, u)) do
L4          while peb[x] < 2 and FIND-PEBBLE(x, y) succeeds do nothing more
L5      if peb[u] + peb[v] = 4 then
L6          peb[u] ← peb[u] - 1;  add the arc u → v to D;  mark uv independent
L7      else mark uv redundant
L8  return the marks and D
FIND-PEBBLE(x, y)
L9  search D by depth-first search from x for a vertex w ∉ {x, y} with peb[w] > 0
L10 if there is no such w then return false
L11 reverse every arc of the path from x to w;  peb[w] ← peb[w] - 1;  peb[x] ← peb[x] + 1
L12 return true
RIGID-COMPONENTS(n, E)
L13 run PEBBLE-GAME(n, E);  C ← an empty list
L14 for each edge uv of E such that no set in C contains both u and v do
L15     gather pebbles on u and v as in lines L3 and L4, but stop at 3 in total
L16     X ← the vertices from which D reaches some w ∉ {u, v} with peb[w] > 0
L17     add V ∖ X to C
L18 return C
```

The search in line L9 may pass through $y$ but must not take a pebble from it, because $y$ needs its pebbles too. Reversing a path in line L11 moves one pebble from $w$ to $x$: every inner vertex of the path loses one out-arc and gains one, so its count stays. Every out-degree is at most 2, so the search is cheap.

## Example

Take $n = 6$ and the edges in the order $01, 02, 12, 13, 23, 03, 34, 45, 35, 25$: a $K_4$ on $\{0, 1, 2, 3\}$, a triangle $345$ that shares vertex 3 with it, and the edge $25$. The column "moves" lists the successful searches, written $x \leftarrow w$ when $x$ takes a pebble from $w$.

| step | edge | moves | result | free pebbles on $0, 1, 2, 3, 4, 5$ after |
| --- | --- | --- | --- | --- |
| 1 | $01$ | none | accept, arc $0 \to 1$ | 1, 2, 2, 2, 2, 2 |
| 2 | $02$ | $0 \leftarrow 1$ | accept, arc $0 \to 2$ | 1, 1, 2, 2, 2, 2 |
| 3 | $12$ | $1 \leftarrow 0$ | accept, arc $1 \to 2$ | 0, 1, 2, 2, 2, 2 |
| 4 | $13$ | $1 \leftarrow 2$ | accept, arc $1 \to 3$ | 0, 1, 1, 2, 2, 2 |
| 5 | $23$ | $2 \leftarrow 1$ | accept, arc $2 \to 3$ | 0, 0, 1, 2, 2, 2 |
| 6 | $03$ | $0 \leftarrow 2$, then the search from 0 fails | redundant: only 3 pebbles | 1, 0, 0, 2, 2, 2 |
| 7 | $34$ | none | accept, arc $3 \to 4$ | 1, 0, 0, 1, 2, 2 |
| 8 | $45$ | none | accept, arc $4 \to 5$ | 1, 0, 0, 1, 1, 2 |
| 9 | $35$ | $3 \leftarrow 4$ | accept, arc $3 \to 5$ | 1, 0, 0, 1, 0, 2 |
| 10 | $25$ | $2 \leftarrow 3$, $2 \leftarrow 0$ | accept, arc $2 \to 5$ | 0, 0, 1, 0, 0, 2 |

In step 6, after $0 \leftarrow 2$, the vertices that 0 can reach are $0, 1, 2, 3$, and the only free pebbles among them are the one on 0 and the two on 3. So the set $\{0, 1, 2, 3\}$ already spans $2 \cdot 4 - 3 = 5$ accepted edges, and $03$ would be a sixth. After step 9 the rank is 8 $< 9$, and RIGID-COMPONENTS returns $\{0, 1, 2, 3\}$ and $\{3, 4, 5\}$: two rigid bodies joined at a hinge. Step 10 adds the ninth independent edge, the rank becomes $9 = 2n - 3$, and the whole graph is one rigid component. At the end $12 - 9 = 3$ free pebbles remain, the three motions of the plane.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Invariant.** At every step $\mathrm{peb}[v] \ge 0$ and $\mathrm{peb}[v] + \mathrm{outdeg}_D(v) = 2$. So for every vertex set $X$, $2|X| = \mathrm{peb}(X) + i_B(X) + \mathrm{out}(X)$, where $B$ is the set of accepted edges, $i_B(X)$ the number of them inside $X$, and $\mathrm{out}(X)$ the number of arcs that leave $X$.
- **Accepted edges are independent.** Four pebbles on $u$ and $v$ mean $i_B(X) \le 2|X| - 4$ for every $X \ni u, v$, so adding $uv$ keeps the count $2|X| - 3$.
- **Rejected edges are dependent.** If fewer than four pebbles can be gathered, the vertices reachable from the failed search form a set $R \ni u, v$ with no arc leaving it and no free pebble except on $u$ and $v$. The identity gives $i_B(R) \ge 2|R| - 3$, so $uv$ would break the count on $R$.
- **Greedy basis.** Hence an edge is accepted exactly when it is independent of the edges accepted before it, which is the greedy algorithm in the planar rigidity matroid. The number of accepted edges is the rank.
- **Components.** After three pebbles are gathered on an edge $uv$, the vertices that cannot reach any other free pebble form a closed set with exactly 3 free pebbles, so it spans $2|S| - 3$ accepted edges and is rigid, and the largest rigid set that contains $u$ and $v$ has the same two properties, so the two sets are equal.

## Complexity

- **One search.** $D$ has at most $2n - 3$ arcs, because the accepted edges satisfy the count on $X = V$, and every out-degree is at most 2. So a depth-first search in line L9 and the reversal in line L11 take $O(n)$ time.
- **One edge.** Lines L3 and L4 make at most four successful searches, one per missing pebble, and at most two failed ones. So each edge costs $O(n)$, and PEBBLE-GAME takes $O(nm)$ time. When no search is needed, as for a forest, each edge costs $O(1)$, so the best case is $\Theta(n + m)$.
- **Laman test.** A Laman graph has $m = 2n - 3$, and the test can stop at the first redundant edge, so it takes $O(n^2)$ time. This is the bound of Jacobs and Hendrickson.
- **Components.** Each component holds at least one accepted edge and two components share no edge, so there are at most $2n - 3$ of them. Each one costs $O(n)$ for the gathering and the backward search in line L16. The membership test of line L14 costs $O(n)$ per edge. So RIGID-COMPONENTS also takes $O(nm)$ time. Lee and Streinu keep the components during the game and get $O(n^2)$ for all of them.
- **Space.** $D$, the counts and the marks take $\Theta(n + m)$ space.

## Properties

- **Exact and combinatorial.** The game uses only the graph. It decides generic rigidity, so it says nothing about a particular placement: at special positions, such as $K_{3,3}$ on a conic, a graph that the game calls rigid gives an infinitesimally flexible framework.
- **Order dependent output, order independent rank.** Which edges are marked redundant depends on the order, but their number does not, and neither do the rigid components.
- **Incremental.** Edges can be added one at a time, and the state after each edge is a valid certificate: the orientation $D$ shows the count, and the free pebbles count the degrees of freedom, $2n - \mathrm{rank}$.
- **Deterministic.** With a fixed order of the arcs in each adjacency list, the moves are fixed, as in the trace above.
- **The count matroid in general.** The same game with $k$ pebbles per vertex and acceptance at $\ell + 1$ pebbles decides the $(k, \ell)$ counts for $0 \le \ell < 2k$ (Lee and Streinu). The case $(1, 1)$ is the [graphic matroid](/graphic-matroid/), and $(2, 3)$ is the planar rigidity matroid.

## Variants and improvements

- **$(k, \ell)$ pebble games.** Lee and Streinu (2008) gave the general game and proved that it accepts exactly the $(k, \ell)$-sparse graphs. For $k = 6$ and $\ell = 6$ it tests the body-and-bar counts of [Tay's theorem](/tay-theorem/) in space.
- **Components during the game.** Instead of a second pass, keep the components as the edges arrive. A new edge inside a known component is redundant at once, which saves the search.
- **Rigidity percolation and proteins.** Jacobs and Hendrickson designed the game for networks with millions of sites, in models of glass, and Jacobs, Rader, Kuhn and Thorpe used a version for bond-bending networks in the program FIRST, which finds the rigid and flexible regions of proteins.
- **Other exact tests.** Hendrickson (1992) tested the Laman counts by bipartite matching on doubled edges, and the two spanning tree form of Laman's theorem gives a test by [spanning tree packing](/spanning-tree-packing/). Algorithms based on matroid sums by Gabow and Westermann are faster in theory.
- **Randomized rank.** For any dimension, the rank of the rigidity matrix at a random integer placement gives the generic rank with high probability. It is slower, $O(m n^2)$ by elimination, but it works in space, where no count test is known.

## When to use it

- To decide whether a sketch of points and distances is well-constrained in the generic sense, and to find over-constrained edges, in CAD [degrees of freedom analysis](/degrees-of-freedom-analysis/).
- To design a rigid formation or a sensor network in the plane, and to see which links are redundant.
- To find rigid clusters in large planar networks, where computing ranks of large matrices would be too slow.

Do not use it for bar-and-joint frameworks in three dimensions: the $(3, 6)$ count is not sufficient there, as the double banana shows, and $(3, 6)$ is not even a matroid count for the game ($\ell = 6 = 2k$). Do not use it to check a particular placement: compute the rank of the rigidity matrix at the given coordinates instead.

## Pitfalls

- **Taking the partner's pebble.** The search from $u$ must not take a free pebble from $v$, or the four pebbles are counted twice. It may still pass through $v$.
- **Blocking the partner.** Treating $v$ as a wall in the search from $u$ is wrong in the other direction: a path through $v$ to a free pebble is a legal move and may be the only one.
- **Three or four.** An edge needs four pebbles to be accepted. Three pebbles is the test for components. Mixing the two gives either too many or too few accepted edges.
- **Repeated edges.** A second copy of an accepted edge is redundant, because the pair already spans $1 = 2 \cdot 2 - 3$ edges. Code that drops duplicates silently changes the counts of a multigraph.
- **Testing a vertex set by its accepted edges.** The accepted edges inside a vertex set $X$ can be fewer than the rank of $G[X]$, because an edge inside $X$ can be rejected through a circuit that leaves $X$. For a rigid component the count is exact, but to test an arbitrary set, run a new game on $G[X]$.
- **Recursion.** A recursive search can be $n$ deep on a long path. Use an explicit stack, as the implementation does.

## Implementations

## History

Rigidity percolation, the study of when a random network becomes rigid, needed a fast exact test of the Laman counts on very large graphs. Hendrickson (1992) had given a polynomial test by bipartite matching. Jacobs and Thorpe used a pebble game for rigidity percolation in 1995, and in 1997 Jacobs and Hendrickson published the full algorithm, with its proof, the rigid cluster decomposition and a quadratic worst case. It later became the core of the FIRST program for proteins. Lee and Streinu (2008) generalized it to all $(k, \ell)$ counts with $0 \le \ell < 2k$, proved the equivalence with sparsity in this setting, and gave the component algorithms. The pebble game of rigidity is not related to the [red-blue pebble game](/red-blue-pebble-game/) of I/O complexity.

## References
