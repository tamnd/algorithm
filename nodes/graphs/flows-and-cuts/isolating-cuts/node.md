---
tag: 6EABNH
kind: technique
slug: isolating-cuts
name: Isolating cuts
aliases:
- isolating cuts lemma
area: graphs/flows-and-cuts
level: research
summary: Compute minimum cuts isolating each of several terminals using few max-flow calls.
prereqs: [min-cut-problem, max-flow-problem, submodular-function, graph-contraction]
see_also: [global-min-cut-problem, gomory-hu-tree, all-pairs-min-cut-problem, almost-linear-max-flow, multiway-cut-problem, vertex-connectivity, stoer-wagner, karger-stein]
sources:
  - paper: doi:10.1109/FOCS46700.2020.00017
    title: Jason Li and Debmalya Panigrahi, Deterministic min-cut in poly-logarithmic max-flows, 2020 IEEE 61st Annual Symposium on Foundations of Computer Science (FOCS)
    locator: the isolating cuts lemma and its use for the deterministic global minimum cut
  - paper: doi:10.1145/3406325.3451073
    title: Amir Abboud, Robert Krauthgamer and Ohad Trabelsi, Subcubic algorithms for Gomory-Hu tree in unweighted graphs, Proceedings of the 53rd Annual ACM SIGACT Symposium on Theory of Computing (STOC 2021)
    locator: the use of isolating cuts to find many minimum cuts from one source at once
---

The isolating cuts technique computes, for each terminal $t$ of a set $T$ of $k$ terminals in an undirected graph, a minimum cut that separates $t$ from all other terminals, a *minimum isolating cut*, with only $O(\log k)$ [maximum flow](/max-flow-problem/) computations on the whole graph plus flows on disjoint pieces of total size $O(m)$. The naive method needs $k$ flows. The trick is to split the terminals into two halves along each bit of their binary labels, take one [minimum cut](/min-cut-problem/) per bit, and intersect the sides: by [submodularity](/submodular-function/) of the cut function, each terminal has a minimum isolating cut inside the region its sides share, and these regions are disjoint. Li and Panigrahi introduced the lemma in 2020 for a deterministic [global minimum cut](/global-min-cut-problem/) with polylogarithmically many flows, and it has since become a basic tool for [Gomory-Hu trees](/gomory-hu-tree/), Steiner cuts and connectivity.

## In plain words

You have a network and several marked points, and for each marked point you want the cheapest way to cut it off from all the other marked points. Doing a separate computation for each point is slow when there are many.

Give each marked point a number written in binary. For each binary digit, split the marked points into those with a 0 there and those with a 1, and find the cheapest cut between the two groups. That is only a handful of cuts. Each marked point now has its own region: the places that landed on its side in every one of those cuts. No two marked points share a region, and the cheapest cut for each point fits inside its region. So each point needs only one small computation inside its own region, and all these regions together are no bigger than the network.

## When it applies

- **Undirected graphs** with weights $w(e) \ge 0$, integer or real; parallel edges add up and self-loops do not matter. The argument uses only that the cut function $w(\delta(S))$ is submodular, so it also holds for the cut function of a directed graph, $w(\delta^{\mathrm{out}}(S))$, with each edge, including each edge of an antiparallel pair, counted in the direction it leaves $S$.
- **Many terminals, one query each.** The goal is a minimum isolating cut for every terminal, or the best of them. For the cut between two specific terminals, one flow is enough.
- **Flows are the expensive step.** The technique saves when a maximum flow costs much more than linear time, or when it is the only black box allowed, as in deterministic reductions.

## The template

For a terminal $t$, an *isolating cut* is a set $S$ with $S \cap T = \{t\}$; its weight is $w(\delta(S))$, the total weight of the edges with exactly one end in $S$. For disjoint terminal sets $A$, $B$, a minimum $(A, B)$-cut is a minimum $s$-$t$ cut after merging $A$ into one source and $B$ into one sink.

```pseudo id=main
ISOLATING-CUTS(G, w, T)
L1  give the terminals distinct labels in {0, ..., k − 1}, with b ← ⌈log2 k⌉ bits each
L2  for i ← 1 to b do
L3      A_i ← the terminals whose bit i is 0; B_i ← the others
L4      X_i ← the source side of a minimum (A_i, B_i)-cut, found by one maximum flow
L5  for each terminal t do
L6      U_t ← the intersection, over i, of X_i if t ∈ A_i and of V \ X_i if t ∈ B_i
L7      G_t ← G with V \ U_t contracted into one vertex z_t
L8      S_t ← the source side of a minimum t-z_t cut of G_t
L9  return the sets S_t and their weights
```

**Why it works.** *Disjoint regions.* Two terminals differ in some bit $i$, so one of them is in $X_i$ and the other is not, and their regions are disjoint. Each $U_t$ contains $t$ and no other terminal.

*A minimum isolating cut fits in $U_t$.* Let $S^{*}$ be a minimum isolating cut for $t$, and let $Y$ be the side of the cut of bit $i$ that contains $t$, so $Y$ is a minimum cut between $t$'s class and the other class. The set $S^{*} \cup Y$ contains the class of $t$, because $Y$ does, and no terminal of the other class, because neither $S^{*}$ nor $Y$ does; so it is also a cut between the two classes, and $w(\delta(S^{*} \cup Y)) \ge w(\delta(Y))$. Submodularity, $w(\delta(S^{*} \cap Y)) + w(\delta(S^{*} \cup Y)) \le w(\delta(S^{*})) + w(\delta(Y))$, gives $w(\delta(S^{*} \cap Y)) \le w(\delta(S^{*}))$. And $S^{*} \cap Y$ contains $t$ and no other terminal, so it is again a minimum isolating cut. Doing this for each bit gives a minimum isolating cut inside $U_t$.

*Line L8 finds it.* A set $S$ with $t \in S \subseteq U_t$ has the same weight in $G$ and in $G_t$, because the contraction keeps all edges with an end in $U_t$. So the minimum $t$-$z_t$ cut of $G_t$ is a minimum isolating cut of $t$ in $G$.

*Size.* An edge appears in $G_t$ only if it has an end in $U_t$, and the regions are disjoint, so each edge appears in at most two of the graphs $G_t$. Their total size is $O(n + m)$. With an [almost-linear maximum flow](/almost-linear-max-flow/), the whole computation takes $m^{1+o(1)} \log k$ time.

## Classic examples

**A small run.** The graph has terminals $t_1, t_2, t_3$ and other vertices $a, b, c$, with the edges $t_1 a$ (3), $t_1 b$ (3), $a c$ (1), $b c$ (1), $c t_2$ (2), $c t_3$ (2), $t_2 t_3$ (1). Label $t_1 = 00$, $t_2 = 01$, $t_3 = 10$.

- Bit 1: $A_1 = \{t_1, t_3\}$, $B_1 = \{t_2\}$. A minimum cut is $\{t_2\}$, of weight 3, so $X_1 = V \setminus \{t_2\}$.
- Bit 2: $A_2 = \{t_1, t_2\}$, $B_2 = \{t_3\}$. A minimum cut is $\{t_3\}$, of weight 3, so $X_2 = V \setminus \{t_3\}$.
- Regions: $U_{t_1} = \{t_1, a, b, c\}$, $U_{t_2} = \{t_2\}$, $U_{t_3} = \{t_3\}$.
- Inside $U_{t_1}$, the candidates are $\{t_1\}$ (6), $\{t_1, a\}$ (4), $\{t_1, a, b\}$ (2) and $\{t_1, a, b, c\}$ (4), so $S_{t_1} = \{t_1, a, b\}$ with weight 2. The other two are $\{t_2\}$ and $\{t_3\}$, each of weight 3.

Two flows on the whole graph and three small flows replace three flows on the whole graph; with $k$ terminals, it is $\lceil \log_2 k \rceil$ instead of $k$.

**Edge cases.** An edge of weight 0 adds nothing to any cut. If a terminal $t$ lies in a different component from all other terminals, its component is an isolating cut of weight 0, and line L8 finds weight 0. With $k = 1$ there are no bits and $U_t = V$; the isolating cut is then not defined unless the convention is that it must be a proper subset.

**Deterministic global minimum cut.** Li and Panigrahi pick terminal sets such that, for a minimum cut $C$, some terminal set meets the smaller side of $C$ in exactly one vertex. The minimum isolating cut of that terminal then has weight at most $w(\delta(C))$, so it is a global minimum cut. This gives a [global minimum cut](/global-min-cut-problem/) deterministically with polylogarithmically many maximum flows, in place of the randomized [Karger-Stein](/karger-stein/) or the $O(nm)$ deterministic [Stoer-Wagner](/stoer-wagner/).

**Gomory-Hu trees.** To build a [Gomory-Hu tree](/gomory-hu-tree/), one needs minimum cuts from a pivot to many vertices at once. Isolating cuts on a random set of terminals together with the pivot find many of them in one round; Abboud, Krauthgamer and Trabelsi used this for the first subcubic Gomory-Hu tree algorithm for unweighted graphs.

## Variations

- **Vertex cuts.** With [vertex splitting](/vertex-capacities-flow/), the same lemma finds minimum vertex cuts that isolate terminals, used in recent algorithms for [vertex connectivity](/vertex-connectivity/).
- **Directed graphs.** Since only submodularity is used, the lemma holds for out-cuts of directed graphs, with flows in the directed graph.
- **Steiner cuts.** The best of all isolating cuts is a minimum cut that separates $T$, a Steiner minimum cut, if one side of some optimal such cut contains exactly one terminal.

## Pitfalls

- **Using the cuts of line L4 directly.** The bit cuts are not isolating cuts; they only bound the regions. The step at line L8 is needed.
- **Forgetting to contract the outside.** If line L8 cuts $t$ from only the other terminals in the whole graph, the work is a full flow per terminal again. The outside must be contracted to one sink so that the pieces have total size $O(m)$.
- **Assuming every minimum isolating cut lies in $U_t$.** Only one does, the intersection built in the proof; another minimum isolating cut may cross the region boundary.
- **Labels that are not distinct.** Two terminals with the same label are never separated by a bit, and their regions overlap.
- **Expecting minimum isolating cuts to be a partition.** The sets $S_t$ are disjoint, but they need not cover $V$, and their union is not a [multiway cut](/multiway-cut-problem/) of minimum weight in general.

## References
