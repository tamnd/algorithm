---
tag: F5917B
kind: algorithm
slug: echo-algorithm
name: Echo algorithm
aliases:
- Echo
- Chang's echo algorithm
- propagation of information with feedback
- PIF
area: distributed/distributed-graph-algorithms
level: core
summary: Flooding followed by echoes back to the initiator, which learns when the broadcast is complete. Exactly 2m messages, a spanning tree as a side effect, works in any timing model.
solves: [broadcast-problem]
model: asynchronous-model
complexity:
  vars: {n: the number of nodes, m: the number of edges, D: the diameter of the network}
  time: {worst: O(n), synchronous: O(D)}
  messages: {worst: 2m}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
prereqs: [flooding, broadcast-problem, asynchronous-model, distributed-spanning-tree]
see_also: [flooding, convergecast, distributed-spanning-tree, termination-detection, dijkstra-scholten, breadth-first-search-distributed, floodmax, depth-first-search]
sources:
  - paper: doi:10.1109/TSE.1982.235573
    title: Ernest J. H. Chang, Echo algorithms, depth parallel operations on general graphs, IEEE Transactions on Software Engineering SE-8(4), 391-401, 1982
    locator: the echo algorithm, its message count and its use for further graph operations
  - paper: doi:10.1109/TIT.1983.1056620
    title: Adrian Segall, Distributed network protocols, IEEE Transactions on Information Theory 29(1), 23-35, 1983
    locator: the protocol PIF (propagation of information with feedback)
  - book: isbn:9780521794831
    title: Gerard Tel, Introduction to Distributed Algorithms, second edition, Cambridge University Press, 2000
    locator: Chapter 6, Section 6.2 (wave algorithms, the echo algorithm)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 15, Section 15.3 (broadcast with acknowledgements, AsynchBcastAck)
---

The echo algorithm is [flooding](/flooding/) with a return path. The initiator sends a token to all its neighbours; every node takes the sender of its first token as its parent and sends the token to its other neighbours; and a node that has received a token on every incident edge sends a token, the echo, to its parent. When the initiator has received a token on all its edges, every node has the message and the run is over, and the initiator knows it. Exactly one token crosses each edge in each direction, so the run sends exactly $2m$ messages on a graph with $m$ edges, and the parent pointers form a [spanning tree](/distributed-spanning-tree/). Chang (1982) named and analysed it; Segall (1983) calls the same pattern PIF, propagation of information with feedback.

## In plain words

A manager sends a question to all the team leads. Each person who gets the question for the first time passes it on to all their contacts, except the person who asked them, and remembers that person as their boss.

A person who gets the question again from somebody else does not pass it on. They just count it as an answer.

When a person has heard back on every contact, all the people they told have finished, so they report to their boss. When the manager has heard back from every contact, the whole company has the question and nobody is still working on it. Each contact pair talks exactly twice, once in each direction.

## The problem

**Network.** A connected undirected graph $G = (V, E)$ with $n$ nodes, $m$ edges, diameter $D$ and maximum degree $\Delta$. Channels are reliable and need not be FIFO. There are no failures.

**Knowledge.** A node knows its ports and its degree. It needs no identifier and no value of $n$, $m$ or $D$, so the algorithm runs in the [port numbering](/port-numbering/) model and on anonymous networks. One node, the initiator $s$, starts the run.

**Timing.** The algorithm is correct in the [asynchronous model](/asynchronous-model/) with any finite delays. Time bounds use delays of at most one unit. In the [synchronous model](/synchronous-model/) it runs in lock-step rounds.

**Goal.** Broadcast a message from $s$ to all nodes (the [broadcast problem](/broadcast-problem/)) so that $s$ learns when every node has it and no message of the run is still in transit. In the terms of Tel (2000), this is a *wave* with a single decision at the initiator.

## The algorithm

```pseudo id=main
ECHO(v)                                    ▷ the code of node v; s is the initiator
L1  on start, at v = s only:
L2      reached ← true, rec ← 0
L3      send TOKEN to every neighbour
L4  on receipt of TOKEN from neighbour u:
L5      rec ← rec + 1
L6      if not reached then
L7          reached ← true, parent ← u
L8          send TOKEN to every neighbour except u
L9      if rec = deg(v) then
L10         if v = s then decide          ▷ every node has the message
L11         else send TOKEN to parent      ▷ the echo
```

Every token counts at line L5, whether it is a first copy, a crossing copy or an echo. The first token makes the node a member of the tree (line L7) and starts its part of the flood (line L8). The last token, number $\deg(v)$, means that all neighbours other than the parent have sent their token to $v$, and those that are children of $v$ sent it as an echo, after their whole subtree finished. So the echo of line L11 carries the meaning "my subtree is done". A node with degree 1 other than $s$ runs lines L7, L8 (with no message) and L11 on the same receipt.

## Example

Take the graph with $n = 6$ nodes and $m = 7$ edges $\{0,1\}, \{0,2\}, \{1,2\}, \{1,3\}, \{2,4\}, \{3,4\}, \{4,5\}$, initiator $s = 0$, in the synchronous model. Tokens received in the same round are handled in port order.

| round | tokens sent | effect |
|---|---|---|
| 1 | $0 \to 1$, $0 \to 2$ | 1 and 2 reached, parent 0 |
| 2 | $1 \to 2$, $1 \to 3$, $2 \to 1$, $2 \to 4$ | 3 reached (parent 1), 4 reached (parent 2); 1 and 2 count a crossing token |
| 3 | $3 \to 4$, $4 \to 3$, $4 \to 5$ | 3 completes ($2$ of $2$); 5 reached and completes ($1$ of $1$) |
| 4 | $3 \to 1$, $5 \to 4$ (echoes) | 1 completes ($3$ of $3$); 4 completes ($3$ of $3$) |
| 5 | $1 \to 0$, $4 \to 2$ (echoes) | 2 completes ($3$ of $3$) |
| 6 | $2 \to 0$ (echo) | 0 completes ($2$ of $2$) and decides |

The count is $2 + 4 + 3 + 2 + 2 + 1 = 14 = 2m$. The tree is $\{1,0\}, \{2,0\}, \{3,1\}, \{4,2\}, \{5,4\}$, a breadth-first tree. The eccentricity of 0 is $e = 3$, and the decision comes in round $6 = 2e$: three rounds out to node 5, three rounds of echoes back.

## Correctness

The first part of the run is flooding, so every node is reached and the parent pointers form a spanning tree. Each node sends exactly one token on each incident edge: at line L3 or L8 on the non-parent edges, and at line L11 on the parent edge. So each node receives exactly $\deg(v)$ tokens and completes, by induction from the leaves of the tree up. When $s$ decides, every child of $s$ has completed, so by induction down the tree every node has completed and has received all $\deg(v)$ of its tokens. That accounts for all $2m$ tokens, so none is in transit and no node will send again. The [full proof](proofs/correctness/) gives every step, with the round and time bounds.

## Complexity

**Messages.** Exactly $2m$ under every schedule: $n - 1$ more than flooding, one echo per tree edge. Each message is a token of $O(1)$ size plus the broadcast message.

**Rounds (synchronous).** With $e$ the eccentricity of $s$ ($e \le D$), the initiator decides in round $r$ with $2e \le r \le 2e + 1$. The bound $2e$ is reached on a path started at an end. The extra round appears when the last layer has edges inside it, whose crossing tokens arrive one round late. This is $O(D)$, and at least $2e$ rounds are needed by any algorithm in which $s$ learns that a node at distance $e$ has the message.

**Time (asynchronous).** With delays of at most 1, $s$ decides by time $e + 1 + h$, where $h$ is the height of the tree. The tree need not be a breadth-first tree: on the complete graph ($D = 1$), if the copies from $s$ are slow except one, the first tokens can run along a path of length $n - 1$, and then the echoes come back along the same path, one unit per hop. So the time is $O(n)$ and can be $\Theta(n)$ when $D = 1$. Use [a distributed BFS](/breadth-first-search-distributed/) first if the time must be $O(D)$ in the asynchronous model.

**Space.** A node keeps a flag, a parent port and a counter of $O(\log \Delta)$ size.

## Properties

- **Deterministic and schedule independent.** The message count, the fact of termination and the safety of the decision do not depend on delays.
- **Termination detection built in.** The initiator learns that the wave is complete, which [flooding](/flooding/) cannot do.
- **Builds a spanning tree.** In the synchronous model the tree is a breadth-first tree; in the asynchronous model it is any spanning tree that the schedule produces.
- **Anonymous.** No identifiers are used, only ports.
- **Single initiator.** With several initiators the waves mix; see the variants.

## Variants and improvements

- **Aggregation on the way back.** An echo can carry a value computed from the subtree, such as a sum, a count or a maximum. Then the initiator gets the aggregate over all nodes at the cost of the same $2m$ messages. This is a [convergecast](/convergecast/) on the tree that the flood builds.
- **Broadcast and echo on a known tree.** If a [spanning tree](/distributed-spanning-tree/) is known, sending only on tree edges costs $2(n - 1)$ messages, and the depth of the tree in rounds each way.
- **Several initiators.** Each wave carries the identifier of its initiator, and a node joins the wave with the largest identifier and drops the others. Only that wave completes, so its initiator becomes the leader. This is echo with extinction, a [leader election](/floodmax/) method for general graphs with $O(nm)$ messages in the worst case (Tel 2000, Chapter 7).
- **Depth-first token.** A single token that walks the graph in [depth-first](/depth-first-search/) order also visits every node and returns to the initiator, with $2m$ messages but $\Theta(m)$ time, since only one message moves at a time.
- **Termination of a diffusing computation.** The [Dijkstra-Scholten algorithm](/dijkstra-scholten/) generalises the echo: the basic computation may send any number of messages, and a node signals its parent when its deficit falls to zero.

## When to use it

Use the echo algorithm when one node must broadcast to all and learn that every node has the message, or must collect a value from every node, and no structure is known. It costs twice the messages of a broadcast on a tree but needs no tree in advance; it leaves one behind. In the synchronous model its round count is within a factor of about 2 of flooding. In an asynchronous network where time matters, its time depends on the height of the tree it builds, which the schedule can make about $n$.

## Pitfalls

- **Echo on first receipt.** A node must not send the echo when it is first reached. It sends the echo only when $\mathit{rec} = \deg(v)$; otherwise the initiator may decide before distant nodes are reached.
- **Not counting the crossing tokens.** A token from a non-parent neighbour that is not a first copy still counts at line L5. If it is discarded without counting, the node never completes.
- **Counting only the children.** A node does not know which neighbours are its children; it counts all its edges. That is why each edge must carry a token in each direction.
- **Expecting a BFS tree in an asynchronous network.** The parent is the first sender, as in flooding.
- **Several initiators without extinction.** Two waves without identifiers mix their counters and can make a node complete too early.

## Implementations

## History

Chang (1982) introduced the echo algorithm under that name and showed how a flood with echoes supports further operations on general graphs, such as the computation of graph properties in one wave. Segall (1983) treated the same scheme as PIF, propagation of information with feedback, together with its use for repeated broadcasts in changing networks. Dijkstra and Scholten (1980) had earlier given the more general detection of termination of diffusing computations, of which the echo is the special case with one message per edge in each direction. Tel (2000) places the echo algorithm among the wave algorithms, and Lynch (1996) presents it as broadcast with acknowledgements.

## References
