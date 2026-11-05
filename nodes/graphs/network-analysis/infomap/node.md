---
tag: R7CYRH
kind: algorithm
slug: infomap
name: Infomap
aliases:
- map equation
area: graphs/network-analysis
level: advanced
summary: Finds communities that minimise the description length of random-walk trajectories.
solves: [community-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 2008
  people: [Martin Rosvall, Carl T. Bergstrom]
  note: The map equation appeared in the Proceedings of the National Academy of Sciences in 2008; the fast two-phase search, close to the Louvain method, followed in 2009 with Daniel Axelsson.
prereqs: [community-detection, shannon-entropy, huffman-coding, stationary-distribution, weighted-graph]
see_also: [louvain-method, leiden-algorithm, label-propagation-algorithm, markov-clustering, walktrap-algorithm, pagerank, minimum-description-length]
sources:
  - paper: doi:10.1073/pnas.0706851105
    title: Martin Rosvall and Carl T. Bergstrom, Maps of random walks on complex networks reveal community structure, Proceedings of the National Academy of Sciences 105(4), 1118 to 1123 (2008)
    locator: the map equation (the two-level code of a random walk, with an index codebook and one codebook per module), and the search by greedy merging and simulated annealing
  - paper: doi:10.1140/epjst/e2010-01179-1
    title: M. Rosvall, D. Axelsson and C. T. Bergstrom, The map equation, European Physical Journal Special Topics 178, 13 to 23 (2009)
    locator: the expanded form of the map equation with the plogp terms, the flows of undirected and directed networks, and the core algorithm of repeated local moves and aggregation with submodule and single-node movements
  - paper: doi:10.1371/journal.pone.0018209
    title: Martin Rosvall and Carl T. Bergstrom, Multilevel compression of random walks on networks reveals hierarchical organization in large integrated systems, PLoS ONE 6(4), e18209 (2011)
    locator: the hierarchical map equation and the multilevel version of Infomap
  - paper: doi:10.1103/PhysRevE.80.056117
    title: Andrea Lancichinetti and Santo Fortunato, Community detection algorithms, a comparative analysis, Physical Review E 80, 056117 (2009)
    locator: the tests on the LFR benchmark graphs, where Infomap is among the most accurate methods
  - paper: doi:10.1103/PhysRevE.91.012809
    title: Tatsuro Kawamoto and Martin Rosvall, Estimating the resolution limit of the map equation in community detection, Physical Review E 91, 012809 (2015)
    locator: the resolution limit of the two-level map equation, which depends on the number of links between modules rather than on the size of the network
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 379 to 423 (1948)
    locator: the source coding theorem, the lower bound by the entropy on the mean length of a code word
---

Infomap finds [communities](/community-detection/) as the modules of a code for a random walk on the graph. A walker that moves along the edges spends long stretches inside a well-knit group, so a code that gives each group its own short names for its vertices, and spends extra bits only when the walker leaves a group, describes the walk in fewer bits. The *map equation* of Rosvall and Bergstrom gives the length $L(\mathcal{M})$ of this code per step for a partition $\mathcal{M}$, and Infomap searches for a partition with a small $L$. The search on this page is the core of the algorithm of Rosvall, Axelsson and Bergstrom: move one vertex at a time to the neighbouring module that shortens the code most, then shrink each module to a vertex and repeat, as in the [Louvain method](/louvain-method/). Each sweep costs $O(n + m)$ time, and the result is a local optimum with no bound on its distance to the best partition.

## In plain words

Picture a tourist who wanders a city at random, and a friend who must report each street corner the tourist reaches. If the friend names every corner with one code for the whole city, each name is long. If the city is split into districts, the friend can name corners with short local codes and only say "now entering a new district" when the tourist crosses a border. When the tourist rarely crosses borders, the report gets much shorter.

Infomap looks for the split into districts that makes the report shortest. A split that cuts through a dense neighbourhood makes the tourist cross borders all the time, which costs extra words. A split that lumps everything into one district loses the benefit of short local names. The best split sits in between, and its districts are the communities.

## The problem

The input is an undirected [weighted graph](/weighted-graph/) $G = (V, E)$ with $n$ vertices, $m$ edges, positive integer weights $A_{uv}$ and no self-loops. Let $k_u = \sum_v A_{uv}$ and $W = \frac12 \sum_u k_u$. A random walk that moves from $u$ to $v$ with probability $A_{uv}/k_u$ has the [stationary distribution](/stationary-distribution/) $p_u = k_u/2W$ when $W > 0$.

For a partition $\mathcal{M}$ of $V$ into modules, a module $i$ has the visit rate $p_i = \sum_{u \in i} p_u = \mathrm{tot}(i)/2W$ and the exit rate

$$q_i = \sum_{u \in i} \sum_{v \notin i} p_u \frac{A_{uv}}{k_u} = \frac{\mathrm{cut}(i)}{2W},$$

where $\mathrm{cut}(i)$ is the weight of the edges with one end in $i$. Let $q = \sum_i q_i$.

**The map equation.** The code has an index codebook that names the module entered, used at rate $q$, and one codebook per module $i$ that names its vertices and an exit word, used at rate $q_i + p_i$. By Shannon's source coding theorem, the best codes have mean lengths equal to the [entropies](/shannon-entropy/) of their frequencies, which gives

$$L(\mathcal{M}) = q \, H(\mathcal{Q}) + \sum_i (q_i + p_i) \, H(\mathcal{P}_i),$$

with $\mathcal{Q} = (q_i/q)_i$ and $\mathcal{P}_i$ the distribution $(q_i, (p_u)_{u \in i})$ divided by $q_i + p_i$. With $\mathrm{plogp}(x) = x \log_2 x$, it expands to

$$L(\mathcal{M}) = \mathrm{plogp}(q) - 2 \sum_i \mathrm{plogp}(q_i) - \sum_u \mathrm{plogp}(p_u) + \sum_i \mathrm{plogp}(q_i + p_i).$$

The goal is a partition with small $L$, in bits per step. The third sum does not depend on $\mathcal{M}$, so a move changes only the terms of the two modules involved and $q$.

**An exact form.** Write $f(a) = a \log_2 a$ for an integer $a \ge 0$, with $f(0) = 0$. Since every rate is an integer over $2W$, the terms in $\log_2 2W$ cancel, and

$$2W \, L(\mathcal{M}) = f\Bigl(\sum_i \mathrm{cut}(i)\Bigr) - 2 \sum_i f(\mathrm{cut}(i)) - \sum_u f(k_u) + \sum_i f(\mathrm{cut}(i) + \mathrm{tot}(i)).$$

So $2^{2W L}$ is a fraction of products of powers $a^a$ of integers, and two partitions can be compared exactly. The code on this page does this; it is practical only for small weights, and real implementations use floating point.

## The algorithm

```pseudo id=main
INFOMAP(G)
L1  P ← the partition of V into singletons; H ← G
L2  loop
L3      mod[v] ← v for each vertex v of H
L4      repeat                                         ▷ phase 1: local moving
L5          improved ← false
L6          for each vertex v of H, in a fixed order do
L7              remove v from mod[v]; old ← its module
L8              M ← the module, among old and those of the neighbours of v, that gives the smallest L; keep old on ties, else take the smallest id
L9              put v into M; if M ≠ old then improved ← true
L10         until not improved
L11     if no vertex of H changed module in lines L4 to L10 then return P
L12     P ← the partition of V that merges the parts of P in each module of H
L13     H ← the graph with one vertex per module, the edge weight between two modules the sum of the weights between them, and a self-loop of weight in(M)   ▷ phase 2
```

A vertex $x$ of $H$ has the flow of the part of $V$ it stands for: its degree $k_x$ is $\mathrm{tot}$ of that part, and its exit weight when alone is $k_x$ minus twice its self-loop, the cut of the part. With these, the map equation of a partition of $H$ equals the map equation of the matching partition of $V$, and line L8 needs only $\mathrm{cut}$ and $\mathrm{tot}$ of the modules, $k_{v,M}$ and the sum of the cuts.

**The change of one move.** Take $v$ out of its module, so that the other modules are $\mathcal{M}^-$. Putting $v$ into $M$ gives $M$ the cut $\mathrm{cut}(M) + c_v - 2k_{v,M}$, where $c_v$ is the exit weight of $v$ alone, and the total $\mathrm{tot}(M) + k_v$. The three terms of $M$ and the term of $q$ change, so each candidate costs $O(1)$ after the sums $k_{v,M}$ are found in $O(\deg(v))$.

**What this page leaves out.** The full Infomap does more, and these parts are not covered here.

- *Teleportation.* On a directed graph, the walk may get stuck, so the walker jumps to a random vertex with a small probability, as in [PageRank](/pagerank/), and the flows come from the power method. For an undirected connected graph no jump is needed and the flows are $k_u/2W$.
- *Directed graphs.* The exit rate then uses the flow on each arc, and $q_i$ is not $\mathrm{cut}(i)/2W$.
- *Multilevel map equation.* Rosvall and Bergstrom (2011) code a hierarchy of modules inside modules; this page uses two levels only.
- *Fine-tuning and coarse-tuning.* Rosvall, Axelsson and Bergstrom move single vertices out of the final modules, and move submodules found by running the algorithm inside each module; both can undo a bad early merge.
- *Random orders and several trials.* Implementations shuffle the order of line L6 and keep the best of many runs.
- *Self-loops in the input.* This page refuses them; with a self-loop the walk stays put with some probability, and implementations differ on how to count that.

## Example

Take the graph of the Louvain page: the vertices 0 to 6 and the unit-weight edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$, so $2W = 18$, the degrees are $2, 3, 3, 3, 3, 2, 2$, and $\sum_u f(k_u) = 6 + 12 \log_2 3$. Modules are named by the vertex that started them, and the table gives $L$ in bits, rounded, for each place where the vertex can go.

| sweep | vertex | $L$ for each module | move |
|---|---|---|---|
| 1 | 0 | stay 4.780; to 1: 4.415; to 2: 4.415 | joins 1 (tie, smallest id) |
| 1 | 1 | stay 4.415; to 2: 4.456; to 3: 4.456 | stays |
| 1 | 2 | stay 4.415; to 1: 3.734; to 3: 4.111 | joins 1 |
| 1 | 3 | stay 3.734; to 1: 3.111; to 4: 3.480 | joins 1 |
| 1 | 4 | stay 3.111; to 1: 3.249; to 5: 2.889; to 6: 2.889 | joins 5 (tie, smallest id) |
| 1 | 5 | stay 2.889; to 6: 2.834 | joins 6 |
| 1 | 6 | stay 2.834; to 5: 2.889 | stays |
| 2 | 4 | stay 2.834; to 1: 3.027; to 6: 2.444 | joins 6 |
| 3 | all | | no move |

In sweep 2, the vertices other than 4 stay. The moves are the same as those of the Louvain method on this graph. The two modules $\{0,1,2,3\}$ and $\{4,5,6\}$ each have cut 1 and totals 11 and 7, so by the exact form

$$18 \, L = f(2) - 2 \cdot 0 - (6 + 12 \log_2 3) + f(12) + f(8) = 2 - 6 - 12 \log_2 3 + 24 + 12 \log_2 3 + 24 = 44,$$

and $L = 22/9 \approx 2.444$ bits. The second level has two vertices, and merging them gives one module with $L = H(p) \approx 2.780$, the entropy of the degree distribution, so nothing moves and the algorithm returns $\{0,1,2,3\}$, $\{4,5,6\}$. The partition into singletons costs $H(p) + 2 \approx 4.780$ bits: for singletons, the formula reduces to exactly 2 bits more than for one module.

## Correctness

Each move of line L8 lowers $L$ strictly, since a vertex keeps its module on ties, and line L13 keeps $L$ unchanged, because the map equation depends only on the cut and the total of each module and these are the same in $H$ as in $G$. There are finitely many partitions of $V$, so the moves stop. A level that moves something ends with a partition of $H$ with smaller $L$ than the singletons, so it merges some vertices, and there are at most $n$ levels. At the end, no vertex of the last graph $H$, that is no module, lowers $L$ by joining the module of a neighbour. The proof, with the exact form and the invariance under aggregation, is in [the proof page](proofs/correctness.md).

## Complexity

- **One sweep.** Line L8 sums the weights from $v$ to each neighbouring module with a hash map and evaluates the change of $L$ for each in $O(1)$ arithmetic operations, so a sweep costs $O(n + m)$. The exact powers of the Python code make each operation cost more than $O(1)$; with floating point it is $O(1)$.
- **Aggregation.** Line L13 scans every edge of $H$ once, $O(n + m)$.
- **Number of sweeps.** Each sweep but the last of a level lowers $L$, and there are at most $n$ levels. Unlike modularity, $2W L$ is not an integer, and this page knows no polynomial bound on the number of moves. In practice the sweeps are few, as for Louvain.
- **Best case.** A graph where no vertex gains by moving stops after one sweep of one level, $\Theta(n + m)$.
- **Space.** The module labels, the cuts, the totals and the aggregated graph take $\Theta(n + m)$ words.

## Properties

- **A flow-based objective.** Modularity counts edges inside groups against a random null model; the map equation measures how long a random walk stays inside a group. On graphs where flow and density agree, both find the same groups, as in the example.
- **No free parameter.** The two-level map equation has no resolution parameter. It has a resolution limit of its own, which Kawamoto and Rosvall show depends on the number of edges between modules rather than on the size of the graph, so it is less severe than that of modularity.
- **One module wins on graphs without structure.** On a complete graph or a random graph without groups, one module gives the shortest code, so Infomap reports no communities; modularity maximization still splits such graphs.
- **Locally optimal, not globally.** No single vertex of the last level can shorten the code by moving to the module of a neighbour, but the optimum can be far away.
- **Communities can be disconnected.** As in Louvain, a vertex that holds a module together can leave in a later sweep, and later levels never split a module again.
- **Accurate on benchmarks.** Lancichinetti and Fortunato found Infomap among the most accurate methods on the LFR benchmark graphs.

## Variants and improvements

- **Directed and weighted flows.** Compute $p_u$ and the arc flows by the power method with teleportation, then use the same map equation.
- **Hierarchical map equation.** Code modules inside modules; the multilevel Infomap of Rosvall and Bergstrom finds the number of levels.
- **Overlapping modules.** Let a vertex be named in several module codebooks, or use higher-order flows with memory, so that a vertex can belong to several modules.
- **Other search strategies.** The first version merged modules greedily and refined the result with simulated annealing; the two-phase search on this page is much faster.

## When to use it

Use it when communities should be groups where flow stays, for example citation, traffic or information networks, and especially for directed graphs, where the full Infomap with teleportation applies. It is accurate on benchmarks and needs no resolution parameter. To optimise [modularity](/modularity/) with connected communities, use the [Leiden algorithm](/leiden-algorithm/). For a quick rough answer on huge graphs, use [label propagation](/label-propagation-algorithm/). For flow-based clustering by random-walk powers, see [Markov clustering](/markov-clustering/).

## Pitfalls

- **Wrong flows.** For an undirected graph the visit rates are $k_u/2W$; using a uniform distribution or forgetting the factor 2 changes the codelength and the result.
- **Floating-point ties.** Equal codelengths can differ in the last digits, so the tie rule of line L8 becomes random; compare with a tolerance.
- **Disconnected input.** A random walk cannot leave its component, but the flows are still $k_u/2W$. A vertex joins only the module of a neighbour, so a module never spans two components.
- **Comparing codelengths across graphs.** $L$ depends on the entropy of the degree distribution; compare it with the one-module codelength $H(p)$ of the same graph, not across graphs.
- **Self-loops.** Decide how a self-loop affects the walk before computing the flows; the code on this page refuses them.

## Implementations

## History

Martin Rosvall and Carl Bergstrom proposed the map equation in 2008, using ideas from [minimum description length](/minimum-description-length/) and Huffman coding: a good partition is one that compresses the description of a random walk. Their first search merged modules greedily and refined the result with simulated annealing. In 2009, with Daniel Axelsson, they gave the expanded form of the map equation and the fast search of local moves and aggregation, in the style of the Louvain method, with fine-tuning and coarse-tuning. In 2011 they extended it to hierarchies of modules. The Infomap software implements these versions and the later ones for higher-order and overlapping flows.

## References
