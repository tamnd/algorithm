---
tag: SZRPP9
kind: concept
slug: count-to-infinity
name: Count-to-infinity problem
aliases:
- slow convergence problem
- counting to infinity
area: systems/networking-algorithms
level: intro
summary: "After a failure, distance-vector routers can feed each other stale costs and raise them step by step until the cap I; with least link cost c this takes up to ceil(I/c) rounds, with loops meanwhile."
prereqs: [distance-vector-routing]
see_also: [split-horizon-poison-reverse, distributed-bellman-ford, bellman-ford, link-state-routing, path-vector-routing, aodv]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc1058
    title: C. Hedrick, Routing Information Protocol, RFC 1058, June 1988
    locator: Section 2.2 (the problem of counting to infinity, and the choice of 16 as infinity), Sections 2.2.1 and 2.2.2 (split horizon and triggered updates as partial remedies, and three gateways in mutual deception)
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition, Pearson, 2021
    locator: Chapter 5, Section 5.2.2 (link-cost changes and link failure, the count-to-infinity problem, poisoned reverse)
  - book: isbn:9780132009164
    title: Dimitri Bertsekas and Robert Gallager, Data Networks, second edition, Prentice Hall, 1992
    locator: Section 5.2.4, the asynchronous Bellman-Ford algorithm and its behaviour after link failures (section number not checked)
  - paper: "J. J. Garcia-Luna-Aceves, Loop-free routing using diffusing computations, IEEE/ACM Transactions on Networking 1(1), 1993, pages 130 to 141"
    locator: the feasibility condition and DUAL, a distance-vector method that is loop-free at every instant
---

The count-to-infinity problem is the slow convergence of [distance-vector routing](/distance-vector-routing/) after bad news: when a destination becomes unreachable or more costly, routers keep using each other's old costs, raise them by small steps in each exchange, and forward packets in loops until the costs reach the protocol's value for "unreachable". With a cap $I$ on the metric and least link cost $c$, the counting stops after at most about $\lceil I/c \rceil$ rounds; without a cap it never stops. It is the reason RIP uses the small value 16 as infinity, and the main motive for split horizon, [link-state routing](/link-state-routing/) and [path-vector routing](/path-vector-routing/).

## In plain words

Three towns stand on one road: A, B and C. B is next to C, and A reaches C through B. One day the road from B to C closes. B asks its only other neighbour, A, how far C is. A says "two", but A's two was the old way through B. B does not know this, so it thinks: "then I am three away, through A". A hears "three" from B and moves to four. B hears four and moves to five. The two towns pass the same false hope back and forth, and the number grows by one each time. Mail for C goes back and forth between A and B the whole time. The towns stop only when the number reaches an agreed value that means "no way there".

## The idea

A router in distance-vector routing sets its cost to destination $t$ to $\min_y (w(x, y) + D(y))$ over its neighbours $y$, using the last cost $D(y)$ that each neighbour sent. The rule does not record where a neighbour's cost came from. After a failure, a neighbour's cost can rest on a path that goes back through $x$ itself, and the rule cannot tell. Good news (a cost falls) spreads one hop per exchange, because the true smaller value wins each minimum. Bad news (a cost rises) is hidden as long as some stale smaller value still circulates.

The [correctness proof](/distance-vector-routing/) of distance-vector routing makes the speed exact. In synchronous rounds, each value in round $r$ is either a real path cost to $t$ or the cost of a walk of $r$ links plus an old value. So

$$D_r(x) \ge \min\bigl(I, \delta(x, t), r c\bigr),$$

where $\delta$ is the new distance and $c > 0$ the least link cost. When $t$ is cut off, $\delta(x, t) = \infty$, and the bound shows that the values must climb at a rate of about $c$ per round. They reach the cap $I$ after at most $\lceil I/c \rceil$ rounds, and they can take that long, as the line example below shows. When $t$ is still reachable but farther away, the counting stops at the new distance instead of at $I$. In both cases the number of rounds depends on the costs, not on the number of routers.

While the values count, the next hops form loops: in each round some router forwards to a neighbour whose route leads back to it. Packets circle until their hop limit runs out, and they load the links on the loop.

Hedrick states the problem and the answer of RIP in RFC 1058 (Section 2.2): choose infinity small, so that counting ends soon, but large enough for the longest real path. RIP uses 16, so RIP networks have paths of at most 15 hops.

## Examples

All examples use synchronous rounds: in each round every router sends its vector to its neighbours, then recomputes. A failure is seen by both ends at the start of a round. The numbers come from a simulation of the [distance-vector](/distance-vector-routing/) rule with $I = 16$.

**A line of three routers.** $A - B - C$, unit costs, destination $C$. Before the failure, $D(A) = 2$ via $B$ and $D(B) = 1$. Link $B - C$ fails.

| round | 0 | 1 | 2 | 3 | 4 | ... | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|
| $D(A)$ | 2 | 4 | 4 | 6 | 6 | ... | 14 | 16 | 16 |
| $D(B)$ | 3 | 3 | 5 | 5 | 7 | ... | 15 | 15 | 16 |

Both reach 16 after 14 rounds. With RIP's 30 second period and no triggered updates this is 7 minutes, and for all of that time packets for $C$ go back and forth between $A$ and $B$.

**A cost that rises.** A triangle $x, y, z$ with $w(x, y) = 4$, $w(y, z) = 1$, $w(x, z) = 50$, destination $x$, and no cap ($I$ very large). Then $w(x, y)$ rises to 60. The new distances are 51 for $y$ (through $z$) and 50 for $z$ (direct). The routers $y$ and $z$ pass the stale route back and forth, and they settle after 46 rounds. With poison reverse they settle after 2 rounds, because $z$, which routes through $y$, tells $y$ that its cost is infinite.

**A loop of three routers.** Routers $A$, $B$, $C$ form a triangle, $C$ has a link to $D$, all costs are 1, and the destination is $D$. Then link $C - D$ fails. Even with [split horizon and poison reverse](/split-horizon-poison-reverse/), a false route goes round the triangle:

| round | $A$ | $B$ | $C$ |
|---|---|---|---|
| 0 | 2 via C | 2 via C | 16 |
| 1 | 3 via B | 3 via A | 16 |
| 2 | 16 | 16 | 4 via A |
| 3 | 16 | 5 via C | 16 |
| 4 | 6 via B | 16 | 16 |
| 13 | 15 via B | 16 | 16 |
| 14 | 16 | 16 | 16 |

Poison reverse stops each router from taking back its own route from the next hop. Here the stale route travels $B \to A \to C \to B$ with a cost one larger at each step, and each router hears it from a neighbour that is not its next hop. All three are at 16 after 14 rounds, the same as without split horizon.

**Not count to infinity.** In [link-state routing](/link-state-routing/), a failure is flooded with a new sequence number, and each router runs [Dijkstra's algorithm](/dijkstra/) on the new map, so no stale cost is ever reused. Short loops can still exist for the time of one flood, while some routers have the new map and others the old one, but no value counts.

## Where it is used

- **RIP** caps the metric at 16 and adds split horizon, poison reverse and triggered updates; see [distance-vector routing](/distance-vector-routing/). Triggered updates make each step of the count faster in time, but they do not lower the number of steps.
- **Split horizon with poison reverse** removes the count on loops of two routers only; see [split horizon with poison reverse](/split-horizon-poison-reverse/).
- **Hold-down.** Some implementations refuse new routes to a destination for a fixed time after it became unreachable, so that the stale values die first. This also delays real good news.
- **DUAL and EIGRP.** Garcia-Luna-Aceves's diffusing update algorithm (1993) never forms a loop. Each router keeps its feasible distance, the least cost that it has had to the destination since the last diffusing computation. It may switch to a neighbour only if that neighbour's reported distance is smaller than its feasible distance (the feasibility condition); a neighbour that meets it cannot route back through the router. If no neighbour meets it, the router freezes its route and asks its neighbours, and waits for all replies before it changes.
- **Path vector.** A route carries its whole path, and a router rejects a path that contains itself; see [path-vector routing](/path-vector-routing/) and [BGP](/bgp/). This removes the count, but BGP can still explore many longer paths after a withdrawal before it gives up.
- **Destination sequence numbers.** Routing protocols for ad hoc networks such as [AODV](/aodv/) tag each route with a sequence number from the destination, and a router never takes a route with an older number.
- **The proof of distance vector.** The bound $\lceil I/c \rceil + n - 1$ rounds of [distance-vector routing](/distance-vector-routing/) has the term $I/c$ only because of the count to infinity. [Distributed Bellman-Ford](/distributed-bellman-ford/) from a clean start has no stale values and needs only $n - 1$ rounds.

## References
