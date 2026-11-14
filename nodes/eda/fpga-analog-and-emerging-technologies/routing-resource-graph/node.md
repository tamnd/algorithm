---
tag: 4ASKQ1
kind: data-structure
slug: routing-resource-graph
name: Routing resource graph
aliases:
- RR graph
area: eda/fpga-analog-and-emerging-technologies
level: core
summary: A directed graph whose nodes are the wires and pins of an FPGA and whose edges are its programmable switches, on which FPGA routers search for paths.
model: word-ram
complexity:
  vars: {V: the number of nodes, E: the number of edges, k: the number of sinks of a net}
  time: {build: O(V + E), route_net: O(k (V + E)), out: O(1)}
  space: {graph: O(V + E)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1997
  people: [Vaughn Betz, Jonathan Rose]
  note: PathFinder (1995) routed on a graph whose nodes are wires and pins. Betz and Rose made the routing resource graph the central structure of VPR, built from a short description of the architecture, so one router serves every architecture that the description covers.
prereqs: [island-style-fpga, fpga-switch-block, graph]
see_also: [negotiated-congestion-routing, minimum-channel-width, universal-switch-block, sat-based-fpga-routing, breadth-first-search, dijkstra, arborescence, lee-maze-routing]
sources:
  - book: isbn:9780792384601
    title: Vaughn Betz, Jonathan Rose and Alexander Marquardt, Architecture and CAD for Deep-Submicron FPGAs, Kluwer, 1999 (doi 10.1007/978-1-4615-5145-4)
    locator: Chapter 4, Section 4.2 Architecture Parameterization and Generation (the routing resource graph with SOURCE, OPIN, CHANX, CHANY, IPIN and SINK nodes, and node capacities) and Section 4.3 Routability-Driven Router
  - paper: doi:10.1145/201310.201328
    title: Larry McMurchie and Carl Ebeling, PathFinder, a negotiation-based performance-driven router for FPGAs, Proceedings of the ACM Symposium on Field-Programmable Gate Arrays (FPGA '95), 111 to 117, 1995
    locator: the routing graph with wires and pins as nodes of capacity 1, and routes as trees in it
  - paper: "Vaughn Betz and Jonathan Rose, VPR, a new packing, placement and routing tool for FPGA research, Field-Programmable Logic and Applications (FPL 1997), Lecture Notes in Computer Science 1304, Springer, 1997"
    locator: the description of VPR and its architecture-driven router (general locator)
  - paper: doi:10.1145/2617593
    title: Jason Luu and others, VTR 7.0, next generation architecture and CAD system for FPGAs, ACM Transactions on Reconfigurable Technology and Systems 7(2), 2014
    locator: the routing resource graph of the VTR flow (general locator)
---

A routing resource graph is a directed [graph](/graph/) that holds every routing resource of an FPGA: each wire segment, each pin, and each source and sink of a logic block is a node, and each programmable switch that can drive one resource from another is a directed edge. Each node has a capacity, 1 for a wire or a pin, so a legal routing gives each net its own nodes. A router finds the route of a net as a tree in this graph and never needs to know the grid of the [island-style FPGA](/island-style-fpga/), the [switch block](/fpga-switch-block/) pattern or the connection block pattern. The structure belongs to the FPGA CAD topic of this sub-area.

## In plain words

Think of every wire piece and every pin of the chip as a stop on a map, and of every switch as a one-way road from one stop to the next. A signal starts at the output of one block and must reach the inputs of other blocks by following roads.

Routing a net then means picking a set of stops that starts at the output and reaches every input the net needs, without two nets ever using the same stop. If two nets met on one wire, they would short each other.

The map hides how the chip is drawn. The same search code works whether the chip has short or long wires, or one switch pattern or another, because all of that is already in the roads.

## The abstract type

The graph $G = (V, E)$ is built once from the architecture and then only read. Each node $v$ has a kind, a position, a track number when it is a wire, and a capacity $c(v) \ge 1$. The kinds are:

- **SOURCE** and **SINK**: the logical start of the output of a block and the logical end of one of its inputs.
- **OPIN** and **IPIN**: an output pin and an input pin of a block.
- **CHANX** and **CHANY**: one wire segment in a horizontal or a vertical channel.

The edges follow the electrical paths: SOURCE to OPIN, OPIN to wires through the output connection block, wire to wire through switch blocks, wire to IPIN through the input connection block, and IPIN to SINK.

A **net** $i$ is a source node $s_i$ and a set $K_i$ of sink nodes. A **route** of net $i$ is a subgraph $R_i$ of $G$ in which every node of $K_i$ is reachable from $s_i$. A **routing** of the nets is **legal** when no node is in more than $c(v)$ of the routes; with all capacities 1, the node sets of the routes are pairwise disjoint. A route is **minimal** when no edge can be removed from it with all sinks still reachable from $s_i$.

The operations are BUILD, OUT(v) (the list of edges that leave $v$), and ROUTE-NET, the search that the routers of this page and of [negotiated congestion routing](/negotiated-congestion-routing/) run on it.

## Representation

Nodes are numbered $0$ to $|V| - 1$. Arrays give the kind, the position and the track of each node, and a hash map gives the number of a node from its key, such as (CHANX, $x$, $y$, $t$). Each node keeps the list of its out-edges, which is an adjacency list. A real tool also stores the resistance and capacitance of each wire and the switch type of each edge, for the delays, and the base cost of each node for the router.

In the implementation, the array has $n_x \times n_y$ blocks, each with one output pin and $P$ input pins. All segments have length 1. The output pin drives tracks $0$ to $F_{out} - 1$ on each of the four sides of the block. Input pin $p$ reads the $F_{in}$ tracks $p, p + 1, \ldots$ (mod $W$) of the channel on side $p \bmod 4$. Each switch block joins track $t$ on side $a$ to track $\pi_{ab}(t)$ on side $b$, for each pair of sides that exist, in both directions. The patterns are the subset pattern ($\pi = $ identity), the pattern of the [universal switch block](/universal-switch-block/), and an illustrative pattern in which turns change the track.

## Operations

```pseudo id=main
BUILD(n_x, n_y, W, P, F_in, F_out, π)
L1  for each block (x, y): add SOURCE, OPIN, P IPIN and P SINK nodes, the edge SOURCE → OPIN and the edges IPIN_p → SINK_p
L2  for each channel piece and each track t: add one CHANX or CHANY node
L3  for each block and each of its 4 sides: add edges OPIN → tracks 0 to F_out − 1 of the channel piece on that side
L4  for each block and pin p: add edges from tracks p to p + F_in − 1 (mod W) of the piece on side p mod 4 → IPIN_p
L5  for each switch block, each pair of its sides (a, b) and each track t: add the edges (a, t) → (b, π_ab(t)) and back

ROUTE-NET(G, s, K, used)
L6  tree ← {s};  route ← no edges
L7  for each sink k in K, in order:
L8      breadth-first search from all nodes of tree at once, entering only nodes that are in neither used nor tree, until k is found
L9      if k is not found then return FAIL
L10     follow the search links back from k to the first node of tree; add the path's nodes to tree and its edges to route
L11 return tree, route
```

ROUTE-NET is a maze search on the graph, the FPGA form of [Lee's algorithm](/lee-maze-routing/). With unit node costs, [breadth-first search](/breadth-first-search/) gives a path with the fewest edges; a router with costs uses [Dijkstra's algorithm](/dijkstra/) in line L8 instead. The caller adds the nodes of a returned tree to used, which reserves them for the net.

## Example

Take $n_x = 2$, $n_y = 1$, $W = 2$, $P = 1$, $F_{in} = 2$, $F_{out} = 1$. The two blocks give $2 \cdot 4 = 8$ pin, source and sink nodes, and the channels give $2 (2 \cdot 2 + 1 \cdot 3) = 14$ track nodes, so $|V| = 22$ and $|E| = 56$. Pin 0 of each block reads both tracks of the channel above it, and the output pin drives track 0 on all four sides.

Net $a$ goes from block $(1,1)$ to the input of block $(2,1)$, and net $b$ from block $(2,1)$ to the input of block $(1,1)$. They are routed in this order.

- Net $a$: SOURCE$(1,1)$, OPIN$(1,1)$, CHANX$(1,1,0)$, CHANX$(2,1,0)$, IPIN$(2,1,0)$, SINK$(2,1,0)$. The top channel goes straight across the switch block between the two blocks. The tree has 5 edges.
- Net $b$ with the universal pattern: SOURCE$(2,1)$, OPIN$(2,1)$, CHANY$(1,1,0)$, CHANX$(1,1,1)$, IPIN$(1,1,0)$, SINK$(1,1,0)$. The vertical wire between the blocks turns left into the top channel, and the turn from the bottom side to the left side swaps track 0 to track 1, which is free.
- Net $b$ with the subset pattern: FAIL. Every track that the output of block $(2,1)$ reaches is track 0, and the input of block $(1,1)$ can only be reached from track 0 through CHANX$(1,1,0)$, which net $a$ holds.

With the subset pattern, the reverse order fails too. Yet a legal routing exists: net $a$ goes around the bottom, through CHANX$(1,0,0)$, CHANX$(2,0,0)$, CHANY$(2,1,0)$ and CHANX$(2,1,0)$, and net $b$ takes CHANY$(1,1,0)$ and CHANX$(1,1,0)$. A shortest path for one net can block the next one, which is why routers rip up and reroute.

## Correctness

The [full proof](proofs/correctness.md) shows the following.

- **Routings are disjoint trees.** With capacity 1 on every node, a family of minimal routes is a legal routing if and only if it is a family of pairwise vertex-disjoint out-trees, one rooted at each source $s_i$, each holding all of $K_i$ and with only sinks as leaves. So searching for trees loses nothing.
- **ROUTE-NET is right.** If it returns, the result is such a tree and avoids every node of used. It returns FAIL if and only if some sink of the net is not reachable from $s$ through nodes outside used, so the failure is real for that set of used nodes.
- **Shortest steps.** Each path that line L10 adds has the fewest edges among the paths from the current tree to that sink through free nodes.

The router of one net is exact. Routing the nets one by one is not: as the example shows, a net can fail although a legal routing of all nets exists.

## Complexity

- **Size.** With unit-length segments, the implementation has $|V| = n_x n_y (2 + 2P) + W (n_x (n_y + 1) + n_y (n_x + 1))$ nodes. A switch block with $s$ sides adds $W s (s - 1)$ directed edges, and each block adds $1 + P + 4 F_{out} + P F_{in}$ more. The test checks these closed forms.
- **BUILD** adds each node and edge once, in $O(|V| + |E|)$ time and space.
- **OUT(v)** is a list, so a search reads each edge in $O(1)$.
- **ROUTE-NET** runs one breadth-first search per sink, each in $O(|V| + |E|)$, so $O(k (|V| + |E|))$ for $k$ sinks. With Dijkstra's algorithm and a binary heap, each search takes $O(|E| \log |V|)$.

For a square array of $n$ blocks, $|V|$ and $|E|$ grow as $\Theta(n W)$ for fixed $P$, $F_{in}$ and $F_{out}$, so the graph of a large FPGA has millions of nodes, and memory is a real limit of the method.

## Variants

- **Longer segments.** A node of a segment of length $L$ spans $L$ blocks. Switch blocks then join segment ends and, in some patterns, the middle of a segment.
- **Single-driver wires.** Each segment is driven by one multiplexer at its start, so the edges into a node are the inputs of its multiplexer. The graph stays the same kind of object.
- **Equivalent pins.** When the inputs of a cluster are logically equivalent, as with a full local crossbar, VPR uses one SINK node per block with capacity equal to the number of equivalent pins. The disjoint tree statement then holds for every node except such sinks.
- **Edges with switches as nodes.** Some tools make each switch a node too, so that switches can have their own cost and capacity.
- **Inside the cluster.** The local crossbar of a [logic cluster](/fpga-logic-cluster/) can be added as more nodes and edges, which is what an architecture-aware packer routes on.

## When to use it

Use a routing resource graph whenever a router must work on more than one FPGA architecture, or on an architecture with irregular parts such as memory columns and long wires. Routers such as [negotiated congestion routing](/negotiated-congestion-routing/) and the binary search for the [minimum channel width](/minimum-channel-width/) all work on it. For a fixed regular array with one pattern, a direct grid model is smaller, but it ties the router to that array. Exact methods such as [SAT-based FPGA routing](/sat-based-fpga-routing/) need fewer variables when they work on the tracks of a fixed global routing instead of the whole graph.

## Pitfalls

- **Edges in one direction only.** A switch between two bidirectional wires needs two directed edges. With one edge, the router misses half of the paths.
- **Capacity on edges.** In an FPGA, nets conflict on wires, not on switches. A model with capacities on edges lets two nets share a wire. Put the capacity on nodes.
- **Routing through a pin.** IPIN nodes lead only to their SINK, and SOURCE nodes have no in-edges, so no route can pass through another block. A graph that joins pins in other ways can make routes that pass through a block.
- **Sharing a node inside one net.** A net uses a node once even when two of its sinks pass through it. Count usage per net, not per path.
- **Order of nets.** A router that routes the nets once, in a fixed order, can fail on a routable instance, as in the example.

## Implementations

## History

McMurchie and Ebeling's PathFinder (1995) routed FPGAs on a graph whose nodes are wires and pins, with capacity 1 per node. Betz and Rose built VPR around a routing resource graph that the tool generates from a short description of the architecture: the channel width, the segment lengths, $F_c$, $F_s$ and the switch block pattern. Their book (1999, Chapter 4) describes the node kinds and how the graph is built. This let the same router compare many architectures, and the graph remains the routing model of the VTR flow.

## References
