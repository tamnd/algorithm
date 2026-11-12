---
tag: NQ1A74
kind: algorithm
slug: aodv
name: AODV
aliases:
- ad hoc on-demand distance vector
- AODV routing
area: systems/networking-algorithms
level: advanced
summary: "An ad hoc routing protocol that floods a route request only when a route is needed, and keeps next-hop tables with destination sequence numbers, which keep the routes loop-free."
solves: [ad-hoc-routing]
model: asynchronous-model
complexity:
  vars: {n: the number of nodes, m: the number of links}
  time: {worst: O(n + m), expected: O(n + m)}
  space: {extra: O(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1999
  people: [Charles E. Perkins, Elizabeth M. Royer, Samir R. Das]
  note: Perkins and Royer presented AODV at WMCSA 1999 as an on-demand successor of DSDV. The IETF published it as the experimental RFC 3561 in 2003, with Das as a third author.
prereqs: [ad-hoc-routing, distance-vector-routing, flooding]
see_also: [count-to-infinity, distributed-bellman-ford, geographic-routing, gpsr, link-state-routing, broadcast-problem]
sources:
  - paper: doi:10.1109/MCSA.1999.749281
    title: "Charles E. Perkins and Elizabeth M. Royer, Ad-hoc on-demand distance vector routing, Second IEEE Workshop on Mobile Computing Systems and Applications (WMCSA), 1999"
    locator: pages 90 to 100 (route requests and replies, sequence numbers, route maintenance, the loop freedom argument)
  - url: "https://www.rfc-editor.org/rfc/rfc3561"
    title: "C. Perkins, E. Belding-Royer and S. Das, RFC 3561, Ad hoc On-Demand Distance Vector (AODV) Routing, 2003"
    locator: Section 6 (6.1 sequence numbers, 6.5 processing a RREQ, 6.6 generating a RREP, 6.7 receiving a RREP, 6.11 route error messages)
  - paper: doi:10.1145/190314.190336
    title: "Charles E. Perkins and Pravin Bhagwat, Highly dynamic destination-sequenced distance-vector routing (DSDV) for mobile computers, ACM SIGCOMM 1994"
    locator: pages 234 to 244 (destination sequence numbers and the loop freedom argument that AODV inherits)
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition, Pearson, 2011
    locator: Chapter 5, Section 5.2 (routing in ad hoc networks, a worked AODV example)
---

AODV (ad hoc on-demand distance vector) is a routing protocol for [ad hoc networks](/ad-hoc-routing/). A node keeps no route until it needs one. Then it [floods](/flooding/) a route request (RREQ); every node that forwards the request learns a route back to the source, and the destination, or a node with a recent enough route to it, sends a route reply (RREP) back along that reverse path, which sets up the forward route hop by hop. Each node keeps only a next hop and a hop count per destination, as in [distance vector routing](/distance-vector-routing/). What keeps the routes free of loops is a *destination sequence number*: each route carries a number that only the destination can raise, a node prefers routes with larger numbers, and a broken route is advertised with a larger number than the route it replaces.

## In plain words

You want to send a letter to someone in a crowd, and nobody has a map. You shout "who can reach Dana?" and everyone who hears it shouts it on, remembering who told them, so each person knows the way back to you. When the shout reaches Dana, or someone who recently learned the way to Dana, the answer goes back along that trail of people, and each one on it notes "for Dana, hand it to the person who just told me". If someone on the way leaves, the people who relied on them pass on a warning. Every piece of route news carries a freshness stamp from Dana, so nobody trusts old news over new.

## The problem

Nodes form a wireless network whose links appear and break as they move. Each node can send to its current neighbors only, and nobody knows the whole graph. When a node has packets for a destination, it needs a next hop toward it, and every node on the way needs one too. The routes must not form loops even while links change and messages are delayed or lost, and the protocol should send no control traffic for destinations that nobody uses. This is the reactive form of [ad hoc routing](/ad-hoc-routing/).

## The algorithm

Every node $u$ has its own sequence number $\mathit{seq}[u]$ and, for each destination it knows, an entry with the next hop, the hop count, the destination's sequence number as last heard, and a valid flag. One rule decides whether a message about destination $d$ with number $s$ and $h$ hops replaces the current entry: it does if there is no entry, if $s$ is larger, or if $s$ is equal and the entry is invalid or has more hops. The rule is applied at lines L3 and L7.

```pseudo id=main
AODV(s, d)                                         ▷ s has data for d and no valid route
L1  seq[s] ← seq[s] + 1; broadcast RREQ(s, seq[s], new id, d, last known seq of d or 0, hops 0)
L2  on RREQ at u from v: if (s, id) was seen before then drop it; else hops ← hops + 1
L3      update u's route to s to next hop v by the rule
L4      if u = d then seq[d] ← max(seq[d], requested seq); send RREP(d, seq[d], hops 0) toward s
L5      else if u has a valid route to d with seq ≥ requested seq then send RREP(d, that seq, its hops) toward s
L6      else broadcast the RREQ with requested seq ← max(requested seq, u's seq for d)
L7  on RREP at u from v: hops ← hops + 1; update u's route to d to next hop v by the rule
L8      if the route was updated and u ≠ s then send the RREP on along u's route to s
L9  on a broken link (u, v): for each valid route of u through v: mark it invalid, seq ← seq + 1; broadcast RERR(d, seq)
L10 on RERR(d, r) at u from v: if u's route to d is valid and goes through v then mark it invalid, seq ← max(seq, r); broadcast RERR(d, seq)
```

"Toward $s$" means to the next hop of the reverse route that line L3 just set or kept. Line L1 raises the source's own number, so its reverse routes are fresh. Line L4 is the only place where a destination's number grows, apart from the increments of line L9 on behalf of a broken route. The RFC sends an RERR only to the *precursors* of a route, the neighbors that use it, and it also keeps hello messages, route lifetimes, expanding ring searches and gratuitous replies; they do not change the core.

## Example

**Discovery on a line.** Nodes $0 - 1 - 2 - 3 - 4$, all sequence numbers $0$. Node $0$ wants a route to $4$.

1. $0$ raises its number to $1$ and sends RREQ$(0, 1, \ldots, 4, 0, 0)$ to $1$.
2. $1$ sets the reverse route "to $0$ via $0$, 1 hop, number 1" and rebroadcasts to $0$ and $2$; $0$ drops its own request. Nodes $2$ and $3$ do the same, with 2 and 3 hops back to $0$.
3. $4$ gets the request with 4 hops, keeps its number $0$ (the request asked for $0$, meaning unknown), and sends RREP$(4, 0, 0)$ to $3$.
4. The reply goes $3 \to 2 \to 1 \to 0$. Each node sets "to $4$ via the sender" with $1, 2, 3, 4$ hops.

The discovery took $11$ messages: $7$ copies of the request and $4$ hops of the reply. Now $0$ and $4$ have routes both ways.

**A break and a repair on a ring.** Six nodes in a ring $0 - 1 - 2 - 3 - 4 - 5 - 0$. Node $0$ finds the route $0, 1, 2$, with destination number $0$. Then the link $1 - 2$ fails.

1. Node $1$ marks its route to $2$ invalid, raises its number to $1$, and sends RERR$(2, 1)$ to $0$.
2. Node $0$ uses $1$ as its next hop, so it marks its route invalid with number $1$.
3. Node $0$ asks again, now with requested number $1$. Nodes $1$ and $5$ have no valid route with a number $\ge 1$, so they forward.
4. Node $2$ raises its own number to $1$ and replies; the reply travels $3, 4, 5, 0$.

The new route is $0, 5, 4, 3, 2$ with number $1$, and node $1$ is left with an invalid route, which it will not offer to anyone.

**A lost error message.** On the line $0 - 1 - 2 - 3$, all nodes have routes to $3$. The link $2 - 3$ fails, and the RERR from $2$ to $1$ is lost. Node $2$ asks for $3$ with requested number $1$. Node $1$ still has a valid route to $3$, via $2$, but with number $0 < 1$, so it does not answer. No route is found, which is correct: $3$ is unreachable. A distance vector protocol without sequence numbers answers from node $1$, and $2$ and $1$ then point at each other, the start of [counting to infinity](/count-to-infinity/).

## Correctness

The safety property is that the valid entries for any destination never form a loop. For a valid entry of node $i$ with next hop $j$, call $(s_i, h_i)$ its number and hop count, and let the destination itself count as valid with its own number and 0 hops. The invariant is: $j$'s number is larger than $s_i$, or it is equal, $j$'s route is valid, and $h_j < h_i$. Along a path of valid entries the pair $(s, -h)$ then increases strictly, so no node can repeat.

The invariant holds because every piece of state moves only forward. A route request or reply carries a pair that its sender has, or is behind, at the time it is sent. A valid route is only replaced by one with a larger number, or with the same number and fewer hops. A route is never invalidated without a larger number: line L9 adds one, and line L10 takes a number from the next hop that is larger than the one the route was learned with, because the next hop raised its own number when it invalidated. That last step needs the link to deliver messages in order, so that the error cannot overtake the reply that set the route. Lost messages do no harm. The proof file below carries out this induction over all events, and the tests check the invariant after every delivery in random topologies with link failures, new links and lost messages.

Loop freedom does not promise delivery. A request can be lost or reach only nodes with stale routes; the source then repeats it with a larger number, and in a network that stops changing a repeated request reaches the destination along the flood.

## Complexity

- **Messages per discovery.** A flood sends each request once per node, $n$ broadcasts, which is up to $2m$ link transmissions, plus a reply of one message per hop. So a discovery costs $O(n + m)$ messages. Expanding ring searches, with a limited hop count at first, cut this when the destination is near.
- **Time.** On the order of twice the hop distance in message delays: the request goes out, the reply comes back.
- **State.** A node keeps one entry per active destination plus a cache of recently seen request ids: $O(n)$ in the worst case, often much less.
- **Repair.** A broken link costs one RERR broadcast per node that loses a route, and a new discovery if the source still has traffic.

## Properties

- **On demand.** No control traffic for idle destinations. The first packet of a flow waits for the discovery.
- **Loop-free at all times**, not only after the network settles, by the sequence number argument.
- **No counting to infinity**, since a node never accepts an old route that passes through itself.
- **Hop count only.** Routes minimize hops among the fresh enough ones; there is no link cost, which ignores link quality.
- **Symmetric links assumed.** The reply travels the reverse path of the request, so a one-way link breaks discovery; the RFC adds blacklists for this case.
- **Stale replies.** An intermediate node answers from its cache, which saves a flood but can give a longer path than a fresh one.

## Variants and improvements

- **DSDV.** The proactive ancestor: distance vectors with destination sequence numbers, sent periodically to all neighbors.
- **DSR.** Dynamic source routing floods requests too, but returns the whole path and puts it in each packet; there are no per-hop tables.
- **AOMDV.** Keeps several loop-free and link-disjoint paths per destination, so a break does not always need a new flood.
- **LOADng and AODVv2.** Later IETF work simplified AODV for low-power networks and dropped intermediate replies.
- **HWMP.** The path selection of IEEE 802.11s mesh networks uses an AODV-like on-demand mode next to a proactive tree mode.
- **Link metrics.** Replacing hop count by a link quality metric such as the expected number of transmissions improves throughput; the update rule then compares costs instead of hops.

## When to use it

Use AODV when nodes move, traffic flows between relatively few pairs at a time, and node positions are unknown. If most nodes talk to most others all the time, a proactive protocol such as OLSR, a [link state](/link-state-routing/) design, spends its overhead better and has no discovery delay. If positions are known, [geographic routing](/geographic-routing/) needs no route state at all. In a fixed wired network, standard [distance vector](/distance-vector-routing/) or link state routing is simpler.

## Pitfalls

- **Raising sequence numbers in the wrong place.** Only the destination may raise its own number in a reply, and intermediate nodes may raise a number only when they invalidate a route. A node that invents a larger number for a valid route can attract traffic and create loops or black holes.
- **Accepting an RERR from any neighbor.** An error must come from the next hop of the route; otherwise a neighbor that is not on the route can tear it down, and the larger number it carries may block good replies.
- **Forgetting the duplicate cache.** Without the request id cache, a flood never ends.
- **Equal numbers, more hops.** A valid route with the same number must only be replaced by a shorter one. Allowing a longer one breaks the invariant.
- **Broadcast storms.** In dense networks the flood of a request causes many collisions on the [CSMA/CA](/csma-ca/) channel; jitter before rebroadcasting and expanding ring searches help.
- **Sequence number wraparound.** Real numbers are 32-bit and compared with modular arithmetic, so a node that restarts must wait or use a fresh number.

## Implementations

## History

Charles Perkins and Pravin Bhagwat introduced destination sequence numbers in DSDV in 1994 to make distance vectors loop-free for mobile hosts. Perkins and Elizabeth Royer turned it into an on-demand protocol, AODV, in 1999, at the same time as the MANET working group of the IETF was comparing DSR, AODV, TORA and others. AODV was published as the experimental RFC 3561 in 2003. Its ideas live on in the routing of IEEE 802.11s mesh networks, Zigbee and later low-power protocols.

## References
