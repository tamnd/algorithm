---
tag: JQ763C
kind: algorithm
slug: multi-probe-consistent-hashing
name: Multi-probe consistent hashing
aliases:
- multi-probe hashing
- multi-probe consistent hash
area: systems/load-balancing-and-hashing
level: advanced
summary: Put each node once on the ring, hash each key k times, and pick the node nearest to any probe. With 21 probes the peak load is about 1.05 times the mean.
solves: [dynamic-partitioning-problem]
model: word-ram
complexity:
  vars: {n: the number of nodes, k: the number of probes per key}
  time: {worst: O(k log n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2015
  people: [Ben Appleton, "Michael O'Reilly"]
  note: Appleton and O'Reilly of Google described the scheme on arXiv in 2015 as a ring with one point per node and several hashes per key.
prereqs: [consistent-hashing, hash-ring]
see_also: [virtual-nodes, monotonicity-property, power-of-two-choices, rendezvous-hashing, jump-consistent-hash, bounded-load-consistent-hashing, consistent-hashing-max-load-bound, spread-and-load]
sources:
  - url: https://arxiv.org/abs/1505.00062
    title: Ben Appleton and Michael O'Reilly, Multi-probe consistent hashing, arXiv:1505.00062, 2015
    locator: Section 3.3 (the scheme, Lemma 1 and Theorem 1, a peak of K/(K - 1) times the mean), Section 3.4 (monotonicity), Section 5.1 and Tables 2 and 3 (measured peak-to-average for K = 2 and K = 21)
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, Proceedings of the 29th ACM Symposium on Theory of Computing (STOC), 1997
    locator: the ring with several points per server, and the monotonicity, spread and load properties
---

Multi-probe consistent hashing puts each node at one point on the [hash ring](/hash-ring/) and hashes each key $k$ times. For each probe it finds the next node clockwise and its distance, and the key goes to the node with the smallest distance over all probes. One point per node gives a very uneven ring, but the $k$ probes even it out: with random node points, the largest share is about $k/(k-1)$ times the mean, so 21 probes give about 1.05. The scheme keeps the [monotonicity property](/monotonicity-property/) and needs only $\Theta(n)$ memory, with no [virtual nodes](/virtual-nodes/).

## In plain words

Put each server at one random spot on a circle. A plain ring sends a key to the first server after the key's spot, so a server that follows a long empty stretch of the circle gets many keys. Here the key throws several darts at the circle. Each dart walks clockwise to the next server and measures how far it had to walk. The key goes to the server that the shortest walk reaches.

A server behind a long empty stretch still catches many darts, but those darts usually have long walks and lose to a shorter walk of another dart. So the long stretches lose their advantage, and the loads become nearly equal.

## The problem

The input is a key and a set of $n$ nodes, each with a name. The output is one node. The goals are those of the [dynamic partitioning problem](/dynamic-partitioning-problem/): all clients compute the same node with no communication, the shares are nearly equal, and a change to the node set moves few keys. The plain [consistent hashing](/consistent-hashing/) ring with one point per node has a largest share of about $\ln n$ times the mean. The usual fix is $\Theta(\log n)$ or more virtual nodes per node, which multiplies the memory. Multi-probe hashing moves the cost from memory to lookup time.

## The algorithm

$P$ is the sorted list of node points on a ring of $R$ positions, and $h_1, \ldots, h_k$ are $k$ different hash functions for keys.

```pseudo id=main
MP-LOOKUP(key, P, k)
L1  best_dist ← R, best ← nil
L2  for i ← 1 to k do
L3      q ← h_i(key)
L4      p ← the first point of P at or after q, or P[0] if there is none
L5      d ← (p − q) mod R                          ▷ the clockwise distance
L6      if d < best_dist then
L7          best_dist ← d, best ← p
L8  return the node whose point is best
```

Line L4 is a binary search in the sorted list. Adding or removing a node inserts or deletes one point of $P$. The key hashes do not depend on the nodes.

## Example

Take a ring of 100 positions and three nodes: A at 10, B at 40 and C at 90. A plain ring gives A the arc from 90 to 10 (length 20), B the arc from 10 to 40 (length 30) and C the arc from 40 to 90 (length 50). Let $k = 2$.

| key | probe points | next node, distance | result |
|---|---|---|---|
| $x$ | 33, 85 | B at 7, C at 5 | C |
| $y$ | 95, 60 | A at 15, C at 30 | A |
| $z$ | 12, 70 | B at 28, C at 20 | C |

With one probe, the shares are the arc lengths, 0.2, 0.3 and 0.5, so the largest share is 1.5 times the mean. With $k$ probes, the share of a node is $k \int_0^{a} G(t)^{k-1} dt$, where $a$ is the length of its arc and $G(t)$ is the probability that one probe walks more than $t$ (Theorem 4 of the proof). For this ring:

| probes $k$ | share of A | share of B | share of C | largest share / mean |
|---|---|---|---|---|
| 1 | 0.2000 | 0.3000 | 0.5000 | 1.500 |
| 2 | 0.2800 | 0.3400 | 0.3800 | 1.140 |
| 3 | 0.3120 | 0.3400 | 0.3480 | 1.044 |
| 5 | 0.3299 | 0.3349 | 0.3352 | 1.006 |

**Random node points.** The table gives the exact largest share divided by the mean, with node points from BLAKE2b, as the median over 41 different node sets, next to the medians that the paper reports in Tables 2 and 3.

| nodes $n$ | $k = 1$ | $k = 2$ | paper, $K = 2$ | $k = 21$ | paper, $K = 21$ |
|---|---|---|---|---|---|
| 10 | 2.78 | 1.70 | 1.74 | 1.058 | 1.04 |
| 100 | 5.08 | 1.97 | 1.96 | 1.044 | 1.05 |
| 1000 | 7.15 | 2.00 | 2.00 | 1.050 | 1.05 |

The value for $k = 21$ depends on the node set. For the 100 nodes named node0 to node99, it is 1.10, which is close to the 99th percentile of 1.10 in Table 3 of the paper. The smallest share in that set is only 0.028 times the mean, because a node with a very short arc catches few probes.

## Correctness

For one probe, the node found in line L4 is the node with the smallest clockwise distance from the probe. The loop keeps the smallest distance seen so far, and the first probe wins a tie. So the lookup returns the node of the pair (probe, node) with the smallest distance over all probes and all nodes. Adding a node only adds pairs and leaves the distances of the other pairs as they were, so a key keeps its node or moves to the new node. Removing a node only takes away its pairs, so only its keys move. With independent uniform probes, the share of a node is the integral above, and the shares add up to 1. The full proof is below.

## Complexity

- **Lookup.** $k$ hashes and $k$ binary searches, so $O(k \log n)$ time. The paper stores the points in a hash table of small sorted buckets instead of a sorted list, which makes each probe $O(1)$ expected time and a lookup $O(k)$.
- **Space.** $\Theta(n)$: one point per node, against $\Theta(n \log n / \varepsilon^2)$ points for a ring with virtual nodes and a largest share of $1 + \varepsilon$.
- **Change of the node set.** One insert or delete in the list of points. With a sorted array this is $O(n)$, with a balanced tree or the bucket table of the paper $O(\log n)$ or $O(1)$.
- **Balance.** For random node points and $2 \le k \ll \sqrt{n}/\ln n$, the largest share is $\frac{k}{k-1} \cdot \frac{1}{n} + o(1/n)$ with high probability (Theorem 1 of the paper). For a largest share of $1 + \varepsilon$ times the mean, take $k = 1 + 1/\varepsilon$, so a lookup costs $O(1/\varepsilon)$ probes.

## Properties

- **Monotone.** Adding a node moves keys only to it, and removing a node moves only its keys (Theorems 2 and 3 of the proof). See the [monotonicity property](/monotonicity-property/).
- **Balance with high probability, not always.** The bound $k/(k-1)$ is for random node points. A given node set can be worse, and the low side has no bound: a node with arc $a$ gets at most $k a$ of the keys.
- **Arbitrary removals.** Unlike [jump consistent hash](/jump-consistent-hash/), any node can leave.
- **Small memory.** The only state is the list of node points.
- **Deterministic.** All clients with the same node set and the same $k$ hash functions agree.

## Variants and improvements

- **Weights.** The paper leaves weights open. A heavier node can get a few points, as with virtual nodes, but then the scheme loses part of its memory advantage.
- **Bounded loads.** When a hard cap on each node is needed, add the capacity rule of [consistent hashing with bounded loads](/bounded-load-consistent-hashing/) on top of a ring.
- **Rendezvous hashing.** [Rendezvous hashing](/rendezvous-hashing/) has equal shares in expectation for any node set, at a cost of $n$ hashes per lookup. Multi-probe hashing is the middle point: $k$ hashes, and nearly equal shares.
- **A link with two choices.** Picking the shorter of two walks is close in spirit to [the power of two choices](/power-of-two-choices/): a few random options cut the worst case. Here the option is chosen by distance, not by current load, so the choice needs no shared state.

## When to use it

Use multi-probe hashing when nodes come and go in any order, clients must agree with no coordination, and the memory of many virtual nodes per node is too much, for example in a client library that holds the ring for thousands of nodes. Use jump consistent hash when the nodes are numbered shards that only grow at the end, and rendezvous hashing when $n$ is small enough that $n$ hashes per lookup is cheap.

## Pitfalls

- **Few keys per node.** The bound is on the expected shares. With 1,000 keys per node, the count of a node has a standard deviation of about 32 keys, so a measured peak of 1.10 to 1.20 is normal noise on top of the 1.05.
- **Probes that are not independent.** The $k$ hash functions must behave as independent. Deriving the probes as $h(x) + i$ or from one weak hash puts them close together on the ring, and then they reach the same node.
- **A light tail.** Nodes with very short arcs get far less than the mean. If an empty node is a problem, give it a second point.
- **A changed $k$.** Each probe is a different hash function, so changing $k$ changes the result for many keys. All clients must use the same $k$.
- **Ties.** Two probes can have the same distance to different nodes. All clients must break ties the same way, here by the lower probe number.

## Implementations

## History

Ben Appleton and Michael O'Reilly of Google described multi-probe consistent hashing on arXiv in 2015. They proved that two probes already turn the $\Theta(\log n)$ peak of a ring with one point per node into a constant, and that $k$ probes give a peak of $k/(k-1)$ times the mean. They measured a median peak of 1.05 with 21 probes and up to 100,000 nodes, and compared the scheme with the ring of Karger et al. (1997) and with jump consistent hash (2014).

## References
