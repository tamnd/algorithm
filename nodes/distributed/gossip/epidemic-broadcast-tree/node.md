---
tag: HVTE8H
kind: algorithm
slug: epidemic-broadcast-tree
name: Epidemic broadcast trees
aliases:
- Plumtree
- push-lazy-push multicast tree
area: distributed/gossip
level: advanced
summary: Gossip broadcast that sends the payload only on the links of a tree, built by pruning the links that carry duplicates, and sends message ids on the other links so that the tree can heal.
model: asynchronous-model
complexity:
  vars: {n: the number of nodes, m: the number of overlay links, D: the overlay diameter, Δ: the maximum degree, B: the messages kept for repair}
  messages: {payloads: Θ(n), total: Θ(m)}
  time: {rounds: O(D)}
  space: {extra: O(Δ + B)}
properties: {deterministic: true, recursive: false}
history:
  year: 2007
  people: [João Leitão, José Pereira, Luís Rodrigues]
  note: Leitão, Pereira and Rodrigues combined eager push on a tree with lazy push on the other links of a HyParView overlay, and named the protocol Plumtree, for push-lazy-push multicast tree.
prereqs: [flooding, push-gossip, broadcast-problem, spanning-tree]
see_also: [hyparview, peer-sampling-service, bimodal-multicast, probabilistic-broadcast, gossip-fanout, lpbcast, multicast-routing, shortest-path-tree]
sources:
  - paper: doi:10.1109/SRDS.2007.27
    title: João Leitão, José Pereira and Luís Rodrigues, Epidemic broadcast trees, Proceedings of the 26th IEEE International Symposium on Reliable Distributed Systems (SRDS), 301-310, 2007
    locator: Section 2 (the RMR and LDH metrics), Section 3 (Algorithms 1 to 4, tree construction, repair, membership changes, shared trees, the optimization), Section 4 (evaluation on 10 000 nodes, Table 1)
  - paper: doi:10.1109/DSN.2007.56
    title: João Leitão, José Pereira and Luís Rodrigues, HyParView, a membership protocol for reliable gossip-based broadcast, Proceedings of the 37th IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 419-429, 2007
    locator: the overlay with small symmetric active views that Plumtree uses
---

An epidemic broadcast tree, or Plumtree, is a broadcast protocol of Leitão, Pereira and Rodrigues (2007) that runs on a gossip overlay. Each node sends the full message (eager push) only on the links of a spanning tree, and sends only the message id (lazy push) on all other links. The tree is not computed in advance: the first broadcast floods all links, and every link that delivers a duplicate is moved from eager to lazy. When a tree link fails, a node that hears the id but not the message asks for it with a GRAFT, and that link joins the tree.

## In plain words

A group of friends passes news along a fixed set of friendships. The first time, everybody tells every friend. If somebody hears the news a second time from a friend, they agree with that friend to send only short notes from now on: "I have news number 7".

After the first news, each person gets the full news from exactly one friend, so the full news crosses each person only once. The short notes still travel on all the other friendships.

If a friend in the chain drops out, the full news stops on that branch. A person who gets the note "I have news number 7" but not the news waits a little, then asks the friend who sent the note to send the news. From then on that friendship carries the full news, and the chain is mended.

## The problem

The task is the [broadcast problem](/broadcast-problem/): a node broadcasts a message, and every correct node must deliver it once, with few payload messages and few hops. The nodes form an overlay graph with $n$ nodes and $m$ links, kept by a [peer sampling service](/peer-sampling-service/); the paper uses [HyParView](/hyparview/), whose links are symmetric and stable, and runs Plumtree over TCP connections. [Flooding](/flooding/) on the overlay is reliable but sends a payload on every link in both directions, about $2m$ payloads; a fixed tree sends $n - 1$ payloads but breaks when one link fails. Plumtree aims at $n - 1$ payloads when nothing fails and the reliability of flooding when links fail. The model is the [asynchronous model](/asynchronous-model/) with reliable links; the membership layer reports each failed neighbor with a NeighborDown event. The examples use the lock-step simulator, where every message takes one step.

The paper measures the **relative message redundancy**, $\mathrm{RMR} = \frac{P}{r - 1} - 1$, where $P$ is the number of payload messages and $r$ the number of nodes that receive the message, and the **last delivery hop** (LDH), the largest hop count at which a node first delivers the message. RMR is $0$ when every node receives exactly one payload. Control messages (IHAVE, PRUNE, GRAFT) do not count in RMR.

| Symbol | Meaning |
|---|---|
| $n$ | the number of nodes |
| $m$ | the number of overlay links (in this page $m$ is not a message count) |
| $D$ | the diameter of the overlay |
| $\Delta$ | the largest number of neighbors of a node |
| $f$ | the number of nodes that crash (Section 3 of the paper uses $f$ for the gossip fanout instead) |
| $B$ | the number of messages a node keeps to answer GRAFT |
| $\text{timeout}_1, \text{timeout}_2$ | the wait after the first IHAVE, and the wait after a GRAFT |

## The algorithm

```pseudo id=main
PLUMTREE at node p: eager ← all overlay neighbors, lazy ← ∅
ON BROADCAST(m)
L1  deliver m; send GOSSIP(m, hop 1) to every eager peer and IHAVE(m, hop 1) to every lazy peer
ON GOSSIP(m, h) from s
L2  if m is new: deliver m, stop its timer, send GOSSIP(m, h+1) to eager and IHAVE(m, h+1) to lazy peers other than s; move s to eager
L3  else: move s to lazy and send PRUNE to s
ON PRUNE from s
L4  move s to lazy
ON IHAVE(m, h) from s
L5  if m is not delivered: record (m, s, h) as missing; if m has no timer, start one for timeout1
ON TIMER for m
L6  start a timer for timeout2; take the first missing record (m, s, h); move s to eager; send GRAFT(m, h) to s
ON GRAFT(m, h) from s
L7  move s to eager; if p has m then send GOSSIP(m) to s
ON NEIGHBORDOWN(s)
L8  remove s from eager and lazy, and remove the missing records that came from s
```

**Tree construction (lines L2 to L4).** At the start every link is eager, so the first broadcast is a flood. A node keeps the link on which its first copy came (line L2). A second copy makes the receiver move the sender to lazy and send PRUNE (line L3), and the PRUNE makes the sender do the same (line L4). When the first broadcast ends, each node is eager only with the node that gave it its first copy and with the nodes it gave their first copy, so the eager links form a spanning tree.

**Tree repair (lines L5 to L7).** On the lazy links the node sends IHAVE with the message id. A node that gets IHAVE for a message it has not delivered starts a timer. If the payload has not come when the timer fires, the node sends GRAFT to the first node that announced the message, which moves that link to eager at both ends and makes the announcer send the payload. A second, shorter timer makes the node try the next announcer if this one does not answer. If repairs make a cycle of eager links, the duplicates that it carries prune it again.

**Membership changes (line L8).** A failed neighbor is removed from both sets, and its announcements are forgotten. In the paper, a new neighbor (NeighborUp) is added to the eager set; the simulator has a fixed overlay and does not use NeighborUp.

In the paper, IHAVE messages may wait in a queue and go out together, as long as each one is sent at some time; the simulator sends each IHAVE at once, as the paper's evaluation does.

## Example

**A triangle.** Take the nodes 0, 1 and 2, all linked, with $\text{timeout}_1 = 3$, and let node 0 broadcast three messages.

| Broadcast | What happens | Payloads | Control |
|---|---|---|---|
| 1 | 0 sends GOSSIP to 1 and 2. Both deliver it at hop 1 and forward it to each other. Both copies are duplicates, so 1 and 2 move each other to lazy and send PRUNE. | 4 | 2 PRUNE |
| 2 | 0 sends GOSSIP to 1 and 2; 1 and 2 send IHAVE to each other, which arrives after the payload and is ignored. | 2 | 2 IHAVE |
| 3, after link 0-2 fails | 0 sends GOSSIP to 1 only. Node 1 sends IHAVE to 2. Node 2 starts a timer, and after 3 steps it sends GRAFT to 1. Node 1 sends the payload, and 2 delivers it at hop 2. The tree is now 0-1-2. | 2 | 1 IHAVE, 1 GRAFT |

The first broadcast has $\mathrm{RMR} = 4/2 - 1 = 1$; the second has $\mathrm{RMR} = 0$.

**A random overlay.** The overlay is the union of 3 random Hamiltonian cycles on $n = 200$ nodes (seed 1): $m = 595$ links, and every node has 5 or 6 neighbors. Node 0 broadcasts.

| Broadcast | GOSSIP | IHAVE | PRUNE | GRAFT | RMR | LDH |
|---|---|---|---|---|---|---|
| 1, the flood | 991 | 0 | 792 | 0 | 3.98 | 5 |
| 2 | 199 | 792 | 0 | 0 | 0 | 5 |
| 3, after 30 tree links fail | 323 | 700 | 124 | 92 | 0.62 | 6 |
| 4 | 199 | 732 | 0 | 0 | 0 | 6 |

All 200 nodes deliver every message. The numbers of the first broadcast follow from the proof file: $2m - (n - 1) = 1190 - 199 = 991$ payloads, and two PRUNE messages for each of the $m - (n - 1) = 396$ links outside the tree. In broadcast 2, each of those 396 links carries one IHAVE in each direction. After the failures, 92 GRAFT messages rebuild a tree, and broadcast 4 is again at RMR 0, with $565 - 199 = 366$ lazy links and 732 IHAVE messages. With seed 5 ($m = 590$), the repair takes 163 GRAFT messages, RMR is 1.34 and LDH grows from 5 to 7.

**One tree for several senders.** After a first broadcast from a random node, 7 more broadcasts come from random nodes on the same tree (seed 1). All 200 nodes deliver every message.

| $\text{timeout}_1$ | GRAFT per broadcast | RMR | LDH |
|---|---|---|---|
| 1 | 59 to 121 | 0.59 to 1.22 | 8 to 9 |
| 3 | 10 to 34 | 0.10 to 0.34 | 8 to 11 |
| 12 | 0 | 0 | 6 to 10 |

The tree is a shortest path tree for the first sender (LDH 5), so the payload from another sender takes a longer path. If $\text{timeout}_1$ is short, an IHAVE on a short lazy path makes a node graft before the payload arrives on the tree, which costs extra payloads. With $\text{timeout}_1 = 12$, which is at least twice the depth 5 of the tree, no GRAFT happens, as the proof file shows. The price is a larger LDH.

**The paper's numbers.** On 10 000 nodes with HyParView active views of size 5 and fanout 4, the eager gossip baseline had RMR 3 and Plumtree had RMR 0 for most messages (Figure 2a). In the 100th cycle, eager gossip received 39 984 payloads, and Plumtree 9 999 payloads and about 29 990 control messages (Table 1), so the total count was about the same but almost all of it was small control messages.

## Correctness

The proofs are in the proof file.

- **The first broadcast builds a tree.** On a connected overlay without failures, with all links eager at the start, the first broadcast ends with eager links at both ends exactly on a spanning tree, and lazy links at both ends on all other links. It uses $2m - (n - 1)$ payloads, $2(m - n + 1)$ PRUNE messages and no IHAVE. With equal link delays, the tree is a [shortest path tree](/shortest-path-tree/) from the sender, so LDH is the eccentricity of the sender. (Proved.)
- **Later broadcasts use only the tree.** If the eager links form such a tree, a broadcast with no GRAFT sends exactly $n - 1$ payloads (RMR 0), and the tree does not change. For the sender that built the tree no GRAFT happens; for any sender none happens if $\text{timeout}_1$ is at least twice the depth of the tree (in lock-step). (Proved.)
- **Delivery.** If links are reliable and the overlay of live links is connected, every node delivers every broadcast once, and the number of messages is finite. (Proved.) The lazy links make this hold whatever the eager sets are.
- **Not proved here.** That the eager links form a tree again after a repair is checked by the tests in many runs, and the paper argues that duplicates prune the cycles, but this page does not prove it. The behavior under message loss or under failures during a broadcast is only measured.

## Complexity

- **Messages.** A broadcast on the tree sends $n - 1$ payloads and $2(m - n + 1)$ IHAVE messages, so $\Theta(m)$ messages and $\Theta(n)$ payloads. The first broadcast sends $2m - (n - 1)$ payloads and $2(m - n + 1)$ PRUNE messages. The IHAVE messages of many broadcasts can share one packet.
- **Time.** For the sender that built the tree, LDH is its eccentricity, at most $D$. For another sender with no GRAFT, the payload goes along the tree, so LDH is at most $2D$. A repair adds about $\text{timeout}_1$ plus a round trip for each GRAFT on the path.
- **Space.** A node keeps its eager and lazy sets, $O(\Delta)$, the missing records, and the messages it may need to send on a GRAFT, $B$ of them.

## Properties

- No random choices: the overlay and the message delays decide the tree. The simulator shuffles the messages that arrive in the same step, with a seeded generator.
- Reliability does not depend on the tree: if a node has delivered a message, each of its live neighbors gets the payload or the id, as in flooding.
- One tree is shared by all senders, and it is a shortest path tree only for the first sender.
- The total message count is about that of flooding, but most messages are ids, not payloads.

## Variants and improvements

- **One tree per sender.** For the best latency, a node can run one Plumtree instance per sender, at the cost of state for each tree (Section 3.7 of the paper).
- **The optimization (Algorithm 4).** When a node receives the payload at hop $h$ but had an IHAVE for it at hop $r$ with $h - r$ at least a threshold, it sends GRAFT to the announcer and PRUNE to the eager sender, which swaps a slow tree link for a faster one. The paper used a threshold of 3 for a single sender and 7 for several senders, close to the overlay diameter of 8 to 9; with several senders this added about 22.5% control messages. The simulator does not implement it.
- **IHAVE scheduling.** The ids can be delayed and sent in batches, which saves packets but slows the repair.
- **Pure lazy push.** Sending only ids on every link and pulling the payload has a low payload cost but adds a round trip to every hop; Plumtree pays the round trip only on repair.

## When to use it

Use it to broadcast a stream of messages, many from the same sender or a few senders, on a stable overlay such as [HyParView](/hyparview/), when payloads are large compared with ids. It is a poor fit when the overlay changes all the time, because each change moves links and costs grafts, or when every message comes from a different sender and latency matters, unless the optimization or one tree per sender is used. For one-shot dissemination with no state, plain [push gossip](/push-gossip/) or [probabilistic broadcast](/probabilistic-broadcast/) is simpler.

## Pitfalls

- **A timeout that is too short.** With several senders, the tree path can be much longer than the overlay distance, and a short $\text{timeout}_1$ makes nodes graft and receive duplicates (see the Example).
- **A timeout that is too long.** Repair after a failure waits $\text{timeout}_1$ at every level of the broken subtree, which delays delivery.
- **Not keeping the payload.** A node must keep each message long enough to answer GRAFT; otherwise a repair can fail.
- **An overlay that is not symmetric.** The tree links are eager at both ends only if the overlay links are symmetric; with one-way views the tree is harder to share between senders, as the paper notes.
- **Partitions.** If the live overlay is disconnected, no lazy link crosses the cut, and the nodes on the far side miss the message until the peer sampling service heals the overlay.

## Implementations

The Python code is a seeded lock-step simulator. Each node keeps its eager and lazy sets, its delivered message ids with the hop count, its missing records and its timers. The message types are GOSSIP, IHAVE, PRUNE and GRAFT, and each message takes one step. `Network.broadcast` runs one broadcast until no message and no timer is left, and returns the message counts, the number of nodes that delivered and the LDH. `fail_link` drops a link and calls NeighborDown at both ends. `random_overlay` builds the union of random Hamiltonian cycles, and `tree_edges` returns the links that are eager at both ends.

## History

Bimodal multicast (Birman et al. 1999) had already combined a multicast with gossip repair, but it needed IP multicast and two protocols. Leitão, Pereira and Rodrigues presented Plumtree at SRDS 2007, together with the HyParView overlay at DSN 2007. Their technical report DI-FCUL TR-07-14 was updated in October 2019 to fix a minor bug in Algorithm 1; the section numbers on this page follow that report.

## References
