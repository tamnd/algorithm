---
tag: T872QV
kind: definition
slug: happened-before
name: Happened-before relation
aliases:
- Lamport's happened-before
- causal precedence
area: distributed/clocks-and-ordering
level: intro
summary: 'The smallest transitive relation on the events of a run that contains program order and send-before-receive. It is a strict partial order: the order of potential cause and effect.'
prereqs: [asynchronous-model, space-time-diagram]
see_also: [concurrent-events, space-time-diagram, lamport-clocks, vector-clocks, vector-clock-characterization, causal-ordering, consistent-cut, transitive-closure]
sources:
  - paper: doi:10.1145/359545.359563
    title: Leslie Lamport, Time, clocks, and the ordering of events in a distributed system, Communications of the ACM 21(7), 1978
    locator: pages 558 to 565, section The Partial Ordering (the definition of the relation and of concurrency)
  - paper: doi:10.1007/BF02277859
    title: Reinhard Schwarz and Friedemann Mattern, Detecting causal relationships in distributed computations, in search of the holy grail, Distributed Computing 7(3), 1994
    locator: the sections on causality and causal histories
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 6, Section 6.1 (the happens-before relation)
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 2 (the causal precedence relation)
---

The happened-before relation orders the events of a distributed run by potential cause and effect. Leslie Lamport defined it in 1978: an event happened before another if they are on the same process in that order, or if one sends a message that the other receives, or if a chain of such steps links them. It does not use real time at all. It is a strict partial order, so some pairs of events are not ordered; these are the [concurrent events](/concurrent-events/).

## Definition

**Model.** A run of a system of processes $P_1, \ldots, P_n$ in the [asynchronous model](/asynchronous-model/) consists of events. Each event belongs to one process, and the events of a process are totally ordered by its local history. An event is a local step, a send of a message or a receive of a message, and each receive matches exactly one send. In every run, a receive happens after its send in real time.

**Definition.** The *happened-before* relation $\to$ on the events of a run is the smallest relation such that:

1. if $a$ and $b$ are events of the same process and $a$ comes before $b$, then $a \to b$;
2. if $a$ sends a message and $b$ receives that message, then $a \to b$;
3. if $a \to b$ and $b \to c$, then $a \to c$.

So $\to$ is the [transitive closure](/transitive-closure/) of the union of program order and the send-receive pairs. In the [space-time diagram](/space-time-diagram/) of the run, $a \to b$ means that a directed path leads from $a$ to $b$.

The *causal history* of an event $e$ is $C(e) = \{f : f \to e\} \cup \{e\}$, the event together with everything that could have influenced it.

**Proposition 1.** The relation $\to$ is a strict partial order: it is irreflexive ($a \not\to a$), transitive, and hence asymmetric ($a \to b$ implies $b \not\to a$).

*Proof.* Transitivity is rule 3. For irreflexivity, write $t(e)$ for the real time of an event $e$, with ties between processes broken in any fixed way, and ties within a process broken by local order. Each pair given by rules 1 and 2 has $t(a) < t(b)$: a process does its events one after another, and a receive comes after its send. Rule 3 keeps the strict inequality, so $a \to b$ implies $t(a) < t(b)$. Then $a \to a$ would give $t(a) < t(a)$, which is false. If $a \to b$ and $b \to a$, transitivity would give $a \to a$, so the relation is asymmetric. $\square$

**Proposition 2 (causal histories).** For events $e \ne f$, $e \to f$ if and only if $C(e) \subsetneq C(f)$.

*Proof.* If $e \to f$, then every $g \to e$ also has $g \to f$ by transitivity, and $e \in C(f)$, so $C(e) \subseteq C(f)$. The event $f$ is in $C(f)$ but not in $C(e)$, because $f \to e$ would contradict asymmetry and $f \ne e$. So the inclusion is strict. Conversely, if $C(e) \subsetneq C(f)$, then $e \in C(f)$ and $e \ne f$, so $e \to f$. $\square$

[Vector clocks](/vector-clocks/) encode $C(e)$ by counting its events at each process, which is why they capture $\to$ exactly.

## Examples and non-examples

In the running example of this area:

- $P_1$: $a$ sends to $P_2$, then $b$ is local.
- $P_2$: $c$ is local, $d$ receives from $a$, $e$ sends to $P_3$.
- $P_3$: $f$ is local, $g$ receives from $e$.

**Examples.** $a \to b$ by rule 1, $a \to d$ by rule 2, and $a \to g$ by rule 3 along $a \to d \to e \to g$. In total, 11 of the 21 pairs of events are ordered. The causal history of $g$ is $C(g) = \{a, c, d, e, f, g\}$, which misses only $b$.

**Non-examples.**

- $b$ and $e$ are not ordered: no message leaves $P_1$ after $b$, and no message enters $P_1$ at all. They are concurrent, written $b \parallel e$, even if $b$ happened earlier in real time.
- Real time order does not imply $\to$. If $f$ happened at noon and $c$ at one o'clock, still $f \not\to c$, because no message links them.
- $a \to d$ does not mean that $a$ *caused* $d$ in the sense of the program logic. The relation records only that information could have flowed from $a$ to $d$. Lamport calls it the order in which events *could* have affected each other.
- Two events of one process are always ordered. Concurrency only arises between processes.

## Related definitions

- **[Concurrent events](/concurrent-events/).** $a \parallel b$ if neither $a \to b$ nor $b \to a$. Unlike $\to$, this relation is not transitive.
- **[Lamport's clock condition](/lamport-clock-condition/).** A clock $C$ satisfies it if $a \to b$ implies $C(a) < C(b)$. [Lamport clocks](/lamport-clocks/) meet it.
- **[Vector clock characterization](/vector-clock-characterization/).** With vector clocks, $a \to b$ holds if and only if $V(a) < V(b)$, so the relation can be tested from timestamps.
- **[Total order](/total-order/).** Any linear extension of $\to$, such as the order of Lamport timestamps with process ids as tie-breakers.
- **[Causal ordering](/causal-ordering/).** A delivery rule for messages: if the send of $m$ happened before the send of $m'$, deliver $m$ first.
- **[Consistent cut](/consistent-cut/).** A set of events closed downward under $\to$, which is a state the system could have passed through.

## References
