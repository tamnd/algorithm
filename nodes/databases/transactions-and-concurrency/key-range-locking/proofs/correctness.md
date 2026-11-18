---
title: Next-key locking keeps a lock on the cover of every key value that a transaction used, so there are no phantoms
proves: [correctness]
status: full
---

**Setting.** The index holds a set $K$ of keys from an ordered domain $D$. EOF is a key above all of $D$; it is never in $K$, but it can be locked. Each value $v \in D$ is a *slot*, whether or not $v \in K$. The operations use the slots as follows:

- $\mathrm{scan}(lo, hi)$ reads the slots $lo, \dots, hi$ (also the empty ones);
- $\mathrm{fetch}(k)$ reads the slot $k$;
- $\mathrm{insert}(k)$ writes the slot $k$ if $k \notin K$, and reads it if $k \in K$ (a duplicate key);
- $\mathrm{delete}(k)$ writes the slot $k$ if $k \in K$, and reads it otherwise.

The result of an operation depends only on the slots it reads or writes, and it changes only the slots it writes. A phantom is a change of a slot that a transaction read, by another transaction that is still running or that comes after it in the serial order. So it is enough to show that the schedule of slot reads and writes is strict and conflict serializable.

For $v \in D$, let $\mathrm{next}(v)$ be the smallest key of $K$ above $v$, or EOF (line L1), and let the *cover* of $v$ be $\mathrm{cov}(v) = v$ if $v \in K$ and $\mathrm{cov}(v) = \mathrm{next}(v)$ otherwise: the smallest element of $K \cup \{\mathrm{EOF}\}$ that is at least $v$. Locks are S or X, two locks of different transactions on one key are compatible only if both are S, and the lock table never has two incompatible holders on one key. A lock is held to the end of its transaction, except the instant lock of line L6, which is only tested. An operation runs in the same step in which it has all the locks that lines L2 to L9 ask for, computed on the current $K$; after a wait, the locks are computed again.

**Lemma 1 (how a cover moves).** Adding a key $j$ to $K$ changes the cover of exactly the slots $v$ with $v \le j < \mathrm{cov}(v)$, and for those $\mathrm{cov}(v) = \mathrm{cov}(j)$ before the change, and $\mathrm{cov}(v) = j$ after it. Removing a key $j$ changes the cover of exactly the slots $v$ with $\mathrm{cov}(v) = j$, which then becomes $\mathrm{next}(j)$.

*Proof.* The cover is the smallest element of $K \cup \{\mathrm{EOF}\}$ that is at least $v$. A new element $j$ changes this minimum exactly when $v \le j$ and $j$ is below the old minimum. Then no key lies in $[v, \mathrm{cov}(v))$, so also none in $[j, \mathrm{cov}(v))$, and $\mathrm{cov}(j) = \mathrm{cov}(v)$. Removing $j$ changes the minimum exactly when $j$ was the minimum, and the next element is $\mathrm{next}(j)$. $\square$

**Invariant (I).** After every step, for every active transaction $T$ and every slot $v$ that $T$ has read or written: $T$ holds a lock on $\mathrm{cov}(v)$, and the lock is X if $T$ has written $v$.

*Proof.* By induction on the steps. At the start no transaction is active. A step that only grants locks, or that makes a transaction wait, does not change $K$ and only adds locks. A commit ends its transaction. The other steps are the following.

*An operation of $T$ uses new slots.* Look at $K$ just before the operation.

- $\mathrm{scan}(lo, hi)$: for $lo \le v \le hi$, the cover of $v$ is a key of $K$ in $[lo, hi]$, or the smallest key above $hi$, which is $\mathrm{next}(hi)$. Line L2 locks all of them.
- $\mathrm{fetch}(k)$ and the failed operations: line L4, L5 or L8 locks $k$ if $k \in K$ and $\mathrm{next}(k)$ if not, which is $\mathrm{cov}(k)$, and $K$ does not change.
- A successful $\mathrm{insert}(k)$: line L7 locks $k$ in X, and after the insert $\mathrm{cov}(k) = k$.
- A successful $\mathrm{delete}(k)$: line L9 locks $\mathrm{next}(k)$ in X, and after the delete $\mathrm{cov}(k) = \mathrm{next}(k)$, because no key lies between $k$ and $\mathrm{next}(k)$.

*A change of $K$ by a transaction $U$ moves the cover of slots of $T$.* There are four ways that $U$ changes $K$: a successful insert, a successful delete, and, at the abort of $U$ (line L10), the removal of a key that $U$ inserted and the return of a key that $U$ deleted. In each case $U$ holds an X lock on the old cover of every slot whose cover moves:

- An insert of $j$ by $U$: by Lemma 1, the moved slots have the old cover $\mathrm{cov}(j) = \mathrm{next}(j)$, since $j \notin K$. Line L6 tested an instant X lock on it in the same step, so no other transaction holds a lock on it.
- The return of a deleted key $j$ at the abort of $U$: $U$ wrote the slot $j$, so by (I) before the step, $U$ holds X on $\mathrm{cov}(j)$, the old cover of the moved slots.
- A delete of $j$ by $U$: line L9 holds X on $j$, the old cover of the moved slots.
- The removal of an inserted key $j$ at the abort of $U$: $U$ wrote the slot $j$ and $j \in K$, so by (I), $U$ holds X on $\mathrm{cov}(j) = j$.

So if $T \ne U$ held a lock on the old cover, it would hold a lock that is incompatible with the X lock of $U$ on the same key. This cannot be, so no slot of another active transaction moves. If $T = U$ and the change comes from an operation, the new cover is $j$ after an insert (X by line L7) or $\mathrm{next}(j)$ after a delete (X by line L9). If $T = U$ and the change comes from the abort, $T$ ends in this step, and (I) says nothing about it.

*Releases.* Locks are released only at the end of their transaction, and the instant lock of line L6 is never kept, so no step removes a lock that (I) needs. $\square$

**Theorem 1 (conflicting slot accesses do not overlap).** If $T$ reads or writes the slot $v$, and later another transaction $U$ makes an access to $v$ that conflicts with it (one of the two is a write), then $T$ ended before the access of $U$.

*Proof.* Suppose $T$ is still active after the step of $U$. By (I) after this step, $T$ and $U$ both hold a lock on the same key $\mathrm{cov}(v)$, and one of them holds X. The lock table never has such a pair. $\square$

**Corollary 1 (no phantoms).** The schedule of slot accesses is strict, and its committed projection is conflict equivalent to the serial schedule in commit order. Each committed transaction gets the same results as in the serial run of the committed transactions in commit order, and the final set of keys is the same.

*Proof.* By Theorem 1, every access that follows a write of another transaction to the same slot comes after the end of that transaction, so the schedule is strict. For committed $T$ and $U$ with conflicting accesses, the access of $T$ first, Theorem 1 puts the commit of $T$ before the access of $U$, so before the commit of $U$; all conflicting pairs are in commit order.

For the results: by Theorem 1, between a write of a slot by a transaction $U$ that aborts and the abort, no other transaction uses the slot, and the undo of line L10 gives it back the value it had before the first write of $U$. So the aborted transactions can be removed without changing what any other operation sees. The value of a slot that an operation of a committed transaction sees is then the value written by the last write before it, which by the order of the conflicting pairs is the last write in the serial run in commit order. The result of an operation depends only on the values of its slots, so it is the same as in the serial run, and so are the final values of all slots. $\square$

**Deadlocks.** The method does not prevent deadlocks: two transactions that have scanned the same range and then both insert into it each wait for the S lock of the other on a next key. The driver of the tests aborts the largest transaction id on a cycle of the wait-for graph; the proof above covers the undo of an aborted transaction.

**What the tests check.** The tests check (I) after every step of the driver, and Corollary 1 for every output, in three ways: against a serial run of the committed transactions in commit order on a plain sorted list, with the helper `dbsched` for strictness and conflict equivalence on the slots, and by brute force over all serial orders for up to three committed transactions. They do this for all interleavings of four pairs of programs (a scan against an insert into the range, a missed lookup against an insert into the gap, a gap below EOF, and a delete against a scan) and for 600 random interleavings of three or five transactions. They also run a naive variant that locks only the keys that exist and that the operation touches, and they check that it gives phantoms, in each of the four pairs and in the random runs.
