---
tag: DX6H2N
kind: definition
slug: concurrent-events
name: Concurrent events
aliases:
- causally concurrent events
area: distributed/clocks-and-ordering
level: intro
summary: Two distinct events neither of which happened before the other. The relation is symmetric but not transitive, and vector clocks detect it as incomparable timestamps.
prereqs: [happened-before]
see_also: [happened-before, vector-clocks, vector-clock-characterization, version-vectors, space-time-diagram, consistent-cut, weak-conjunctive-predicate-detection, plausible-clocks]
sources:
  - paper: doi:10.1145/359545.359563
    title: Leslie Lamport, Time, clocks, and the ordering of events in a distributed system, Communications of the ACM 21(7), 1978
    locator: pages 558 to 565, section The Partial Ordering (the definition of concurrent events)
  - paper: "Friedemann Mattern, Virtual time and global states of distributed systems, in M. Cosnard et al. (eds.), Parallel and Distributed Algorithms, North-Holland, 1989"
    title: Friedemann Mattern, Virtual time and global states of distributed systems, Parallel and Distributed Algorithms, North-Holland, 1989
    locator: pages 215 to 226 (concurrency and its test with vector time)
  - paper: doi:10.1007/BF02277859
    title: Reinhard Schwarz and Friedemann Mattern, Detecting causal relationships in distributed computations, in search of the holy grail, Distributed Computing 7(3), 1994
    locator: the sections on concurrency, causal histories and vector time
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 2 (logical and physical concurrency) and Chapter 3, Section 3.4 (vector time)
---

Two events of a distributed run are *concurrent* if neither [happened before](/happened-before/) the other. Then no chain of messages links them, so neither could have influenced the other. Concurrency says nothing about real time: concurrent events may happen at very different moments. The relation is symmetric but not transitive, which is why one counter per event cannot detect it and [vector clocks](/vector-clocks/) are needed.

## Definition

Let $\to$ be the happened-before relation on the events of a run. Two events $a$ and $b$ are *concurrent*, written $a \parallel b$, if $a \ne b$, $a \not\to b$ and $b \not\to a$.

So every pair of distinct events is in exactly one of three cases: $a \to b$, $b \to a$, or $a \parallel b$. Two events of the same process are never concurrent, because local order puts one before the other.

**Basic facts.**

1. $\parallel$ is symmetric and irreflexive. This follows from the definition.
2. $\parallel$ is not transitive. The example below has $a \parallel f$ and $f \parallel e$, but $a \to e$.
3. **Test with vector clocks.** With vector timestamps $V$, $a \parallel b$ if and only if $V(a)$ and $V(b)$ are incomparable: some entry of $V(a)$ is larger and some entry of $V(b)$ is larger. If $a$ is on process $P_i$ and $b$ on $P_j$, it is enough to check the two entries $V(a)[i] > V(b)[i]$ and $V(b)[j] > V(a)[j]$. Both claims follow from the [vector clock characterization](/vector-clock-characterization/).
4. **Concurrent events fit on one cut.** Let $e_1, \ldots, e_k$ be pairwise concurrent events on distinct processes. Then the union $S$ of their causal histories is a [consistent cut](/consistent-cut/), and on the process of each $e_i$, the last event in $S$ is $e_i$.

*Proof of fact 4.* A union of sets closed downward under $\to$ is closed downward, so $S$ is consistent. Let $f$ be an event on the process of $e_i$ that comes after $e_i$. If $f$ were in $S$, then $f \to e_j$ or $f = e_j$ for some $j$. Since $e_i \to f$, this would give $e_i \to e_j$ for some $j \ne i$, against the assumption, or $f = e_j$ on the process of $e_i$, which is impossible because the events are on distinct processes. $\square$

Fact 4 is the reason why detecting a conjunction of local predicates, as in [weak conjunctive predicate detection](/weak-conjunctive-predicate-detection/), searches for pairwise concurrent events.

## Examples and non-examples

The running example of this area has vector timestamps:

| event | process | what it does | vector |
|---|---|---|---|
| $a$ | $P_1$ | send to $P_2$ | $(1,0,0)$ |
| $b$ | $P_1$ | local | $(2,0,0)$ |
| $c$ | $P_2$ | local | $(0,1,0)$ |
| $d$ | $P_2$ | receive from $a$ | $(1,2,0)$ |
| $e$ | $P_2$ | send to $P_3$ | $(1,3,0)$ |
| $f$ | $P_3$ | local | $(0,0,1)$ |
| $g$ | $P_3$ | receive from $e$ | $(1,3,2)$ |

**Examples.** The concurrent pairs are $a \parallel c$, $a \parallel f$, $b \parallel c$, $b \parallel d$, $b \parallel e$, $b \parallel f$, $b \parallel g$, $c \parallel f$, $d \parallel f$ and $e \parallel f$: 10 of the 21 pairs. For $b$ and $e$, the two-entry test gives $V(b)[1] = 2 > 1 = V(e)[1]$ and $V(e)[2] = 3 > 0 = V(b)[2]$. The event $b$ is concurrent with every event outside $P_1$, because no message leaves $P_1$ after it, and none enters $P_1$.

**Not transitive.** $a \parallel f$ and $f \parallel e$, but $a \to e$. A relation that is not transitive is not an equivalence, so events cannot be grouped into classes of mutually concurrent events.

**Non-examples.**

- $c$ and $d$ are on one process, so $c \to d$. They are never concurrent.
- $f$ and $g$ are not concurrent: $f \to g$ by local order, even though the message into $g$ came from elsewhere.
- Lamport timestamps do not detect concurrency. In the example, $C(b) = 2 < 3 = C(e)$, but $b \parallel e$. A scalar clock maps a partial order into a total one, so it must order some concurrent pairs.

## Related definitions

- **[Happened-before](/happened-before/).** Concurrency is the absence of $\to$ in both directions.
- **[Vector clock characterization](/vector-clock-characterization/).** Gives the exact test of concurrency from vector timestamps, and Charron-Bost's result that no vector with fewer than $n$ entries can always give it.
- **[Version vectors](/version-vectors/).** In replicated data, two updates are in conflict when their version vectors are concurrent.
- **[Plausible clocks](/plausible-clocks/).** Constant-size clocks that never reverse a causal pair, but may report some concurrent pairs as ordered.
- **Physical simultaneity.** Concurrent events need not be close in real time, and events that are close in real time need not be concurrent: a receive and the next send on the same process can happen within a microsecond and are still ordered.
- **Concurrent operations on shared objects.** In shared memory models, two operations are concurrent when their time intervals overlap. That is a real-time notion, and it is different from the causal notion of this page.

## References
