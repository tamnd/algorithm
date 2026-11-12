---
tag: 6GA09P
kind: algorithm
slug: spanning-tree-protocol
name: Spanning Tree Protocol
aliases:
- IEEE 802.1D
- Perlman's spanning tree algorithm
area: systems/networking-algorithms
level: intro
summary: "Bridges elect the bridge with the least id as root. Each takes its cheapest port toward the root, each LAN gets one designated port, and all other ports block, which leaves a loop-free tree."
solves: [routing-problem]
model: synchronous-model
complexity:
  vars: {n: the number of bridges, m: the number of ports, D: the depth of the final tree in bridges}
  time: {worst: O(D)}
  messages: {worst: O(D m)}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1985
  people: [Radia Perlman]
  note: Radia Perlman designed the algorithm at Digital Equipment Corporation and published it at SIGCOMM 1985. It became IEEE 802.1D; the rapid version (RSTP, 802.1w) replaced it in 802.1D-2004.
prereqs: [spanning-tree, shortest-path-tree, synchronous-model]
see_also: [distributed-spanning-tree, minimum-spanning-tree, flooding, count-to-infinity, distance-vector-routing, link-state-routing, routing-problem, broadcast-problem]
sources:
  - paper: "Radia Perlman, An algorithm for distributed computation of a spanning tree in an extended LAN, ACM SIGCOMM Computer Communication Review 15(4), 1985, pages 44 to 53"
    locator: the election of the root by least id, the choice of root port and designated bridge per LAN, and the timers (page numbers not checked)
  - paper: "IEEE Std 802.1D-2004, IEEE Standard for Local and Metropolitan Area Networks, Media Access Control (MAC) Bridges, IEEE, 2004"
    locator: the Rapid Spanning Tree Protocol clause, which carries the priority vectors (root id, root path cost, designated bridge id, designated port id, port id) and the port roles (clause number not checked)
  - book: isbn:9780201634488
    title: Radia Perlman, Interconnections, Bridges, Routers, Switches, and Internetworking Protocols, second edition, Addison-Wesley, 2000
    locator: Chapter 3, transparent bridges and the spanning tree algorithm (chapter number not checked)
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition, Morgan Kaufmann, 2012
    locator: Chapter 3, the section on bridges and LAN switches, spanning tree algorithm (section number not checked)
---

The Spanning Tree Protocol (STP) lets the bridges (switches) of a local network turn off just enough of their ports that the network has no loops, while every LAN segment stays reachable. Radia Perlman designed it in 1985 and it became IEEE 802.1D. The bridges elect the one with the least bridge id as the root. Each other bridge keeps the port with the cheapest path to the root (its root port), and each LAN keeps the one port that offers the cheapest path to the root (its designated port). All other ports block. Ties go to the lower bridge id and then the lower port id, so the result is one fixed tree: the [shortest-path tree](/shortest-path-tree/) from the root, with these tie-breaks. In a stable network it forms within $O(D)$ rounds of messages, where $D$ is the depth of the tree.

## In plain words

Bridges join LANs together. If the bridges form a loop, a broadcast frame goes around the loop for ever and multiplies, and the network stops working. So the bridges must agree to switch off some ports.

They do it like this. Every bridge has a number. The bridge with the smallest number is the boss, the root. Every other bridge finds its cheapest way to the root and keeps that port open. On each LAN, the bridge that is closest to the root carries the traffic for that LAN. Every other port stays closed. The bridges learn all this by sending small messages that say "I think the root is X, and I am this far from it". The open ports then form a tree.

## The problem

A bridged LAN is a bipartite graph of bridges and LANs. A port joins one bridge to one LAN; it has an id that is unique on its bridge and a path cost (802.1D suggests costs that fall with the link speed). Bridges forward frames between their ports and learn where stations are, but a frame has no hop count, so a cycle of bridges makes broadcast frames loop and multiply. The task is to choose a set of forwarding ports such that the bridges and LANs, joined by these ports, form a spanning tree of each connected component, using only messages between bridges on the same LAN, and to repair the tree when a bridge or link fails.

## The algorithm

Bridges send configuration BPDUs (bridge protocol data units) that carry a *priority vector* (root id, root path cost, sender bridge id, sender port id) and a message age. Vectors are compared in that order, and smaller is better. Each port stores the best vector it has heard on its LAN. The pseudocode runs at bridge $b$ once per round (each hello time).

```pseudo id=main
STP-ROUND(b)                        ▷ info[p]: stored vector of port p; c(p): its cost
L1  drop info[p] on every port p whose message age has reached MAXAGE
L2  best ← (b, 0, b, 0, 0);  rootport ← nil
L3  for each port p of b with info[p] = (R, C, S, P) do
L4      if (R, C + c(p), S, P, id(p)) < best then best ← that vector;  rootport ← p
L5  (root, cost) ← the first two entries of best
L6  each port p ≠ rootport is designated if info[p] is nil or (root, cost, b, id(p)) < info[p], else blocked
L7  if b = root, or a BPDU reached rootport in the last round, then for each designated port p do
L8      send (root, cost, b, id(p)) on p, with age 0 if b = root, else the age received on rootport plus 1
    ▷ on receipt of a BPDU v on port q:
L9  if info[q] is nil, or v < info[q], or v comes from the same bridge and port as info[q] then
L10     info[q] ← v;  restart its age at the age carried in v
```

Lines L2 to L5 elect the root and the root port: the bridge believes in the least root id that it has heard, and it reaches that root through the port with the least (cost, neighbour bridge, neighbour port, own port). Line L6 makes a port designated when this bridge offers its LAN a better vector than anything else heard there. Lines L7 and L8 relay the root's hello outward through the tree, one hop per round, adding one to the age at each hop. Line L9 lets a vector replace a worse one, and also lets the current designated bridge replace its own vector by a worse one when its path to the root gets longer.

In a real bridge, a port does not forward as soon as it becomes designated or root. Classic 802.1D moves it through the *listening* and *learning* states, each lasting the forward delay (15 s by default), so that the old tree has time to block its ports before the new tree opens. The tree is also refreshed all the time: the root sends a BPDU every hello time (2 s by default), and information that is not refreshed for MAXAGE (20 s by default) is dropped.

## Example

Three bridges with ids 1, 2 and 3 join three LANs in a triangle: bridges 1 and 2 share LAN $a$, bridges 1 and 3 share LAN $b$, and bridges 2 and 3 share LAN $c$. Every port has cost 1.

| round | bridge 1 | bridge 2 | bridge 3 |
|---|---|---|---|
| 1 | root 1, cost 0 | root 2, cost 0 | root 3, cost 0 |
| 2 | root 1, cost 0 | root 1, cost 1, root port on $a$ | root 1, cost 1, root port on $b$ |
| 3 | same | same | same; its port on $c$ blocks |

In round 1, each bridge believes it is the root and sends its own vector on every port. At the end of round 1, bridge 2 has heard $(1, 0, 1, \cdot)$ on $a$, and bridge 3 has heard it on $b$. In round 2, both accept root 1 at cost 1 and send $(1, 1, 2, 2)$ and $(1, 1, 3, 2)$ on LAN $c$. Both offers have cost 1, so in round 3 bridge 2 wins LAN $c$ by its lower id: its port on $c$ stays designated, and bridge 3 blocks its port on $c$. The forwarding ports are 1 on $a$, 1 on $b$, 2 on $a$, 3 on $b$ and 2 on $c$: a tree on the six nodes. If bridge 2 fails, bridge 3 stops hearing $(1, 1, 2, 2)$ on $c$, the vector ages out, and its port on $c$ becomes designated again.

## Correctness

The full proof is in [the correctness proof](#proof-correctness). It covers a network that does not change, with no lost messages.

**No false information beats the truth.** Let $r$ be the least bridge id in a connected component and $d(x)$ the least cost from $r$ to bridge $x$. Every root id ever sent is the id of a real bridge, so it is at least $r$. A bridge that claims root $r$ at cost $C$ got $C$ by adding a port cost to a cost that another bridge on that LAN claimed, so by induction $C \ge d(x)$. Thus no vector is ever better than the true one.

**The truth spreads one level per round.** The root knows it is the root from the first round. The designated bridge of a LAN offers the least vector on it, so every other port on that LAN accepts the vector and nothing replaces it. By induction on depth, a bridge at depth $k$ has the right root and cost from round $k + 1$, provided $D$ is below MAXAGE so that no true vector ages out.

**The roles form a tree.** After $D + 2$ rounds, each LAN has exactly one designated port and each bridge except the root has exactly one root port. Point each bridge to its root LAN and each LAN to its designated bridge. The cost to the root falls strictly along these pointers, so they have no cycle, and a graph in which every node except one has one parent, with no cycle, is a spanning tree.

## Complexity

With synchronous rounds and no failures, the protocol converges in $D + 2$ rounds, where $D \le n$ is the depth of the final tree. In each round a bridge sends one BPDU per designated port, so at most $m$ BPDUs per round over $m$ ports, and $O(D m)$ before the tree is stable. Each port stores one vector, so the space is $O(m)$ in all and $O(\text{ports})$ per bridge. In a real network the rounds are hello times of 2 s, and after a failure the old information must first age out, so classic STP needs up to MAXAGE plus twice the forward delay, about 50 s with the default timers, before traffic flows again.

| measure | bound | case |
|---|---|---|
| rounds to converge | $D + 2$ | fixed network, synchronous rounds |
| BPDUs per round | at most $m$ | one per designated port |
| storage | $O(m)$ | one vector per port |
| recovery after a failure | about MAXAGE + 2 forward delays | classic 802.1D timers, about 50 s |

## Properties

- **A shortest-path tree, not a minimum spanning tree.** Each bridge reaches the root at least cost, but the total cost of the tree is not minimal. Compare [distributed MST algorithms](/distributed-spanning-tree/) such as GHS, which build a [minimum spanning tree](/minimum-spanning-tree/) and have no root to choose.
- **One fixed answer.** The tie-breaks by bridge id and port id make the tree unique for given ids and costs, so all bridges agree without a vote.
- **Local messages only.** BPDUs go only to the bridges on the same LAN, and each carries a constant amount of data.
- **Soft state.** Information lives only as long as the root keeps refreshing it, so a failed bridge's information disappears without an explicit withdrawal.
- **All traffic shares one tree.** Ports that block carry no data, so their capacity is wasted, and traffic between two leaves can take a long way round through the root.

## Variants and improvements

- **Rapid Spanning Tree Protocol (RSTP, IEEE 802.1w).** It keeps the vectors and roles but adds alternate and backup ports, explicit proposal and agreement handshakes on point-to-point links, and edge ports. A port can move to forwarding in about one round trip instead of after two forward delays. 802.1D-2004 replaced classic STP by RSTP.
- **Multiple Spanning Tree Protocol (MSTP, IEEE 802.1s, now in 802.1Q).** It runs several trees, one per group of VLANs, so that ports blocked in one tree can carry traffic of another.
- **Per-VLAN spanning tree.** Vendor variants run a separate tree per VLAN.
- **Shortest path bridging (IEEE 802.1aq) and TRILL.** These replace the single tree by [link-state routing](/link-state-routing/) among bridges, so each frame takes a shortest path and all links carry traffic. Perlman was also a designer of TRILL.

## When to use it

Use STP or RSTP in any Ethernet network that has redundant links between switches, so that a cabling mistake or a backup link does not create a loop. It is simple and needs no configuration beyond bridge priorities. In large or fast networks, use RSTP at least, choose the root by setting its priority, and consider MSTP, shortest path bridging, or a routed (layer 3) design when the wasted capacity of blocked links or the slow recovery matters.

## Pitfalls

- **Root placement by accident.** The root is the bridge with the least id, and the id starts with a configurable priority and then the MAC address. If nobody sets priorities, an old, slow switch with a low MAC address can become the root, and all traffic crosses it.
- **Forwarding too early.** A port that forwards before the old tree has blocked its ports can create a temporary loop. This is the reason for the listening and learning states.
- **One-way links.** If a link carries frames in one direction only, a bridge stops hearing BPDUs, makes its port designated, and opens a loop. Features such as loop guard and unidirectional link detection exist for this.
- **Topology changes flush tables.** After a change, bridges shorten the aging time of their address tables, which causes a burst of flooded frames.
- **Too deep a network.** Message age grows by one per hop, so the tree must have fewer levels than MAXAGE allows; 802.1D recommends a diameter of at most 7 bridges with the default timers.
- **Not a routing protocol for loops in general.** STP removes loops by not using links. It does not balance load and does not find a best path between two bridges, only to the root.

## Implementations

The Python code simulates the protocol in synchronous rounds on a set of ports, each given as (bridge, LAN, port id, cost). In each round every live bridge runs lines L1 to L6, then sends BPDUs as in lines L7 and L8, and receivers apply lines L9 and L10. A second function computes the expected tree directly: the least id as root, Dijkstra for root path costs, the least (cost, bridge, port) as the designated port of each LAN, and the 802.1D order for root ports. The tests run the protocol on seeded random bridged LANs, with several ports of one bridge on the same LAN in some cases, and check that it ends with the same root, costs and port roles as the direct computation, that the forwarding ports form a spanning forest with the same components as the network, and that the tree is right again after a bridge, often the root, fails and its information ages out.

## History

Bridges that learn station addresses appeared at Digital Equipment Corporation in the early 1980s, and loops in bridged networks had to be prevented without changing the hosts or the frame format. Radia Perlman designed the spanning tree algorithm for this and published it at SIGCOMM 1985; she summed it up in a short poem, "Algorhyme". The algorithm became the core of IEEE 802.1D. Slow recovery led to the Rapid Spanning Tree Protocol, 802.1w, published in 2001 and folded into 802.1D-2004, and the need to use all links led to MSTP and later to shortest path bridging and TRILL.

## References
