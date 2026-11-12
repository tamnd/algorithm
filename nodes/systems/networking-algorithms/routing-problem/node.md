---
tag: 5ATKEV
kind: problem
slug: routing-problem
name: Routing problem
aliases:
- network routing
- packet routing
area: systems/networking-algorithms
level: intro
summary: "Choose, for each source and destination in a network, a path for packets, and set up the forwarding state that sends each packet along it with no loops. The paths should be short or obey a policy."
prereqs: [graph, weighted-graph, shortest-path]
see_also: [distance-vector-routing, link-state-routing, path-vector-routing, compact-routing, multicast-routing, maximum-throughput-routing, oblivious-routing, all-pairs-shortest-paths]
sources:
  - book: isbn:9780132009164
    title: Dimitri Bertsekas and Robert Gallager, Data Networks, second edition, Prentice Hall, 1992
    locator: Chapter 5, Routing in data networks (the routing problem, its performance measures, and shortest-path and optimal routing; section numbers not checked)
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition, Pearson, 2021
    locator: Chapter 4, Section 4.1 (forwarding and routing, the data plane and the control plane) and Chapter 5, Sections 5.1 to 5.4 (routing algorithms, intra-AS and inter-AS routing)
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition, Morgan Kaufmann, 2011
    locator: Chapter 3, Section 3.3 (routing, forwarding against routing, the network as a graph)
  - paper: "David Peleg and Eli Upfal, A trade-off between space and efficiency for routing tables, Journal of the ACM 36(3), 1989, pages 510 to 530"
    locator: the definition of a routing scheme by local tables and the trade-off between stretch and table size
  - paper: "Frank Thomson Leighton, Bruce M. Maggs and Satish B. Rao, Packet routing and job-shop scheduling in O(congestion + dilation) steps, Combinatorica 14(2), 1994, pages 167 to 186"
    locator: the main theorem, a schedule of length O(C + D) for packets on fixed paths
---

The routing problem asks how to get packets from their sources to their destinations through a network of links and routers. A solution has two parts. The control part chooses the paths: shortest by some metric, or the best under an operator's policy. The forwarding part is the state at each router that sends each packet one step along its path. Forwarding must be consistent: the next hops of the routers, put together, must not send a packet around a loop. The paths must be found again when links fail or change. The same graph question appears in many settings, from the Internet to the interconnection network of a parallel computer.

## In plain words

Think of a country of towns and roads. A letter must go from any town to any other town. No town has a map of the whole country, but each town can talk to its neighbours. Each town needs a signpost that says, for every destination, which road to take next.

The signposts must agree with each other. If town A points to B for the capital, and B points back to A, the letter goes back and forth for ever. The routes should also be good: short, cheap, or allowed by the rules of the regions they cross. When a road closes, the signposts must change quickly, and they must not point in circles while they change.

## Definition

**Input.** A graph $G = (V, E)$ of routers and links, directed or undirected, with a metric on each link: a cost $w(e) > 0$, such as 1 per hop, a delay, or a value derived from bandwidth. The graph and the metric can change over time. The input can also include a policy that says which paths each router accepts and which it prefers.

**Forwarding state.** In **hop-by-hop routing**, each router $x$ holds a table $f_x$ that maps each destination $t$ to a next hop $f_x(t)$, a neighbour of $x$, or to "drop". A packet for $t$ at $x$ goes to $f_x(t)$. In **source routing**, the source writes the whole path into the packet header, and the routers only follow it.

**Consistency.** A hop-by-hop state is loop-free for destination $t$ if no walk $x, f_x(t), f_{f_x(t)}(t), \dots$ visits a router twice. Then every walk from a router that does not drop ends at $t$. Equivalently, the edges $(x, f_x(t))$ form an [arborescence](/arborescence/) (an in-tree) directed toward $t$. This must hold for every $t$ at once.

**Goal.** Shortest-path routing asks for each $f_x(t)$ to be the first link of a shortest path from $x$ to $t$, so that each in-tree is a [shortest path tree](/shortest-path-tree/). Any choice of first links on shortest paths is loop-free, because the distance to $t$ falls at each hop. Other goals use other metrics: the widest path, the least delay under load, or the most preferred path under a policy. A dynamic routing protocol must also return to a consistent state after each change.

**Destination-based forwarding limits the paths.** A table indexed by destination alone sends all packets for $t$ that reach $x$ along the same suffix. So the set of chosen paths must be suffix-closed: if the path from $s$ to $t$ passes $x$, its part from $x$ is the path from $x$ to $t$. Shortest paths with one fixed choice for each pair have this property. Paths chosen by policy need not have it.

## Variants

- **Static or dynamic.** Static routes are set by hand or computed once. Dynamic routing runs a distributed protocol that recomputes routes after failures and changes of cost.
- **Intra-domain or inter-domain.** Inside one autonomous system (AS), one operator sets one metric and all routers cooperate: [distance-vector routing](/distance-vector-routing/) (RIP) or [link-state routing](/link-state-routing/) (OSPF, IS-IS). Between ASes, each AS applies its own policy and does not publish its internal map. The Internet uses [path-vector routing](/path-vector-routing/) with [BGP](/bgp/) there. The exit from one AS into the next is often chosen by [hot-potato routing](/hot-potato-routing/).
- **Hop-by-hop or source routing.** Hop-by-hop routing needs a table at each router and suffix-closed paths. Source routing allows any path, at the cost of a larger header and of a source that must know the paths.
- **Unicast, multicast and broadcast.** One destination, a group of destinations ([multicast routing](/multicast-routing/)), or all nodes ([broadcast](/broadcast-problem/)).
- **Compact routing.** Bound the size of the tables and the headers, and allow paths up to a factor (the stretch) longer than shortest; see [compact routing](/compact-routing/).
- **Routing for throughput.** Choose paths, or split traffic over several paths, to carry the most traffic or keep the most loaded link light: [maximum-throughput routing](/maximum-throughput-routing/), [oblivious routing](/oblivious-routing/), [Valiant routing](/valiant-routing/) and [backpressure routing](/backpressure-routing/).
- **Packet routing on fixed networks.** In the interconnection network of a parallel machine, route a set of packets (often a permutation) on a mesh, hypercube or butterfly: [permutation routing](/permutation-routing/) and [dimension-order routing](/dimension-order-routing/).
- **Networks without fixed structure.** Mobile ad hoc networks ([ad hoc routing](/ad-hoc-routing/), [AODV](/aodv/)) and position-based methods ([geographic routing](/geographic-routing/)). Overlay networks route lookups by key, as in [Chord](/chord/) and [Kademlia](/kademlia/).
- **Layer 2.** Ethernet bridges do not route; they forward on one tree that the [Spanning Tree Protocol](/spanning-tree-protocol/) builds, so that frames never loop.

## Examples

**Shortest paths with hop count.** In a ring of six routers $0, \dots, 5$ with cost 1 on each link, router 0 sends packets for 1 and 2 clockwise and for 4 and 5 counterclockwise. For 3, both ways cost 3, and router 0 may choose either; say it sends to 1. Router 1 is at distance 2 from 3, and its only shortest path goes on to 2. If router 1 sent packets for 3 back to 0, which is not on a shortest path from 1, the two routers would form a loop. So the rule is: each router picks a first link on one of its own shortest paths. Then the distance to 3 falls at every hop, and no loop is possible, whatever the ties.

**An inconsistent state.** In a line $A - B - C$, if $f_A(C) = B$ and $f_B(C) = A$, a packet for $C$ goes back and forth until its time-to-live runs out. This is the state that [distance-vector routing](/distance-vector-routing/) can reach for a time after link $B - C$ fails; see [count to infinity](/count-to-infinity/).

**A path that hop-by-hop forwarding cannot express.** Let $s_1$ and $s_2$ both reach $t$ through $x$, and let a policy require $s_1$'s packets to leave $x$ on link $a$ and $s_2$'s packets on link $b$. A table at $x$ indexed only by $t$ cannot do this. Source routing, a table indexed by source and destination, or a tunnel can.

## Known algorithms

| method | where it is used | what it computes | page |
|---|---|---|---|
| distance vector | RIP, small networks | shortest paths by distributed Bellman-Ford | [distance-vector routing](/distance-vector-routing/) |
| link state | OSPF, IS-IS | the full map by flooding, then Dijkstra at each router | [link-state routing](/link-state-routing/) |
| path vector | BGP between ASes | policy-preferred paths, with the whole path in each route | [path-vector routing](/path-vector-routing/), [BGP](/bgp/) |
| nearest egress | ISP backbones | the exit with the least internal cost | [hot-potato routing](/hot-potato-routing/) |
| spanning tree | Ethernet bridges | one shortest-path tree to a root bridge | [Spanning Tree Protocol](/spanning-tree-protocol/) |
| compact schemes | theory, large graphs | stretch 3 with tables of about $\sqrt{n}$ entries | [compact routing](/compact-routing/) |
| on-demand discovery | mobile ad hoc networks | routes found when needed, by flooding a request | [AODV](/aodv/) |
| greedy by position | sensor and wireless networks | the neighbour closest to the destination | [GPSR](/gpsr/) |
| randomized two-phase | interconnection networks | a random intermediate node to spread load | [Valiant routing](/valiant-routing/) |

The table lookup itself, from a destination address to a next hop, is a separate problem; in IP it is [longest prefix match](/longest-prefix-match/).

## Bounds

- **Shortest paths.** A centralized computation of all next hops is the [all-pairs shortest paths](/all-pairs-shortest-paths/) problem, one [single-source](/single-source-shortest-paths/) run per destination (or per source, on an undirected graph). The distributed protocols need about $n$ rounds or one network-wide flood after a change.
- **Table size against stretch.** Shortest-path routing can need tables of $\Theta(n)$ entries at a router. Peleg and Upfal (1989) showed a trade-off: a smaller total table size forces longer paths. Gavoille and Gengler showed that any scheme with stretch below 3 needs $\Omega(n)$ bits at some router of some graph. Thorup and Zwick reached stretch 3 with tables of $\tilde{O}(\sqrt{n})$ words. See [compact routing](/compact-routing/).
- **Packet scheduling.** When each packet has a fixed path, let $C$ be the largest number of paths that use one link (the congestion) and $D$ the longest path (the dilation). Any schedule needs at least $\max(C, D)$ steps, and Leighton, Maggs and Rao (1994) showed that a schedule of $O(C + D)$ steps always exists.
- **Policy routing.** With arbitrary preferences, a stable choice of paths may not exist, and deciding whether one exists is NP-complete (Griffin, Shepherd and Wilfong); see [path-vector routing](/path-vector-routing/).

## Reductions

- **Hop-by-hop shortest-path routing reduces to shortest paths.** For each destination $t$, compute a [shortest path tree](/shortest-path-tree/) toward $t$ and set $f_x(t)$ to the parent of $x$. Distance-vector routing does this for all $t$ at once with [distributed Bellman-Ford](/distributed-bellman-ford/), and link-state routing does it with one [Dijkstra](/dijkstra/) run per router.
- **Loop-freedom reduces to a potential.** If some function $\phi_t$ falls strictly at every hop toward $t$, the state is loop-free. The distance to $t$ is such a function. DUAL's feasibility condition, AODV's sequence numbers and the AS path check of path vector are other ways to keep such a potential during changes.
- **Minimum-cost multicast reduces to Steiner trees.** A cheapest tree that joins a source to a set of receivers is a [Steiner tree](/steiner-tree-problem/), which is NP-hard; see [multicast routing](/multicast-routing/).
- **Routing tables and distance labels.** A routing scheme with short labels is close to a [distance labeling](/distance-labeling/) or a [distance oracle](/distance-oracle/): the Thorup-Zwick routing scheme uses the same landmarks and clusters as the [Thorup-Zwick oracle](/thorup-zwick-oracle/).

## Applications

- **The Internet.** Routers inside each AS run OSPF, IS-IS or RIP. The border routers run BGP between ASes.
- **Data centres.** Fabrics of many equal paths use link-state routing or BGP with [ECMP hashing](/ecmp-hashing/) to spread flows.
- **Local networks.** Ethernet uses the [Spanning Tree Protocol](/spanning-tree-protocol/) to forward on one tree.
- **Parallel computers and chips.** Networks on chips and supercomputer interconnects use [dimension-order routing](/dimension-order-routing/), [wormhole routing](/wormhole-routing/) and [Valiant routing](/valiant-routing/).
- **Wireless and mobile networks.** [Ad hoc routing](/ad-hoc-routing/) and [geographic routing](/geographic-routing/).

## References
