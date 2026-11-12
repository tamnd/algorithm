---
tag: 454KX4
kind: algorithm
slug: link-state-routing
name: Link-state routing
aliases:
- link-state protocol
- OSPF-style routing
- shortest path first routing
area: systems/networking-algorithms
level: core
summary: "Each router floods an advertisement of its links, with a sequence number and an age, to all routers. Each then runs Dijkstra on the full map and keeps the first hop of each shortest path."
solves: [routing-problem]
model: asynchronous-model
complexity:
  vars: {n: the number of routers, m: the number of links, D: the hop diameter of the network}
  time: {worst: O(D)}
  messages: {worst: O(n m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1980
  people: [John M. McQuillan, Ira Richer, Eric C. Rosen]
  note: The ARPANET replaced its distance-vector routing with a link-state method in 1979 and 1980 (McQuillan, Richer and Rosen, 1980). OSPF (RFC 2328) and IS-IS (ISO/IEC 10589) are the link-state protocols in use today.
prereqs: [routing-problem, dijkstra, flooding, asynchronous-model]
see_also: [distance-vector-routing, count-to-infinity, path-vector-routing, bgp, hot-potato-routing, shortest-path-tree, ecmp-hashing, ad-hoc-routing]
sources:
  - paper: "John M. McQuillan, Ira Richer and Eric C. Rosen, The new routing algorithm for the ARPANET, IEEE Transactions on Communications 28(5), 1980, pages 711 to 719"
    locator: the description of the updating protocol (flooding with sequence numbers) and of the shortest-path computation at each node
  - paper: "Eric C. Rosen, Vulnerabilities of network control protocols, an example, ACM SIGSOFT Software Engineering Notes 6(1), January 1981"
    locator: the ARPANET collapse of 27 October 1980, the three updates from IMP 50 with sequence numbers 8, 40 and 44 (page numbers not checked)
  - url: https://www.rfc-editor.org/rfc/rfc789
    title: E. C. Rosen, Vulnerabilities of Network Control Protocols, An Example, RFC 789, July 1981
    locator: the same report as an RFC, with the rule for comparing 6-bit sequence numbers
  - url: https://www.rfc-editor.org/rfc/rfc2328
    title: J. Moy, OSPF Version 2, RFC 2328, April 1998
    locator: Section 12.1.6 (LS sequence number), Section 13 (the flooding procedure), Section 13.1 (which LSA is newer), Section 16.1 (the shortest-path tree, with the check for a link back), Appendix B (MaxAge and LSRefreshTime)
  - url: https://www.rfc-editor.org/rfc/rfc1142
    title: D. Oran (editor), OSI IS-IS Intra-domain Routing Protocol, RFC 1142, February 1990
    locator: the republication of the ISO/IEC 10589 draft; the update process (flooding of link state PDUs) and the decision process
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition, Pearson, 2021
    locator: Chapter 5, Section 5.2.1 (the link-state routing algorithm) and Section 5.3 (OSPF)
  - book: isbn:9780201634488
    title: Radia Perlman, Interconnections, Bridges, Routers, Switches, and Internetworking Protocols, second edition, Addison-Wesley, 2000
    locator: the chapters on link-state routing and on the robust flooding of link-state packets (chapter numbers not checked)
---

Link-state routing is the routing method in which every router learns the whole map of the network and computes its routes itself. Each router describes its own links, with their costs, in a small message called a link-state advertisement (LSA), and sends it by reliable flooding to every other router. Each router keeps the newest LSA of every router in a database, builds the graph from it, and runs [Dijkstra's algorithm](/dijkstra/) from itself. The forwarding table keeps the first hop of each shortest path. It solves the [routing problem](/routing-problem/) inside one network. Unlike [distance-vector routing](/distance-vector-routing/), it reuses no other router's cost, so it has no [count to infinity](/count-to-infinity/). After the last change, it converges in about the time of one flood plus one Dijkstra run. OSPF and IS-IS work in this way.

## In plain words

Every router makes a short note: "I am router B, this is my note number 7, and I have links to A with cost 2, to C with cost 1 and to D with cost 4." It gives the note to all its neighbours. They pass it on to their neighbours, and so on, until every router has a copy. Each router keeps only the note with the highest number from each other router, so an old note can never replace a new one.

When a router has the notes of all routers, it can draw the whole map. It then finds the shortest way from itself to every other router, and for each destination it remembers only the first step. When a link breaks, the two routers at its ends write new notes, and everyone draws the map again.

## The problem

The network is an undirected graph $G = (V, E)$ of $n$ routers and $m$ links, with a cost $w(u, v) > 0$ on each link. Links fail, recover and change cost. Messages on a link can be lost. The output at each router $x$ is a next hop $\mathrm{next}[x][t]$ for every router $t$ that it can reach. The goal is that, a short time after the last change, following the next hops from any $s$ leads to any reachable $t$ along a shortest path, with no loop. This must hold for all pairs at the same time, although every router computes its own table.

## The algorithm

An LSA $A$ has four fields: the origin router, a sequence number, an age, and the list of the origin's working links with their costs. Router $y$ keeps a database $\mathrm{DB}[y]$ with the newest LSA of each origin.

```pseudo id=main
LS-ROUTER(y)                       ▷ event handlers of router y
L1  on START or a change of a local link: seq ← seq + 1;  A ← (y, seq, age 0, the working links of y)
L2      INSTALL(y, A);  FLOOD(y, A, nil)
L3  on RECEIVE LSA A from neighbour x: send ACK(A) to x
L4      cur ← DB[y][A.origin]
L5      if cur = nil or A.seq is newer than cur.seq then INSTALL(y, A);  FLOOD(y, A, x)
L6      else if cur.seq is newer than A.seq then send cur to x      ▷ x has an old copy

FLOOD(y, A, from)
L7  for each neighbour z ≠ from: send A to z with age + 1, and keep A in the list of z until z acknowledges it
L8  on RETRANSMIT timer for (z, A): if A is still in the list of z then send A to z again

INSTALL(y, A)
L9  DB[y][A.origin] ← A
L10 G ← the graph of the links (u, v) that both u and v list in DB[y]
L11 run Dijkstra from y on G;  next[y][t] ← the first hop of the path to t

L12 on AGE timer: delete each LSA whose age reached MAXAGE, and recompute
```

**Reliable flooding.** Lines L3 to L8 are the [flooding](/flooding/) broadcast with three additions. First, acknowledgements and retransmission make delivery reliable over lossy links. Second, the sequence number lets a router tell a new LSA from an old copy, so it forwards each LSA once and drops repeats; plain flooding only drops repeats of the same message, while here a newer LSA replaces an older one from the same origin. Third, the age removes the LSA of a router that has died or been cut off: each router counts the age up, and an LSA that reaches MAXAGE is deleted. OSPF uses a MaxAge of one hour, and each router floods a fresh copy of its own LSA every 30 minutes (RFC 2328, Appendix B). Line L6 repairs a neighbour that has an old copy, for example after it restarts.

**The two-way check.** Line L10 uses a link only if both ends report it. This keeps out a link that one end has stopped using, even while a stale LSA from the other end still lists it. OSPF does the same when it builds its tree (RFC 2328, Section 16.1).

**Sequence numbers.** The numbers must be compared so that "newer" is a total order on the numbers in use. OSPF uses a linear space of 32-bit signed numbers (RFC 2328, Sections 12.1.6 and 13.1). When a router finds a copy of its own LSA with a higher number than its own counter, for example after a restart, it jumps past that number and floods a new LSA.

## Example

Five routers, with links $A - B$ cost 2, $A - C$ cost 4, $B - C$ cost 1, $B - D$ cost 4, $C - D$ cost 1, $C - E$ cost 7 and $D - E$ cost 3. After the first flood every router holds the same five LSAs:

| origin | links in its LSA |
|---|---|
| A | B 2, C 4 |
| B | A 2, C 1, D 4 |
| C | A 4, B 1, D 1, E 7 |
| D | B 4, C 1, E 3 |
| E | C 7, D 3 |

Dijkstra at $A$ settles the routers in the order $A$ 0, $B$ 2, $C$ 3 (through $B$), $D$ 4 (through $B$ and $C$), $E$ 7 (through $D$). So every route of $A$ starts at $B$.

Now link $B - C$ fails. $B$ and $C$ each flood a new LSA with a higher sequence number and without that link. When the new LSAs arrive at $A$, it runs Dijkstra again: $B$ 2 through $B$, $C$ 4 direct, $D$ 5 through $C$, $E$ 8 through $C$. Router $B$ computes $D$ 4 direct and $C$ 5 through $D$. No router reuses an old cost, so there is no counting. While the flood is under way, a router with the old map and a router with the new map can disagree, but this lasts only until the new LSAs arrive.

## Correctness

The proof assumes that the topology stops changing, that a message sent again and again over a working link eventually arrives, that sequence numbers are compared as integers and that no LSA ages out during the flood. It has four steps.

1. No copy of an LSA of $o$ is newer than the last LSA $L_o$ that $o$ originates, so a router that installs $L_o$ keeps it.
2. By induction on the hop distance from $o$, every router in the component of $o$ installs $L_o$: a neighbour that installs it keeps sending it until it is acknowledged.
3. Each router floods each LSA once, so the flood ends.
4. With the two-way check, the graph that each router builds equals its component with the true costs.

Dijkstra then gives every router the true distances $\delta$. Next hops are loop-free for all pairs even if routers break ties differently: the next hop $h$ of $x$ toward $t$ satisfies $\delta(x, t) = w(x, h) + \delta(h, t)$, so $\delta(\cdot, t)$ falls strictly along the walk, and the walk ends at $t$ with cost $\delta(x, t)$. The full proof is in [the correctness proof](#proof-correctness).

The first step fails if sequence numbers wrap around and are compared circularly, and this is not only a theory problem: it brought down the ARPANET in 1980 (see History).

## Complexity

- **Messages.** One LSA crosses each link at most once in each direction, plus one acknowledgement each time, so one flood costs $O(m)$ messages when no message is lost. A cold start floods all $n$ LSAs, $O(nm)$ messages in all. A change of one link floods two LSAs, $O(m)$ messages.
- **Time.** A flood reaches every router after at most $D$ message delays, where $D$ is the hop diameter, plus retransmission delays on lossy links. Each router then runs Dijkstra in $O(m + n \log n)$ time with a Fibonacci heap, or $O((n + m) \log n)$ with a [binary heap](/binary-heap/).
- **Space.** Each router stores the whole map: $O(n + m)$ entries.

| measure | bound | case |
|---|---|---|
| message delays per flood | $O(D)$ | no loss |
| messages per change | $O(m)$ | worst case |
| messages at a cold start | $O(nm)$ | worst case |
| local work per change | $O((n + m) \log n)$ | binary heap |
| database size | $O(n + m)$ | per router |

Compare [distance-vector routing](/distance-vector-routing/), whose bad news needs up to $\lceil I/c \rceil + n - 1$ rounds, and whose routers store only $O(n d)$ values.

## Properties

- **No count to infinity.** A router computes from first-hand reports only. A failure is known everywhere after one flood.
- **Consistent when the databases agree.** If all routers hold the same map, the next hops of all routers together form loop-free shortest paths, whatever the tie-breaks.
- **Transient loops.** During a flood, routers with different maps can forward a packet back and forth. These micro-loops last about one flood time.
- **Global knowledge.** Every router knows the full topology. This helps traffic engineering and debugging, but it costs memory and flooding traffic that grow with the network.
- **Each router decides alone.** No router depends on another router's computation, only on its LSA. A router with a bad Dijkstra implementation hurts only its own routes, though a router that floods false LSAs hurts everyone.

## Variants and improvements

- **Areas and levels.** OSPF splits a large network into areas joined by a backbone, and IS-IS has two levels. Routers flood full LSAs only within their area and receive summaries of other areas.
- **Designated routers.** On a broadcast LAN, OSPF elects a designated router that floods on behalf of the LAN, so the LAN appears as a single node instead of a full mesh.
- **Equal-cost multipath.** Keep all first hops on shortest paths and spread flows among them; see [ECMP hashing](/ecmp-hashing/).
- **Incremental shortest paths.** After a small change, update the tree instead of running Dijkstra from scratch.
- **Fast reroute.** Precompute a loop-free alternate next hop for each destination, so that a router can move traffic at once when a link fails, before the flood ends.
- **Ad hoc networks.** OLSR reduces flooding with multipoint relays, a subset of neighbours that forward the LSAs; see [ad hoc routing](/ad-hoc-routing/).

## When to use it

Link-state routing is the usual choice inside one administrative domain, such as an ISP backbone, a campus or a data centre, where all routers trust each other and agree on one cost metric. It converges fast and lets operators see the whole topology. Between domains, where each network has its own policy and will not publish its internal map, the Internet uses [path-vector routing](/path-vector-routing/) with [BGP](/bgp/). On small or simple networks, [distance-vector routing](/distance-vector-routing/) needs less memory and configuration.

## Pitfalls

- **Circular sequence numbers.** If numbers wrap around and are compared modulo the space, three numbers can each look newer than another, and the flood never ends. Use a linear space, as OSPF does, with a rule for the end of the space.
- **No two-way check.** Without line L10's test, a stale LSA of a router that has lost a link can still draw that link into the graph, and routers can send traffic into a dead link.
- **Old LSAs of a restarted router.** After a restart, a router starts its counter again, and its new LSAs look older than the copies still in the network. The router must accept its own old LSA and jump past its number (line L5).
- **Flood storms.** A link that goes up and down often makes the routers flood and run Dijkstra again and again. Protocols set a minimum time between two LSAs from one router and between two Dijkstra runs.
- **Different metrics.** All routers must use the same costs. If two routers compute on different maps for a long time, for example because one ignores some LSAs, loops can last.

## Implementations

The Python code is a discrete-event simulation of reliable flooding with sequence numbers, ages, acknowledgements, retransmission over lossy links, and a Dijkstra run after each change. The tests compare the tables with true shortest-path distances on seeded random graphs with lost messages, follow the next hops for every pair of routers to check that they are loop-free and consistent, and repeat this after link failures and cost changes. They also replay the three sequence numbers of the 1980 ARPANET incident: the flood ends with linear comparison, and it never ends with circular comparison.

## History

From 1969 the ARPANET used a distributed Bellman-Ford method, which reacted slowly to bad news. In 1979 and 1980 it moved to a new method, described by McQuillan, Richer and Rosen in 1980: each node measured the delay on its lines, flooded the measurements to all nodes with sequence numbers, and ran a shortest-path computation. On 27 October 1980, a faulty node, IMP 50, put three updates with sequence numbers 8, 40 and 44 into the network. In the 6-bit circular space, each was newer than another, so every node kept replacing one with the next and flooding it again. The updates filled the network, and it had to be restarted by hand. Rosen's report of 1981 (also RFC 789) is a classic case study.

Radia Perlman designed robust flooding with a lollipop-shaped sequence space for the routing of DECnet, and this work led to IS-IS, standardized as ISO/IEC 10589 and published for the Internet as RFC 1142 in 1990. John Moy designed OSPF for the IETF. OSPF version 2 is RFC 2328 of April 1998, and it uses a linear sequence space with an age field.

## References
