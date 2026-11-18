---
title: The Silo commit protocol is conflict serializable in the order of its serialization points
proves: [correctness]
status: full
---

**Model.** This is the model of the implementation on the page. Every line of the pseudocode is one atomic step, and the steps of all transactions and of ADVANCE-EPOCH are interleaved in some order. Line L4 takes one lock per step and waits while another transaction holds it; line L7 checks one record per step; line L10 installs one record per step. A record is written only by line L10 of a transaction that holds its lock. A transaction *reads* $x$ at line L2 (line L1 returns its own write and is not an access to the database), and *writes* $x$ at line L10. For a committed transaction $T$, let $sp(T)$ be the time of its line L5. Two operations of different committed transactions *conflict* when they access the same record and at least one is a write. There are no inserts, deletes or range scans.

**Lemma 1 (locks).** If a committed transaction $T$ writes $x$, then $T$ holds the lock of $x$ during the whole interval from before $sp(T)$ until its write of $x$, and no other transaction writes $x$ in that interval.

*Proof.* Line L4 locks all of $W(T)$ before line L5. The lock of $x$ is released only at the install of $x$ in line L10, or at an abort, and $T$ does not abort. Only the lock holder writes $x$. $\square$

**Lemma 2 (write-write).** If committed transactions $T_1 \ne T_2$ both write $x$, and $T_1$ writes it first, then $sp(T_1) < sp(T_2)$.

*Proof.* By Lemma 1 each holds the lock of $x$ from before its serialization point to its write, and the two intervals cannot overlap. $T_1$ writes first, so the interval of $T_1$ ends before the interval of $T_2$ starts, and $sp(T_1) < sp(T_2)$. $\square$

**Lemma 3 (write-read).** If committed $T_2$ reads $x$ after committed $T_1$ wrote it, then $sp(T_1) < sp(T_2)$.

*Proof.* $sp(T_1)$ comes before the write of $T_1$ by Lemma 1. The read of $T_2$ comes after that write, and $sp(T_2)$ comes after all reads of $T_2$, since line L5 runs after the program ends. $\square$

**Lemma 4 (read-write).** If committed $T_1$ reads $x$ before committed $T_2 \ne T_1$ writes it, then $sp(T_1) < sp(T_2)$.

*Proof.* Let $t$ be the TID that $T_1$ saw at its first read of $x$, stored in $R(T_1)$ by line L2. Suppose $sp(T_2) < sp(T_1)$. $T_2$ locked $x$ before $sp(T_2)$ and holds it until its write of $x$. Line L7 of $T_1$ checks $x$ after $sp(T_1)$, so after $T_2$ locked $x$. At that check, either $T_2$ still holds the lock, and $T_1$ sees $x$ locked by another transaction, or $T_2$ has written $x$. In the second case $x.tid$ is the TID of $T_2$, or of a later writer. By Lemma 5 below, that TID is larger than $t$, so $x.tid \ne t$. In both cases $T_1$ aborts, which contradicts the assumption that it commits. The serialization points are distinct steps, so $sp(T_1) < sp(T_2)$. If $T_1$ also writes $x$, it holds the lock itself, and Lemma 2 applies to the two writes. $\square$

**Lemma 5 (TIDs grow).** Every write of a record $x$ sets $x.tid$ to a value larger than the value it replaces. The TID of a transaction is larger than every TID in its read set and larger than the previous TID of its worker. Its epoch is the value of $E$ at its serialization point.

*Proof.* Line L8 picks a TID in epoch $e$ above the maximum $b$ of the TIDs in $R(T)$, the current TIDs of the records in $W(T)$, and $last[w]$. Such a TID exists when the epoch of $b$ is at most $e$. Every TID in the maximum was chosen by a transaction whose epoch was read at its serialization point before $sp(T)$ (by Lemmas 2 and 3 for records, and by the order of the worker for $last[w]$), and $E$ never decreases, so the epoch of $b$ is at most $e$. The records of $W(T)$ are locked from before $sp(T)$, so their TIDs do not change between line L8 and line L10. $\square$

**Theorem 6.** In every run, the committed projection of the history is conflict equivalent to the serial history of the committed transactions in the order of $sp$. So it is conflict serializable.

*Proof.* By Lemmas 2, 3 and 4, every pair of conflicting operations of two committed transactions comes in the same order as their serialization points. So every arc of the conflict graph goes forward in the order of $sp$, the graph is acyclic, and the serial order of $sp$ puts every conflicting pair in the same order as the history. By the [serializability theorem](/serializability-theorem/) the two histories are conflict equivalent. Aborted transactions write nothing to the database, because they never reach line L10. $\square$

**Corollary 7 (epochs and TIDs).** Along the order of $sp$ the epochs of committed transactions never decrease. If $T_1 \to T_2$ is a write-write or write-read arc of the conflict graph, then the TID of $T_1$ is smaller than the TID of $T_2$. The TIDs of one worker increase.

*Proof.* The epoch of $T$ is $E$ at $sp(T)$, and $E$ only grows. For a write-read arc on $x$, $T_2$ saw a TID at least the TID of $T_1$ on $x$ (Lemma 5 for the later writers between them), and its own TID is larger. For a write-write arc on $x$, line L8 of $T_2$ runs after $T_1$ installed $x$, since $T_2$ waited for the lock, and its TID exceeds $x.tid$. The worker case is the $last[w]$ term of line L8. $\square$

An arc $T_1 \to T_2$ from a read of $T_1$ to a write of $T_2$ need not have a larger TID at $T_2$, so the TIDs alone are not a serial order; the epochs and the serialization points are. **Without the check of line L7** Lemma 4 fails. The test `test_without_validation_some_run_is_not_serializable` finds such a run, and `test_random_runs_are_serializable` checks Theorem 6 and Corollary 7 on 400 seeded runs, together with a serial replay in the order of $sp$ that gives the same reads and the same final values.
