---
tag: D9N3VE
kind: concept
slug: total-order
name: Total order of events
aliases:
- Lamport total order
- total ordering of events
area: distributed/clocks-and-ordering
level: intro
summary: An order of all events of a run that extends happened-before. Lamport's version sorts by clock value and breaks ties by process id, so every process can compute the same order.
prereqs: [lamport-clocks, happened-before]
see_also: [lamport-clocks, lamport-clock-condition, happened-before, total-order-broadcast, topological-sort, mutual-exclusion-problem, replicated-state-machine, last-writer-wins]
sources:
  - paper: doi:10.1145/359545.359563
    title: Leslie Lamport, Time, clocks, and the ordering of events in a distributed system, Communications of the ACM 21(7), 1978
    locator: pages 558 to 565, section Ordering the Events Totally (the relation ⇒ and the mutual exclusion algorithm) and the discussion of anomalous behavior
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 6, Section 6.1 (logical timestamps and their total order)
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 3 (scalar time and the total order it gives)
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 9, Ordering Guarantees (Lamport timestamps, and why they are not enough for uniqueness constraints)
---

A total order of events puts all events of a distributed run in one sequence that respects [happened-before](/happened-before/): if $a \to b$, then $a$ comes first. Happened-before leaves [concurrent](/concurrent-events/) events unordered, so many such sequences exist, and the processes need a rule to agree on one. Lamport's rule sorts events by their [Lamport clock](/lamport-clocks/) value and breaks ties by process id. Each process can compute it from timestamps alone, with no extra messages.

## In plain words

Happened-before is a partial order. It says which events came first only when one could have influenced the other. For a shared queue, a lock, or a log of commands, we need a single line.

Lamport's trick is simple. Each event already has a counter value from a Lamport clock. Sort the events by that value. When two events have the same value, they cannot be related, so pick an order that everyone agrees on: the event of the process with the smaller number goes first.

The result is one line that respects cause and effect. The order among unrelated events is arbitrary but fixed, so all computers that see the same timestamps build the same line.

## The idea

**Definition.** Let $C$ be a clock that satisfies [Lamport's clock condition](/lamport-clock-condition/), and number the processes $1$ to $n$. For an event $a$ of process $P_i$ and an event $b$ of process $P_j$, define
$$a \Rightarrow b \iff C(a) < C(b) \text{ or } (C(a) = C(b) \text{ and } i < j).$$

**Proposition.** $\Rightarrow$ is a strict total order on the events, and it extends $\to$.

*Proof.* The relation compares the pairs $(C(e), \text{process of } e)$ lexicographically, and the lexicographic order on pairs is a strict total order. Two distinct events have distinct pairs: on the same process, condition C1 gives them different clock values. So $\Rightarrow$ is a strict total order on events. If $a \to b$, then $C(a) < C(b)$ by the clock condition, so $a \Rightarrow b$. $\square$

**One extension among many.** Any linear extension $L$ of $\to$ comes from some clock: give each event its position in $L$. So the clock condition alone allows every one of them, and the choice of $\Rightarrow$ is a convention. Lamport clocks with the process id tie-break choose one particular extension, and they can be computed online.

**What the order does not say.**

- $a \Rightarrow b$ does not imply $a \to b$. The order of concurrent events is arbitrary.
- The order need not match real time. Lamport described this *anomalous behavior*: a person issues request $a$, then calls a friend by telephone, who issues request $b$. The system cannot see the call, so $b$ may get a smaller timestamp and come first. His fix was a stronger condition with physical clocks.
- An event cannot know its final position when it happens. To know that no event with a smaller timestamp will arrive later, a process must hear from every other process, which is why Lamport's mutual exclusion assumes FIFO channels and waits for a message from each process.

**Total order versus total order broadcast.** This page is about ordering events that already happened. [Total order broadcast](/total-order-broadcast/) is a fault-tolerant service that makes all correct processes deliver the same messages in the same order. Lamport timestamps can implement it when no process fails and channels are FIFO, by delivering a message once every process has sent something with a larger timestamp. With crashes, one silent process blocks this rule forever, and total order broadcast then needs consensus.

## Examples

The running example has events $a$, $b$ on $P_1$; $c$, $d$, $e$ on $P_2$; and $f$, $g$ on $P_3$, with messages $a \to d$ and $e \to g$.

| event | $a$ | $c$ | $f$ | $b$ | $d$ | $e$ | $g$ |
|---|---|---|---|---|---|---|---|
| Lamport value | 1 | 1 | 1 | 2 | 2 | 3 | 4 |
| process | 1 | 2 | 3 | 1 | 2 | 2 | 3 |

So the total order is $a \Rightarrow c \Rightarrow f \Rightarrow b \Rightarrow d \Rightarrow e \Rightarrow g$. A script that enumerates all permutations finds 52 orders of these seven events that extend $\to$, and this is one of them. The pair $b$ and $e$ is concurrent, and the order puts $b$ first only because $2 < 3$.

**A different tie-break.** Ordering processes as $P_3 < P_2 < P_1$ gives $f, c, a, d, b, e, g$. This is also a valid extension of $\to$, which shows that the choice is a convention.

**A wrong tie-break.** Breaking ties by the arrival time at some observer does not give the same order at all observers, so it is not a usable rule.

## Where it is used

- **[Mutual exclusion](/mutual-exclusion-problem/).** In Lamport's 1978 algorithm, every process keeps a queue of requests sorted by $\Rightarrow$ and enters the critical section when its request is first and it has heard a later message from every process.
- **[Bakery algorithm](/lamport-bakery-algorithm/).** Lamport's shared-memory mutual exclusion uses the same rule: a customer with ticket number $t$ and id $i$ goes before one with $(t', j)$ if $(t, i)$ is lexicographically smaller.
- **[Replicated state machines](/replicated-state-machine/).** Lamport presented the total order as a way to make all processes apply commands in the same order. Modern systems use consensus for this, because they must tolerate failures.
- **[Last-writer-wins](/last-writer-wins/).** Replicas order concurrent writes by (timestamp, replica id) and keep the largest, which is this total order applied to writes.
- **Unique ids.** A pair (Lamport value, process id) is unique across the system, so it can name events, transactions or list elements in collaborative editors.
- **Ordering a graph.** Outside distributed computing, a [topological sort](/topological-sort/) computes a linear extension of a known DAG. The Lamport order computes one online, without anyone seeing the whole graph.

## References
