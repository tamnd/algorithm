---
tag: 3QCX94
kind: theorem
slug: peleg-rubinovich-lower-bound
name: Peleg-Rubinovich lower bound for distributed MST
aliases:
- Omega(sqrt(n)+D) MST lower bound
- Peleg-Rubinovich theorem
area: distributed/distributed-graph-algorithms
level: research
summary: Any distributed MST algorithm needs Omega(D + sqrt(n)/B) rounds in CONGEST with B-bit messages on some graphs of diameter D = Omega(log n). Later work covers approximation and randomization.
prereqs: [distributed-mst, congest-model, communication-complexity, disjointness-problem, round-complexity]
see_also: [distributed-mst, gallager-humblet-spira, low-congestion-shortcuts, diameter-lower-bound-distributed, randomized-communication-complexity, distributed-shortest-paths, distributed-min-cut, distributed-connected-components]
sources:
  - paper: doi:10.1137/S0097539700369740
    title: David Peleg and Vitaly Rubinovich, A near-tight lower bound on the time complexity of distributed minimum-weight spanning tree construction, SIAM Journal on Computing 30(5), 2000
    locator: pages 1427 to 1442 (the graph family, the mailing problem and the main theorem); the conference version is in FOCS 1999, pages 253 to 261
  - paper: "Michael Elkin, An unconditional lower bound on the time-approximation trade-off for the distributed minimum spanning tree problem, SIAM Journal on Computing 36(2), 2006"
    locator: pages 433 to 456, the lower bound for α-approximate MST
  - paper: doi:10.1137/11085178X
    title: Atish Das Sarma, Stephan Holzer, Liah Kor, Amos Korman, Danupon Nanongkai, Gopal Pandurangan, David Peleg and Roger Wattenhofer, Distributed verification and hardness of distributed approximation, SIAM Journal on Computing 41(5), 2012
    locator: pages 1235 to 1265, Section 3.1 (the graph G(Γ, d, p) and Lemma 3.2), Theorem 3.1 (the Simulation Theorem) and Theorem 5.1; the conference version is STOC 2011, doi:10.1145/1993636.1993686
  - paper: "Gopal Pandurangan, Peter Robinson and Michele Scquizzato, The distributed minimum spanning tree problem, Bulletin of the EATCS 125, 2018"
    locator: Section 3 (the lower bounds and their history)
---

## Statement

The model is [CONGEST](/congest-model/) with messages of $B$ bits: the network is a graph with $n$ nodes, the nodes have unique identifiers, and in each synchronous round each node sends at most one message of $B$ bits on each incident edge. An algorithm solves [distributed MST](/distributed-mst/) if at the end each node knows which of its incident edges are in the minimum spanning tree.

**Theorem (Peleg and Rubinovich, 2000).** For every large $n$ there is a family of weighted graphs with $\Theta(n)$ nodes and hop diameter $D = \Theta(\log n)$ such that every deterministic distributed MST algorithm with $B$-bit messages needs $\Omega(\sqrt{n}/B)$ rounds on some graph of the family. With a path added to make the diameter larger, the bound is $\Omega(D + \sqrt{n}/B)$ for each $D = \Omega(\log n)$. For $B = O(\log n)$ this is

$$\Omega\!\left(D + \frac{\sqrt{n}}{\log n}\right) \text{ rounds.}$$

**Later forms.** Two later results extend the bound.

- **Elkin (SIAM J. Comput. 2006).** For $\alpha$-approximate MST the bound is about $\Omega(\sqrt{n/(\alpha B \log n)})$ rounds, so it falls slowly as $\alpha$ grows.
- **Das Sarma et al. (SIAM J. Comput. 2012).** For each approximation ratio, also for randomized Monte Carlo algorithms with constant error, the bound is $\Omega(D + \sqrt{n/(B \log n)})$ rounds. The same bound holds for many verification problems, such as "is the marked subgraph $H$ connected and spanning".

## In plain words

Some networks have a small diameter but are still slow for MST. Picture $\sqrt{n}$ long parallel roads, each with $\sqrt{n}$ towns, between two cities $s$ and $t$. A small tree of fast links joins the roads, so any two towns are close in hops.

The weights are set so that the right choice of tree edges at $t$ depends on $\sqrt{n}$ bits that only $s$ knows. A bit can travel to $t$ along a road, which takes $\sqrt{n}$ rounds. Or it can use the fast links, but there are few of them, and each carries only $B$ bits in each round. So either the run is long, or the fast links carry about $\sqrt{n}$ bits through a narrow cut. Both cost about $\sqrt{n}/B$ rounds or more, up to log factors.

## Proof

The original proof uses a mailing problem and counts the states of the nodes. The later proof of Das Sarma et al. uses a reduction from two-party [communication complexity](/communication-complexity/). Both are given here as sketches. **Sketch: the graph, the constants and the simulation are given without all details; see the papers for the full proofs.**

**The mailing argument of Peleg and Rubinovich (sketch).**

*The graph.* Take $m = \Theta(\sqrt{n})$ paths $P_1, \ldots, P_m$, each with $\ell = \Theta(\sqrt{n})$ nodes, and a further path, the *highway*, with $\ell$ nodes. Spokes join the $j$-th node of each path to the $j$-th node of the highway. A balanced tree on top of the highway makes the diameter $O(\log n)$. The node $s$ is at one end of the highway and $t$ is at the other end. An $s$-edge joins $s$ to the first node of each path, and a $t$-edge joins $t$ to the last node of each path.

*The weights.* Path edges and highway and tree edges have weight 0. Spokes have weight 4, $t$-edges have weight 2, and the $s$-edge of $P_i$ has weight $1$ or $3$, chosen by an input bit $x_i$ that only $s$ knows. Each path is joined to the rest by its lightest leaving edge. So the $t$-edge of $P_i$ is in the MST if and only if the $s$-edge of $P_i$ has weight 3. To output its MST edges, $t$ must learn all $m$ bits $x_1, \ldots, x_m$. This is the *mailing problem*: send $m$ bits from $s$ to $t$.

*The counting.* A bit from $s$ that travels only along paths needs about $\ell$ rounds to reach $t$. Consider an algorithm with $r$ rounds, $r$ much smaller than $\ell$. Then the state of $t$ after $r$ rounds is a function of the messages on the few highway and tree edges that separate the side of $s$ from the side of $t$. Each such edge carries, in each round, either nothing or one of $2^B$ messages, so it has at most $(2^B + 1)^r$ possible histories. With $k$ such edges, $t$ ends in at most $(2^B + 1)^{kr}$ states. The $2^m$ inputs need $2^m$ different outputs at $t$, so $(2^B + 1)^{kr} \ge 2^m$ and $r \ge m / (k (B + 1))$. The construction of the paper keeps the effective cut small as the rounds go on, and with $m = \Theta(\sqrt{n})$ this gives $r = \Omega(\sqrt{n}/B)$. Together with the trivial bound $\Omega(D)$, this gives the theorem.

**The simulation argument of Das Sarma et al. (sketch).**

*The graph $G(\Gamma, d, p)$.* Take $\Gamma$ paths, each with $d^p$ nodes $v^\ell_0, \ldots, v^\ell_{d^p - 1}$, and a tree of depth $p$ in which each inner node has $d$ children. The $j$-th leaf $u^p_j$ of the tree has a spoke to the $j$-th node $v^\ell_j$ of each path. Set $s = u^p_0$ and $r = u^p_{d^p - 1}$. By their Lemma 3.2, the graph has $n = \Theta(\Gamma d^p)$ nodes and diameter $2p + 2$.

*The Simulation Theorem (their Theorem 3.1).* Let $f(x, y)$ be a function of two $\Gamma$-bit strings, and give $x$ to $s$ and $y$ to $r$. If a distributed algorithm computes $f$ on $G(\Gamma, d, p)$ in $R < (d^p - 1)/2$ rounds with error $\epsilon$, then

$$R^{cc\text{-}pub}_\epsilon(f) \le 2dpB \cdot R,$$

where $R^{cc\text{-}pub}_\epsilon(f)$ is the public-coin [randomized communication complexity](/randomized-communication-complexity/) of $f$. Alice simulates, in round $i$, all the nodes in a left region that loses one column of path nodes in each round. Bob does the same on the right. A path node of Alice's region in round $i$ only hears from nodes that Alice simulated in round $i - 1$. Only the tree edges cross between the two regions, and at most $d$ of them cross at each of the $p$ levels. So in each round the players exchange at most $2dp$ messages of $B$ bits. Since $R < (d^p - 1)/2$, the regions never become empty, and at the end Alice knows the state of $s$ and Bob the state of $r$.

*The reduction.* Mark all path and tree edges as in $H$. Mark the spoke from $s$ to $P_i$ as in $H$ if $x_i = 0$, and the spoke from $r$ to $P_i$ as in $H$ if $y_i = 0$. Then $H$ is a connected spanning subgraph if and only if $x$ and $y$ are disjoint as sets, so an algorithm that checks $H$ solves [set disjointness](/disjointness-problem/), which needs $\Omega(\Gamma)$ bits of randomized communication. Give the edges of $H$ weight 1 and the other edges a weight $W$ that is much larger than $\alpha n$. An $\alpha$-approximate MST then has weight less than $W$ if and only if $H$ is connected and spanning. So $R \ge \Omega(\Gamma/(dpB))$ unless $R \ge (d^p - 1)/2$.

*The numbers.* Take $d = 2$ and choose $\Gamma \approx d^p \cdot dpB$, so that both terms balance. Then $n = \Theta(\Gamma d^p)$ gives $d^p = \Theta(\sqrt{n/(pB)})$ and $p = \Theta(\log n)$. So $R = \Omega(\sqrt{n/(B \log n)})$ on a graph of diameter $O(\log n)$. A path attached to the graph adds $\Omega(D)$.

Code cannot prove a lower bound. The [distributed MST](/distributed-mst/) page has a CONGEST simulator that counts rounds and bits, which shows the costs of a real algorithm against this bound.

## Consequences

- **Near-optimal algorithms.** Kutten and Peleg's $O(D + \sqrt{n} \log^* n)$ algorithm and the $\tilde{O}(D + \sqrt{n})$ algorithms of 2017 and 2018 are optimal up to polylog factors. See [distributed MST](/distributed-mst/).
- **Approximation does not help.** By Das Sarma et al., any approximation ratio needs the same $\tilde{\Omega}(D + \sqrt{n})$ rounds. This is unlike sequential computing, where approximation often helps.
- **Many problems inherit the bound.** The same graphs and reductions give $\tilde{\Omega}(D + \sqrt{n})$ for [connectivity of a subgraph](/distributed-connected-components/), [min cut](/distributed-min-cut/), [shortest paths](/distributed-shortest-paths/) and their approximations, [max flow](/distributed-max-flow/), and many verification problems.
- **Global problems are hard even with small diameter.** A small $D$ alone does not make a problem fast in CONGEST. The structure of the graph matters, which is the motivation for [low-congestion shortcuts](/low-congestion-shortcuts/).

## Tightness

- **Upper bounds match.** Algorithms with $\tilde{O}(D + \sqrt{n})$ rounds exist, so the bound is tight up to polylog factors for $D = \Omega(\log n)$.
- **The $\log$ factors.** The exact power of $\log n$ is not settled. The best upper bounds have a factor of $\log n$ or $\log^* n$, and the lower bounds lose a factor of about $\sqrt{\log n}$ to $\log n$.
- **Small diameter is different.** For $D = 1$ (the [congested clique](/congested-clique-model/)) MST takes $O(1)$ rounds with randomization, and for $D = 2$ it takes $O(\log n)$ rounds. For $D = 3$ and $D = 4$ the lower bounds are $\tilde{\Omega}(n^{1/4})$ and $\tilde{\Omega}(n^{1/3})$ (Lotker, Patt-Shamir and Peleg, 2006; Das Sarma et al., Theorem 5.1). In general, Theorem 5.1 gives $\Omega((n/(pB))^{1/2 - 1/(2(2p+1))})$ on graphs of diameter $2p + 2$.
- **Message size.** With no limit on $B$ (the [LOCAL model](/local-model/)), MST takes $O(D)$ rounds, so the bound depends on the bandwidth.
- **Special graphs.** The lower bound graphs are not planar. On planar graphs, MST takes $\tilde{O}(D)$ rounds with [low-congestion shortcuts](/low-congestion-shortcuts/).

## History

Garay, Kutten and Peleg gave the first sublinear MST algorithm in 1993, and Kutten and Peleg reached $O(D + \sqrt{n} \log^* n)$ in 1995. Peleg and Rubinovich showed at FOCS 1999 that this is near optimal. Their bound was for deterministic exact algorithms. Lotker, Patt-Shamir and Peleg extended the method to small diameters, and Elkin to approximation in 2004 (journal version 2006). Das Sarma et al. (STOC 2011) replaced the counting by a simulation of a two-party protocol. This made the bound hold for Monte Carlo algorithms and for any approximation ratio, and it applied to a long list of problems.

## References
