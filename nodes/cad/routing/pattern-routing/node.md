---
tag: D2CZPG
kind: technique
slug: pattern-routing
name: Pattern routing
aliases:
- L-shaped and Z-shaped routing
area: cad/routing
level: core
summary: Routes each two-pin connection only by L-shaped or Z-shaped patterns with one or two bends, which is fast and leaves maze routing for hard nets.
prereqs: [global-routing]
see_also: [global-routing, lee-maze-routing, rip-up-and-reroute, negotiated-congestion-routing, flute, rectilinear-minimum-spanning-tree, layer-assignment]
sources:
  - paper: doi:10.1109/TCAD.2002.1013891
    title: Ryan Kastner, Elaheh Bozorgzadeh and Majid Sarrafzadeh, Pattern routing, use and theory for increasing predictability and avoiding coupling, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 21(7), 777 to 790, 2002
    locator: the definition of L-shaped and Z-shaped patterns for two-pin connections and the experiments that route with L-shapes (general locator)
  - paper: "Ryan Kastner, Elaheh Bozorgzadeh and Majid Sarrafzadeh, Predictable routing, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 110 to 114, 2000"
    locator: the conference version of pattern routing (general locator)
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 5, Global Routing (single-net routing and modern global routing; general locator)
---

Pattern routing is a technique of [global routing](/global-routing/) that routes each two-pin connection by one of a few fixed shapes: an L with one bend or a Z with two bends, inside the bounding box of the two pins. A connection whose pins differ by $d_x$ columns and $d_y$ rows, both at least 1, has exactly $d_x + d_y$ such routes, against $\binom{d_x + d_y}{d_x}$ shortest routes in all. The router picks the cheapest pattern under the current congestion costs. It is much faster than [maze routing](/lee-maze-routing/), and the routes are short and have few bends. Connections for which no pattern is good are left to a maze router in a later [rip-up and reroute](/rip-up-and-reroute/) step.

## In plain words

A wire from one corner of a box to the opposite corner can go many ways. Most of them zigzag. Pattern routing tries only the simple ones: go along one side and then up the other side, which is an L, or go part of the way, turn, cross, and turn back, which is a Z.

There are only a few such shapes, so the router can try them all and take the one that passes through the least crowded places. Each shape is as short as any route between the two points, and it has at most two turns, so it needs few vias.

The price is that the router does not look at other shapes. If every simple shape passes through a crowded spot, the router must try again with a slower search that can follow any path.

## When it applies

- The routing graph is a grid, and each net is split into two-pin connections, for example along a [rectilinear minimum spanning tree](/rectilinear-minimum-spanning-tree/) or a Steiner tree from [FLUTE](/flute/).
- A short route with few bends is wanted. A pattern always has the least length $d_x + d_y$, so it adds no wirelength over the [half-perimeter wirelength](/half-perimeter-wirelength/) of the connection.
- Speed is more important than the quality of each single route: the first routing of a full netlist, a congestion estimate during placement, or a router that must run on millions of connections.
- The congestion is moderate. On a very crowded grid, the best pattern often crosses a full edge, and the router must fall back to a search over all paths.

## The template

Let a connection go from $s = (x_s, y_s)$ to $t = (x_t, y_t)$, with $d_x = |x_t - x_s|$ and $d_y = |y_t - y_s|$. Each grid edge $e$ has a cost $\mathrm{cost}(e)$ that grows with its usage, for example a large penalty when the edge is full.

1. **Build the candidate set.**
   - If $d_x = 0$ or $d_y = 0$, the only pattern is the straight segment.
   - Else the two **L-shapes**: horizontal then vertical, through the corner $(x_t, y_s)$, and vertical then horizontal, through $(x_s, y_t)$.
   - The **Z-shapes** with a vertical middle segment: horizontal from $s$ to column $x'$, vertical to row $y_t$, horizontal to $t$, for each column $x'$ strictly between $x_s$ and $x_t$. There are $d_x - 1$ of them.
   - The **Z-shapes** with a horizontal middle segment, for each row $y'$ strictly between $y_s$ and $y_t$. There are $d_y - 1$ of them.
2. **Price each candidate.** Its cost is the sum of the edge costs along its 2 or 3 straight segments, plus a cost per bend if bends or vias count.
3. **Commit the cheapest** candidate: add 1 to the usage of each edge on it, and update the costs.
4. **Hand the rest on.** Mark connections whose chosen pattern crosses a full edge. A later step rips them up and routes them by maze search.

**Why there are $d_x + d_y$ patterns.** A shortest route is a sequence of $d_x$ horizontal and $d_y$ vertical steps. A route with one bend has all horizontal steps before all vertical steps or the other way round: 2 routes. A route with exactly two bends is $H^a V^{d_y} H^{d_x - a}$ with $1 \le a \le d_x - 1$, or $V^b H^{d_x} V^{d_y - b}$ with $1 \le b \le d_y - 1$: $d_x + d_y - 2$ routes. The total is $d_x + d_y$.

**Cost of the evaluation.** Keep a prefix sum of the edge costs along each row and each column. A straight segment then costs $O(1)$ to price, so all $d_x + d_y$ patterns are priced in $O(d_x + d_y)$ time. A maze search with [Dijkstra's algorithm](/dijkstra/) inside the bounding box looks at up to $(d_x + 1)(d_y + 1)$ gcells and takes $O(d_x d_y \log(d_x d_y))$ time.

## Classic examples

**A Z-shape beats both L-shapes.** Take a grid of 4 columns and 3 rows, with $s = (0, 0)$ and $t = (3, 2)$, so $d_x = 3$ and $d_y = 2$. A free edge costs 1 and a full edge costs 4. The full edges are $(1,0)(2,0)$ on the bottom row and $(1,2)(2,2)$ on the top row. There are $3 + 2 = 5$ patterns, each with 5 edges.

| pattern | gcells | cost |
| --- | --- | --- |
| L, horizontal first | (0,0) (1,0) (2,0) (3,0) (3,1) (3,2) | 8 |
| L, vertical first | (0,0) (0,1) (0,2) (1,2) (2,2) (3,2) | 8 |
| Z, middle column 1 | (0,0) (1,0) (1,1) (1,2) (2,2) (3,2) | 8 |
| Z, middle column 2 | (0,0) (1,0) (2,0) (2,1) (2,2) (3,2) | 8 |
| Z, middle row 1 | (0,0) (0,1) (1,1) (2,1) (3,1) (3,2) | 5 |

The Z-shape through the middle row avoids both full edges and wins with cost 5.

**All patterns fail, a staircase succeeds.** Make the edge $(0,1)(1,1)$ full as well. Now the last Z-shape also costs 8, so every pattern crosses a full edge. But the route $(0,0)$, $(1,0)$, $(1,1)$, $(2,1)$, $(2,2)$, $(3,2)$ has cost 5 and no full edge. It is a shortest route with 4 bends, one of the $\binom{5}{2} = 10$ shortest routes, and a maze search finds it. This connection is the kind that pattern routing leaves to the next stage.

**Straight connections.** If $s$ and $t$ lie in the same row, the straight segment is the only pattern. When one of its edges is full, any legal route must leave the row, and it is longer than $d_x$.

## Variations

- **L-shapes only.** The fastest form, with 2 candidates per connection. The experiments of Kastner, Bozorgzadeh and Sarrafzadeh use L-shapes.
- **U-shapes.** Routes with two bends that leave the bounding box on one side and come back. They are longer than $d_x + d_y$, but they can go around a crowded box.
- **Monotone routing.** Allow every shortest route, not only those with two bends. A dynamic program over the gcells of the bounding box finds the cheapest one in $O(d_x d_y)$ time, since each gcell is reached from its left or its lower neighbor (for $x_t > x_s$ and $y_t > y_s$).
- **Patterns with layers.** In a three-dimensional grid, each straight segment is put on one layer of the right direction and each bend becomes a via. A small dynamic program over the segments chooses the layers, which joins pattern routing with [layer assignment](/layer-assignment/).
- **Patterns inside other routers.** A router can use patterns for the first routing and then [negotiated congestion routing](/negotiated-congestion-routing/) or [rip-up and reroute](/rip-up-and-reroute/) with maze search for the connections that still overflow.

## Pitfalls

- **Counting a net twice on one edge.** When a multi-pin net is split into two-pin connections, two connections of the same net can share an edge. The usage of that edge goes up by 1 for the net, not by 2.
- **Order of the connections.** Each committed pattern changes the costs for the next connections. The result depends on the order, as in every sequential router. Routers often route short or critical connections first.
- **The bounding box is a hard limit.** A pattern never leaves the bounding box. If a cut across the box is full, no pattern is legal, and only a detour can help.
- **Bends cost vias.** In a grid with one direction per layer, each bend is at least one via. A Z-shape has two bends, so its cost must include them when vias matter.
- **Mixing up the pattern count.** The number of Z-shapes is $d_x + d_y - 2$, not $d_x d_y$. The extreme columns $x' = x_s$ and $x' = x_t$ give the L-shapes, so they are not counted twice.
- **Claims of quality.** Pattern routing gives no bound on the overflow of the whole routing. Its quality is measured on benchmarks, and a router that uses it needs a stronger stage after it.

## Exercises

1. Prove that a connection with $d_x, d_y \ge 1$ has $\binom{d_x + d_y}{d_x}$ shortest routes, of which exactly $d_x + d_y$ have at most two bends. For $d_x = d_y = 4$, compute both numbers (answer: 70 and 8).
2. Show how to price all $d_x + d_y$ patterns in $O(d_x + d_y)$ time with prefix sums. How much time does an update of the prefix sums take after a route is committed?
3. Give the dynamic program for the cheapest monotone route in a bounding box, and prove that it runs in $O(d_x d_y)$ time.
4. Build a grid and a connection for which every pattern crosses a full edge, every shortest route crosses a full edge, and a longer route has no full edge.
5. Two connections of one net share a segment. Show that a router that counts the usage of each connection on its own can report overflow where there is none.

## References
