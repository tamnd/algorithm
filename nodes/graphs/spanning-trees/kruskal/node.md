---
tag: 1DB0HR
kind: algorithm
slug: kruskal
name: Kruskal's algorithm
aliases:
- Kruskal's MST algorithm
area: graphs/spanning-trees
level: intro
summary: Sort the edges and add each edge that joins two different components.
solves: [minimum-spanning-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m log m), best: Ω(m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1956
  people: [Joseph B. Kruskal]
  note: Kruskal published the method in the Proceedings of the American Mathematical Society in 1956.
prereqs: [minimum-spanning-tree, cut-property, disjoint-set, sorting-problem]
see_also: [prim, boruvka, reverse-delete, generic-mst-method, greedy-mst-algorithm, cycle-property, graphic-matroid, disjoint-set-forest]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 21, Section 21.2 (Kruskal's algorithm); Chapter 19 (disjoint sets)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.5 (the minimum spanning tree problem, the cut property and the proof for Kruskal) and Section 4.6 (the union-find structure)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.3, Minimum Spanning Trees (Kruskal's algorithm)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 7, Minimum Spanning Trees (the section on Kruskal's algorithm)
  - paper: doi:10.1090/S0002-9939-1956-0078686-7
    title: "Joseph B. Kruskal, On the shortest spanning subtree of a graph and the traveling salesman problem, Proceedings of the American Mathematical Society 7(1) (1956), 48-50"
    locator: the whole paper (Construction A)
---

Kruskal's algorithm finds a [minimum spanning tree](/minimum-spanning-tree/) of a connected, undirected, [weighted graph](/weighted-graph/): it scans the edges in non-decreasing order of weight and keeps each edge that joins two different components of the edges kept so far. With a [disjoint-set](/disjoint-set/) structure for the components, it runs in $O(m \log m)$ time, and the sort is the slowest step. On a graph that is not connected, the same procedure returns a minimum spanning forest. It is the standard example of a [greedy algorithm](/greedy-algorithm/) that is correct, and its proof uses the [cut property](/cut-property/).

## In plain words

You must connect some towns with roads, and each possible road has a price. You want all towns connected at the least total price.

Put the possible roads in order, from the cheapest to the most expensive. Look at each road in turn. If the two towns at its ends are already connected by the roads you took, skip the road, because it adds only a loop. Otherwise, take it. When you reach the end of the list, the roads you took connect every town that can be connected, and no other choice of roads costs less.

To know quickly if two towns are already connected, keep the towns in groups. Two towns are in the same group when your roads connect them. Taking a road joins two groups into one.

## The problem

The input is an undirected graph $G = (V, E)$ with $n = |V|$ vertices, $m = |E|$ edges and a weight $w(e)$ on each edge, a real number or an integer. Weights may be negative and may tie. Parallel edges and [self-loops](/self-loop/) are allowed. The graph does not have to be [connected](/connected-graph/).

The output is a set $F \subseteq E$ that is a spanning forest of $G$, that is, a forest with the same [connected components](/connected-components/) as $G$, and that has the least total weight $w(F) = \sum_{e \in F} w(e)$ of all such forests. When $G$ is connected, $F$ is a [spanning tree](/spanning-tree/) with $n - 1$ edges, and it is a minimum spanning tree. When weights tie, more than one forest can be minimum, and the algorithm returns one of them, fixed by the order of the sort.

## The algorithm

The procedures MAKE-SET, FIND-SET and UNION are the operations of a [disjoint-set](/disjoint-set/) structure. FIND-SET$(u)$ returns the representative of the set that holds $u$.

```pseudo id=main
KRUSKAL(G, w)
L1  F ← ∅
L2  for each vertex v ∈ V do MAKE-SET(v)
L3  sort the edges of E into non-decreasing order of w
L4  for each edge (u, v) ∈ E, in this order do
L5      if FIND-SET(u) ≠ FIND-SET(v) then          ▷ u and v are in different trees of F
L6          F ← F ∪ {(u, v)}
L7          UNION(u, v)
L8  return F
```

At each moment, the sets of the disjoint-set structure are the vertex sets of the trees of $F$. Line L5 asks if the edge joins two different trees. If it does, the edge cannot close a cycle, so lines L6 and L7 add it and merge the two trees. If both ends are in the same tree, the edge would close a cycle with edges of $F$, and the algorithm drops it for good. A self-loop always has both ends in the same set, so it is never taken.

A program can stop the loop after $n - c$ edges are in $F$, where $c$ is the number of components, if it knows $c$. For a connected graph this is $n - 1$ edges.

## Example

The graph has the vertices $a$ to $f$ and nine edges. Two pairs of edges tie: $bd$ and $ef$ have weight 2, and $ab$ and $cd$ have weight 4. The sort puts tied edges in input order.

| edge | $ab$ | $ac$ | $bc$ | $bd$ | $cd$ | $ce$ | $de$ | $df$ | $ef$ |
|---|---|---|---|---|---|---|---|---|---|
| weight | 4 | 3 | 1 | 2 | 4 | 5 | 7 | 6 | 2 |

| step | edge | weight | action | $w(F)$ | the trees of $F$ after the step |
|---|---|---|---|---|---|
| 1 | $bc$ | 1 | add | 1 | $\{a\}, \{b, c\}, \{d\}, \{e\}, \{f\}$ |
| 2 | $bd$ | 2 | add | 3 | $\{a\}, \{b, c, d\}, \{e\}, \{f\}$ |
| 3 | $ef$ | 2 | add | 5 | $\{a\}, \{b, c, d\}, \{e, f\}$ |
| 4 | $ac$ | 3 | add | 8 | $\{a, b, c, d\}, \{e, f\}$ |
| 5 | $ab$ | 4 | skip: $a$ and $b$ in one tree | 8 | no change |
| 6 | $cd$ | 4 | skip: $c$ and $d$ in one tree | 8 | no change |
| 7 | $ce$ | 5 | add | 13 | $\{a, b, c, d, e, f\}$ |
| 8 | $df$ | 6 | skip | 13 | no change |
| 9 | $de$ | 7 | skip | 13 | no change |

The tree is $\{bc, bd, ef, ac, ce\}$ with weight 13. The graph has 55 spanning trees, and this is the only one of weight 13. Steps 8 and 9 do no useful work: after step 7, $F$ has $n - 1 = 5$ edges, and a program that counts the edges can stop there.

## Correctness

**Theorem.** For each finite undirected graph with real edge weights, KRUSKAL returns a minimum spanning forest. Ties in the weights and disconnected graphs are allowed.

The main invariant is: *before each test of line L5, there is a minimum spanning forest $F^*$ of $G$ with $F \subseteq F^*$.* At the start $F = \emptyset$, so the invariant holds. When line L6 adds the edge $e = (u, v)$, take the cut $(S, V \setminus S)$ where $S$ is the vertex set of the tree of $F$ that holds $u$. No edge of $F$ crosses this cut, and $e$ crosses it. Each edge that crosses the cut and comes before $e$ in the sorted order was dropped earlier, so its two ends were in one tree of $F$ at that time, and they still are; it cannot cross the cut. So $e$ is a lightest edge across the cut, and the [cut property](/cut-property/) shows that $F \cup \{e\}$ is still inside some minimum spanning forest. At the end, each dropped edge has both ends in one tree of $F$, so $F$ has the components of $G$, and $F \subseteq F^*$ forces $F = F^*$. The full proof, with the exchange step written out for ties, is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM, with a comparison of two weights in $O(1)$ time.

- **Line L2** makes $n$ sets in $O(n)$ time.
- **Line L3** sorts $m$ edges in $O(m \log m)$ time with a comparison sort such as [merge sort](/merge-sort/). For a simple graph $m < n^2$, so $\log m < 2 \log n$ and this is also $O(m \log n)$. If the weights are small integers, [counting sort](/counting-sort/) or [radix sort](/radix-sort/) makes this step $O(m)$ or near it.
- **Lines L4 to L7** do $2m$ FIND-SET calls and at most $n - 1$ UNION calls. With [union by rank](/union-by-rank/) or by size and [path compression](/path-compression/), they take $O(m \, \alpha(n))$ time in total, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/). With union by size alone, each FIND-SET takes $O(\log n)$ time, which gives $O(m \log n)$ and still fits the bound.

The total is $O(m \log m)$ in the worst case. Each edge is read at least once, so the time is $\Omega(m)$ on each input. When the edges arrive already sorted, the time is $O(m \, \alpha(n))$. The extra space is $O(n)$ for the disjoint-set arrays and $O(m)$ for the sorted order of the edges.

| claim | bound | case |
|---|---|---|
| time | $O(m \log m)$, which is $O(m \log n)$ for a simple graph | worst |
| time | $\Omega(m)$ | best |
| extra space | $O(n + m)$ | worst |

## Properties

- **Deterministic.** The order of the sort fixes the output. A stable sort keeps tied edges in input order.
- **Greedy and offline.** Each decision is final, but the algorithm needs all edges before it starts, because it sorts them.
- **Forests for free.** On a disconnected graph it returns a minimum spanning forest with no change to the code.
- **Only the order of the weights matters.** The algorithm compares weights and never adds them. So any strictly increasing function of the weights gives the same tree, and negative weights need no special case.

## Variants and improvements

- **Stop early.** Stop when $F$ has $n - c$ edges. This saves the scan of the heaviest edges, but not the sort.
- **Filter-Kruskal.** Partition the edges around a pivot weight as in quicksort, solve the light part first, and drop the heavy edges whose ends are already joined before sorting them. It runs fast in practice on dense graphs.
- **Maximum spanning tree.** Sort in non-increasing order to get a [maximum spanning tree](/maximum-spanning-tree/).
- **Matroids.** Kruskal's algorithm is the [matroid greedy algorithm](/matroid-greedy-algorithm/) on the [graphic matroid](/graphic-matroid/). The same proof works for each [matroid](/matroid/).
- **Reverse-delete.** The mirror method [reverse-delete](/reverse-delete/) scans from the heaviest edge and removes each edge whose removal keeps the graph connected. It uses the [cycle property](/cycle-property/).
- **Single linkage clustering.** Stop when $F$ has $n - k$ edges. The $k$ trees are the clusters of maximum spacing (Kleinberg and Tardos, Section 4.7).

## When to use it

Use Kruskal's algorithm when the graph is given as an [edge list](/edge-list/), when it is sparse, or when you need a spanning forest of a graph that may be disconnected. It is short to write when a disjoint-set structure is at hand. On a dense graph with $m = \Theta(n^2)$, [Prim's algorithm](/prim/) with an array runs in $O(n^2)$ time and does not sort. For parallel or external-memory work, [Borůvka's algorithm](/boruvka/) is easier to split. For the theory of the fastest methods, see the [Karger-Klein-Tarjan algorithm](/karger-klein-tarjan-mst/) and [Chazelle's algorithm](/chazelle-mst/).

## Pitfalls

- **No cycle test.** Adding the edges in sorted order without the test of line L5 gives a graph with cycles. The test case with all weights equal on a triangle catches it: the output must have 2 edges, not 3.
- **A slow cycle test.** A DFS from $u$ to look for $v$ in $F$ at each edge costs $O(n)$ per edge and $O(mn)$ in total. Use a disjoint-set structure.
- **Union by representative only.** UNION$(u, v)$ must link the two roots, not the vertices $u$ and $v$ themselves. Writing `parent[v] ← u` breaks the sets when $v$ is not a root.
- **Expecting $n - 1$ edges.** On a disconnected graph the output has $n - c$ edges. Code that returns "no tree" or loops forever while $|F| < n - 1$ fails the disconnected test case.
- **Sorting only by weight with an unstable sort, and then comparing trees.** With ties, two correct runs can return different trees with the same weight. A test must compare the total weight, or fix the tie-break, as the test of the implementation does with the edge index.
- **Integer overflow in the total weight.** Sum the weights in a type wide enough for $n - 1$ edges of the largest weight.

## Implementations

## History

Joseph Kruskal published the method in 1956, in a three-page paper in the Proceedings of the American Mathematical Society, which also discusses the traveling salesman problem. The paper gives the method as a construction on a finite graph with distinct lengths, and also shows that the tree is then unique. The paper does not give a data structure for the cycle test. The fast disjoint-set structures that make the loop near linear are a separate line of work, described in CLRS, Chapter 19.

## References
