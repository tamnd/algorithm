---
tag: NQF31F
kind: algorithm
slug: cyclon
name: Cyclon
aliases:
- Cyclon peer sampling
- CYCLON enhanced shuffling
area: distributed/gossip
level: advanced
summary: Each node keeps c aged entries and once per cycle swaps l of them with its oldest neighbour, which gives an overlay close to a random graph with an even in-degree.
solves: [random-peer-sampling]
model: asynchronous-model
complexity:
  vars: {n: the number of nodes, c: the cache size, l: the shuffle length}
  time: {worst: O(c)}
  space: {extra: O(c)}
properties: {deterministic: false, recursive: false}
prereqs: [peer-sampling-service, random-peer-sampling, newscast]
see_also: [newscast, peer-sampling-service, random-peer-sampling, hyparview, scamp, membership-management, churn, clustering-coefficient]
sources:
  - paper: doi:10.1007/s10922-005-4441-x
    title: Spyros Voulgaris, Daniela Gavidia and Maarten van Steen, CYCLON, inexpensive membership management for unstructured P2P overlays, Journal of Network and Systems Management 13(2), 2005
    locator: pages 197 to 217 (basic shuffling, enhanced shuffling with ages and the oldest neighbour, the join by random walks, and the measurements of in-degree, clustering, path length and dead links)
  - paper: doi:10.1145/1275517.1275520
    title: Márk Jelasity, Spyros Voulgaris, Rachid Guerraoui, Anne-Marie Kermarrec and Maarten van Steen, Gossip-based peer sampling, ACM Transactions on Computer Systems 25(3), article 8, 2007
    locator: Cyclon as the swapper instance of the generic framework, with tail peer selection and push-pull propagation
---

Cyclon is a gossip protocol for [random peer sampling](/random-peer-sampling/), from Voulgaris, Gavidia and van Steen (2005), in which each node keeps a cache of $c$ entries with ages and, once per cycle, swaps $l$ of them with the neighbour whose entry is the oldest. A swap moves entries instead of copying them, and the node sends a fresh entry about itself in place of the entry of its partner, so the link between the two is reversed. The result is an overlay close to a random graph, with an in-degree that stays near $c$ and a low clustering coefficient. Contacting the oldest neighbour also finds crashed nodes, but healing is slower than in [Newscast](/newscast/).

## In plain words

Each computer keeps a small address book. Every entry has an age, the number of rounds since it was made.

Once per round, each computer calls the oldest friend in its book. It crosses that friend out, and gives the friend a fresh card with its own address together with a few random cards from its book. The friend gives back the same number of random cards from its own book. Each side puts the new cards in the places of the cards it gave away.

Cards are swapped, not copied, so no computer ends up in far more books than the others. Calling the oldest friend first means that a friend who has crashed is found soon: the call fails, and the card is gone.

## The problem

Every node must return peers that are close to uniform random live nodes, with a view of only $c$ entries, under joins and crashes. In-degree balance matters here: a node is returned by getPeer at a uniform node with probability equal to its in-degree divided by $nc$ (see [random peer sampling](/random-peer-sampling/)).

## The algorithm

An entry is a pair (address, age). The cache of node $P$ holds at most $c$ entries with distinct addresses other than $P$. The shuffle length $l \le c$ is a parameter. Once per cycle, $P$ runs:

```pseudo id=main
CYCLON-SHUFFLE(P)
L1  add 1 to the age of every entry of cache(P)
L2  Q ← the entry with the highest age; S ← l − 1 other random entries of cache(P)
L3  remove the entry of Q from cache(P)
L4  send S ∪ {(P, 0)} to Q
L5  if Q does not answer, stop
L6  receive R, a set of at most l random entries that Q took from its cache
L7  discard the entries of R that point to P or that cache(P) already holds
L8  put the remaining entries of R into the empty slots of cache(P)
L9  put the rest in place of entries of S, one for one
```

When $Q$ receives the set from $P$, it chooses $R$, sends it back, and merges the received set into its own cache with lines L7 to L9, with the roles of $P$ and $Q$ exchanged: it discards entries that point to $Q$ or that it holds, fills empty slots, and then replaces entries of $R$. Ages travel with the entries.

**Join.** A new node $P$ knows one introducer $I$. $I$ starts $c$ random walks over the overlay, each of a fixed length (the paper uses the average path length). The node $A$ at the end of a walk replaces one random entry of its cache by $(P, 0)$ and gives the replaced entry to $P$. So $P$ gets up to $c$ entries and an in-degree equal to its out-degree, while every other node keeps its cache size.

**Leave and crash.** A node just stops. The entries that point to it are removed when their holders pick them as the oldest (line L5), or when they are replaced in a later swap.

**getPeer** returns a uniform entry of the cache.

## Example

Take $c = 4$ and $l = 3$. Before its shuffle, node $P$ holds $(A, 2), (B, 5), (C, 1), (D, 3)$. Line L1 makes the ages $3, 6, 2, 4$. The oldest is $B$, so $Q = B$, and suppose line L2 picks $S = \{(A, 3), (D, 4)\}$. Line L3 removes $B$, so $P$ holds $(A, 3), (C, 2), (D, 4)$ and has one empty slot. $P$ sends $\{(A, 3), (D, 4), (P, 0)\}$ to $B$.

$B$ holds $(C, 7), (E, 1), (F, 2), (G, 4)$ and picks $R = \{(C, 7), (E, 1), (G, 4)\}$. $B$ merges the set from $P$: all three entries are new to $B$, $B$ has no empty slot, so they replace $C, E, G$, and $B$ holds $(A, 3), (D, 4), (P, 0), (F, 2)$.

$P$ merges $R$: line L7 discards $(C, 7)$, which $P$ already holds. Line L8 puts $(E, 1)$ into the empty slot. Line L9 puts $(G, 4)$ in place of $A$. Now $P$ holds $(G, 4), (C, 2), (D, 4), (E, 1)$. The link from $P$ to $B$ became a link from $B$ to $P$, and $D$, which $P$ sent but did not replace, is now in both caches.

**Simulation.** The implementation runs 1000 nodes with $c = 20$ and $l = 8$ from random caches. After 50 cycles, the in-degree has mean 20 and variance 6.2, with all values from 14 to 29. A random graph with out-degree 20 has in-degree variance $c(1 - c/n) \approx 19.6$, and [Newscast](/newscast/) with the same $c$ has about 91. The mean local [clustering coefficient](/clustering-coefficient/) of the undirected overlay is 0.038 for Cyclon and 0.29 for Newscast. From a ring start with clustering 0.52, Cyclon reaches 0.039 within 20 cycles.

Then half of the nodes crash. The number of entries that point to crashed nodes:

| cycles after the crash | 0 | 5 | 10 | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|---|---|
| dead entries | 4989 | 4198 | 3530 | 2717 | 1803 | 758 | 129 |

The fall is close to linear for 20 cycles and then fast: a dead entry is removed when it becomes the oldest entry of its holder, which takes about $c$ cycles. Compare Newscast, which removes 99.5 percent of them in 10 cycles. The 500 live nodes stay connected. Under churn of 1 percent of the nodes per cycle for 30 cycles, about 10 percent of the entries point to crashed nodes, and the overlay stays connected.

## Correctness

The claims proved are the safety invariants and the structural facts behind the even in-degree: every cache holds at most $c$ distinct entries other than its owner; the partner $Q$ never loses cache size in a shuffle; a successful shuffle in which $Q$ did not hold $P$ reverses the link between $P$ and $Q$; each shuffle removes the oldest entry of $P$, so a dead oldest entry is removed; no entry about a crashed node is ever created; and a join gives the new node an in-degree equal to its out-degree without changing any other out-degree. The full proof is below.

The closeness of the overlay to a random graph is not proved. It is the result of the measurements in the paper and on this page.

## Complexity

- **Messages.** Each live node starts one shuffle per cycle, with two messages of at most $l$ entries each. A node is the partner of others in one shuffle per cycle on average, and the even in-degree keeps this load even.
- **Local work.** $O(c)$ per shuffle for the ages and the merge.
- **Space.** $O(c)$ per node.
- **Join.** $c$ random walks of a fixed length, so $O(c \cdot \text{walk length})$ messages.

## Properties

- **Even in-degree.** A swap reverses the link with the partner and moves the other entries instead of copying them, so the number of entries that point to a node changes little. The in-degree variance is smaller than in a random graph.
- **Low clustering.** The two caches after a swap share few entries, because each side gives away what the other gets.
- **Healing in about $c$ cycles.** Each entry ages by one per cycle at its holder, and each node removes its oldest entry per cycle, so a dead entry is selected about $c$ cycles after it was made at the latest, if no older entries keep arriving.
- **No clocks.** Ages are local counters, so Cyclon needs no synchronized clocks.
- **Copies can appear.** When the partner returns entries that a node already holds, the node keeps some entries that it sent, and these now exist twice. Discarding duplicates in line L7 keeps the effect small.

## Variants and improvements

- **Basic shuffling.** The first version in the paper picks a random neighbour and has no ages. It mixes the overlay just as well, but it does not detect crashed nodes in bounded time.
- **Framework view.** In the framework of Jelasity et al. (2007), Cyclon is close to tail peer selection, push-pull, and the swapper view selection ($H = 0$, $S = c/2$).
- **[HyParView](/hyparview/)** uses a Cyclon-like shuffle for its passive view.
- **Byzantine settings.** Cyclon has no defence against nodes that send entries of their own choice; protocols for that setting limit and mix the sources of entries.

## When to use it

Use Cyclon when the protocols on top need samples close to uniform with an even load, such as gossip dissemination, averaging, or random walks over the overlay. It is cheap: two short messages per node per cycle. When crashed nodes must disappear within a few cycles, [Newscast](/newscast/) heals faster.

## Pitfalls

- **Swap without discard.** If a node does not discard entries that point to itself or that it holds, its cache fills with duplicates and self-pointers.
- **Removing the partner before the answer.** The partner entry is removed in line L3 on purpose. If the partner answers, the link is reversed; if not, the dead entry is gone. Keeping the entry until the answer arrives slows down healing.
- **Join by copying.** Giving a joiner a copy of the introducer's cache creates many copies and an uneven in-degree. The join by random walks avoids it.
- **Large $l$.** With $l$ close to $c$, a shuffle replaces almost the whole cache, and the cache of a node depends mostly on its last partner.

## Implementations

## History

Cyclon was published by Voulgaris, Gavidia and van Steen in the Journal of Network and Systems Management in 2005. It built on the shuffling protocol of Stavrou, Rubenstein and Sahu (2002) for random overlays, and added the ages, the choice of the oldest neighbour and the fresh self entry. Jelasity, Voulgaris, Guerraoui, Kermarrec and van Steen (2007) placed it in their generic framework of gossip-based peer sampling as the swapper.

## References
