---
tag: PQWDHA
kind: algorithm
slug: dijkstra-scholten
name: Dijkstra-Scholten algorithm
aliases:
- Dijkstra-Scholten termination detection
- diffusing computation algorithm
- deficit counting
area: distributed/distributed-graph-algorithms
level: advanced
summary: Detects the end of a diffusing computation. Engaged nodes form a tree, each basic message is answered by exactly one signal, and the root announces when it is passive with zero deficit.
solves: [termination-detection]
model: asynchronous-model
complexity:
  vars: {n: the number of nodes, B: the number of basic messages, h: the height of the engagement tree at termination}
  time: {worst: O(h)}
  messages: {worst: B}
  space: {extra: O(log B)}
properties: {deterministic: true, recursive: false}
prereqs: [termination-detection, asynchronous-model, distributed-spanning-tree, echo-algorithm]
see_also: [termination-detection, echo-algorithm, convergecast, global-snapshot, chandy-lamport-snapshot, consistent-cut, distributed-predicate-detection, flooding]
sources:
  - paper: doi:10.1016/0020-0190(80)90021-6
    title: Edsger W. Dijkstra and Carel S. Scholten, Termination detection for diffusing computations, Information Processing Letters 11(1), 1-4, 1980
    locator: the deficit counters, the engagement tree and the signals, with the invariants for safety and liveness
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 19, Section 19.1 (termination detection for diffusing algorithms, the DijkstraScholten algorithm)
  - book: isbn:9780521794831
    title: Gerard Tel, Introduction to Distributed Algorithms, second edition, Cambridge University Press, 2000
    locator: Chapter 8 (termination detection, the Dijkstra-Scholten algorithm and its extension by Shavit and Francez)
  - paper: doi:10.1007/BF01843569
    title: K. Mani Chandy and Jayadev Misra, How processes learn, Distributed Computing 1(1), 40-52, 1986
    locator: the lower bound that termination detection needs, in the worst case, as many control messages as basic messages
---

The Dijkstra-Scholten algorithm detects when a *diffusing computation* has ended: a computation started by one node, the root, in which other nodes become active only when a message of the computation reaches them. Every node counts its *deficit*, the number of messages it has sent that are not yet answered. A node joins a tree, the *engagement tree*, when the first message reaches it, with the sender as its parent; every later message it receives is answered at once by a *signal*, and the message that engaged it is answered only when the node leaves the tree, which it does when it is passive and its deficit is zero. When the root is passive with deficit zero, the computation has terminated, and the root announces it. The overhead is exactly one signal per message of the computation, which matches the lower bound for the problem. The general problem, its other methods and its lower bounds are on the page on [termination detection](/termination-detection/).

## In plain words

A manager hands out tasks. Each worker who gets a first task from someone notes that person as their boss. A worker can hand out tasks to others too.

Every task that is handed out must be answered with "done" exactly once. If a worker already has a boss, they answer "done" for a new task at once and just do the work. The task that made them join is answered last.

A worker counts the tasks they have handed out and not yet seen answered. When the worker is idle and that count is zero, they send "done" to their boss and leave.

When the manager is idle and has all answers back, all work is over.

## The problem

**Network.** An asynchronous network: a connected graph of $n$ nodes, reliable channels that need not be FIFO, arbitrary finite delays, and no failures. Nodes have identifiers or at least ports; the algorithm uses only "reply to the sender" and "send to my parent", so ports are enough.

**Basic computation.** Each node is *active* or *passive*. Only an active node sends basic messages; an active node can become passive at any time; a passive node becomes active only when a basic message arrives. At the start, the root $r$ is active and all other nodes are passive. This is a *diffusing computation*.

**Goal.** The root must announce termination (safety) only when every node is passive and no basic message is in transit, and (liveness) it must announce after the computation has terminated. The extra messages are *control* messages; their number and the delay of the announcement are the costs. The detection must not delay or change the basic computation.

## The algorithm

```pseudo id=main
DIJKSTRA-SCHOLTEN(v)                       ▷ runs beside the basic computation; r is the root
L1  initially: deficit ← 0; at r: engaged ← true, active ← true, parent ← r; elsewhere: engaged ← false
L2  when v sends a basic message: deficit ← deficit + 1
L3  on receipt of a basic message from u:
L4      active ← true
L5      if not engaged then engaged ← true, parent ← u        ▷ the signal for this message waits
L6      else send SIGNAL to u                                  ▷ answered at once
L7  on receipt of SIGNAL: deficit ← deficit − 1; TRY-LEAVE
L8  when v becomes passive: TRY-LEAVE
L9  TRY-LEAVE: if engaged and not active and deficit = 0 then
L10     if v = r then announce termination
L11     else send SIGNAL to parent; engaged ← false
```

The deficit of a node counts three kinds of open messages: messages still in transit, messages answered by a signal still on its way back, and the engaging messages of its current children. A node can be engaged several times in one run: after it leaves, a new basic message engages it again, possibly with a different parent.

## Example

Three nodes: the root 0 and nodes 1 and 2.

| step | event | deficits $(\delta_0, \delta_1, \delta_2)$ | engaged (parent) |
|---|---|---|---|
| 1 | 0 sends a basic message to 1 (line L2) | $(1, 0, 0)$ | 0 |
| 2 | it arrives; 1 is engaged with parent 0 (line L5) | $(1, 0, 0)$ | 0, 1 (0) |
| 3 | 0 becomes passive; TRY-LEAVE fails since $\delta_0 = 1$ | $(1, 0, 0)$ | 0, 1 (0) |
| 4 | 1 sends to 2 and to 0 | $(1, 2, 0)$ | 0, 1 (0) |
| 5 | 2 is engaged with parent 1; 0 is active again, engaged already, signals 1 at once (line L6) | $(1, 2, 0)$ | 0, 1 (0), 2 (1) |
| 6 | the signal reaches 1 (line L7) | $(1, 1, 0)$ | same |
| 7 | 0 and 1 become passive; both still have deficit 1 | $(1, 1, 0)$ | same |
| 8 | 2 becomes passive with $\delta_2 = 0$: it signals 1 and leaves | $(1, 1, 0)$ | 0, 1 (0) |
| 9 | the signal reaches 1: $\delta_1 = 0$, 1 is passive, so it signals 0 and leaves | $(1, 0, 0)$ | 0 |
| 10 | the signal reaches 0: $\delta_0 = 0$ and 0 is passive, so 0 announces | $(0, 0, 0)$ | 0 |

There were 3 basic messages and 3 signals. After step 7 nodes 0 and 1 are passive, but node 2 is still active, so the computation has not ended, and no node can leave yet. The computation ends at step 8, when 2 becomes passive, and the announcement follows two signal delays later. The test file replays this run event by event.

## Correctness

The proof rests on three invariants: the deficit of $v$ equals the number of its open messages, each of which is in transit, answered by a signal in transit, or the engaging message of a child; a node that is active or has a positive deficit is engaged; and the engaged nodes form a tree rooted at $r$, which loses only leaves. When the root announces, it is passive with deficit zero, so it has no child, so it is the only engaged node; every other node is therefore passive with deficit zero, so no basic message is in transit. Conversely, once the computation has terminated, only signals move, and the tree shrinks leaf by leaf until the root's deficit is zero. Every basic message is answered by exactly one signal, at line L6 or line L11. The [full proof](proofs/correctness/) gives all steps.

## Complexity

**Messages.** Exactly $B$ signals for $B$ basic messages, in every execution. Chandy and Misra (1986) prove that, in the worst case, every termination detection algorithm needs as many control messages as the computation has basic messages, so Dijkstra-Scholten is optimal in the worst case. It is not optimal for every execution: a computation with many messages and a short life pays for every message.

**Detection delay.** With delays of at most one unit, let the computation terminate at time $t_0$ with an engagement tree of height $h$. All signals in transit at $t_0$ arrive by $t_0 + 1$, so every leaf has left by then; by induction a node of height $k$ in the tree leaves by $t_0 + 1 + k$, and the root announces by $t_0 + 1 + h$. The tree can be a path, so $h \le n - 1$ and the delay is $O(n)$.

**Space.** A deficit counter of $O(\log B)$ bits, a parent pointer and two flags. The root needs nothing more.

## Properties

- **Exact overhead.** One signal per basic message; no other control messages, no waves, no snapshots.
- **No global knowledge.** Nodes need not know $n$, the graph or identifiers; they answer the sender and their parent.
- **Works without FIFO channels.** The argument never uses the order of messages on a channel.
- **Detects a stable property.** Termination of a diffusing computation, once true, stays true; the algorithm does not detect properties that can become false again.
- **One initiator only.** The engagement tree needs one root. Computations started by several nodes need an extension.
- **No fault tolerance.** A lost signal or a crashed node blocks the announcement for ever.

## Variants and improvements

- **Several initiators.** Shavit and Francez (1986) keep a forest, one tree per initiator, and detect that the forest is empty with a separate wave, such as the [echo algorithm](/echo-algorithm/). Tel (2000, Chapter 8) presents it.
- **Weight throwing.** Instead of answering each message, a node sends weight back to the root only when it becomes passive, and the root announces when it has all the weight (Mattern 1989, Huang 1989). This can save signals when nodes send many messages per activation; see [termination detection](/termination-detection/).
- **Echo as a special case.** If the basic computation is [flooding](/flooding/) and every node sends one batch on its first message, Dijkstra-Scholten becomes the echo algorithm: each message is signalled at once except the engaging one, whose signal is the echo.
- **Snapshots instead of trees.** A [global snapshot](/global-snapshot/), for example by the [Chandy-Lamport algorithm](/chandy-lamport-snapshot/), records a [consistent cut](/consistent-cut/) on which termination can be tested; this works for any computation, not only diffusing ones, at the cost of repeated snapshots.
- **Garbage collection.** The same scheme of deficits and signals detects when a distributed object has no more references, as in reference listing with acknowledgements.

## When to use it

Use Dijkstra-Scholten when a single node starts a computation, the channels are reliable and the number of basic messages is moderate: it is simple, needs no knowledge of the network, and its overhead is exactly one control message per basic message. Use a wave-based or counter-based method when the computation has several initiators or sends very many messages per unit of work, and a snapshot-based method when termination is one of several stable properties to be detected.

## Pitfalls

- **Signalling the engaging message at once.** If a node answers the message that engaged it immediately, its parent can leave while the node is still active, and the root can announce too early.
- **Leaving while active.** Line L9 needs the node to be passive. A node that leaves when its deficit is zero but it is still active can send a basic message later with no tree above it.
- **Counting received instead of sent messages.** The deficit counts messages the node has sent. A counter of received messages does not tell whether the messages of the node are still in flight.
- **Assuming the tree is fixed.** Nodes leave and join again. The tree at the end is not the tree at the start; any data stored on it must allow this.
- **Using it with several roots.** Two roots that both announce do not know about each other's part of the computation.

## Implementations

## History

Dijkstra and Scholten (1980) introduced diffusing computations and this algorithm, with the deficit counters and the tree of engaged processes, in a four-page note. Francez (1980) and Dijkstra, Feijen and van Gasteren (1983) studied termination detection on other topologies at about the same time. Chandy and Misra (1986) showed, with their theory of knowledge in distributed systems, that the number of control messages in the worst case must equal the number of basic messages, so the algorithm is optimal in that sense. Shavit and Francez (1986) extended it to several initiators. Lynch (1996, Section 19.1) and Tel (2000, Chapter 8) give textbook proofs.

## References
