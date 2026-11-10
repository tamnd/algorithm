---
tag: YJ10N1
kind: concept
slug: virtual-time
name: Virtual time
aliases:
- logical simulation time
area: distributed/clocks-and-ordering
level: advanced
summary: A time axis that the program sets, not the hardware. Each message has a send and a receive time, and each process must act as if it handled its messages in order of receive time.
prereqs: [happened-before, lamport-clocks]
see_also: [lamport-clocks, time-warp, chandy-misra-bryant, global-virtual-time, parallel-discrete-event-simulation, event-driven-simulation, happened-before]
sources:
  - paper: "David R. Jefferson, Virtual time, ACM Transactions on Programming Languages and Systems 7(3), 1985, pages 404 to 425"
    locator: the definition of virtual time, the two rules on send and receive times, the correctness criterion, and the Time Warp mechanism (volume and pages from memory, to be checked)
  - paper: doi:10.1145/359545.359563
    title: Leslie Lamport, Time, clocks, and the ordering of events in a distributed system, Communications of the ACM 21(7), 1978
    locator: pages 558 to 565, the Clock Condition, which virtual time satisfies
  - book: isbn:9780471183839
    title: Richard M. Fujimoto, Parallel and Distributed Simulation Systems, Wiley, 2000
    locator: the chapters on the local causality constraint, conservative synchronization, Time Warp, and the time management services of the High Level Architecture (ISBN from memory, to be checked)
  - paper: "David Jefferson and others, Distributed simulation and the Time Warp Operating System, Proceedings of the 11th ACM Symposium on Operating Systems Principles (SOSP), 1987"
    locator: the design of the Time Warp Operating System at the Jet Propulsion Laboratory (authors and venue from memory, to be checked)
---

*Virtual time* is a time axis that a distributed program defines for itself, separate from the clocks of the machines. David Jefferson introduced it in 1985. Every event of the program has a virtual time, and every message carries a *virtual send time* and a larger *virtual receive time*. The system may run the events in any real order, on any number of processors, but the result must be the same as if each process had handled its messages in increasing order of virtual receive time. Simulation time in a [parallel discrete event simulation](/parallel-discrete-event-simulation/) is the main example; [Time Warp](/time-warp/) and the [Chandy-Misra-Bryant algorithm](/chandy-misra-bryant/) are two ways to keep the promise.

## In plain words

In a simulation of a bank, a customer arrives at 9:00, waits, and is served at 9:07. These times are part of the model, not of the computer. The computer may compute these events in any order and on any machine, if the answer is the one that the model gives.

Virtual time is this idea for any distributed program. The program puts a time on each message, and the time of a reply must be later than the time of the question. Each process then promises to act as if it read its mail in order of these times. Then the result is the same as on one computer that runs every event in order of time.

[Lamport clocks](/lamport-clocks/) go the other way. They are computed from the run, and they only report an order that already happened. Virtual time is given first, and the run must obey it.

## The idea

**Rules.** An event is the handling of one message by a process, together with the messages that the handling sends, so a message is sent at the virtual time of the event that sends it. Let $VT(e)$ be the virtual time of event $e$. A message $m$ is sent at virtual time $\mathit{send}(m)$ and received at virtual time $\mathit{recv}(m)$. The program must keep two rules:

1. $\mathit{send}(m) < \mathit{recv}(m)$ for every message;
2. the virtual times of the events of one process strictly increase, in the order in which the process runs them.

Rule 2 is what the system must enforce: each process handles its incoming messages in increasing order of receive time, and ties are broken by a fixed key such as the sender and a sequence number. In simulation this is the *local causality constraint*.

**Theorem 1 (virtual time is a Lamport clock).** If the two rules hold, then $e \to f$ implies $VT(e) < VT(f)$, where $\to$ is [happened-before](/happened-before/).

*Proof.* $\to$ is the transitive closure of two kinds of steps: two events of one process in order, and the send and the receive of one message. Rule 2 gives $VT(e) < VT(f)$ for a step of the first kind, and rule 1 for a step of the second, since the send event has time $\mathit{send}(m)$ and the receive event has time $\mathit{recv}(m)$. Strict order is transitive. $\square$

**Theorem 2 (the sequential meaning).** If the rules hold and the events have distinct keys $(VT(e), \text{tie key})$, then the sequential program that runs all events in order of key, one at a time, gives every process the same messages in the same order, and so the same states, as the distributed run.

*Proof.* Order the events by key. By Theorem 1, this order puts every send before its receive and keeps the order of each process, so it is an order of the events that respects $\to$, a run of the same computation. In it, each process runs the same events in the same order as before, by rule 2, and receives the same messages. A process is deterministic in its own events and messages, so it passes through the same states. $\square$

So the correctness of a distributed run is a local property: each process needs only to handle its own messages in the right order. The hard part is that a process does not know whether a message with a smaller receive time is still on the way. Two answers exist:

- **Conservative.** Wait until it is safe: run a message only when no message with a smaller receive time can still arrive. This needs bounds on future messages, as in the [Chandy-Misra-Bryant algorithm](/chandy-misra-bryant/).
- **Optimistic.** Run at once, and if a message with a smaller receive time, a *straggler*, arrives later, undo the work done after its time and cancel the messages that work sent. This is [Time Warp](/time-warp/).

**Global virtual time.** In the optimistic case, the [global virtual time](/global-virtual-time/) is the least virtual time of all work not yet done and all messages in transit. No rollback can go below it, so all work before it is final.

## Examples

**Two tellers.** In a simulation of a bank, process $A$ is the front desk and process $B$ is a teller. At virtual time 10, $A$ sends "customer 1 arrives" to $B$ with receive time 12, and at virtual time 11 it sends "customer 2 arrives" with receive time 14. The machine of $B$ is fast, and the message for time 14 arrives first. $B$ must not serve customer 2 first: a conservative $B$ waits until it knows that nothing below 14 can still come, and an optimistic $B$ serves customer 2, then gets the message for time 12, undoes the service of customer 2, and runs both in order.

**A broken rule.** If $B$ answers a message received at virtual time 12 with a message whose receive time is 12, rule 1 fails, and the sequential order of Theorem 2 is not defined: both events must come first. In simulation, this is a zero delay, and it is the case where conservative methods can deadlock and must use a tie key.

**Not the order in real time.** In the first example the real arrival order at $B$ was 14, then 12. Virtual time says that the meaning of the program is 12, then 14, whatever the network did.

## Where it is used

- **Parallel discrete event simulation.** Simulation time is virtual time. Both [Time Warp](/time-warp/) and [Chandy-Misra-Bryant](/chandy-misra-bryant/) enforce the local causality constraint.
- **The Time Warp Operating System.** Jefferson and his group built an operating system for simulations on this model at the Jet Propulsion Laboratory in the late 1980s.
- **Federated simulation.** The High Level Architecture standard, IEEE 1516, has time management services in which each federate asks for permission to advance its logical time.
- **Reasoning about order.** Theorem 1 shows that a virtual time is a valid [Lamport clock](/lamport-clocks/), so every result about Lamport clocks applies to it.

## References
