---
tag: F6ZVRW
kind: data-structure
slug: hybrid-logical-clocks
name: Hybrid logical clocks
aliases:
- HLC
area: distributed/clocks-and-ordering
level: advanced
summary: A pair (l, c) per event. l is the largest physical time heard of and c breaks ties, so happened-before gives a smaller pair and l stays within the clock skew of physical time.
model: asynchronous-model
complexity:
  vars: {n: the number of processes}
  time: {worst: O(1)}
  space: {extra: O(1)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2014
  people: [Sandeep S. Kulkarni, Murat Demirbas, Deepak Madappa, Bharadwaj Avva, Marcelo Leone]
  note: Kulkarni, Demirbas, Madappa, Avva and Leone presented hybrid logical clocks at OPODIS 2014.
prereqs: [lamport-clocks, clock-skew]
see_also: [lamport-clocks, truetime, clock-synchronization, ntp, consistent-cut, external-consistency, last-writer-wins, monotonic-clock]
sources:
  - paper: doi:10.1007/978-3-319-14472-6_2
    title: Sandeep S. Kulkarni, Murat Demirbas, Deepak Madappa, Bharadwaj Avva and Marcelo Leone, Logical physical clocks, OPODIS 2014, LNCS 8878
    locator: the naive algorithm and its unbounded drift (Figures 3 and 4), the HLC algorithm, Theorem 1 and Corollaries 1 to 4
  - paper: doi:10.1145/3299869.3314049
    title: Misha Tyulenev, Andy Schwerin, Asya Kamsky, Randolph Tan, Alyson Cabral and Jack Mulrow, Implementation of cluster-wide logical clock and causal consistency in MongoDB, SIGMOD 2019
    locator: the cluster time, a hybrid logical clock
  - paper: doi:10.1145/3318464.3386134
    title: Rebecca Taft and others, CockroachDB, the resilient geo-distributed SQL database, SIGMOD 2020
    locator: the section on transaction timestamps from hybrid logical clocks
---

A hybrid logical clock (HLC) gives each event a timestamp $(l, c)$. The part $l$ is the largest physical clock reading that the process has heard of, directly or through messages, and $c$ is a small counter that breaks ties between events with the same $l$. Like a [Lamport clock](/lamport-clocks/), it gives a smaller timestamp to an event that happened before another. Unlike a Lamport clock, $l$ never moves more than the [clock skew](/clock-skew/) $\varepsilon$ ahead of the physical clock, so a timestamp can stand in for wall-clock time. Sandeep Kulkarni, Murat Demirbas and their coauthors described HLC in 2014.

## In plain words

Each server has a wall clock, and the wall clocks are close but not equal. A Lamport counter respects cause and effect but says nothing about real time. A wall clock says roughly when something happened, but a message can arrive at a server whose clock is behind the clock of the sender, so the effect looks older than its cause.

A hybrid clock keeps the larger of two things: its own wall clock, and the latest time it has seen on a message. When these two are equal, a small counter separates the events. So effects always get later stamps than their causes, and the stamp is never far ahead of the wall clock, because every value in it came from some real clock that was close to this one.

## The abstract type

The model is the [asynchronous model](/asynchronous-model/) with $n$ processes. Each process can read a physical clock $pt$ that never goes back, and any two clocks differ by at most $\varepsilon$ at the same real time. Each process has a clock with these operations:

- SEND-OR-LOCAL$(pt)$: stamp a local or send event, and return the stamp to put on the message.
- RECEIVE$(l_m, c_m, pt)$: stamp the receipt of a message that carries $(l_m, c_m)$.

Stamps are compared lexicographically: first by $l$, then by $c$. The specification has three parts:

1. If $e$ [happened before](/happened-before/) $f$, then $(l.e, c.e) < (l.f, c.f)$.
2. $0 \le l.f - pt.f \le \varepsilon$ at every event $f$.
3. $c$ stays bounded, so that a stamp fits in a fixed number of bits.

## Representation

Each process keeps two integers, $l$ and $c$, both $0$ at the start. A stamp is the pair, and it is the same size as one physical timestamp plus a small counter. Systems often pack it into one 64-bit word, with $l$ in the high bits and $c$ in the low bits, so that integer order is the lexicographic order.

## Operations

```pseudo id=main
init
L1  l ← 0;  c ← 0

SEND-OR-LOCAL(pt)
L2  l' ← l
L3  l ← max(l', pt)
L4  if l = l' then c ← c + 1 else c ← 0;  return (l, c)

RECEIVE(l_m, c_m, pt)
L5  l' ← l;  l ← max(l', l_m, pt)
L6  if l = l' = l_m then c ← max(c, c_m) + 1
L7  else if l = l' then c ← c + 1
L8  else if l = l_m then c ← c_m + 1
L9  else c ← 0
    return (l, c)
```

The counter restarts at $0$ whenever the physical clock is ahead of everything that the process has seen. It grows only while the process is held at a value of $l$ that came from a faster clock.

## Example

Process $P_1$ runs slow, $P_2$ runs fast, and $P_3$ is in between.

| event | process | $pt$ | rule | $(l, c)$ |
|---|---|---|---|---|
| send $m$ to $P_1$ | $P_2$ | 10 | L3, L4 | $(10, 0)$ |
| local | $P_1$ | 7 | L3, L4 | $(7, 0)$ |
| receive $m$ | $P_1$ | 8 | L8 | $(10, 1)$ |
| send $m'$ to $P_3$ | $P_1$ | 9 | L4 | $(10, 2)$ |
| receive $m'$ | $P_3$ | 9 | L8 | $(10, 3)$ |
| local | $P_1$ | 11 | L4 | $(11, 0)$ |

The message from the fast $P_2$ pulls $l$ at $P_1$ up to $10$. Until the physical clock of $P_1$ passes $10$, its events keep $l = 10$ and count with $c$. At $pt = 11$ the physical clock wins and $c$ restarts. Each stamp is larger than the stamps of its causes, and $l - pt$ is at most $2$ here, at the receipt of $m$. This is within the skew of $3$ between $P_2$ and $P_1$.

## Correctness

Every rule takes $l$ as a maximum that includes the $l$ of each direct predecessor, so $l$ never decreases along a causal chain. When $l$ stays the same, the rules set $c$ to $1$ more than the counter of the predecessor that has the same $l$. So each direct step strictly increases the pair, and by transitivity every causal chain does. For closeness, each $l$ is the physical reading $pt.g$ of some event $g$ in the causal past, and $g$ happened no later in real time. So $pt.g$ is at most $\varepsilon$ above the current reading. For the counter, $c.f$ is at most the number of causal predecessors that share $l.f$. Those events read a physical value between $l.f - \varepsilon$ and $l.f$, so if each process reads a new value at each event, there are at most $n(\varepsilon + 1)$ of them. The full proof is below.

## Complexity

Each operation does a constant number of comparisons and additions, so it takes $O(1)$ time. The state and each stamp take $O(1)$ words. The counter is at most $n(\varepsilon + 1)$ when clock readings advance at each event. In practice $c$ stays small, because it is reset whenever the local clock moves past the largest $l$ seen.

## Variants

- **[Lamport clocks](/lamport-clocks/).** The special case without physical clocks. They also satisfy the clock condition, but their values drift away from real time without bound.
- **The naive hybrid.** The OPODIS paper first shows a simpler algorithm that keeps only $l$. Its $l$ can drift away from physical time without bound, and the separate counter $c$ fixes that.
- **[TrueTime](/truetime/).** Spanner's clock gives an interval of real time with a guaranteed error bound, and it waits out the uncertainty to give [external consistency](/external-consistency/). HLC gives no such bound by itself, but it needs no special hardware.

## When to use it

Use HLC when a system needs timestamps that respect causality and also mean something to people: multi-version databases that read at a timestamp, [consistent snapshots](/consistent-cut/) taken "at time $t$", and [last-writer-wins](/last-writer-wins/) registers where the winner should be the causally later write. MongoDB uses a hybrid logical clock for its cluster time, and CockroachDB uses one for transaction timestamps. If only causality matters, a [Lamport clock](/lamport-clocks/) is simpler. If concurrent events must be detected, use [vector clocks](/vector-clocks/).

## Pitfalls

- **A clock that jumps ahead.** If one process has a clock far in the future, its messages pull every $l$ forward, and the closeness bound no longer holds, because the skew assumption failed. A system can reject or log a message whose $l$ is more than a configured maximum offset ahead of the local clock.
- **HLC order is not concurrency detection.** Two concurrent events still get ordered stamps. A smaller stamp does not prove that one event caused the other.
- **Clocks that go back.** The rules assume the physical clock never goes back. A [monotonic clock](/monotonic-clock/) or a clamp on the reading is needed.
- **Overflow of $c$.** With a coarse clock, many events can share one reading, and $c$ grows with them. A packed format must leave enough bits for the counter.

## Implementations

## History

Sandeep S. Kulkarni, Murat Demirbas, Deepak Madappa, Bharadwaj Avva and Marcelo Leone presented hybrid logical clocks at OPODIS 2014 in the paper "Logical physical clocks". They compared it with the TrueTime clock of Spanner, which needs special hardware. The paper also showed that a simpler algorithm with only $l$ drifts without bound. CockroachDB and MongoDB later built their timestamps on HLC.

## References
