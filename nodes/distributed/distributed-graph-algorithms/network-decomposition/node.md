---
tag: 1Q6NFT
kind: technique
slug: network-decomposition
name: Network decomposition
aliases:
- low-diameter cluster decomposition
area: distributed/distributed-graph-algorithms
level: research
summary: Partition the nodes into clusters of small diameter and colour the clusters so that adjacent clusters differ. Then C colours and diameter D solve MIS and colouring in O(C D) rounds.
prereqs: [local-model, distributed-mis, ruling-set, round-complexity]
see_also: [low-diameter-decomposition, sparse-neighborhood-cover, distributed-mis, distributed-vertex-coloring, locally-checkable-labeling, distributed-dominating-set, ruling-set, frt-tree-embedding]
sources:
  - paper: doi:10.1109/SFCS.1989.63504
    title: Baruch Awerbuch, Andrew V. Goldberg, Michael Luby and Serge A. Plotkin, Network decomposition and locality in distributed computation, FOCS 1989
    locator: pp. 364 to 369 (the definition, the deterministic 2^O(sqrt(log n log log n)) construction, and its use for MIS and colouring)
  - paper: doi:10.1007/BF01303516
    title: Nathan Linial and Michael Saks, Low diameter graph decompositions, Combinatorica 13(4), 1993
    locator: pp. 441 to 454 (the randomized (O(log n), O(log n)) decomposition by random radii, and the existence of such decompositions)
  - paper: doi:10.1006/jagm.1996.0017
    title: Alessandro Panconesi and Aravind Srinivasan, On the complexity of distributed network decomposition, Journal of Algorithms 20(2), 1996
    locator: pp. 356 to 374 (deterministic 2^O(sqrt(log n)) rounds)
  - paper: doi:10.1145/3357713.3384298
    title: Václav Rozhoň and Mohsen Ghaffari, Polylogarithmic-time deterministic network decomposition and distributed derandomization, STOC 2020
    locator: pp. 350 to 363 (the first deterministic poly(log n) decomposition, with O(log n) colours and poly(log n) weak diameter)
  - paper: doi:10.1137/1.9781611976465.173
    title: Mohsen Ghaffari, Christoph Grunau and Václav Rozhoň, Improved deterministic network decomposition, SODA 2021
    locator: pp. 2904 to 2923 (a faster deterministic construction with strong diameter)
  - paper: doi:10.1109/FOCS61266.2024.00007
    title: Mohsen Ghaffari and Christoph Grunau, Near-optimal deterministic network decomposition and ruling set, and improved MIS, FOCS 2024
    locator: pp. 2148 to 2179 (O(log n) colours and O(log n) diameter in O~(log^2 n) deterministic rounds, and the remark that C times D is Omega~(log^2 n) in general)
  - paper: doi:10.1145/2933057.2933094
    title: Michael Elkin and Ofer Neiman, Distributed strong diameter network decomposition, PODC 2016
    locator: pp. 211 to 216 (randomized strong-diameter (O(log n), O(log n)) decomposition by exponential shifts)
---

A network decomposition splits the nodes of a graph into clusters of small diameter and gives each cluster one of a few colours, so that clusters joined by an edge get different colours. With $C$ colours and diameter $D$, a [LOCAL](/local-model/) algorithm can handle the colours one at a time and solve each cluster by gathering it at one node, so many symmetry-breaking problems, such as [MIS](/distributed-mis/) and [$(\Delta + 1)$-colouring](/distributed-vertex-coloring/), take $O(C \cdot D)$ rounds. Awerbuch, Goldberg, Luby and Plotkin (1989) introduced the method, Linial and Saks (1993) gave a randomized $(O(\log n), O(\log n))$ decomposition, and Rozhoň and Ghaffari (2020) gave the first deterministic one in $\mathrm{poly}(\log n)$ rounds.

Notation on this page: $G = (V, E)$ has $n$ nodes with distinct identifiers, and $\mathrm{dist}$ is the shortest path distance in $G$. A $(C, D)$ **network decomposition** is a partition of $V$ into clusters with a colour in $\{1, \dots, C\}$ per cluster, such that two clusters with an edge between them have different colours, and every cluster has diameter at most $D$. The diameter is **strong** if it is measured in the subgraph induced by the cluster, and **weak** if it is measured in $G$. "With high probability" (w.h.p.) means with probability at least $1 - n^{-c}$.

## In plain words

A large country must make many local decisions, and every town's decision depends on its neighbours'. Deciding town by town is too slow. Instead, the country is split into small districts, and the districts get a few colours so that neighbouring districts differ.

Now all districts of the first colour decide at the same time. Each district is small, so one town in it can collect the whole district, decide for all its towns, and send the answers back. Districts of one colour do not touch, so their decisions cannot conflict. Then the second colour goes, and so on.

The time is the number of colours times the time to cross a district. The hard part is to find such a split with few colours and small districts, using only local talk. Random radii do it in a few rounds; methods without randomness took thirty years to become as good.

## When it applies

- **The problem can be solved greedily in some order.** If a solution can be built by visiting the nodes one at a time, where each node looks only at nodes within distance $r$ that were visited before, then a $(C, D)$ decomposition of $G^r$ solves it in $O(C \cdot D \cdot r)$ rounds. MIS, $(\Delta + 1)$-colouring, maximal matching and $(\deg + 1)$-list colouring all have $r = 1$. This class is called SLOCAL.
- **The LOCAL model, or enough bandwidth.** A cluster is solved by gathering its whole topology, which needs large messages. In [CONGEST](/congest-model/), the use and the construction must be adapted.
- **Derandomization.** A randomized algorithm for a locally checkable problem can be turned into a deterministic one by fixing its random bits cluster by cluster, with a conditional expectation argument inside each cluster.
- **Not for global problems.** Problems whose answer depends on far parts of the graph, such as a spanning tree, need $\Omega(\mathrm{diameter})$ rounds whatever decomposition is used.

## The template

The randomized construction of Linial and Saks, in the form used here. It runs in phases, and the phase number becomes the colour. $B = \lceil 3 \log_2 n \rceil$ caps the radii.

```pseudo id=main
LINIAL-SAKS(G)
L1  alive ← V
L2  while some node is alive do
L3      each alive u draws r_u with Pr[r_u ≥ j] = 2^(−j), and r_u ← min(r_u, B)
L4      each alive v finds the alive u of largest identifier with dist_alive(u, v) ≤ r_u
L5      v joins this phase if dist_alive(u, v) < r_u
L6      for each joining v: cluster(v) ← u; colour(v) ← phase
L7      alive ← alive minus the joining nodes
L8      phase ← phase + 1
L9  return the clusters and colours
```

Here $\mathrm{dist}_{\mathrm{alive}}$ is the distance in the subgraph induced by the alive nodes. Line L4 takes $B$ rounds: each $u$ floods its identifier and radius $r_u$ to distance $r_u$ through alive nodes.

**The use.** Given a $(C, D)$ decomposition, for colour $c = 1, \dots, C$: every cluster of colour $c$ gathers its nodes, their edges and the current state of their neighbours at a leader in $O(D)$ rounds; the leader extends the partial solution on the cluster, for example by a greedy MIS of the free nodes; it sends the answers back in $O(D)$ rounds. Clusters of colour $c$ are not adjacent, so their choices are compatible. The total is $O(C \cdot D)$ rounds.

*Theorem (Linial and Saks).* The template returns a decomposition in which clusters of the same colour are not adjacent and every cluster has weak diameter at most $2(B - 1)$. In each phase, each alive node joins with probability at least $\frac{1}{2} - n^{-2}$. So for $n \ge 2$, with probability at least $1 - n^{-c}$ it ends within $(c + 1) \log_{4/3} n$ phases, and it uses $O(\log n)$ colours and $O(\log^2 n)$ rounds.

*Proof.* **Same colour, not adjacent.** Let $v$ join in a phase with centre $u$, so $\mathrm{dist}_{\mathrm{alive}}(u, v) < r_u$, and let $w$ be an alive neighbour of $v$ that joins in the same phase with centre $u'$. Then $\mathrm{dist}_{\mathrm{alive}}(u, w) \le r_u$, so $u$ covers $w$, and $\mathrm{id}(u') \ge \mathrm{id}(u)$ by the choice of $w$. Also $\mathrm{dist}_{\mathrm{alive}}(u', v) \le \mathrm{dist}_{\mathrm{alive}}(u', w) + 1 \le r_{u'}$, so $u'$ covers $v$, and $\mathrm{id}(u) \ge \mathrm{id}(u')$. Hence $u = u'$. Nodes clustered in earlier phases have other colours, so an edge between two clusters of one colour cannot exist.

**Diameter.** Every member $v$ of the cluster of $u$ has $\mathrm{dist}(u, v) \le \mathrm{dist}_{\mathrm{alive}}(u, v) < r_u \le B$, so two members are at distance at most $2(B - 1)$ in $G$.

**Progress.** Fix a phase and an alive node $v$, and condition on the radii of all nodes except one node $u$. The event $A_u$ that $u$ is the chosen centre of $v$ is the event that $r_u \ge d$, where $d = \mathrm{dist}_{\mathrm{alive}}(u, v)$, and that no alive node of larger identifier covers $v$; the second part does not depend on $r_u$. Given $A_u$, $v$ joins exactly when $r_u > d$, and for $d < B$, $\Pr[r_u > d \mid r_u \ge d] = \frac{1}{2}$ because the radii are geometric. The events $A_u$ are disjoint and one of them happens, since $v$ covers itself. So $v$ joins with probability at least $\frac{1}{2} - \sum_u \Pr[A_u \text{ with } d = B] \ge \frac{1}{2} - n \cdot 2^{-B} \ge \frac{1}{2} - n^{-2}$, which is at least $\frac{1}{4}$ for $n \ge 2$. After $(c + 1) \log_{4/3} n$ phases, $v$ is still alive with probability at most $n^{-(c+1)}$, and a [union bound](/union-bound/) over the nodes finishes the proof. Each phase takes $B = O(\log n)$ rounds. $\blacksquare$

The diameter here is weak: two members of a cluster may be joined only through nodes of other clusters. The gathering step still works, since it routes through $G$, but each node may then forward messages for several clusters.

## Classic examples

- **MIS in $O(\log^2 n)$ rounds.** The template plus the use gives an MIS in $O(\log n) \cdot O(\log n)$ rounds; this is slower than [Luby](/luby-mis/), but the use is deterministic once the decomposition is fixed.
- **Deterministic algorithms.** A deterministic decomposition gives deterministic MIS, $(\Delta + 1)$-colouring and maximal matching. The history of the deterministic bounds is the history of decompositions:

| Result | Colours $C$ | Diameter $D$ | Rounds |
|---|---|---|---|
| Awerbuch, Goldberg, Luby and Plotkin (1989) | $2^{O(\sqrt{\log n \log \log n})}$ | $2^{O(\sqrt{\log n \log \log n})}$ | $2^{O(\sqrt{\log n \log \log n})}$ |
| Panconesi and Srinivasan (1992, 1996) | $2^{O(\sqrt{\log n})}$ | $2^{O(\sqrt{\log n})}$ | $2^{O(\sqrt{\log n})}$ |
| Rozhoň and Ghaffari (2020) | $O(\log n)$ | $\mathrm{poly}(\log n)$, weak | $\mathrm{poly}(\log n)$ |
| Ghaffari and Grunau (2024) | $O(\log n)$ | $O(\log n)$ | $\tilde{O}(\log^2 n)$ |

- **Randomized, strong diameter.** Elkin and Neiman (2016) get strong diameter $O(\log n)$ and $O(\log n)$ colours w.h.p. in $O(\log^2 n)$ rounds, by running the exponential shifts of [low-diameter decomposition](/low-diameter-decomposition/) in phases.
- **Shattering.** In randomized MIS and colouring algorithms, the nodes left after a random phase form small components of $N = \mathrm{poly}(\log n)$ nodes, and a deterministic decomposition finishes them in $\mathrm{poly}(\log N) = \mathrm{poly}(\log \log n)$ rounds.
- **Derandomization of LCLs.** Ghaffari, Kuhn and Maus (2017) and Ghaffari, Harris and Kuhn (2018) show that a deterministic $\mathrm{poly}(\log n)$ decomposition makes every [locally checkable](/locally-checkable-labeling/) problem with a $\mathrm{poly}(\log n)$ randomized algorithm solvable deterministically in $\mathrm{poly}(\log n)$ rounds. Rozhoň and Ghaffari supplied the decomposition.

## Variations

- **Existence.** Every graph has an $(O(\log n), O(\log n))$ decomposition with strong diameter, by growing balls one at a time until the next layer is smaller than the ball. The product $C \cdot D$ cannot be much smaller in general: Ghaffari and Grunau note that it is $\tilde{\Omega}(\log^2 n)$ on some graphs, which is why the use costs that much.
- **Trade-offs.** The random radii can be drawn with other parameters to trade colours against diameter: Linial and Saks get diameter $O(k)$ with about $n^{1/k} \log n$ colours.
- **Decompositions of $G^r$.** For problems with radius $r$, decompose the power graph, so that clusters of one colour are more than $r$ apart in $G$.
- **[Sparse neighbourhood covers](/sparse-neighborhood-cover/).** Instead of a partition, a family of overlapping clusters such that each ball of radius $r$ lies inside one cluster. Covers and decompositions can be built from each other.
- **[Low-diameter decomposition](/low-diameter-decomposition/).** A partition with small diameter that cuts few edges, with no colouring of the clusters. It is the probabilistic tool behind Elkin-Neiman and the parallel algorithms of Miller, Peng and Xu.

## Pitfalls

- **Weak and strong diameter.** A weak-diameter cluster may be disconnected inside itself. Gathering then uses paths through other clusters, which costs congestion in CONGEST, and some uses, such as building a tree inside each cluster, need strong diameter.
- **Distances in the remaining graph.** In the template, distances must be measured among alive nodes. With distances in $G$, a cluster can reach across a node clustered earlier, and the non-adjacency proof still holds, but the weak diameter is then the only guarantee.
- **Disjoint is not enough.** Clusters of one colour must have no edge between them, not merely be disjoint; otherwise two clusters may both add adjacent nodes to an MIS.
- **The radius of the problem.** A problem whose greedy rule looks at distance 2, such as distance-2 colouring, needs a decomposition of $G^2$; a decomposition of $G$ lets two clusters of one colour make conflicting choices.
- **$C \cdot D$ is the cost.** A decomposition with few colours but large diameter is not cheaper to use; the use takes $O(C \cdot D)$ rounds, and both factors count.

## Exercises

1. Show that a $(C, D)$ decomposition with strong diameter gives a $(\Delta + 1)$-colouring in $O(C \cdot D)$ rounds, and explain why the cluster leader can always extend the partial colouring.
2. Run the template on a path of 8 nodes with identifiers $1, \dots, 8$ in order, with the radii $r = (0, 2, 0, 1, 0, 0, 3, 0)$ in the first phase. Which nodes join, and with which centres?
3. Show that if the radii are drawn with $\Pr[r_u \ge j] = q^j$ for $q < 1$, each alive node joins with probability $1 - q$ per phase, and find the trade-off between the number of phases and the cap $B$ needed to keep the cut probability below $n^{-2}$.

## References
