---
tag: NG8AFY
kind: model
slug: timely-dataflow
name: Timely dataflow
aliases:
- Naiad timely dataflow
area: databases/stream-and-incremental-processing
level: research
summary: "A dataflow model with logical timestamps on messages and progress tracking, which supports cyclic, incremental and low-latency computation."
prereqs: [happened-before]
see_also: [differential-dataflow, dbsp, dataflow-model, event-time-watermark, stream-punctuation, lamport-clocks, vector-clocks, asynchronous-barrier-snapshotting]
sources:
  - paper: "Derek G. Murray, Frank McSherry, Rebecca Isaacs, Michael Isard, Paul Barham and Martín Abadi, Naiad, a timely dataflow system, Proceedings of ACM SOSP 2013"
    title: "Naiad: a timely dataflow system"
    locator: "the sections on timely dataflow (graph structure, vertex computation, progress tracking with pointstamps, occurrence and precursor counts) and on distributed progress tracking (the page numbers are not checked here)"
  - paper: "Frank McSherry, Derek G. Murray, Rebecca Isaacs and Michael Isard, Differential dataflow, Proceedings of the Conference on Innovative Data Systems Research (CIDR), 2013"
    title: Differential dataflow
    locator: the incremental and iterative computation that timely dataflow was built to run (general locator)
---

Timely dataflow is a model of computation in which a directed graph of stateful vertices exchanges messages that carry logical timestamps, and a progress tracking protocol tells each vertex when no more messages with a given timestamp can reach it. The timestamps hold an input epoch and a counter for each loop, so the graph can have cycles, and one computation can work on many epochs and iterations at once. The general [dataflow model](/dataflow-model/) has no such notion of completeness, and [DBSP](/dbsp/) is synchronous, with one step of every operator per tick, while timely dataflow runs its vertices asynchronously and learns completeness from the protocol. It is the model that [differential dataflow](/differential-dataflow/) runs on.

## The machine

**Timestamps.** A timestamp is $t = (e, \langle c_1, \ldots, c_k \rangle)$: an epoch $e$ from the input, and one loop counter for each loop that contains the current place in the graph, innermost last. Timestamps with the same $k$ are ordered by $t_1 \le t_2$ when $e_1 \le e_2$ and the counters of $t_1$ are at most those of $t_2$ in lexicographic order. This is a partial order: $(0, \langle 3 \rangle)$ and $(1, \langle 0 \rangle)$ are not comparable.

**The graph.** Vertices are connected by directed edges, and the graph may have cycles, but only inside *loop contexts*. Every edge into a loop context passes an *ingress* vertex, which adds a counter $0$. Every edge out of it passes an *egress* vertex, which removes the last counter. Every cycle passes a *feedback* vertex, which adds 1 to the last counter. All other vertices keep the timestamp. So a timestamp grows strictly along every cycle.

**Vertices.** A vertex receives messages in calls of `OnRecv(edge, message, t)` and sends with `SendBy(edge, message, t')`. It can ask with `NotifyAt(t)` to be called with `OnNotify(t)` once it can receive no more messages with times $\le t$. A vertex may send, or ask for notification, only at times $t' \ge t$, where $t$ is the time of the call that it is handling. Inputs are vertices that take records from outside, put them in the current epoch, and then declare the epoch closed.

**Pointstamps and progress.** A *pointstamp* is a pair $(t, l)$ of a timestamp and a location, an edge for an unprocessed message or a vertex for a pending notification. A pointstamp $(t_1, l_1)$ *could result in* $(t_2, l_2)$ if some path from $l_1$ to $l_2$ changes $t_1$ by its ingress, egress and feedback vertices into a timestamp $\le t_2$. For each active pointstamp the system keeps an *occurrence count*, the number of messages or requests at it, and a *precursor count*, the number of active pointstamps that could result in it. The *frontier* is the set of active pointstamps with precursor count 0. A notification for $(t, v)$ is delivered when $(t, v)$ is in the frontier.

**Example.** A graph has the input A, the ingress I, a loop vertex B, the feedback F, the egress E and the output C, with the edges $A \to I \to B$, $B \to F \to B$ and $B \to E \to C$. Three pointstamps are active:

| pointstamp | what it is | could result in |
|---|---|---|
| $p_1 = ((0, \langle 3 \rangle), F \to B)$ | a message of epoch 0 in iteration 3 | $p_3$, through B and E, which removes the counter |
| $p_2 = ((1, \langle 0 \rangle), I \to B)$ | a message of epoch 1 | nothing, since epoch 1 is not $\le$ epoch 0 |
| $p_3 = ((0), C)$ | C waits for the end of epoch 0 | nothing |

The frontier is $\{p_1, p_2\}$, so C must wait. When B handles the message of $p_1$ and sends nothing more for epoch 0, the occurrence count of $p_1$ falls to 0, the precursor count of $p_3$ falls to 0, and the frontier becomes $\{p_2, p_3\}$. C then gets the notification for epoch 0 while epoch 1 is still in the loop.

**Distributed form.** The graph runs on many workers, each with a copy of every vertex for a part of the data, and messages between workers go through exchange edges, as in the [exchange operator](/exchange-operator/). Each worker keeps its own copy of the occurrence counts and broadcasts its changes to all workers. A worker sends the increase for a new pointstamp before the decrease for the event that caused it, so a local copy may be behind the true counts but never shows a frontier that has gone too far.

## What it counts

The model counts messages, notifications and the updates of the progress protocol, with $p$ the number of active pointstamps and $l$ the number of locations.

- **Per message.** Sending and receiving a message changes two occurrence counts. A count that rises from 0 or falls to 0 changes the precursor counts of up to $p$ pointstamps, so the worst case is $O(p)$ per message. Many messages share a pointstamp, and workers add their changes together before they broadcast them, so the amortized cost per message is close to $O(1)$ when $p$ is small.
- **Memory.** The protocol keeps $O(p)$ counts. The could-result-in relation needs, for each pair of locations, the least change of timestamp along a path, which takes $O(l^2)$ space and is computed once from the graph.
- **Latency.** A notification is delivered as soon as the frontier passes its time, without waiting for all vertices to finish a global step. Vertex state, such as the indexed traces of differential dataflow, is not counted by the model.

## Relation to other models

- **Dataflow and stream models.** In the [dataflow model](/dataflow-model/) and in stream systems with [punctuation](/stream-punctuation/) or an [event-time watermark](/event-time-watermark/), completeness is a message that flows with the data. In timely dataflow it comes from the counts of the protocol, and the frontier plays the role of the watermark for logical time.
- **Logical clocks.** Timestamps and the could-result-in relation are like the [happened-before](/happened-before/) order of [Lamport clocks](/lamport-clocks/) and [vector clocks](/vector-clocks/), as an analogy only: they are set by the program and by the structure of the graph, not by the exchange of messages, and they describe which future events are still possible, not which past events caused an event.
- **Synchronous models.** Bulk synchronous models and [DBSP](/dbsp/) take one step of every operator at each tick. Timely dataflow lets different vertices work on different epochs and iterations at the same time, which is what [differential dataflow](/differential-dataflow/) needs for its partially ordered times.
- **Snapshots.** Progress tracking says when a time is complete, which is the information that a consistent snapshot of a stream job also needs. [Asynchronous barrier snapshotting](/asynchronous-barrier-snapshotting/) gets it from barriers that flow with the data instead.
- **Late data.** An input vertex closes an epoch by giving up its pointstamp for it. A record that arrives after that cannot enter the closed epoch, so it is put in the current epoch. To place records by event time, the input must keep an epoch open until it has seen enough, as with a watermark.

## Known results in the model

- **Safety of notification.** If every vertex sends only at times at or above the time that it is handling, and every cycle passes a feedback vertex, then no pointstamp could result in a different pointstamp that could result in it back, and a notification for $(t, v)$ is delivered only when no message with a time $\le t$ can still arrive at $v$.
- **Progress.** While some pointstamp is active, the frontier is not empty, because could-result-in is a partial order on the finitely many active pointstamps. So some message or notification can always be delivered.
- **Distributed counts.** With the order of updates described above and delivery in order between each pair of workers, the frontier that a worker sees is never ahead of the true frontier, so local decisions to deliver notifications are safe.
- **Expressiveness.** Batch jobs, streams with low latency, iterative graph algorithms and incremental iterative computation run in the same graph. Murray et al. report Naiad running such programs on a cluster, with differential dataflow among them.

## References
