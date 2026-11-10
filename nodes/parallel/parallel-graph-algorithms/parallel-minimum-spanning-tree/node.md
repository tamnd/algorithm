---
tag: 8WQPZV
kind: algorithm
slug: parallel-minimum-spanning-tree
name: Parallel minimum spanning tree
aliases:
- parallel Boruvka
- parallel minimum spanning forest
area: parallel/parallel-graph-algorithms
level: advanced
summary: Borůvka-style rounds where every component picks its lightest edge in parallel, followed by contraction.
solves: [minimum-spanning-tree]
model: work-span-model
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O((n + m) log n)}
  depth: {worst: O(log^2 n)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [boruvka, cut-property, graph-contraction, pointer-jumping, parallel-pack]
see_also: [minimum-spanning-tree, kruskal, prim, shiloach-vishkin, random-mate-contraction, karger-klein-tarjan-mst, pettie-ramachandran-mst, mst-uniqueness]
sources:
  - paper: "Otakar Borůvka, O jistém problému minimálním, Práce Moravské přírodovědecké společnosti 3, 1926"
    title: O jistém problému minimálním (On a certain minimal problem)
    locator: pp. 37 to 58 (the method of joining every fragment to its nearest neighbour)
  - paper: doi:10.1109/TC.1987.1676868
    title: Baruch Awerbuch and Yossi Shiloach, New connectivity and MSF algorithms for shuffle-exchange network and PRAM, IEEE Transactions on Computers C-36(10), 1987
    locator: pp. 1258 to 1263 (minimum spanning forests by hooking along the lightest edges, O(log n) time on the CRCW PRAM)
  - paper: doi:10.1145/237502.237563
    title: Richard Cole, Philip N. Klein and Robert E. Tarjan, Finding minimum spanning forests in logarithmic time and linear work using random sampling, SPAA 1996
    locator: the randomized algorithm with O(m) expected work and O(log n 2^(log* n)) time; time bound to be checked
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 5, the section on minimum spanning trees; section number to be checked
---

Parallel Borůvka computes a minimum spanning forest by rounds of [Borůvka's](/boruvka/) step done in parallel: every supervertex picks the lightest edge that leaves it, the picked edges join the supervertices into trees, and each tree is contracted to one supervertex. Every supervertex with an edge merges with at least one other, so the number of supervertices with edges at least halves in each round, and there are at most $\lceil \log_2 n \rceil$ rounds. In the [work-span model](/work-span-model/) this gives $O((n + m) \log n)$ work and $O(\log^2 n)$ span, deterministic and in the worst case.

Notation on this page: $G = (V, E)$ is an undirected graph with $n$ vertices, $m$ edges and real weights $w$; parallel edges are allowed. $W$ is the work, $S$ the span and $T_p$ the time on $p$ processors. The model is the work-span model with binary forking; a minimum over a set of $k$ values costs $O(k)$ work and $O(\log k)$ span. Edge $i$ has the key $(w_i, i)$, and edges are compared by key, so no two keys are equal and the [minimum spanning forest is unique](/mst-uniqueness/). For distinct weights it is the usual one; with ties it is the one that breaks ties by index.

## In plain words

Think of every vertex as a small town. Each town builds the cheapest road that leaves it. All towns do this at the same moment.

Each new road joins two towns, so after the step the towns form groups linked by the new roads. Each group becomes one bigger town, and roads inside a group are no longer needed.

Every town with a road joins at least one other town, so the number of towns falls at least by half in each step. After a number of steps that grows with the logarithm of the number of towns, no two towns are left with a road between them.

Each road that a town picks is the cheapest way out of that town, and a cheapest way out of any group of towns is always part of some best network. So the roads picked over all steps form the cheapest network.

## The problem

The input is $G$ as a list of weighted edges. The output is the [minimum spanning forest](/minimum-spanning-tree/): a set $F$ of edges with no cycle, with the same connected components as $G$, and with the least total weight; with the keys above it is unique.

## The algorithm

A supervertex is a set of original vertices joined by edges of $F$, named by one of them. $E$ is the list of edges between different supervertices, with their endpoints renamed to the names of the supervertices and their keys kept.

```pseudo id=main
PARALLEL-BORUVKA(V, E)
L1  F ← ∅
L2  while E is not empty do
L3      for all v in V in parallel do best[v] ← the edge of least key among the edges of E at v
L4      for all v in V in parallel do P[v] ← the other end of best[v]
L5      for all v in V in parallel do if P[P[v]] = v and v < P[v] then P[v] ← v     ▷ break each 2-cycle
L6      for all v in V with P[v] ≠ v in parallel do add best[v] to F
L7      repeat P[v] ← P[P[v]] for all v in V in parallel, until no P changes          ▷ pointer jumping
L8      E ← the edges (P[u], P[v]) of E with P[u] ≠ P[v], with their keys            ▷ pack
L9      V ← the vertices that are ends of an edge of E
L10 return F
```

Following $P$ from $v$ after line L4, the keys of the picked edges never grow: $best[P[v]]$ is at most $best[v]$, because $best[v]$ is also an edge at $P[v]$. They stay equal only if the two picked edges are the same edge, so the only cycles of $P$ are 2-cycles of two vertices that picked the same edge. Line L5 makes the smaller of the two a root, so $P$ is a forest, and every vertex that is not a root adds its own picked edge in line L6, which adds the edge of a 2-cycle once. Line L9 drops supervertices with no edges left; they are finished components.

## Example

The graph has the vertices 0 to 5 and the edges $\{0,1\}$ of weight 4, $\{1,2\}$: 2, $\{2,3\}$: 6, $\{3,4\}$: 3, $\{4,5\}$: 1, $\{5,0\}$: 5 and $\{1,4\}$: 7.

| round | $v$ | $best[v]$ | $P[v]$ after L5 | added to $F$ |
|---|---|---|---|---|
| 1 | 0 | $\{0,1\}$: 4 | 1 | $\{0,1\}$ |
| 1 | 1 | $\{1,2\}$: 2 | 1 (2-cycle with 2, root) | |
| 1 | 2 | $\{1,2\}$: 2 | 1 | $\{1,2\}$ |
| 1 | 3 | $\{3,4\}$: 3 | 4 | $\{3,4\}$ |
| 1 | 4 | $\{4,5\}$: 1 | 4 (2-cycle with 5, root) | |
| 1 | 5 | $\{4,5\}$: 1 | 4 | $\{4,5\}$ |
| 2 | 1 | $\{5,0\}$: 5 | 1 (2-cycle with 4, root) | |
| 2 | 4 | $\{5,0\}$: 5 | 1 | $\{5,0\}$ |

After round 1 the supervertices are $\{0, 1, 2\}$ named 1 and $\{3, 4, 5\}$ named 4. The edges $\{2,3\}$, $\{5,0\}$ and $\{1,4\}$ become three parallel edges between 1 and 4, and both supervertices pick the lightest, $\{5,0\}$. After round 2, $E$ is empty. $F$ has total weight $4 + 2 + 3 + 1 + 5 = 15$, the same as [Kruskal's algorithm](/kruskal/) gives. The 6 vertices took 2 rounds, within $\lceil \log_2 6 \rceil = 3$.

## Correctness

The proof file proves, in full, the invariant that $F$ is a subset of the minimum spanning forest $M$ and that the supervertices are the components of $(V, F)$. In each round, $best[v]$ is the lightest edge of $G$ that leaves the supervertex $v$, because every edge of $G$ that leaves it is still in $E$; by the [cut property](/cut-property/) it is in $M$. The picked edges join supervertices along the trees of $P$, so the supervertices stay the components of $F$. When $E$ is empty, no edge of $M$ joins two components of $F$, so $M \subseteq F$, and $F = M$.

## Complexity

The model is the work-span model. Let $n_t$ be the number of supervertices with an edge at the start of round $t$, and $m_t \le m$ the number of edges.

- **Rounds.** Every vertex of $V$ is in a tree of $P$ with at least one other vertex: a vertex that is not a root points to another, and a root $r$ of line L5 is the target of its 2-cycle partner. So $n_{t+1} \le n_t / 2$, and as $n_1 \le n$, there are at most $\lceil \log_2 n \rceil$ rounds for $n \ge 1$. The proof file proves this bound.
- **One round.** The minima of line L3 are a grouped reduction over $2 m_t$ arc entries: $O(m_t + n_t)$ work and $O(\log n)$ span. Lines L4 to L6 cost $O(n_t)$ work and $O(1)$ span. The trees of $P$ can be paths, so [pointer jumping](/pointer-jumping/) takes up to $\lceil \log_2 n_t \rceil$ steps of $O(n_t)$ work. The [pack](/parallel-pack/) of line L8 and the vertex set of line L9 cost $O(m_t + n_t)$ work and $O(\log n)$ span.
- **Total.** Summing over the rounds, the pointer jumping costs $\sum_t n_t \log n_t \le 2 n \log_2 n$, because the $n_t$ halve, and the edge steps cost $O(m)$ in each of $O(\log n)$ rounds, because the number of edges need not fall. So

$$W = O((n + m) \log n), \qquad S = O(\log^2 n).$$

By [Brent's theorem](/brent-theorem/), $T_p = O((n + m) \log n / p + \log^2 n)$. For $m \ge n$ this matches the $O(m \log n)$ time of sequential [Kruskal](/kruskal/) and of [Prim](/prim/) with a binary heap, but it is not work-efficient against the linear expected time of [Karger, Klein and Tarjan](/karger-klein-tarjan-mst/). In the tests, on random graphs with $3n$ edges, the mean number of rounds is 2.9 for $n = 64$, 3.9 for $n = 256$ and 4.4 for $n = 1{,}024$: well under the $\lceil \log_2 n \rceil$ bound, because most supervertices merge with more than one other.

## Properties

- **Deterministic.** With the keys $(w_i, i)$, the output is the same for every schedule.
- **Exact halving in the worst case.** A path whose lightest edges form a perfect matching in every round, for example the path on $2^k$ vertices with the weight of edge $\{i, i+1\}$ equal to the number of trailing zero bits of $i + 1$, keeps every tree of $P$ at size 2, so it needs exactly $k = \log_2 n$ rounds.
- **Forest output.** On a disconnected graph the result is a minimum spanning forest, one tree for each component.
- **Parallel edges.** Contraction makes parallel edges, and the algorithm needs no step to remove them; only the lightest one between two supervertices can be picked.

## Variants and improvements

- **Constant time per round on the CRCW PRAM.** Awerbuch and Shiloach hook stars along the lightest edges in the style of [Shiloach-Vishkin](/shiloach-vishkin/), with $O(1)$ time per iteration and $O(\log n)$ iterations, so $O(\log n)$ time.
- **Removing parallel edges.** Keeping only the lightest edge between each pair of supervertices bounds $m_t$ by $n_t^2$ and makes the late rounds cheaper on dense graphs. It needs a sort or a hash of the edges by their pair of ends in each round.
- **Random sampling.** Cole, Klein and Tarjan (1996) combine Borůvka rounds with the random sampling of [Karger, Klein and Tarjan](/karger-klein-tarjan-mst/) to get $O(m)$ expected work with a time bound close to $O(\log n)$. [Pettie and Ramachandran](/pettie-ramachandran-mst/) give a randomized algorithm that is optimal in both time and work on the EREW PRAM.
- **Star contraction.** With [random-mate](/random-mate-contraction/) coins, a tails supervertex joins along its lightest edge only when the other end is heads. The blocks are stars, so no pointer jumping is needed; a supervertex merges with probability at least $1/4$, which gives $O(\log n)$ expected rounds of $O(\log n)$ span each.

## When to use it

Use it to compute a minimum spanning forest on a multicore or a distributed machine. The rounds are few and each is a reduction, a few array steps and a pack, which parallelize well. It is also the base step of the fastest randomized algorithms. On one core, [Kruskal](/kruskal/) with a fast sort or [Prim](/prim/) with a heap is simpler.

## Pitfalls

- **Ties without a tie-break.** With equal weights and no rule, two supervertices can pick different edges of the same weight that close a cycle, for example three vertices joined in a triangle of equal weights where each picks the edge to its right. The keys $(w_i, i)$ prevent this.
- **Adding both edges of a 2-cycle.** Two supervertices that pick the same edge must add it once. Line L5 makes one of them a root and only non-roots add an edge.
- **No rule for the root of a 2-cycle.** If both ends of a 2-cycle become roots, the shared edge is not added and the two supervertices do not merge. If neither does, $P$ keeps a cycle and pointer jumping never ends. The test $v < P[v]$ picks exactly one end.
- **Removing isolated supervertices too early.** A supervertex with no edges is a finished component, but its vertices still need their pointers if the caller wants component labels; keep the label array of every original vertex.
- **Counting on the edges to fall.** The number of supervertices halves, but the number of edges between them does not have to, so each round can cost $\Theta(m)$.

## Implementations

## History

Borůvka (1926) gave the method of joining every fragment to its nearest neighbour, for the design of an electric network in Moravia, and Sollin rediscovered it later; it is the oldest minimum spanning tree algorithm. Its rounds are independent across fragments, which makes it the natural parallel method. Awerbuch and Shiloach (1987) gave an $O(\log n)$ time CRCW PRAM algorithm for minimum spanning forests by hooking along the lightest edges. Cole, Klein and Tarjan (1996) reached linear expected work with random sampling.

## References
