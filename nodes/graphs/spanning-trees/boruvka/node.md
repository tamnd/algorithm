---
tag: 1APEF6
kind: algorithm
slug: boruvka
name: Borůvka's algorithm
aliases:
- Sollin's algorithm
area: graphs/spanning-trees
level: core
summary: Each component repeatedly adds its cheapest outgoing edge; O(log n) rounds.
solves: [minimum-spanning-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O((n + m) log n), best: Ω(n + m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1926
  people: [Otakar Borůvka]
  note: Borůvka published the method in 1926 for the design of an electrical network in Moravia.
prereqs: [minimum-spanning-tree, cut-property, connected-components, greedy-algorithm]
see_also: [kruskal, prim, generic-mst-method, karger-klein-tarjan-mst, fredman-tarjan-mst, chazelle-mst, graph-contraction, mst-uniqueness]
sources:
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 7, Minimum Spanning Trees (the sections on distinct edge weights and on Borůvka's algorithm)
  - paper: doi:10.1016/S0012-365X(00)00224-7
    title: "Jaroslav Nešetřil, Eva Milková and Helena Nešetřilová, Otakar Borůvka on minimum spanning tree problem: translation of both the 1926 papers, comments, history, Discrete Mathematics 233(1-3) (2001), 3-36"
    locator: the translations of the two 1926 papers and the comments
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms, SIAM (1983)
    locator: Chapter 6, Minimum Spanning Trees (Sollin's algorithm as an application of the blue rule)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.3, Minimum Spanning Trees (the exercise on Borůvka's algorithm)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 21, Minimum Spanning Trees (the chapter problems)
  - paper: "Andrew Chi-Chih Yao, An O(|E| log log |V|) algorithm for finding minimum spanning trees, Information Processing Letters 4(1) (1975), 21-23"
    locator: the whole paper
  - paper: "Robert G. Gallager, Pierre A. Humblet and Philip M. Spira, A distributed algorithm for minimum-weight spanning trees, ACM Transactions on Programming Languages and Systems 5(1) (1983), 66-77"
    locator: the whole paper
---

Borůvka's algorithm finds a [minimum spanning tree](/minimum-spanning-tree/) by rounds: in each round, every tree of the current forest picks the lightest edge that leaves it, and all picked edges are added at once. Each round at least halves the number of trees that can still grow, so there are at most $\lfloor \lg n \rfloor + 1$ rounds, and the algorithm runs in $O((n + m) \log n)$ time. It is the oldest algorithm for the problem, from 1926. Because the trees of one round act on their own, it is the base of parallel and distributed MST algorithms, and of the fast algorithms of [Karger, Klein and Tarjan](/karger-klein-tarjan-mst/) and of [Chazelle](/chazelle-mst/).

## In plain words

Start with every town alone. In each round, every group of towns looks at the roads that leave the group and picks the cheapest one. Then all the picked roads are built at the same time, and the groups they join become larger groups. Repeat until no road leaves any group.

Each group joins at least one other group in a round, so the number of groups at least halves. With a thousand towns there are at most about ten rounds.

One detail matters. If two roads have the same price, every group must break the tie in the same way, for example by a road number. Otherwise three groups in a ring can each pick a different road of equal price, and the roads close a loop.

## The problem

The input is an undirected graph $G = (V, E)$ with $n$ vertices, $m$ edges and a real weight $w(e)$ on each edge. Weights may tie; parallel edges and self-loops are allowed. The graph need not be [connected](/connected-graph/). The output is a minimum spanning forest: a forest with the same [connected components](/connected-components/) as $G$ and the least total weight. For a connected graph it is a minimum spanning tree.

The algorithm compares edges by the strict total order

$$e \prec f \iff (w(e), \mathrm{id}(e)) < (w(f), \mathrm{id}(f)) \text{ in lexicographic order},$$

where $\mathrm{id}$ is a fixed number for each edge, such as its position in the input. This order agrees with the weights and breaks every tie.

## The algorithm

```pseudo id=main
BORŮVKA(G, w)
L1  F ← ∅
L2  repeat
L3      label each vertex v with comp[v], the tree of (V, F) that holds v      ▷ by a graph search
L4      best[C] ← nil for each tree C
L5      for each edge e = (u, v) ∈ E do
L6          if comp[u] ≠ comp[v] then                                         ▷ e leaves two trees
L7              for each X ∈ {comp[u], comp[v]} do
L8                  if best[X] = nil or e ≺ best[X] then best[X] ← e
L9      A ← {best[C] : best[C] ≠ nil}                                         ▷ as a set: an edge picked twice counts once
L10     F ← F ∪ A
L11 until A = ∅
L12 return F
```

Line L3 finds the trees of the forest by a [depth-first](/depth-first-search/) or [breadth-first search](/breadth-first-search/) over the edges of $F$. Lines L5 to L8 scan every edge once and keep, for each tree, the $\prec$-least edge that leaves it. An edge with both ends in one tree, including a self-loop, is skipped. Line L9 collects the picks; when two trees pick the same edge, it is added once. If no tree has an edge that leaves it, each tree is a whole component of $G$, and the loop stops.

A program may also stop as soon as $|F| = n - c$, where $c$ is the number of components, and save the last scan.

## Example

The graph has the vertices $a$ to $f$ and these edges, numbered in this order for the tie-break:

| id | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| edge | $ab$ | $ac$ | $bc$ | $bd$ | $cd$ | $ce$ | $de$ | $df$ | $ef$ |
| weight | 4 | 3 | 1 | 2 | 4 | 5 | 7 | 6 | 2 |

**Round 1.** Each vertex is a tree.

| tree | edges that leave it | pick |
|---|---|---|
| $\{a\}$ | $ab = 4$, $ac = 3$ | $ac$ |
| $\{b\}$ | $ab = 4$, $bc = 1$, $bd = 2$ | $bc$ |
| $\{c\}$ | $ac = 3$, $bc = 1$, $cd = 4$, $ce = 5$ | $bc$ |
| $\{d\}$ | $bd = 2$, $cd = 4$, $de = 7$, $df = 6$ | $bd$ |
| $\{e\}$ | $ce = 5$, $de = 7$, $ef = 2$ | $ef$ |
| $\{f\}$ | $df = 6$, $ef = 2$ | $ef$ |

So $A = \{ac, bc, bd, ef\}$, with weight 8, and the trees become $\{a, b, c, d\}$ and $\{e, f\}$.

**Round 2.** The edges that leave $\{a, b, c, d\}$ are $ce = 5$, $de = 7$ and $df = 6$; they are also the edges that leave $\{e, f\}$. Both trees pick $ce$, so $A = \{ce\}$ and there is one tree.

**Round 3.** No edge leaves the tree, so $A = \emptyset$ and the algorithm stops.

The result is $F = \{ac, bc, bd, ef, ce\}$ with weight $8 + 5 = 13$, the only minimum spanning tree of this graph. There were 6 trees, then 2, then 1.

## Correctness

**Theorem.** For each finite undirected graph with real edge weights, BORŮVKA returns a minimum spanning forest, after at most $\lfloor \lg n \rfloor + 1$ rounds. Ties are allowed; the graph may be disconnected.

The key fact is that the order $\prec$ is strict. Let $T^*$ be the forest that [Kruskal's algorithm](/kruskal/) returns when it sorts the edges by $\prec$. It is a minimum spanning forest. If an edge $e$ is the $\prec$-least edge that crosses some cut, then $e \in T^*$: when Kruskal's algorithm reaches $e$, no earlier edge crosses the cut, so the ends of $e$ are in different trees and it adds $e$. In each round, $\mathrm{best}[C]$ is the $\prec$-least edge across the cut around $C$, so every picked edge is in $T^*$. So the invariant $F \subseteq T^*$ holds, $F$ never has a cycle, and at the end $F$ has the components of $G$ and equals $T^*$. The full proof, with the count of rounds, is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM, with a comparison of two weights in $O(1)$ time.

**One round.** Line L3 is a graph search over $n$ vertices and $|F| < n$ edges, $O(n)$ time. Lines L4 to L8 scan $m$ edges with $O(1)$ work each. Lines L9 and L10 take $O(n)$ time. So a round costs $O(n + m)$.

**The number of rounds.** Call a tree of $F$ *open* when some edge leaves it. In a round, each open tree picks an edge to another tree, so each open tree is merged with at least one other tree. A new tree that is still open is a union of at least two old open trees. So if there are $k$ open trees before a round, there are at most $\lfloor k / 2 \rfloor$ after it. At the start $k \le n$. After $r$ rounds that add edges, $k \le n / 2^r$, and a round adds an edge only when $k \ge 2$. So at most $\lfloor \lg n \rfloor$ rounds add edges, and one more round finds $A = \emptyset$.

**Total.** At most $\lfloor \lg n \rfloor + 1$ rounds of $O(n + m)$ time each: $O((n + m) \log n)$ in the worst case, which is $O(m \log n)$ for a connected graph. Each round reads all $m$ edges, so the time is $\Omega(n + m)$ on each input. The extra space is $O(n + m)$ for the labels, the picks and the adjacency of $F$.

| claim | bound | case |
|---|---|---|
| time | $O((n + m) \log n)$ | worst |
| time | $\Omega(n + m)$ | best |
| rounds | at most $\lfloor \lg n \rfloor + 1$ | worst |
| extra space | $O(n + m)$ | worst |

**Contraction.** A common version contracts each tree to one vertex after each round and deletes self-loops and all but the lightest of each group of parallel edges. Then round $i$ works on a graph of at most $n / 2^{i}$ vertices. For planar graphs, and for any family closed under contraction with $m = O(n)$, the edge count also halves, so the total is $O(n)$ (see [graph contraction](/graph-contraction/)).

## Properties

- **Deterministic**, once the tie-break by $\mathrm{id}$ is fixed.
- **Parallel by nature.** The picks of one round are independent, so one round is a parallel scan and a [graph contraction](/graph-contraction/). This is why parallel and distributed MST algorithms start from Borůvka.
- **Needs a strict order.** The proof of acyclicity needs a strict order on the edges. Plain weights with ties are not enough.
- **Works on forests.** On a disconnected graph it returns a minimum spanning forest with no change.

## Variants and improvements

- **Borůvka with contraction.** Contract the trees after each round, as in the Complexity section. The same $O(m \log n)$ bound holds in general, and $O(n)$ for planar graphs.
- **Borůvka steps as preprocessing.** A few rounds cut the number of vertices by a constant factor each in $O(m)$ time. The [Fredman-Tarjan](/fredman-tarjan-mst/), [Karger-Klein-Tarjan](/karger-klein-tarjan-mst/) and [Chazelle](/chazelle-mst/) algorithms use them.
- **Yao's algorithm.** Yao (1975) split the edges at each vertex into groups by weight, so that a round costs less, and got $O(m \log \log n)$ time; see [Yao's MST algorithm](/yao-mst/).
- **Distributed MST.** The algorithm of Gallager, Humblet and Spira (1983) merges fragments along their lightest outgoing edges by message passing, in the manner of Borůvka.

## When to use it

Use Borůvka's algorithm for parallel or distributed computation, for graphs that are too large to sort, and as a first phase of a faster method. On one processor, for a general graph, [Kruskal's](/kruskal/) and [Prim's](/prim/) algorithms are as fast in theory and usually faster in practice, because a round of Borůvka scans every edge again. On planar graphs and other sparse families closed under contraction, Borůvka with contraction runs in linear time and is the method of choice.

## Pitfalls

- **Ties without a tie-break.** Comparing only weights in line L8 can add a cycle. On a triangle with three edges of weight 1, the three vertices can pick three different edges. The tie test case catches it: the output must have $n - 1$ edges and no cycle. Compare $(w(e), \mathrm{id}(e))$, not $w(e)$.
- **Adding an edge twice.** The two trees at the ends of an edge often pick the same edge. Line L9 must treat $A$ as a set; a list that holds the edge twice gives $|F| > n - c$.
- **Stale labels.** The labels comp of line L3 must be recomputed after each round. Using the labels of the round before keeps edges inside a merged tree as candidates, and they close cycles.
- **Stopping when one tree is left.** On a disconnected graph the loop must stop when no edge leaves any tree, not when one tree is left; the disconnected test case catches a loop that never ends.

## Implementations

## History

Otakar Borůvka published the method in 1926, in two papers in Czech, written for the design of an economical electrical network in Moravia. Nešetřil, Milková and Nešetřilová (2001) translated both papers into English and comment on their content and history. The method was found again later by others, and the name "Sollin's algorithm", which Tarjan's 1983 monograph uses (Chapter 6), comes from one of these rediscoveries.

## References
