---
tag: A6GVSF
kind: problem
slug: parallel-discrete-event-simulation
name: Parallel discrete event simulation
aliases:
- PDES
- distributed discrete event simulation
area: distributed/clocks-and-ordering
level: advanced
summary: Run a discrete event simulation on several processors, split into logical processes that exchange timestamped events, and get the same result as one processor that runs every event in timestamp order.
prereqs: [virtual-time, event-driven-simulation]
see_also: [chandy-misra-bryant, time-warp, global-virtual-time, virtual-time, event-driven-simulation, calendar-queue, lamport-clocks]
sources:
  - paper: "Richard M. Fujimoto, Parallel discrete event simulation, Communications of the ACM 33(10), 1990, pages 30 to 53"
    locator: the problem, the local causality constraint, conservative and optimistic methods, lookahead (volume and pages from memory, to be checked)
  - paper: "Jayadev Misra, Distributed discrete-event simulation, ACM Computing Surveys 18(1), 1986, pages 39 to 65"
    locator: the model of logical processes and channels, null messages, and deadlock (volume and pages from memory, to be checked)
  - book: isbn:9780471183839
    title: Richard M. Fujimoto, Parallel and Distributed Simulation Systems, Wiley, 2000
    locator: the chapters on the local causality constraint, conservative synchronization, synchronous window methods, Time Warp and global virtual time (ISBN from memory, to be checked)
  - paper: "David R. Jefferson, Virtual time, ACM Transactions on Programming Languages and Systems 7(3), 1985, pages 404 to 425"
    locator: virtual time as the correctness criterion, and Time Warp (volume and pages from memory, to be checked)
---

*Parallel discrete event simulation* (PDES) runs one [discrete event simulation](/event-driven-simulation/) on many processors. The model is split into *logical processes* (LPs), for example one per router of a network or one per station of a factory, that send each other events with timestamps. A sequential simulator runs every event in timestamp order from one queue; a parallel simulator must give the same result while each processor runs its own LPs. The difficulty is that an LP cannot know whether an event with a smaller timestamp is still on its way. *Conservative* methods such as the [Chandy-Misra-Bryant algorithm](/chandy-misra-bryant/) wait until it is safe; *optimistic* methods such as [Time Warp](/time-warp/) go ahead and roll back when they were wrong.

## In plain words

A sequential simulator keeps one list of future events, sorted by simulated time. It takes the earliest event, runs it, which may add later events to the list, and repeats. The simulated time jumps from event to event.

To use many processors, give each part of the model its own list and its own processor. A part that runs an event may create an event for another part, and sends it as a message. Now each part must still run its own events in time order. But part $B$ may be at simulated time 50 when part $A$, which is slower, sends it an event for time 40. Either $B$ should have waited, or it must undo what it did after 40. Every PDES method is a choice between these two.

## Definition

**Model.** There are $n$ logical processes. LP $i$ has a state $S_i$. An *event* $e$ has a timestamp $\mathrm{ts}(e)$, a destination LP, and a unique key $k(e) = (\mathrm{ts}(e), \text{tie key})$, so that events are totally ordered. Running $e$ at its LP is a deterministic function of $S_i$ and $e$: it changes $S_i$, and it schedules zero or more new events $e'$ with $\mathrm{ts}(e') > \mathrm{ts}(e)$. Some events are given at the start, and an end time $T$ stops the simulation.

**The sequential simulation.** Put the initial events in a priority queue, and repeatedly remove the event with the least key and run it. This defines, for each LP, the list of the events that it runs and its final state.

**The problem.** Run the LPs on several processors that communicate only by messages, and output, for every LP, the same list of events and the same final state as the sequential simulation.

**The local causality constraint.** Each LP runs the events sent to it in increasing order of key.

**Theorem (local order is enough).** If every LP runs exactly the events that are scheduled for it, in increasing order of key, then every LP runs the same events, in the same order and with the same states, as in the sequential simulation.

*Proof.* Let $Q$ be the events of the sequential run and $P$ the events of the parallel run. We show by induction on the keys that an event is in $Q$ if and only if it is in $P$, and that it is run on the same state in both. Take the event $e$ with the least key for which this fails, in $Q$ or in $P$. If $e$ is an initial event, it is in both. Otherwise its parent $p$, the event that scheduled it, has a smaller key, so by the choice of $e$, $p$ is in both runs and is run on the same state, and so it schedules the same children in both: $e$ is in both. The events of the LP of $e$ with keys below $k(e)$ are the same in both runs, again by the choice of $e$, and both runs run them in key order before $e$. So the state before $e$ is the same, a contradiction. $\square$

This is Theorem 2 of the page on [virtual time](/virtual-time/), with simulation time as the virtual time.

## Variants

- **Conservative or optimistic.** A conservative simulator never breaks the local causality constraint. An optimistic one breaks it for a while and repairs the effect by a rollback.
- **Asynchronous or synchronous.** In asynchronous methods each LP moves at its own pace. In synchronous, or window, methods all LPs process the events of one time window $[t, t + w)$ and then meet at a barrier.
- **Lookahead.** An LP has lookahead $L$ if every event it schedules has a timestamp at least $L$ above its own current time. Conservative methods need $L > 0$; their speed grows with it.
- **Zero delay.** If an event may schedule another event at the same timestamp, the tie key must order them, and conservative methods must handle cycles of zero delay.
- **Shared memory or message passing.** On shared memory the LPs can share one global view of the least timestamp, which makes the synchronization cheaper.

## Examples

**A factory line.** LP $A$ is a machine that sends each finished part to LP $B$, a second machine, and $B$ sends some parts back to $A$ for rework. A part takes at least 2 time units on each machine. The sequential order of events is the order of their timestamps across both machines. In parallel, $B$ at time 30 may not run an event for time 35 while $A$ is still at time 20, since $A$ may still send a part to $B$ for any time from 22 on. With lookahead $L = 2$, $B$ may run its events up to time 22 without waiting, because nothing from $A$ can arrive below 22.

**A causality error.** If $B$ ran its event for time 35, and then a part from $A$ arrived for time 25, the state that $B$ used at time 35 would be wrong: it misses the part of time 25. A conservative method prevents this; [Time Warp](/time-warp/) undoes the event of time 35, runs the one of time 25, and runs time 35 again.

## Known algorithms

| Method | Kind | Idea |
|---|---|---|
| [Chandy-Misra-Bryant](/chandy-misra-bryant/) (1977 to 1979) | conservative, asynchronous | an LP runs an event when every input link has a larger bound; null messages carry bounds to avoid deadlock |
| Deadlock detection and recovery (Chandy and Misra 1981) | conservative, asynchronous | no null messages; detect the deadlock, then run the events with the least timestamp |
| Window methods | conservative, synchronous | compute a safe window from the least timestamp and the lookahead, run it, and meet at a barrier |
| [Time Warp](/time-warp/) (Jefferson 1985) | optimistic | run at once; on a straggler, roll back and send antimessages; commit below the [global virtual time](/global-virtual-time/) |

**Why the window method is safe.** Let $t$ be the least timestamp of all unprocessed events and events in transit, and let every LP have lookahead $L$. Each event run in the window $[t, t + L)$ has a timestamp of at least $t$, so it schedules events at $t + L$ or later. So no event in the window can be created by another event in the window, and the LPs can run the window in parallel, each in key order, without any causality error. $\square$

## Bounds

- **The critical path.** Draw an arrow from each event to the next event of the same LP and to each event that it schedules. If every event costs one unit and an event can run only after the events before it on these arrows, then no simulator that keeps the local causality constraint finishes in fewer units than the longest path of arrows, whatever the number of processors. The sequential simulator takes as many units as there are events, so the ratio of the two bounds the speedup.
- **Lookahead.** In the [Chandy-Misra-Bryant algorithm](/chandy-misra-bryant/), take a cycle of LPs with lookahead $L$ and no events to run. Each null message carries the bound it got plus exactly $L$, so moving the bounds from 0 to time $T$ takes about $T / L$ null messages along the cycle. Small lookahead makes conservative methods slow.
- **Memory.** An optimistic method must keep the state that it may roll back to; without [global virtual time](/global-virtual-time/) and fossil collection, the memory grows with the length of the run.

## Reductions

- **To virtual time.** PDES is the problem of executing a program in [virtual time](/virtual-time/), with simulation time as the virtual time.
- **Global virtual time to snapshots.** The least timestamp of the unprocessed and in-transit events is a property of a consistent global state, so a [global snapshot](/global-snapshot/), or Mattern's colouring, computes it.
- **Deadlock.** A conservative simulator without null messages can stop with work left, a [deadlock](/deadlock/); the null messages of Chandy-Misra-Bryant and the detection and recovery of Chandy and Misra are two answers.

## Applications

- Simulation of computer networks and of the Internet, with one LP per router or per host.
- Simulation of digital circuits, with one LP per gate or block.
- Military and training simulations, which link many simulators with the time management of the High Level Architecture, IEEE 1516.
- Simulation of traffic, epidemics and supply chains with many agents.

## References
