---
title: Percolator gives snapshot isolation, and lazy cleanup keeps each transaction all or nothing
proves: [correctness, messages]
status: full
---

We use the line numbers of the pseudocode on the page. The model is the model of the page and of the toy code. Each step of a client or of a cleanup is one row transaction: it reads and changes the columns of one cell atomically. (The toy does the two row transactions of a cleanup in one step; the argument below does not need this, see the remark after Lemma 2.) The timestamp oracle returns strictly increasing timestamps, so no two calls return the same value. Clients can crash at any time, and a reader may clean up the lock of any client, dead or alive.

Each cell $x$ has a lock column, a data column and a write column, all indexed by timestamp. A write record $\mathrm{write}[x][c] = s$ says that the transaction with start timestamp $s$ wrote $x$ with commit timestamp $c$. We say a transaction $W$ with writes is *committed* when its primary cell $p$ has a write record that points to $W.\mathrm{start}$. A transaction with no writes is committed when it returns from its last read.

**Lemma 1 (write records).** Every write record $\mathrm{write}[x][c] = s$ belongs to a committed transaction $W$ with $W.\mathrm{start} = s$ and $W.\mathrm{commit} = c$, and $x$ is in the write set of $W$.

*Proof.* A write record is made at three places. Line L6 makes the record of the primary, and this step makes $W$ committed. Line L7 makes the record of a secondary, and the client runs it only after line L6 has succeeded. Line L12 makes a record on $x$ only when it finds the record of the primary of $s$, so $W$ is already committed, and it copies the commit timestamp of that record. Write records are never removed. $\square$

**Lemma 2 (the commit point is final).** If $W$ is committed, then no step ever removes a lock of $W$ without putting the write record of $W$ in its place, and no step removes data of $W$. If $W$ is not committed when a roll back of $W$ removes the primary lock, then $W$ never commits.

*Proof.* Locks of $W$ are removed at four places: line L6 and line L7 (which write the record in the same step), the roll forward of line L12 (the same), and a roll back, by the client after an abort or by a cleanup at line L12. The client rolls back only after line L4 or line L6 failed, and then $W$ is not committed. A cleanup rolls back only when the primary has no record of $W$, and it removes the primary lock first. Line L6 commits only if the primary lock of $W$ is still there, in the same row transaction as the check. So once the primary lock is gone without a record, line L6 fails for ever, and $W$ is never committed. In the other order, once line L6 has made the record, every later cleanup of $W$ finds it and rolls forward. Data is removed only by a roll back. $\square$

*Remark.* If a cleanup runs as two row transactions, first on the primary and then on $x$, Lemma 2 still holds. The decision is made in the step on the primary, and the step on $x$ only repeats it: a roll forward writes the same record that line L7 writes, and a roll back of $x$ follows a roll back of the primary, after which $W$ cannot commit.

**Theorem 1 (snapshot reads).** Let $T$ read $x$ at line L9 with start timestamp $s$. The value it returns is the value that $x$ has in the committed writer $W$ of $x$ with the largest commit timestamp below $s$.

*Proof.* Let $W$ be any committed writer of $x$ with $c = W.\mathrm{commit} < s$. $W$ wrote its lock on $x$ (line L11) before it asked the oracle for $c$ (line L5), and $T$ got $s$ (line L1) after the oracle gave out $c$, because $c < s$. $T$ reads only after it has $s$. So when $T$ reads $x$, the lock of $W$ on $x$ is there, or it has been removed. Its start timestamp is below $c < s$, so if it is there, line L8 sees it and $T$ waits. If it has been removed, Lemma 2 says the record $\mathrm{write}[x][c]$ is there. So line L9 runs only when every committed writer of $x$ with commit timestamp below $s$ has its record on $x$. By Lemma 1 every record on $x$ belongs to a committed writer of $x$. Hence the largest record below $s$ is the record of $W$ with the largest commit timestamp below $s$. Its data is still there by Lemma 2. (No commit timestamp equals $s$, because timestamps are unique.) $\blacksquare$

**Theorem 2 (first committer wins).** If two committed transactions $A$ and $B$ both write $x$, then $A.\mathrm{commit} < B.\mathrm{start}$ or $B.\mathrm{commit} < A.\mathrm{start}$.

*Proof.* Suppose not. The timestamps are distinct, so with no loss of generality $A.\mathrm{start} < B.\mathrm{start} < A.\mathrm{commit}$. Both ran line L11 on $x$. Look at the one that ran line L10 on $x$ second.

If it is $B$: the lock of $A$ on $x$ is still there, and line L10 aborts $B$; or the lock is gone, and since $A$ commits, Lemma 2 puts the record $\mathrm{write}[x][A.\mathrm{commit}]$ in its place, with $A.\mathrm{commit} > B.\mathrm{start}$, and line L10 aborts $B$.

If it is $A$: the lock of $B$ is still there, and line L10 aborts $A$; or it is gone, and the record $\mathrm{write}[x][B.\mathrm{commit}]$ is there, with $B.\mathrm{commit} > B.\mathrm{start} > A.\mathrm{start}$, and line L10 aborts $A$.

In each case one of them does not commit, which is a contradiction. $\blacksquare$

Theorems 1 and 2 are the two rules of snapshot isolation: each transaction reads the committed state at its start timestamp, and two concurrent transactions do not both write an item. The commit timestamps order the committed transactions, and each one acts as if it read at its start timestamp and wrote at its commit timestamp.

**Theorem 3 (all or nothing).** For a committed writer $W$, every item of its write set eventually has the record of $W$ if some reader with a later start timestamp reads it. For a writer that is not committed, no item ever has a record of $W$, and after a reader with a later start timestamp has read every item of $W$, no lock or data of $W$ is left.

*Proof.* The first part: the reader at line L8 sees the lock of $W$ on $x$ (start timestamp below its own) until the lock is replaced, and by Lemma 2 a lock of a committed $W$ is only replaced by its record. If the client of $W$ crashed, the reader runs line L12, finds the record of the primary and rolls forward. The second part: by Lemma 1 a record of $W$ exists only if $W$ is committed. A reader that meets a lock of a dead $W$ that is not committed runs line L12, finds no record on the primary, and removes the lock and data. After a roll back of the primary, $W$ cannot commit (Lemma 2), so the decision does not change later. $\blacksquare$

**Progress in the toy.** A reader waits only at line L8, for the lock of a writer. A writer holds locks only after its reads and never waits after that: lines L4 to L7 either succeed or abort at once. So a live writer always finishes, and the reader then goes on. A lock of a crashed writer is cleaned up by the first reader that meets it. So no client waits for ever, and there is no deadlock. In Percolator, a reader must first decide that the owner is dead (from its Chubby token or the wall time in the lock), which needs time-outs; safety does not depend on this decision, by Lemma 2.

**Theorem 4 (requests).** A transaction that runs alone, reads $r$ items and writes $w \ge 1$ items makes $r + 2w + 2$ requests: two to the oracle, $r$ reads, $w$ prewrites and $w$ commits. Each request has one reply, so this is $2r + 4w + 4$ messages.

*Proof.* With no other client there is no lock to wait for at line L8 and no conflict at line L10. The client asks the oracle at lines L1 and L5, reads each item once at line L9, prewrites each item once at line L11, and commits the primary at line L6 and each of the $w - 1$ secondaries at line L7. $\blacksquare$

**Snapshot isolation is not serializability.** Let $x = y = 1$ and let two transactions each read $x$ and $y$ and, if $x + y \ge 2$, set one of them to 0: $T_1$ sets $x$ and $T_2$ sets $y$. If both start before either commits, both read $x = y = 1$, their write sets do not meet, and Theorem 2 lets both commit. The result $x = y = 0$ is not the result of $T_1$ then $T_2$ (which gives $x = 0, y = 1$) or of $T_2$ then $T_1$. This is write skew, and Percolator allows it.
