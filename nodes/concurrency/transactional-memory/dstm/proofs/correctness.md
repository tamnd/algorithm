---
title: DSTM with strict validation is opaque and obstruction-free
proves: [correctness, opacity, obstruction-freedom]
status: full
---

We prove two claims about DSTM as given by the pseudocode of the page (lines L1 to L15), with the strict validation of L11. First, each history is [opaque](/opacity/). Second, a transaction that runs alone from some point on commits after at most one more abort, so the algorithm is [obstruction-free](/obstruction-freedom/). We also show where the proof breaks if validation checks only the committed version.

**Model.** The processes are asynchronous and may stop at any time. Each object $o$ has a word start$(o)$ that holds a locator (owner, old, new); old and new are versions, each with a unique identity. Each transaction has a status word that starts as ACTIVE and changes at most once, to COMMITTED by its own CAS at L13 or to ABORTED by any CAS or by its own write at L14. The primitives are atomic read, write and compare-and-swap, under sequential consistency.

**Definition.** The *current version* $cv(o)$ at time $t$ is new if the owner of the locator in start$(o)$ is COMMITTED (or there is no owner), and old otherwise.

**Lemma 1 (versions).** (a) Installing a locator (L8), changing the value of an own locator (L6), aborting a transaction and killing one do not change $cv(o)$. (b) $cv(o)$ changes only when the owner $T$ of the current locator of $o$ commits by its CAS at L13, and then it becomes the new version of $T$, whose identity is fresh. (c) So the identity of $cv(o)$ never returns to an earlier value.

*Proof.* (a) A transaction computes cur at L2 to L4 only after it has seen the owner COMMITTED or ABORTED, which are final; so the $cv(o)$ of the locator it read is fixed, and the CAS at L8 succeeds only if that locator is still in start$(o)$. The new locator has old $=$ cur and an ACTIVE owner, so $cv(o)$ is unchanged. The other cases change no committed state of any locator. (b) and (c) follow, since a status becomes COMMITTED only once. $\square$

**Lemma 2 (owned objects).** Let $T$ commit at time $c_T$, and let $T$ install its locator on $o$ at time $i$. Then in $[i, c_T]$ the locator of $T$ stays in start$(o)$, no open of $o$ by another transaction returns, and every validation of another transaction that checks $o$ in this interval fails.

*Proof.* Another transaction replaces a locator only after it has seen the owner COMMITTED or ABORTED at L3 or L4. $T$ is ACTIVE in $[i, c_T)$, and once ABORTED it could not commit. So the locator stays, and an open of $o$ in this interval keeps looping at L3: it backs off or kills $T$, and a kill would stop $T$ from committing. A strict validation that reads $o$ sees an ACTIVE owner and fails. $\square$

**Lemma 3 (validation).** If a call of VALIDATE that starts at time $s$ returns true, then the status of the caller was ACTIVE at $s$, and for each entry $(o, id)$ of its read table, $cv(o)$ had identity $id$ at $s$.

*Proof.* The entry was added at L5 after the open had found $cv(o) = id$, before $s$. The scan finds the same identity at a later time. By Lemma 1c the identity did not change in between, so it was $id$ at $s$. $\square$

**Theorem 1 (opacity).** Each finite history of DSTM with strict validation is opaque.

*Proof.* Complete the history: a commit-pending transaction whose CAS at L13 succeeded is completed as committed, every other live or commit-pending one as aborted. Give each transaction $T$ a point $s_T$: the start of its last VALIDATE that returned true (for a committed $T$ this is the one at L12), or its begin if there is none. Order the transactions by $s_T$, and let only the committed ones take effect.

*Legality.* A read of an object that $T$ owns returns the last own write. Take a read of $o$ by $T$ from another version, with identity $id$. By Lemma 3, $cv(o)$ had identity $id$ at $s_T$, so $id$ is the version of the last committed writer $W$ of $o$ with $c_W < s_T$ (or the initial version). We show that this is also the last writer of $o$ before $T$ in the serial order.

First, the committed writers of $o$ are in the same order by $s$ and by $c$. If $U_1$ and $U_2$ both write $o$ and $U_1$ commits first, then $U_2$ installs its locator after $c_{U_1}$ (Lemma 2), and $s_{U_2}$ comes after that, while $s_{U_1} < c_{U_1}$. So $W$ comes before $T$, and every writer of $o$ that commits after $W$ and before $s_T$ does not exist by the choice of $W$.

Second, no committed writer $U$ of $o$ has $s_U < s_T < c_U$. Such a $U$ installed its locator on $o$ at a time $i_U < s_U$. If $T$ opened $o$ in $[i_U, c_U]$, the open would not return (Lemma 2). If $T$ opened $o$ before $i_U$, its validation that starts at $s_T$ checks $o$ at a time after $i_U$: before $c_U$ it sees an ACTIVE owner and fails (Lemma 2), and after $c_U$ it sees a new identity and fails. If $T$ opened $o$ after $c_U$, the read is after $s_T$, which is impossible, since $s_T$ follows every read of $T$ that returned a value (each read is followed by a successful validation at L5, by the choice of $s_T$). So each read of $T$ returns the value that the serial order gives. A read whose validation fails ends in ABORT and returns no value.

*Real-time order.* If $T$ completes before $U$ begins, then $s_T$ is before the end of $T$ and $s_U$ is after the begin of $U$, so $T$ comes first.

So the completed history is equivalent to a legal serial history that respects real-time order. $\blacksquare$

**Where version-only validation fails.** The second step of the legality proof uses the strict check: if $T$ read $o$ before $U$ installed its locator, a validation of $T$ between $i_U$ and $c_U$ must fail. If VALIDATE checks only that the identity of $cv(o)$ is unchanged, it passes there, since $cv(o)$ is still the old version. Then two transactions $T$ (reads $x$, writes $y$) and $U$ (reads $y$, writes $x$) can each pass the validation at L12 before either CAS at L13, and both commit. Neither serial order explains this history, so it is not even serializable. The test `test_version_only_validation_allows_write_skew` runs it.

**Theorem 2 (obstruction-freedom).** If from some time on a transaction attempt of $p$ and its retries are the only steps taken, then $p$ commits after at most one abort.

*Proof.* In a solo attempt, an open of $o$ that finds an ACTIVE owner backs off at most a bounded number of times and then kills the owner, so L2 to L4 end in a bounded number of steps. The CAS at L8 can fail only if start$(o)$ changed since L2, which needs a step of another process. A validation can fail only if a read object changed or is owned by an ACTIVE transaction. In the attempt that was running when the solo period began, an object in the read table may have been opened for writing before that time, so one abort is possible. In the next attempt, every object that $p$ reads has been opened by $p$ alone, with every ACTIVE owner killed first, and no other process steps; so every validation passes and the CAS at L13 succeeds. $\square$

The contention manager does not appear in Theorem 1, and Theorem 2 needs only that it kills an active owner after a bounded number of back-offs. A contention manager that could wait for ever for a stopped owner would make DSTM blocking.
