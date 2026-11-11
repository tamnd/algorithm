---
tag: YCXNV8
kind: problem
slug: distributed-min-cut
name: Distributed minimum cut
aliases:
- distributed minimum cut problem
- distributed global min cut
area: distributed/distributed-graph-algorithms
level: research
summary: The nodes of a network find a smallest set of links whose removal cuts the network. In CONGEST the exact weighted problem takes Õ(√n + D) rounds, which matches the lower bound.
model: congest-model
complexity:
  vars: {n: the number of nodes, D: the hop diameter}
  time: {worst: "Õ(n^(1/2) + D)"}
prereqs: [global-min-cut-problem, congest-model, distributed-mst, convergecast]
see_also: [global-min-cut-problem, karger-min-cut, spanning-tree-packing, edge-connectivity, distributed-max-flow, distributed-connected-components, peleg-rubinovich-lower-bound, low-congestion-shortcuts]
sources:
  - paper: doi:10.1007/978-3-642-41527-2_1
    title: Mohsen Ghaffari and Fabian Kuhn, Distributed minimum cut approximation, DISC 2013, LNCS 8205
    locator: pages 1 to 15, the (2+ε) approximation in Õ((D + n^(1/2))/ε^5) rounds from Matula's method, and the lower bound for simple graphs; arXiv 1305.5520
  - paper: "Danupon Nanongkai and Hsin-Hao Su, Almost-tight distributed minimum cut algorithms, DISC 2014"
    locator: pages 439 to 453, the (1+ε) approximation in O((n^(1/2) log* n + D) ε^(-5) log^3 n) rounds and the exact algorithm in O((n^(1/2) log* n + D) λ^4 log^2 n) rounds; arXiv 1408.0557
  - paper: doi:10.1145/3313276.3316346
    title: Mohit Daga, Monika Henzinger, Danupon Nanongkai and Thatchaphol Saranurak, Distributed edge connectivity in sublinear time, STOC 2019
    locator: pages 343 to 354, the exact edge connectivity of simple graphs in Õ(n^(1-1/353) D^(1/353) + n^(1-1/706)) rounds; arXiv 1904.04341
  - paper: doi:10.1145/3406325.3451020
    title: Michal Dory, Yuval Efron, Sagnik Mukhopadhyay and Danupon Nanongkai, Distributed weighted min-cut in nearly-optimal time, STOC 2021
    locator: pages 1144 to 1153, the exact weighted min cut in Õ(n^(1/2) + D) rounds; arXiv 2004.09129
  - paper: doi:10.1137/11085178X
    title: Atish Das Sarma, Stephan Holzer, Liah Kor, Amos Korman, Danupon Nanongkai, Gopal Pandurangan, David Peleg and Roger Wattenhofer, Distributed verification and hardness of distributed approximation, SIAM Journal on Computing 41(5), 2012
    locator: pages 1235 to 1265, the lower bound Ω̃(n^(1/2) + D) for any approximation of the weighted minimum cut
  - paper: doi:10.1145/331605.331608
    title: David R. Karger, Minimum cuts in near-linear time, Journal of the ACM 47(1), 2000
    locator: pages 46 to 76, the tree packing in which some tree crosses the minimum cut at most twice, and the computation of the cuts that cross one tree edge
---

In distributed minimum cut, the network is the input graph. The nodes must find a [global minimum cut](/global-min-cut-problem/): a set of links of least total weight whose removal splits the network into two parts. At the end, each node knows its side of the cut, and all nodes know the cut value $\lambda$. In the [CONGEST model](/congest-model/), the problem now has a near-tight answer. Dory, Efron, Mukhopadhyay and Nanongkai (STOC 2021) find an exact weighted min cut in $\tilde{O}(\sqrt{n} + D)$ rounds, and Das Sarma et al. show that even an approximation needs $\tilde{\Omega}(\sqrt{n} + D)$ rounds. The route there passed through approximations: $(2 + \epsilon)$ by Ghaffari and Kuhn (DISC 2013), $(1 + \epsilon)$ by Nanongkai and Su (DISC 2014), and the first sublinear exact algorithm by Daga, Henzinger, Nanongkai and Saranurak (STOC 2019).

This page is about networks that cut themselves. It is not about [Karger's contraction algorithm](/karger-min-cut/), which contracts random edges in one memory. Contraction needs a global order of the edges, so it is a poor fit for message passing. The distributed algorithms use another idea of Karger: the min cut crosses some spanning tree of a [tree packing](/spanning-tree-packing/) only once or twice, and the cuts that cross a tree few times can be found by sums over the tree. For the $s$-$t$ version, see [distributed max flow](/distributed-max-flow/).

## In plain words

A network of computers wants to know its weakest point: the fewest cables (or the cables of least total weight) that, if they all fail, split the network in two.

One simple guess is the computer with the fewest cables, since cutting all its cables isolates it. But the weakest point can be in the middle of the network, between two large parts. To find it, the computers build a spanning tree and check each tree edge: if you remove it, the tree falls into two parts, and the computers count the cables between the two parts. If the weakest cut crosses the tree only once, one of these checks finds it. Good trees make this true, or true with two tree edges in place of one.

## Definition

**Input.** A connected network $G = (V, E)$ with $n$ nodes, hop diameter $D$, and a weight $w(e) \ge 1$ on each link, polynomial in $n$. Each node knows the weights of its own links. In the unweighted case, all weights are 1 and $\lambda$ is the edge connectivity.

**Output.** A set $S$ with $\emptyset \ne S \ne V$ that minimizes $w(\delta(S)) = \sum_{e \in \delta(S)} w(e)$, where $\delta(S)$ is the set of links with one end in $S$. Each node $v$ learns whether $v \in S$, and all nodes learn $\lambda = w(\delta(S))$. An $\alpha$-approximation outputs a set with $w(\delta(S)) \le \alpha \lambda$.

**Cost.** Synchronous rounds with one message of $O(\log n)$ bits per link and direction per round.

## Variants

- **The value only.** All nodes learn $\lambda$, or a value within a factor $\alpha$. The lower bounds hold for this weaker output too.
- **Unweighted simple graphs.** The input has no parallel links and no weights. For small $\lambda$ there are fast special algorithms, and the lower bound is weaker (see Bounds).
- **Small $\lambda$.** Exact algorithms whose rounds grow with $\lambda$, such as Nanongkai and Su's $O((\sqrt{n} \log^* n + D) \lambda^4 \log^2 n)$.
- **Vertex cuts and $s$-$t$ cuts.** Removing nodes in place of links, or separating two given nodes. The $s$-$t$ cut is the dual of [max flow](/distributed-max-flow/).
- **The [congested clique](/congested-clique-model/).** All pairs talk, and the graph is the input. The min cut there is faster, since MST and connectivity take $O(1)$ rounds.

## Examples

**One tree edge finds the cut.** Take two copies of $K_4$, on $\{0, 1, 2, 3\}$ and $\{4, 5, 6, 7\}$, joined by the links $3 4$ and $2 5$. All weights are 1, and $\lambda = 2$. The smallest degree is 3, so the degree guess is wrong here.

Take the spanning tree $T$ with the edges $0 1$, $0 2$, $0 3$, $3 4$, $4 5$, $4 6$, $4 7$, rooted at 0. For each node $v \ne 0$, let $v^\downarrow$ be the subtree of $v$. Removing the tree edge above $v$ gives the cut $\delta(v^\downarrow)$, whose value is

$$
w(\delta(v^\downarrow)) = \sum_{u \in v^\downarrow} \deg(u) - 2\, |E(v^\downarrow)|,
$$

where $E(v^\downarrow)$ is the set of links with both ends in $v^\downarrow$. A link has both ends in $v^\downarrow$ exactly when its lowest common ancestor in $T$ is in $v^\downarrow$. So if $\rho(u)$ is the number of links whose lowest common ancestor is $u$, then $|E(v^\downarrow)| = \sum_{u \in v^\downarrow} \rho(u)$. Here $\rho(0) = 7$ (the six links of the first $K_4$ and $2 5$), $\rho(3) = 1$ (the link $3 4$), $\rho(4) = 6$, and $\rho$ is 0 elsewhere.

| $v$ | $v^\downarrow$ | sum of degrees | links inside | cut value |
|---|---|---|---|---|
| 1 | $\{1\}$ | 3 | 0 | 3 |
| 2 | $\{2\}$ | 4 | 0 | 4 |
| 3 | $\{3, 4, 5, 6, 7\}$ | 18 | 7 | 4 |
| 4 | $\{4, 5, 6, 7\}$ | 14 | 6 | 2 |
| 5, 6, 7 | one node | 4, 3, 3 | 0 | 4, 3, 3 |

The smallest value is 2, at $v = 4$, and this is the min cut, because the min cut crosses $T$ only at the edge $3 4$. Both sums are [convergecasts](/convergecast/) up the tree, so given $\rho$, all values take $O(\text{depth of } T)$ rounds. With a tree that crosses the min cut twice, for example one that holds both $3 4$ and $2 5$, no single tree edge gives the min cut, and the algorithm must look at pairs of tree edges.

## Known algorithms

| result | approximation | rounds | graphs |
|---|---|---|---|
| Ghaffari and Kuhn, DISC 2013 | $O(\epsilon^{-1})$ | $O(D) + \tilde{O}(n^{1/2 + \epsilon})$ | weighted |
| Ghaffari and Kuhn, DISC 2013 | $2 + \epsilon$ | $\tilde{O}((D + \sqrt{n}) / \epsilon^5)$ | weighted |
| Nanongkai and Su, DISC 2014 | $1 + \epsilon$ | $O((\sqrt{n} \log^* n + D) \epsilon^{-5} \log^3 n)$ | weighted |
| Nanongkai and Su, DISC 2014 | exact | $O((\sqrt{n} \log^* n + D) \lambda^4 \log^2 n)$ | small $\lambda$ |
| Daga, Henzinger, Nanongkai and Saranurak, STOC 2019 | exact | $\tilde{O}(n^{1 - 1/353} D^{1/353} + n^{1 - 1/706})$ | simple, unweighted |
| Ghaffari, Nowicki and Thorup, SODA 2020 | exact | $\tilde{O}(n^{0.8} D^{0.2} + n^{0.9})$ | simple, unweighted |
| Dory, Efron, Mukhopadhyay and Nanongkai, STOC 2021 | exact | $\tilde{O}(\sqrt{n} + D)$ | weighted |

The bounds in the table are the ones in the abstracts of the papers.

**Matula's method, distributed (Ghaffari and Kuhn).** *Sketch.* Matula's sequential $(2 + \epsilon)$ method repeats one step: with $\delta$ the smallest weighted degree, find a sparse certificate that keeps all cuts of value below about $\delta$, and contract the links that are not in it. Each repetition makes the graph smaller by a constant factor, so $O(\log n)$ repetitions are enough. Ghaffari and Kuhn do the contraction with the fragments of a [distributed MST](/distributed-mst/), so each step costs $\tilde{O}(\sqrt{n} + D)$ rounds.

**One-respecting and two-respecting cuts (Nanongkai and Su, then Dory et al.).** *Sketch.* By Karger's tree packing, for a set of $O(\log n)$ spanning trees, the min cut crosses some tree at most twice with high probability. If it crosses once, the formula in the example finds it. The hard part in CONGEST is $\rho$, since a link must find the lowest common ancestor of its ends in a tree that can be deep. Nanongkai and Su use the fragment decomposition of the MST algorithms (fragments of about $\sqrt{n}$ nodes, joined by a tree of fragments of depth $O(\sqrt{n} + D)$) to compute these sums in $\tilde{O}(\sqrt{n} + D)$ rounds. After sampling the edges with Karger's method, so that $\lambda$ becomes $O(\epsilon^{-2} \log n)$, this gives the $(1 + \epsilon)$ approximation. Dory et al. handle the cuts that cross a tree twice with two structural lemmas that let each node look at few candidate pairs, which gives the exact $\tilde{O}(\sqrt{n} + D)$ bound.

**Expander decomposition (Daga et al.).** *Sketch.* For simple graphs, split the graph into parts with high conductance, with few links between the parts. In a part of high conductance, the nontrivial small cuts are few, so contracting the parts keeps all min cuts that are not single nodes. The contracted graph is small, and its cut is found with certificates. This gave the first exact sublinear bound.

## Bounds

- **Lower bound for weighted graphs.** Any $\alpha$-approximation of the min cut, for any $\alpha \ge 1$, needs $\tilde{\Omega}(\sqrt{n} + D)$ rounds (Das Sarma et al., SIAM J. Comput. 2012). The proof reduces from set disjointness on the graphs of the [Peleg-Rubinovich bound](/peleg-rubinovich-lower-bound/). The links of the subgraph $H$ to test get a large weight $W$ and the other links get weight 1. If $H$ is connected, each cut crosses a link of $H$, so $\lambda \ge W$. If not, the cut around a component of $H$ crosses only links of weight 1, so $\lambda < n^2$. With $W$ larger than $\alpha n^2$, an $\alpha$-approximation tells the two cases apart. So the hard part is the subgraph connectivity of [distributed connected components](/distributed-connected-components/).
- **Lower bound for simple graphs.** Ghaffari and Kuhn extend the bound: on unweighted simple graphs with suitable diameter, an $\alpha$-approximation needs $\tilde{\Omega}(D + \sqrt{n / (\alpha \lambda)})$ rounds. For large $\lambda$, the bound is weaker.
- **Upper bound.** $\tilde{O}(\sqrt{n} + D)$, exact and weighted (Dory et al., STOC 2021). So the problem is solved up to polylogarithmic factors in the worst case.
- **Better graphs.** On planar networks and others with good [low-congestion shortcuts](/low-congestion-shortcuts/), the tree sums are faster. A PODC 2022 paper on universally optimal exact min cut runs in $\tilde{O}(\sqrt{n} + D)$ rounds on all graphs and faster on graphs with good shortcuts.

## Reductions

- **From subgraph connectivity.** With a large weight on the links of a spanning subgraph $H$ and weight 1 elsewhere, $\lambda$ is small if and only if $H$ is not connected. So a min cut algorithm decides [subgraph connectivity](/distributed-connected-components/), and the lower bound carries over.
- **To tree sums.** Given a good tree, each one-respecting cut is a pair of sums over subtrees. The rest of the work is to find good trees and to deal with two tree edges.
- **To MST.** Both the tree packing (by repeated MST with weights that grow with use) and the contraction in Matula's method run on top of [distributed MST](/distributed-mst/).

## Applications

- **Network reliability.** The value $\lambda$ is the number of link failures that the network can survive and stay connected. A network can test itself, for example after a change in its links.
- **Finding bottlenecks.** The min cut shows where to add links.
- **A step in other algorithms.** Cuts give connectivity certificates, and the tree packing gives a set of edge-disjoint spanning trees, which are used for fault-tolerant broadcast.

## References
