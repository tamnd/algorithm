---
tag: 8QEP75
kind: algorithm
slug: gpsr
name: GPSR
aliases:
- greedy perimeter stateless routing
area: systems/networking-algorithms
level: advanced
summary: "Geographic routing that sends each packet to the neighbor closest to the destination and, at a dead end, walks the faces of a local planar subgraph by the right-hand rule."
solves: [geographic-routing]
model: asynchronous-model
complexity:
  vars: {n: the number of nodes, d: the number of neighbors of a node}
  time: {worst: O(d^2), expected: O(d)}
  space: {extra: O(d)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2000
  people: [Brad Karp, H. T. Kung]
  note: Karp and Kung presented GPSR at MobiCom 2000. Its perimeter mode is face routing on a planar subgraph, which Bose, Morin, Stojmenovic and Urrutia had proved to deliver in 1999.
prereqs: [geographic-routing, gabriel-graph, relative-neighborhood-graph, planar-face]
see_also: [aodv, ad-hoc-routing, planar-graph, orientation-test, segment-intersection-detection, random-geometric-graph]
sources:
  - paper: doi:10.1145/345910.345953
    title: "Brad Karp and H. T. Kung, GPSR: greedy perimeter stateless routing for wireless networks, ACM MobiCom 2000"
    locator: pages 243 to 254 (greedy forwarding, the right-hand rule, planarization by GG and RNG, the perimeter mode header and face changes)
  - paper: doi:10.1023/A:1012319418150
    title: "Prosenjit Bose, Pat Morin, Ivan Stojmenovic and Jorge Urrutia, Routing with guaranteed delivery in ad hoc wireless networks, Wireless Networks 7(6), 2001"
    locator: pages 609 to 616 (face routing on the Gabriel graph and its delivery proof); first at DIAL-M 1999, pages 48 to 55
  - paper: "Gregory G. Finn, Routing and addressing problems in large metropolitan-scale internetworks, ISI Research Report ISI/RR-87-180, USC Information Sciences Institute, 1987"
    locator: greedy geographic forwarding and its dead ends
  - paper: doi:10.1145/778415.778447
    title: "Fabian Kuhn, Roger Wattenhofer and Aaron Zollinger, Worst-case optimal and average-case efficient geometric ad-hoc routing, ACM MobiHoc 2003"
    locator: pages 267 to 278 (GOAFR, the bound on the cost of face routing relative to the optimal path)
---

GPSR (greedy perimeter stateless routing) is a [geographic routing](/geographic-routing/) protocol for wireless networks in which every node knows its own position, the positions of its neighbors and the position of the packet's destination. In *greedy mode* a node forwards a packet to the neighbor closest to the destination. When no neighbor is closer than the node itself, the packet is at a dead end, and it switches to *perimeter mode*: it walks around the faces of a [planar](/planar-graph/) subgraph of the network, the [Gabriel graph](/gabriel-graph/) or the [relative neighborhood graph](/relative-neighborhood-graph/), which each node computes from its neighbors alone. As soon as the packet reaches a node closer to the destination than the dead end, it returns to greedy mode. Nodes keep no routes: the only state is the neighbor list, and a few fields in the packet header.

## In plain words

You walk toward a mountain you can see, and at each step you pick the path that brings you closest to it. Usually that works. Sometimes you reach the edge of a lake: every way forward takes you farther away. Then you put your right hand on the shore and walk along it, keeping the water on your hand's side, until you are closer to the mountain than where you hit the lake. Then you head straight for the mountain again. GPSR does this with radio hops. To make "walk along the shore" well defined, each radio first ignores some of its links so that no two links cross on the map.

## The problem

Nodes are points in the plane, and two nodes are neighbors when they are within the radio range $r$, so the network is a unit disk graph. Each node learns its neighbors and their positions from beacons. A packet carries the position $D$ of its destination, provided by a location service. The task is to forward the packet hop by hop to the destination with no route tables and no route discovery, so that the state per node does not grow with the network and nothing must be repaired when nodes move.

## The algorithm

Each node keeps its neighbors $N(x)$ and its edges in a planar subgraph $P$. In the Gabriel graph, $x$ keeps the edge $xy$ unless some neighbor $w$ lies inside the circle with diameter $xy$: $|xw|^2 + |yw|^2 < |xy|^2$. In the relative neighborhood graph, it keeps $xy$ unless some neighbor $w$ is closer to both $x$ and $y$ than they are to each other. A packet in perimeter mode carries $L_p$, the position where it entered perimeter mode, $L_f$, the point where it entered the current face, and $e_0$, the first edge it took on that face. The routine runs at node $x$ for a packet $P$ that arrived from node $y$:

```pseudo id=main
GPSR(x, P)                                      ▷ P is for position D and arrived from y
L1  if x is the destination then deliver P and stop
L2  if P is in perimeter mode and |x D| < |L_p D| then P.mode ← greedy
L3  if P is in greedy mode then
L4      z ← the neighbor of x closest to D
L5      if |z D| < |x D| then forward P to z and stop
L6      P.mode ← perimeter; L_p ← x; L_f ← x; e ← first edge of P at x counterclockwise from the ray x→D
L7  else e ← the next edge of P at x counterclockwise from the edge (x, y)         ▷ the right-hand rule
L8  while e crosses the segment L_p D at a point p with |p D| < |L_f D| do L_f ← p; e ← the next edge counterclockwise after e
L9  if a face change happened at L6 or L8 then e_0 ← e else if e = e_0 for the second time then drop P   ▷ the whole face was walked
L10 forward P along e
```

Greedy mode uses all neighbors; perimeter mode uses only the edges of the planar subgraph. Line L8 is the *face change*: when the next edge on the current face crosses the line from $L_p$ to $D$ closer to $D$ than before, the packet moves to the next face that this line passes through. Line L9 detects that the packet went once around a face without making progress, which happens only when the destination is unreachable.

## Example

Seven nodes with range $r = 1.2$: $S = (0, 0)$, $F = (0.9, -0.2)$, $A = (0, 1)$, $B = (1, 1.5)$, $C = (2, 1.5)$, $E = (2.6, 0.7)$ and the destination $D = (2.6, -0.3)$. The links are $S F$, $S A$, $A B$, $B C$, $C E$ and $E D$; the graph is a tree, so it is its own Gabriel graph.

1. At $S$, $|SD| \approx 2.617$. Its closest neighbor to $D$ is $F$ with $|FD| \approx 1.712$, so the packet goes greedily to $F$.
2. At $F$, the only neighbor is $S$, farther from $D$. Dead end: the packet enters perimeter mode with $L_p = L_f = F$ and takes the first edge counterclockwise from the ray $F \to D$, the edge back to $S$.
3. At $S$, $|SD| > |FD|$, so it stays in perimeter mode. Counterclockwise from the edge $S F$ comes $S A$. Then at $A$ the rule gives $A B$, at $B$ it gives $B C$, at $C$ it gives $C E$. None of these edges crosses the segment from $F$ to $D$, so there is no face change.
4. At $E$, $|ED| = 1 < 1.712$, so the packet returns to greedy mode and goes to $D$.

The path is $S, F, S, A, B, C, E, D$: 2 greedy hops and 5 perimeter hops. Greedy forwarding alone would have stopped at $F$.

**On random networks.** In 40 networks of 60 nodes placed uniformly in the unit square with range $0.2$ (seeds 0 to 39), routing from every third node to every node in its component gave 42904 packets. Greedy forwarding alone got stuck on 8021 of them, about 19 percent. GPSR delivered all 42904, over the Gabriel graph and over the relative neighborhood graph, and 8021 of them used perimeter mode. The mean path length was 1.47 times the shortest hop count with the Gabriel graph and 1.62 times with the relative neighborhood graph, whose faces are larger. The mean degree was 6.2 in the full graph, 3.0 in the Gabriel graph and 2.2 in the relative neighborhood graph.

## Correctness

Three facts carry the argument, proved in the proof file below.

- **The planar subgraph is local, planar and connected.** A witness that removes $xy$ is closer to $x$ than $y$ is, so it is a neighbor of $x$, and each node decides its edges from its neighbors' positions. Two crossing edges of the Gabriel graph span a convex quadrilateral with an angle above $90$ degrees, and the vertex of that angle lies inside the circle on the opposite diagonal, which removes one of the edges. The relative neighborhood graph is a subgraph of the Gabriel graph and contains every minimum spanning tree of the unit disk graph, so both keep the connectivity of the network.
- **Every packet stops.** Greedy hops strictly reduce the distance to $D$. Each new perimeter phase starts at a node closer to $D$ than the previous one. Inside a phase, each face change moves $L_f$ strictly closer to $D$ along a fixed segment, and the right-hand walk around one face comes back to its first edge, where line L9 drops the packet.
- **Delivery.** If the segment from $L_p$ to $D$ leaves each face at the edge where the face change happens, the part of the segment just past $L_f$ is always inside the face being walked. A whole walk around that face then has to meet either $D$ or an edge where the segment leaves the face closer to $D$, and that edge triggers a face change. So a packet is dropped only when $D$ is unreachable.

The published rule changes faces at the first crossing closer than $L_f$, without checking from which side the segment crosses, and the delivery argument above needs that crossing to be an exit. Bose, Morin, Stojmenovic and Urrutia proved delivery for face routing variants; Frey and Stojmenovic later examined cases in which some face change rules fail. All the random tests delivered every packet.

## Complexity

- **Per hop.** A node scans its $d$ neighbors to find the closest one or the next edge counterclockwise: $O(d)$. Each face change at line L8 repeats the scan, and one hop has at most $d$ face changes, so a hop costs $O(d^2)$ in the worst case and $O(d)$ in the usual case of no face change.
- **Planarization.** Each node tests each of its edges against each neighbor: $O(d^2)$ per node, once per change of the neighborhood.
- **State.** $O(d)$ per node, the neighbor table. The packet header adds $L_p$, $L_f$, $e_0$ and the mode.
- **Path length.** Greedy paths are short when the network is dense. Perimeter walks can be long: on a large face the packet may go around the whole face. GOAFR, which bounds face exploration by an ellipse, keeps the path within a constant times the square of the optimal one, which is the best possible for geographic routing.

## Properties

- **Stateless.** No route tables, no route discovery, no repair after moves; only beacons for the neighbor table.
- **Local.** Every decision uses the node's own neighborhood and the packet header.
- **Scales with density, not size.** The work per hop depends on the degree.
- **Needs positions.** GPS or a localization scheme for all nodes, and a location service for destinations.
- **Sensitive to the unit disk model.** Planarization assumes that links exist exactly within range $r$. With irregular radio ranges, the local Gabriel test can remove a needed link or keep crossing links, and perimeter mode can fail.

## Variants and improvements

- **Greedy only.** Finn's 1987 scheme drops the packet, or searches by flooding, at a dead end.
- **Face routing.** Bose, Morin, Stojmenovic and Urrutia route on faces alone, changing faces along the line from source to destination, and prove delivery on connected planar graphs.
- **GOAFR and GOAFR+.** Kuhn, Wattenhofer, Zhang and Zollinger combine greedy and face routing with a bounding ellipse or circle, which gives worst-case optimal path lengths; GOAFR+ also performs well on average.
- **Cross-link detection.** For real radios, nodes probe whether their kept links cross and remove one link of each crossing pair, as in the CLDP protocol of Kim, Govindan, Karp and Shenker.
- **Virtual coordinates.** When positions are unknown, nodes compute coordinates from hop distances to landmarks and route greedily on them.

## When to use it

Use GPSR in dense wireless networks where nodes know their positions and move often, such as vehicular and sensor networks, and where keeping routes would cost more than carrying a position in each packet. It also routes to a geographic region, as in geocasting. Avoid it when positions are poor, when radio ranges are very irregular so that the planar subgraph is wrong, or when the network has large voids that make perimeter walks long; there, a route discovery protocol such as [AODV](/aodv/) can find shorter paths.

## Pitfalls

- **Planarizing with the wrong graph.** The Gabriel and relative neighborhood tests must use all neighbors in range; a node that misses a neighbor keeps crossing edges, and perimeter mode then loops or drops.
- **Using all links in perimeter mode.** The right-hand rule only traces faces on a planar graph.
- **Comparing angles with floating point carelessly.** The next edge counterclockwise and the crossing test are [orientation tests](/orientation-test/); ties need a consistent rule.
- **Returning to greedy too early.** The return test compares with $L_p$, the point where perimeter mode began, not with the previous node; otherwise the packet can cycle between greedy and perimeter mode.
- **Stale positions.** A neighbor that moved away since its last beacon looks like the best next hop and swallows packets; short beacon intervals or link-layer feedback are needed.

## Implementations

## History

Gregory Finn described greedy geographic forwarding in 1987 and noted its dead ends. Kranakis, Singh and Urrutia introduced compass routing on planar graphs in 1999, and Bose, Morin, Stojmenovic and Urrutia gave face routing on the Gabriel graph of a unit disk graph with guaranteed delivery the same year. Brad Karp and H. T. Kung combined greedy forwarding with face traversal in GPSR at MobiCom 2000, using the local Gabriel and relative neighborhood graphs as the planar subgraph. Kuhn, Wattenhofer and Zollinger then gave the worst-case optimal GOAFR family in 2003.

## References
