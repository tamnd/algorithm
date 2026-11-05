---
tag: K4ZNR0
kind: algorithm
slug: leiden-algorithm
name: Leiden algorithm
aliases:
- Leiden
area: graphs/network-analysis
level: advanced
summary: Improves Louvain by guaranteeing well-connected communities.
solves: [community-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n m^2 (n + m)), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 2019
  people: [Vincent A. Traag, Ludo Waltman, Nees Jan van Eck]
  note: Published in Scientific Reports in 2019; named after Leiden University, where the authors work at the Centre for Science and Technology Studies.
prereqs: [louvain-method, modularity, community-detection, connected-components]
see_also: [louvain-method, label-propagation-algorithm, infomap, girvan-newman-algorithm, stochastic-block-model, spectral-clustering]
sources:
  - paper: doi:10.1038/s41598-019-41695-z
    title: V. A. Traag, L. Waltman and N. J. van Eck, From Louvain to Leiden, guaranteeing well-connected communities, Scientific Reports 9, 5233 (2019)
    locator: the section on the Leiden algorithm (fast local moving, refinement and aggregation based on the refined partition), the guarantees of Table 1, and the pseudocode and proofs of the Supplementary Information
  - paper: doi:10.1088/1742-5468/2008/10/P10008
    title: Vincent D. Blondel, Jean-Loup Guillaume, Renaud Lambiotte and Etienne Lefebvre, Fast unfolding of communities in large networks, Journal of Statistical Mechanics, Theory and Experiment 2008, P10008 (2008)
    locator: Section 2, the local moving and aggregation phases that the Leiden algorithm keeps
  - paper: doi:10.1140/epjb/e2013-40829-0
    title: Ludo Waltman and Nees Jan van Eck, A smart local moving algorithm for large-scale modularity-based community detection, European Physical Journal B 86, 471 (2013)
    locator: the smart local moving algorithm, which splits communities into subcommunities before aggregation, the idea behind the refinement phase
  - paper: doi:10.1103/PhysRevE.84.016114
    title: V. A. Traag, P. Van Dooren and Y. Nesterov, Narrow scope for resolution-limit-free community detection, Physical Review E 84, 016114 (2011)
    locator: the constant Potts model, the second quality function that the Leiden algorithm optimizes
  - paper: doi:10.1073/pnas.0605965104
    title: Santo Fortunato and Marc Barthélemy, Resolution limit in community detection, Proceedings of the National Academy of Sciences 104(1), 36 to 41 (2007)
    locator: the resolution limit of modularity, which the Leiden algorithm inherits when it maximizes modularity
---

The Leiden algorithm finds [communities](/community-detection/) by raising [modularity](/modularity/), like the [Louvain method](/louvain-method/), but it adds a refinement phase that keeps every community connected. Each round moves vertices to better communities, with a queue so that only vertices whose neighbourhood changed are visited again. It then splits each community into well-connected pieces by merging lone vertices inside it, and shrinks each piece, not each community, to a single vertex of the next graph. Traag, Waltman and van Eck introduced it in 2019 after showing that Louvain can return badly connected and even disconnected communities. Every community it returns is connected, it is often faster than Louvain, and it reaches the same or higher modularity, but, like Louvain, it gives no bound on how far it is from the best partition.

## In plain words

Start with everyone alone, and let each person join the group of a friend when that raises the score of how well the groups hang together, as in the Louvain method. A queue keeps track of who should look again: when someone moves, their friends outside the new group are put back in line.

Louvain then glues each whole group into one big person. The trouble is that a group can lose the one member who held it together, and gluing it then freezes a group made of two parts that do not touch. Leiden checks first: inside each group, it builds small pieces, each grown by adding a lone person who is well linked to a piece. Only these pieces are glued. A piece is always connected, and the groups at the end are pieces, so they are connected too.

## The problem

The input is an undirected [weighted graph](/weighted-graph/) $G = (V, E)$ with $n$ vertices, $m$ edges and positive integer weights $A_{ij}$, possibly with self-loops. As on the [Louvain page](/louvain-method/), $k_i = \sum_j A_{ij}$ is the weighted degree with a self-loop counted twice, $W = \frac12 \sum_i k_i$, and a partition $\mathcal{C}$ of $V$ has modularity

$$Q(\mathcal{C}) = \sum_{C \in \mathcal{C}} \left( \frac{\mathrm{in}(C)}{W} - \left( \frac{\mathrm{tot}(C)}{2W} \right)^2 \right),$$

with $\mathrm{in}(C)$ the weight inside $C$ and $\mathrm{tot}(C) = \sum_{i \in C} k_i$. The goal is a partition with large $Q$ in which every community induces a [connected](/connected-graph/) subgraph.

**Modularity gain.** For a vertex $v$ taken out of its community, so that it stands alone, and a community $C$ that does not contain it,

$$\Delta Q(v, C) = \frac{k_{v,C}}{W} - \frac{\mathrm{tot}(C) \, k_v}{2W^2},$$

where $k_{v,C}$ is the weight of the edges from $v$ to $C$. Joining an empty community has gain 0.

**Well connected.** Inside a community $C$, a set $S \subseteq C$ is *well connected* when

$$E(S, C \setminus S) \ge \frac{\mathrm{tot}(S) \, (\mathrm{tot}(C) - \mathrm{tot}(S))}{2W},$$

where $E(S, T)$ is the weight of the edges between $S$ and $T$. This is the modularity form of the $\gamma$-connectivity of Traag and co-authors, with $\gamma = 1/2W$; for a single vertex it says $\Delta Q(v, C \setminus \{v\}) \ge 0$.

## The algorithm

```pseudo id=main
LEIDEN(G)
L1  P ← the partition of V into singletons
L2  repeat
L3      P_old ← P; H ← G                                ▷ each vertex of H stands for a set of vertices of G
L4      loop
L5          P ← MOVE-NODES-FAST(H, P)
L6          if every community of P is a single vertex of H then exit the loop
L7          R ← REFINE(H, P)
L8          H ← the graph with one vertex per part of R, edge weights summed and a self-loop of weight in(S) for each part S
L9          P ← the partition of the vertices of H that puts two parts of R together when they lie in the same community of P
L10 until P, read as a partition of V, equals P_old
L11 return P, read as a partition of V
```

```pseudo id=move
MOVE-NODES-FAST(H, P)
L12 Q ← a queue of all vertices of H in index order
L13 while Q is not empty do
L14     v ← the front of Q, removed; take v out of comm[v]; old ← its community
L15     C ← among old, the communities of the neighbours of v and an empty community, the one with the largest ΔQ(v, C); keep old on ties, else take the smallest id, the empty community last
L16     put v into C
L17     if C ≠ old then append to Q each neighbour w of v with comm[w] ≠ C that is not in Q
L18     if Q is empty then append to Q each vertex that line L15 would move   ▷ a final check that this page adds
L19 return P
```

```pseudo id=refine
REFINE(H, P)
L20 R ← the partition of the vertices of H into singletons
L21 for each community C of P, in the order of its smallest vertex do
L22     A ← the vertices v of C such that {v} is well connected in C
L23     for each v of A in index order do
L24         if v is alone in its part of R then
L25             T ← the parts S ⊆ C of R, other than {v}, that are adjacent to v and well connected in C
L26             S ← the part of T with the largest ΔQ(v, S); ties to the smallest id
L27             if T is not empty and ΔQ(v, S) ≥ 0 then move v into S
L28 return R
```

Each vertex of $H$ stands for a set of vertices of $G$, so a partition of the vertices of $H$ is a partition of $V$. Line L8 builds $H$ from the refined partition $R$, but line L9 starts the next level from the communities of $P$, not from $R$; so the communities do not shrink, but each one may now be split again by the next round of moves. The modularity of a partition of $H$, computed in $H$ with its self-loops, equals the modularity of the matching partition of $V$ in $G$, as on the Louvain page.

**What differs from Louvain.**

- *Fast local moving.* Louvain sweeps over all vertices until a sweep moves nothing. Leiden keeps a queue and revisits only the neighbours of a vertex that moved. Traag and co-authors stop when the queue is empty; this page adds line L18, one more pass over all vertices, because a move also changes $\mathrm{tot}$ of two communities and can make a vertex that is not a neighbour want to move. With this check, the end of MOVE-NODES-FAST is a partition where no vertex gains by moving.
- *Empty community.* A vertex may leave and stand alone, which Louvain does not try.
- *Refinement.* Lines L20 to L28. The parts of $R$ grow only by merging a lone vertex with an adjacent part of the same community, so each part is connected.
- *Aggregation by $R$.* Line L8 uses $R$, which is finer than $P$, so a community whose parts drifted apart can still split at the next level.
- *Repetition.* Lines L2 to L10 run the whole algorithm again from its own output until nothing changes, as the authors advise and the leidenalg package does with a negative number of iterations.

**Randomness.** In the paper, line L26 picks $S$ at random with probability proportional to $\exp(\Delta Q(v, S)/\theta)$ among the parts with $\Delta Q \ge 0$, and the order of the queue is random. This page takes the limit $\theta \to 0$, the part of largest gain, and fixes the order, which makes the algorithm deterministic. Traag and co-authors note that the randomness helps to explore more partitions; the connectivity guarantee does not depend on it.

**Quality functions.** The same algorithm works for any quality that is a sum over communities and has a gain formula of this form. The authors use modularity with a resolution parameter and the constant Potts model of Traag, Van Dooren and Nesterov, for which $\mathrm{tot}$ is replaced by the number of vertices and $\gamma$ is a free parameter.

## Example

Take the graph of the Louvain page: the vertices 0 to 6 and the unit-weight edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$, so $W = 9$. Communities are named by the vertex that started them. The gains are $\Delta Q$ values; the gain of an empty community is 0 and is not shown.

| step | vertex | gains | move | queue after |
|---|---|---|---|---|
| 1 | 0 | stay 0; to 1: 2/27; to 2: 2/27 | joins 1 | 1 2 3 4 5 6 |
| 2 | 1 | stay 2/27; to 2: 1/18; to 3: 1/18 | stays | 2 3 4 5 6 |
| 3 | 2 | stay 0; to 1: 7/54; to 3: 1/18 | joins 1 | 3 4 5 6 |
| 4 | 3 | stay 0; to 1: 2/27; to 4: 1/18 | joins 1 | 4 5 6 |
| 5 | 4 | stay 0; to 1: -5/54; to 5: 2/27; to 6: 2/27 | joins 5 | 5 6 3 |
| 6 | 5 | stay 2/27; to 6: 7/81 | joins 6 | 6 3 4 |
| 7 | 6 | stay 7/81; to 5: 2/27 | stays | 3 4 |
| 8 | 3 | stay 2/27; to 5: 1/18 | stays | 4 |
| 9 | 4 | stay 0; to 1: -5/54; to 6: 4/27 | joins 6 | 3 |
| 10 | 3 | stay 2/27; to 6: -1/54 | stays | empty |

When vertex 4 joins community 5, its neighbour 3 goes back into the queue; vertex 6 is already there. The check of line L18 finds no vertex that wants to move. The communities are $\{0,1,2,3\}$ and $\{4,5,6\}$, with $Q = 59/162 \approx 0.364$.

The refinement of $\{0,1,2,3\}$, with $\mathrm{tot} = 11$: every vertex is well connected, for example vertex 0 has $E = 2 \ge 2 \cdot 9/18$. Vertex 0 joins $\{1\}$, with gain $2/27$, tied with $\{2\}$ and broken by the smaller id. Vertex 1 is no longer alone. Vertex 2 can join $\{0,1\}$, with gain $7/54$, or $\{3\}$, with gain $1/18$; it joins $\{0,1\}$. Vertex 3 joins $\{0,1,2\}$ with gain $2/27 \ge 0$. In the same way $\{4,5,6\}$ becomes one part. So $R = P$, and $H$ has two vertices, with self-loops of weight 5 and 3 and an edge of weight 1. Merging them has gain $-1/3$, so nothing moves, each community is a single vertex of $H$, and the loop ends. The second pass from this partition changes nothing, and the algorithm returns $\{0,1,2,3\}$, $\{4,5,6\}$, the same answer as Louvain.

## Correctness

Every move of line L15 raises $Q$ strictly, since a vertex keeps its community on ties, and lines L7 to L9 do not change the partition of $V$; the refinement only merges inside communities, and the aggregation keeps $Q$, as on the Louvain page. For integer weights, $4W^2 Q$ is an integer, so there are fewer than $8W^2$ moves in all, and every loop ends. At the start of a refinement, every vertex of a community $C$ with two or more vertices is well connected in $C$, because MOVE-NODES-FAST ended with no vertex that gains by standing alone. The gains of the first vertex of $C$ toward the other singletons of $C$ add up to $\Delta Q(v, C \setminus \{v\}) \ge 0$, so one of them is non-negative and line L27 merges something. So $H$ loses a vertex at each level, and the loop of lines L4 to L9 ends after at most $n$ levels.

The communities returned are connected. Each vertex of $H$ stands for a connected set of vertices of $G$: a part of $R$ grows only by a vertex adjacent to it. At line L6, each community is a single vertex of $H$. In the last pass, nothing moves, so the first call of MOVE-NODES-FAST on $G$ itself shows that no vertex of $G$ gains by moving to the community of a neighbour or by standing alone. The full proof is in [the proof page](proofs/correctness.md). The paper proves more: after each level, the communities are $\gamma$-separated and $\gamma$-connected, and when the iteration converges they are uniformly $\gamma$-dense and subset optimal. This page states those results and does not prove them.

## Complexity

- **One visit.** Line L15 sums the weights from $v$ to each neighbouring community with a hash map, so it costs $O(\deg(v))$; finding an empty community takes $O(1)$ with a list of free ids (the Python code scans, $O(n)$).
- **Queue.** A vertex enters the queue only when a neighbour moved or the check of line L18 found it, so the visits after the first pass cost $O(\sum_{\text{moves}} \deg(v))$, plus $O(n + m)$ per check.
- **Refinement and aggregation.** Each costs $O(n + m)$ on $H$: the sums $E(S, C \setminus S)$ and $\mathrm{tot}(S)$ are kept per part and updated in $O(\deg(v))$ per merge.
- **Worst case.** For unit weights there are fewer than $8m^2$ moves in all, at most $n$ levels in a pass, and each pass but the last makes a move. Each check that finds a vertex is followed by a move, so the number of checks is at most the number of moves plus the number of calls. This gives $O(n m^2 (n + m))$ time, a crude bound like that of Louvain.
- **In practice.** Traag and co-authors measured it as faster than Louvain on large benchmark graphs and real networks, mostly because the queue avoids visiting stable vertices.
- **Best case.** A graph where no vertex gains by moving stops after one call of MOVE-NODES-FAST and one check, $\Theta(n + m)$.
- **Space.** The labels, the totals, the queue and the aggregated graph take $\Theta(n + m)$ words.

## Properties

- **Connected communities.** Every community returned induces a connected subgraph of $G$. Traag and co-authors found that Louvain left up to a quarter of its communities badly connected and up to 16% disconnected on some real networks.
- **Locally optimal for single vertices.** At the end, no vertex of $G$ raises $Q$ by moving to the community of a neighbour or by standing alone. Louvain guarantees this only for the vertices of its last graph.
- **Never lower modularity.** $Q$ increases at each move and never decreases.
- **Hierarchical.** The communities of one level are unions of the vertices of $H$, and each vertex of $H$ is a connected piece.
- **Deterministic as written.** The randomized version of the paper can give different partitions on different runs.
- **Resolution limit.** With modularity, it inherits the resolution limit of Fortunato and Barthélemy. The constant Potts model avoids it.

## Variants and improvements

- **Constant Potts model.** Replace the null model term by $\gamma \binom{|C|}{2}$; the resolution $\gamma$ then sets a density threshold that does not depend on the size of the graph.
- **Resolution parameter.** Multiply the second term of $\Delta Q$ by $\gamma$; larger $\gamma$ gives smaller communities.
- **Randomized refinement.** The choice of line L26 with probability proportional to $\exp(\Delta Q/\theta)$ explores more of the space, with $\theta = 0.01$ as the default of the authors.
- **Fixed number of iterations.** The authors often run two passes instead of iterating to a fixed point; the guarantees of the paper are stated for the fixed point.
- **Smart local moving.** The earlier algorithm of Waltman and van Eck also splits communities before aggregation, by running local moving inside each community, but it is slower.
- **Parallel versions.** Shared-memory implementations move many vertices at once and refine the communities in parallel.

## When to use it

Use it in place of the [Louvain method](/louvain-method/) whenever communities must be connected, which is most of the time, and when speed matters on large graphs; it is the default in tools such as Scanpy for clustering single-cell data. To find communities by the flow of a random walk instead of by density, use [Infomap](/infomap/). For a fast and rough answer on huge graphs, use [label propagation](/label-propagation-algorithm/). For a statistical model with a likelihood, fit a [stochastic block model](/stochastic-block-model/).

## Pitfalls

- **Stopping at the empty queue.** Without the check of line L18, a vertex far from the last move can still gain by moving; the paper accepts this for speed, but then the end result is not locally optimal for single vertices.
- **Aggregating by $P$ instead of $R$.** That is Louvain again, and the connectivity guarantee is lost.
- **Floating-point gains.** Equal gains can differ in the last digits, so the tie rules become random; compare with a tolerance or use exact arithmetic.
- **Reading one run as the answer.** The randomized version can return different partitions; run it several times or fix the seed.
- **Resolution.** Small, clearly separate groups can merge in a large graph when modularity is the quality; try the constant Potts model or several resolutions.

## Implementations

## History

The [Louvain method](/louvain-method/) of Blondel and co-authors (2008) became the standard heuristic for modularity. In 2013 Waltman and van Eck proposed smart local moving, which runs local moving inside each community before aggregation. In 2019 Vincent Traag, Ludo Waltman and Nees Jan van Eck, at the Centre for Science and Technology Studies of Leiden University, showed that Louvain can return disconnected communities. They proposed the Leiden algorithm, with fast local moving, the refinement phase and aggregation by the refined partition, proved its guarantees and released the leidenalg package.

## References
