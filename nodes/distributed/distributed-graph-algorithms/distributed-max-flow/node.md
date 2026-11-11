---
tag: 6669RS
kind: problem
slug: distributed-max-flow
name: Distributed maximum flow
aliases:
- distributed maxflow
- distributed max-flow approximation
area: distributed/distributed-graph-algorithms
level: research
summary: The nodes of a network compute a maximum s-t flow over its own links. Push-relabel needs O(n²) rounds; a (1+o(1)) approximation takes (√n + D) n^o(1) rounds on undirected graphs.
model: congest-model
complexity:
  vars: {n: the number of nodes, D: the hop diameter}
  time: {worst: O(n^2)}
  messages: {worst: O(n^3)}
prereqs: [max-flow-problem, push-relabel, congest-model, max-flow-min-cut-theorem]
see_also: [max-flow-problem, push-relabel, parallel-push-relabel, almost-linear-max-flow, electrical-flow, distributed-min-cut, peleg-rubinovich-lower-bound, low-congestion-shortcuts]
sources:
  - paper: doi:10.1145/48014.61051
    title: Andrew V. Goldberg and Robert E. Tarjan, A new approach to the maximum-flow problem, Journal of the ACM 35(4), 1988
    locator: pages 921 to 940, the synchronous distributed version of push-relabel, with O(n^2) pulses and O(n^3) messages
  - paper: doi:10.1137/17M113277X
    title: Mohsen Ghaffari, Andreas Karrenbauer, Fabian Kuhn, Christoph Lenzen and Boaz Patt-Shamir, Near-optimal distributed maximum flow, SIAM Journal on Computing 47(6), 2018
    locator: pages 2078 to 2117, the (1+o(1)) approximation in (D + n^(1/2)) n^(o(1)) rounds for undirected graphs; the conference version is PODC 2015, pages 81 to 90
  - paper: doi:10.1137/11085178X
    title: Atish Das Sarma, Stephan Holzer, Liah Kor, Amos Korman, Danupon Nanongkai, Gopal Pandurangan, David Peleg and Roger Wattenhofer, Distributed verification and hardness of distributed approximation, SIAM Journal on Computing 41(5), 2012
    locator: pages 1235 to 1265, the lower bound Ω̃(n^(1/2) + D) for the approximation of the minimum s-t cut
  - paper: "Sebastian Forster, Gramoz Goranci, Yang P. Liu, Richard Peng, Xiaorui Sun and Mingquan Ye, Minor sparsifiers and the distributed Laplacian paradigm, FOCS 2021"
    locator: pages 989 to 999, a Laplacian solver in n^(o(1)) (n^(1/2) + D) rounds and exact maximum flow in CONGEST through interior point methods; arXiv 2012.15675
  - paper: "Jonah Sherman, Nearly maximum flows in nearly linear time, FOCS 2013"
    locator: the congestion approximator and the gradient method that the distributed algorithm of Ghaffari et al. runs
---

In distributed maximum flow, the network is the flow graph. Each node is a processor that knows the capacities of its own links, and the nodes must find a [maximum flow](/max-flow-problem/) from a source $s$ to a sink $t$ by sending messages over these links. At the end, each node knows the flow on each of its links. In the [CONGEST model](/congest-model/), the classic answer is [push-relabel](/push-relabel/), which is local by nature: each step reads only one node and its neighbours. Its synchronous form needs $O(n^2)$ rounds. The best approximation is much faster. Ghaffari, Karrenbauer, Kuhn, Lenzen and Patt-Shamir (PODC 2015) find a $(1 + o(1))$-approximate flow in $(\sqrt{n} + D) \cdot n^{o(1)}$ rounds on undirected graphs. This nearly matches the $\tilde{\Omega}(\sqrt{n} + D)$ lower bound, which comes from [the Peleg-Rubinovich technique](/peleg-rubinovich-lower-bound/).

This page is about networks that compute flows over their own links. The sequential problem is on [maximum flow](/max-flow-problem/), the shared-memory version is [parallel push-relabel](/parallel-push-relabel/), and the min cut side of the same networks is on [distributed min cut](/distributed-min-cut/).

## In plain words

Water must go from one computer, the source, to another, the sink, through pipes that are the network cables. Each pipe can carry only so much. The computers must agree how much water goes through each pipe, so that the sink gets as much as possible.

Push-relabel works well here: each computer looks only at its own pipes. A computer with too much water pushes it down to a lower neighbour, and if it cannot, it raises its own height. This is simple, but water that cannot reach the sink must climb all the way back to the source. That can take many rounds, even in a small network.

The fast methods give up a tiny bit of the answer. They find a flow that is almost the maximum, in about as many rounds as the lower bound.

## Definition

**Input.** A connected network $G = (V, E)$ with $n$ nodes, $m$ links and hop diameter $D$. Each arc $(u, v)$ has an integer capacity $c(u, v) \ge 0$, known to $u$ and $v$. An undirected edge is two arcs with the same capacity. Two nodes $s$ and $t$ know their roles.

**Output.** A flow $f$: each node $v$ knows $f(v, w)$ for each neighbour $w$, with

- $f(v, w) = -f(w, v)$ (skew symmetry),
- $f(v, w) \le c(v, w)$ (capacity),
- $\sum_w f(w, v) = 0$ for each $v \ne s, t$ (conservation),

and the value $|f| = \sum_w f(w, t)$ is as large as possible. A $(1 - \epsilon)$-approximate flow has value at least $(1 - \epsilon)$ times the maximum.

**Cost.** Synchronous rounds with one message of $O(\log n)$ bits per link and direction per round. A message holds one capacity or one flow amount, so the capacities are polynomial in $n$.

## Variants

- **The flow value only.** Each node learns $|f|$. By the [max-flow min-cut theorem](/max-flow-min-cut-theorem/), this is the minimum $s$-$t$ cut value, so the lower bounds for cuts apply.
- **Undirected or directed.** The fast approximation is for undirected graphs. For directed graphs, the known exact algorithms are slower, and near-optimal bounds are open.
- **Exact flow.** Forster, Goranci, Liu, Peng, Sun and Ye (FOCS 2021) give a Laplacian solver in $n^{o(1)} (\sqrt{n} + D)$ rounds. With interior point methods, this gives exact maximum flow in CONGEST in fewer than $n$ rounds for sparse graphs with small diameter.
- **Minimum cost flow** and **multicommodity flow** follow the same plan: a central method from the [Laplacian paradigm](/electrical-flow/) with a distributed linear solver in each step.

## Examples

**Synchronous push-relabel on 5 nodes.** Take a path $a - b - c$, the source $s$ joined to $a$, $b$ and $c$, and the sink $t$ joined to $b$ and $c$. The links $s a$, $s b$, $s c$, $a b$ and $b c$ have capacity 3, and $b t$, $c t$ have capacity 1. The hop diameter is 2, and the maximum flow is 2 (the cut is $\{b t, c t\}$).

In round 0, $s$ has height $n = 5$ and saturates its three links, so $a$, $b$ and $c$ hold 9 units. Only 2 units can enter $t$. The other 7 units must go back to $s$, so the heights of $a$, $b$ and $c$ must rise above 5 one step at a time. The implementation takes 7 pulses (15 rounds), sends 62 messages, and the highest height is 6. The same shape with $k$ path nodes takes $n + 2$ pulses although the diameter stays 2, while $\sqrt{n} + D$ grows only as $\sqrt{n}$. The tests check this.

## Known algorithms

**Synchronous push-relabel (Goldberg and Tarjan, 1988).** Each node $v$ holds a height $d(v)$ and an excess $e(v)$. Start with $d(s) = n$, $d(v) = 0$ otherwise, and let $s$ saturate its arcs. Then repeat pulses of two rounds, while some node other than $s$ and $t$ has excess:

1. Each active node pushes its excess (as it was at the start of the pulse) along residual arcs $(v, w)$ with $d(v) = d(w) + 1$. Each push is one message with the amount.
2. Each active node that still has excess sets $d(v) = 1 + \min\{d(w) : (v, w)$ is residual$\}$, with the heights of the start of the pulse, and sends its new height to its neighbours.

*What it gives.* The heights stay valid ($d(v) \le d(w) + 1$ for each residual arc), so no residual path joins $s$ to $t$, and at the end the preflow is a maximum flow. Each height stays below $2n$. Goldberg and Tarjan show that the synchronous algorithm stops after $O(n^2)$ pulses with $O(n^3)$ messages. Each message holds one amount, so the CONGEST budget holds when the capacities are polynomial. The run time depends on $n$ and not on $D$, as the example shows.

**Near-optimal approximation (Ghaffari, Karrenbauer, Kuhn, Lenzen and Patt-Shamir).** For undirected graphs, a $(1 + o(1))$-approximate flow in $(D + \sqrt{n}) \cdot n^{o(1)}$ rounds. *Sketch only.* The algorithm runs Sherman's gradient method (FOCS 2013). Its main tool is a congestion approximator: a small set of cuts, here the cuts of $O(\log n)$ virtual trees from a spanning tree of average stretch $n^{o(1)}$, that tells within a factor $n^{o(1)}$ how congested the best routing of each demand is. Each step of the method evaluates the approximator, which is a set of sums over tree parts, and the paper does each step in $(D + \sqrt{n}) n^{o(1)}$ rounds. The method needs $n^{o(1)}$ steps.

**Exact flow through the Laplacian paradigm.** Forster et al. (FOCS 2021) build a distributed Laplacian solver from minor sparsifiers and use it in interior point methods for exact flows. *We give no round bound here*, since the bounds for exact flow in the follow-up papers differ in form, and none of them is near $\sqrt{n} + D$.

## Bounds

- **Lower bound.** Each algorithm that approximates the minimum $s$-$t$ cut within any polynomial factor needs $\tilde{\Omega}(\sqrt{n} + D)$ rounds, even with randomization (Das Sarma et al., SIAM J. Comput. 2012). The flow value equals the cut value, so the same bound holds for any approximate flow value. The proof is the [Peleg-Rubinovich](/peleg-rubinovich-lower-bound/) style reduction from set disjointness.
- **Upper bound.** $(D + \sqrt{n}) \cdot n^{o(1)}$ for $(1 + o(1))$ approximation on undirected graphs, so the gap is a factor $n^{o(1)}$.
- **Exact.** The trivial upper bound is to collect the whole graph at one node: $O(m + D)$ rounds. Push-relabel gives $O(n^2)$, which does not use the collection.

## Reductions

- **From cuts.** The flow value is the min $s$-$t$ cut value, so flow is at least as hard as $s$-$t$ cut approximation, which is at least as hard as the subgraph connectivity of [distributed connected components](/distributed-connected-components/).
- **To linear algebra.** The fast exact algorithms reduce flow to a sequence of Laplacian systems ([electrical flows](/electrical-flow/)), and the distributed work is in the solver.
- **Global min cut.** The global min cut is the smallest $s$-$t$ cut over the pairs with a fixed $s$, but the fast [distributed min cut](/distributed-min-cut/) algorithms do not use flows.

## Applications

- **Network capacity.** A network finds how much traffic it can carry between two points, for example between two data centres, from the link capacities that each router knows.
- **Routing.** A flow gives a routing of one demand with low congestion. The congestion approximator of the fast algorithm is close to [oblivious routing](/oblivious-routing/).
- **A tool in other algorithms.** Flows give cuts, and cuts give tests of connectivity, matchings in bipartite networks and bounds for many partitioning problems.

## References
