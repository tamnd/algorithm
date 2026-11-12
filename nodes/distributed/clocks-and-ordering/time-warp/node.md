---
tag: GQ6HAV
kind: algorithm
slug: time-warp
name: Time Warp
aliases:
- optimistic parallel simulation
area: distributed/clocks-and-ordering
level: research
summary: Optimistic parallel simulation. Each process runs its events at once. A message from its past rolls it back, and antimessages cancel what the undone events sent. Work below GVT is final.
solves: [parallel-discrete-event-simulation]
model: asynchronous-model
complexity:
  vars: {E: the number of events of the sequential simulation, R: the number of events that rollbacks undo}
  time: {worst: O((E + R) log(E + R))}
  space: {extra: O(E + R)}
  messages: {worst: O(E + R)}
properties: {deterministic: true, recursive: false}
history:
  year: 1985
  people: [David R. Jefferson]
  note: Jefferson published virtual time and the Time Warp mechanism, with rollback, antimessages and global virtual time, in ACM Transactions on Programming Languages and Systems in 1985.
prereqs: [parallel-discrete-event-simulation, virtual-time]
see_also: [global-virtual-time, chandy-misra-bryant, virtual-time, parallel-discrete-event-simulation, lai-yang-snapshot, optimistic-concurrency-control, checkpointing]
sources:
  - paper: "David R. Jefferson, Virtual time, ACM Transactions on Programming Languages and Systems 7(3), 1985, pages 404 to 425"
    locator: the Time Warp mechanism (state queues, rollback, antimessages and annihilation, global virtual time and fossil collection), and the argument that GVT never decreases (volume and pages from memory, to be checked)
  - paper: "Richard M. Fujimoto, Parallel discrete event simulation, Communications of the ACM 33(10), 1990, pages 30 to 53"
    locator: the section on optimistic methods (lazy and aggressive cancellation, state saving; volume and pages from memory, to be checked)
  - book: isbn:9780471183839
    title: Richard M. Fujimoto, Parallel and Distributed Simulation Systems, Wiley, 2000
    locator: the chapters on Time Warp, state saving, cancellation and memory management (ISBN from memory, to be checked)
  - paper: "David R. Jefferson and Henry A. Sowizral, Fast concurrent simulation using the Time Warp mechanism, part I, local control, Rand Note N-1906-AF, The RAND Corporation, 1982"
    locator: the first description of Time Warp (title, number and year from memory, to be checked)
  - paper: "David Jefferson and others, Distributed simulation and the Time Warp Operating System, Proceedings of the 11th ACM Symposium on Operating Systems Principles (SOSP), 1987"
    locator: the Time Warp Operating System at the Jet Propulsion Laboratory (authors and venue from memory, to be checked)
---

*Time Warp* is the optimistic method for [parallel discrete event simulation](/parallel-discrete-event-simulation/), introduced by David Jefferson with [virtual time](/virtual-time/) in 1985. Each logical process (LP) runs its next event at once, without waiting to learn whether an earlier event is still on its way. If one comes later, a *straggler*, the LP *rolls back*: it restores the state saved before the events it ran too early, and for every message those events sent it sends an *antimessage* that cancels it. The least timestamp in the whole system, the [global virtual time](/global-virtual-time/) (GVT), is a time below which nothing can be undone, so the work below it is final and its saved states can be freed.

## In plain words

A teller in a simulated bank serves her queue as fast as she can. Sometimes a customer turns up who, in simulated time, arrived earlier than the ones she has already served. Then she goes back: she restores the state of her desk to the moment when that customer arrived, and she serves everyone again in the right order.

Her first service may have sent forms to other desks that are now wrong. So for each such form, she sends an "ignore that form" note. A desk that gets such a note before the form throws both away. A desk that already used the form goes back in time itself.

Each desk keeps old states in case it has to go back. But no desk can ever be sent back before the earliest work still pending anywhere in the bank. Everything before that time is safe to forget.

## The problem

**Model.** As in [parallel discrete event simulation](/parallel-discrete-event-simulation/): $n$ LPs, events with unique keys $(\mathrm{ts}, \text{tie key})$, and running an event at an LP is a deterministic function of the LP state and the event, which schedules new events with larger timestamps. LPs communicate by reliable messages with unbounded delay; the channels need not be FIFO. Processes do not fail.

**Goal.** At the end, each LP has run, and committed, the same events with the same states as in the sequential simulation. Nothing below a known time may be undone, so that output and memory below that time can be released.

## The algorithm

Each LP keeps its pending events, sorted by key; its processed events, each with the state before it and the messages it sent; and a set of antimessages that came before their message.

```pseudo id=main
RUN(i)                                          ▷ whenever LP i has a pending event
L1  e ← the pending event with the least key; remove it from the pending events
L2  save (e, the state before e); run e; send the events it schedules; save them with e

RECEIVE(i, m)                                   ▷ a message, positive or an antimessage
    if m is positive
        if its antimessage is waiting here then delete both and return
L3      if key(m) < the key of the last processed event then ROLLBACK(i, key(m))
        add m to the pending events
    else
L4      if the event of m has been processed then ROLLBACK(i, key(m))
L5      if the event of m is pending then remove it, else keep m until its event comes

ROLLBACK(i, k)
    for each processed event e with key ≥ k, the latest first
L6      restore the state saved before e; put e back into the pending events
L7      for each message that e sent, send its antimessage

FOSSIL-COLLECT(g)                               ▷ g: the GVT, or a lower bound on it
L8  commit, and forget the saved states of, the processed events with timestamp < g
```

The GVT is the least timestamp of all pending events and all messages in transit, positive or negative. A separate algorithm, such as Mattern's in [global virtual time](/global-virtual-time/), computes a lower bound on it while the simulation runs. The implementation here reads it exactly from the simulator.

## Example

Two LPs, $A$ and $B$. The state of an LP is a number, and an event with value $x$ adds $x$ to it. $B$ has pending events at times 5 and 8; $A$ is slow.

| step | at $B$ | state of $B$ |
|---|---|---|
| 1 | runs the event at 5 (L1, L2), saves 0 | 5 |
| 2 | runs the event at 8, saves 5; the event sends $+[12]$ to $A$ | 13 |
| 3 | a message from $A$ for time 6 arrives: a straggler (L3) | |
| 4 | rolls back the event at 8: restores 5 (L6), puts it back, sends $-[12]$ to $A$ (L7) | 5 |
| 5 | runs the event at 6 | 11 |
| 6 | runs the event at 8 again, which sends a new $+[12]$ to $A$ | 19 |

The final state $19 = 5 + 6 + 8$ is the result of running the three events in time order. At $A$, the antimessage $-[12]$ either meets $+[12]$ in the pending events and both go (L5), or arrives first and waits for it, or finds that $A$ already ran it, and then $A$ rolls back to 12 (L4). In this example the new message has the same content as the old one; the variant *lazy cancellation* would notice this and send neither the antimessage nor the copy.

If the GVT is 7 after step 6, $B$ commits the events at 5 and 6 and forgets their saved states (L8). The event at 8 stays undoable.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

- **Order.** Every pending key is above every processed key, at all times: line L1 takes the least pending event, and line L3 rolls back before it adds an earlier one. So each LP's processed events are always in key order, each run on the state that its predecessors left.
- **Cancellation.** An event is cancelled exactly when the run of the event that sent it is undone, since line L7 is the only source of antimessages, and lines L4 and L5 remove the event wherever it is. So when the run ends, the events that are left are the initial ones and those sent by runs that were never undone.
- **Equal to the sequential result.** These two facts give each LP exactly the hypothesis of the theorem on the [PDES page](/parallel-discrete-event-simulation/): it ran exactly the events scheduled for it by the final runs, in key order.
- **GVT.** Every new event, message or antimessage has a timestamp at least the GVT at the time it is made, so the GVT never decreases, and no rollback ever undoes an event below it. Fossil collection is safe.

The seeded tests run 30 simulations of 2 to 6 LPs with random delays and compare the committed events and final states with the sequential simulation; the runs did roll back and did send antimessages. Every rollback checks that it stays above the last GVT, and the GVT values of each run are checked to never decrease.

## Complexity

Without rollbacks, each of the $E$ events is run once, with $O(\log E)$ time for a priority queue, and it sends its messages. Each event that a rollback undoes costs a restore, a reinsertion and one antimessage for each message that it sent, and it is run again later. With $R$ undone events and a bounded number of messages per event, as in the model here, this is $O((E + R) \log (E + R))$ time and $O(E + R)$ messages. $R$ has no bound in terms of $E$: in bad cases, rollbacks cascade from LP to LP. The saved states take $O(E + R)$ space without fossil collection, and fossil collection keeps only those above the GVT.

## Properties

- **No lookahead needed.** It works when an event can schedule another event at almost the same time, where [conservative methods](/chandy-misra-bryant/) are slow.
- **Not deterministic in its work.** The amount of rollback depends on the delays and the speed of the processors. The committed result does not.
- **Memory hungry.** Each LP keeps old states until the GVT passes them.
- **Output must wait.** An event can be undone until the GVT passes it, so printing, writing to disk or any action that cannot be undone must wait for the commit.

## Variants and improvements

- **Lazy cancellation.** After a rollback, do not send the antimessages at once. Run the events again, and send an antimessage only for a message that the new run does not send again.
- **State saving.** Save a full copy of the state before each event, or only the changes, or every $k$ events and run forward from the last copy after a rollback.
- **Reverse computation.** Instead of saving the state, run an inverse of each event to undo it.
- **Throttling.** Limit how far an LP may run ahead of the GVT, to bound rollbacks and memory.
- **Hybrid methods.** Use lookahead where it is known and run optimistically only where it is not.

## When to use it

Use it when the model has little or no lookahead, so that conservative methods would mostly wait, and when the state of each LP is small or easy to save or reverse. It also fits when the links between LPs change during the run, since it needs no fixed graph.

## Pitfalls

- **Cascading rollbacks.** A rollback sends antimessages, which roll back other LPs, which send more antimessages. Lazy cancellation and throttling reduce this.
- **Running out of memory.** Without a GVT algorithm and fossil collection, the saved states grow with the length of the run.
- **Antimessages that arrive first.** On non-FIFO channels an antimessage can overtake its message. It must be kept until the message arrives, or the message will run and never be cancelled.
- **Side effects.** An event that writes a file or sends a packet to the outside world cannot be rolled back. Hold such output until the GVT passes its time.
- **Equal timestamps.** Rollback compares keys, so the tie key must be unique and the same in every run; otherwise a run of the same event may get a different key and its antimessage will not match.

## Implementations

## History

David Jefferson worked out Time Warp with Henry Sowizral in the early 1980s and published it, with the general theory of virtual time, in ACM Transactions on Programming Languages and Systems in 1985. With colleagues at the Jet Propulsion Laboratory he then built the Time Warp Operating System. Lazy cancellation, incremental state saving and many GVT algorithms followed in the late 1980s and 1990s, and Fujimoto's survey of 1990 compared the optimistic and conservative methods.

## References
