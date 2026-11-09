---
tag: VJCF98
kind: algorithm
slug: chazelle-monotone-point-location
name: Chazelle's point location in monotone subdivisions
aliases:
- optimal point location in monotone subdivisions
- chain method with fractional cascading
- Edelsbrunner-Guibas-Stolfi point location
- separating chain method
area: geometry/point-location
level: research
summary: Search a balanced tree of separating chains and speed up the searches in the chains by fractional cascading, for O(log n) query time and O(n) space.
solves: [planar-point-location, vertical-ray-shooting]
model: real-ram
complexity:
  vars: {n: the number of edges of the regular subdivision}
  time: {build: O(n log n) worst case, query: O(log n) worst case, query-without-cascading: O(log^2 n) worst case}
  space: {extra: O(n) worst case}
properties: {online: false, deterministic: true, recursive: false, static: true}
history:
  year: 1986
  people: [Herbert Edelsbrunner, Leonidas J. Guibas, Jorge Stolfi, Bernard Chazelle]
  note: Lee and Preparata introduced the chain method in 1977 with O(log^2 n) query time; in 1986 Edelsbrunner, Guibas and Stolfi used the fractional cascading of Chazelle and Guibas to bring the query to O(log n) with O(n) space.
prereqs: [monotone-subdivision, multiple-list-search, binary-search]
see_also: [catalog-graph, fractional-cascading-bridge, slab-method-point-location, sarnak-tarjan-point-location, kirkpatrick-point-location, trapezoidal-map, topological-sort, monotone-polygon-partition]
sources:
  - paper: doi:10.1137/0215023
    title: Herbert Edelsbrunner, Leonidas J. Guibas and Jorge Stolfi, Optimal point location in a monotone subdivision, SIAM Journal on Computing 15(2), 1986
    locator: the separator tree, the storage of each edge at one node, and the O(log n) query with fractional cascading
  - paper: doi:10.1137/0206043
    title: D. T. Lee and Franco P. Preparata, Location of a point in a planar subdivision and its applications, SIAM Journal on Computing 6(3), 1977
    locator: the chain method, the complete set of separating chains and the O(log^2 n) query
  - paper: doi:10.1007/BF01840440
    title: Bernard Chazelle and Leonidas J. Guibas, Fractional cascading, I. A data structuring technique, Algorithmica 1, 1986
    locator: the augmented catalogs, bridges and the O(log n + k) search along a path of a tree
  - paper: doi:10.1007/BF01840441
    title: Bernard Chazelle and Leonidas J. Guibas, Fractional cascading, II. Applications, Algorithmica 1, 1986
    locator: the application to planar point location by separating chains
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 2, Section 2.2.2.2, The chain method, and the remark on its improvement
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 38, Point location, by Jack Snoeyink, Section 38.3 (separating chains and fractional cascading)
---

The chain method locates a point in a [monotone subdivision](/monotone-subdivision/) by a binary search over a sorted family of separating chains, where each test against a chain is itself a binary search. The chains can hold $\Theta(n^2)$ edge entries, so each edge is stored only once, at the highest node of a balanced tree of chains whose chain contains it; with a binary search at each node, a query costs $O(\log^2 n)$ time. Edelsbrunner, Guibas and Stolfi then used [fractional cascading](/multiple-list-search/), in the form of Chazelle and Guibas, which turns the searches along a root-to-leaf path into one binary search plus $O(1)$ work per level. The result is optimal: $O(n \log n)$ build time, $O(n)$ space and $O(\log n)$ query time, all worst case.

## In plain words

Think of the map as a stack of roads that all run from the far left of the map to the far right, never crossing, each one a little higher than the one below it. Every street of the map lies on at least one road. To find a point, ask "is the point above or below the middle road?", then the same question for the middle road of the remaining half, and so on.

Each question needs the part of the road that passes the point. A street shared by many roads is written down only once, at the most important road that uses it. Each list also keeps a sample of the lists below it, with links into them. So after the first lookup, every later lookup is just a step or two away along a link.

## The problem

**Notation.** $P$ is the set of vertices, $n$ the number of edges, $p = (x, y)$ a point, and $d = 2$. $\mathrm{orient}(p, q, r)$ is the sign of $(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$, positive when $p, q, r$ turn counterclockwise. A query has output size $h = 1$. The predicate $\mathrm{incircle}$ is not used. Points are compared in the lexicographic order $<_{\mathrm{lex}}$, and $v_1$ and $v_N$ are the smallest and the largest vertex. $f$ is the number of bounded faces. The tree of chains has $2^k - 1$ nodes with the keys $1, \ldots, 2^k - 1$, where $k$ is the number of binary digits of $f + 1$.

The input is a regular planar straight-line graph: segments that meet only at shared end points, in which every vertex other than $v_1$ and $v_N$ has an edge to a smaller and an edge to a larger vertex. By the [monotone subdivision](/monotone-subdivision/) page, every bounded face is then an $x$-monotone polygon, and any planar subdivision can be made regular by adding $O(n)$ edges in $O(n \log n)$ time. A query point $q$ gets the vertex $q$, the edge that contains $q$, or the face answer (above, below): the edges hit by the vertical rays up and down from $q$, the canonical answer of [vertical ray shooting](/vertical-ray-shooting/).

**Degenerate input.** A symbolic shear $(x, y) \mapsto (x + \varepsilon y, y)$ makes all sheared $x$-coordinates distinct and no edge vertical, and the order of the sheared $x$-coordinates is $<_{\mathrm{lex}}$. An edge $(a, b)$ with $a <_{\mathrm{lex}} b$ *spans* $q$ if $a <_{\mathrm{lex}} q <_{\mathrm{lex}} b$. A query with the same $x$ as a vertex is ordered by $y$, and $q$ is on the spanning edge $(a, b)$ exactly when $\mathrm{orient}(a, b, q) = 0$. Vertical edges, equal $x$, and queries on edges or vertices need no special case.

## The algorithm

Each edge $(a, b)$ is stored with $a <_{\mathrm{lex}} b$; its left side is its upper side. The separating chains are those of the [monotone subdivision](/monotone-subdivision/) page: with the bounded faces numbered $1, \ldots, f$ from bottom to top, chain $C_j$ is the upper boundary of the outer part below the graph together with the faces $1, \ldots, j$. Chain $C_j$ belongs to the tree node with key $j + 1$, so the in-order of the tree is the order of the chains. A node with key larger than $f + 1$ has no chain and counts as above everything.

```pseudo id=main
MLOC-BUILD(S)
L1  sort the edges at each vertex by angle and trace the faces of the subdivision
L2  number the bounded faces 1 .. f in a topological order of "directly below"
L3  for each edge e: lo(e) ← the number of the face below e (0 if outer); hi(e) ← the number of the face above e (f + 1 if outer) − 1
L4  for each edge e: add e to L(m), where m is the key in [lo(e) + 1, hi(e) + 1] with the most trailing zeros
L5  from the leaves up: A(m) ← L(m) merged with every second element of A(left child) and of A(right child), by left end point, with pointers nat and down
MLOC-QUERY(q)
    if q is a vertex then return q; if q <lex v1 or q >lex vN then return the face with no edge above or below
L6  m ← the root; pos ← the number of keys of A(m) smaller than q; low ← high ← nil
    repeat
        j ← m − 1                                   ▷ the chain of node m
        if j > f then above ← false
        else e ← the native edge nat(m, pos) of L(m), if it spans q
L7          if there is no such e then above ← (low ≠ nil and hi(low) ≥ j)
L8          else o ← orient(a(e), b(e), q); if o = 0 then return e; above ← (o > 0); if above then low ← e else high ← e
        if m is a leaf then return the face (high, low)
L9      m ← the right child if above else the left child; pos ← down(pos); while A(m)[pos] < q do pos ← pos + 1
```

- **Lines L1 and L2.** The faces come from the next pointers of a [DCEL](/planar-subdivision/): the next edge after $u \to v$ is $v \to w$ for the neighbor $w$ that follows $u$ clockwise around $v$. Face $F$ is directly below face $F'$ if an edge has $F$ below and $F'$ above. This relation is acyclic for a regular graph, so a [topological sort](/topological-sort/) numbers the faces. The code breaks ties by the smallest vertex of the face, which makes the numbering deterministic.
- **Line L3.** Edge $e$ is on the upper boundary of faces $1, \ldots, j$ exactly when the face below $e$ is among them and the face above is not, so $e$ is in the chains $C_{\mathrm{lo}(e)}, \ldots, C_{\mathrm{hi}(e)}$, a contiguous range.
- **Line L4.** The key with the most trailing zeros in an interval of keys is the root of the smallest subtree that contains the interval. So each edge is stored exactly once, at the highest node whose chain contains it, and the edges in $L(m)$ all belong to $C_{m-1}$. They have disjoint $x$-ranges and are sorted by left end point.
- **Line L5.** The list $A(m)$ holds the keys (left end points) of $L(m)$ and of the elements at odd positions of $A(c)$ for both children $c$. For a position $p$, $\mathrm{nat}(m, p)$ is the last own edge among the first $p$ keys of $A(m)$, and $\mathrm{down}(p)$ is the number of keys of $A(c)$ that are at most the $p$-th key of $A(m)$.
- **Line L7.** If $L(m)$ has no edge that spans $q$, the edge of $C_j$ that spans $q$ is stored at an ancestor of $m$, where it was tested. It is then the current $\mathrm{low}$ if $q$ is above it, and otherwise $q$ is below $C_j$. The test $\mathrm{hi}(\mathrm{low}) \ge j$ tells which case holds, without a new orientation test.
- **Line L9.** After the pointer, at most one key of the child lies between the predecessor of $q$ in $A(m)$ and $q$, since among two consecutive keys of the child one was copied into $A(m)$. So the loop runs at most once.

With `cascade=False`, the code replaces lines L6 and L9 by a binary search in $L(m)$ at each node, which is the simple chain method on the same tree, in $O(\log^2 n)$ time.

## Example

The subdivision is the one of the [monotone subdivision](/monotone-subdivision/) page: $a = (0,2)$, $b = (2,0)$, $c = (2,4)$, $d = (4,2)$, $e = (6,0)$, $f = (6,4)$, $g = (8,2)$ and the ten edges $ab, ac, bd, cd, be, cf, de, df, eg, fg$. Lines L1 and L2 number the faces $bed = 1$, $abdc = 2$, $defg = 3$, $cdf = 4$, so there are $f + 1 = 5$ chains, $C_0 = abeg$, $C_1 = abdeg$, $C_2 = acdeg$, $C_3 = acdfg$ and $C_4 = acfg$. Line L3 gives the ranges, and line L4 stores each edge at one of the $7$ nodes, with the root $4$:

| node $m$ | chain | $L(m)$ | keys of $A(m)$ |
|---|---|---|---|
| 1 | $C_0$ | $be$ $[0, 0]$ | $b$ |
| 2 | $C_1$ | $ab$ $[0, 1]$, $bd$ $[1, 1]$, $de$ $[1, 2]$, $eg$ $[0, 2]$ | $a, b, d, e$ |
| 3 | $C_2$ | none | none |
| 4 | $C_3$ | $ac$ $[2, 4]$, $cd$ $[2, 3]$, $df$ $[3, 3]$, $fg$ $[3, 4]$ | $a, b, c, d, e, f$ |
| 5 | $C_4$ | $cf$ $[4, 4]$ | $c$ |
| 6, 7 | none | none | none |

The chains hold $18$ edge entries, but the lists $L$ hold each of the $10$ edges once, and the lists $A$ hold $12$ keys. $A(4)$ has its own keys $a, c, d, f$ and the copies $b, e$ of positions $1$ and $3$ of $A(2)$.

For $q = (3, 2)$, line L6 finds $3$ keys of $A(4)$ smaller than $q$ ($a$, $b$ and $c$), and the last own key among them is $c$, so the edge is $cd$. It spans $q$, and $\mathrm{orient}(c, d, q) = (4-2)(2-4) - (2-4)(3-2) = -2 < 0$, so $q$ is below $C_3$ and $\mathrm{high} = cd$. The pointer into $A(2)$ is $2$, and $A(2)[2] = d$ is larger than $q$, so no step is needed. The native edge is $bd$, and $\mathrm{orient}(b, d, q) = 2 > 0$, so $q$ is above $C_1$ and $\mathrm{low} = bd$. At node $3$, $L(3)$ is empty: the edge of $C_2$ at $q$ is $cd$, stored at the root. Line L7 finds $\mathrm{hi}(bd) = 1 < 2$, so $q$ is below $C_2$. Node $3$ is a leaf, and the answer is the face between $cd$ above and $bd$ below, the face $abdc$, after two orientation tests. For $q = (3, 1)$ the second test gives $\mathrm{orient}(b, d, q) = 0$, and the answer is the edge $bd$. The test file checks these numbers.

## Correctness

**Theorem.** For every regular planar straight-line graph and every query point $q$, MLOC-QUERY returns the vertex $q$, the edge that contains $q$ in its relative interior, or the lowest edge above and the highest edge below $q$ in the sheared plane (nil if there is none).

The proof has four parts. The ranges of line L3 describe the chains of the [monotone subdivision](/monotone-subdivision/) page, which are $x$-monotone, cover every edge, and are ordered from bottom to top, so "$q$ is above $C_j$" is monotone in $j$ and each chain has exactly one edge that spans $q$. The storage rule puts the spanning edge of $C_j$ at node $j + 1$ or at an ancestor of it. The invariant of the search is: after each node, $\mathrm{low}$ is the spanning edge of the highest chain known to be below $q$, and $\mathrm{high}$ that of the lowest chain known to be above it; it makes the inherited decision of line L7 correct. The cascading invariant is that $\mathrm{pos}$ is the number of keys of $A(m)$ smaller than $q$, so $\mathrm{nat}(m, \mathrm{pos})$ is the only own edge that can span $q$. The binary search over the chains then ends with the two consecutive chains around $q$, whose spanning edges are the edges directly below and above $q$. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Build time.** Line L1 sorts the edges at each vertex, in $O(n \log n)$ time in total, and traces the $2n$ half-edges in $O(n)$. Line L2 is a topological sort in $O(n)$ time; the code uses a heap for its tie rule, in $O(n \log n)$. Lines L3 and L4 take $O(1)$ per edge with a trailing-zero instruction, or $O(\log n)$ by a descent from the root. Line L5 merges sorted lists, in time linear in their total size. So the build takes $O(n \log n)$ time in the worst case on the [real RAM](/real-ram/).
- **Space.** By Euler's formula, $f \le n$, so the tree has fewer than $2(f + 1) \le 2n + 2$ nodes. Each edge is in one list $L(m)$. Each list $A(m)$ has $|L(m)|$ own keys and at most half of the keys of each child list, so the total size $S$ satisfies $S \le n + S/2$, which gives $S \le 2n$, and the pointers have the same size. The space is $O(n)$ in the worst case, while the chains themselves would hold $\Theta(n^2)$ entries in the worst case.
- **Query time.** Line L6 is a binary search in $O(\log n)$ time. Each of the $k = O(\log n)$ levels then costs at most one orientation test and at most one step of line L9. So a query takes $O(\log n)$ time in the worst case, which matches the $\Omega(\log n)$ lower bound of [planar point location](/planar-point-location/) in the [algebraic decision tree](/algebraic-decision-tree/) model. Without cascading, each level costs a binary search, and a query takes $O(\log^2 n)$ time in the worst case.

## Properties

- **Optimal and deterministic.** $O(n \log n)$ build, $O(n)$ space and $O(\log n)$ query, all worst case, with no randomization.
- **Needs a regular graph.** A general subdivision must first be regularized, which adds $O(n)$ edges; each new face remembers the original face that contains it.
- **Few predicates.** A query uses lexicographic comparisons and at most one orientation test per level, and the build uses orientation tests only to sort the edges around each vertex.
- **Static.** A new edge can change the face order and many chains.

## Variants and improvements

- **The simple chain method.** Lee and Preparata (1977) search the edges stored at each node of the tree of chains by a separate binary search: $O(\log^2 n)$ query time and $O(n)$ space.
- **Bridges.** The original fractional cascading of Chazelle and Guibas keeps the copied elements between a node and each child as [bridges](/fractional-cascading-bridge/) in a general [catalog graph](/catalog-graph/). Copying every second element is the special case for a tree.
- **Other optimal methods.** [Kirkpatrick's hierarchy](/kirkpatrick-point-location/), [Sarnak and Tarjan's persistent tree](/sarnak-tarjan-point-location/) and the randomized [trapezoidal map](/trapezoidal-map/) reach the same bounds with different ideas.
- **Dynamic versions.** [Dynamic fractional cascading](/dynamic-fractional-cascading/) supports insertions and deletions in the lists, and dynamic point location in monotone subdivisions builds on the same separating chains.

## When to use it

Use it when the subdivision is already monotone or regular, for example a triangulation, and worst-case deterministic bounds are needed. The query is a short descent with one orientation test per level, which suits batches of queries. For a general set of segments without face structure, the [Sarnak-Tarjan method](/sarnak-tarjan-point-location/) or the [trapezoidal map](/trapezoidal-map/) needs no regularization step and is simpler to code.

## Pitfalls

- **Storing every chain in full.** A long edge shared by many chains then appears $\Theta(n)$ times, and the space becomes $\Theta(n^2)$. Store each edge only at the highest node of its range (line L4).
- **Treating a missing edge as "below".** If $L(m)$ has no edge that spans $q$, the decision at $m$ is inherited from an ancestor (line L7). Guessing a side breaks the search.
- **Pointers into one child only.** Every key of $A(m)$ needs a down pointer into both children, including the keys copied from the other child, since the search can turn either way after any key.
- **Using the $x$-coordinate alone.** Vertices with equal $x$ make the chains look non-monotone and edges vertical. Compare points lexicographically, which is the symbolic shear.
- **Unregularized input.** A face with a hole or a vertex with no edge to the left has no family of separating chains. The code raises an error for such input.

## Implementations

## History

D. T. Lee and Franco Preparata introduced the chain method in 1977: the separating chains in a balanced tree, each edge stored at one node, $O(n)$ space and $O(\log^2 n)$ query time. In 1986 Herbert Edelsbrunner, Leonidas Guibas and Jorge Stolfi built the chains from a topological order of the faces in linear time and used the fractional cascading of Bernard Chazelle and Leonidas Guibas to reach $O(\log n)$ query time with $O(n)$ space. Chazelle and Guibas presented the same application in the second part of their fractional cascading papers, which is why the method is often credited to the fractional cascading work. It was one of the first optimal methods for planar point location, together with Kirkpatrick's hierarchy (1983) and the persistent search trees of Sarnak and Tarjan and of Cole (1986).

## References
