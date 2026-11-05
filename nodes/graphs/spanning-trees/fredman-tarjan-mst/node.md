---
tag: 37AZFW
kind: algorithm
slug: fredman-tarjan-mst
name: Fredman-Tarjan algorithm
aliases:
- Fibonacci-heap MST algorithm
area: graphs/spanning-trees
level: advanced
summary: Borůvka and Prim steps on Fibonacci heaps, O(m β(m,n)) time.
solves: [minimum-spanning-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, "β(m, n)": the number of times log must be applied to n to reach m/n or less}
  time: {worst: "O(m β(m, n))"}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [prim, boruvka, fibonacci-heap, cut-property, iterated-logarithm]
see_also: [prim, boruvka, karger-klein-tarjan-mst, chazelle-mst, pettie-ramachandran-mst, generic-mst-method, fibonacci-heap, kruskal]
sources:
  - paper: doi:10.1145/28869.28874
    title: "Michael L. Fredman and Robert E. Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3) (1987), 596-615"
    locator: the section on minimum spanning trees (the phases with the heap limit k = 2^(2m/t) and the O(m β(m, n)) bound)
  - paper: doi:10.1007/BF02579168
    title: "Harold N. Gabow, Zvi Galil, Thomas Spencer and Robert E. Tarjan, Efficient algorithms for finding minimum spanning trees in undirected and directed graphs, Combinatorica 6(2) (1986), 109-122"
    locator: the sections on undirected graphs (packets of edges, which improve the bound to O(m log β(m, n)))
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 21, Minimum Spanning Trees (Prim's algorithm with a Fibonacci heap, and the chapter notes on faster algorithms)
---

The Fredman-Tarjan algorithm finds a [minimum spanning tree](/minimum-spanning-tree/) in $O(m \, \beta(m, n))$ time, where $\beta(m, n)$ is the number of times the logarithm must be applied to $n$ before the result is at most $m/n$. It mixes [Prim's algorithm](/prim/) and [Borůvka's algorithm](/boruvka/). Each phase grows many small trees one after another, Prim style, with a [Fibonacci heap](/fibonacci-heap/), but stops each tree as soon as its heap holds more than $k$ vertices, so that every heap stays small. Then it contracts every tree to one vertex, as in a Borůvka round, and starts the next phase with a much larger limit. Since $\beta(m, n) \le \log^* n$, and $\beta(m, n) = 1$ once $m \ge n \log n$, the bound is linear for all but very sparse graphs. Fredman and Tarjan gave it in 1984 as an application of Fibonacci heaps.

## In plain words

Prim's algorithm grows one tree from one starting point, and keeps a list of the points next to the tree, sorted by the cheapest road to each. The cost comes from that list: when it grows long, each step to pick the cheapest point gets slower.

This algorithm never lets the list grow long. It grows a tree only until its list holds more than a fixed number of points, then starts a new tree elsewhere. If a tree runs into an earlier tree, it joins it and stops. When every point is in some tree, each tree is squeezed into a single point, and the work repeats on the much smaller network, with a much longer list allowed. After a few rounds, one tree covers everything.

## The problem

The input is an undirected graph with $n$ vertices, $m$ edges and a real weight on each edge. Weights may tie; the implementation breaks ties by the edge index, so that all keys are distinct. The graph need not be [connected](/connected-graph/); then the algorithm returns a minimum [spanning forest](/spanning-forest/). Parallel edges and self-loops are allowed. The output is a set of edges of least total weight among the spanning forests.

## The algorithm

Here $F$ is the set of chosen edges, $t$ is the number of vertices of the current graph, and $m$ is fixed: the number of edges of the input after loops and parallel edges are removed.

```pseudo id=main
FREDMAN-TARJAN(G)
L1  while the current graph has an edge do                         ▷ one phase
L2      k ← 2^(2m/t)                                               ▷ the heap limit of this phase
L3      for each vertex v0 that has an edge and is in no tree of this phase do
L4          T ← {v0}; H ← a Fibonacci heap of the neighbours x of T, keyed by the lightest edge from T to x
L5          while H is not empty do
L6              (u, e) ← EXTRACT-MIN(H); F ← F ∪ {e}
L7              if u is in an earlier tree of this phase then T joins that tree; stop growing T
L8              add u to T; INSERT or DECREASE-KEY each neighbour of u outside T; if |H| > k then stop growing T
L9          if T joined no earlier tree then T is a new tree
L10     contract each tree to one vertex; drop loops; keep the lightest of each set of parallel edges
L11 return F
```

Lines L4 to L8 are Prim's algorithm with a limit. Line L10 is the contraction step of Borůvka's algorithm. The limit $k$ is the heart of the method: with at most $k$ vertices in a heap, each EXTRACT-MIN costs $O(\log k)$ amortized time, and DECREASE-KEY costs $O(1)$.

## Example

The graph has the vertices $a$ to $f$ and the edges $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$, so $m = 9$ and $t = 6$. The rule of line L2 gives $k = 2^{18/6} = 8$, larger than any heap can be, so the first phase is Prim's algorithm from $a$ and finds the tree at once. To show the phases, take $k = 1$ instead.

**Phase 1, $k = 1$.**

| tree from | heap after the start | steps | why it stops | label |
|---|---|---|---|---|
| $a$ | $b{:}4$, $c{:}3$ | take $ac$; the heap becomes $b{:}1$, $d{:}4$, $e{:}5$ | heap size $3 > 1$ | tree 1 $= \{a, c\}$ |
| $b$ | $a{:}4$, $c{:}1$, $d{:}2$ | take $bc$; $c$ is in tree 1 | joined tree 1 | tree 1 |
| $d$ | $b{:}2$, $c{:}4$, $e{:}7$, $f{:}6$ | take $bd$; $b$ is in tree 1 | joined tree 1 | tree 1 |
| $e$ | $c{:}5$, $d{:}7$, $f{:}2$ | take $ef$; the heap becomes $c{:}5$, $d{:}6$ | heap size $2 > 1$ | tree 2 $= \{e, f\}$ |

After phase 1, $F = \{ac, bc, bd, ef\}$, and contraction leaves two vertices, $\{a, b, c, d\}$ and $\{e, f\}$. Between them run $ce = 5$, $de = 7$ and $df = 6$; line L10 keeps only $ce$.

**Phase 2.** The tree from the first vertex takes $ce$, and the heap runs empty. The result is $F = \{ac, bc, bd, ef, ce\}$, of weight 13, the minimum spanning tree.

## Correctness

**Theorem.** For every finite undirected graph, the algorithm stops, and it returns a minimum spanning forest.

Order the edges by (weight, index). The key step is that each edge taken at line L6 is the lightest edge that leaves the set of input vertices behind the tree $T$. The heap holds every neighbour of $T$ keyed by its lightest edge to $T$, and line L10 keeps, between each two contracted vertices, the lightest input edge between their sets, so nothing lighter is hidden. By the [cut property](/cut-property/), the edge is in the minimum spanning forest. The edges of one phase join the vertices of each label into one tree, so contraction is sound. Each tree takes at least one edge, so each phase at least halves the number of vertices with edges, and the loop stops. At the end, no edge joins two contracted sets, so $F$ spans each component. The heap limit plays no part in correctness; it only bounds the time. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM, with weights that are only compared.

- **One phase.** Building the adjacency lists and line L10 take $O(m)$ time with a bucket sort or hashing. Each edge causes at most one INSERT or DECREASE-KEY from each end, which is $O(m)$ amortized. Each of the $t$ vertices is extracted at most once, and every extraction except the first of each tree happens while the heap holds at most $k$ vertices, because a tree stops as soon as its heap passes $k$. The first extraction sees at most $d$ vertices, where $d$ is the degree of the start vertex, and costs $O(\log d) \le O(d)$, which sums to $O(m)$ over all trees. So each EXTRACT-MIN costs $O(\log k)$ amortized, and together they cost $O(t \log k) = O(t \cdot 2m/t) = O(m)$. So each phase takes $O(m)$ time.
- **Few vertices remain.** A label that still has edges after a phase started with a tree that stopped with more than $k$ vertices in its heap, so it has more than $k$ edge ends. Hence at most $2m/k$ vertices remain, and the next limit is $2^{2m/t'} \ge 2^k$.
- **Few phases.** The limit grows as a tower of twos from $2^{2m/n}$. Once it reaches the number of vertices, the phase grows each tree to a whole component and is the last. This takes at most $\beta(m, n) + 1$ phases, where $\beta(m, n) = \min\{i : \log^{(i)} n \le m/n\}$.
- **Total.** $O(m \, \beta(m, n))$ time in the worst case, and $O(n + m)$ space.

| claim | bound | case |
|---|---|---|
| time | $O(m \, \beta(m, n))$ | worst |
| phases | at most $\beta(m, n) + 1 \le \log^* n + 1$ | every input |
| time when $m \ge n \log n$ | $O(m)$ | worst |
| extra space | $O(n + m)$ | worst |

Prim's algorithm with a Fibonacci heap takes $O(m + n \log n)$, which is the same as this bound when $m \ge n \log n$; the gain is on sparse graphs, where it replaces $\log n$ by $\beta(m, n)$.

## Properties

- **Deterministic** and comparison-based.
- **Ties and forests.** Ties are broken by the edge index, and a disconnected graph gives a minimum spanning forest.
- **Not in place.** Each phase builds a new contracted graph.
- **Uses amortization.** The bound relies on the amortized costs of the Fibonacci heap; a [binary heap](/binary-heap/) makes DECREASE-KEY cost $O(\log k)$ and loses the bound.

## Variants and improvements

- **Packets of edges.** Gabow, Galil, Spencer and Tarjan (1986) group the edges at each vertex into packets and keep only the lightest edge of a packet in the heap, which brings the bound to $O(m \log \beta(m, n))$.
- **Randomized linear time.** The [Karger-Klein-Tarjan algorithm](/karger-klein-tarjan-mst/) combines Borůvka steps with random sampling and linear-time verification, for expected $O(m)$ time.
- **The inverse Ackermann bound.** [Chazelle's algorithm](/chazelle-mst/) runs in $O(m \, \alpha(m, n))$ time with soft heaps, and the [Pettie-Ramachandran algorithm](/pettie-ramachandran-mst/) is optimal for the comparison model, with an unknown bound.
- **Borůvka phases first.** Running a few [Borůvka](/boruvka/) rounds first lowers $n$ and raises $m/n$, which lowers $\beta(m, n)$.

## When to use it

It is mostly of theoretical interest: it was the first algorithm to beat $O(m \log \log n)$ on sparse graphs, and it shows how a limit on heap sizes turns a Fibonacci heap into nearly linear time. In practice, Kruskal's algorithm on sorted edges, Prim's algorithm with a binary heap, or Borůvka's algorithm are simpler and faster on real graphs, where $\log n$ is small.

## Pitfalls

- **A tree that takes no edge.** If the size test runs before the first extraction, a vertex whose degree exceeds $k$ becomes a tree with no edge, and with a small fixed $k$ the phase can make no progress at all. Test the size after each insertion, as in line L8, so that every tree takes at least one edge.
- **A limit from the current edge count.** The limit must use the number of edges of the input, not of the current graph. With the current count, the limit need not grow from phase to phase, and the bound on the number of phases fails.
- **Skipping the cleaning step.** Without removing loops and parallel edges at line L10, the contracted graph keeps up to $m$ edges between few vertices, and the scans and heaps fill with useless entries.
- **Joining without stopping.** When a tree reaches an earlier tree of the same phase, it must take the edge and stop. Growing on through the earlier tree's vertices would mix two trees in one heap.
- **Finished components.** A tree whose heap runs empty is a whole component; drop it from later phases, or it inflates $t$ and lowers the next limit.

## Implementations

## History

Michael Fredman and Robert Tarjan introduced Fibonacci heaps at FOCS 1984 and, in the same paper, published in the Journal of the ACM in 1987, used them for this minimum spanning tree algorithm with the bound $O(m \, \beta(m, n))$. Gabow, Galil, Spencer and Tarjan improved it to $O(m \log \beta(m, n))$ in 1986. These were the best deterministic bounds until Chazelle's $O(m \, \alpha(m, n))$ algorithm of 2000.

## References
