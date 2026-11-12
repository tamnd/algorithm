---
tag: R3ET6W
kind: problem
slug: wireless-link-scheduling
name: Wireless link scheduling
aliases:
- wireless scheduling
- max-weight link scheduling
area: systems/networking-algorithms
level: advanced
summary: "Choose a set of wireless links that can transmit together in each slot, under a conflict graph or SINR model, so that the queues stay stable for every load the network can carry."
prereqs: [packet-scheduling, maximum-independent-set, maximal-matching]
see_also: [backpressure-routing, proportional-fair-scheduling, switch-scheduling, maximum-weight-matching, greedy-independent-set, line-graph, csma-ca, slotted-aloha]
sources:
  - paper: doi:10.1109/9.182479
    title: Leandros Tassiulas and Anthony Ephremides, Stability properties of constrained queueing systems and scheduling policies for maximum throughput in multihop radio networks, IEEE Transactions on Automatic Control 37(12) (1992)
    locator: pp. 1936 to 1948 (the capacity region as the convex hull of the activation sets, and the max-weight policy that keeps the queues stable for every load inside it)
  - paper: doi:10.1109/TNET.2006.872546
    title: Xiaojun Lin and Ness B. Shroff, The impact of imperfect scheduling on cross-layer congestion control in wireless networks, IEEE/ACM Transactions on Networking 14(2) (2006)
    locator: pp. 302 to 315 (maximal scheduling under node-exclusive interference reaches at least half of the capacity region)
  - paper: doi:10.1109/INFCOM.2005.1498460
    title: Xiaojun Lin and Ness B. Shroff, The impact of imperfect scheduling on cross-layer rate control in multihop wireless networks, IEEE INFOCOM (2005)
    locator: the conference version of the half-capacity result for maximal scheduling
  - paper: doi:10.1239/aap/1151337082
    title: Antonios Dimakis and Jean Walrand, Sufficient conditions for stability of longest-queue-first scheduling, second-order properties using fluid limits, Advances in Applied Probability 38(2) (2006)
    locator: pp. 505 to 521 (the local pooling condition, under which longest queue first is throughput optimal)
  - paper: doi:10.1109/INFOCOM.2008.165
    title: Changhee Joo, Xiaojun Lin and Ness B. Shroff, Understanding the capacity region of the greedy maximal scheduling algorithm in multi-hop wireless networks, IEEE INFOCOM (2008)
    locator: pp. 1103 to 1111 (the local pooling factor and the efficiency ratio of greedy maximal scheduling)
  - paper: doi:10.1109/TNET.2009.2026276
    title: Changhee Joo, Xiaojun Lin and Ness B. Shroff, Understanding the capacity region of the greedy maximal scheduling algorithm in multihop wireless networks, IEEE/ACM Transactions on Networking 17(4) (2009)
    locator: pp. 1132 to 1145 (the efficiency ratio of greedy maximal scheduling equals the overall local pooling factor)
  - book: isbn:9781107036055
    title: R. Srikant and Lei Ying, Communication Networks, An Optimization, Control and Stochastic Networks Perspective, Cambridge University Press, 2014
    locator: Section 4.2 (the capacity region and MaxWeight), Section 5.4 (MaxWeight for ad hoc wireless networks) and Section 5.6 (Q-CSMA)
---

Wireless link scheduling is the problem of choosing, in each time slot, a set of links of a wireless network that transmit at the same time. Links near each other interfere, so not every set works. The interference is given by a *conflict graph* on the links, where a feasible set is an independent set, or by the *SINR model*, where every active link needs a signal strong enough against the noise and the sum of the other signals. The usual goal is throughput: keep all queues stable for every arrival rate that some schedule can carry. Tassiulas and Ephremides (1992) showed that the *max-weight* rule, which picks the feasible set with the largest sum of queue lengths, does this. On a conflict graph that rule is a maximum weight independent set (MWIS), which is NP-hard, so practical systems use greedy or random-access rules that reach a known fraction of the capacity. Under node-exclusive interference, schedules are matchings, and greedy maximal matching reaches at least half of it.

## In plain words

Radios that are close together cannot all talk at once, or their signals mix and nothing gets through. In each short time slot, the network must decide which links may send.

A good choice keeps the waiting data small. The best known rule gives priority to links with long queues: among all groups of links that can send together, take the group whose queues add up to the most. This rule keeps every queue under control whenever that is possible at all.

Finding that best group is a hard puzzle when the network is large, much like finding the best group of non-neighbors in a graph. So real networks use quick rules, for example taking the longest queue first and then adding links that do not clash. These quick rules lose some capacity, and theory tells how much.

## Definition

A network has a set $L$ of $m$ directed links. Time is slotted. A set $S \subseteq L$ is *feasible* if all its links can transmit in one slot. Two models of interference are common.

- **Conflict graph.** A graph $G_c$ on the links has an edge between two links that cannot be active together. The feasible sets are the independent sets of $G_c$. Under *node-exclusive* (primary) interference, two links conflict when they share a node, so $G_c$ is the [line graph](/line-graph/) of the network and the feasible sets are its matchings. Under *$k$-hop* interference, links within $k$ hops conflict.
- **SINR.** Link $l$ has a sender with power $P_l$, and the gain from the sender of $k$ to the receiver of $l$ is $g_{kl}$. A set $S$ is feasible if for every $l \in S$,

$$\frac{P_l\, g_{ll}}{N_0 + \sum_{k \in S,\, k \ne l} P_k\, g_{kl}} \ge \beta.$$

Let $\mathcal{S}$ be the feasible sets and $\mathbf{1}_S \in \{0,1\}^m$ the vector of a set. Packets arrive at link $l$ at rate $\lambda_l$ per slot, and an active link sends one packet. The *capacity region* is $\Lambda = \{\lambda : \lambda < \mu \text{ for some } \mu \in \text{conv}\{\mathbf{1}_S : S \in \mathcal{S}\}\}$. No policy can keep the queues stable for $\lambda$ outside the closure of $\Lambda$. A policy is *throughput optimal* if it keeps the queues stable for every $\lambda \in \Lambda$, and its *efficiency ratio* is the largest $\gamma$ such that it keeps them stable for every $\lambda \in \gamma\Lambda$.

The one-slot problem, the *max-weight schedule*, is: given weights $w_l \ge 0$, usually the queue lengths $q_l(t)$, find

$$S^*(t) \in \arg\max_{S \in \mathcal{S}} \sum_{l \in S} w_l.$$

## Variants

- **Max-weight per slot.** The one-slot problem above, which is MWIS on the conflict graph.
- **Minimum-length schedule.** Serve a given demand $d_l$ for each link in the fewest slots. On a conflict graph, this is a multicoloring problem: link $l$ needs $d_l$ colors, and links that conflict share none.
- **Multihop with routing.** Choose links and the packets they carry, as in [backpressure routing](/backpressure-routing/).
- **Fading channels.** The rates depend on a random channel state, and the max-weight rule uses the rate times the queue length. [Proportional fair scheduling](/proportional-fair-scheduling/) is the single-cell case without queues.
- **Distributed scheduling.** Each link decides from local information, through contention as in [CSMA/CA](/csma-ca/) or [slotted ALOHA](/slotted-aloha/), or through message passing.

## Examples

**A path.** Nodes $a, b, c, d$ form a path with links $ab$, $bc$ and $cd$, and queue lengths 2, 3 and 2. Under node-exclusive interference, $bc$ conflicts with both others, and the feasible sets are the matchings $\{ab, cd\}$, $\{bc\}$ and their subsets. The max-weight schedule is $\{ab, cd\}$ with weight 4. Greedy maximal scheduling takes the longest queue $bc$ first, and then no other link fits, so it gets 3. The capacity region is $\lambda_{bc} + \max(\lambda_{ab}, \lambda_{cd}) < 1$.

**A star conflict graph.** A link with queue 11 conflicts with ten links that have queue 10 each, and these ten do not conflict with each other. Greedy takes the link with 11 and gets 11, but the optimum takes the ten others and gets 100. On a general conflict graph, greedy can be far from optimal.

**SINR is not pairwise.** Three links have own gain 1, cross gain $1/2$, power 1, noise $N_0 = 0.1$ and threshold $\beta = 1$. A pair gives SINR $1 / (0.1 + 0.5) \approx 1.67$, so every pair is feasible. All three give $1 / (0.1 + 1) \approx 0.91$, so the triple is not. The conflict graph of this example has no edges, and it would wrongly allow all three links.

## Known algorithms

| algorithm | idea | guarantee |
|---|---|---|
| max-weight (Tassiulas and Ephremides) | solve MWIS on the queue lengths in each slot | throughput optimal; NP-hard per slot in general |
| exact MWIS for small instances | branch on a link: leave it out, or take it and drop its conflicts | $O(2^m)$ per slot |
| max-weight matching | node-exclusive interference only | throughput optimal, polynomial time |
| greedy maximal scheduling (longest queue first) | take the longest queue, drop its conflicts, repeat | efficiency ratio equal to the local pooling factor; at least 1/2 under node-exclusive interference |
| [greedy independent set](/greedy-independent-set/) by weight | the same rule seen as a graph algorithm | a maximal independent set |
| pick and compare | keep the last schedule, compare it with a random new one, keep the heavier | throughput optimal with linear work per slot |
| Q-CSMA and adaptive CSMA | random access with back-off rates set by the queue lengths | throughput optimal in the limit, fully distributed |
| random access (ALOHA) | each link sends with a fixed probability | a small fraction of the capacity |

## Bounds

- **Hardness.** On a general conflict graph, the max-weight schedule is MWIS, which is NP-hard and, unless P = NP, cannot be approximated within $m^{1-\varepsilon}$ for any fixed $\varepsilon > 0$. Scheduling in the SINR model is also NP-hard.
- **Node-exclusive interference.** The max-weight schedule is a [maximum weight matching](/maximum-weight-matching/) of the network graph, solvable in polynomial time. A greedy matching by weight has at least half the maximum weight, since each edge it takes blocks at most two edges of an optimal matching, each of weight at most its own. Lin and Shroff showed that greedy maximal scheduling then keeps the queues stable for every $\lambda \in \Lambda / 2$.
- **Local pooling.** Dimakis and Walrand defined local pooling: for every subset of links, no convex combination of the maximal schedules of that subset is strictly smaller on every link of the subset than another convex combination of them. When it holds, greedy maximal scheduling is throughput optimal. Joo, Lin and Shroff defined the local pooling factor $\sigma^* \in (0, 1]$ and proved that the efficiency ratio of greedy maximal scheduling is exactly $\sigma^*$.
- **Capacity region.** No policy keeps the queues stable for $\lambda$ outside the closure of $\Lambda$, because the long-run service vector of any policy lies in $\text{conv}\{\mathbf{1}_S\}$.

## Reductions

- **From MWIS.** Every graph is the conflict graph of some set of links, so the max-weight schedule on a conflict graph is as hard as MWIS. Conversely, any MWIS solver gives the max-weight schedule.
- **To matching.** Under node-exclusive interference, schedules are matchings of the network graph, and max-weight scheduling is maximum weight matching. Input-queued [switch scheduling](/switch-scheduling/) is the special case of a complete bipartite network.
- **To coloring.** Serving a demand of one slot per link in the fewest slots is coloring the conflict graph.
- **From stability to optimization.** The Lyapunov drift of $\sum_l q_l^2$ is smallest for the max-weight schedule, which reduces the stability problem to the one-slot problem. [Backpressure routing](/backpressure-routing/) extends this to multihop flows.

## Applications

- Scheduling of mesh and ad hoc networks, sensor networks and vehicle networks with time-slotted access.
- The design of random-access protocols that approach the capacity of max-weight scheduling, such as Q-CSMA.
- Cross-layer design, where a rate control layer and a scheduling layer together solve a [network utility maximization](/network-utility-maximization/) problem.
- Scheduling the uplink and downlink of cellular systems with several cells, and device-to-device links.

## References
