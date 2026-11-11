---
tag: 0WMBJP
kind: algorithm
slug: flooding
name: Flooding
aliases:
- flood broadcast
- naive flooding
area: distributed/distributed-graph-algorithms
level: intro
summary: Broadcast in which each node forwards the message once, on first receipt, to all other neighbours. Exactly 2m − n + 1 messages, D rounds, and no node learns that the broadcast is over.
solves: [broadcast-problem]
model: asynchronous-model
complexity:
  vars: {n: the number of nodes, m: the number of edges, D: the diameter of the network}
  time: {worst: O(D)}
  messages: {worst: 2m − n + 1}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
prereqs: [broadcast-problem, synchronous-model, asynchronous-model, message-complexity, round-complexity]
see_also: [echo-algorithm, distributed-spanning-tree, breadth-first-search-distributed, convergecast, floodmax, breadth-first-search, push-gossip, termination-detection]
sources:
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 2, Section 2.3 (flooding and building a spanning tree)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 15, Section 15.3 (AsynchSpanningTree, broadcast and convergecast); Chapter 4, Section 4.2 (SynchBFS)
  - book: isbn:9780898714647
    title: David Peleg, Distributed Computing, A Locality-Sensitive Approach, SIAM, 2000
    locator: Chapter 3 (broadcast and convergecast, the flooding algorithm and its message and time bounds)
  - paper: doi:10.1109/TIT.1983.1056620
    title: Adrian Segall, Distributed network protocols, IEEE Transactions on Information Theory 29(1), 23-35, 1983
    locator: the protocol PI (propagation of information) and its extension PIF (propagation of information with feedback)
---

Flooding is the simplest algorithm for the [broadcast problem](/broadcast-problem/): the source sends its message to all its neighbours, and every other node, the first time it gets the message, sends it on to all its neighbours except the one it got it from. Later copies are discarded. On a connected graph with $n$ nodes and $m$ edges it sends exactly $2m - (n - 1)$ messages under every schedule, it reaches every node within $D$ rounds or time units, where $D$ is the diameter, and the first copies leave behind a [spanning tree](/distributed-spanning-tree/). No node learns when the broadcast is complete; the [echo algorithm](/echo-algorithm/) adds this at the cost of $n - 1$ more messages.

## In plain words

A rumour starts with one person in a crowd. Each person who hears the rumour for the first time tells it to every friend, except the friend who told them. A person who hears the rumour again does nothing.

The rumour spreads one step of friendship at a time, so it reaches everyone after as many steps as the longest chain of friends from the start. Each person speaks only once, so the number of messages is about two per friendship.

Each person remembers who told them first. These "who told me" links form a tree that connects everyone. But no person knows when the last one has heard the rumour.

## The problem

**Network.** A connected undirected graph $G = (V, E)$ with $n = |V|$ nodes, $m = |E|$ edges, diameter $D$ and maximum degree $\Delta$. Each edge is a reliable channel in both directions; channels need not be FIFO. There are no failures.

**Knowledge.** A node knows its own ports, one for each incident edge. It does not need an identifier, the value of $n$ or the graph: flooding runs in the [port numbering](/port-numbering/) model, even in an anonymous network.

**Timing.** Flooding is correct in the [synchronous model](/synchronous-model/) (lock-step rounds) and in the [asynchronous model](/asynchronous-model/) (any finite delays). For time bounds in the asynchronous model, each message delay is at most one time unit and local steps take no time.

**Goal.** One source $s$ holds a message $M$. Every node must receive $M$. This is the [broadcast problem](/broadcast-problem/).

## The algorithm

```pseudo id=main
FLOOD(v)                                   ▷ the code of node v; s is the source
L1  on start, at v = s only:
L2      reached ← true, parent ← v
L3      send M to every neighbour
L4  on receipt of M from neighbour u:
L5      if reached then
L6          discard the copy               ▷ a later copy carries nothing new
L7      else reached ← true, parent ← u
L8          send M to every neighbour except u
```

The source starts the run (lines L1 to L3). Every other node is passive until the first copy of $M$ arrives. Then it records the sender as its parent (line L7) and sends $M$ on all its other edges (line L8). The test of line L5 stops the flood: a node sends at most one batch of messages in the whole run.

In a synchronous round in which a node gets two or more first copies, it takes any one sender as its parent, for example the one on the smallest port, and sends on all other edges, including the edges of the other senders. Those copies cross copies coming the other way and are discarded at line L6.

## Example

Take the graph with $n = 6$ nodes, $m = 7$ edges $\{0,1\}, \{0,2\}, \{1,2\}, \{1,3\}, \{2,4\}, \{3,4\}, \{4,5\}$, source $s = 0$, in the synchronous model.

| round | messages sent | newly reached (parent) | messages discarded |
|---|---|---|---|
| 1 | $0 \to 1$, $0 \to 2$ | 1 (0), 2 (0) | none |
| 2 | $1 \to 2$, $1 \to 3$, $2 \to 1$, $2 \to 4$ | 3 (1), 4 (2) | at 1 and at 2 |
| 3 | $3 \to 4$, $4 \to 3$, $4 \to 5$ | 5 (4) | at 3 and at 4 |

Node 5 has no other neighbour, so it sends nothing, and the run stops after round 3. The count is $2 + 4 + 3 = 9 = 2 \cdot 7 - (6 - 1)$. Each node is reached in the round equal to its distance from 0, and the parent edges $\{1,0\}, \{2,0\}, \{3,1\}, \{4,2\}, \{5,4\}$ form a breadth-first tree. Edges $\{1,2\}$ and $\{3,4\}$ carry one copy in each direction, and both copies are discarded.

In the asynchronous model the count is again 9, but the tree can change. On the triangle $0, 1, 2$ with source 0, if the copy $0 \to 2$ is slow and the copies $0 \to 1$ and $1 \to 2$ are fast, node 2 takes 1 as its parent although it is a neighbour of the source. The tree is still a spanning tree, but it is not a breadth-first tree.

## Correctness

Every node is reached, because on each edge from a reached node to an unreached node a copy of $M$ is sent (the only edge a node skips is the edge to its parent, which is reached). Each node sends one batch: $\deg(s)$ messages at the source and $\deg(v) - 1$ at every other node, so the total is $\sum_v \deg(v) - (n - 1) = 2m - (n - 1)$. The parent of a node was reached strictly earlier, so following parent pointers ends at $s$, and the pointers form a spanning tree. In the synchronous model a node at distance $d$ is reached in round $d$, by induction on $d$. The [full proof](proofs/correctness/) gives all steps.

## Complexity

**Messages.** Exactly $2m - (n - 1)$ under every schedule, in both timing models. This is $\Theta(m)$ for every connected graph, since $m \ge n - 1$. For $n = 1$ it is $0$; on a tree it is $n - 1$, one message on each edge; on the complete graph it is $n(n-1) - (n - 1) = (n-1)^2$.

**Rounds (synchronous).** Node $v$ is reached in round $\mathrm{dist}(s, v)$, so all nodes are reached by round $e = \max_v \mathrm{dist}(s, v)$, the eccentricity of $s$, and $e \le D$. Nodes reached in round $e$ may still send in round $e + 1$, so the last message is sent in round $e$ or $e + 1$.

**Time (asynchronous).** With delays of at most one unit, node $v$ is reached by time $\mathrm{dist}(s, v)$ and the last copy arrives by time $e + 1$. Flooding is as fast as possible: no algorithm can inform a node at distance $d$ before round or time $d$.

**Bits and space.** Each message holds $M$ and nothing else, so the run sends $(2m - n + 1)|M|$ bits. A node stores one bit and one port number.

## Properties

- **Deterministic.**
- **Works in every timing model.** Correctness and the exact count do not depend on the schedule.
- **Needs no identifiers and no knowledge of $n$ or $D$.** Port numbers are enough.
- **Builds a spanning tree as a side effect.** In the synchronous model it is a breadth-first tree; in the asynchronous model it can be any spanning tree that the schedule produces.
- **No termination detection.** A node knows that it has $M$, but no node knows that all nodes have it. A node that has sent its batch does not know whether more copies will arrive.
- **Not fault tolerant.** One crashed node can cut off the part of the graph behind it, unless the graph stays connected without it; then the flood goes around.

## Variants and improvements

- **Send to all neighbours.** If line L8 also sends back to $u$, the count is $\sum_v \deg(v) = 2m$ exactly. This is the form in some textbooks; it wastes $n - 1$ messages.
- **Flooding with an [echo](/echo-algorithm/).** Each node answers every copy, and sends its answer to its parent only when all its other edges have answered. The source learns that the broadcast is over. The count rises to exactly $2m$.
- **Broadcast on a known tree.** If a [spanning tree](/distributed-spanning-tree/) is already known, sending only on tree edges costs $n - 1$ messages and as many rounds as the depth of the tree. This is the reason to build a tree once and use it many times.
- **Repeated broadcasts and sequence numbers.** When many messages are flooded, each carries the source and a sequence number, and a node discards a message whose number it has already seen. This is how link state routing protocols spread their updates.
- **Time to live.** A hop counter in the message limits the flood to a radius; this is how a node collects its neighbourhood of radius $r$ in $r$ rounds in the [LOCAL model](/local-model/).
- **Gossip.** [Push gossip](/push-gossip/) sends to one random neighbour per round instead of to all, and so trades messages for time and a probability of failure.

## When to use it

Use flooding when no structure is known, the network is small or the broadcast is rare, and nobody must learn that it is over. For a one time broadcast it is optimal up to a constant factor in both rounds and messages when nodes know only their own ports, by the lower bounds on the [broadcast problem](/broadcast-problem/). If the source must know when every node has the message, use the [echo algorithm](/echo-algorithm/). If many broadcasts follow, build a [spanning tree](/distributed-spanning-tree/) once and send on its edges only.

## Pitfalls

- **Forwarding every copy.** If line L8 runs on every receipt instead of the first (line L5 left out), a cycle makes the flood run forever. The test of line L5 is what makes the run finite.
- **Expecting a breadth-first tree in an asynchronous network.** The parent set in line L7 is the first sender, not the nearest one. Use a [distributed BFS](/breadth-first-search-distributed/) algorithm when distances matter.
- **Treating silence as the end.** In the asynchronous model a node cannot conclude from a quiet period that the flood is over. Termination must be detected by an echo, by [termination detection](/termination-detection/), or by a known bound $D$ in the synchronous model.
- **Counting $2m$ when only $2m - n + 1$ are sent, or the reverse.** The two counts belong to the two forms of line L8; state which form you analyse.

## Implementations

## History

Flooding is folklore of early packet networks, and no single first source is known for it. Segall (1983) gave a systematic treatment of propagation of information (PI) and of propagation of information with feedback (PIF) in general networks. The textbooks of Lynch (1996, Section 15.3), Peleg (2000, Chapter 3) and Attiya and Welch (2004, Section 2.3) present it as the basic broadcast algorithm, together with the spanning tree it builds.

## References
