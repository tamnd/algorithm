---
tag: 6F205G
kind: algorithm
slug: edmonds-blossom
name: Edmonds' blossom algorithm
aliases:
- Edmonds matching algorithm
- blossom algorithm
area: graphs/matching
level: advanced
summary: Finds maximum matchings in general graphs by contracting blossoms during augmenting-path search.
solves: [maximum-matching]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n^3)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1965
  people: [Jack Edmonds]
  note: Edmonds gave the first polynomial-time algorithm for maximum matching in general graphs in Paths, trees, and flowers (1965), together with the case for polynomial time as the measure of a good algorithm.
prereqs: [blossom, berge-lemma]
see_also: [micali-vazirani-algorithm, hopcroft-karp, kuhn-algorithm, tutte-berge-formula, gallai-edmonds-decomposition, maximum-weight-matching, minimum-weight-perfect-matching, disjoint-set-forest]
sources:
  - paper: doi:10.4153/CJM-1965-045-4
    title: Jack Edmonds, Paths, trees, and flowers, Canadian Journal of Mathematics 17, 449 to 467 (1965)
    locator: the whole paper (the alternating forest, the shrinking of blossoms, and the proof of maximality)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.3, Matchings in general graphs (Edmonds' blossom algorithm)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Section 24.2, Cardinality matching algorithm, Section 24.2a, An O(n^3) algorithm, and Section 24.4a, Complexity survey for cardinality nonbipartite matching
---

Edmonds' blossom algorithm finds a [maximum matching](/maximum-matching/) in any [graph](/graph/), bipartite or not. Like the bipartite methods it repeatedly finds an [augmenting path](/augmenting-path/) and flips it, but it grows its search forest in a way that copes with odd cycles: when the search closes an odd alternating cycle, a [blossom](/blossom/), it contracts the cycle to a single vertex and goes on in the smaller graph. It was the first polynomial-time algorithm for the problem, and the version here runs in $O(n^3)$ time. The graph is general and unweighted; the weighted version, with dual variables on blossoms, solves [maximum weight matching](/maximum-weight-matching/).

## In plain words

To make a matching bigger, find a chain that starts and ends at unpaired vertices and switches between unused and used edges, then switch every edge on it. In a graph with two sides, a search can tell for each vertex whether a chain arrives on an unused or a used edge, and visit each vertex once.

An odd ring of vertices spoils this, because going round one way or the other way gives different answers. Edmonds' idea is to squeeze such a ring into a single point as soon as the search finds it, and keep searching. When a chain is found that passes through a squeezed point, the ring is unfolded, and the chain goes round it on the side that keeps the switching pattern. Each search either makes the matching bigger or proves that it is already the biggest.

## The problem

The input is an undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges. The output is a matching $M$, a set of edges with no common end, of largest size $\nu(G)$, given as an array $\text{mate}$ with $\text{mate}[v] = \text{NIL}$ for a free vertex.

**Assumptions.** The graph need not be bipartite, connected, or simple: self-loops are ignored and parallel edges act as one. It is unweighted. For bipartite graphs [Hopcroft-Karp](/hopcroft-karp/) is simpler and faster.

## The algorithm

The algorithm runs in phases. A phase grows an *alternating forest* $F$ with one tree per free vertex: each free vertex is an *outer* root; from an outer vertex the search follows an unmatched edge to a new vertex, which becomes *inner*, and then its matched edge to its partner, which becomes outer. It works in a graph $G'$ in which some blossoms have been contracted, given by an array $\text{base}$ that maps each vertex of $G$ to the vertex of $G'$ containing it.

```pseudo id=main
EDMONDS(G)
L1  M ← ∅
L2  repeat   ▷ one phase
L3      G' ← G;  M' ← M;  each free vertex is an outer root of its own tree;  Q ← the free vertices
L4      while Q is not empty do v ← DEQUEUE(Q)
L5          for each edge vw of G at v do
L6              if v and w lie in one vertex of G', or vw ∈ M, then skip w
L7              if w is outer and lies in another tree than v then
L8                  P' ← the tree path from the root of v to v, the edge vw, the tree path from w to its root;  P ← P' with each contracted blossom expanded;  M ← M △ P;  start the next phase
L9              else if w is outer then   ▷ vw closes a blossom B in the tree of v and w
L10                 contract B in G' and M' to one outer vertex;  ENQUEUE every vertex of B that was inner
L11             else if w is in no tree then w becomes inner, with parent v;  mate(w) becomes outer in the tree of v;  ENQUEUE(Q, mate(w))
L12 until a phase ends without augmenting;  return M
```

Line L6 skips edges inside a contracted blossom and the matched edge back to the parent. An edge from an outer vertex to an inner vertex is skipped too, by falling through all tests. Line L8 joins two trees through an unmatched edge between outer vertices, which gives an augmenting path in $G'$; expanding a blossom $B$ on it replaces the contracted vertex by the way round $B$ that has even length, as on the [blossom](/blossom/) page, so the result is an augmenting path in $G$. Line L10 contracts a blossom: its base is the lowest common ancestor of $v$ and $w$ in the tree, and all its vertices become outer, so the formerly inner ones are scanned from now on. Blossoms can be nested, because a contracted vertex can lie on a later blossom.

## Example

The graph has the vertices $r, a, b, c, d, t$ and the edges $ab$, $cb$, $ar$, $cd$, $rd$, $at$, in this order; each vertex lists its edges in this order, and the vertices are numbered $a, c, r, t, d, b$. The 5-cycle $r\,a\,b\,c\,d$ and the pendant edge $at$ make a graph with a perfect matching, $\{rd, cb, at\}$.

| phase | search | event | $M$ after the phase |
|---|---|---|---|
| 1 | all six vertices are roots; from $a$ the edge $ab$ reaches the root $b$ | augment $a\,b$ | $\{ab\}$ |
| 2 | roots $c, r, t, d$; from $c$, $b$ becomes inner and $a$ outer; then $cd$ reaches the root $d$ | augment $c\,d$ | $\{ab, cd\}$ |
| 3 | roots $r, t$; from $r$, $a$ and $d$ become inner, $b$ and $c$ outer; from $t$ the edge $ta$ meets the inner $a$ and is skipped | | |
| 3 | from $b$ the edge $bc$ joins two outer vertices of the tree of $r$ | blossom $r\,a\,b\,c\,d$ with base $r$, contracted; $a$ and $d$ become outer | |
| 3 | from $a$ the edge $at$ reaches the root $t$ of another tree | augment $r\,d\,c\,b\,a\,t$ | $\{rd, cb, at\}$ |
| 4 | no free vertex, no root | stop | $\nu = 3$ |

In phase 3 the path in $G'$ is $\beta\,t$, where $\beta$ is the contracted blossom. Expanding $\beta$ replaces it by the even way round the cycle from the base $r$ to $a$, which is $r\,d\,c\,b\,a$: it starts with the unmatched edge $rd$ and ends with the matched edge $ba$, so $at$ can follow. A search that treats the graph as bipartite labels $a$ inner in phase 3, never leaves $a$ by an unmatched edge, and stops with only 2 edges.

**Odd cycles.** On the cycle $C_5$ the algorithm returns 2 edges and leaves one vertex free, and on $C_7$ 3 edges; in the last phase the only free vertex grows a tree that closes the whole cycle as a blossom and finds no other root.

**No perfect matching.** Take three triangles and one more vertex $z$ joined to one vertex of each triangle. Removing $z$ leaves three odd components, so at least two vertices stay free and $\nu = 4$ on 10 vertices, which the algorithm finds.

**Edge cases.** With no vertices, or with no edges, every vertex is a root, no edge exists, and the first phase returns the empty matching.

## Correctness

Within a phase, $F$ is an alternating forest in $G'$, every free vertex of $G'$ is a root, and every vertex of $G'$ that is a contracted blossom is outer. Line L8 finds an augmenting path in $G'$, because the two tree paths are alternating, end at free roots, and lie in different trees; by the lifting step of the blossom theorem it expands to an augmenting path of $G$. If a phase ends without augmenting, every edge at an outer vertex of $G'$ goes to an inner vertex, so deleting the inner vertices leaves the outer ones as isolated vertices. By the easy half of the [Tutte-Berge formula](/tutte-berge-formula/), $M'$ is then maximum in $G'$, and by the blossom theorem, $M$ is maximum in $G$. The full proof is in the proof files below.

## Complexity

The model is the [word RAM](/word-ram/); vertices are indices.

- **Phases.** Each phase but the last adds one edge to $M$, so there are at most $\lfloor n/2 \rfloor + 1$ phases.
- **One phase.** Each vertex is enqueued at most once, when it becomes outer, and scans its edges once: $O(n + m)$ for the scans and the tests of line L6, which compare two entries of $\text{base}$. Each contraction merges at least three vertices of $G'$ into one, so there are at most $n/2$ contractions in a phase. Finding the base by walking up the tree, marking the blossom and updating $\text{base}$ for all vertices cost $O(n)$ per contraction, $O(n^2)$ per phase. Expanding the blossoms on the augmenting path and flipping it cost $O(n)$.
- **Total.** $O(n(n^2 + m)) = O(n^3)$ time for a simple graph, and $\Theta(n + m)$ space for the adjacency lists and the arrays of the forest.

The full argument is in the complexity proof below.

## Properties

- **General graphs.** It works on every graph; on a bipartite graph no blossom is ever found, and it becomes the alternating forest search of bipartite matching.
- **Certificate.** The last phase gives a set $U$, the inner vertices, such that $\nu(G) = \frac{1}{2}(n + |U| - \text{odd}(G - U))$, the [Tutte-Berge formula](/tutte-berge-formula/). From it one also reads the [Gallai-Edmonds decomposition](/gallai-edmonds-decomposition/): the vertices outer in the last phase are those missed by some maximum matching.
- **Deterministic.** The matching found depends only on the order of the vertices and of the adjacency lists.
- **Matched vertices stay matched.** An augmentation never frees a vertex.

## Variants and improvements

- **Edmonds' original version.** Edmonds builds the contracted graphs explicitly and searches from one root at a time; with straightforward data structures this costs $O(n^4)$.
- **$O(n^3)$ and $O(nm)$.** Gabow (1976) and Lawler (1976) gave $O(n^3)$ implementations without explicit contraction, close to the one above. With a [disjoint-set forest](/disjoint-set-forest/) for the blossoms and an incremental computation of bases, Gabow and Tarjan reached $O(nm \alpha(m, n))$, and $O(nm)$ with their linear-time special case of union-find.
- **$O(m\sqrt n)$.** The [Micali-Vazirani algorithm](/micali-vazirani-algorithm/) finds a maximal set of shortest augmenting paths per phase, as [Hopcroft-Karp](/hopcroft-karp/) does for bipartite graphs, with blossoms handled during a double depth-first search.
- **Weighted matching.** Edmonds' weighted algorithm keeps a dual variable on every vertex and every blossom, grows the forest in the subgraph of tight edges, and also expands blossoms whose dual reaches zero. It solves [maximum weight matching](/maximum-weight-matching/) and [minimum-weight perfect matching](/minimum-weight-perfect-matching/) in polynomial time, and its correctness proof gives [Edmonds' matching polytope theorem](/edmonds-polytope-theorem/).
- **Randomized algebraic methods.** The [Tutte matrix](/tutte-matrix/) gives a randomized $O(n^\omega)$ algorithm, with no blossoms at all.

## When to use it

Use it for maximum cardinality matching in a graph that may have odd cycles, such as pairing people for shared rooms or players for games, when the graph has up to a few thousand vertices. For bipartite graphs use [Hopcroft-Karp](/hopcroft-karp/) or [Kuhn's algorithm](/kuhn-algorithm/). For large sparse graphs, a Micali-Vazirani implementation or a library implementation with good heuristics is faster. A greedy [maximal matching](/maximal-matching/) as a starting point saves most of the early phases.

## Pitfalls

- **Treating the graph as bipartite.** Marking each vertex once as inner or outer, without contracting blossoms, misses augmenting paths, as the example shows. The answer is then too small, without any error.
- **Expanding a blossom the wrong way round.** Inside a blossom there are two ways from the base to a vertex; only the one of even length, which ends with a matched edge, continues an alternating path. Nested blossoms must be expanded recursively, or with links set at contraction time.
- **Forgetting the inner vertices of a blossom.** After a contraction, the formerly inner vertices of the blossom are outer, and their edges must be scanned.
- **Comparing vertices instead of blossoms.** After contractions, the test of line L6 must compare the bases of $v$ and $w$, not $v$ and $w$ themselves.
- **Recursion.** Expanding nested blossoms recursively can go $\Theta(n)$ deep; the implementation follows links in a loop instead.

## Implementations

The Python version takes the vertex count and an edge list and returns the size, the array $\text{mate}$ with $-1$ for free vertices, and the number of phases. It grows the forest from all free vertices at once and does not build $G'$: an array $\text{base}$ names the contracted vertex of each vertex, and at each contraction the outer vertices on the two tree paths get links that point round the blossom. Following $\text{mate}$ and these links from any outer vertex then gives its even alternating path to the root, with every blossom expanded, which line L8 needs. A callback reports each blossom and each augmenting path; the tests check every reported path against the matching before it.

## History

Jack Edmonds published the algorithm in 1965 in "Paths, trees, and flowers", which also argued that an efficient algorithm should be one whose running time is bounded by a polynomial; maximum matching in general graphs was the main example. In the same year he solved the weighted problem and described the matching polytope. Faster implementations followed: Gabow and Lawler in 1976 with $O(n^3)$, Even and Kariv in 1975 with $O(n^{5/2})$, and Micali and Vazirani in 1980 with $O(m\sqrt n)$, whose full proof was completed only decades later.

## References
