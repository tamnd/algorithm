---
tag: CXP807
kind: definition
slug: one-copy-serializability
name: One-copy serializability
aliases:
- 1SR
area: databases/distributed-databases
level: core
summary: "An execution on replicated data is one-copy serializable when it is equivalent to a serial execution on a single copy of each item."
prereqs: [serializability, view-serializability]
see_also: [read-one-write-all, primary-copy-locking, quorum-replication, multiversion-serializability, linearizability, consistency-models, highly-available-transactions, view-serializability-np-completeness]
sources:
  - book: isbn:9780201107159
    title: "Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987"
    locator: "Chapter 8, Replicated Data: the write-all-available example (Section 8.1), RD histories, 1C histories and the definition of 1SR with Lemma 8.2 and Theorem 8.3 (Section 8.3), and the replicated data serialization graph with Theorem 8.4 (Section 8.4)"
  - paper: doi:10.1145/1994.2207
    title: "Philip A. Bernstein and Nathan Goodman, An algorithm for concurrency control and recovery in replicated distributed databases, ACM Transactions on Database Systems 9(4), 1984, pages 596 to 615"
    locator: "one-copy serializability as the correctness criterion for replicated data, and its use to prove the available copies algorithm correct"
---

One-copy serializability (1SR) is the standard correctness criterion for transactions on replicated data. The database keeps several copies of each item, at different sites, and the system turns each read and write of an item into reads and writes of copies. An execution is one-copy serializable if the users cannot tell it apart from a serial execution of the same transactions on a database with one copy of each item: each transaction reads the same values, and the database ends in the same state. Ordinary [serializability](/serializability/) of the copy-level execution is not enough. An execution can be conflict serializable as a history over copies and still give results that no one-copy execution gives.

## Definition

The definition is that of Bernstein, Hadzilacos and Goodman (1987), Section 8.3. Let $T_0, T_1, \dots, T_n$ be transactions over items $x, y, \dots$, where $T_0$ writes the initial value of every copy. Each item $x$ has copies $x_A, x_B, \dots$ at sites $A, B, \dots$.

**Replicated data history.** A *translation* maps each read $r_i[x]$ to a read $r_i[x_A]$ of one copy, and each write $w_i[x]$ to writes $w_i[x_{A_1}], \dots, w_i[x_{A_m}]$ of one or more copies. A *replicated data (RD) history* is a partial order of the translated operations, plus commits and aborts, such that:

1. it keeps the order of the operations inside each transaction;
2. every copy that is read was written before, at least by $T_0$;
3. any two operations on the same copy, at least one of them a write, are ordered;
4. if $T_i$ writes $x$ and then reads $x$, it reads a copy that it wrote.

A *one-copy (1C) history* is an ordinary history over the items, as if each item had one copy. As in the book, take every history to be the committed projection of itself.

**Reads-from on items.** $T_j$ *reads $x$ from* $T_i$ in an RD history $H$ if, for some copy $x_A$, $w_i[x_A] < r_j[x_A]$ and no other write of $x_A$ comes between them. A transaction reads each item at most once and reads one copy, so this relation is a function. In a 1C history, reads-from is the usual relation on items.

**Final writes.** $w_i[x_A]$ is a *final write* for the copy $x_A$ in $H$ if every other write of $x_A$ comes before it. In a 1C history, the final write for $x$ is the last write of $x$.

**Equivalence.** An RD history $H$ is *equivalent* to a 1C history $H_{1C}$ over the same transactions if

1. $T_j$ reads $x$ from $T_i$ in $H$ if and only if $T_j$ reads $x$ from $T_i$ in $H_{1C}$, and
2. for each final write $w_i[x]$ in $H_{1C}$, $w_i[x_A]$ is a final write in $H$ for some copy $x_A$ of $x$.

**One-copy serializability.** $H$ is *one-copy serializable* if it is equivalent to a serial 1C history.

This is [view equivalence](/view-serializability/) between a history over copies and a history over items. Conflict equivalence cannot be used, because the two histories have different operations: two writes of $x$ conflict in $H_{1C}$, but their translations may touch different copies. The second condition asks only that the last write of each item reach some copy. It does not ask the copies to be equal at the end.

**A sufficient test.** Let $\mathrm{SG}(H)$ be the serialization graph of $H$ over copies, with an edge $T_i \to T_j$ for each pair of conflicting operations on one copy with $T_i$'s operation first. A *replicated data serialization graph* (RDSG) is $\mathrm{SG}(H)$ with edges added so that (a) any two transactions that write $x$ are connected by a path, in one direction or the other, and (b) if $T_j$ reads $x$ from $T_i$, $T_k$ writes $x$, $k \neq i, j$, and there is a path from $T_i$ to $T_k$, then there is a path from $T_j$ to $T_k$. Theorem 8.4 of the book states: if $H$ has an acyclic RDSG, then $H$ is 1SR, and a topological order of the graph is an equivalent serial order. Most correctness proofs of replica control protocols use this theorem or Theorem 8.3, which states that the same reads-from relation as a serial 1C history in an order consistent with $\mathrm{SG}(H)$ is enough.

## Examples and non-examples

Each claim below was checked by a brute-force search over all serial orders, with the helper of the [read-one write-all](/read-one-write-all/) page. $T_0$ is implicit.

**Read one, write all.** $H = w_1[x_A]\, w_1[x_B]\, c_1\, r_2[x_B]\, c_2$. $T_2$ reads $x$ from $T_1$, so the equivalent serial 1C history is $T_1\, T_2$. Write-all with strict two-phase locking gives histories of this kind.

**A serial history over copies that is not 1SR.** This is history $H_1$ of Section 8.1 of the book, in which $T_1$ wrote only one copy of $x$:

$$H_1 = r_1[y_C]\, w_1[x_A]\, c_1\, r_2[x_B]\, w_2[y_C]\, c_2.$$

$T_2$ reads $x_B$ from $T_0$, an old copy. In a serial 1C history in the order $T_1\, T_2$, $T_2$ would read $x$ from $T_1$. In the order $T_2\, T_1$, $T_1$ would read $y$ from $T_2$. Neither holds, so $H_1$ is not 1SR, although it is serial as a history over copies.

**A conflict serializable history over copies that is not 1SR.** This is history $H_4$ of Section 8.4. $T_1 = r_1[x]\, w_1[y]$ and $T_2 = r_2[y]\, w_2[x]$, with copies $x_A, x_B, y_C, y_D$:

$$H_4 = r_1[x_A]\, r_2[y_D]\, x_A \text{ fails}\, y_D \text{ fails}\, w_1[y_C]\, w_2[x_B]\, c_1\, c_2.$$

No two operations touch the same copy, so the copy-level serialization graph has no edges between $T_1$ and $T_2$. But each transaction reads an item that the other one writes, and neither reads the other's value, so no serial 1C history fits. Two-phase locking on copies cannot prevent this, because the logical conflicts never become conflicts on copies. The available copies algorithm adds checks at commit for this reason.

**Copies that differ at the end.** $H = w_1[x_A]\, w_1[x_B]\, c_1\, w_2[x_A]\, c_2$. At the end $x_A$ holds the value of $T_2$ and $x_B$ holds the value of $T_1$. The history is 1SR, and in two ways: in the order $T_1\, T_2$ the final write of $T_2$ is the final write of $x_A$, and in the order $T_2\, T_1$ the final write of $T_1$ is the final write of $x_B$. The criterion speaks about what transactions read, so a stale copy is harmless as long as no one reads it.

**A stale read that 1SR allows.** $H = w_1[x_A]\, c_1\, r_2[x_B]\, c_2$, where $T_2$ starts after $T_1$ commits. $T_2$ reads the initial value from $x_B$. The history is 1SR in the order $T_2\, T_1$: the definition has no notion of real time. A client that sees $T_1$ commit and then starts $T_2$ can still see the old value. Strong one-copy serializability, also called strict serializability, adds the rule that the serial order must respect the real-time order of transactions that do not overlap.

**One copy per item.** If every item has exactly one copy, an RD history is an ordinary history, and the definition becomes view serializability. So deciding whether a history is 1SR is NP-complete in general, by the [NP-completeness of view serializability](/view-serializability-np-completeness/). Protocols therefore aim at sufficient conditions, such as an acyclic RDSG, that they can enforce one step at a time.

## Related definitions

- **[Serializability](/serializability/) and [view serializability](/view-serializability/).** 1SR is view serializability where the history on the left is over copies and the serial history on the right is over items.
- **[Multiversion serializability](/multiversion-serializability/).** Multiversion histories use the same idea: a history over versions is correct if it is equivalent to a serial history over items with one version each. Bernstein, Hadzilacos and Goodman point out that the two theories are very similar.
- **Strong one-copy serializability.** 1SR plus the real-time order of non-overlapping transactions. It is the transactional form of [linearizability](/linearizability/), which is defined for single operations on single objects.
- **Weaker criteria.** Many replicated systems give less than 1SR: snapshot isolation on replicas, the [consistency models](/consistency-models/) of replicated stores, and the [highly available transactions](/highly-available-transactions/) of Bailis et al., which can run without coordination when the network is partitioned. In the asynchronous model with partitions that can last forever, no system can give 1SR and stay available at the same time.
- **Protocols.** [Read-one write-all](/read-one-write-all/) and its available copies form, [primary copy locking](/primary-copy-locking/) and [quorum replication](/quorum-replication/) with two-phase locking are the classic protocols that give 1SR.

## References
