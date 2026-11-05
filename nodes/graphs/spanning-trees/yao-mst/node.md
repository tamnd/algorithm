---
tag: CXZBFW
kind: algorithm
slug: yao-mst
name: Yao's minimum spanning tree algorithm
aliases:
- Yao MST algorithm
area: graphs/spanning-trees
level: research
summary: Deterministic MST algorithm with O(m log log n) running time.
solves: [minimum-spanning-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m log log n + n), best: Ω(n + m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1975
  people: [Andrew Chi-Chih Yao]
  note: Yao published the method in Information Processing Letters in 1975, the first MST algorithm to beat O(m log n) on sparse graphs.
prereqs: [boruvka, median-of-medians, disjoint-set, cut-property]
see_also: [boruvka, fredman-tarjan-mst, karger-klein-tarjan-mst, chazelle-mst, pettie-ramachandran-mst, kruskal, prim, graph-contraction]
sources:
  - paper: doi:10.1016/0020-0190(75)90056-3
    title: Andrew Chi-Chih Yao, An O(|E| log log |V|) algorithm for finding minimum spanning trees, Information Processing Letters 4(1) (1975), 21-23
    locator: the whole paper (the split of each edge list into groups by linear-time selection, and the Borůvka phases over the groups)
  - paper: doi:10.1137/0205051
    title: David Cheriton and Robert Endre Tarjan, Finding minimum spanning trees, SIAM Journal on Computing 5(4) (1976), 724-742
    locator: the whole paper (another O(m log log n) method, with mergeable heaps, and a discussion of Yao's method)
  - paper: doi:10.1016/S0022-0000(73)80033-9
    title: Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest and Robert E. Tarjan, Time bounds for selection, Journal of Computer and System Sciences 7(4) (1973), 448-461
    locator: the linear-time selection algorithm used to split the edge lists
---

Yao's algorithm finds a [minimum spanning tree](/minimum-spanning-tree/) in $O(m \log \log n)$ time on a graph with $n$ vertices and $m$ edges. It is [Borůvka's algorithm](/boruvka/) with one change: before the phases, the edges at each vertex are split into about $\log n$ groups of increasing weight by [linear-time selection](/median-of-medians/), so that a phase can find the lightest edge leaving a vertex by looking at one small group instead of the whole list. Published in 1975, it was the first algorithm to beat the $O(m \log n)$ bound of the classical methods on sparse graphs. Later methods, from [Fredman and Tarjan](/fredman-tarjan-mst/) to [Chazelle](/chazelle-mst/), improved the bound further.

## In plain words

Borůvka's method works in rounds. In each round, every group of joined towns picks its cheapest road to another group, and all picked roads are built. The number of groups at least halves each round, so there are few rounds. The slow part is that each round looks at every road again.

Yao's idea is to sort the roads at each town only roughly: put them into a few piles, so that every road in a pile is cheaper than every road in the next pile. To find the cheapest useful road at a town, look only at its first pile that still has a road to another group. Roads that now join a group to itself are thrown away for good. A rough sort costs much less than a full sort, and a round now reads only small piles.

## The problem

The input is an undirected graph $G = (V, E)$ with $n$ vertices, $m$ edges and a real weight $w(e)$ on each edge. Weights may be negative and may tie. Parallel edges and self-loops are allowed, and the graph does not have to be [connected](/connected-graph/).

The output is a minimum spanning forest, which is a minimum spanning tree when $G$ is connected. Edges are compared by the pair $(w(e), \text{index of } e)$, so all keys are distinct, and the output is the unique minimum forest for this order. With ties in $w$, it is one of the minimum forests, the one that [Kruskal's algorithm](/kruskal/) returns when it breaks ties by index. Borůvka phases need distinct keys: with two equal lightest edges, two components could pick different edges between them and close a cycle.

## The algorithm

```pseudo id=main
YAO-MST(G, w)
L1  F ← ∅; compare edges by the key (w(e), index of e)
L2  run ⌈log₂ log₂ n⌉ Borůvka phases on G, adding the chosen edges to F, and contract the components
L3  let H be the contracted graph without self-loops, with n′ vertices, and let k ← max(1, ⌈log₂ n′⌉)
L4  for each vertex v of H do
L5      split the edges at v into groups L(v, 1), …, L(v, k), each key in L(v, j) below each key in L(v, j + 1), by repeated median selection
L6      c(v) ← 1
L7  while some component has an edge to another component do
L8      for each vertex v of H do
L9          let C be the component that contains v
L10         remove from L(v, c(v)) the edges with both ends in one component; while it is empty and c(v) < k, increase c(v) and repeat
L11         let e_v be the least edge in L(v, c(v)), if any
L12         if e_v is less than the best edge e_C of C so far then e_C ← e_v
L13     add every e_C to F and merge the components that they join
L14 return F
```

Line L2 is plain Borůvka: each phase scans all edges, finds the lightest edge that leaves each component, adds these edges, and merges. After $p = \lceil \log_2 \log_2 n \rceil$ phases, each component that still has an edge to another one contains at least $2^p \ge \log_2 n$ vertices, so $H$ has at most $n / \log_2 n$ vertices with edges.

Line L5 splits the list of $d$ edges at $v$ into $k$ groups of size at most about $d/k$. Find the edge of rank $\lfloor d/2 \rfloor$ by selection, split the list at it, and repeat on both halves; after $\log_2 k$ levels of $O(d)$ work each, there are $k$ groups.

Lines L7 to L13 are Borůvka phases on $H$. The components are kept in a [disjoint-set](/disjoint-set/) structure. In line L10, an edge with both ends in one component stays that way forever, so it is removed for good. Since all groups before $L(v, c(v))$ are empty and all groups after it hold larger keys, the least edge in the current group is the least edge that leaves the component at $v$.

## Example

The graph has the vertices $a$ to $f$ and nine edges, with two ties in weight that the index breaks.

| edge | $ab$ | $ac$ | $bc$ | $bd$ | $cd$ | $ce$ | $de$ | $df$ | $ef$ |
|---|---|---|---|---|---|---|---|---|---|
| weight | 4 | 3 | 1 | 2 | 4 | 5 | 7 | 6 | 2 |

With $n = 6$, line L2 would run two phases, which already finish this small graph. To show the groups, the trace skips line L2, so $H = G$, $n' = 6$ and $k = \lceil \log_2 6 \rceil = 3$. The groups of line L5, from light to heavy:

| vertex | $L(v, 1)$ | $L(v, 2)$ | $L(v, 3)$ |
|---|---|---|---|
| $a$ | | $ac$ | $ab$ |
| $b$ | $bc$ | $bd$ | $ab$ |
| $c$ | $bc$ | $ac$ | $cd, ce$ |
| $d$ | $bd$ | $cd$ | $de, df$ |
| $e$ | $ef$ | $ce$ | $de$ |
| $f$ | | $ef$ | $df$ |

| phase | vertex work in line L10 and L11 | chosen edges | components after |
|---|---|---|---|
| 1 | $a$: group 1 is empty, so $e_a = ac$; $b$: $bc$; $c$: $bc$; $d$: $bd$; $e$: $ef$; $f$: group 1 is empty, so $e_f = ef$ | $ac, bc, bd, ef$ | $\{a, b, c, d\}$, $\{e, f\}$ |
| 2 | $a$: $ac$ and then $ab$ are inside, all groups empty; $b$: all three groups empty; $c$: $bc$, $ac$, $cd$ removed, $e_c = ce$; $d$: $bd$, $cd$ removed, $e_d = df$; $e$: $ef$ removed, $e_e = ce$; $f$: $ef$ removed, $e_f = df$ | $ce$ for both components | $\{a, \ldots, f\}$ |
| 3 | no edge leaves the single component | | stop |

The result is $\{ac, bc, bd, ce, ef\}$ with weight 13, the same tree that Kruskal's and Prim's algorithms find.

## Correctness

**Theorem.** For each finite undirected graph with real weights, YAO-MST returns the minimum spanning forest for the order of the keys $(w(e), \text{index})$, which is a minimum spanning forest for $w$.

Every edge added in line L2 or line L13 is the least edge that leaves some component $C$ of the current forest. By the [cut property](/cut-property/) with distinct keys, it belongs to the unique minimum forest $F^\ast$. So $F$ together with all edges chosen in one phase lies inside the forest $F^\ast$, and the chosen edges cannot close a cycle. Line L13 skips an edge whose ends are already merged, which happens only when two components chose the same edge. So $F \subseteq F^\ast$ at all times. The loop stops when no edge leaves any component, so the components of $F$ are those of $G$, and $F = F^\ast$. The key step is that line L11 does find the least leaving edge at $v$, which holds because the groups are ordered and removed edges never leave a component again. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM with comparisons of keys in $O(1)$ time.

- **Line L2.** Each plain phase costs $O(n + m)$ when the components are relabelled by one graph search after the phase, so $p$ phases cost $O((n + m) \log \log n)$.
- **Lines L4 to L6.** Splitting a list of $d$ edges into $k$ groups costs $O(d \log k)$ by selection. Summed over $v$, this is $O(m \log k) = O(m \log \log n)$.
- **Lines L7 to L13.** Each phase at least halves the number of components that have edges, so there are at most $\log_2 n'$ phases. In one phase, the vertex $v$ reads its current group, which has $O(d(v)/k + 1)$ edges, plus the groups that it empties. Each edge is removed only once, so the removals cost $O(m)$ in total. The rest costs $O(m/k + n')$ for each phase, so $O((m/k + n') \log n') = O(m + n)$ in total, since $k \ge \log_2 n'$ and $n' \log_2 n' \le n$.

| claim | bound | case |
|---|---|---|
| time | $O(m \log \log n + n)$ | worst |
| time | $\Omega(n + m)$ | best |
| extra space | $O(n + m)$ | worst |

The term $O(n)$ matters only when $m$ is less than $n$. The best case is linear because every edge must be read.

## Properties

- **Deterministic.** The order of the keys fixes the output. No random bits are used.
- **Uses only comparisons.** The algorithm compares keys and never adds weights, so it works with any totally ordered weights.
- **Two kinds of Borůvka phase.** The first phases read every edge; the later phases read only the current groups. The switch is made when the number of vertices with edges has fallen to $n / \log n$, so the per-phase term $n'$ adds up to $O(n)$.
- **Groups are only roughly sorted.** Inside a group, edges are in no order; the algorithm pays for that with a linear scan of one small group.

## Variants and improvements

- **Cheriton and Tarjan (1976).** A different $O(m \log \log n)$ method grows components with mergeable heaps and picks the smallest component to grow next.
- **Fredman and Tarjan (1987).** [Fibonacci heaps](/fibonacci-heap/) give $O(m \beta(m, n))$, where $\beta(m, n) \le \log^\ast n$; see [Fredman-Tarjan](/fredman-tarjan-mst/).
- **Randomized linear time.** The [Karger-Klein-Tarjan](/karger-klein-tarjan-mst/) algorithm runs in expected $O(m)$ time.
- **Near-linear deterministic.** [Chazelle's algorithm](/chazelle-mst/) runs in $O(m \alpha(m, n))$, and the [Pettie-Ramachandran](/pettie-ramachandran-mst/) algorithm is optimal up to the unknown decision-tree complexity.
- **Other group counts.** Any $k$ with $\log k = O(\log \log n)$ and $k \ge \log n'$ gives the same bound. Using $k = 1$ is plain Borůvka.

## When to use it

Yao's algorithm is mostly of historical and teaching value: it shows how a rough sort can cut the cost of repeated minimum searches. In practice, [Kruskal's](/kruskal/) and [Prim's](/prim/) algorithms are simpler and fast enough, and for very large sparse graphs Borůvka or randomized methods are used. Its idea of splitting edge lists into ordered groups reappears in later MST algorithms.

## Pitfalls

- **Ties without a tie-break.** With equal weights and no index in the key, two components can pick different edges of equal weight between them and close a cycle. The test with $K_4$ and all weights 1 catches it.
- **Not removing inner edges.** If line L10 only skips edges inside a component but leaves them in the group, the same edges are read again in each phase and the time bound is lost.
- **Stopping at the first group.** If line L10 does not move on when the current group becomes empty, a vertex reports no edge while later groups still hold leaving edges. The example catches this in phase 2 at vertex $c$, whose first two groups become empty.
- **Groups out of order.** If the split does not put every key of a group below every key of the next group, line L11 can return an edge that is not the least. The split test checks the order.
- **Too few plain phases.** Without line L2, the term $O(n')$ per phase becomes $O(n \log n)$ in total; the result is still correct, which the tests check, but the bound fails on sparse graphs.
- **Expecting $n - 1$ edges.** On a disconnected graph the output has $n - c$ edges for $c$ components. The disconnected test checks this.

## Implementations

## History

Andrew Yao published the algorithm in 1975 in a three-page note in Information Processing Letters. It combined Borůvka's phases with the linear-time selection algorithm of Blum, Floyd, Pratt, Rivest and Tarjan from 1973. Cheriton and Tarjan gave another $O(m \log \log n)$ algorithm in 1976 and discussed both methods. The bound stood until Fredman and Tarjan's Fibonacci heaps in 1984 to 1987.

## References
