---
tag: FW9GHE
kind: technique
slug: low-diameter-decomposition
name: Low-diameter decomposition
aliases:
- LDD
- Miller-Peng-Xu decomposition
area: distributed/distributed-graph-algorithms
level: research
summary: Partition a graph into clusters of diameter O(log n / beta) so that each edge is cut with probability at most beta. Exponential shifts do this in O(log n / beta) rounds.
prereqs: [local-model, round-complexity]
see_also: [network-decomposition, sparse-neighborhood-cover, frt-tree-embedding, metric-tree-embedding, synchronizer, distributed-mis, ruling-set]
sources:
  - paper: doi:10.1145/2486159.2486180
    title: Gary L. Miller, Richard Peng and Shen Chen Xu, Parallel graph decompositions using random shifts, SPAA 2013
    locator: pp. 196 to 203 (the exponential shift clustering, the cut probability bound, and the diameter bound)
  - paper: doi:10.1145/2933057.2933094
    title: Michael Elkin and Ofer Neiman, Distributed strong diameter network decomposition, PODC 2016
    locator: pp. 211 to 216 (exponential shifts in the distributed setting, and a strong-diameter network decomposition built from them)
  - paper: doi:10.1109/SFCS.1996.548477
    title: Yair Bartal, Probabilistic approximation of metric spaces and its algorithmic applications, FOCS 1996
    locator: pp. 184 to 193 (probabilistic partitions of metrics with cut probability O(log n) times distance over diameter)
  - paper: doi:10.1007/BF01303516
    title: Nathan Linial and Michael Saks, Low diameter graph decompositions, Combinatorica 13(4), 1993
    locator: pp. 441 to 454 (ball growing and random radii; the existence of decompositions with small diameter)
  - paper: doi:10.1145/4221.4227
    title: Baruch Awerbuch, Complexity of network synchronization, Journal of the ACM 32(4), 1985
    locator: pp. 804 to 823 (the partition by ball growing used in synchronizer gamma)
---

A low-diameter decomposition (LDD) splits the nodes of a graph into clusters of small diameter so that few edges go between clusters. With a parameter $\beta \in (0, 1)$, the exponential shift method of Miller, Peng and Xu (2013) gives clusters of strong diameter $O(\log n / \beta)$ w.h.p. and cuts each edge with probability at most $\beta$. It takes $O(\log n / \beta)$ rounds in the [LOCAL](/local-model/) model, with messages small enough for [CONGEST](/congest-model/).

Notation on this page: $G = (V, E)$ is an unweighted undirected graph with $n$ nodes and $m$ edges, and $\mathrm{dist}$ is the shortest path distance in $G$. $\mathrm{Exp}(\beta)$ is the exponential distribution with rate $\beta$, so $\Pr[\delta > t] = e^{-\beta t}$ for $t \ge 0$. A cluster has **strong** diameter $D$ if any two of its nodes are joined by a path of length at most $D$ inside the cluster. An edge is **cut** if its ends are in different clusters. "W.h.p." means with probability at least $1 - n^{-c}$ for a constant $c$ of our choice.

## In plain words

Every node starts a fire at a random moment. Most fires start late, but a few start early, and early fires spread further before the others begin. All fires spread at the same speed, one edge per time step. Each node belongs to the fire that reaches it first.

A fire that starts early can only spread for as long as its head start lasts, and very large head starts are rare, so no cluster is very wide. Two neighbours end up in different clusters only when two fires arrive at almost the same moment. Because the start times are random in a memoryless way, such a near tie is rare, and its chance is set by one parameter.

The method needs no coordination: each node only passes on the best offer it has heard so far.

## When it applies

- **A partition is enough.** LDD gives disjoint clusters of small diameter and few cut edges, but no colouring of the clusters. Two adjacent clusters may act at the same time, so LDD alone does not solve MIS or colouring; that needs a [network decomposition](/network-decomposition/), where clusters of one colour are not adjacent.
- **Divide and conquer on edges.** If a problem can be solved inside each cluster and the cut edges can be handled separately, because they are few, LDD is the right tool. Examples are spanners, low-stretch trees, and approximate shortest paths.
- **Unweighted or weighted.** The template is written for unweighted graphs. With positive edge lengths, the same rule with weighted distances cuts an edge of length $\ell$ with probability at most $1 - e^{-\beta \ell} \le \beta \ell$.
- **Randomness.** The method is randomized, and the guarantee on cut edges holds in expectation for each edge. A deterministic partition with the same trade-off exists by ball growing, but it is sequential.

## The template

```pseudo id=main
MPX(G, β)
L1  each node u draws δ_u from Exp(β)
L2  best(v) ← (δ_v, v)
L3  for round 1, …, R do
L4      each node v sends best(v) to its neighbours
L5      each v sets best(v) to the largest of best(v) and (x − 1, u) over received pairs (x, u)
L6  centre(v) ← the second part of best(v)
```

The pairs are compared first by value and then by identifier. After the loop, $v$ holds the pair $(\delta_u - \mathrm{dist}(u, v), u)$ that is largest over all $u$ with $\mathrm{dist}(u, v) \le R$. In practice $R = \lceil (c + 1) \ln n / \beta \rceil$; the code on this page uses $R = \lfloor \max_u \delta_u \rfloor + 1$, which is the least value that is always correct.

*Theorem (Miller, Peng and Xu).* Let $R > \max_u \delta_u$. Then every node $v$ is in the cluster of the node $u$ that maximizes $\delta_u - \mathrm{dist}(u, v)$; each cluster is connected and has strong radius at most $\max_u \delta_u$ around its centre; with probability at least $1 - n^{-c}$, $\max_u \delta_u \le (c + 1) \ln n / \beta$; and each edge is cut with probability at most $1 - e^{-\beta} \le \beta$.

*Proof.* **The rounds compute the rule.** By induction on the rounds, after $r$ rounds $v$ holds the largest pair over the nodes at distance at most $r$. Let $u^*$ be the true maximizer for $v$. Since $v$ itself offers $\delta_v \ge 0$, we have $\delta_{u^*} - \mathrm{dist}(u^*, v) \ge 0$, so $\mathrm{dist}(u^*, v) \le \delta_{u^*} < R$, and $v$ hears $u^*$.

**Clusters are connected, with small radius.** Let $v$ choose $u$, and let $w$ be a node on a shortest path from $u$ to $v$. If $w$ chose some $u' \ne u$, then $\delta_{u'} - \mathrm{dist}(u', w) > \delta_u - \mathrm{dist}(u, w)$ in the pair order, and adding $\mathrm{dist}(w, v)$ to both distances gives $\delta_{u'} - \mathrm{dist}(u', v) \ge \delta_{u'} - \mathrm{dist}(u', w) - \mathrm{dist}(w, v) > \delta_u - \mathrm{dist}(u, v)$, against the choice of $v$. So the whole path lies in the cluster of $u$, and its length is $\mathrm{dist}(u, v) \le \delta_u$.

**Largest shift.** $\Pr[\delta_u > t] = e^{-\beta t}$, so with $t = (c + 1) \ln n / \beta$ each node exceeds $t$ with probability $n^{-(c+1)}$, and a [union bound](/union-bound/) over the $n$ nodes gives the claim. The strong diameter of each cluster is then at most $2t = O(\log n / \beta)$.

**Cut edges.** First a lemma. Let $a_1, \dots, a_n$ be fixed reals, let the $\delta_u$ be independent $\mathrm{Exp}(\beta)$, and let $X_u = \delta_u - a_u$. Then the largest $X_u$ beats the second largest by at most $\gamma$ with probability at most $1 - e^{-\beta \gamma}$. To see this, fix $u$ and condition on all $\delta_w$ with $w \ne u$; let $M = \max_{w \ne u} X_w$ and $s = M + a_u$. The node $u$ is the top one exactly when $\delta_u > s$, and it is the top one with a gap of at most $\gamma$ exactly when $\delta_u \in (s, s + \gamma]$. If $s \ge 0$, memorylessness gives $\Pr[\delta_u \in (s, s + \gamma]] = (1 - e^{-\beta \gamma}) \Pr[\delta_u > s]$; if $s < 0$, the left side is at most $1 - e^{-\beta \gamma}$ and $\Pr[\delta_u > s] = 1$. So in both cases the probability is at most $(1 - e^{-\beta \gamma}) \Pr[u \text{ is the top}]$, and the sum over $u$ is at most $1 - e^{-\beta \gamma}$, since exactly one $u$ is the top (ties have probability 0).

Now take an edge $\{x, y\}$ and put $a_u = \min(\mathrm{dist}(u, x), \mathrm{dist}(u, y)) + \frac{1}{2}$, the distance from $u$ to the middle of the edge. Since the two distances differ by at most 1, $\delta_u - \mathrm{dist}(u, x)$ and $\delta_u - \mathrm{dist}(u, y)$ are both within $\frac{1}{2}$ of $X_u$. If the top $u^*$ beats every other $X_w$ by more than 1, then at $x$ the value of $u^*$ is more than $X_w + \frac{1}{2}$, which is at least the value of $w$, for every $w$; so $x$ chooses $u^*$, and so does $y$. Hence a cut edge needs a gap of at most 1, which has probability at most $1 - e^{-\beta}$ by the lemma with $\gamma = 1$. $\blacksquare$

By [linearity of expectation](/linearity-of-expectation/), the expected number of cut edges is at most $\beta m$. The bound is per edge and in expectation; a single run can cut more.

**Rounds and messages.** The loop takes $R = O(\log n / \beta)$ rounds w.h.p. A message is one value and one identifier. With the shifts rounded to $O(\log n)$ bits, which changes the bounds only by small terms, the template runs in CONGEST in the same number of rounds.

## Classic examples

- **Network decomposition with strong diameter.** Elkin and Neiman (2016) use exponential shifts to build an $(O(\log n), O(\log n))$ [network decomposition](/network-decomposition/) with strong diameter. The idea: run MPX with a constant $\beta$, and keep a node $v$ if its best value beats the second best at $v$ by more than 1. By the lemma, $v$ is kept with probability at least $e^{-\beta}$. Two kept nodes that are adjacent are in the same cluster: if $v$ keeps $u$ and its neighbour $w$ keeps $u' \ne u$, the values at $w$ are within 1 of those at $v$, so the gap at $v$ is less than 1. So the kept nodes form one colour class. Repeat on the other nodes for $O(\log n)$ phases. Their paper deals with the remaining details, such as the strong diameter of the kept part of a cluster.
- **Parallel graph algorithms.** Miller, Peng and Xu introduced the method for the PRAM, where it takes linear work and $\tilde{O}(\log n / \beta)$ depth, and it is a step in parallel algorithms for spanners, low-stretch trees and linear system solvers. The distributed view counts rounds, not work and span: the $O(m)$ work does not matter in LOCAL, but the $O(\log n / \beta)$ rounds do.
- **Synchronizers.** Awerbuch's synchronizer $\gamma$ (1985) uses a partition into clusters of small diameter with few edges between clusters, built by ball growing; see [synchronizer](/synchronizer/). An LDD gives such a partition with a randomized local algorithm.
- **Tree embeddings.** Probabilistic partitions of a metric, where a pair at distance $d$ is separated with probability $O(d \log n / D)$ by clusters of diameter $D$, are the basis of Bartal's embeddings into trees and of the [FRT embedding](/frt-tree-embedding/).

## Variations

- **Ball growing.** Pick a node, grow a ball layer by layer until the edges that leave it number at most $\beta$ times (the edges inside it plus 1), cut there, remove the ball and repeat. While a ball grows, its edge count grows by a factor $1 + \beta$ per layer, so every ball stops within $O(\log n / \beta)$ layers, and at most $\beta (m + n)$ edges are cut in total. This is deterministic and sequential; Awerbuch (1985) and Linial and Saks (1993) use it.
- **Random radii.** [Linial and Saks](/network-decomposition/) draw geometric radii, which have the same memoryless property in discrete form, and use the largest identifier among the covering centres. With colours from the phases, this gives a network decomposition with weak diameter.
- **Weighted graphs.** With edge lengths, an edge of length $\ell$ is cut with probability at most $\beta \ell$ by the same proof with $\gamma = \ell$.
- **Bartal's partitions.** For a general metric and a target diameter $D$, a pair at distance $d$ is separated with probability $O(d \log n / D)$. This is the same trade-off as MPX with $\beta = \Theta(\log n / D)$.
- **Tightness.** On constant-degree expanders, every set with at most half the nodes has a boundary that is a constant fraction of its edges, and a cluster of diameter $D$ has at most $d^{D+1}$ nodes. So any partition that cuts less than a constant fraction of the edges has a cluster of diameter $\Omega(\log n)$, and the $\log n$ in the diameter cannot be removed in general.

## Pitfalls

- **No colouring.** An LDD is not a network decomposition. Adjacent clusters exist, and solving clusters in parallel without coordination can break MIS or colouring along cut edges.
- **The bound is per edge.** The fraction of cut edges is at most $\beta$ in expectation, not in every run; a test or an algorithm that needs it always must repeat or use a concentration bound.
- **Too few rounds.** If $R$ is too small, a node may never hear its true centre, and the clusters can then be disconnected. Use $R \ge (c + 1) \ln n / \beta$, which needs an estimate of $n$.
- **Ties.** With real shifts, ties have probability 0, but rounded shifts can tie. Break ties by identifier, the same way at every node, or the cluster of a node and of its neighbour on the path can differ.
- **Strong and weak diameter.** MPX clusters have strong diameter. Methods that measure distances in $G$ but restrict membership, such as phases on the remaining graph, may give only weak diameter.

## Exercises

1. Show that on a cycle with $n$ nodes, any partition into clusters of diameter at most $D$ cuts at least $n / (D + 1)$ edges. Compare with the bound $\beta n$ for the cut edges and the bound $O(\log n / \beta)$ for the diameter.
2. Fix the shifts on a path of 6 nodes as $\delta = (0.2, 2.7, 0.1, 0.4, 1.6, 0.3)$. Find the centre of every node and the cut edges.
3. Prove that a node $v$ whose best value beats its second best by more than 2 has all its neighbours in its own cluster, and use this to show that the expected number of nodes with a neighbour in another cluster is at most $(1 - e^{-2\beta}) n$.

## References
