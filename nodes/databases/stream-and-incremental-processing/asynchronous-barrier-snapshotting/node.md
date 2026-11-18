---
tag: 8TJ3Y4
kind: algorithm
slug: asynchronous-barrier-snapshotting
name: Asynchronous barrier snapshotting
aliases:
- ABS
- barrier-aligned checkpointing
area: databases/stream-and-incremental-processing
level: research
summary: "Take consistent snapshots of a stream job by injecting barriers into the sources and aligning them at each operator, without stopping the job."
solves: [global-snapshot]
model: word-ram
complexity:
  vars: {s: the size of the states of all tasks, c: the number of channels, b: the number of records held at blocked inputs or logged on back edges}
  time: {worst: "O(s + c + b)", average: "O(s + c + b)", best: "O(s + c)"}
  space: {extra: "O(s + b)"}
properties: {deterministic: true, exact: true, online: true, external: false, in_place: false, recursive: false}
history:
  year: 2015
  people: [Paris Carbone, Gyula Fóra, Stephan Ewen, Seif Haridi, Kostas Tzoumas]
  note: "Carbone, Fóra, Ewen, Haridi and Tzoumas described the algorithm in 2015 as the snapshot method of Apache Flink, an adaptation of the Chandy and Lamport snapshot to dataflow jobs."
prereqs: [chandy-lamport-snapshot, consistent-cut]
see_also: [chandy-lamport-snapshot, consistent-cut, global-snapshot, checkpointing, backpressure, two-phase-commit, timely-dataflow, event-time-watermark]
sources:
  - paper: arxiv:1506.08603
    title: "Paris Carbone, Gyula Fóra, Stephan Ewen, Seif Haridi and Kostas Tzoumas, Lightweight asynchronous snapshots for distributed dataflows, arXiv 2015"
    locator: "Section 4.1 (the snapshot problem on the graph of tasks and channels, with termination and feasibility), Section 4.2 and Algorithm 1 (acyclic graphs, no channel state), Section 4.3 and Algorithm 2 (cyclic graphs, back edges found by depth-first search and logged), Section 5 (recovery)"
  - paper: "Paris Carbone, Stephan Ewen, Gyula Fóra, Seif Haridi, Stefan Richter and Kostas Tzoumas, State management in Apache Flink, consistent stateful distributed stream processing, PVLDB 10(12), 2017, pages 1718 to 1729"
    title: "State management in Apache Flink: consistent stateful distributed stream processing"
    locator: "the snapshot protocol as used in production, with partitioned state, alignment, rescaling and outputs to external systems (general locator)"
  - paper: doi:10.1145/214451.214456
    title: "K. Mani Chandy and Leslie Lamport, Distributed snapshots, determining global states of distributed systems, ACM Transactions on Computer Systems 3(1), 1985, pages 63 to 75"
    locator: "the marker rules and the proof that the recorded state is reachable, which this algorithm adapts (general locator)"
---

Asynchronous barrier snapshotting is an algorithm that takes a consistent snapshot of a running stream job: the sources put a *barrier* into their output streams, and each task copies its state when the barrier has arrived on all its inputs, holding back the inputs on which it came first. It solves the [global snapshot](/global-snapshot/) problem for dataflow graphs. The [Chandy and Lamport snapshot](/chandy-lamport-snapshot/) also sends markers, but it records the records in flight on every channel, while this algorithm records no channel state on an acyclic graph and logs only the records on the back edges of cycles. Unlike a database [checkpoint](/checkpointing/) with a log, recovery restores the copies and replays the inputs from the stored offsets.

## In plain words

Workers pass items along fixed lines, and each worker keeps counts. You want a photo of all counts that fits together, without stopping work.

At the start of the lines, you drop a flag into each line. A worker that sees a flag on one input line stops taking from that line and keeps working on the others. When the flag has come on all its input lines, the worker writes down its counts, sends the flag on, and takes from all lines again. So every count in the photo includes exactly the items that came before the flags.

After a crash, every worker starts from its written counts, and the lines start again from the place where the flags went in. Each item is counted once. If the lines form a loop, a worker also writes down the items that come back around the loop before the flag does.

## The problem

A job is a directed graph of tasks joined by FIFO channels that lose no message. Sources read records from inputs that can be read again from any offset, such as a log. Every other task has a state and applies a deterministic operator to each record. A snapshot must hold a state for each task, an offset for each source, and the records in flight on each channel, all at one [consistent cut](/consistent-cut/): no record is counted in the state of its receiver unless its sender had sent it in its own part of the snapshot. Restarting the job from the snapshot must then give a run in which each input record changes each state once. The job must not stop while the snapshot is taken.

## The algorithm

A depth-first search from the sources marks the *back edges*, the channels that close a cycle. All other channels are regular, and they form an acyclic graph. For snapshot $n$:

```pseudo id=main
ON-BARRIER(t, c, n)                      ▷ task t takes barrier n from input channel c
L1  if c is regular then block c; seen ← seen ∪ {c}  else mark the back edge c
L2  if t has no copy for n and seen holds every regular input of t then
L3      send barrier n on every output channel of t
L4      copy ← the state of t;  log ← empty;  start logging
L5      unblock every input of t;  seen ← ∅
L6  if t is logging and barrier n has come on every back edge into t then
L7      stop logging; store (copy, log) as the part of t in snapshot n
ON-RECORD(t, c, x)
L8  if t is logging and c is a back edge then append (c, x) to log
L9  apply the operator of t to x and send its output records
ON-TRIGGER(s, n)                         ▷ the coordinator starts snapshot n at source s
L10 store the offset of s as its part of snapshot n; send barrier n on every output channel of s
```

A blocked channel keeps its records in its buffer until line L5. On an acyclic graph, line L6 holds at once and the log is empty, which is Algorithm 1 of Carbone et al. With cycles, the back edges are never blocked, since a task that waits for a barrier from its own cycle would wait forever; the records logged at line L8 are the state of those channels, which is Algorithm 2. The snapshot is complete when every task has stored its part.

To recover, every task gets its copy, every source goes back to its stored offset, the regular channels are empty, and each log is put at the front of its back edge.

## Example

Sources $s_1$ and $s_2$ read the records 1, 4 and the record 5. Tasks $m_1$ and $m_2$ map $x$ to $x \bmod 3$, and a task cnt with inputs from $m_1$ and $m_2$ counts the keys. The steps are:

1. $s_1$ sends 1. Snapshot 0 starts: $s_1$ stores offset 1 and sends the barrier, then sends 4. $s_2$ sends 5, stores offset 1 and sends the barrier.
2. $m_1$ passes the key 1, the barrier and the key 1 of record 4. $m_2$ passes the key 2 and the barrier.
3. cnt takes the key 1, then the barrier from $m_1$, and blocks that input. The key of record 4 waits in its buffer.
4. cnt takes the key 2 from $m_2$, then the barrier from $m_2$. It copies its state and unblocks.

| | with alignment | copy at the first barrier, no blocking |
|---|---|---|
| copy of cnt | $\{1{:}\ 1,\ 2{:}\ 1\}$ | $\{1{:}\ 1\}$ |
| cnt after recovery from offsets 1 and 1 and a run to the end | $\{1{:}\ 2,\ 2{:}\ 1\}$ | $\{1{:}\ 2\}$ |
| cnt in the run without failure | $\{1{:}\ 2,\ 2{:}\ 1\}$ | $\{1{:}\ 2,\ 2{:}\ 1\}$ |

Without blocking, cnt takes the key 2 after its copy, but $s_2$ had sent record 5 before its offset. The record is in neither the copy nor the replay, and it is lost.

## Correctness

Barrier $n$ leaves a task at the moment of its copy, and a task copies only after it has taken the barrier from every regular input. So along a regular channel the receiver copies after the sender, and along a back edge the sender copies after the receiver, because the search reached the sender from the receiver along regular channels. Blocking makes sure that a task takes, before its copy, only records that were ahead of the barrier on their channel, so their senders sent them before their own copies: the copies form a consistent cut. On a regular channel every record ahead of the barrier is taken before the copy, so the channel is empty in the cut. On a back edge the records in flight are those that arrive after the copy and before the barrier, which is what line L8 logs. Ordering the events before the cut by their real order gives a run of the job that ends in the snapshot, and so recovery continues a run without failure. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

Costs are in the [word RAM](/word-ram/) model, per snapshot and per record, in the worst case and not amortized.

- **Per record.** Line L8 and the test for a blocked input add $O(1)$ time to each record, in the worst case.
- **Per snapshot.** Each barrier crosses each channel once, $O(c)$, and the copies cost $O(s)$. Logging and buffering add $O(b)$, so a snapshot costs $O(s + c + b)$, and $O(s + c)$ on an acyclic graph whose inputs are never blocked long. A real system writes the copies to durable storage in the background, with copy-on-write state, so that the tasks do not wait for the write.
- **Memory.** The copies take $O(s)$. The buffers of the blocked inputs hold the records that arrive between the first and the last barrier at a task, and the logs hold the records on back edges during a snapshot. Both are $O(b)$, and the algorithm alone does not bound $b$: it depends on how far the barriers of the inputs of a task are apart, which [backpressure](/backpressure/) limits by slowing the sources.

## Properties

- **Exactly once for the state.** Each input record changes each task state once, after any number of failures, if the sources can replay and the operators are deterministic.
- **Asynchronous.** No global pause: a task stops only the inputs on which the barrier has come, and only until its other inputs catch up.
- **Small snapshots.** On acyclic graphs no record in flight is stored. The snapshot is the task states and the source offsets.
- **Late data.** The barrier divides the records by the order in which they arrive, not by event time. A late record is an ordinary record, and the state of event-time operators, such as their open windows and the current [event-time watermark](/event-time-watermark/), is part of the copy. After recovery the replay delivers the same records in the same order, so a late record is either handled or dropped exactly as in the run without failure.

## Variants and improvements

- **Without alignment, at least once.** Tasks do not block and copy at the last barrier. Records after an early barrier are in the copy and are replayed again, so recovery can count them twice. Systems offer this for lower latency when duplicates are acceptable.
- **Unaligned barriers.** A task copies its state at the first barrier and also stores, as channel state, the records that are ahead of the barrier on the other inputs, as in the Chandy and Lamport snapshot. This removes the wait for slow inputs at the price of larger snapshots. Apache Flink added such a mode later.
- **Incremental copies.** Only the part of the state that changed since the last snapshot is written.
- **Outputs to external systems.** The snapshot covers only the internal state. Writes to an outside system are made exactly once by holding them in a transaction that commits when the snapshot completes, which is a form of [two-phase commit](/two-phase-commit/).

## When to use it

Use it for fault tolerance of long-running stateful stream jobs with replayable sources, where the job must keep running while it is backed up, and where the state is large but the records in flight should not be stored. With very skewed inputs, where barriers arrive far apart and alignment holds back too much, use unaligned barriers. Prefer [Chandy and Lamport](/chandy-lamport-snapshot/) when there are no sources to replay from and all channel state must be stored.

## Pitfalls

- **No alignment.** Copying at the first barrier without blocking loses records, as in the example. Copying at the last barrier without blocking counts some twice.
- **Blocking back edges.** A task in a cycle that waits for the barrier from its back edge waits for itself, and the snapshot never completes.
- **Sources that cannot replay.** Offsets mean nothing if the input cannot be read again from them, so a socket or a queue without retention gives no exactly-once guarantee.
- **Nondeterministic operators.** Operators that read the clock or a random source give a different run after recovery. The run is still consistent with the snapshot, but its outputs can differ from those already sent.
- **Slow alignment.** A slow input holds back the barrier of all other inputs of its task, and the buffers grow, which raises latency and memory until backpressure acts.

## Implementations

## History

Chandy and Lamport (1985) gave the snapshot algorithm with markers on FIFO channels that records channel states. Carbone, Fóra, Ewen, Haridi and Tzoumas (2015) adapted it to dataflow jobs as asynchronous barrier snapshotting, with alignment to remove channel state on acyclic graphs and logging only on back edges, and used it in Apache Flink. Carbone, Ewen, Fóra, Haridi, Richter and Tzoumas (2017) described the state management of Flink built on it, including outputs to external systems.

## References
