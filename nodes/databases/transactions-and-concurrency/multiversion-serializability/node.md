---
tag: 7MFAKN
kind: definition
slug: multiversion-serializability
name: Multiversion serializability
aliases:
- multiversion serialization graph
- MVSR
- one-copy serializability of multiversion schedules
area: databases/transactions-and-concurrency
level: advanced
summary: "A multiversion schedule is serializable when its reads-from relation is that of a serial run on one copy of each item. A version order with an acyclic MVSG proves it."
prereqs: [view-serializability, multiversion-concurrency-control]
see_also: [one-copy-serializability, conflict-serializability, snapshot-isolation, adya-isolation-levels, timestamp-ordering, view-serializability-np-completeness, serializability-theorem, snapshot-isolation-dangerous-structure]
sources:
  - paper: doi:10.1145/319996.319998
    title: "Philip A. Bernstein and Nathan Goodman, Multiversion concurrency control, theory and algorithms, ACM Transactions on Database Systems 8(4), 1983, pages 465 to 483"
    locator: "the definitions of multiversion histories and one-copy serializability, and the multiversion serialization graph theorem"
  - paper: doi:10.1145/348.318588
    title: "Christos H. Papadimitriou and Paris C. Kanellakis, On concurrency control by multiple versions, ACM Transactions on Database Systems 9(1), 1984, pages 89 to 99"
    locator: "the NP-completeness of testing multiversion serializability, chapter level only"
  - book: isbn:9780201107159
    title: "Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987"
    locator: "Chapter 5, Multiversion Concurrency Control (multiversion histories, one-copy serializability and the MVSG theorem)"
  - book: isbn:9781558605084
    title: "Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001"
    locator: "Chapter 5, Multiversion Concurrency Control (the classes MVSR and MCSR, VSR inside MVSR, and the NP-completeness of MVSR)"
---

A *multiversion schedule* lets a read return an older version of an item, as [multiversion concurrency control](/multiversion-concurrency-control/) does. *Multiversion serializability* (MVSR) says when such a schedule is correct: it must look, to every transaction, like a serial run on a database with one copy of each item. The notion uses the reads-from relation, as [view serializability](/view-serializability/) does, and not the order of conflicting steps of [conflict serializability](/conflict-serializability/), because writes of the same item no longer overwrite each other. Bernstein and Goodman (1983) called it *one-copy serializability*, the name also used for replicated data on the [one-copy serializability](/one-copy-serializability/) page. The *multiversion serialization graph* (MVSG) is the tool to prove it: a schedule is MVSR if and only if some order of the versions of each item makes this graph acyclic. Testing MVSR is NP-complete, so schedulers such as multiversion [timestamp ordering](/timestamp-ordering/) and [snapshot isolation](/snapshot-isolation/) fix the version order in advance.

## Definition

**Versions.** Each write $w_i(x)$ of transaction $T_i$ makes a new version $x_i$. An initial transaction $T_0$ writes the version $x_0$ of every item before the schedule starts. A *multiversion schedule* $m$ is a schedule of steps $r_i(x_j)$ and $w_i(x_i)$, together with commits and aborts, in which each read $r_i(x_j)$ comes after $w_j(x_j)$, and a transaction that has written $x$ reads its own version $x_i$. The map from each read to the version it returns is the *version function*. A *monoversion* schedule is one where each read returns the version of the last write of the item before it; this is an ordinary schedule.

**Reads-from.** $T_i$ *reads $x$ from* $T_j$ in $m$ if $m$ contains $r_i(x_j)$. Two multiversion schedules on the same transactions are *view equivalent* if they have the same steps and the same reads-from relation. There is no condition on final writes, because every version stays available.

**MVSR.** A multiversion schedule $m$ is *multiversion serializable* if its committed projection is view equivalent to a serial monoversion schedule of the same committed transactions. In the serial monoversion schedule each read returns the last version written before it in the serial order.

**Version order and MVSG.** A *version order* $\ll$ is, for each item $x$, a total order on the committed versions of $x$ with $x_0$ first. For a schedule $m$ and a version order $\ll$, the graph $MVSG(m, \ll)$ has a node for each committed transaction, including $T_0$, and these arcs:

1. $T_j \to T_i$ whenever $T_i$ reads $x$ from $T_j$, $i \ne j$ (the reads-from arcs);
2. for each read $r_k(x_j)$ and each write $w_i(x_i)$ with $i$, $j$, $k$ distinct: $T_i \to T_j$ if $x_i \ll x_j$, and $T_k \to T_i$ if $x_j \ll x_i$ (the version order arcs).

**MVSG theorem** (Bernstein and Goodman, 1983). A multiversion schedule is MVSR if and only if there is a version order $\ll$ such that $MVSG(m, \ll)$ is acyclic. A serial order is then any topological sort of the graph.

The version order arcs say that a writer $T_i$ of $x$ goes either before the writer $T_j$ of the version that $T_k$ read, or after the reader $T_k$; it cannot fall between them, since then $T_k$ would read $x_i$ in the serial run.

**Multiversion conflicts.** A simpler, conflict-based class MCSR counts only the pair "$r_i(x_j)$ before $w_k(x_k)$" as a conflict. Weikum and Vossen show that MCSR is strictly contained in MVSR, and that MCSR can be tested in polynomial time.

## Examples and non-examples

**An old version repairs a schedule.** $T_1$ reads $x$ and $y$; $T_2$ writes both.

$$m = r_1(x_0)\, w_2(x_2)\, w_2(y_2)\, c_2\, r_1(y_0)\, c_1.$$

As a monoversion schedule, $r_1(y)$ would read $y_2$, $T_1$ would come before $T_2$ on $x$ and after it on $y$, and the schedule would not be serializable. With the old version $y_0$, $T_1$ reads both items from $T_0$, which is the serial schedule $T_0\, T_1\, T_2$. With $x_0 \ll x_2$ and $y_0 \ll y_2$, the MVSG has the reads-from arc $T_0 \to T_1$ and the version order arc $T_1 \to T_2$ (from $r_1(x_0)$ and $w_2(x_2)$, and again from $r_1(y_0)$ and $w_2(y_2)$), and no cycle. A long read-only transaction under multiversion timestamp ordering or snapshot isolation behaves in this way.

**Write skew is not MVSR.**

$$m = r_1(x_0)\, r_1(y_0)\, r_2(x_0)\, r_2(y_0)\, w_1(x_1)\, w_2(y_2)\, c_1\, c_2.$$

In the serial order $T_1 T_2$, $T_2$ would read $x_1$; in $T_2 T_1$, $T_1$ would read $y_2$. Neither matches. In the graph, the only possible version order puts $x_0$ first, so $r_2(x_0)$ and $w_1(x_1)$ give $T_2 \to T_1$, and $r_1(y_0)$ and $w_2(y_2)$ give $T_1 \to T_2$: a cycle for every version order. [Snapshot isolation](/snapshot-isolation/) allows this schedule; it is the [write skew](/write-skew/).

**The version order matters.** In $m = w_1(x_1)\, c_1\, w_2(x_2)\, c_2\, r_3(x_1)\, c_3$, the order $x_0 \ll x_1 \ll x_2$ gives the arcs $T_1 \to T_3$ and, from $r_3(x_1)$ and $w_2(x_2)$, $T_3 \to T_2$: the serial order is $T_1\, T_3\, T_2$, so $m$ is MVSR. The order $x_0 \ll x_2 \ll x_1$ also gives an acyclic graph, with the serial order $T_2\, T_1\, T_3$. Read as a monoversion schedule, $r_3(x)$ would return $x_2$ and not $x_1$, so the multiversion schedule has a reads-from relation that no monoversion schedule with the same step order has.

**Monoversion schedules.** A view serializable monoversion schedule is MVSR with its own version function, so VSR is contained in MVSR. The containment is strict, as the first example shows.

**Not MVSR, for every version order.** $m = r_1(x_0)\, w_2(x_2)\, c_2\, r_1(x_2)\, c_1$ reads two different versions of $x$ in one transaction with no write of $T_1$ between. Before $T_2$ in the serial order, $T_1$ reads $x_0$ twice; after it, $T_1$ reads $x_2$ twice. Neither matches, so $m$ is not MVSR.

## Related definitions

- [View serializability](/view-serializability/) is the monoversion form; it also needs the same final writes. Its test is NP-complete, by [view-serializability NP-completeness](/view-serializability-np-completeness/); Papadimitriou and Kanellakis (1984) proved the same for MVSR.
- [Conflict serializability](/conflict-serializability/), tested by the [serializability theorem](/serializability-theorem/), is contained in view serializability, so a conflict serializable monoversion schedule is MVSR. The MVSG has no arcs for two writes alone: the order of two blind writes matters only through the reads around them.
- [One-copy serializability](/one-copy-serializability/) for replicated data has the same form: the copies there play the part of versions here.
- [Snapshot isolation](/snapshot-isolation/) and multiversion [timestamp ordering](/timestamp-ordering/) fix the version order by commit time or by timestamp, so the MVSG becomes a graph that a scheduler can keep.
- [Adya's isolation levels](/adya-isolation-levels/) use the same graph with the version order given by the history, split into write, read and anti-dependency arcs, and define weaker levels by the cycles they forbid. The [dangerous structure theorem](/snapshot-isolation-dangerous-structure/) is a statement about the cycles of this graph under snapshot isolation.

## References
