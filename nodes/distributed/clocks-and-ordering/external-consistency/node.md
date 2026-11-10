---
tag: A68QW9
kind: definition
slug: external-consistency
name: External consistency
aliases:
- strict serializability
- strong serializability
area: distributed/clocks-and-ordering
level: advanced
summary: A history of transactions is externally consistent if some serial order explains it and that order puts T1 before T2 whenever T1 commits before T2 starts in real time.
prereqs: [linearizability, serializability]
see_also: [truetime, serializability, linearizability, snapshot-isolation, sequential-consistency, consistency-models, two-phase-locking, happened-before]
sources:
  - paper: "David K. Gifford, Information storage in a decentralized computer system, PhD thesis, Stanford University, 1981"
    title: David K. Gifford, Information storage in a decentralized computer system, PhD thesis, Stanford University, 1981; also Xerox PARC report CSL-81-8
    locator: the definition of external consistency for transactions (year of the report to be checked, cited by Spanner as 1982)
  - paper: doi:10.1145/322154.322158
    title: Christos H. Papadimitriou, The serializability of concurrent database updates, Journal of the ACM 26(4), 1979
    locator: pages 631 to 653, the definition of strict serializability (DOI from memory, to be checked)
  - paper: doi:10.1145/78969.78972
    title: Maurice P. Herlihy and Jeannette M. Wing, Linearizability, a correctness condition for concurrent objects, ACM Transactions on Programming Languages and Systems 12(3), 1990
    locator: pages 463 to 492, the relation of linearizability to strict serializability (DOI from memory, to be checked)
  - url: https://www.usenix.org/conference/osdi12/technical-sessions/presentation/corbett
    title: James C. Corbett, Jeffrey Dean, Michael Epstein and others, Spanner, Google's globally-distributed database, OSDI 2012
    locator: Section 4 (external consistency, "or equivalently, linearizability"), Section 4.1.2 (the proof for read-write transactions)
---

*External consistency* is a correctness condition for transactions: the system must behave as if the transactions ran one at a time, in an order that agrees with real time. If $T_1$ commits before $T_2$ starts, then $T_2$ must see the effects of $T_1$. David Gifford gave the name in 1981; the same condition is called *strict serializability* (Papadimitriou 1979), and it is [linearizability](/linearizability/) with whole transactions as the operations.

## Definition

**Histories.** A *history* $H$ is a set of committed transactions. Each transaction $T$ has a start time $\mathrm{st}(T)$ and a commit time $\mathrm{ct}(T)$ in real time, with $\mathrm{st}(T) < \mathrm{ct}(T)$, and a set of reads with the values that they returned. The *real-time order* is $T_1 <_{\mathrm{rt}} T_2$ if and only if $\mathrm{ct}(T_1) < \mathrm{st}(T_2)$. A *serial order* is a total order $<_S$ of the transactions; it *explains* $H$ if every read returns the value of the last write to the same item before it in $<_S$ (or the read's own transaction), as in [serializability](/serializability/).

**External consistency.** $H$ is *externally consistent* if there is a serial order $<_S$ that explains $H$ and extends the real-time order:
$$T_1 <_{\mathrm{rt}} T_2 \implies T_1 <_S T_2.$$

**In timestamp form.** A system that gives each transaction a commit timestamp $s(T)$, and makes reads at timestamp $s$ see exactly the writes with smaller timestamps, is externally consistent if $\mathrm{ct}(T_1) < \mathrm{st}(T_2)$ implies $s(T_1) < s(T_2)$. Then the order of the timestamps is the serial order. This is the form that Spanner proves with [TrueTime](/truetime/).

**Lemma 1.** The real-time order $<_{\mathrm{rt}}$ is a strict partial order.

*Proof.* It is irreflexive, since $\mathrm{ct}(T) < \mathrm{st}(T)$ is false. It is transitive: if $\mathrm{ct}(T_1) < \mathrm{st}(T_2)$ and $\mathrm{ct}(T_2) < \mathrm{st}(T_3)$, then $\mathrm{ct}(T_1) < \mathrm{st}(T_2) < \mathrm{ct}(T_2) < \mathrm{st}(T_3)$. $\square$

So the definition asks for a linear extension of a partial order that also explains the reads. Two transactions that overlap in time are not ordered by $<_{\mathrm{rt}}$, and the serial order may put them either way.

## Examples and non-examples

- **A serial system.** A database on one machine that runs one transaction at a time is externally consistent: the order of execution is a serial order, and it extends real time.
- **Two-phase locking on one node.** With strict [two-phase locking](/two-phase-locking/), order the transactions by the time they reach their lock point. If $T_1$ commits before $T_2$ starts, $T_1$ reached its lock point first, so this order extends real time. So strict 2PL is externally consistent.
- **A stale read (non-example).** Item $x$ is 0. $T_1$ writes $x = 1$ and commits at time 1. $T_2$ starts at time 2 and reads $x = 0$ from a replica that lags. The serial order $T_2, T_1$ explains the history, so it is serializable. But $T_1 <_{\mathrm{rt}} T_2$ forces $T_1$ first, and then $T_2$ would have to read 1. So the history is not externally consistent.
- **Timestamps without commit wait (non-example).** On the [TrueTime](/truetime/) page, $T_1$ commits at real time 0.001 with $s_1 = 0.014$, and $T_2$ starts at 0.003 with $s_2 = 0.003$. The timestamp order puts $T_2$ first, against the real-time order.
- **Write skew under snapshot isolation (non-example).** Two transactions read $x$ and $y$, and each writes the item that the other did not write. Under [snapshot isolation](/snapshot-isolation/) both commit, and no serial order explains the history at all. So it is neither serializable nor externally consistent.

## Related definitions

- **Serializability.** Drop the real-time condition: some serial order explains $H$. Every externally consistent history is serializable, but the stale read above shows that the converse is false.
- **Linearizability.** Herlihy and Wing (1990) define [linearizability](/linearizability/) for single operations on shared objects: each operation takes effect at one point between its call and its return. If the whole database is one object and each transaction is one operation, linearizability is exactly external consistency. Herlihy and Wing note that strict serializability is this condition for transactions. Linearizability is also *local*: a history is linearizable if each object's part is. External consistency is not local in this sense, since a transaction touches many items at once.
- **Sequential consistency.** [Sequential consistency](/sequential-consistency/) keeps the order of each process but not real time between processes, so it is weaker than linearizability. The map of [consistency models](/consistency-models/) places all of these conditions.
- **TrueTime.** [TrueTime](/truetime/) is not a consistency condition but a clock API, and commit wait is a mechanism that gives external consistency. The two pages are a pair: this page says what must hold, the TrueTime page says how Spanner makes it hold.
- **Causal order.** The [happened-before](/happened-before/) relation orders events by messages, not by real time. Two transactions on machines that never talk can be in real-time order but not causally related; external consistency still orders them.

## References
