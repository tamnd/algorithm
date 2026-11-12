---
tag: PD33TK
kind: problem
slug: overlay-lookup
name: Overlay lookup
aliases:
- DHT lookup
- distributed key lookup
area: systems/networking-algorithms
level: advanced
summary: "Given a key and any node of a peer-to-peer overlay, find the node responsible for the key by messages between nodes, with small routing tables and while nodes join and fail."
prereqs: [consistent-hashing, hash-function, routing-problem]
see_also: [chord, kademlia, hash-ring, compact-routing, kleinberg-small-world-model, de-bruijn-graph, churn, gossip-protocol]
sources:
  - paper: doi:10.1145/383059.383071
    title: Ion Stoica, Robert Morris, David Karger, M. Frans Kaashoek and Hari Balakrishnan, Chord, a scalable peer-to-peer lookup service for Internet applications, ACM SIGCOMM 2001
    locator: pages 149 to 160; Section 2 (the lookup problem in peer-to-peer systems), Section 4 (the protocol and Theorem 2)
  - paper: doi:10.1007/3-540-45748-8_5
    title: Petar Maymounkov and David Mazières, Kademlia, a peer-to-peer information system based on the XOR metric, IPTPS 2002, LNCS 2429
    locator: pages 53 to 65; Section 2 (the XOR metric, k-buckets and the node lookup), Section 3 (the sketch of proof)
  - paper: doi:10.1145/383059.383072
    title: Sylvia Ratnasamy, Paul Francis, Mark Handley, Richard Karp and Scott Shenker, A scalable content-addressable network, ACM SIGCOMM 2001
    locator: pages 161 to 172 (the d-dimensional coordinate space, 2d neighbours per node and the path length)
  - paper: doi:10.1007/3-540-45518-3_18
    title: Antony Rowstron and Peter Druschel, Pastry, scalable, decentralized object location and routing for large-scale peer-to-peer systems, Middleware 2001, LNCS 2218
    locator: pages 329 to 350 (prefix routing with digits of 2^b values, the leaf set and the routing table)
  - paper: doi:10.1007/978-3-540-45172-3_9
    title: M. Frans Kaashoek and David R. Karger, Koorde, a simple degree-optimal distributed hash table, IPTPS 2003, LNCS 2735
    locator: pages 98 to 107 (de Bruijn routing with degree 2 and with degree O(log n))
  - paper: doi:10.1145/571825.571863
    title: David Liben-Nowell, Hari Balakrishnan and David Karger, Analysis of the evolution of peer-to-peer systems, ACM PODC 2002
    locator: pages 233 to 242; Section 3 (the half-life and the lower bound on notifications per half-life)
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, distributed caching protocols for relieving hot spots on the World Wide Web, STOC 1997
    locator: pages 654 to 663 (consistent hashing, which places the keys)
---

Overlay lookup is the central problem of structured peer-to-peer systems, also called distributed hash tables. Many computers form an *overlay*, a network of logical links on top of the Internet, and each data item has a key. A rule maps each key to the node that is *responsible* for it, usually by hashing keys and nodes into one identifier space, as in [consistent hashing](/consistent-hashing/). The task is to find the responsible node from any node, when each node knows only a small part of the membership and nodes join and fail all the time. [Chord](/chord/) and [Kademlia](/kademlia/) solve it in $O(\log n)$ hops with $O(\log n)$ state for $n$ nodes, and a simple counting argument shows that a node with $d$ links cannot do much better than $\log_d n$ hops.

## In plain words

Imagine a phone book split among a million people, with no central office. Each person keeps a few pages, and a fixed rule says which person keeps the page for each name. When you need a number, you must find the person who keeps that page.

You do not know everybody. You only know a few people, and they each know a few others. So you ask someone who is closer to the right person, and that person asks someone closer still, until the message reaches the keeper.

A good design needs few steps and a short contact list for each person, and it keeps working while people join, leave and stop answering.

## Definition

**Identifiers.** A set $I$ of identifiers with a notion of closeness. Common choices are the ring $\mathbb{Z}_{2^m}$, the $b$-bit strings with the XOR distance, and the $d$-dimensional unit torus.

**Placement.** A hash function $h$ maps each key to a point of $I$, and each node $v$ has an identifier $\mathrm{id}(v) \in I$, usually the hash of its address. For a set $N$ of live nodes, a responsibility rule $\mathrm{owner}_N : I \to N$ gives the node responsible for each point: the first node clockwise on a ring (Chord), the node closest by XOR (Kademlia), or the node whose zone contains the point (CAN). The rule should depend only on $N$ and move few points when $N$ changes.

**Routing state.** Each node $v$ keeps a table $\Gamma(v) \subseteq N$ of other nodes it can send messages to. The tables define a directed *overlay graph* on $N$.

**Input.** A key $\kappa$ and a live start node $u$.

**Output.** The node $\mathrm{owner}_N(h(\kappa))$, reached by a sequence of messages $u = v_0, v_1, \ldots, v_\ell$, where each $v_{j+1} \in \Gamma(v_j)$ is chosen from the target and the local state of $v_j$ only. Some systems want the $r$ owners of a key, for example the $r$ closest nodes, for replication.

**Costs.** The *path length* $\ell$ (hops), the *degree* $|\Gamma(v)|$, the messages needed to keep the tables correct while nodes join and fail, and the *balance* of keys and of lookup traffic among nodes.

## Variants

- **One owner or several.** Return the single responsible node, or the $r$ nodes that hold replicas of the key.
- **Iterative or recursive.** In the iterative style the start node contacts each hop itself and learns the next hop from it. In the recursive style each node forwards the request.
- **Static or dynamic.** With a fixed membership the tables can be exact. Under [churn](/churn/), joins and failures happen during lookups, and the design must keep lookups correct with stale tables.
- **Degree and hops.** Constant-degree designs, logarithmic designs, and one-hop designs in which every node knows every other node.
- **Proximity.** Minimize the network delay of a lookup, not only the number of hops, by choosing contacts near in the underlying network.
- **Adversarial nodes.** Some nodes lie or choose their identifiers to take over keys. The lookup must still succeed with high probability.
- **Unstructured search.** If data can be anywhere, with no placement rule, the problem is search, not lookup, and the tools are [flooding](/flooding/) and random walks.

## Examples

**One node set, two rules.** Identifiers are 6-bit numbers (0 to 63), and the nodes are 1, 8, 14, 21, 32, 38, 42, 48, 51 and 56.

| key point | owner by the ring rule (first node at or after the point) | owner by XOR (closest node) | XOR distance of that node |
|---|---|---|---|
| 3 | 8 | 1 | 2 |
| 10 | 14 | 8 | 2 |
| 24 | 32 | 21 | 13 |
| 54 | 56 | 51 | 5 |

The two rules give different owners for the same nodes, so a node set and a rule together define the problem. Under the ring rule, the [Chord](/chord/) lookup for key point 54 from node 8 goes $8 \to 42 \to 51$, and node 51 knows that its successor 56 is the owner. Under the XOR rule, the three closest nodes to 54 are 51, 48 and 56, at distances 5, 6 and 14; a [Kademlia](/kademlia/) node with $k = 3$ stores the key on these three.

**The extremes.** If each node knows only its successor on the ring, a lookup walks up to $n - 1$ hops. If each node knows all others, a lookup takes one hop, but each join or failure must reach all $n$ nodes.

## Known algorithms

| method | identifier space and rule | degree | hops |
|---|---|---|---|
| successor walk | ring, successor | 1 | up to $n - 1$ |
| full membership ([hash ring](/hash-ring/) on each node) | ring, successor | $n - 1$ | 1 |
| [Chord](/chord/) | ring, successor | $O(\log n)$ | $O(\log n)$ w.h.p., about $\frac{1}{2} \log_2 n$ on average |
| [Kademlia](/kademlia/) | bit strings, XOR | $O(k \log n)$ | $O(\log n)$ rounds, $\alpha$ calls in parallel |
| Pastry | digits of $2^b$ values, prefix and numeric closeness | about $(2^b - 1) \log_{2^b} n$ plus a leaf set | about $\log_{2^b} n$ |
| CAN | $d$-dimensional torus, zones | $2d$ | $\frac{d}{4} n^{1/d}$ on average |
| Koorde | ring with [de Bruijn](/de-bruijn-graph/) edges | 2, or $O(\log n)$ | $O(\log n)$, or $O(\log n / \log \log n)$ |

**Chord** places nodes and keys on a ring with [consistent hashing](/consistent-hashing/) and keeps fingers at distances $1, 2, 4, \ldots$; each hop halves the distance. **Kademlia** uses the XOR distance, keeps up to $k$ contacts for each distance range $[2^i, 2^{i+1})$, and queries $\alpha$ nodes at a time. **Pastry** routes by fixing one more digit of the key at each hop. **CAN** splits a $d$-dimensional torus into zones and forwards greedily to the neighbour zone closest to the key. **Koorde** embeds a de Bruijn graph in the Chord ring, so a node shifts one more bit of the key into its position at each hop.

## Bounds

**Degree against hops.** Let every node have at most $d \ge 2$ links. Then some lookup from any start node $u$ needs at least $\lceil \log_d((d - 1) n + 1) \rceil - 1$ hops.

*Proof.* Each node owns at least the point of its own identifier, so a lookup from $u$ must be able to end at each of the $n$ nodes. Within $h$ hops, $u$ reaches at most $1 + d + d^2 + \cdots + d^h = (d^{h+1} - 1)/(d - 1)$ nodes, because each node adds at most $d$ new nodes to the next level. If every node is reachable within $h$ hops, then $(d^{h+1} - 1)/(d - 1) \ge n$, so $d^{h+1} \ge (d - 1) n + 1$ and $h \ge \log_d((d - 1)n + 1) - 1$. $\square$

So degree $O(1)$ forces $\Omega(\log n)$ hops, and degree $O(\log n)$ forces $\Omega(\log n / \log \log n)$ hops. Koorde meets both bounds within a constant factor, and Chord and Kademlia meet the first with a larger degree. For $n = 10^6$, degree 2 needs at least 19 hops in the worst case, and degree 20 at least 5.

**Maintenance under churn.** Liben-Nowell, Balakrishnan and Karger (2002) measure churn by the *half-life*, the time in which half of the nodes are replaced. They show that there is a sequence of joins and leaves under which an $n$-node network that gives each node $o(\log n)$ notifications per half-life falls apart. So keeping an overlay connected costs $\Omega(\log n)$ messages per node per half-life.

**Load.** With one random identifier per node, the largest share of the ring that one node owns is $\Theta(\log n / n)$ with high probability, $\Theta(\log n)$ times the mean. $\Theta(\log n)$ virtual nodes per node bring the largest share down to $O(1/n)$; see [virtual nodes](/virtual-nodes/).

## Reductions

- **From a dictionary.** A distributed [dictionary](/dictionary/) with `put` and `get` reduces to one lookup per operation: find the owner of $h(\kappa)$, then store or read there. Replication to $r$ owners costs $r$ more messages.
- **From key placement to point ownership.** [Consistent hashing](/consistent-hashing/) turns "who stores key $\kappa$" into "who owns the point $h(\kappa)$", so the lookup only routes to a point.
- **To decentralized routing in a graph.** A lookup is greedy routing toward a target with local knowledge. [Kleinberg's small-world model](/kleinberg-small-world-model/) studies the same question on a grid with random long links, and [compact routing](/compact-routing/) studies the trade-off between table size and path length in a given network.
- **Not to gossip.** A [gossip protocol](/gossip-protocol/) spreads a value to all nodes in $O(\log n)$ rounds, but it does not route one request to one node. Overlays use gossip for membership, not for lookups.

## Applications

- **File sharing.** The BitTorrent and eMule networks find peers for a file through a Kademlia-based distributed hash table, with no central tracker.
- **Content-addressed storage.** Systems such as IPFS find the nodes that hold a block from the hash of its content.
- **Key-value stores.** [Dynamo-style](/dynamo-style-replication/) stores place keys with consistent hashing but give each node the full membership, which is the one-hop end of the trade-off.
- **Node discovery.** Block chain clients find peers through a Kademlia-like overlay.
- **Research systems.** Cooperative file systems, multicast and name services were built on Chord, Pastry and CAN.

## References
