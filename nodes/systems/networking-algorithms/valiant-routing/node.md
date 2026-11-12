---
tag: NZAZBW
kind: algorithm
slug: valiant-routing
name: Valiant's randomized routing
aliases:
- two-phase randomized routing
- Valiant-Brebner routing
area: systems/networking-algorithms
level: advanced
summary: "Send each packet to a random intermediate node, then to its destination. On the n-cube any permutation finishes in O(n) steps with high probability; deterministic oblivious routes may need √N/n."
solves: [permutation-routing]
model: synchronous-model
complexity:
  vars: {n: the dimension of the hypercube}
  time: {worst: O(2^n), expected: O(n)}
  space: {extra: Θ(2^n)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1981
  people: [Leslie G. Valiant, Gordon J. Brebner]
  note: Valiant and Brebner presented the scheme at STOC 1981, and Valiant gave the full analysis in SIAM Journal on Computing in 1982.
prereqs: [permutation-routing, chernoff-bound, union-bound]
see_also: [oblivious-routing, dimension-order-routing, benes-network-routing, bit-reversal-permutation, store-and-forward, randomized-algorithm, maximum-throughput-routing, wormhole-routing]
sources:
  - paper: doi:10.1137/0211027
    title: "Leslie G. Valiant, A scheme for fast parallel communication, SIAM Journal on Computing 11(2) (1982), 350-361"
    locator: the two-phase scheme with random intermediate nodes and its O(log N) bound with high probability on the hypercube
  - paper: doi:10.1145/800076.802479
    title: "Leslie G. Valiant and Gordon J. Brebner, Universal schemes for parallel communication, Proceedings of the 13th ACM Symposium on Theory of Computing (1981), 263-277"
    locator: the first presentation of randomized two-phase routing on the hypercube and related networks
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 4, the section Application, packet routing in sparse networks (permutation routing on the hypercube, the delay lemma, and the 14n bound)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 4, Section 4.2, Routing in a parallel computer (the lower bound for deterministic oblivious routing and the randomized two-phase algorithm)
  - paper: doi:10.1007/BF02090400
    title: "Christos Kaklamanis, Danny Krizanc and Thanasis Tsantilas, Tight bounds for oblivious routing in the hypercube, Mathematical Systems Theory 24(4) (1991), 223-232"
    locator: the lower bound Ω(√N/d) for deterministic oblivious routing on networks of degree d, and a matching algorithm on the hypercube
  - book: isbn:9780122007514
    title: William J. Dally and Brian Towles, Principles and Practices of Interconnection Networks, Morgan Kaufmann, 2004
    locator: Chapter 9, oblivious routing (Valiant's algorithm and its cost in locality)
---

Valiant's randomized routing sends each packet in two phases: first to an intermediate node chosen uniformly at random, then from there to its real destination, each phase along a fixed simple route such as dimension-order (bit-fixing) routing. The random step turns every input, even a worst-case [permutation](/permutation-routing/), into two random-looking ones. On the $n$-dimensional hypercube with $N = 2^n$ nodes, one packet per node and one packet per edge per step, every packet arrives within $14n$ steps with probability at least $1 - 1/N$ (Valiant 1982). Without the random step, any deterministic [oblivious](/oblivious-routing/) scheme has some permutation that needs about $\sqrt{N}/n$ steps. The cost is that each packet travels up to twice as far, and the scheme throws away locality.

## In plain words

Many cars must cross a city, each to a different place. If everyone takes the shortest road, a bad set of trips can send most cars down one street, and they wait in a long line. So each driver first drives to a place picked by a coin toss, and only then to the real goal.

Now no one can plan a bad set of trips, because the coin tosses spread the cars over the whole city. Each street gets about the same small number of cars on average. The trips are about twice as long, but no street gets a long line, so all cars arrive soon.

## The problem

**Input.** A [permutation routing](/permutation-routing/) instance on the hypercube: node $p$ holds one packet with destination $d_p$, and $d$ is a permutation of the $N = 2^n$ nodes.

**Model.** Synchronous steps; each directed edge carries one packet per step; a packet that waits sits in a FIFO queue at the edge it wants. Queues are not bounded. The route of each packet may depend only on its own source, destination and random bits, not on other packets: the scheme is oblivious.

**Output.** Every packet at its destination. The measure is the number of steps until the last packet arrives.

## The algorithm

The bit-fixing route from $u$ to $t$ looks at the address bits from the most significant to the least, and crosses dimension $i$ when bit $i$ of the current node differs from bit $i$ of $t$.

```pseudo id=main
VALIANT-ROUTE(d)                                ▷ packet p starts at node p, goes to d_p
L1  for each packet p, in parallel do
L2      r_p ← a node chosen uniformly at random
L3  for phase ← 1 to 2 do
L4      for each packet p, in parallel, from its node (p in phase 1, r_p in phase 2)
L5          to its target t (r_p in phase 1, d_p in phase 2) do
L6          for i ← n − 1 down to 0 do                ▷ bit-fixing, leftmost bit first
L7              if bit i of the current node differs from bit i of t then
L8                  join the FIFO queue of the edge of dimension i; cross it when served
L9      wait until every packet has finished this phase
L10 return
```

Line L9 separates the phases, as the proof needs. In practice each packet starts phase 2 as soon as it reaches $r_p$; this pipelined form is a little faster in the measurements below.

## Example

Take $n = 4$ and packet $p = 0110$ with destination $d_p = 1011$. Without randomization it crosses dimensions 3, 2 and 0, in that order: $0110 \to 1110 \to 1010 \to 1011$. With $r_p = 0011$, phase 1 crosses dimensions 2 and 0 ($0110 \to 0010 \to 0011$) and phase 2 crosses dimension 3 ($0011 \to 1011$). Each phase route has at most $n$ edges.

The point of the method shows up on hard permutations. Under **bit reversal** (the destination of $x$ is $x$ with its bits in reverse order) and under **transpose** (swap the two halves of the address), plain bit-fixing sends many packets through a few nodes. For example, every packet that starts at a node $a\,0^{n/2}$ with $a$ odd must enter node $0^n$ along the same edge, dimension $n/2$, before it can fix the low half; there are $\sqrt{N}/2$ such packets, so at least $\sqrt{N}/2$ steps are needed. The implementation measures:

| $n$ | $N$ | plain bit-fixing, bit reversal | plain bit-fixing, transpose | $\sqrt{N}/2$ | two-phase, phased (seeds 0, 1, 2) | two-phase, pipelined |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | 64 | 7 | 7 | 4 | 14, 12, 14 | 11, 10, 10 |
| 8 | 256 | 12 | 12 | 8 | 16, 18, 16 | 14, 14, 14 |
| 10 | 1024 | 21 | 21 | 16 | 20, 21, 20 | 19, 17, 20 |
| 12 | 4096 | 38 | 38 | 32 | 23, 25, 24 | 21, 22, 22 |
| 14 | 16384 | 71 | 71 | 64 | 28, 29, 29 | 25, 25, 26 |
| 16 | 65536 | 136 | 136 | 128 | 33, 33, 33 | 28, 30, 29 |

Plain bit-fixing grows like $\sqrt{N}$; the two-phase scheme grows like $2n$. The crossover is near $N = 1024$, because for small $N$ the doubled path length costs more than the congestion saves. On a random permutation, plain bit-fixing needed exactly $n$ steps for each of these sizes (seed 0): randomization helps only against bad inputs, and Valiant's scheme makes every input look random.

For $n = 10$ and bit reversal (seed 0), each phase took 10 steps, the largest delay of a packet was 3, and the largest number of other packets sharing an edge with one packet was 8, with a mean of about 1.5. Plain bit-fixing took 21 steps with a largest delay of 11.

## Correctness

Each phase delivers every packet, because each bit-fixing route is finite and an edge with a waiting packet always sends one. The time bound has three parts, proved in full below.

1. **Routes meet once.** Two bit-fixing routes share one contiguous segment, if any: once they separate, they never meet again.
2. **Delay lemma.** The delay of packet $p$ in a phase is at most the number $|S|$ of other packets whose routes share an edge with the route of $p$. Each unit of delay can be charged to a different packet of $S$ that leaves the route of $p$.
3. **Load.** With random intermediate nodes, each edge is on the route of $1/2$ packet in expectation, in either phase. So $\mathbb{E}|S| \le n/2$, and $|S|$ is a sum of independent 0-1 variables. A [Chernoff bound](/chernoff-bound/) gives $\Pr[|S| \ge 6n] \le 2^{-6n}$, so a phase ends within $7n$ steps for all packets except with probability $2^{-5n}$, by a [union bound](/union-bound/).

Two phases give $14n$ steps with probability at least $1 - 2^{-5n+1} \ge 1 - 1/N$.

## Complexity

- **Steps.** $O(n) = O(\log N)$ with high probability, and $O(n)$ in expectation. In the worst case over the random bits, the delay lemma still bounds each phase by $n + N - 1$ steps, so the total is $O(N)$.
- **Path length.** Each packet travels up to $2n$ edges, against at most $n$ for direct routing; on average $n$ against $n/2$.
- **Queues.** The analysis allows unbounded queues. With high probability the largest queue is $O(n)$, by the same counting; bounded-queue versions exist on the butterfly.
- **Local work.** Each node picks one random number per packet and, per hop, compares two addresses: $O(1)$ word operations per hop.

## Properties

- **Oblivious.** The route of a packet depends only on its source, destination and random bits.
- **Randomized, with a guarantee for every input.** The bound holds for every permutation; the probability is over the random choices only.
- **Load balancing.** In throughput terms, each phase turns any admissible traffic matrix into uniform traffic. On a torus or on a full mesh of links, where uniform traffic is the easiest load, two-phase routing therefore gives every admissible pattern at least half of the throughput that the network has for uniform traffic (Dally and Towles, Chapter 9).
- **Loses locality.** A packet to a neighbor still goes, on average, half way across the network and back.

## Variants and improvements

- **Other networks.** The same scheme works on the butterfly and on meshes and tori, with the intermediate node random and each phase routed by [dimension-order routing](/dimension-order-routing/).
- **Minimal oblivious routing (ROMM).** Pick the intermediate node at random inside the smallest box that contains source and destination, so that paths stay minimal. It keeps locality but loses the worst-case guarantee on some patterns.
- **Valiant load balancing.** In backbone and data center networks, traffic between ingress and egress points is split evenly over all intermediate points, which gives the same half-capacity guarantee with no knowledge of the traffic.
- **Better oblivious routing on general graphs.** Räcke's oblivious routing gives congestion within $O(\log n)$ of optimal on any graph with $n$ nodes; see [oblivious routing](/oblivious-routing/).
- **Deterministic oblivious routing.** Kaklamanis, Krizanc and Tsantilas (1991) gave a deterministic oblivious algorithm with $O(\sqrt{N}/n)$ steps on the hypercube, matching the lower bound, so randomization is needed for $O(n)$.

## When to use it

Use two-phase routing when the traffic is unknown or chosen by an adversary and the network is regular: interconnects of parallel machines, and backbone or data center fabrics that must accept any traffic matrix within their capacity. Do not use it when the traffic is local or uniform already: then it doubles the path length for nothing. Adaptive routing, which watches queue lengths, often beats it in practice, but it is not oblivious and its worst case is harder to bound.

## Pitfalls

- **Picking the intermediate node only among some nodes.** The load calculation uses a uniform intermediate node over the whole network. A biased choice puts back the hot spots.
- **Reusing one random intermediate node for many packets.** All packets of one flow then share a path. Choose one intermediate node per packet, or per flow when packet order must be kept, with the matching loss in balance.
- **Applying the proof to the pipelined form.** The delay lemma assumes that all packets of a phase run on their own. When phases overlap, the stated proof does not apply, even though measurements show that the pipelined form is fast.
- **Ignoring the factor 2.** At low load, the scheme doubles the latency. It is a worst-case tool.
- **Deadlock with finite buffers.** With wormhole or bounded buffers, the two phases need separate virtual channels, or a packet in phase 2 can block one in phase 1 in a cycle.

## Implementations

## History

Valiant and Brebner (STOC 1981) introduced the randomized two-phase scheme for the hypercube and related networks, and Valiant (SIAM Journal on Computing, 1982) gave the analysis. The motivation was a lower bound: Borodin and Hopcroft (1982, journal version 1985) showed that deterministic oblivious routing must be slow on some permutation, and Kaklamanis, Krizanc and Tsantilas (1991) made that bound tight on the hypercube. The scheme later became a standard tool in the theory of parallel computation, the basis of the PRAM simulations of the 1980s, and, under the name Valiant load balancing, a design for backbone and data center networks in the 2000s.

## References
