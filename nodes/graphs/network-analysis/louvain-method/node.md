---
tag: GC71E9
kind: algorithm
slug: louvain-method
name: Louvain method
aliases:
- Louvain algorithm
area: graphs/network-analysis
level: core
summary: Greedy modularity optimisation with hierarchical aggregation of communities.
solves: [community-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m^2 (n + m)), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 2008
  people: [Vincent D. Blondel, Jean-Loup Guillaume, Renaud Lambiotte, Etienne Lefebvre]
  note: Published in the Journal of Statistical Mechanics in 2008; named after the Université catholique de Louvain, where most of the authors worked.
prereqs: [modularity, community-detection, weighted-graph]
see_also: [leiden-algorithm, label-propagation-algorithm, girvan-newman-algorithm, infomap, spectral-clustering, stochastic-block-model]
sources:
  - paper: doi:10.1088/1742-5468/2008/10/P10008
    title: Vincent D. Blondel, Jean-Loup Guillaume, Renaud Lambiotte and Etienne Lefebvre, Fast unfolding of communities in large networks, Journal of Statistical Mechanics, Theory and Experiment 2008, P10008 (2008)
    locator: Section 2, the two phases (local moving with the modularity gain formula, then aggregation), and Section 3, the tests on the Belgian phone network and the web graph
  - paper: doi:10.1038/s41598-019-41695-z
    title: V. A. Traag, L. Waltman and N. J. van Eck, From Louvain to Leiden, guaranteeing well-connected communities, Scientific Reports 9, 5233 (2019)
    locator: the section on the Louvain algorithm, which shows that it can return badly connected and even disconnected communities
  - paper: doi:10.1103/PhysRevE.70.066111
    title: Aaron Clauset, M. E. J. Newman and Cristopher Moore, Finding community structure in very large networks, Physical Review E 70, 066111 (2004)
    locator: the greedy agglomerative maximization of modularity that the Louvain method improved on
  - paper: doi:10.1109/TKDE.2007.190689
    title: Ulrik Brandes, Daniel Delling, Marco Gaertler, Robert Görke, Martin Hoefer, Zoran Nikoloski and Dorothea Wagner, On modularity clustering, IEEE Transactions on Knowledge and Data Engineering 20(2), 172 to 188 (2008)
    locator: the NP-completeness of maximizing modularity, which is why heuristics such as this one are used
---

The Louvain method finds [communities](/community-detection/) by raising [modularity](/modularity/) greedily, one vertex at a time, and then shrinking each community to a single vertex and repeating on the smaller graph. In the first phase, each vertex moves to the neighbouring community that gives the largest gain in modularity, until no move helps. In the second phase, the communities become the vertices of a new weighted graph. The two phases repeat until a level changes nothing. Each sweep over the vertices costs $O(n + m)$ time, and the method handles graphs with hundreds of millions of edges. It returns a hierarchy of partitions, but no guarantee of how close it is to the best modularity, and its communities can be badly connected.

## In plain words

Imagine a party where everyone starts alone. One by one, each guest looks at the groups their friends are in, and joins the group where they add the most to a score of how well the groups hang together. Guests keep moving until nobody can raise the score by switching.

Then each group is treated as one big guest. The big guests play the same game: whole groups can now merge with other groups. This repeats, with fewer and bigger guests each time, until no merge raises the score. The groups at the end are the communities, and the groups at each earlier stage give a finer view.

## The problem

The input is an undirected [weighted graph](/weighted-graph/) $G = (V, E)$ with $n$ vertices, $m$ edges and positive edge weights $A_{ij}$, possibly with self-loops; an unweighted graph has all weights 1. Let $k_i = \sum_j A_{ij}$ be the weighted degree, with a self-loop counted twice, and $W = \frac12 \sum_i k_i$ the total weight. The goal is a partition $\mathcal{C}$ of $V$ with large modularity

$$Q(\mathcal{C}) = \sum_{C \in \mathcal{C}} \left( \frac{\mathrm{in}(C)}{W} - \left( \frac{\mathrm{tot}(C)}{2W} \right)^2 \right),$$

where $\mathrm{in}(C)$ is the total weight of the edges with both ends in $C$ and $\mathrm{tot}(C) = \sum_{i \in C} k_i$. Finding the maximum is NP-hard, as Brandes and co-authors show, so the method is a heuristic: it returns a partition where no single move of a vertex of the last level raises $Q$.

**Modularity gain.** Take a vertex $v$ out of its community, so it stands alone. Putting it into a community $C$ that does not contain it changes $Q$ by

$$\Delta Q(v, C) = \frac{k_{v,C}}{W} - \frac{\mathrm{tot}(C) \, k_v}{2W^2},$$

where $k_{v,C}$ is the total weight of the edges from $v$ to $C$. This needs only the weights at $v$ and one number per community, so each move costs $O(\deg(v))$.

## The algorithm

```pseudo id=main
LOUVAIN(G)
L1  P ← the partition of V into singletons; H ← G
L2  loop
L3      comm[v] ← v for each vertex v of H
L4      repeat                                         ▷ phase 1: local moving
L5          improved ← false
L6          for each vertex v of H, in a fixed order do
L7              remove v from comm[v]; old ← its community
L8              C ← the community, among old and those of the neighbours of v, with the largest ΔQ(v, C); keep old on ties, else take the smallest id
L9              put v into C; if C ≠ old then improved ← true
L10         until not improved
L11     if no vertex of H changed community in lines L4 to L10 then return P
L12     P ← the partition of V that merges the parts of P in each community of H
L13     H ← the graph with one vertex per community, the edge weight between two communities the sum of the weights between them, and a self-loop of weight in(C)   ▷ phase 2
```

Each vertex of $H$ stands for a part of $P$, so the partitions of the vertices of $H$ are partitions of $V$ that keep the parts of $P$ together. The modularity of a partition of $H$, computed in $H$ with its self-loops, equals the modularity of the matching partition of $V$ in $G$; this is why the aggregation is correct.

**Ties, order and disconnected graphs.** The order of line L6 and the tie rule of line L8 change the result. Blondel and co-authors note that the order has little effect on the final modularity but can change the running time. This page fixes the order of the vertex indices and the tie rule above, which makes the method deterministic. A vertex only joins a community of a neighbour, so every community stays inside one [connected component](/connected-components/), and an isolated vertex stays alone. A graph with no edges has no modularity, and the method returns the singletons.

**Directed graphs.** The method is stated for undirected graphs. With the directed form of modularity of Leicht and Newman, the gain has one term for out-degrees and one for in-degrees, and the same two phases apply.

## Example

Take the vertices 0 to 6 and the unit-weight edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$, so $W = 9$. Communities are named by the vertex that started them. The gains are $\Delta Q$ values.

| sweep | vertex | gains | move |
|---|---|---|---|
| 1 | 0 | stay 0; to 1: 2/27; to 2: 2/27 | joins 1 (tie, smallest id) |
| 1 | 1 | stay 2/27; to 2: 1/18; to 3: 1/18 | stays |
| 1 | 2 | stay 0; to 1: 7/54; to 3: 1/18 | joins 1 |
| 1 | 3 | stay 0; to 1: 2/27; to 4: 1/18 | joins 1 |
| 1 | 4 | stay 0; to 1: -5/54; to 5: 2/27; to 6: 2/27 | joins 5 (tie, smallest id) |
| 1 | 5 | stay 2/27; to 6: 7/81 | joins 6 |
| 1 | 6 | stay 7/81; to 5: 2/27 | stays |
| 2 | 4 | stay 0; to 1: -5/54; to 6: 4/27 | joins 6 |
| 3 | all | | no move |

In sweep 2, the vertices other than 4 stay where they are.

After sweep 1 the communities are $\{0,1,2,3\}$, $\{4\}$, $\{5,6\}$ with $Q = 47/324 \approx 0.145$; after sweep 2 they are $\{0,1,2,3\}$ and $\{4,5,6\}$ with $Q = 59/162 \approx 0.364$. Vertex 4 moved to the community of 5 first, and that community then lost vertex 5, which shows how moves undo each other. The second level has two vertices, with self-loops of weight 5 and 3 and an edge of weight 1. Merging them has the gain $1/9 - 6 \cdot 12/(2 \cdot 81) = -1/3$, so nothing moves and the method returns $\{0,1,2,3\}$, $\{4,5,6\}$, the partition of largest modularity of this graph.

## Correctness

The method never lowers $Q$: line L8 moves a vertex only when the gain of the new community is strictly larger than the gain of returning to the old one, so each move raises $Q$ by a positive amount, and phase 2 keeps $Q$ unchanged. For integer weights, $4W^2 Q$ is an integer, so each move raises it by at least 1, and since $-1 \le Q < 1$, there are fewer than $8W^2$ moves in the whole run. Each level that moves something raises $Q$ above that of the all-singleton partition of $H$, so it merges some vertices, and $H$ shrinks; so there are at most $n$ levels. At the end, no single vertex of the last $H$ can move to a neighbouring community and raise $Q$. The full proof, with the identity behind the gain formula and the invariance of $Q$ under aggregation, is in [the proof page](proofs/correctness.md).

## Complexity

- **One sweep.** Line L8 sums the weights from $v$ to each neighbouring community with a hash map and reads $\mathrm{tot}(C)$ from an array, so it costs $O(\deg(v))$, and a sweep costs $O(n + m)$.
- **Aggregation.** Line L13 scans every edge of $H$ once, $O(n + m)$.
- **Worst case.** By the counting argument above, an unweighted graph has fewer than $8m^2$ moves in all. Every sweep but the last of each level makes a move, so there are $O(m^2 + n)$ sweeps, and the time is $O(m^2 (n + m))$. This bound is crude, and no matching bad example is known to this page.
- **In practice.** The first level does most of the work, the number of sweeps is small, and the graph shrinks fast, so the run time is close to linear in $m$. Blondel and co-authors processed a web graph with about 118 million vertices and a billion edges.
- **Best case.** A graph where no vertex gains by moving stops after one sweep of one level, $\Theta(n + m)$.
- **Space.** The community labels, the totals and the aggregated graph take $\Theta(n + m)$ words.

## Properties

- **Hierarchical.** Each level gives a partition, coarser than the one before, so the output is a dendrogram of a few levels.
- **Deterministic for a fixed order.** Most implementations shuffle the order, which makes the result random; Blondel and co-authors report that the order has little effect on the modularity reached.
- **Locally optimal, not globally.** No single vertex of the last level can improve $Q$ by moving, but moves of single vertices of $G$ can still help, and the optimum can be far away.
- **Badly connected communities.** Traag, Waltman and van Eck show that a community can become disconnected: a vertex that holds it together can move away in a later sweep, and later levels never split a community again. The [Leiden algorithm](/leiden-algorithm/) fixes this.
- **Resolution limit.** As a modularity maximizer, it inherits the resolution limit: it can merge small, clearly separate groups in a large graph.

## Variants and improvements

- **Resolution parameter.** Multiply the second term of $\Delta Q$ by $\gamma$; larger $\gamma$ gives smaller communities.
- **Leiden algorithm.** Adds a refinement phase between local moving and aggregation, so that every community is connected, and moves only vertices whose neighbourhood changed.
- **Parallel and distributed versions.** Move many vertices at once, with rules to avoid swapping pairs, on shared-memory machines and GPUs.
- **Other objectives.** The two-phase scheme works for any objective that is a sum over communities, such as the map equation in [Infomap](/infomap/).

## When to use it

Use it for a good modularity partition of a large graph in seconds, or a few coarse levels of community structure. It is a standard default in network analysis tools. Prefer the [Leiden algorithm](/leiden-algorithm/), which has the same speed and fixes the disconnected communities. For tiny graphs where an exact or near-exact answer is wanted, use exact modularity maximization; for a fast, rougher answer on huge graphs, use [label propagation](/label-propagation-algorithm/).

## Pitfalls

- **Floating-point gains.** Gains of equal value can differ in the last digits, so the tie rule of line L8 becomes random. Compare with a small tolerance, or use exact arithmetic on small integer weights.
- **Wrong self-loops in the aggregate.** In line L13, the self-loop of a community must carry the internal weight $\mathrm{in}(C)$, and the degree of the new vertex must count it twice. Otherwise the modularity of the new graph differs from that of the partition of $G$.
- **Reading the levels as a ground truth.** The intermediate levels depend on the order and are not the optimal partitions at their scale.
- **Assuming connected communities.** Check and split communities into connected parts if the application needs it, or use Leiden.

## Implementations

## History

Clauset, Newman and Moore gave in 2004 a fast greedy method that merges, again and again, the pair of communities with the largest gain in modularity. In 2008 Vincent Blondel, Jean-Loup Guillaume, Renaud Lambiotte and Etienne Lefebvre at the Université catholique de Louvain proposed the method of local moves and aggregation, tested it on a Belgian mobile phone network of about 2.6 million customers, where the communities matched the language groups, and on a web graph of 118 million vertices. It became the most used community detection method. In 2019 Traag, Waltman and van Eck showed its connectivity problem and proposed the Leiden algorithm.

## References
