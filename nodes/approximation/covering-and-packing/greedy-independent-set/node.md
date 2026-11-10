---
tag: V2FWT9
kind: algorithm
slug: greedy-independent-set
name: Greedy independent set algorithm
aliases:
- minimum-degree greedy independent set
- GREEDY for maximum independent set
area: approximation/covering-and-packing
level: intro
summary: Repeatedly take a vertex of minimum degree and delete it with its neighbours; the result has at least the Caro-Wei bound of vertices, and its ratio is (Δ + 2)/3 on graphs of maximum degree Δ.
solves: [maximum-independent-set]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O((n + m) log n)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1983
  people: [Jerrold R. Griggs, Magnús M. Halldórsson, Jaikumar Radhakrishnan]
  note: The bound of Caro (1979) and Wei (1981) holds for the minimum-degree greedy, as Griggs (1983) observed; Halldórsson and Radhakrishnan (1997) proved the ratio (Δ + 2)/3.
prereqs: [independent-set, maximum-independent-set, greedy-algorithm]
see_also: [caro-wei-theorem, turan-theorem, maximum-independent-set, independence-number, clique-inapproximability, degeneracy, vertex-cover]
sources:
  - paper: doi:10.1007/BF02523693
    title: Magnús M. Halldórsson and Jaikumar Radhakrishnan, Greed is good, approximating independent sets in sparse and bounded-degree graphs, Algorithmica 18(1), 1997
    locator: pages 145 to 163 (the ratio (Δ + 2)/3 of the minimum-degree greedy)
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition
    locator: The Probabilistic Lens, Turán's theorem (after Chapter 6)
  - title: Jerrold R. Griggs, Lower bounds on the independence number in terms of the degrees, Journal of Combinatorial Theory, Series B 34(1), 1983
    locator: pages 22 to 39
---

The greedy independent set algorithm builds an [independent set](/independent-set/) of a graph by taking a vertex of minimum degree, deleting it and its neighbours, and repeating on what remains. The output has at least $\sum_v 1/(\deg(v) + 1)$ vertices, the bound of the [Caro-Wei theorem](/caro-wei-theorem/), so it proves that bound by an algorithm. On graphs of maximum degree $\Delta \ge 1$, its approximation ratio for [maximum independent set](/maximum-independent-set/) is $(\Delta + 2)/3$, and this is tight. On general graphs no polynomial-time algorithm has ratio $n^{1 - \varepsilon}$ unless P = NP, so the bounds of this page depend on the degrees.

## In plain words

You want many points of a network with no link between any two of them. Take a point with the fewest links. Remove it and its linked points, because they cannot join it. Repeat until no point is left.

Give each point a score of one divided by one plus its number of links. A point with few links has a high score. When you take a point with the fewest links, the removed points each have at least as many links, so their scores add up to at most one. The scores of the other points can only grow. So each step uses up at most one unit of the total score, and you take at least as many points as the total score.

## The problem

The input is an undirected graph $G = (V, E)$ with $n$ vertices, $m$ edges and no self-loops. The output is a set $I \subseteq V$ with no edge between two of its vertices. The goal is a large $|I|$. OPT is the [independence number](/independence-number/) $\alpha(G)$, and the ratio convention for this maximization problem is ALG $\ge$ OPT$/\rho$, so a ratio $\rho \ge 1$ means $\alpha(G) \le \rho \cdot |I|$. The degree of $v$ is $\deg(v)$, and $\Delta$ is the largest degree.

## The algorithm

```pseudo id=main
GREEDY-INDEPENDENT-SET(G)
L1  H ← G, I ← empty list
L2  while H has a vertex do
L3      v ← a vertex of minimum degree in H
L4      append v to I
L5      H ← H − N_H[v]                 ▷ delete v and its neighbours in H
L6  return I
```

Line L3 uses the degrees in the remaining graph $H$, not in $G$. Line L5 deletes the closed neighbourhood $N_H[v]$, so no later pick is adjacent to $v$. Ties in line L3 may be broken in any way; the implementation takes the smallest label.

## Example

The graph $G$ has the vertices 0 to 6 and the edges 0-1, 0-2, 1-2, 1-3, 2-3, 3-4, 4-5, 4-6 and 5-6. The degrees in $G$ are 2, 3, 3, 3, 3, 2, 2.

| step | degrees in $H$ | pick | deleted |
|---|---|---|---|
| 1 | 0:2, 1:3, 2:3, 3:3, 4:3, 5:2, 6:2 | 0 | 0, 1, 2 |
| 2 | 3:1, 4:3, 5:2, 6:2 | 3 | 3, 4 |
| 3 | 5:1, 6:1 | 5 | 5, 6 |

The output is $I = \{0, 3, 5\}$, which is a maximum independent set: $\alpha(G) = 3$. The Caro-Wei bound is $3 \cdot 1/3 + 4 \cdot 1/4 = 2$, and greedy beats it.

Greedy can miss the optimum. On the graph with the edges 0-1, 0-2, 1-6, 2-3, 2-6, 3-4, 3-5, 4-6 and 5-6, greedy first takes 0 (degree 2) and deletes 0, 1 and 2. The rest is the 4-cycle 3-4-6-5, and greedy takes 3 and then 6. So $|I| = 3$, but $\{1, 2, 4, 5\}$ is independent, so $\alpha = 4$. The Caro-Wei bound here is $61/30 \approx 2.03$, and $\Delta = 4$, so the ratio bound is $(4 + 2)/3 = 2$.

## Correctness

The output is independent, because each pick has no neighbour among the earlier picks: they deleted all their neighbours. It is maximal, because each vertex leaves $H$ as a pick or as a neighbour of a pick. For the size, let $\Phi(H) = \sum_{u \in H} 1/(d_H(u) + 1)$. When $v$ has minimum degree $d$ in $H$, the $d + 1$ deleted vertices each have degree at least $d$, so their terms add up to at most 1. The other vertices lose neighbours, so their terms grow or stay equal. So each step lowers $\Phi$ by at most 1, and $\Phi$ falls from $\Phi(G)$ to 0.

**Theorem.** GREEDY-INDEPENDENT-SET returns a maximal independent set with $|I| \ge \sum_{v \in V} 1/(\deg(v) + 1) \ge n/(\bar d + 1)$, where $\bar d = 2m/n$ is the average degree.

The full proof is in the proof file below. The second bound is the [Turán bound](/turan-theorem/), by convexity.

**Ratio.** For maximum degree $\Delta$, the theorem gives $|I| \ge n/(\Delta + 1) \ge \alpha(G)/(\Delta + 1)$. Halldórsson and Radhakrishnan (1997) proved the better ratio $\alpha(G) \le \frac{\Delta + 2}{3} |I|$ for $\Delta \ge 1$, and showed that it is tight for this algorithm. They also proved the ratio $(\bar d + 2)/2$ in terms of the average degree. The proof of $(\Delta + 2)/3$ is not given here.

**The upper bound used.** The simple ratio $\Delta + 1$ compares $|I|$ with $n \ge \alpha(G)$. The finer ratio compares the vertices that each pick deletes with the vertices of an optimal set among them.

**Hardness.** On general graphs, maximum independent set is as hard as [maximum clique](/clique-problem/) on the complement: a ratio of $n^{1 - \varepsilon}$ is NP-hard for each $\varepsilon > 0$; see [clique inapproximability](/clique-inapproximability/). On graphs of degree at most $\Delta$, the problem is APX-hard for each fixed $\Delta \ge 3$.

## Complexity

- **Time.** The implementation keeps the current degrees and a min-heap of (degree, vertex) pairs. Deleting a vertex lowers the degree of each living neighbour, and pushes a new pair; old pairs are skipped when popped. Each edge causes at most two pushes, so there are $O(n + m)$ heap operations, and the time is $O((n + m) \log n)$ in the worst case, in the [word RAM](/word-ram/). With a bucket queue indexed by degree, as in the computation of [degeneracy](/degeneracy/), the time is $\Theta(n + m)$.
- **Space.** The adjacency lists, the degrees and the heap take $\Theta(n + m)$ extra space.

## Properties

- **Deterministic.** With a fixed tie rule, the output depends only on the input.
- **Maximal output.** The output is a maximal independent set, and $V \setminus I$ is a [vertex cover](/vertex-cover/).
- **Any tie rule.** The Caro-Wei bound and the ratio $(\Delta + 2)/3$ hold for each tie rule.
- **Exact on some classes.** On a disjoint union of cliques, greedy takes one vertex of each clique, which is optimal, and the Caro-Wei bound holds with equality. On a forest, a vertex of degree at most 1 always exists, and taking a leaf is always safe, so greedy is optimal.

## Variants and improvements

- **Random order.** Take a random order of the vertices and keep each vertex that comes before all its neighbours. The expected size is again $\sum_v 1/(\deg(v) + 1)$; this is the proof of the [Caro-Wei theorem](/caro-wei-theorem/).
- **Maximum-degree removal.** Delete a vertex of maximum degree until no edge is left, and return the rest. This also reaches the Caro-Wei bound, and it is the dual view of greedy vertex cover.
- **Weighted version.** With vertex weights, pick $v$ that maximizes $w(v)/(d_H(v) + 1)$. The result has weight at least $\sum_v w(v)/(\deg(v) + 1)$.
- **Better ratios for bounded degree.** Local search and semidefinite programming give ratios of the form $O(\Delta \log \log \Delta / \log \Delta)$ for large $\Delta$, better than $(\Delta + 2)/3$.
- **Planar graphs.** For [planar graphs](/planar-graph/), [Baker's technique](/baker-technique/) gives a PTAS.

## When to use it

Use the minimum-degree greedy when you need a large independent set in a sparse graph fast, or when you need a constructive proof of the Caro-Wei or Turán bound. It is often close to optimal on sparse graphs met in practice, and it is a good start for local search or for an exact branch-and-bound. For dense graphs, its guarantee is weak, as for all polynomial-time algorithms.

## Pitfalls

- **Degrees in $G$ instead of $H$.** Line L3 must use the degree in the remaining graph. With the degrees of $G$ fixed at the start, the step bound of Lemma 3 no longer holds, and the proof fails.
- **Deleting only $v$.** Line L5 must delete the neighbours too. Otherwise a later pick can be adjacent to $v$.
- **The ratio for $\Delta = 0$.** On a graph with no edges, greedy takes all vertices, and the formula $(\Delta + 2)/3 = 2/3$ is below 1, so it is not a valid ratio. State the bound for $\Delta \ge 1$.
- **Stale heap entries.** With a lazy heap, an entry is valid only if its degree equals the current degree and the vertex is alive. Skipping this test picks deleted vertices.

## Implementations

## History

Caro (1979) and Wei (1981) proved the lower bound $\sum_v 1/(\deg(v) + 1)$ on the independence number, and Griggs (1983) and others observed that the minimum-degree greedy reaches it. Halldórsson and Radhakrishnan (1997) gave the tight ratio $(\Delta + 2)/3$, and named their paper "Greed is good".

## References
