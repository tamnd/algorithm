---
tag: DWVTYT
kind: algorithm
slug: distance-vector-routing
name: Distance-vector routing
aliases:
- Bellman-Ford routing
- routing information protocol
- distance vector protocol
area: systems/networking-algorithms
level: core
summary: "Each router keeps the last distance vector of each neighbour, takes the minimum of link cost plus advertised cost, and resends its vector on a timer and after changes. RIP caps metrics at 16."
solves: [routing-problem]
model: synchronous-model
complexity:
  vars: {n: the number of routers, m: the number of links, d: the largest degree of a router, I: "the metric that means unreachable, 16 in RIP"}
  time: {worst: O(n + I)}
  messages: {worst: O(m (n + I))}
  space: {extra: O(n d)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1988
  people: [Charles Hedrick]
  note: RFC 1058 (Hedrick, 1988) wrote down RIP, the distance-vector protocol of BSD routed. RIP version 2 is RFC 2453 (Malkin, 1998).
prereqs: [routing-problem, bellman-ford, distributed-bellman-ford, synchronous-model]
see_also: [count-to-infinity, split-horizon-poison-reverse, link-state-routing, path-vector-routing, dijkstra, shortest-path-tree, asynchronous-model, edge-relaxation]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc1058
    title: C. Hedrick, Routing Information Protocol, RFC 1058, June 1988
    locator: Section 2 (the distance-vector algorithm), Section 2.2 (counting to infinity, with 16 as infinity), Sections 2.2.1 and 2.2.2 (split horizon and triggered updates)
  - url: https://www.rfc-editor.org/rfc/rfc2453
    title: G. Malkin, RIP Version 2, RFC 2453, November 1998
    locator: Sections 3.4.1 to 3.4.4 (infinity, split horizon, poisoned reverse, triggered updates), Section 3.8 (the 30 s update, 180 s timeout and 120 s garbage-collection timers), Section 3.9.2 (processing of response messages), Section 3.10.1 (the 1 to 5 s limit on triggered updates)
  - book: isbn:9780132009164
    title: Dimitri Bertsekas and Robert Gallager, Data Networks, second edition, Prentice Hall, 1992
    locator: Section 5.2.4, the distributed asynchronous Bellman-Ford algorithm and its convergence in finite time after the last change with positive link lengths (section number not checked)
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition, Pearson, 2021
    locator: Chapter 5, Section 5.2.2 (the distance-vector algorithm, link-cost changes, poisoned reverse)
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition, Morgan Kaufmann, 2011
    locator: Chapter 3, Section 3.3.2 (distance vector and RIP)
  - paper: "John M. McQuillan, Ira Richer and Eric C. Rosen, The new routing algorithm for the ARPANET, IEEE Transactions on Communications 28(5), 1980, pages 711 to 719"
    locator: the introduction, on the distance-vector method that the ARPANET used before 1979 and its slow response to bad news
  - paper: "J. J. Garcia-Luna-Aceves, Loop-free routing using diffusing computations, IEEE/ACM Transactions on Networking 1(1), 1993, pages 130 to 141"
    locator: DUAL, the feasibility condition and the diffusing computations
---

Distance-vector routing is the distributed protocol in which each router tells its neighbours its current cost to every destination, and computes its own costs as the minimum, over its neighbours, of the link cost plus the neighbour's advertised cost. It solves the [routing problem](/routing-problem/) inside one network with no router that sees the whole map. It is the protocol form of the [Bellman-Ford algorithm](/bellman-ford/): [distributed Bellman-Ford](/distributed-bellman-ford/) is the bare message-passing computation, and this page adds what a real protocol needs: periodic and triggered updates, timers for silent neighbours, a finite metric $I$ for "unreachable" (16 in RIP), and the behaviour after failures. With positive link costs, the tables reach the true distances within $\lceil I/c \rceil + n - 1$ synchronous rounds after the last change, where $c$ is the least link cost; the price of this simplicity is the slow [count to infinity](/count-to-infinity/) after a failure.

## In plain words

Each router has a list with one line per destination: how far it is, and which neighbour to send to. Every half minute, each router reads its list to its neighbours. When a router hears a neighbour's list, it adds the cost of the link to that neighbour to every number on it. For each destination it keeps the smallest sum it has heard, and notes the neighbour that gave it.

No router knows the whole map. Good news, such as a new short link, spreads one hop per exchange. Bad news spreads slowly: when a link breaks, two routers can keep each other's old numbers alive and raise them one step at a time. So the protocol treats a fixed large number, sixteen, as "cannot reach".

## The problem

The network is a connected undirected graph $G = (V, E)$ of $n$ routers and $m$ links, each link $(x, y)$ with a cost $w(x, y) \ge c > 0$. The output is a forwarding table at each router $x$: for each destination $t$, a metric $D[x][t]$ and a next hop $h[x][t]$ that is a neighbour of $x$. The aim is $D[x][t] = \min(I, \delta(x, t))$, where $\delta$ is the shortest-path distance and $I$ the metric for "unreachable", and the next hops must form, for each $t$, a [shortest path tree](/shortest-path-tree/) toward $t$. Links can fail, come back, or change cost at any time. The protocol must reach the right tables again after the last change.

## The algorithm

Router $y$ stores $V[y][x]$, the last vector that it heard from each neighbour $x$, and its own table $D[y]$. The mode decides what $y$ tells a neighbour about routes that go through that neighbour: everything ("none"), nothing (simple split horizon) or $I$ ([split horizon with poison reverse](/split-horizon-poison-reverse/)).

```pseudo id=main
DV-ROUTER(y)                       ▷ event handlers of router y; I is the unreachable metric
L1  on START: V[y] ← empty;  D[y][y] ← (0, y);  start the periodic timer
L2  on RECEIVE(x, vec): V[y][x] ← vec;  heard[x] ← now
L3      RECOMPUTE(y)
L4  on TIMER: delete each V[y][x] with now − heard[x] ≥ TIMEOUT   ▷ silent neighbour
L5      RECOMPUTE(y);  SEND-ALL(y);  restart the timer for PERIOD
L6  on LINK-DOWN(x): delete V[y][x] and the link;  RECOMPUTE(y)

RECOMPUTE(y)
L7  for each destination t ≠ y that occurs in D[y] or in some V[y][x] do
L8      (m, h) ← (I, nil)
L9      for each neighbour x with t in V[y][x] do: if min(I, w(y, x) + V[y][x][t]) < m then (m, h) ← (that value, x)
L10     D[y][t] ← (m, h)
L11 if a metric changed and triggered updates are on then SEND-ALL(y)

SEND-ALL(y)
L12 for each neighbour x: vec ← D[y] with each route whose next hop is x left out (split) or set to I (poison)
L13     send vec to x
```

Line L9 is the Bellman-Ford relaxation over the neighbours, with the sum capped at $I$. The neighbours are scanned in a fixed order and only a strictly smaller value replaces the best, so ties go to the first neighbour. The table is recomputed from scratch from the stored vectors, so a neighbour that raises its cost raises the routes through it at once. RIP itself works incrementally on each received entry (RFC 2453, Section 3.9.2): it accepts any new metric from the current next hop, and it switches to another neighbour only for a strictly smaller metric. The two rules have the same fixed points.

The timers of RIP are: a periodic update every 30 seconds with a small random offset, so that routers do not fall into step; a timeout of 180 seconds, after which a route whose next hop is silent becomes unreachable; and a garbage-collection time of 120 seconds during which the route is still sent with metric 16 before it is deleted. A triggered update goes out soon after a metric changes, with a random gap of 1 to 5 seconds between triggered updates (RFC 2453, Sections 3.8 and 3.10.1).

## Example

Three routers in a line, $A - B - C$, with cost 1 on each link, and destination $C$. The rounds are synchronous: in each round every router sends its vector, then every router recomputes. After two rounds the tables are $D[B][C] = (1, C)$ and $D[A][C] = (2, B)$. Then link $B - C$ fails at the start of a round, and both ends see it.

| round after the failure | $D[A][C]$ | $D[B][C]$ | why |
|---|---|---|---|
| 0 | 2 via B | 3 via A | B lost its vector from C; A's last vector says 2 |
| 1 | 4 via B | 3 via A | A hears 3 from B |
| 2 | 4 via B | 5 via A | B hears 4 from A |
| 3 | 6 via B | 5 via A | |
| 12 | 14 via B | 15 via A | |
| 13 | 16, none | 15 via A | 1 + 15 reaches the cap |
| 14 | 16, none | 16, none | both know that C is unreachable |

So the bad news takes 14 rounds, which is 7 minutes with 30 second updates and no triggered updates. With split horizon, or with poison reverse, $A$ does not tell $B$ about a route that goes through $B$. Then $B$ has no route to $C$ at once, and both metrics are 16 after one round.

## Correctness

The proof uses the synchronous model: in round $r$ each router sends the vector computed in round $r - 1$, and recomputes from the vectors it receives. The initial vectors $D_0$ are arbitrary values in $[0, I]$, which covers both a cold start and the stale state just after a change. Let $\delta(x, t)$ be the distance after the last change, $\infty$ if $t$ is not reachable, and let $c > 0$ be the least link cost.

**Theorem.** In each mode, for every round $r \ge \lceil I/c \rceil + n - 1$ and all $x, t$: $D_r[x][t] = \min(I, \delta(x, t))$, and from round $r + 1$ on, when this is less than $I$, the next hops lead from $x$ to $t$ along a shortest path.

The proof has two parts. A lower bound, by induction on $r$: $D_r[x][t] \ge \min(I, \delta(x, t), rc)$, because each finite value is either a link to $t$ or a link cost plus a neighbour's value from the round before. So after $\lceil I/c \rceil$ rounds no value is below $\min(I, \delta)$; this is where positive costs are needed. An upper bound, by induction on the depth of $x$ in a shortest path tree toward $t$: the parent $y$ of $x$ has the right value one round earlier, and its next hop is not $x$, because a route through $x$ would cost more than $\delta(y, t)$. So $y$ advertises its true value to $x$ even under split horizon. The full proof is in [the correctness proof](#proof-correctness). Bertsekas and Gallager prove the same finite convergence for the asynchronous version, with arbitrary delays, when every router keeps sending (Data Networks, Section 5.2.4).

## Complexity

The counts are for the synchronous model, with all $n$ routers as destinations.

- **Rounds.** By the theorem, at most $\lceil I/c \rceil + n - 1$ rounds after the last change. With integer costs $c \ge 1$ this is $O(n + I)$. From a cold start, where each router knows only its links, the plain rule needs at most $n - 1$ rounds, because after $r$ rounds the value is the shortest path of at most $r + 1$ links. The term $I/c$ is the cost of bad news: it is the count to infinity.
- **Messages.** Each round sends one vector over each direction of each link, so $2m$ messages of at most $n$ entries. Over $O(n + I)$ rounds this is $O(m(n + I))$ messages. RIP sends them periodically whether or not anything changed.
- **Work and space at a router.** RECOMPUTE scans the $n$ destinations and the $\deg(y)$ stored vectors, so $O(n \deg(y))$ time, and the stored vectors take $O(n d)$ space, with $d$ the largest degree.

| measure | bound | case |
|---|---|---|
| rounds after the last change | $O(n + I)$ | worst case, integer costs |
| messages | $O(m(n + I))$ | worst case |
| space per router | $O(nd)$ | worst case |

## Properties

- **Distributed and local.** A router uses only its own links and its neighbours' vectors.
- **Self-correcting.** The theorem holds from any initial values in $[0, I]$, so corrupt tables are also repaired.
- **Not loop-free while it converges.** During the count to infinity in the example, $A$ forwards to $B$ and $B$ forwards to $A$, so packets loop until their TTL runs out.
- **Bounded diameter.** A destination at distance $I$ or more is unreachable. With $I = 16$ and unit costs, RIP is limited to networks whose paths have at most 15 hops.

## Variants and improvements

- **Split horizon and poison reverse.** These stop loops of two routers; loops of three or more can still count to infinity. See [split horizon with poison reverse](/split-horizon-poison-reverse/).
- **Hold-down.** Some implementations ignore new routes to a destination for a fixed time after it became unreachable, so that stale news can die out. This slows good news as well.
- **DUAL and EIGRP.** Garcia-Luna-Aceves's diffusing update algorithm keeps loop freedom at every instant: a router takes a new next hop only if the neighbour's cost is less than the router's own feasible distance, and otherwise it asks its neighbours first. See [count to infinity](/count-to-infinity/).
- **Path vector.** Send the whole path instead of the cost, and reject a path that already contains the receiver. See [path-vector routing](/path-vector-routing/).
- **Link state.** Flood the topology and compute paths locally. See [link-state routing](/link-state-routing/).

## When to use it

Distance vector needs little memory and little configuration, and it suits small networks with few changes. RIP is still found in small sites and as a simple protocol between a router and a host. In larger networks, operators use [link-state routing](/link-state-routing/) (OSPF, IS-IS), which converges in about the time of one flood and one [Dijkstra](/dijkstra/) run and has no count to infinity. Between administrative domains, where policy matters more than cost, the Internet uses the path-vector protocol [BGP](/bgp/).

## Pitfalls

- **No cap on the metric.** Without the cap $\min(I, \cdot)$ in line L9, a destination that is cut off is never declared unreachable: in the line example the metrics grow by 2 every 2 rounds for ever. The test of a partition catches this.
- **Keeping the old route when the next hop raises its cost.** An incremental rule "replace only if smaller" for all neighbours is wrong: after a cost rise, the router keeps a stale metric. The rule must accept any change from the current next hop (RFC 2453, Section 3.9.2), or recompute from all stored vectors as in line L9.
- **Infinity too large.** A large $I$ makes the count to infinity longer. In a triangle $x, y, z$ with $w(x, y) = 4$, $w(y, z) = 1$, $w(x, z) = 50$, a rise of $w(x, y)$ to 60 takes 46 synchronous rounds before $y$ and $z$ settle on 51 and 50 toward $x$; with poison reverse it takes 2.
- **Timers in step.** Routers whose 30 second timers fall into step send their updates at the same moment and load the links in bursts. RIP requires a random offset on the timer (RFC 2453, Section 3.8).
- **Silent failures.** If a link fails without an interface event, only the 180 second timeout of line L4 removes the routes through it. Until then, traffic is lost.

## Implementations

The Python code is a discrete-event simulation with an integer clock, periodic timers with seeded jitter, triggered updates, timeouts, link failures, silent cuts and cost changes. The tests compare the tables with [Dijkstra](/dijkstra/) distances on seeded random graphs, follow the next hops to check that they are loop-free, and reproduce the round counts of this page.

## History

The ARPANET used a distributed Bellman-Ford method for routing from 1969 until it moved to link-state routing in 1979 and 1980. RIP descends from the routing protocol of the Xerox Network Systems and from the routed program of BSD Unix; Hedrick documented it as RFC 1058 in June 1988, with infinity 16, split horizon and triggered updates. Malkin's RIP version 2, RFC 2453 of November 1998, added subnet masks, next-hop fields and authentication. Garcia-Luna-Aceves's DUAL (1993) gave a distance-vector method that is loop-free at every instant, and Cisco's EIGRP uses it.

## References
