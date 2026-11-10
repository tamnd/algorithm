---
tag: 0C4P35
kind: problem
slug: global-snapshot
name: Global snapshot
aliases:
- distributed snapshot
- consistent global state recording
area: distributed/clocks-and-ordering
level: core
summary: Record the local state of every process and the messages in every channel at one consistent cut, while the computation keeps running. The result is reachable from the start and leads to the end.
prereqs: [consistent-cut]
see_also: [chandy-lamport-snapshot, lai-yang-snapshot, consistent-cut, termination-detection, deadlock-detection, checkpointing, distributed-predicate-detection, global-virtual-time]
sources:
  - paper: doi:10.1145/214451.214456
    title: K. Mani Chandy and Leslie Lamport, Distributed snapshots, determining global states of distributed systems, ACM Transactions on Computer Systems 3(1), 1985
    locator: pages 63 to 75; the problem, the reachability theorem and stable property detection (DOI from memory, to be checked)
  - paper: doi:10.1016/0020-0190(87)90125-6
    title: Ten H. Lai and Tao H. Yang, On distributed snapshots, Information Processing Letters 25(3), 1987
    locator: pages 153 to 158
  - paper: doi:10.1006/jpdc.1993.1075
    title: Friedemann Mattern, Efficient algorithms for distributed snapshots and global virtual time approximation, Journal of Parallel and Distributed Computing 18(4), 1993
    locator: pages 423 to 434
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 4 (global state and snapshot recording algorithms)
---

The *global snapshot* problem asks for a record of the state of a distributed system, the local state of each process and the messages in each channel, taken while the system keeps running. No process can see the whole system at one instant, so the record cannot be a photograph at one real time. Instead it must be the global state of a [consistent cut](/consistent-cut/). Chandy and Lamport (1985) showed that such a record is a state that the system could have passed through, which makes it good enough to detect stable properties such as termination and deadlock.

## In plain words

Imagine counting the money in a bank with many branches that send money to each other all day. You cannot close every branch at the same moment, and while you count, money is on the way between branches. If you count one branch before a transfer leaves and the other after it arrives, the money is counted twice. If you count the other way round, and forget the money on the way, it is lost.

A global snapshot is a method to count each branch once and each transfer exactly once, without closing anything. The result may not match the totals at any single clock time. But it matches a moment that could have happened, so a fact that, once true, stays true (such as "all branches are idle") can be checked on it.

## Definition

**Model.** $n$ processes are connected by directed channels that are reliable and have unbounded delay, as in the [asynchronous model](/asynchronous-model/). Each process has a local state that changes at its events: internal events, sends and receives. The state of a channel is the sequence (or, for non-FIFO channels, the multiset) of messages sent on it and not yet received. A *global state* is a local state for each process and a state for each channel.

**The problem.** While the computation runs, each process $p_i$ records a local state $LS_i$ at some point, and the system records a state $SC_{ij}$ for each channel from $p_i$ to $p_j$, such that:

1. the cut $C$ made of the events of each $p_i$ before it records is a [consistent cut](/consistent-cut/);
2. $SC_{ij}$ is exactly the set of messages that $p_i$ sent before recording and $p_j$ received after recording.

The recorded global state $S^\ast$ is then the global state of $C$. The algorithm may add control messages and piggyback data on application messages, but it may not stop or delay the application.

**Theorem (reachability, Chandy and Lamport).** Let the snapshot start in global state $S_\iota$ and end in global state $S_\phi$. Then $S^\ast$ is reachable from $S_\iota$, and $S_\phi$ is reachable from $S^\ast$.

*Proof.* Let $\sigma = f_1, f_2, \dots, f_r$ be the events that the system ran from $S_\iota$ to $S_\phi$. Call an event *pre* if it is in $C$ and *post* otherwise; events before $S_\iota$ are all pre. No post event happened before a pre event, since $C$ is closed under [happened-before](/happened-before/). Suppose $\sigma$ has a post event $f$ directly followed by a pre event $g$. They are on different processes, since on one process $f$ would happen before $g$. And $g$ is not the receive of a message that $f$ sent, for the same reason. An event is enabled by the state of its own process and, for a receive, by the presence of its message in the channel, and $f$ changes neither of these for $g$. So the sequence with $f$ and $g$ swapped is also a run, and it ends in the same state. Repeat until all pre events come first; each swap removes one inverted pair, so this ends. In the new run $\sigma'$, after the pre events, each process has run exactly its events in $C$, so its state is $LS_i$, and each channel holds the messages sent in $C$ and not received in $C$, which is $SC_{ij}$. So $\sigma'$ goes from $S_\iota$ through $S^\ast$ to $S_\phi$. $\square$

**Stable properties.** A predicate $\Phi$ on global states is *stable* if $\Phi(S)$ implies $\Phi(S')$ for every $S'$ reachable from $S$. Examples are "the computation has terminated", "these processes are deadlocked" and "this object is garbage".

**Corollary (stable property detection).** If $\Phi$ is stable, then $\Phi(S^\ast)$ implies $\Phi(S_\phi)$, and $\Phi(S_\iota)$ implies $\Phi(S^\ast)$.

*Proof.* Both follow from the theorem and the definition of stable. $\square$

So a snapshot that shows $\Phi$ proves that $\Phi$ holds now; and if $\Phi$ already held when the snapshot started, the snapshot shows it. Repeated snapshots detect a stable property at most one snapshot after it becomes true.

## Variants

- **FIFO or non-FIFO channels.** With FIFO channels a marker can separate the messages before and after a recording. With non-FIFO channels the messages must carry the information themselves.
- **Who starts.** One process, or several at once; the algorithms must give one consistent cut even if many start.
- **Repeated snapshots.** Each snapshot has a number, so that markers and colours of different snapshots do not mix.
- **Incremental and causal channels.** With causal delivery the channel states can be computed with fewer messages.
- **Unstable properties.** A predicate that may become true and false again needs a search over all consistent cuts, not one snapshot; see [distributed predicate detection](/distributed-predicate-detection/).

## Examples

**A bank with two branches.** Branch $p_0$ has 100 and branch $p_1$ has 50, so the bank holds 150. At time 1, $p_1$ sends 30 to $p_0$; the transfer takes 4 time units. At time 2, $p_0$ starts a snapshot and records 100. Its marker reaches $p_1$ first; $p_1$ records 20. Then the transfer of 30 reaches $p_0$, after $p_0$ recorded but before the marker of $p_1$ arrived, so it is recorded as the state of the channel from $p_1$ to $p_0$. The snapshot holds $100 + 20 + 30 = 150$. Here the recorded state really existed, from time 1 to time 5. In other runs the recorded state may never occur at any real time, but by the theorem it is always reachable.

**A wrong record.** If $p_1$ recorded 50 before sending, and $p_0$ recorded 130 after receiving, the record would hold 180: the cut holds the receive of the 30 without its send. This cut is not consistent.

## Known algorithms

| Algorithm | Channels | Control | Cost |
|---|---|---|---|
| [Chandy-Lamport](/chandy-lamport-snapshot/) (1985) | FIFO | one marker on each channel | $O(e)$ markers for $e$ channels |
| [Lai-Yang](/lai-yang-snapshot/) (1987) | non-FIFO | a colour bit on each message, message histories | no control messages; histories grow |
| Mattern (1993) | non-FIFO | colours and message counters | counters instead of histories |
| Synchronized clocks | any | record at an agreed clock time | needs skew below the least message delay |
| Logical clocks | any | record at an agreed [Lamport time](/lamport-clocks/) | processes must reach the agreed time |

## Bounds

- **Messages.** Chandy-Lamport sends exactly one marker on each channel, so $e$ markers in all, and this is enough on FIFO channels. Lai-Yang sends no control messages beyond what the processes already send, but it piggybacks one bit on each message and stores the histories of sent and received messages.
- **Time.** On a network of diameter $D$ with one initiator, every process records within $D$ marker hops of the start, so a snapshot takes $O(D)$ message delays.

## Reductions

- **From clocks.** Let drift-free clocks have [skew](/clock-skew/) at most $\pi$, and let every message take at least $d_{\min} > \pi$. If each process records when its clock reads $T$, the cut is consistent. *Proof.* A message sent after the sender records leaves at a real time $t$ with $C_s(t) \ge T$, and arrives at a real time $t' \ge t + d_{\min}$. Then $C_r(t') = C_r(t) + (t' - t) \ge C_s(t) - \pi + d_{\min} > T$, so it is received after the receiver records. So no message crosses the cut from after to before. $\square$
- **From logical clocks.** The set of events with a [Lamport timestamp](/lamport-clocks/) at most $T$ is a consistent cut, because $f \to e$ implies $L(f) < L(e)$.
- **Termination and deadlock detection.** Both properties are stable, so they reduce to taking snapshots and checking the property on them (see [termination detection](/termination-detection/) and [deadlock detection](/deadlock-detection/)).
- **Global virtual time.** The [global virtual time](/global-virtual-time/) of an optimistic simulation is the minimum timestamp in a consistent snapshot of processes and channels, and Mattern's snapshot algorithm computes it.

## Applications

- Checkpointing for recovery: stream processors such as Apache Flink take asynchronous snapshots in the style of Chandy and Lamport, with barriers in the streams.
- Detection of termination, deadlock and garbage in distributed systems.
- Debugging and monitoring: a consistent view of a running system.
- Computing the global virtual time in [Time Warp](/time-warp/).

## References
