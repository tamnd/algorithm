---
tag: BZKMAQ
kind: algorithm
slug: newscast
name: Newscast
aliases:
- Newscast peer sampling
- Newscast computing
area: distributed/gossip
level: advanced
summary: Each node keeps c time-stamped items about other nodes and, once per cycle, merges caches with a random cached peer, both keeping the c freshest items.
solves: [random-peer-sampling]
model: asynchronous-model
complexity:
  vars: {n: the number of nodes, c: the cache size}
  time: {worst: O(c log c)}
  space: {extra: O(c)}
properties: {deterministic: false, recursive: false}
prereqs: [peer-sampling-service, random-peer-sampling, gossip-protocol]
see_also: [peer-sampling-service, random-peer-sampling, cyclon, gossip-aggregation, membership-management, churn, lpbcast, scamp]
sources:
  - paper: "Márk Jelasity, Wojtek Kowalczyk and Maarten van Steen, Newscast computing, Technical Report IR-CS-006, Department of Computer Science, Vrije Universiteit Amsterdam, 2003"
    locator: the news items with time stamps, the cache of size c, the exchange with a random cached peer in which both keep the c freshest items, and the properties of the resulting overlay
  - paper: "Spyros Voulgaris, Márk Jelasity and Maarten van Steen, A robust and scalable peer-to-peer gossiping protocol, Second International Workshop on Agents and Peer-to-Peer Computing (AP2PC), LNCS 2872, 2003"
    locator: the same protocol and its robustness under node removal
  - paper: doi:10.1145/1275517.1275520
    title: Márk Jelasity, Spyros Voulgaris, Rachid Guerraoui, Anne-Marie Kermarrec and Maarten van Steen, Gossip-based peer sampling, ACM Transactions on Computer Systems 25(3), article 8, 2007
    locator: Newscast as an instance of the generic framework (random peer selection, push-pull, and healing view selection), and its uneven in-degree and fast self-healing
---

Newscast is a gossip protocol for [random peer sampling](/random-peer-sampling/), from Jelasity, Kowalczyk and van Steen (2003), in which each node keeps a cache of $c$ time-stamped items about other nodes. Once per cycle a node picks a random address from its cache, the two nodes merge their caches together with one fresh item about each of them, and both keep the $c$ freshest items. Because items about a crashed node are never refreshed, they age and fall out of all caches within a few cycles, so Newscast heals very fast. The price is an uneven in-degree: some nodes appear in many more caches than others, which makes the samples less uniform than in [Cyclon](/cyclon/).

## In plain words

Each computer keeps a small address book with a few dozen entries. Every entry has the time at which the listed computer last said "I am here".

Once in a while, each computer picks a random entry from its book and calls that computer. The two put their books together, each adds a fresh "I am here" entry about itself, and both keep only the newest entries.

A computer that has crashed can never say "I am here" again. Its entries only get older, and soon every book drops them because newer entries push them out. A new computer that knows one member is soon listed in many books.

The books always mix, so each computer can pick its gossip partners from a list that looks random.

## The problem

Every node must be able to return a peer that is close to a uniform random live node, while it stores only $c$ addresses and the set of nodes changes. Crashed nodes must disappear from the views, new nodes must appear, and the overlay of views must stay connected. See [random peer sampling](/random-peer-sampling/) and the [peer sampling service](/peer-sampling-service/).

## The algorithm

A *news item* is a pair $(a, \tau)$ of a node address $a$ and the time stamp $\tau$ at which node $a$ created the item. The cache of node $p$ holds at most $c$ items, with distinct addresses, none equal to $p$. In the original protocol an item also carries application news from node $a$, and the cache is the input of the application; it does not change the membership part, which is all that is shown here. Time stamps come from the local clocks, which Newscast assumes to be loosely synchronized.

Once per cycle, at time $t$, node $p$ runs:

```pseudo id=main
NEWSCAST-CYCLE(p, t)
L1  q ← an address chosen uniformly from cache(p)
L2  if q does not answer, stop this cycle
L3  M ← cache(p) ∪ cache(q) ∪ {(p, t), (q, t)}
L4  keep in M only the newest item of each address
L5  cache(p) ← the c newest items of M whose address is not p
L6  cache(q) ← the c newest items of M whose address is not q
```

Lines L3 to L6 are one exchange: $p$ sends its cache and a fresh item about itself, $q$ answers with its cache and a fresh item about itself, and each side computes its new cache from the same multiset. Ties between equal time stamps are broken at random.

**getPeer** returns a uniform address of the cache. **Join**: a new node puts one known contact into its cache; its own items spread from the first exchange on. **Leave**: a node just stops; there is no leave message.

## Example

Take $c = 2$ and four nodes $A, B, C, D$. At time 5, the caches are

- $A$: $\{(B, 3), (C, 1)\}$,
- $B$: $\{(C, 4), (D, 2)\}$.

$A$ picks $B$ (line L1). Then $M = \{(B, 3), (C, 1), (C, 4), (D, 2), (A, 5), (B, 5)\}$, and line L4 keeps the newest item of each address: $\{(A, 5), (B, 5), (C, 4), (D, 2)\}$. Line L5 gives $A$ the two newest items other than $A$: $\{(B, 5), (C, 4)\}$. Line L6 gives $B$ the two newest other than $B$: $\{(A, 5), (C, 4)\}$. The old item $(D, 2)$ fell out of both caches. If $D$ has crashed, no node will ever create a newer item about $D$, so this is how dead links disappear.

**Simulation.** The implementation runs 1000 nodes with $c = 20$ from random caches. After 40 cycles the mean in-degree is 20, as it must be with full caches, but the variance of the in-degree is about 91, against about $c(1 - c/n) \approx 19.6$ for a random graph with out-degree $c$. Then half of the nodes crash. The number of cache entries that point to crashed nodes, out of 10,000, is:

| cycles after the crash | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| dead entries | 4986 | 4783 | 4097 | 2671 | 1281 | 448 | 205 | 54 | 23 |

The 500 live nodes stay in one connected overlay throughout. Under churn of 1 percent of the nodes per cycle for 30 cycles, about 1.3 percent of the entries point to crashed nodes, and the overlay stays connected.

## Correctness

Newscast has no exact correctness condition like a sorting algorithm. The page proves the safety invariants and the self-healing argument: every cache holds at most $c$ distinct addresses other than its owner, an item about a crashed node is never refreshed, and once one live node holds a cache of $c$ items newer than the last crash, this property spreads to every node it exchanges with, like a rumor, after which no cache holds a dead entry. The full proof is below.

The randomness of the overlay is not proved. The analysis of Jelasity, Kowalczyk and van Steen and the later study of Jelasity et al. (2007) are by models and simulation, and the overlay that Newscast builds is measurably not a uniform random graph.

## Complexity

- **Messages.** Each live node starts one exchange per cycle, and each exchange has two messages of at most $c + 1$ items. So a node sends 2 messages per cycle on average, and receives 2 on average, but a node with high in-degree is contacted more often.
- **Local work.** Merging two caches and selecting the $c$ newest items takes $O(c \log c)$ time, or $O(c)$ with selection.
- **Space.** $O(c)$ items per node.
- **Healing.** In the simulation above, after a slow first two cycles the dead entries fall by a factor of 2 to 3 per cycle, and 99.5 percent of them are gone after 10 cycles. The proof below shows that healing spreads from node to node like a rumor, which suggests $O(\log n)$ cycles, but this rate is not proved.

## Properties

- **Self-healing.** Items about crashed nodes only age. The healing is faster than in any protocol that does not prefer fresh items, which is why Jelasity et al. classify Newscast as a *healer*.
- **Uneven in-degree.** A node that has just taken part in many exchanges has fresh items in many caches. The in-degree distribution is much wider than in a random graph, so getPeer is biased toward some nodes.
- **Clustering.** The two caches after an exchange share most of their items, so neighbouring nodes have overlapping views. From a ring start, after 30 cycles of the simulation with $n = 400$ and $c = 10$, about 79 percent of the entries point more than 10 positions away on the ring, against 95 percent for uniform views.
- **Clocks.** Time stamps need loosely synchronized clocks. The framework version replaces them by ages that every node increases by one per cycle, which needs no clock.

## Variants and improvements

- **Age instead of time stamp.** In the framework of Jelasity et al. (2007), an item carries a hop count or age, and view selection keeps the youngest items. With random peer selection, push-pull and $H = c/2$ this is close to Newscast.
- **[Cyclon](/cyclon/).** Swaps instead of copies, and contacts the oldest neighbour, which gives an in-degree close to $c$ and a lower clustering, at the cost of slower healing.
- **Size of the exchange.** Sending only $c/2$ items instead of the whole cache halves the message size with little change in behaviour.

## When to use it

Use Newscast when the network has heavy churn and crashed nodes must disappear from the views fast, and when a moderate bias in the samples is acceptable. It was the peer sampling layer under [gossip aggregation](/gossip-aggregation/) in the work of Jelasity, Montresor and Babaoglu. When an even load across nodes matters more than healing speed, use [Cyclon](/cyclon/).

## Pitfalls

- **Clock skew.** A node whose clock runs ahead creates items that look fresher than all others and stay in caches too long. Use ages instead of absolute time stamps if clocks are not trusted.
- **Malicious nodes.** A node can claim future time stamps or flood fresh items about itself, and take over many caches. Newscast has no defence against this.
- **Bias.** Protocols on top of Newscast that assume uniform samples, such as averaging, can be slower than predicted because some nodes are contacted much more often.
- **Small caches.** With very small $c$ the overlay can split under large failures. Values of $c$ from 20 to 40 were used in the papers.

## Implementations

## History

Newscast was introduced by Jelasity, Kowalczyk and van Steen in a 2003 technical report of the Vrije Universiteit Amsterdam, as the communication layer of an agent based computing system in which news items carried application data. Voulgaris, Jelasity and van Steen described the same protocol in 2003 as a robust peer-to-peer gossiping protocol. Jelasity, Guerraoui, Kermarrec and van Steen (2004) and Jelasity, Voulgaris, Guerraoui, Kermarrec and van Steen (2007) placed it in a generic framework of gossip-based peer sampling, where it is a healer with random peer selection and push-pull propagation.

## References
