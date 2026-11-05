---
tag: H6MPAB
kind: problem
slug: tree-diameter
name: Tree diameter
aliases:
- longest path in a tree
area: graphs/tree-algorithms
level: intro
summary: Find a longest path between any two nodes of a tree.
prereqs: [tree, eccentricity]
see_also: [tree-diameter-double-sweep, tree-center, tree-dynamic-programming, rerooting-technique, longest-path-problem, breadth-first-search, centroid, free-tree-properties]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 22.2 (Breadth-first search), Exercise 22.2-8 (the diameter of a tree)
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 14, Tree algorithms, Section 14.2 (Diameter, the dynamic programming method and the method with two depth-first searches) and Section 14.3 (All longest paths)
  - paper: Ruud W. Bulterman, Frans W. van der Sommen, Gerard Zwaan, Tom Verhoeff, A. J. M. van Gasteren and W. H. J. Feijen, On computing a longest path in a tree, Information Processing Letters 81(2), 93 to 96 (2002)
    locator: the whole note, a correctness proof of the two-search method for trees
---

The tree diameter problem asks for the largest distance between two vertices of a [tree](/tree/), and for a path that has this length. In a tree there is only one path between two vertices, so the diameter is also the longest simple path, a problem that is [NP-hard on general graphs](/longest-path-problem/) but takes $\Theta(n)$ time on a tree. Two linear methods are standard: the [double sweep](/tree-diameter-double-sweep/), which searches twice from a farthest vertex, and a bottom-up [tree dynamic program](/tree-dynamic-programming/). The diameter fixes the [centre](/tree-center/) and all [eccentricities](/eccentricity/) of the tree.

## In plain words

A tree is a network of towns joined by roads with no loops, so between any two towns there is exactly one route. The diameter is the length of the longest of these routes: the two towns that are farthest apart, and the road between them. With roads of equal length, the length is the number of roads on the route.

A slow way is to measure the route from every town to every other town. A fast way uses one search to find the town farthest from any starting town, then a second search from that town. The farthest town of the second search is at the other end of a longest route.

## Definition

**Input.** A tree $T = (V, E)$ with $n \ge 1$ vertices, numbered $0, \ldots, n-1$, given as a list of $n - 1$ edges. The tree is free (not rooted). It may be weighted with a length $w(e) \ge 0$ on each edge; when it is not weighted, each edge has length 1.

**Distance.** For $u, v \in V$, $d(u, v)$ is the total length of the unique path from $u$ to $v$. The *eccentricity* of $v$ is $\mathrm{ecc}(v) = \max_{u \in V} d(v, u)$.

**Output.** The diameter

$$D(T) = \max_{u, v \in V} d(u, v) = \max_{v \in V} \mathrm{ecc}(v),$$

and, in the search version, two vertices $a, b$ with $d(a, b) = D(T)$ and the path between them. Such a path is a *diametral path*, and $a$, $b$ are its *ends*.

## Variants

- **Unweighted.** Each edge has length 1, and $D$ is the number of edges of a longest path. Some texts count vertices instead, which adds 1.
- **Non-negative weights.** The double sweep and the dynamic program both work.
- **Arbitrary real weights.** The dynamic program still works, since it only maximizes path sums. The double sweep can fail: on the path $0, 1, 2$ with $w(01) = -2$ and $w(12) = 1$, the farthest vertex from $0$ is $0$ itself (the distances are $0, -2, -1$), and a sweep from it reports $0$, while $D = d(1, 2) = 1$.
- **All eccentricities.** Find $\mathrm{ecc}(v)$ for every $v$. If $a, b$ are the ends of a diametral path and the weights are non-negative, then $\mathrm{ecc}(v) = \max(d(v, a), d(v, b))$, so three searches suffice. The [rerooting technique](/rerooting-technique/) gives the same in one up and one down pass.
- **Counting.** Count the pairs $\{u, v\}$ with $d(u, v) = D$, or the diametral paths. A dynamic program over the tree does it in $O(n)$ time.
- **Dynamic diameter.** Keep the diameter while edges are added, or while edge weights change. Adding a leaf $x$ to a tree with ends $a, b$ gives the new diameter $\max(D, d(x, a), d(x, b))$, which [LCA](/lowest-common-ancestor/) queries compute in $O(\log n)$ time.
- **General graphs.** The diameter of a general graph is the largest shortest-path distance. It needs a shortest-path computation from many sources, such as [all-pairs shortest paths](/all-pairs-shortest-paths/), and the double sweep gives only a lower bound.

## Examples

| tree | $n$ | $D$ | a diametral path |
|---|---|---|---|
| single vertex | 1 | 0 | $0$ |
| path $0, 1, \ldots, n-1$ | $n$ | $n - 1$ | $0, \ldots, n-1$ |
| star, centre $0$, $n \ge 3$ | $n$ | 2 | $1, 0, 2$ |
| edges $01, 02, 13, 14, 25, 46, 47$ | 8 | 5 | $6, 4, 1, 0, 2, 5$ |

In the last tree, the eccentricities of the vertices $0, \ldots, 7$ are $3, 3, 4, 4, 4, 5, 5, 5$. Their maximum is $D = 5$, reached at $5$, $6$ and $7$, and the diametral paths join $5$ to $6$ and $5$ to $7$. Their minimum, the radius, is $3$, at the centre $\{0, 1\}$.

A weighted example: the star with centre $0$ and the edges $01$, $02$, $03$ of lengths $4$, $1$, $3$ has $D = d(1, 3) = 7$.

## Known algorithms

| algorithm | time | extra space | weights |
|---|---|---|---|
| [Double sweep](/tree-diameter-double-sweep/) | $\Theta(n)$ | $\Theta(n)$ | $w \ge 0$ |
| [Tree dynamic programming](/tree-dynamic-programming/): at each vertex, add the two largest child heights | $\Theta(n)$ | $\Theta(n)$ | any |
| [Tree center by leaf peeling](/tree-center-leaf-peeling/): count the peeling rounds | $\Theta(n)$ | $\Theta(n)$ | unweighted |
| A search from every vertex | $\Theta(n^2)$ | $\Theta(n)$ | any |

The dynamic program roots the tree at any vertex, computes the height $h(v)$ of each vertex in [postorder](/postorder-traversal/), and takes the largest value of $h_1(v) + h_2(v)$, where $h_1(v) \ge h_2(v)$ are the two largest values of $h(c) + w(v, c)$ over the children $c$ of $v$ (with missing values taken as $0$). For arbitrary weights, the values $h(c) + w(v, c)$ that are negative are also replaced by $0$, since a path may stop at $v$.

## Bounds

- **Upper bound.** $O(n)$ time in the [word RAM](/word-ram/) model, by the double sweep or the dynamic program. Each reads the $n - 1$ edges a constant number of times.
- **Lower bound.** $\Omega(n)$ time for weighted trees, since each correct algorithm must read every edge weight. If it does not read the weight of some edge $e$, raise that weight above the total of all other weights. The path made of $e$ alone is then longer than the old diameter, so $D$ changes, while the algorithm sees the same input and gives the same answer. So $\Theta(n)$ is tight.
- **Relation to the radius.** For an unweighted tree, the radius $\min_v \mathrm{ecc}(v)$ equals $\lceil D/2 \rceil$, and the centre is the middle vertex or the middle edge of each diametral path. See [tree center](/tree-center/).

## Reductions

- **To two single-source problems.** With non-negative weights, the diameter reduces to two single-source distance computations on the tree, by the double sweep. Each takes $O(n)$ time, with no priority queue, because in a tree the first path found to a vertex is the only one.
- **Longest path in a tree.** A simple path in a tree is the path between its ends, so the longest simple path problem on trees is the diameter problem.
- **To the centre.** The centre of an unweighted tree is the middle of any diametral path, so the [tree center](/tree-center/) problem reduces to the diameter in $O(n)$ extra time.

## Applications

- The worst-case delay between two nodes of a tree-shaped network, such as a spanning tree used for broadcast.
- The centre of a tree, for placing a facility that minimizes the largest distance to the vertices.
- Bounds in tree algorithms: the height of a tree rooted at its centre is $\lceil D/2 \rceil$ in the unweighted case.
- A building block for tree hashing and [tree isomorphism](/tree-isomorphism/), which root the tree at its centre, found from a diametral path.

## References
