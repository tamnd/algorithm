---
tag: M7SS10
kind: technique
slug: split-horizon-poison-reverse
name: Split horizon with poison reverse
aliases:
- poisoned reverse
- split horizon with poisoned reverse
area: systems/networking-algorithms
level: intro
summary: "A distance-vector router sends infinity to the neighbour that is its next hop for a route. This stops counting to infinity between two routers, but loops of three or more can still count."
prereqs: [distance-vector-routing, count-to-infinity]
see_also: [path-vector-routing, bgp, link-state-routing, distributed-bellman-ford]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc1058
    title: C. Hedrick, Routing Information Protocol, RFC 1058, June 1988
    locator: Section 2.2.1 (split horizon, simple and with poisoned reverse) and Section 2.2.2 (the remark that poisoned reverse prevents loops of two gateways only, and that three gateways can still be engaged in mutual deception)
  - url: https://www.rfc-editor.org/rfc/rfc2453
    title: G. Malkin, RIP Version 2, RFC 2453, November 1998
    locator: Section 3.4.3 (split horizon and split horizon with poisoned reverse) and Section 3.4.4 (triggered updates)
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition, Pearson, 2021
    locator: Chapter 5, Section 5.2.2 (adding poisoned reverse, and the remark that loops of three or more nodes are not detected)
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition, Morgan Kaufmann, 2011
    locator: Chapter 3, Section 3.3.2 (split horizon and split horizon with poison reverse)
---

Split horizon with poison reverse is a rule for what a [distance-vector](/distance-vector-routing/) router tells each neighbour: for every destination whose next hop is that neighbour, the router sends the metric for "unreachable" (16 in RIP) instead of its real cost. Simple split horizon leaves such routes out of the message. Both stop the most common form of [count to infinity](/count-to-infinity/), in which two neighbours pass a stale route back and forth. They cost nothing in computation, and RIP uses them. They do not stop a stale route that circulates around a loop of three or more routers.

## In plain words

Suppose you ask a friend for the way to the station, and the friend's only way is to come to you and ask. Then the friend should not say "I know the way, it is two streets". If the friend says that, you may believe it after your own road closes, and the two of you then send each other in a circle.

Split horizon tells each router: do not tell a neighbour about a route that you learned from that neighbour. Poison reverse goes one step further: tell that neighbour, in so many words, "I cannot get there". The neighbour then knows at once that the route through you is no good.

## When it applies

- The protocol sends distances, not paths or maps. A router cannot see where a neighbour's cost came from.
- Each route has one next hop, and the router knows it, so it can tell which routes it learned from each neighbour.
- The links are point-to-point, or the router can address each neighbour with its own message. On a broadcast network where one message reaches all neighbours, the rule must be applied per interface, and it hides routes from routers on the same network that could use them.
- Failures and cost increases happen, and the protocol must not leave two routers pointing at each other.

## The template

```pseudo id=main
EXPORT(y, x, mode)                  ▷ the vector that router y sends to its neighbour x
L1  vec ← an empty vector
L2  for each destination t with entry (m, h) in D[y] do
L3      if LEARNED-FROM(y, t) = x and t ≠ y then      ▷ hole: the source of the route
L4          if mode = split then skip t                ▷ simple split horizon
L5          else vec[t] ← POISON                       ▷ hole: the unreachable metric, I
L6      else vec[t] ← m
L7  return vec
```

The hole LEARNED-FROM is the next hop $h$ in a distance-vector table. In a protocol with several equal-cost next hops it is the set of them, and the test becomes "$x$ is one of them". The hole POISON is the metric $I$ that the receiver treats as unreachable, so the receiver's relaxation $\min(I, w(x, y) + I) = I$ can never pick the route through $y$.

**What it guarantees.** Use the synchronous rounds of [distance-vector routing](/distance-vector-routing/), with next hop $h_r(x)$ after round $r$. If $h_r(x) = y$, then in round $r + 1$ router $x$ sends $I$ to $y$ (or nothing), so $y$ cannot pick $x$ and $h_{r+1}(y) \ne x$. Hence two routers never point at each other in two rounds in a row: a loop $x \leftrightarrow y$ that forms in some round is broken in the next one. And a cost that $y$ learned from $x$ is never sent back to $x$, so the exchange "$x$ raises by one, $y$ raises by one" of the line example cannot happen. The same argument gives no help for a loop $x_1 \to x_2 \to x_3 \to x_1$: each router hears the stale cost from a neighbour that is not its own next hop, so nothing is poisoned.

**Simple split horizon against poison reverse.** If the receiver recomputes its table from the last vector of each neighbour, a missing entry and an entry $I$ have the same effect. RIP does not recompute: it updates a route only when it hears about it (RFC 2453, Section 3.9.2). Under that rule, simple split horizon removes the false route only when the route times out, after 180 seconds, while poison reverse removes it with the next message. The price of poison reverse is a larger message, since every route goes to every neighbour.

## Classic examples

- **The line of three routers** in [count to infinity](/count-to-infinity/). $A - B - C$, link $B - C$ fails. Without the rule, $A$ and $B$ count up to 16 in 14 rounds. With it, $A$ sends $B$ the value 16 for $C$, because $A$'s route goes through $B$. So $B$ has no route at once, and both are at 16 after one round.
- **A cost increase.** In a triangle with $w(x, y) = 4$, $w(y, z) = 1$, $w(x, z) = 50$, a rise of $w(x, y)$ to 60 takes 46 synchronous rounds to settle without the rule and 2 with poison reverse: $z$ routes to $x$ through $y$, so it tells $y$ that its cost is infinite, and $y$ takes the link to $z$ only after $z$ has moved to its direct link.
- **The loop of three routers.** $A$, $B$, $C$ in a triangle, $C$ linked to the destination $D$, all costs 1. After $C - D$ fails, a false route travels round the triangle, and with poison reverse all three still need 14 rounds to reach 16. The table is in [count to infinity](/count-to-infinity/). RFC 1058 (Section 2.2.2) and Kurose and Ross give the same warning.
- **RIP.** [Distance-vector routing](/distance-vector-routing/) as RIP runs it uses simple split horizon or poison reverse together with triggered updates and the cap 16 (RFC 2453, Sections 3.4.3 and 3.4.4).
- **BGP inside one AS.** A [BGP](/bgp/) router does not pass a route that it learned from one internal peer to another internal peer. The AS_PATH check of [path-vector routing](/path-vector-routing/) is the full form of the idea: a router refuses any route that already passed through it, which removes loops of every length.

## Variations

- **Route poisoning.** When a route fails, the router keeps it for a while and sends it with metric $I$ to all neighbours, instead of deleting it quietly. RIP does this during its 120 second garbage-collection time.
- **Triggered updates.** Send a changed route at once instead of at the next 30 second timer. Combined with poison reverse, this removes a two-router loop in about one message delay.
- **Hold-down.** After a route becomes unreachable, refuse new routes to that destination for a fixed time. This also covers some longer loops, at the cost of delaying real repairs.
- **The feasibility condition of DUAL.** Accept a new next hop only if its reported cost is less than the router's own best cost since the last reset. This blocks loops of every length; see [count to infinity](/count-to-infinity/).

## Pitfalls

- **Expecting it to stop all loops.** The guarantee covers two routers only. A network with triangles needs a small infinity, hold-down, DUAL, or a [link-state](/link-state-routing/) or path-vector protocol.
- **Poisoning the router's own address.** The test in line L3 must skip $t = y$, whose next hop is $y$ itself. Otherwise a mistaken comparison can poison the route to the router.
- **Simple split horizon with an incremental receiver.** If the receiver changes a route only when it hears about it, a route that a neighbour silently stops sending stays in use until its timeout. Use poison reverse in that case.
- **Split horizon on a broadcast network.** If one message on a shared network reaches several routers, a route learned from one of them is hidden from all of them. Apply the rule per neighbour where the medium allows it.

## References
