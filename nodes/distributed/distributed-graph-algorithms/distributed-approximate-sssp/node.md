---
tag: 2AFXT0
kind: problem
slug: distributed-approximate-sssp
name: Distributed approximate shortest paths
aliases:
- approximate distributed SSSP
- (1+eps)-approximate distributed shortest paths
area: distributed/distributed-graph-algorithms
level: research
summary: Each node learns its distance to a source within a factor 1 + ε. In CONGEST this takes Õ(√n + D) rounds for constant ε, which matches the lower bound up to polylog factors.
model: congest-model
complexity:
  vars: {n: the number of nodes, D: the hop diameter, ε: the relative error}
  time: {worst: "Õ((n^(1/2) + D) ε^(-O(1)))"}
prereqs: [distributed-shortest-paths, distributed-bellman-ford, hopset, congest-model, breadth-first-search-distributed]
see_also: [distributed-shortest-paths, hopset, distributed-bellman-ford, peleg-rubinovich-lower-bound, low-congestion-shortcuts, distributed-apsp, electrical-flow, congested-clique-model]
sources:
  - paper: "Danupon Nanongkai, Distributed approximation algorithms for weighted shortest paths, STOC 2014"
    locator: the (1+o(1)) approximation in Õ(n^(1/2) D^(1/4) + D) rounds, with light-weight hopsets and the rounding of weights
  - paper: "Monika Henzinger, Sebastian Krinninger and Danupon Nanongkai, A deterministic almost-tight distributed algorithm for approximating single-source shortest paths, STOC 2016"
    locator: the abstract and the main theorem, (1+o(1)) approximation in n^(1/2+o(1)) + D^(1+o(1)) rounds, deterministic, with a deterministic hopset on a skeleton graph; arXiv 1504.07056
  - paper: doi:10.4230/LIPIcs.DISC.2017.7
    title: Ruben Becker, Andreas Karrenbauer, Sebastian Krinninger and Christoph Lenzen, Near-optimal approximate shortest paths and transshipment in distributed and streaming models, DISC 2017
    locator: pages 7:1 to 7:16, the abstract, (1+ε)-approximate SSSP in Õ((n^(1/2) + D) ε^(-O(1))) rounds of broadcast CONGEST and Õ(ε^(-O(1))) rounds of the broadcast congested clique
  - paper: doi:10.1145/3519935.3520074
    title: Václav Rozhoň, Christoph Grunau, Bernhard Haeupler, Goran Zuzic and Jason Li, Undirected (1+ε)-shortest paths via minor-aggregates, STOC 2022
    locator: pages 478 to 487, the deterministic reduction to Õ(1) minor aggregations
  - paper: doi:10.1137/11085178X
    title: Atish Das Sarma, Stephan Holzer, Liah Kor, Amos Korman, Danupon Nanongkai, Gopal Pandurangan, David Peleg and Roger Wattenhofer, Distributed verification and hardness of distributed approximation, SIAM Journal on Computing 41(5), 2012
    locator: pages 1235 to 1265, the lower bound for shortest s-t paths of any polynomial ratio
  - paper: "Nairen Cao, Jeremy T. Fineman and Katina Russell, Brief announcement: an improved distributed approximate single source shortest paths algorithm, PODC 2021"
    locator: directed graphs, Õ((n^(1/2) + D + n^(2/5+o(1)) D^(2/5)) log W / ε^2) rounds; doi:10.1145/3465084.3467945
---

In distributed approximate single-source shortest paths, each node $v$ of a weighted network learns a value $\widetilde{d}(v)$ with $d(s, v) \le \widetilde{d}(v) \le (1 + \epsilon)\, d(s, v)$, where $s$ is the source. This is the approximate form of [distributed SSSP](/distributed-shortest-paths/). The exact problem has a gap between its upper and lower bounds, but the approximate one is solved: $(1 + \epsilon)$-approximate SSSP takes $\tilde{O}((\sqrt{n} + D)\, \epsilon^{-O(1)})$ rounds in [CONGEST](/congest-model/) (Becker, Karrenbauer, Krinninger and Lenzen, DISC 2017), and every algorithm with a polynomial ratio needs $\tilde{\Omega}(\sqrt{n} + D)$ rounds. The main tool of the first near-optimal algorithms is the [hopset](/hopset/): a few extra edges that make every distance nearly correct over a path of few hops.

## In plain words

Each computer in a network must learn about how far it is from a source computer, with a small error, for example at most 1% too much. The exact answer can need a route of almost $n$ cables, and news moves one cable in each round, so the simple method is slow.

The trick is to add a few long "jump" links between chosen computers, with a length that is never shorter than the real route. With the jumps, each route can be done in a few steps, and the error stays small. The jumps are not real cables, so their messages travel over a shared tree. The total time is about $\sqrt{n}$ plus the diameter, and no method can be much faster.

## Definition

**Input.** As for [distributed SSSP](/distributed-shortest-paths/): a connected undirected graph $G = (V, E)$ with $n$ nodes, weights $w(e) \in \{1, \ldots, W\}$ with $W = n^{O(1)}$, and a source $s$. Each node knows the weights of its own edges. A parameter $\epsilon > 0$ is known to all nodes.

**Output.** Each node $v$ outputs $\widetilde{d}(v)$ with

$$d(s, v) \le \widetilde{d}(v) \le (1 + \epsilon)\, d(s, v).$$

Most algorithms also give a tree whose path from $s$ to $v$ has weight at most $(1 + \epsilon)\, d(s, v)$.

**Hop-bounded distances.** Let $d_h(u, v)$ be the least weight of a path from $u$ to $v$ with at most $h$ edges. Then $h$ rounds of [Bellman-Ford](/distributed-bellman-ford/) compute $d_h(s, \cdot)$ exactly. The whole problem is that $d_h$ can be much larger than $d$ for small $h$.

**Hopsets.** A set $F$ of extra weighted pairs is an $(h, \epsilon)$-[hopset](/hopset/) of $G$ if, in the graph $G \cup F$:

1. no distance is less than in $G$, which holds when the weight of each pair $\{u, v\} \in F$ is at least $d(u, v)$, and
2. for all $u, v$: $d^{G \cup F}_h(u, v) \le (1 + \epsilon)\, d(u, v)$.

With an $(h, \epsilon)$-hopset, $h$ rounds of Bellman-Ford on $G \cup F$ give a $(1 + \epsilon)$-approximation. The difference from a *spanner* is that a spanner removes edges and keeps distances close, while a hopset adds edges to cut the number of hops.

## Variants

- **Ratio.** A ratio of $1 + \epsilon$ is the usual goal. A larger ratio, such as $O(\log n)$ or a constant $2k - 1$, comes from tree or spanner methods and can be simpler. The lower bound holds for every polynomial ratio, so a larger ratio does not save more than polylog factors in rounds.
- **Directed graphs.** Cao, Fineman and Russell (PODC 2021) give a $(1 + \epsilon)$-approximation for directed graphs in $\tilde{O}((\sqrt{n} + D + n^{2/5 + o(1)} D^{2/5}) \log W / \epsilon^2)$ rounds. With the reduction of Rozhoň et al. (STOC 2023), this also gives exact distances. See [distributed SSSP](/distributed-shortest-paths/).
- **Special networks.** On planar graphs and other graphs with good [low-congestion shortcuts](/low-congestion-shortcuts/), the $\sqrt{n}$ term can go away. Rozhoň, Grunau, Haeupler, Zuzic and Li (STOC 2022) reduce $(1 + \epsilon)$-SSSP to $\tilde{O}(1)$ *minor aggregations*, which are aggregations over the parts of a partition, as with shortcuts.
- **Other models.** In the broadcast [congested clique](/congested-clique-model/), $(1 + \epsilon)$-SSSP takes $\tilde{O}(\epsilon^{-O(1)})$ rounds (Becker et al.). In the [LOCAL model](/local-model/) the exact problem takes $O(D)$ rounds.
- **Many sources.** With $k$ sources, the same frame with pipelining gives approximate $k$-source distances. For all pairs, see [distributed APSP](/distributed-apsp/).

## Examples

**A hopset for a path.** Let $G$ be a path $v_0, v_1, \ldots, v_{n-1}$ with $n = 2^k$ and weight 1 on each edge. Then $d(v_i, v_j) = |i - j|$, and Bellman-Ford needs $n - 1$ rounds from $v_0$. Add the pair $\{v_i, v_{i + 2^t}\}$ with weight $2^t$ for each $t \ge 1$ and each $i$ that is a multiple of $2^t$ with $i + 2^t \le n - 1$. These are the dyadic intervals, and there are fewer than $n$ of them. No pair is shorter than the path, and the route from $v_i$ to $v_j$ that climbs the dyadic intervals and comes down again uses at most $2k$ hops. So this is an exact $(2 \log_2 n, 0)$-hopset, and Bellman-Ford on $G \cup F$ needs only $2 \log_2 n$ rounds.

For $n = 16$: from $v_0$ to $v_{13}$ the route is $v_0 \to v_8$ (weight 8), $v_8 \to v_{12}$ (weight 4), $v_{12} \to v_{13}$ (weight 1). That is 3 hops for a path of 13 edges, with no error.

In a network, the pair $\{v_0, v_8\}$ is not a link. A message from $v_0$ to $v_8$ must travel over real links. This is why the algorithms build the hopset only on a small *skeleton* of about $\sqrt{n}$ nodes, and send the messages of the skeleton over a BFS tree.

## Known algorithms

**The skeleton and hopset plan.** This is the plan of Nanongkai (2014) and Henzinger, Krinninger and Nanongkai (2016). The text below is a sketch, with the costs of the steps as those papers state them.

1. *Skeleton.* Sample each node into a set $S$ with probability about $1/\sqrt{n}$, and add $s$. Then $|S| = \tilde{O}(\sqrt{n})$, and with high probability each path of $h = \tilde{O}(\sqrt{n})$ consecutive edges on any shortest path has a node of $S$. (Henzinger et al. replace the sampling by a deterministic choice.)
2. *Short distances.* Each node $x \in S$ learns approximate $h$-hop distances to the nodes of $S$ near it. Exact $h$-hop Bellman-Ford from all of $S$ at once would cost too many rounds. Instead the weights are rounded to multiples of a scale, so that each scale becomes a BFS of depth $O(h/\epsilon)$. Many BFS runs can share the edges with random start delays. This gives $(1 + \epsilon)$-approximate $h$-hop distances from all of $S$ in $\tilde{O}(|S| + h/\epsilon + D)$ rounds.
3. *Skeleton graph.* The skeleton graph $G_S$ has the nodes $S$ and an edge $\{x, y\}$ with weight $\widetilde{d}_h(x, y)$. By the lemma below, its distances are $(1 + \epsilon)$-close to those of $G$.
4. *Hopset on the skeleton.* Build an $(\beta, \epsilon)$-hopset $F$ of $G_S$, with $\beta = n^{o(1)}$ in the deterministic construction. Then $\beta$ rounds of Bellman-Ford on $G_S \cup F$ give the distances from $s$ in $G_S$.
5. *Global Bellman-Ford.* Each Bellman-Ford round on $G_S \cup F$ is done by sending the estimate of each skeleton node to all nodes over a BFS tree. With pipelining, $|S|$ values reach all nodes in $O(|S| + D)$ rounds. So step 4 costs $\beta \cdot \tilde{O}(\sqrt{n} + D)$ rounds.
6. *Back to all nodes.* Each skeleton node $x$ starts with its value $\widetilde{d}(x)$, and one $h$-hop (approximate) Bellman-Ford with these start values gives each node $v$ the value $\min_{x \in S} (\widetilde{d}(x) + \widetilde{d}_h(x, v))$.

**Lemma (the skeleton is enough).** Assume that each path of $h$ consecutive edges on some shortest path from $s$ to $v$ has a node of $S$. Then

$$d(s, v) = \min_{x \in S} \big( d_{G_S}(s, x) + d_h(x, v) \big),$$

where $G_S$ has the exact weights $d_h(x, y)$.

*Proof.* Each term on the right is the weight of a walk in $G$ from $s$ to $v$, so it is at least $d(s, v)$. For the other side, take the shortest path $P$ from $s$ to $v$, and let $s = x_0, x_1, \ldots, x_k$ be the nodes of $S$ on $P$, in order. By the assumption, consecutive nodes $x_{i-1}, x_i$ are at most $h$ edges apart on $P$, and $x_k$ is at most $h$ edges from $v$. A sub-path of a shortest path is a shortest path, so $d_h(x_{i-1}, x_i) = d(x_{i-1}, x_i)$, and the sum over $i$ is the weight of $P$ up to $x_k$. So $d_{G_S}(s, x_k) \le d(s, x_k)$ and $d_h(x_k, v) = d(x_k, v)$, and the term for $x = x_k$ is at most $d(s, v)$. $\square$

With $(1 + \epsilon)$-approximate $h$-hop distances in steps 2 and 6, and a $(1 + \epsilon)$-approximation in step 4, the errors multiply to $(1 + \epsilon)^3 \le 1 + 7\epsilon$ for $\epsilon \le 1$. Run with $\epsilon/7$ to get $1 + \epsilon$.

**The results.**

| algorithm | year | ratio | rounds | method |
|---|---|---|---|---|
| Nanongkai, STOC 2014 | 2014 | $1 + o(1)$ | $\tilde{O}(\sqrt{n} D^{1/4} + D)$ | randomized; light-weight hopsets |
| Henzinger, Krinninger and Nanongkai, STOC 2016 | 2016 | $1 + o(1)$ | $n^{1/2 + o(1)} + D^{1 + o(1)}$ | deterministic hopset on the skeleton |
| Becker, Karrenbauer, Krinninger and Lenzen, DISC 2017 | 2017 | $1 + \epsilon$ | $\tilde{O}((\sqrt{n} + D)\, \epsilon^{-O(1)})$ | gradient descent for transshipment on a spanner; no hopset |
| Rozhoň, Grunau, Haeupler, Zuzic and Li, STOC 2022 | 2022 | $1 + \epsilon$ | $\tilde{O}(\sqrt{n} + D)$ for constant $\epsilon$ | deterministic; minor aggregations |

The algorithm of Becker et al. solves the *shortest transshipment* problem, which is min cost flow without capacities, with a gradient descent. Each step needs only a rough $O(\log n)$-approximation, which a sparse spanner gives. The method needs no hopset, and it also works in the broadcast congested clique and in multipass streaming.

## Bounds

**Lower bound.** Das Sarma et al. (SIAM J. Comput. 2012), after Elkin (STOC 2004), proved that each algorithm that approximates the $s$-$t$ distance within any polynomial ratio needs $\Omega(\sqrt{n}/\log n + D)$ rounds on some graphs, also when it is randomized. The graphs are those of the [Peleg-Rubinovich lower bound](/peleg-rubinovich-lower-bound/), and the reduction is from two-party [set disjointness](/disjointness-problem/).

**Tightness.** The algorithms of 2017 and 2022 match this up to polylog factors for constant $\epsilon$. So approximate SSSP has round complexity $\tilde{\Theta}(\sqrt{n} + D)$, the same as [MST](/distributed-mst/). For exact SSSP, the best known bound is $\tilde{O}(n^{2/5 + o(1)} D^{2/5} + \sqrt{n} + D)$.

## Reductions

- **SSSP from transshipment.** Becker et al. solve SSSP as a transshipment problem in which $s$ sends one unit to each other node. A near-optimal dual of this problem is a vector of potentials, which approximates the distances.
- **Lower bound from verification.** Give weight 1 to the edges of a subgraph $H$ and a much larger weight to the other edges. A good approximation of $d(s, t)$ then shows whether $s$ and $t$ are joined in $H$. This carries the lower bound for the verification of connectivity over to approximate SSSP.
- **Exact from approximate.** For directed graphs, Rozhoň et al. (STOC 2023) turn strongly approximate distances into exact distances at almost no extra cost.

## Applications

- **Routing.** Approximate distances give routing tables with paths at most $1 + \epsilon$ times too long.
- **Diameter and radius.** One approximate SSSP from any node gives a 2-approximation of the weighted [diameter](/distributed-diameter/) up to the factor $1 + \epsilon$. Henzinger et al. state a $(2 + o(1))$-approximation of the weighted diameter in the same time.
- **Flows and cuts.** Approximate shortest paths and transshipment are steps in distributed algorithms for [max flow](/distributed-max-flow/) and for [min cut](/distributed-min-cut/), and in the construction of low-stretch trees.

## References
