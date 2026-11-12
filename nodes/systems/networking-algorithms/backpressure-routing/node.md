---
tag: 0WEF6V
kind: algorithm
slug: backpressure-routing
name: Backpressure routing
aliases:
- max-weight routing
- Tassiulas-Ephremides policy
- differential backlog routing
area: systems/networking-algorithms
level: research
summary: "Weigh each link by its largest queue difference over the commodities, activate the feasible link set of largest weight, and send that commodity; this is throughput optimal."
model: word-ram
complexity:
  vars: {s: the number of slots, L: the number of links, K: the number of commodities, A: the number of feasible link sets, N: the number of nodes}
  time: {worst: Θ(s·L·(K + A))}
  space: {extra: Θ(N·K + L)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [wireless-link-scheduling, packet-scheduling]
see_also: [proportional-fair-scheduling, network-utility-maximization, maximum-throughput-routing, routing-problem, switch-scheduling, maximum-weight-matching, congestion-control, backpressure]
sources:
  - paper: doi:10.1109/9.182479
    title: Leandros Tassiulas and Anthony Ephremides, Stability properties of constrained queueing systems and scheduling policies for maximum throughput in multihop radio networks, IEEE Transactions on Automatic Control 37(12) (1992)
    locator: pp. 1936 to 1948 (the policy with differential backlogs, the capacity region, and the proof of stability for every rate inside it)
  - book: isbn:9781608454556
    title: Michael J. Neely, Stochastic Network Optimization with Application to Communication and Queueing Systems, Morgan and Claypool, 2010
    locator: Chapters 3 and 4 (Lyapunov drift, the max-weight rule, and the drift-plus-penalty method)
  - paper: doi:10.1561/1300000001
    title: Leonidas Georgiadis, Michael J. Neely and Leandros Tassiulas, Resource allocation and cross-layer control in wireless networks, Foundations and Trends in Networking 1(1) (2006)
    locator: pp. 1 to 144 (the network model, the capacity region, backpressure routing and its joint use with flow control)
  - book: isbn:9781107036055
    title: R. Srikant and Lei Ying, Communication Networks, An Optimization, Control and Stochastic Networks Perspective, Cambridge University Press, 2014
    locator: Section 4.2 (the capacity region and MaxWeight), Section 5.5 (general MaxWeight) and Section 6.1 (back-pressure routing)
---

Backpressure routing is the routing and scheduling policy of Tassiulas and Ephremides (1992) for networks with many sources and destinations. Each node keeps a queue $Q_n^c$ for every commodity $c$, the packets bound for destination $c$. In each slot, a link $l = (a, b)$ gets the weight $W_l = \max_c (Q_a^c - Q_b^c)^+$, the largest *differential backlog* over the commodities, and the commodity $c_l$ that attains it. The policy activates the feasible set of links with the largest $\sum_l \mu_l W_l$, where $\mu_l$ is the rate of link $l$, and each active link with $W_l > 0$ sends packets of $c_l$. There is no routing table: packets flow from long queues toward short ones, and the destination's own queue is always empty. The policy is *throughput optimal*: it keeps all queues stable for every arrival rate vector inside the capacity region of the network. The proof is a Lyapunov drift argument with $V = \sum Q^2$.

## In plain words

Picture water tanks joined by pipes, with the outlet for each kind of water at its destination. Water flows from a full tank to an emptier one. Backpressure routing moves packets the same way.

Every node keeps a separate pile of packets for each destination. For each link, the node compares its piles with the piles at the other end, and finds the destination with the biggest difference. That difference is the pressure on the link.

When radios interfere, only some links can send at once. In each slot the network picks the group of links with the most total pressure, and those links send.

Nobody computes routes. Packets find their way because the destination always has an empty pile, so the pressure points toward it. If the network can carry the traffic at all, the piles stay bounded.

## The problem

A network has nodes, directed links with rates $\mu_l$ packets per slot, and a list $\mathcal{A}$ of feasible link sets that can be active in the same slot, as in [wireless link scheduling](/wireless-link-scheduling/). Packets for destination $c$ arrive at node $n$ at random, with mean $\lambda_n^c$ per slot. The policy must choose in each slot which links send and which packets they carry, using only the current queues. The aim is stability for every $\lambda$ inside the *capacity region* $\Lambda$: the set of rates for which some flow assignment and some mix of feasible sets carry all traffic to its destinations. No policy can do better, since for rates outside the closure of $\Lambda$ every policy has queues that grow without bound. This is a scheduling and routing problem together; the fixed-route [routing problem](/routing-problem/) and the [maximum throughput routing](/maximum-throughput-routing/) problem are the static versions.

## The algorithm

The pseudocode gives the work of one slot.

```pseudo id=main
BACKPRESSURE-SLOT(queues Q_n^c, links l = (a, b) with rates μ_l, feasible sets A)
L1  for each link l = (a, b):
L2      c_l ← the commodity c with the largest Q_a^c − Q_b^c
L3      W_l ← max(Q_a^{c_l} − Q_b^{c_l}, 0)
L4  S ← the set in A with the largest Σ_{l ∈ S} μ_l W_l
L5  for each link l = (a, b) in S with W_l > 0:
L6      move up to μ_l packets of commodity c_l from node a to node b, from the packets that were at a when the slot began
L7  packets that reach their destination leave the network, so Q_c^c = 0
L8  add the packets that arrive in this slot to their queues
```

In a wired network every set of links is feasible, line L4 takes all links, and each link decides by itself. In a wireless network, line L4 is the max-weight schedule, an NP-hard problem in general.

## Example

**One slot.** The wireless diamond has links $s \to a$, $s \to b$, $a \to d$ and $b \to d$, each with rate 1. A node cannot send and receive in the same slot, so the feasible sets are $\{s{\to}a,\ b{\to}d\}$ and $\{s{\to}b,\ a{\to}d\}$. There is one commodity, destination $d$. The queues are $Q_s = 5$, $Q_a = 3$, $Q_b = 1$ and $Q_d = 0$.

| link | differential | $W_l$ |
|---|---|---|
| $s \to a$ | $5 - 3$ | 2 |
| $s \to b$ | $5 - 1$ | 4 |
| $a \to d$ | $3 - 0$ | 3 |
| $b \to d$ | $1 - 0$ | 1 |

The set $\{s{\to}a, b{\to}d\}$ has weight 3 and $\{s{\to}b, a{\to}d\}$ has weight 7, so line L4 picks the second. One packet goes from $s$ to $b$ and one from $a$ to $d$. With one new arrival at $s$, the queues become $Q_s = 5$, $Q_a = 2$ and $Q_b = 2$.

**Inside and outside the capacity region.** The capacity from $s$ to $d$ in the wireless diamond is 1 packet per slot, because each feasible set has one link into $d$. In seeded runs of 20,000 slots with up to 4 packets per slot at $s$, each present with the same probability:

| load at $s$ | mean backlog | backlog at the end |
|---|---|---|
| 0.8 | 2.8 | 2 |
| 0.95 | 8.8 | 2 |
| 1.2 | 1976 | 3928 |

At load 1.2 the backlog grows by about $1.2 - 1 = 0.2$ packets per slot. In the wired form of the diamond, where all four links run together, the capacity is 2, and the policy splits the traffic over both paths with no routing table.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Let arrivals be independent over slots with finite second moments, and let link rates be bounded.

1. **Greedy in the drift.** Among all choices of a feasible set and of the commodities its links carry, lines L1 to L4 maximize $\sum_l \sum_c \mu_l^c (Q_a^c - Q_b^c)$.
2. **Negative drift.** If $\lambda$ is inside the capacity region with slack $\varepsilon > 0$, then with $V = \sum_{n,c} (Q_n^c)^2$,

$$\mathbb{E}[V(t+1) - V(t) \mid Q(t)] \le B - 2\varepsilon \sum_{n,c} Q_n^c(t)$$

for a constant $B$ that depends on the rates and the arrival moments.
3. **Throughput optimal.** Hence $\limsup_{T \to \infty} \frac{1}{T} \sum_{t < T} \mathbb{E}\big[\sum_{n,c} Q_n^c(t)\big] \le B / (2\varepsilon)$, so all queues are stable for every $\lambda$ in the interior of $\Lambda$. For $\lambda$ outside the closure of $\Lambda$, no policy is stable.

## Complexity

Lines L1 to L3 cost $\Theta(L \cdot K)$ per slot for $L$ links and $K$ commodities. Line L4 scans the list of feasible sets, at $O(L)$ each, so $O(A \cdot L)$ for $A$ sets. In a wired network line L4 is free, and each node needs only its neighbors' queue lengths. In a wireless network with a conflict graph, line L4 is a maximum weight independent set, NP-hard in general, and the list of feasible sets can be exponential in $L$. The space is $\Theta(N \cdot K)$ for the queue counters.

## Properties

- **Throughput optimal.** It stabilizes every load that any policy can stabilize, with no knowledge of the arrival rates.
- **Routes come from the queues.** No routing table or path computation is needed; the routes adapt when links fail or rates change.
- **Local in a wired network.** Each link needs only the queue lengths at its two ends.
- **Large delay at light load.** Packets can wander, even around loops, because a gradient must build up before traffic flows straight. The mean delay grows with the number of nodes.
- **Deterministic per slot.** The randomness comes from the arrivals only; ties are broken by a fixed order.

## Variants and improvements

- **Drift-plus-penalty.** Neely's method adds $V$ times a penalty, such as power, to the drift and minimizes the sum. This gives a time-average penalty within $O(1/V)$ of the optimum with queues of size $O(V)$.
- **Backpressure with flow control.** Sources admit traffic by the size of their own queues, so that the network solves a [network utility maximization](/network-utility-maximization/) problem while it stays stable.
- **Shortest-path bias.** Adding a term for the hop count to the differential cuts the delay at light load and keeps throughput optimality.
- **LIFO backpressure.** Serving the newest packet in each queue cuts the delay of most packets by a large factor, at the cost of a few packets that wait long.
- **Greedy or distributed scheduling.** In wireless networks, replace the max-weight set at line L4 with greedy maximal scheduling or CSMA, which gives up a known fraction of the capacity.

## When to use it

Use backpressure routing when the traffic and the link rates change and no stable set of routes is known, for example in multihop wireless, sensor and vehicle networks, and in data center or satellite networks with fast changes. It is also a tool for proofs: a policy that is greedy in the drift of $\sum Q^2$ is throughput optimal. Use shortest-path routing with [congestion control](/congestion-control/) when the topology is stable and low delay matters most.

## Pitfalls

- **Confusing it with flow-control backpressure.** In [backpressure](/backpressure/) for rate limiting, a full receiver tells a sender to slow down. Backpressure routing is a routing and scheduling policy that uses differential queue lengths.
- **Sending packets that are not there.** If line L6 moves packets that arrive during the slot, a packet can cross several links in one slot. Send only what was in the queue at the start of the slot.
- **Ignoring negative differentials.** A link with $W_l \le 0$ must stay idle. Sending against the gradient breaks the drift argument.
- **Solving line L4 badly.** A heuristic schedule in a wireless network is no longer throughput optimal. Its fraction of the capacity depends on the heuristic.
- **Expecting low delay.** Throughput optimality says nothing about delay. At light load, packets can take long detours.

## Implementations

## History

Leandros Tassiulas and Anthony Ephremides introduced the policy in 1992 for multihop radio networks, with the capacity region and the proof of throughput optimality by a quadratic Lyapunov function. The same max-weight idea was applied to input-queued switches later in the 1990s. Awerbuch and Leighton gave a related local rule for multicommodity flow in 1993. Neely, Modiano and Rohrs extended the method to power allocation and time-varying channels in the early 2000s, and Georgiadis, Neely and Tassiulas surveyed the theory in 2006. Neely's drift-plus-penalty method, described in his 2010 book, joined backpressure with the optimization of time averages. Protocols for sensor networks, such as the Backpressure Collection Protocol of 2010, brought the policy into practice.

## References
