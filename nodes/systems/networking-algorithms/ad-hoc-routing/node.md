---
tag: VWPZYN
kind: problem
slug: ad-hoc-routing
name: Ad hoc routing
aliases:
- mobile ad hoc routing
- MANET routing
area: systems/networking-algorithms
level: advanced
summary: "Route packets over many wireless hops in a network with no fixed routers, where links appear and break as nodes move. Keep routes loop-free while spending little radio time on control traffic."
prereqs: [routing-problem, flooding, random-geometric-graph]
see_also: [aodv, geographic-routing, gpsr, distance-vector-routing, link-state-routing, count-to-infinity, broadcast-problem, csma-ca]
sources:
  - paper: doi:10.1145/190314.190336
    title: "Charles E. Perkins and Pravin Bhagwat, Highly dynamic destination-sequenced distance-vector routing (DSDV) for mobile computers, ACM SIGCOMM 1994"
    locator: pages 234 to 244 (destination sequence numbers, loop freedom and settling times)
  - paper: doi:10.1109/MCSA.1999.749281
    title: "Charles E. Perkins and Elizabeth M. Royer, Ad-hoc on-demand distance vector routing, Second IEEE Workshop on Mobile Computing Systems and Applications (WMCSA), 1999"
    locator: pages 90 to 100 (route discovery on demand with sequence numbers)
  - paper: "David B. Johnson and David A. Maltz, Dynamic source routing in ad hoc wireless networks, in Mobile Computing, T. Imielinski and H. Korth (eds.), Kluwer, 1996"
    locator: Chapter 5, pages 153 to 181 (route discovery, source routes and the route cache)
  - url: "https://www.rfc-editor.org/rfc/rfc3626"
    title: "T. Clausen and P. Jacquet (eds.), RFC 3626, Optimized Link State Routing Protocol (OLSR), 2003"
    locator: Sections 3 and 8 (multipoint relays and their selection)
  - url: "https://www.rfc-editor.org/rfc/rfc4728"
    title: "D. Johnson, Y. Hu and D. Maltz, RFC 4728, The Dynamic Source Routing Protocol (DSR) for Mobile Ad Hoc Networks for IPv4, 2007"
    locator: Sections 3 and 4 (route discovery and route maintenance)
  - paper: "Eli M. Gafni and Dimitri P. Bertsekas, Distributed algorithms for generating loop-free routes in networks with frequently changing topology, IEEE Transactions on Communications 29(1), 1981"
    locator: the full and partial link reversal algorithms
  - paper: doi:10.1109/18.825799
    title: "Piyush Gupta and P. R. Kumar, The capacity of wireless networks, IEEE Transactions on Information Theory 46(2), 2000"
    locator: pages 388 to 404 (throughput per node of order 1/sqrt(n log n) for random networks)
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition, Pearson, 2011
    locator: Chapter 5, Section 5.2 (routing in ad hoc networks, with AODV as the example)
---

Ad hoc routing is the [routing problem](/routing-problem/) for a wireless network with no fixed infrastructure. Every node is both a host and a router, two nodes can talk directly only when they are within radio range, and the nodes move, so the graph of usable links changes all the time. A protocol must find multihop paths, keep them loop-free while they change, and repair them after breaks, and it pays for every control message in shared radio time and battery. The main designs are *proactive* protocols, which keep routes to all nodes at all times (DSDV, OLSR), *reactive* protocols, which search for a route only when a packet needs one ([AODV](/aodv/), DSR), and [geographic](/geographic-routing/) protocols, which route by node positions ([GPSR](/gpsr/)).

## In plain words

Picture hikers with walkie-talkies spread over a valley. Each one can reach only those close by, and a message to someone far away has to be passed from hiker to hiker. Nobody has a map of who is near whom, and people keep walking, so a chain that worked a minute ago may be broken now. Ad hoc routing asks how the hikers can find such chains, fix them when they break, and avoid passing a message around in a circle, while talking as little as possible about the chains themselves, because every word of talk uses up the same radio channel the messages need.

## Definition

**Network.** A set $V$ of $n$ nodes. At time $t$ node $u$ has a position $p_u(t)$, and the *link graph* $G_t$ joins $u$ and $v$ when they can communicate, in the simplest model when $|p_u(t) - p_v(t)| \le r$ for a common range $r$: a unit disk graph, and a [random geometric graph](/random-geometric-graph/) when positions are random. Links are usually assumed symmetric; real radios also have one-way and lossy links. Nodes learn of their links only by hearing neighbors, through periodic hello messages or failed link-layer acknowledgements.

**Task.** Packets arise at sources for destinations. A protocol keeps, at each node, forwarding state that maps a packet to a next hop, and it exchanges control messages over the radio links. At every time the forwarding state should contain no loop, and a packet whose source and destination are connected in $G_t$ long enough should reach the destination.

**Measures.**

- the *delivery ratio*, the fraction of data packets delivered;
- the *control overhead*, the number of control messages or bytes per unit time or per delivered packet;
- the *route acquisition latency*, the delay before the first packet of a new flow can go;
- the *path stretch*, the hop count of the used path over the shortest one;
- the *state* per node.

No protocol wins on all of them; the trade-off depends on how fast nodes move and how much traffic there is.

## Variants

- **Proactive, or table driven.** Every node keeps a route to every destination, updated as links change, as in wired [distance vector](/distance-vector-routing/) and [link state](/link-state-routing/) routing. DSDV adds destination sequence numbers to distance vectors to avoid loops and [counting to infinity](/count-to-infinity/). OLSR is a link state protocol that floods topology updates only through *multipoint relays*, a subset of neighbors that covers all two-hop neighbors. Routes are ready at once, but the updates cost radio time even for destinations nobody uses.
- **Reactive, or on demand.** A source [floods](/flooding/) a route request when it needs a route, and the destination or a node with a fresh route answers. DSR returns the whole path and puts it in each packet header; [AODV](/aodv/) keeps next-hop tables with destination sequence numbers. Overhead follows traffic, but the first packet waits for the search, and every search is a network-wide [broadcast](/broadcast-problem/).
- **Hybrid.** Proactive inside a small zone around each node and reactive beyond it, as in the zone routing protocol.
- **Link reversal.** Gafni and Bertsekas orient the links of a graph toward the destination and reverse links at nodes that lose all outgoing links; TORA builds on this.
- **Geographic.** When nodes know their positions and the destination's position, a node forwards to a neighbor closer to the destination, with a fallback for dead ends. No routes are kept at all: see [geographic routing](/geographic-routing/) and [GPSR](/gpsr/).
- **Delay tolerant.** When no end-to-end path exists at any one time, nodes store packets and carry them until they meet the next relay.

## Examples

- **A line that breaks.** Nodes $1 - 2 - 3 - 4 - 5$ in a row, each in range of its neighbors only. Node $1$ needs a route to $5$. A reactive protocol floods a request; it reaches $5$ after $4$ hops, every node rebroadcasts it once, and the reply follows the reverse path. If node $4$ walks away, node $3$ detects the broken link, tells the nodes that used it, and the source searches again.
- **A stale loop.** Plain distance vectors on the same line can loop after the break: $3$ hears from $2$ an old distance to $5$ that passes through $3$ itself. Destination sequence numbers, as in DSDV and AODV, make $3$ reject the stale route because it is not newer than the one that just broke.
- **Many flows to a few nodes.** In a sensor network where all data goes to one sink, a single tree to the sink, maintained proactively, beats a search per flow.

## Known algorithms

| protocol | year | class | main idea |
|---|---|---|---|
| link reversal (Gafni, Bertsekas) | 1981 | proactive per destination | reverse links to keep a destination-oriented DAG |
| DSDV | 1994 | proactive | distance vectors with destination sequence numbers |
| DSR | 1996 | reactive | flooded route requests, source routes in headers, route caches |
| [AODV](/aodv/) | 1999 | reactive | flooded requests, next-hop tables, destination sequence numbers |
| [GPSR](/gpsr/) | 2000 | geographic | greedy forwarding plus face routing on a planar subgraph |
| OLSR | 2003 | proactive | link state flooded through multipoint relays |

## Bounds

- **Search cost.** A flooded route request on a connected graph with $n$ nodes and $m$ links is sent once by each node, $n$ broadcasts, and received about $2m$ times. A reactive protocol pays this per discovery; expanding ring searches lower it when the destination is near.
- **Proactive cost.** A proactive protocol must react to every link change anywhere, so its overhead grows with the rate of change times the cost of spreading one update.
- **Connectivity.** In a random geometric graph of $n$ uniform nodes in a unit square, the network is connected with high probability when the range $r$ satisfies $\pi r^2 = (\log n + c_n)/n$ with $c_n \to \infty$, and disconnected when $c_n \to -\infty$ (Gupta and Kumar, 1998). Below this range, no protocol can deliver between all pairs.
- **Capacity.** Gupta and Kumar (2000) showed that with $n$ random nodes sharing one channel, each node can get throughput of order only $1/\sqrt{n \log n}$ of the channel rate, because every packet uses many hops and each hop blocks the area around it. Routing cannot beat this scaling; it can only waste less.

## Reductions

- **To shortest paths on a changing graph.** With hop counts as costs, a protocol is a distributed and incremental way to keep [shortest paths](/shortest-path/) in $G_t$; DSDV and AODV are [distributed Bellman-Ford](/distributed-bellman-ford/) with sequence numbers.
- **Route discovery is broadcast.** Each request is an instance of the [broadcast problem](/broadcast-problem/), solved by [flooding](/flooding/) or by flooding through a connected dominating set, which is what multipoint relays approximate.
- **Geographic routing needs planar graphs.** Face routing is guaranteed to deliver only on a planar connected subgraph of the unit disk graph, such as the Gabriel graph; see [geographic routing](/geographic-routing/).

## Applications

Military and tactical radio networks, disaster relief and search and rescue, vehicular networks, community and building mesh networks, and wireless sensor networks. IEEE 802.11s mesh networking uses HWMP, a path selection protocol based on AODV, and Zigbee uses a routing scheme derived from AODV. Smartphone mesh apps and drone swarms use reactive or geographic schemes for the same reasons.

## References
