---
title: Committed transactions under Kung-Robinson validation are conflict serializable
proves: [correctness]
status: full
---

**Model.** The schedule consists of the reads of read phases (line L2, when the item is not in the private write set) and the writes of write phases (lines L6 and L12) on the shared database. Only the operations of committed transactions count. Two operations conflict if they are of different transactions, on the same item, and at least one is a write. A transaction $T_i$ reads only in its read phase and writes only in its write phase, and its read phase ends before its validation, which ends before its write phase.

We use one fact about the counter. $tnc$ only grows, and a transaction $V$ has $tn(V) \le T.start$ if and only if $V$ finished its write phase before $T$ began (both lines L7 and L13 assign the number after the write phase, and line L1 reads $tnc$).

**Theorem 1 (serial validation).** If every transaction uses SERIAL-VALIDATE, the committed transactions are conflict equivalent to the serial schedule in which they appear in increasing order of $tn$.

*Proof.* Let $T_i$ and $T_j$ be committed, $tn(T_i) < tn(T_j)$, and let $p$ of $T_i$ and $q$ of $T_j$ conflict on item $x$. We show that $p$ precedes $q$.

Lines L4 to L7 run as one critical section, and numbers are given in the order of these sections. So the write phase of $T_i$ ends before the write phase of $T_j$ begins.

- *Both are writes.* They lie in the two write phases, so $p$ precedes $q$.
- *$p$ is a read of $T_i$ and $q$ a write of $T_j$.* $p$ is in the read phase of $T_i$, which ends before its write phase, which ends before the write phase of $T_j$. So $p$ precedes $q$.
- *$p$ is a write of $T_i$ and $q$ a read of $T_j$.* Then $x \in WS(T_i) \cap RS(T_j)$. If $tn(T_i) \le T_j.start$, $T_i$ finished its write phase before $T_j$ began, so $p$ precedes $q$. Otherwise $T_j.start < tn(T_i)$. At the validation of $T_j$, $finish = tnc \ge tn(T_i)$, because $T_i$ was numbered before the critical section of $T_j$. So line L5 tests $WS(tn(T_i)) \cap RS(T_j)$, which contains $x$, and $T_j$ aborts, a contradiction.

So every conflict goes from the smaller number to the larger, and the serial schedule in number order orders all conflicting pairs as the schedule does. $\square$

**Theorem 2 (parallel validation).** If every transaction uses PARALLEL-VALIDATE, the committed transactions are conflict equivalent to the serial schedule in the order in which they executed line L8.

*Proof.* Let $T_i$ and $T_j$ be committed, with $T_i$ executing line L8 before $T_j$, and let $p$ of $T_i$ and $q$ of $T_j$ conflict on $x$. At the moment $T_j$ executes line L8, either (a) $T_i$ has executed line L13, or (b) $T_i$ is in $active$, so $T_i \in A$ for $T_j$. ($T_i$ cannot have left $active$ by line L11, since it commits.)

*Case (a).* $T_i$ finished its write phase before $T_j$ entered validation, so before the write phase of $T_j$ and $tn(T_i) \le finish$ of $T_j$. A write-write conflict and a read of $T_i$ against a write of $T_j$ are then ordered $p$ first, as in Theorem 1. For a write of $T_i$ and a read of $T_j$: if $tn(T_i) \le T_j.start$, the write precedes the begin of $T_j$; otherwise $T_j.start < tn(T_i) \le finish$, and line L9 of $T_j$ finds $x$ and $T_j$ aborts, a contradiction.

*Case (b).* Line L10 of $T_j$ tests $WS(T_i) \cap (RS(T_j) \cup WS(T_j))$, which must be empty since $T_j$ commits. So the conflict is a read $p$ of $T_i$ against a write $q$ of $T_j$. The read phase of $T_i$ ended before $T_i$ executed line L8, which is before $T_j$ executed line L8 and so before the write phase of $T_j$. So $p$ precedes $q$.

In all cases $p$ precedes $q$, and the order of line L8 is a serial order. $\square$

**Remark (the numbers in parallel validation).** In case (b) the transaction $T_j$ can finish its write phase before $T_i$ and receive the smaller number. If then $RS(T_i) \cap WS(T_j) \ne \emptyset$, the read of $T_i$ precedes the write of $T_j$, so $T_i$ must precede $T_j$ in any equivalent serial order, against the order of the numbers. The example in the node and the tests of the implementation show such a run. The numbers still serve their purpose in line L9: a transaction with a number above $T.start$ finished during the life of $T$.

**Corollary (no cascading aborts).** Under both forms, the database holds only values written in write phases of validated transactions, so a read never returns a value of a transaction that later aborts.
