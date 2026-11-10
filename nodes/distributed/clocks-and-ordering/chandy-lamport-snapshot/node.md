---
tag: 32HBY1
kind: algorithm
slug: chandy-lamport-snapshot
name: Chandy-Lamport snapshot algorithm
aliases:
- Chandy-Lamport algorithm
- marker-based snapshot
area: distributed/clocks-and-ordering
level: core
summary: On FIFO channels, a process records its state and sends a marker on each outgoing channel. A channel's state is what arrives between the receiver's recording and the marker.
solves: [global-snapshot]
model: asynchronous-model
complexity:
  vars: {e: the number of channels, M: the number of messages recorded as channel state}
  time: {worst: O(e + M)}
  space: {extra: O(e + M)}
  messages: {worst: e}
properties: {deterministic: true, recursive: false}
history:
  year: 1985
  people: [K. Mani Chandy, Leslie Lamport]
  note: Chandy and Lamport published the marker algorithm, the reachability theorem and stable property detection in ACM Transactions on Computer Systems in 1985.
prereqs: [global-snapshot, fifo-delivery]
see_also: [global-snapshot, lai-yang-snapshot, consistent-cut, fifo-delivery, termination-detection, deadlock-detection, checkpointing, happened-before]
sources:
  - paper: doi:10.1145/214451.214456
    title: K. Mani Chandy and Leslie Lamport, Distributed snapshots, determining global states of distributed systems, ACM Transactions on Computer Systems 3(1), 1985
    locator: pages 63 to 75; the marker sending and receiving rules, the proof that the recorded state is reachable, and stable property detection (DOI from memory, to be checked)
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 4 (the Chandy-Lamport algorithm and its correctness)
  - book: isbn:9780132143011
    title: George Coulouris, Jean Dollimore, Tim Kindberg and Gordon Blair, Distributed Systems, Concepts and Design, fifth edition, Addison-Wesley, 2012
    locator: Chapter 14, Section 14.5 (global states and the Chandy and Lamport snapshot algorithm)
---

The *Chandy-Lamport snapshot algorithm* records a [global snapshot](/global-snapshot/) of a running system whose channels deliver messages in FIFO order. When a process records its local state, it sends a *marker* on each of its outgoing channels. A process that receives its first marker records its own state at once; the state of a channel is the sequence of messages that arrive on it after the receiver recorded and before the marker on that channel. The recorded state is the global state of a [consistent cut](/consistent-cut/), and it uses exactly one marker per channel.

## In plain words

One process decides to take a snapshot. It writes down its own state and sends a special message, a marker, to each neighbour. The marker means "everything I sent before this was before my snapshot; everything after it is after".

When a process gets its first marker, it writes down its own state and sends markers to all its neighbours too. Then it keeps a list for each incoming channel. Every normal message that arrives on that channel before the marker on it was sent before the sender's snapshot, so it was "on the wire" at the moment of the snapshot; the process adds it to the list. When the marker arrives on a channel, its list is complete. Because the channels keep messages in order, nothing can slip past a marker.

## The problem

**Model.** A strongly connected directed graph of $n$ processes and $e$ channels. Channels are reliable and FIFO (see [FIFO delivery](/fifo-delivery/)) and have unbounded delay, as in the [asynchronous model](/asynchronous-model/). Processes do not fail. Any process may start the snapshot; the version here has one initiator.

**Goal.** Each process $p_i$ records a local state, and for each channel $c$ into $p_i$ it records a channel state, such that together they are the global state of a consistent cut: every message counted as received is counted as sent, and each channel state is exactly the set of messages sent before the sender recorded and received after the receiver recorded. The application must not be stopped.

## The algorithm

```pseudo id=main
RECORD(p)                                       ▷ called once per process
L1  save the local state of p
L2  for each outgoing channel c of p: send MARKER on c, before any later message on c
    for each incoming channel c of p: State(c) ← empty, start recording c

ON-MARKER(p, c)                                 ▷ a marker arrives at p on channel c
L3  if p has not recorded then
L4      RECORD(p)
L5  stop recording c                            ▷ State(c) is now final

ON-MESSAGE(p, c, m)                             ▷ an application message arrives
    deliver m to the application
L6  if p is recording c then append m to State(c)
```

The initiator calls RECORD on its own. When a process records because of a marker on channel $c$, line L5 stops recording $c$ at once, so the state of $c$ is empty: by FIFO order, every message that the sender sent before its marker has already arrived. The snapshot is complete at a process when it has received a marker on every incoming channel. To assemble the snapshot, each process sends its local state and its channel states to a collector, or along a spanning tree.

## Example

Branch $p_0$ holds 100 and branch $p_1$ holds 50. Application messages take 4 time units and markers take 1, on FIFO channels.

| time | event | recorded |
|---|---|---|
| 1 | $p_1$ sends 30 to $p_0$; $p_1$ now holds 20 | |
| 2 | $p_0$ starts: records 100 (L1), sends a marker to $p_1$ (L2), starts recording channel $(1,0)$ | $LS_0 = 100$ |
| 3 | marker reaches $p_1$: $p_1$ records 20 (L4), sends a marker to $p_0$, stops recording $(0,1)$ (L5) | $LS_1 = 20$, $State(0,1) = \langle\rangle$ |
| 5 | the 30 reaches $p_0$, which is recording $(1,0)$ (L6) | $State(1,0) = \langle 30 \rangle$ |
| 5 | the marker of $p_1$ reaches $p_0$ after the 30, by FIFO order; $p_0$ stops recording $(1,0)$ | done |

The snapshot holds $100 + 20 + 30 = 150$, the money in the bank.

**A non-FIFO channel breaks it.** Let both branches hold 100, let markers take 5 and messages take 1, and let the channel allow overtaking. $p_0$ records 100 at time 0 and sends its marker; at time 0.5 it sends 10 to $p_1$. The 10 overtakes the marker and arrives at time 1.5, so $p_1$ holds 110 when the marker comes at time 5, and it records 110. The record holds the receive of the 10 but not its send, so the cut is not consistent, and the total is 210. On a FIFO channel the 10 would arrive after the marker, $p_1$ would record 100, and the total would be 200. The [Lai-Yang algorithm](/lai-yang-snapshot/) handles such channels.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Let $C$ be the cut of the events that each process runs before it records.

- **Termination.** The initiator records and sends markers. Any process that records sends a marker on every outgoing channel, and markers arrive, so by induction along paths every process records. Each channel carries exactly one marker, so each channel recording stops.
- **Consistency.** Suppose $p_j$ receives a message $m$ from $p_i$ before $p_j$ records, but $p_i$ sent $m$ after recording. Then $p_i$ sent its marker on that channel before $m$, so by FIFO order the marker reached $p_j$ before $m$, and $p_j$ recorded before receiving $m$. This contradicts the choice of $m$. So every receive in $C$ has its send in $C$, and $C$ is consistent.
- **Channel states.** The state of the channel from $p_i$ to $p_j$ is what arrives after $p_j$ records and before $p_i$'s marker. By FIFO order these are exactly the messages that $p_i$ sent before its marker, that is before it recorded, and that $p_j$ received after it recorded.
- **Reachability.** By the theorem on the [global snapshot](/global-snapshot/) page, the recorded state is reachable from the state when the algorithm started, and the state when it ends is reachable from it.

In the bank, money is conserved by every event, so it is the same in every reachable state; the recorded state is reachable, so its total equals the true total. The seeded tests check this on 60 random runs with 2 to 5 branches.

## Complexity

Each process sends one marker on each outgoing channel, so the algorithm sends exactly $e$ markers; on a complete graph that is $n(n-1)$. A process does $O(1)$ work per marker and per recorded message, so the total local work is $O(e + M)$, where $M$ is the number of messages recorded as channel state, and the same amount of memory holds the record. The markers spread along shortest paths, so all processes have recorded within $D$ marker delays, for a graph of diameter $D$, and all channel recordings end one more marker delay later.

## Properties

- **Does not stop the application.** Messages are delivered as usual; the algorithm only observes.
- **The record need not have occurred.** The recorded state may never have existed at any real time, but it is reachable.
- **Needs FIFO channels.** The marker separates "before" from "after" only when no message overtakes it.
- **Concurrent initiators are fine.** If several processes start at once, each process still records once, and the proof does not change.
- **No piggybacking.** Application messages carry nothing extra.

## Variants and improvements

- **Non-FIFO channels.** [Lai and Yang](/lai-yang-snapshot/) colour each message instead of sending markers on its channel. Mattern (1993) uses counters to know when all messages of a colour have arrived.
- **Repeated snapshots.** Number the snapshots and put the number in the marker, so that several snapshots can run one after another.
- **Termination of the collection.** A [termination detection](/termination-detection/) algorithm, or a count of the markers expected, tells the collector that the snapshot is complete.
- **Stream processing.** Asynchronous barrier snapshots in Apache Flink send markers, called barriers, through the data flow. Operators align the barriers of their inputs, which avoids recording channel state in acyclic flows.

## When to use it

Use it to take checkpoints of a running system, or to detect stable properties such as termination and deadlock, when the channels are FIFO, as with TCP connections between each pair of processes. When messages can overtake each other, use [Lai-Yang](/lai-yang-snapshot/) or a counter-based method.

## Pitfalls

- **Overtaking.** Any channel that can reorder messages breaks consistency, as in the example. Several TCP connections or a message broker between the same two processes form such a channel.
- **Sending before the marker.** Line L2 must send the markers before any later application message. A process that records and then sends a message before its markers breaks the separation.
- **Missing channels.** A process must record every incoming channel. A channel that it forgets loses the messages in transit, and the total is wrong.
- **Unstable properties.** A snapshot shows a state that may never have occurred, so a property that can become false again, such as "the queue is empty", cannot be decided from one snapshot. Use [predicate detection](/distributed-predicate-detection/).

## Implementations

## History

K. Mani Chandy and Leslie Lamport published the algorithm in 1985 in ACM Transactions on Computer Systems, under the title Distributed snapshots, determining global states of distributed systems. The paper also gave the reachability theorem and used it to detect stable properties. It became the base of a whole family of snapshot and checkpointing algorithms, and of the snapshot mechanisms of modern stream processors.

## References
