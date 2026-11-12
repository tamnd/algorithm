---
tag: 28GHSZ
kind: problem
slug: geographic-routing
name: Geographic routing
aliases:
- position-based routing
- geometric routing
area: systems/networking-algorithms
level: advanced
summary: "Deliver a packet in a wireless network using only the positions of the current node, its neighbors and the destination, with no route tables, and without getting stuck at voids."
prereqs: [ad-hoc-routing, random-geometric-graph, planar-graph]
see_also: [gpsr, aodv, gabriel-graph, relative-neighborhood-graph, planar-face, delaunay-triangulation, triangle-walk-point-location, geohash]
sources:
  - paper: "Gregory G. Finn, Routing and addressing problems in large metropolitan-scale internetworks, ISI Research Report ISI/RR-87-180, USC Information Sciences Institute, 1987"
    locator: greedy forwarding toward the destination's coordinates and the dead-end problem
  - paper: "Hideaki Takagi and Leonard Kleinrock, Optimal transmission ranges for randomly distributed packet radio terminals, IEEE Transactions on Communications 32(3), 1984"
    locator: pages 246 to 257 (most forward within radius, MFR)
  - paper: "Evangelos Kranakis, Harvinder Singh and Jorge Urrutia, Compass routing on geometric networks, Proceedings of the 11th Canadian Conference on Computational Geometry (CCCG), 1999"
    locator: compass routing, its failure on some planar graphs, and face routing
  - paper: doi:10.1023/A:1012319418150
    title: "Prosenjit Bose, Pat Morin, Ivan Stojmenovic and Jorge Urrutia, Routing with guaranteed delivery in ad hoc wireless networks, Wireless Networks 7(6), 2001"
    locator: pages 609 to 616 (face routing on the Gabriel graph of a unit disk graph, guaranteed delivery)
  - paper: doi:10.1145/345910.345953
    title: "Brad Karp and H. T. Kung, GPSR: greedy perimeter stateless routing for wireless networks, ACM MobiCom 2000"
    locator: pages 243 to 254 (greedy forwarding with perimeter mode)
  - paper: doi:10.1145/778415.778447
    title: "Fabian Kuhn, Roger Wattenhofer and Aaron Zollinger, Worst-case optimal and average-case efficient geometric ad-hoc routing, ACM MobiHoc 2003"
    locator: pages 267 to 278 (GOAFR, the upper bound O(c^2) and the matching lower bound)
  - paper: doi:10.1145/872035.872044
    title: "Fabian Kuhn, Roger Wattenhofer, Yan Zhang and Aaron Zollinger, Geometric ad-hoc routing: of theory and practice, ACM PODC 2003"
    locator: pages 63 to 72 (GOAFR+ and its simulations)
  - paper: "Robert Kleinberg, Geographic routing using hyperbolic space, IEEE INFOCOM 2007"
    locator: greedy embeddings of every connected graph in the hyperbolic plane
---

Geographic routing (also *position-based routing*) is the problem of forwarding packets in a wireless network when every node knows its own position in the plane, the positions of its radio neighbors, and the position of the packet's destination, and nothing else. Each node decides the next hop from this local view and from a few fields in the packet header. Nodes keep no routes, so there is nothing to discover or repair when the network changes; the cost is that a packet can reach a *void*, a node with no neighbor closer to the destination. The problem asks for a forwarding rule that always delivers when a path exists, and that keeps the path short. It is the third main family of [ad hoc routing](/ad-hoc-routing/), next to proactive and reactive protocols such as [AODV](/aodv/).

## In plain words

Picture a city where every person knows only the people within shouting distance and where they stand. A letter carries the address of the person it is for. Each holder passes the letter to whoever nearby stands closest to that address. This usually works, but sometimes the letter reaches someone at the edge of a park: everyone nearby is farther from the address. The letter must then go around the park. The question is how to go around obstacles with only local knowledge, never losing the letter and never sending it on a very long trip.

## Definition

**Network.** The nodes $V$ are points in the plane, and two nodes are neighbors when they are at distance at most the radio range $r$. This graph is the *unit disk graph* of $V$, the model behind [random geometric graphs](/random-geometric-graph/). Some formulations allow any graph drawn in the plane, or a quasi unit disk graph in which links between distance $\rho r$ and $r$ may or may not exist.

**Input at each step.** A node $x$ that holds a packet knows its position, the positions of its neighbors $N(x)$, and the position of the destination $t$, carried in the packet. The packet may carry a header of $O(\log n)$ bits, enough for a constant number of positions and node names, so that a rule can remember where it started a detour.

**Output.** The next hop, a node of $N(x)$, or a decision to deliver or to drop.

**Goals.**

- **Delivery.** A rule *guarantees delivery* if, on every connected network, every packet reaches $t$.
- **Path quality.** Compare the cost of the route with the cost $c$ of the optimal path, in hops or in Euclidean length. A rule is *competitive* if the ratio is bounded.
- **Locality.** Decisions depend only on the local view and the header: no global state, no route tables, no memory at the nodes about past packets (a *memoryless* or *stateless* rule).

Positions come from GPS or from localization. The position of the destination comes from a *location service*, which is a separate problem.

## Variants

- **Greedy routing.** Forward to the neighbor closest to $t$. Variants pick the neighbor with the largest progress along the line to $t$ (most forward within radius, MFR) or the smallest angle to $t$ (compass routing). All of these are memoryless, and all of them can stop at a void or loop.
- **Face routing.** On a [planar graph](/planar-graph/), walk the boundaries of the [faces](/planar-face/) that the line from source to destination crosses, with the right-hand rule, and switch faces at crossings. This needs a planar connected subgraph that nodes can compute locally.
- **Combined greedy and face routing.** Route greedily and switch to face routing only at a void, as in [GPSR](/gpsr/) and the GOAFR family.
- **Geocasting.** Deliver to all nodes in a region instead of to one node.
- **Three dimensions.** Nodes in space, such as underwater or in buildings. There are no faces to walk, and local memoryless delivery is much harder.
- **Unknown positions.** Nodes compute virtual coordinates, for example hop distances to landmarks, and route greedily in them.

## Examples

**A void.** Place nodes on a C-shaped region with the destination just outside the mouth of the C, and the source inside the opposite arm. Greedy forwarding moves toward the destination until it reaches the inner wall of the C, where every neighbor is farther away. The only path goes around the arm, first away from the destination.

**Greedy fails in random networks.** With 60 nodes uniformly in the unit square and range $0.2$, over 40 random networks, greedy forwarding got stuck on about 19 percent of the connected source and destination pairs, while GPSR delivered all of them. The [GPSR page](/gpsr/) gives the numbers.

**Where greedy always works.** On a [Delaunay triangulation](/delaunay-triangulation/), every node other than $t$ has a neighbor closer to $t$, so greedy routing never meets a void. A unit disk graph is not a triangulation, and the full Delaunay triangulation has long edges that are not radio links, so this does not solve the wireless problem by itself. It shows that voids are a property of the graph, and it connects the problem to point location by [walking in a triangulation](/triangle-walk-point-location/).

## Known algorithms

| Algorithm | Year | Delivery | Path cost |
|---|---|---|---|
| Greedy (Finn) | 1987 | no, stops at voids | short when it works |
| Most forward within radius (Takagi, Kleinrock) | 1984 | no | short when it works |
| Compass routing (Kranakis, Singh, Urrutia) | 1999 | no, loops on some planar graphs | |
| Face routing (Kranakis et al.; Bose, Morin, Stojmenovic, Urrutia) | 1999 | yes, on connected planar graphs | can be linear in the number of nodes, even when $c$ is small |
| [GPSR](/gpsr/) (Karp, Kung) | 2000 | yes in the unit disk model, with the planar subgraph; see its page for the face change rule | short in dense networks, no worst-case bound |
| GOAFR, GOAFR+ (Kuhn, Wattenhofer, Zhang, Zollinger) | 2003 | yes | $O(c^2)$, worst-case optimal |
| Greedy on a greedy embedding (Kleinberg) | 2007 | yes, with precomputed coordinates | |

The planar subgraph that face routing needs is usually the [Gabriel graph](/gabriel-graph/) or the [relative neighborhood graph](/relative-neighborhood-graph/) of the unit disk graph. Each node computes its own edges in either graph from the positions of its neighbors, the result is planar, and it has the same components as the unit disk graph because it contains every [minimum spanning tree](/minimum-spanning-tree/).

## Bounds

- **Lower bound on path cost.** Kuhn, Wattenhofer and Zollinger construct unit disk graphs in which the optimal path has cost $c$ but every local geographic routing rule needs $\Omega(c^2)$ steps for some destination: the network is a ring of long dead-end corridors, and only one of them leads through. GOAFR reaches $O(c^2)$, so it is optimal up to a constant factor. The bound assumes a constant lower bound on the distance between nodes, or measures cost in a way that charges for short edges.
- **Face routing is not competitive.** Plain face routing explores whole faces, so its cost is not bounded by any function of $c$.
- **Three dimensions.** Durocher, Kirkpatrick and Narayanan showed that no deterministic local memoryless rule guarantees delivery on all unit ball graphs in three dimensions. Randomized and stateful rules exist.
- **Greedy embeddings.** Kleinberg showed that every connected graph has coordinates in the hyperbolic plane on which greedy routing always succeeds. Leighton and Moitra proved the conjecture of Papadimitriou and Ratajczak that every 3-connected planar graph has such coordinates in the Euclidean plane.

## Reductions

- **Delivery reduces to planarization.** Any local rule that builds a connected planar subgraph, together with face routing on that subgraph, gives guaranteed delivery. In the unit disk model, the Gabriel and relative neighborhood graphs provide it. Outside the unit disk model, the local tests can fail, and planarization needs probes or extra messages, such as cross-link detection.
- **Location service.** A location service turns routing to a node name into routing to a position. Geographic hash tables go the other way: they hash a key to a position and store the value at the node closest to it, using geographic routing for both puts and gets, much as [consistent hashing](/consistent-hashing/) maps keys to servers.
- **From graphs to geometry.** For a network without positions, computing a greedy embedding turns arbitrary routing into geographic routing, at the cost of a global precomputation.

## Applications

- **Sensor networks.** Data is often addressed by region ("the temperature near this point"), which matches routing by position.
- **Vehicular networks.** Cars know their positions from GPS, and the topology changes too fast for route discovery.
- **Data-centric storage.** Geographic hash tables store sensor readings at positions derived from their keys.
- **Geocast.** Emergency messages to everyone in an area.

## References
