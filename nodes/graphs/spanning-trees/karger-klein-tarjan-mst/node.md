---
tag: YYGGT8
kind: algorithm
slug: karger-klein-tarjan-mst
name: Karger-Klein-Tarjan algorithm
aliases:
- randomized linear-time MST
- KKT algorithm
area: graphs/spanning-trees
level: research
summary: Randomized expected linear-time MST using sampling, Borůvka steps and verification.
solves: [minimum-spanning-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {expected: O(m), worst: "O(min(n^2, m log n))"}
  space: {extra: O(n + m)}
properties: {deterministic: false, recursive: true}
prereqs: [boruvka, mst-verification, cut-property, cycle-property, las-vegas-algorithm, random-sampling]
see_also: [boruvka, mst-verification, fredman-tarjan-mst, chazelle-mst, pettie-ramachandran-mst, las-vegas-algorithm, expected-running-time, binary-lifting]
sources:
  - paper: doi:10.1145/201019.201022
    title: "David R. Karger, Philip N. Klein and Robert E. Tarjan, A randomized linear-time algorithm to find minimum spanning trees, Journal of the ACM 42(2) (1995), 321-328"
    locator: the whole paper (the algorithm, the sampling lemma and the expected O(m) bound)
  - paper: doi:10.1007/BF02526037
    title: "Valerie King, A simpler minimum spanning tree verification algorithm, Algorithmica 18(2) (1997), 263-270"
    locator: the whole paper (linear-time verification on the word RAM, which the algorithm needs for line L5)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press (1995)
    locator: Chapter 10, Graph Algorithms (Section 10.3, Minimum Spanning Trees, the random sampling lemma and the analysis)
---

The Karger-Klein-Tarjan algorithm finds a [minimum spanning tree](/minimum-spanning-tree/) in $O(m)$ expected time. It is a [Las Vegas algorithm](/las-vegas-algorithm/): its answer is always correct, and only its running time depends on coin flips. It combines three ideas: [Borůvka](/boruvka/) steps, which cut the number of vertices by a factor of four; [random sampling](/random-sampling/) of half the edges, whose minimum spanning forest $F$ is found recursively; and [MST verification](/mst-verification/), which throws away every edge that is heavier than all edges of its path in $F$, since the [cycle property](/cycle-property/) shows such an edge is in no minimum spanning tree. The key lemma says that only about $2n$ edges survive the filter in expectation, so both recursive calls are small. Among algorithms that only compare weights, it is still the only known one that runs in linear time, in expectation, on all graphs.

## In plain words

You want the cheapest network that joins many towns, and you have far more possible roads than towns. Most of these roads are useless, and the trick is to throw them away quickly.

Flip a coin for each road and keep the roads that come up heads. Find the cheapest network for this half, which is a smaller problem. That network already tells you a lot: if some road is more expensive than every road on the network's route between its two towns, it is never needed. It turns out that only a few roads, about twice the number of towns, can survive this test, so the rest of the work is small. Before each sampling, merge each town with its cheapest neighbour, twice, so that the number of towns also drops fast.

## The problem

The input is an undirected graph with $n$ vertices, $m$ edges and a real weight on each edge. Weights may tie; the algorithm breaks ties by the edge index, so that all keys are distinct and the minimum spanning forest is unique. The graph need not be [connected](/connected-graph/); then the output is the minimum [spanning forest](/spanning-forest/). Parallel edges and self-loops are allowed. The model is the word RAM with random bits: weights are only compared, and the algorithm may flip fair coins.

## The algorithm

```pseudo id=main
KKT(G)
L1  if G has no edges then return ∅
L2  run two Borůvka steps: each vertex picks its lightest edge, C ← the picked edges, contract them; G' ← the contracted graph
L3  H ← each edge of G' kept independently with probability 1/2
L4  F ← KKT(H)                                                ▷ a minimum spanning forest of the sample
L5  G'' ← G' without its F-heavy edges                         ▷ heavier than every edge on their path in F
L6  return C ∪ KKT(G'')
```

An edge $(u, v)$ is *$F$-heavy* when $u$ and $v$ are in the same tree of $F$ and the edge is heavier than every edge of the path between them in $F$; otherwise it is *$F$-light*. The edges of $F$ are $F$-light. Line L5 needs a linear-time verification algorithm, such as King's (1997), which finds the heaviest edge on each of $m$ tree paths in $O(n + m)$ time. Line L2 also removes self-loops and vertices left without edges. Parallel edges may remain.

## Example

The graph has the vertices $a$ to $f$ and the edges $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$.

**Line L2 finishes the job here.** In the first Borůvka step, $a$ picks $ac$, $b$ and $c$ pick $bc$, $d$ picks $bd$, and $e$ and $f$ pick $ef$. Contracting leaves two vertices, $\{a, b, c, d\}$ and $\{e, f\}$, joined by $ce = 5$, $de = 7$ and $df = 6$. In the second step both pick $ce$, and no edge is left. So $C = \{ac, bc, bd, ef, ce\}$, of weight 13, is the answer, on every run.

**The filter of line L5.** To see the sampling step, apply it to the whole graph. Suppose the coins keep $H = \{bc, cd, ce, de, ef\}$. Its minimum spanning forest is $F = \{bc, cd, ce, ef\}$, since $de$ closes the cycle $c, d, e$ and is heaviest there; $a$ is alone in $F$. Now test each edge of $G$ against $F$:

| edge | path in $F$ | heaviest on the path | verdict |
|---|---|---|---|
| $ab = 4$, $ac = 3$ | none: $a$ is in another tree | | light |
| $bd = 2$ | $b, c, d$ | $cd = 4$ | light |
| $de = 7$ | $d, c, e$ | $ce = 5$ | heavy |
| $df = 6$ | $d, c, e, f$ | $ce = 5$ | heavy |
| $bc$, $cd$, $ce$, $ef$ | the edge itself | itself | light |

The filter removes $de$ and $df$, which are indeed in no minimum spanning tree, and the second recursive call works on the 7 edges left.

## Correctness

**Theorem.** On every sequence of coin flips, KKT stops and returns the unique minimum spanning forest for the order by (weight, index).

1. *Borůvka steps.* The lightest edge at a vertex is in the minimum spanning forest, by the [cut property](/cut-property/). Contracting a set $C$ of such edges gives $\mathrm{MSF}(G) = C \cup \mathrm{MSF}(G')$.
2. *Filtering.* $F$ is a set of edges of $G'$. An $F$-heavy edge is the heaviest edge of the cycle it closes with its path in $F$, so by the cycle property it is not in $\mathrm{MSF}(G')$, and removing it does not change $\mathrm{MSF}(G')$. Whatever the sample is, $\mathrm{MSF}(G'') = \mathrm{MSF}(G')$.
3. *Termination.* The first Borůvka step at least halves the number of vertices that have edges, and both recursive calls run on subgraphs of $G'$, so the recursion is well founded.

The sample only affects how many edges survive the filter, never which forest is returned. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM with random bits.

**The sampling lemma.** Let $H$ contain each edge of a graph with $n$ vertices independently with probability $p$, and let $F = \mathrm{MSF}(H)$. Then the expected number of $F$-light edges is at most $n/p$.

*Proof sketch.* Flip the coins lazily while running [Kruskal's algorithm](/kruskal/) on all edges in increasing order, adding an edge to $F$ only when its coin says it is in $H$ and it joins two trees of the current $F$. An edge is $F$-light exactly when it joins two trees at the moment it is examined, which does not depend on its own coin. Each such edge then enters $F$ with probability $p$, independently of the past. Since $F$ has at most $n - 1$ edges, the number of $F$-light edges is at most the number of coin flips needed to see $n - 1$ heads, whose expectation is $(n - 1)/p$. $\square$

**The recurrence.** One call on $n$ vertices and $m$ edges does $O(n + m)$ work outside the recursion, with linear-time verification. After line L2, $G'$ has at most $n/4$ vertices and at most $m$ edges. The sample has $m/2$ edges in expectation, and by the lemma with $p = 1/2$, $G''$ has at most $2 \cdot n/4 = n/2$ edges in expectation. So the expected time satisfies

$$T(n, m) \le T(n/4, m/2) + T(n/4, n/2) + c(n + m),$$

whose solution is $T(n, m) = O(n + m)$: the total edge count over the recursion tree is $O(m + n)$, because the left branch halves the edges and the right branch replaces them by at most half the vertices. Isolated vertices are removed, so $n \le 2m$, and the bound is $O(m)$.

**Worst case.** The coins could keep every edge in the worst case. The recursion still has the structure of Borůvka's algorithm, which gives $O(m \log n)$, and a separate count gives $O(n^2)$, so $O(\min(n^2, m \log n))$ in the worst case, the same as the deterministic bounds of Borůvka's algorithm. The probability of exceeding linear time by more than a constant factor is exponentially small in $m$.

**The implementation.** The Python version replaces King's linear-time verification by [binary lifting](/binary-lifting/), which costs $O((n + m) \log n)$ per call, so it runs in $O(m \log n)$ expected time; it shows the structure, not the bound.

| claim | bound | case |
|---|---|---|
| time | $O(m)$ | expected |
| time | $O(\min(n^2, m \log n))$ | worst |
| $F$-light edges for sampling probability $p$ | at most $n/p$ | expected |
| extra space | $O(n + m)$ | expected |

## Properties

- **Las Vegas.** Always correct; only the running time is random.
- **Ties and forests.** Ties are broken by the edge index, and a disconnected graph gives a minimum spanning forest.
- **Comparison-based.** Weights are only compared, so the algorithm works for any totally ordered weights. Linear verification uses table lookups on small words, which the word RAM allows.
- **Recursive.** Two recursive calls per level, on graphs a quarter of the size in vertices.

## Variants and improvements

- **Deterministic algorithms.** [Chazelle's algorithm](/chazelle-mst/) runs in $O(m \, \alpha(m, n))$ deterministic time, and the [Pettie-Ramachandran algorithm](/pettie-ramachandran-mst/) is optimal among deterministic comparison-based algorithms, with an unknown running time between $\Omega(m)$ and $O(m \, \alpha(m, n))$.
- **Parallel versions.** Cole, Klein and Tarjan gave a parallel version with linear expected work and polylogarithmic time.
- **Fewer random bits.** Later work reduces the number of random bits the algorithm needs.
- **Other uses of the sampling lemma.** The same lemma speeds up other problems that have a verification step, such as some matroid optimization problems.
- **Simpler verification.** In practice, an $O(m \log n)$ verification, as in the implementation, or skipping verification in favour of [Kruskal's](/kruskal/) or Prim's algorithm on the light edges, is simpler.

## When to use it

It is the reference for the claim that minimum spanning trees can be found in expected linear time, and its sampling lemma is a standard tool. In practice, the constant factors of linear-time verification make it slower than [Kruskal's](/kruskal/), [Prim's](/prim/) or [Borůvka's](/boruvka/) algorithms on real graphs. A simplified version, sampling plus a filter with a simple verification, can help for very dense graphs, where most edges are filtered away cheaply.

## Pitfalls

- **Filtering by a forest of the wrong graph.** $F$ must be a minimum spanning forest of a subgraph of the same graph $G'$ that is filtered. The cycle argument needs the path of $F$ to be made of edges of $G'$.
- **Dropping light edges with equal weight.** With ties, an edge whose weight equals the path maximum may be needed. Compare full keys (weight, index), and drop an edge only when it is strictly heavier than the path maximum.
- **Skipping the Borůvka steps.** Without them, the second call works on up to $2n$ edges and $n$ vertices, and the recursion does not shrink fast enough for linear time.
- **Isolated vertices.** After contraction, vertices without edges must be dropped, or $n$ stays large while $m$ shrinks, and the bound is lost.
- **Expecting the same running time on every run.** Only the expectation is linear; for a fixed input the time varies with the coins.

## Implementations

## History

David Karger introduced the random sampling idea for minimum spanning trees in 1993. Philip Klein and Robert Tarjan combined it with Borůvka steps and the linear-time verification of Dixon, Rauch and Tarjan, which builds on Komlós's linear comparison bound, in a STOC 1994 paper, and the three authors published the journal version in 1995. King's 1997 verification algorithm made the verification step simpler. The algorithm is a standard example in Motwani and Raghavan's textbook.

## References
