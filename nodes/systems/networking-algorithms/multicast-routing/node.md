---
tag: XSEK7Q
kind: problem
slug: multicast-routing
name: Multicast routing
aliases:
- multicast tree construction
- IP multicast routing
area: systems/networking-algorithms
level: advanced
summary: "Deliver each packet from a source to a changing group of receivers, one copy per link of a tree. The cheapest tree is a Steiner tree; protocols use shortest-path or shared trees."
prereqs: [routing-problem, shortest-path-tree, flooding]
see_also: [steiner-tree-problem, distance-vector-routing, link-state-routing, spanning-tree-protocol, network-coding, bimodal-multicast, epidemic-broadcast-tree, broadcast-problem]
sources:
  - paper: "Stephen E. Deering and David R. Cheriton, Multicast routing in datagram internetworks and extended LANs, ACM Transactions on Computer Systems 8(2), 1990, pages 85 to 110"
    locator: the host group model, and the multicast extensions of distance-vector routing (reverse path forwarding with pruning) and of link-state routing
  - paper: "Yogen K. Dalal and Robert M. Metcalfe, Reverse path forwarding of broadcast packets, Communications of the ACM 21(12), 1978, pages 1040 to 1048"
    locator: reverse path forwarding and its extended form, which forwards only to neighbours that use the node as their path back to the source
  - url: https://www.rfc-editor.org/rfc/rfc1075
    title: D. Waitzman, C. Partridge and S. Deering, Distance Vector Multicast Routing Protocol, RFC 1075, November 1988
    locator: the use of RIP-style distances to the source for reverse path tests, and the pruning of branches with no members
  - url: https://www.rfc-editor.org/rfc/rfc7761
    title: B. Fenner, M. Handley, H. Holbrook, I. Kouvelas, R. Parekh, Z. Zhang and L. Zheng, Protocol Independent Multicast, Sparse Mode (PIM-SM), Protocol Specification (Revised), RFC 7761, March 2016
    locator: Section 3 (the shared tree rooted at the rendezvous point, source registration, and the switch to the shortest-path tree of a source; section number not checked)
  - paper: "Tony Ballardie, Paul Francis and Jon Crowcroft, Core based trees (CBT), an architecture for scalable inter-domain multicast routing, ACM SIGCOMM 1993"
    locator: one shared bidirectional tree per group, built by joins toward a core router (page numbers not checked)
  - paper: "Makoto Imase and Bernard M. Waxman, Dynamic Steiner tree problem, SIAM Journal on Discrete Mathematics 4(3), 1991, pages 369 to 384"
    locator: the greedy online rule, connecting each new receiver to the tree by a shortest path, is O(log k)-competitive, and no online rule is better up to a constant (page numbers not checked)
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition, Morgan Kaufmann, 2011
    locator: Chapter 4, the section on multicast (DVMRP, PIM, source-specific multicast; section number not checked)
---

Multicast routing delivers a packet from one source to a group of receivers, so that each link carries at most one copy and each receiver gets the packet once. The forwarding state forms a tree: copies split only where the paths to receivers part. Receivers join and leave at any time, and the sender does not know who they are. The problem has two main goals that conflict. A [shortest-path tree](/shortest-path-tree/) from the source gives each receiver the least delay. A tree of least total cost uses the fewest links, but finding it is the [Steiner tree problem](/steiner-tree-problem/), which is NP-hard. Practical protocols build shortest-path trees with reverse path forwarding (DVMRP, PIM-DM, PIM-SSM) or one shared tree per group through a meeting point (CBT, PIM-SM), and they trade router state against path quality.

## In plain words

A radio station sends one program to many listeners. It could send a separate copy to every listener, but then the links near the station carry the same data thousands of times. Multicast sends one copy down each link and copies it only where the roads to the listeners split, like the branches of a tree.

The hard parts are these. Listeners come and go, so the tree must grow and shrink. Routers do not want to store much for each group. And the tree that uses the fewest links is hard to find, so most networks use a simpler tree: each listener's shortest road back to the station, or a tree through a fixed meeting point.

## Definition

**Input.** A graph $G = (V, E)$ of routers and links with costs $w(e) > 0$, a source $s$, and a group $R \subseteq V$ of receivers (the routers with members on their LANs). $R$ changes over time by join and leave events. Many sources can send to one group.

**Output.** For each router, forwarding state for each pair (source, group) or (any source, group): the interface on which a packet is expected and the set of interfaces to which it is copied. Following this state, a packet from $s$ must reach every router of $R$ exactly once and must not loop. The links used form a tree $T$ that contains $s$ and $R$.

**Goals.** The main measures are:

- **path cost**: the cost from $s$ to each receiver along $T$, compared with the distance $\delta(s, r)$;
- **tree cost**: the total cost $w(T)$ of the links that carry a copy;
- **state**: the number of entries per router, per group or per (source, group) pair;
- **control traffic and join delay**: the work to keep $T$ right as $R$ changes, and the time until a new member gets packets;
- **traffic concentration**: how much traffic of many groups crosses the same links.

## Variants

- **Source trees against shared trees.** A source tree is rooted at one sender, often its shortest-path tree. A shared tree serves all senders of a group: it is rooted at a core or rendezvous point (RP), and senders send to the root. A shared tree needs state per group instead of per (source, group), but paths are longer and traffic meets at the root.
- **Dense mode against sparse mode.** Dense-mode protocols assume members are everywhere: they flood packets along reverse paths and prune branches with no members (DVMRP, PIM-DM). Sparse-mode protocols assume few members: routers send explicit joins toward the source or the RP (PIM-SM, CBT).
- **Any-source against source-specific multicast.** In source-specific multicast (SSM, RFC 4607), a receiver joins the pair (source, group), so the network only needs source trees and no RP.
- **Minimum-cost trees.** The tree that minimizes $w(T)$ for a fixed $R$ is a minimum Steiner tree. With a bound on the delay to each receiver, it is the constrained Steiner tree problem. With joins and leaves over time, it is the online (dynamic) Steiner tree problem.
- **Broadcast.** With $R = V$, the problem is network-level broadcast, a special case of the distributed [broadcast problem](/broadcast-problem/).
- **Overlay and gossip multicast.** Hosts can build the tree among themselves at the application layer, or give up the tree and spread packets by gossip, as in [bimodal multicast](/bimodal-multicast/) and [epidemic broadcast trees](/epidemic-broadcast-tree/). These trade some redundant traffic for robustness and need no support from routers.

## Examples

**Flooding against reverse paths.** Take a source $s$ and routers $a, b, c, d$ with links $s - a$, $s - b$, $a - b$, $a - c$, $b - d$ and $c - d$, all of cost 1. So $n = 5$ and $m = 6$. The paths back to $s$ are $a \to s$, $b \to s$, $c \to a \to s$ and $d \to b \to s$.

| method | copies sent per packet | copies accepted |
|---|---|---|
| [flooding](/flooding/), with duplicate detection | 8 | 4 |
| reverse path forwarding | 8 | 4 |
| reverse path broadcasting | 4 | 4 |
| shortest-path tree pruned to $R = \{c\}$ | 2 | 2 |

In flooding, every router forwards the first copy it sees on all its other links, so $s$ sends 2 copies, and $a, b, c, d$ send 2, 2, 1 and 1. That is $2m - n + 1 = 8$ copies, and $2(m - n + 1) = 4$ of them are duplicates; the routers must keep per-packet state to drop them. Reverse path forwarding (Dalal and Metcalfe, 1978) sends the same 8 copies but needs no such state: a router accepts a packet only if it arrives on its own link toward the source. For example $a$ drops the copy from $b$. Reverse path broadcasting forwards a packet only to the neighbours whose path back to $s$ runs through the router, so it sends one copy per tree link, $n - 1 = 4$. If only $c$ has members, $d$ and then $b$ send prunes, and each packet crosses only $s - a$ and $a - c$.

Without duplicate detection, plain flooding never stops in a graph with a cycle. On a 4-cycle with one chord, the number of copies in flight at each hop from one packet grows as 3, 4, 6, 10, 14, 22, 34, 50.

**Shortest-path tree against Steiner tree.** Let $s$ have a link of cost 1 to each of $k$ receivers $r_1, \dots, r_k$, and let $r_i - r_{i+1}$ have cost $\varepsilon$. The shortest-path tree uses the $k$ direct links and costs $k$. The Steiner tree uses one direct link and the chain, with cost $1 + (k - 1)\varepsilon$. So the shortest-path tree can cost about $k$ times the minimum, while the Steiner tree makes $r_k$ wait about $1 + (k - 1)\varepsilon$ instead of 1.

## Known algorithms

| method | tree | state per router | notes |
|---|---|---|---|
| reverse path forwarding (Dalal, Metcalfe 1978) | broadcast on reverse shortest paths | none per packet | $2m - n + 1$ copies, each router accepts one |
| reverse path broadcasting and multicasting with pruning | source shortest-path tree | per (source, group) | flood and prune; DVMRP (RFC 1075), PIM-DM |
| link-state multicast (MOSPF, RFC 1584) | source shortest-path tree | per (source, group) | members flooded in the link-state database; each router computes the tree |
| core based trees (Ballardie, Francis, Crowcroft 1993) | shared bidirectional tree at a core | per group | joins travel toward the core |
| PIM-SM (RFC 7761) | shared tree at the RP, then optional source trees | per group, plus per (source, group) after a switch | receivers join the RP tree; a router may join the source's tree when traffic is high |
| PIM-SSM (RFC 4607) | source shortest-path tree | per (source, group) | joins go straight to the known source |
| Steiner tree approximations | near minimum-cost tree | central computation | MST of the metric closure gives factor 2; better factors exist |
| greedy online Steiner (Imase, Waxman 1991) | grows by shortest paths | per group | $O(\log k)$-competitive for $k$ joins |

Deering and Cheriton (1990) set out the model used on the Internet: hosts join a group address without knowing the senders or other members, routers learn local members with a membership protocol (IGMP for IPv4), and routing protocols extend [distance-vector routing](/distance-vector-routing/) and [link-state routing](/link-state-routing/) to build the trees. DVMRP follows the distance-vector extension. PIM is "protocol independent" because it uses the unicast routing table, whatever protocol built it, for its reverse path tests.

## Bounds

- **Broadcast.** Any method needs at least $n - 1$ transmissions per packet on point-to-point links, and reverse path broadcasting reaches this bound. Flooding with duplicate detection and plain reverse path forwarding send $2m - n + 1$, which is $2(m - n + 1)$ more than needed.
- **Minimum tree cost.** The minimum Steiner tree problem is NP-hard (Karp, 1972) and hard to approximate within some constant factor. The minimum spanning tree of the metric closure on $\{s\} \cup R$ gives a factor of 2, and better constant factors are known; see the [Steiner tree problem](/steiner-tree-problem/).
- **Shortest-path tree cost.** A shortest-path tree can cost up to about $k = |R|$ times the minimum Steiner tree, as in the example; a minimum Steiner tree can have paths much longer than the distances from $s$.
- **Online joins.** If receivers join one by one and the tree may only grow, the greedy rule is $O(\log k)$-competitive, and every online rule is $\Omega(\log k)$-competitive (Imase and Waxman, 1991).
- **State.** Source trees need state for each (source, group) pair on the tree; shared trees need state per group. This is one reason sparse-mode protocols use shared trees first.

## Reductions

- **Unicast** is multicast with $|R| = 1$, and broadcast is multicast with $R = V$.
- **Minimum-cost multicast tree** is the Steiner tree problem in graphs, so any Steiner algorithm or heuristic gives a multicast tree, and hardness carries over.
- **Shortest-path multicast tree** is a [shortest-path tree](/shortest-path-tree/) from $s$, pruned to the union of the paths to $R$. For a shared tree the root is the RP or core instead of $s$.
- **Throughput.** If a link can carry several packets at once and the goal is the highest rate to all receivers, routing on trees can fall short of the max-flow bound, and [network coding](/network-coding/) reaches it.

## Applications

IP multicast carries IPTV inside provider networks, market data feeds in finance, software distribution and some conference systems. Inside one network, routing protocols use link-local multicast addresses for their own messages (OSPF, for example, sends to 224.0.0.5), and Ethernet bridges flood multicast frames along the tree of the [Spanning Tree Protocol](/spanning-tree-protocol/) unless they snoop on IGMP. Wide-area IP multicast saw little use after the MBone experiment of the 1990s, for reasons of control and billing, so most Internet-scale group delivery today uses overlay multicast, content delivery networks or gossip.

## References
