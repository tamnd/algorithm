---
title: SwissTM is opaque, and its two-phase contention manager cannot deadlock
proves: [correctness, opacity, deadlock-freedom]
status: full
---

We prove two claims about SwissTM as given by the pseudocode of the page (lines L1 to L22). First, each history is [opaque](/opacity/). Second, no set of transactions can wait for each other for ever. The proof of opacity follows the one for [TinySTM](/tinystm/); the new parts are the split of each lock into a write lock and a read lock, and the contention manager, which plays no part in safety.

**Model.** The processes are asynchronous. The shared words are the data words, the commit clock CLOCK, the greedy counter, one status word per process, and for each data word $a$ a write lock $wl(a)$ (an owner or FREE) and a read lock $rl(a)$ (a version, which is an integer, or LOCKED). The primitives are atomic read, write, compare-and-swap and fetch-and-add, under sequential consistency.

**Notation.** For a transaction $T$, $vt_T$ is its valid timestamp, set at L1 and at L14. $T$ is an *update* transaction if its write set is not empty at L15; then $ts_T$ is the value of L18. $T$ is *effective* if it has passed L19; it cannot abort after that. Every value drawn from CLOCK is distinct, and later draws give larger values.

**Lemma 1 (locks).** (a) At most one transaction owns $wl(a)$ at a time. (b) Only the owner of $wl(a)$ writes $rl(a)$ or the data word $a$. (c) The owner writes $a$ only at L20, and then $rl(a)$ is LOCKED. (d) When the owner sets $rl(a)$ back to a version, the version is either the version $v_0$ that it saved at L17 (an abort at L19, which wrote no data word) or $ts_T$, which is larger than $v_0$ and than every version that $rl(a)$ had before.

*Proof.* (a) $wl(a)$ is taken only by the CAS at L11, which needs FREE, and is set to FREE only by its owner at L21 or L22. (b) and (c) are read off the code: $T$ takes $wl(a)$ before it puts $a$ in its write set, and L17 to L21 touch only words of the write set. (d) $v_0$ is 0 or the $ts$ of an earlier owner, drawn before that owner released $wl(a)$, so before $T$ took it; $ts_T$ is drawn later. $\square$

So the versions of each read lock only grow, and a data word changes only while its read lock is LOCKED.

For $x \ge 0$ let $S(x)$ be the state obtained from the initial memory by the write sets of the effective transactions with $ts \le x$, applied in increasing order of $ts$.

**Lemma 2 (an unlocked read lock).** If at time $t$ the read lock $rl(a)$ holds the version $v$, then $a$ holds $S(v)[a]$ at $t$, and each effective writer of $a$ that has not released $rl(a)$ before $t$ sets $rl(a)$ to LOCKED after $t$ and has $ts > v$.

*Proof.* By induction on the writes of $rl(a)$. Initially $v = 0$ and $a$ holds $S(0)[a]$. An abort at L22 restores the saved version and changed no data word, so the claim keeps holding. An effective $T$ locks $rl(a)$ at L17, draws $ts_T$, writes $a$, and sets $rl(a)$ to $ts_T$. The effective writers of $a$ are ordered by their periods of ownership of $wl(a)$ (Lemma 1a), and each draws its $ts$ inside its period, so no effective writer of $a$ has a $ts$ between the $v_0$ of $T$ and $ts_T$. So $a$ holds $S(ts_T)[a]$ after L21. A writer that locks $rl(a)$ after $t$ draws its $ts$ after $t$, when CLOCK is at least $v$, so its $ts > v$. $\square$

**Lemma 3 (the read set).** For each live transaction $T$, between its operations, each entry $(a, ver)$ of its read set has $ver \le vt_T$, and the value that $T$ read from $a$ is $S(vt_T)[a]$.

*Proof.* By induction on the steps of $T$.

*A read (L4 to L8).* The two samples $v_1$ and $v_2$ of $rl(a)$ are equal and are versions. A data write to $a$ between them would need $rl(a)$ LOCKED in between, and the next version would be larger than $v_1$ (Lemma 1d), unless the owner aborted, and then it wrote nothing. So the load returned the value of $a$ at the first sample, which is $S(v_1)[a]$ by Lemma 2. If $v_1 \le vt_T$, then $vt_T$ was read before the first sample. An effective writer of $a$ with $ts$ in $(v_1, vt_T]$ drew its $ts$ before that, so it had locked $rl(a)$ before the first sample, and at that sample $rl(a)$ was LOCKED or a version of at least $ts > v_1$. Both contradict the sample. So $S(v_1)[a] = S(vt_T)[a]$. If $v_1 > vt_T$, $T$ extends (L7).

*An extension (L14).* Let $now$ be the clock value read at L14 at time $t$. VALIDATE then checks, after $t$, that $rl(b)$ still holds $ver$ for each entry $(b, ver)$. An effective writer of $b$ with $ts$ in $(ver, now]$ drew its $ts$ before $t$ and locked $rl(b)$ before that; at the check $rl(b)$ would be LOCKED or larger than $ver$. So $S(now)$ and $S(ver)$ agree on each word that $T$ read, and setting $vt_T = now$ keeps the claim. $\square$

**Lemma 4 (commit).** If $T$ is effective, each value that $T$ read is the value in $S(ts_T - 1)$.

*Proof.* If $ts_T = vt_T + 1$, this is Lemma 3. Otherwise VALIDATE at L19 runs after the fetch-and-add of $T$. For a word $b$ that $T$ did not lock, the argument of the extension case applies with $now$ replaced by $ts_T - 1$. For a word $b$ that $T$ also writes, VALIDATE compares $ver$ with the version saved at L17. An effective writer $U$ of $b$ with $ts_U$ in $(ver, ts_T)$ owned $wl(b)$ in a period disjoint from that of $T$ (Lemma 1a). It cannot come after: it would draw $ts_U$ after $T$ released, so after $ts_T$. So it released before $T$ took $wl(b)$, and the saved version is at least $ts_U > ver$; VALIDATE fails. $\square$

**Theorem 1 (opacity).** Each finite history of SwissTM is opaque.

*Proof.* Complete the history: effective transactions without a commit event are completed as committed, and the other live or commit-pending transactions as aborted. Place each effective $T$ at position $ts_T$, a read-only committed $T$ and every other $T$ at $vt_T + \tfrac12$ with its final $vt_T$, and break ties by the time of L1.

*Legality.* Only effective transactions take effect in the serial run, so the state before an effective $T$ is $S(ts_T - 1)$ and the state at $vt + \tfrac12$ is $S(vt)$. A read of a word in the write set returns the own last write (L3). Every other read returns a value of $S(vt_T)$ by Lemma 3, and, if $T$ is effective, of $S(ts_T - 1)$ by Lemma 4. No transaction ever reads a value that is not committed, because data words are written only at L20 by effective transactions.

*Real-time order.* Let $T$ complete before $U$ begins. Each $vt_U$ and $ts_U$ comes from a clock read after $U$ began. If $T$ is effective, $ts_T \le vt_U < ts_U$ for the first $vt_U$, and $vt_U$ only grows. If $T$ is not effective, its final $vt_T$ was read before $T$ completed, so $vt_T \le vt_U$; a tie is broken by L1, where $T$ comes first.

So the completed history is equivalent to a legal serial history that respects real-time order. $\blacksquare$

The contention manager does not appear in this proof. The kill at L12 only changes a status word; it never takes a lock from its owner. Safety rests on the write lock and the read lock alone.

**Theorem 2 (no deadlock).** No set of transactions waits for each other for ever.

*Proof.* A transaction waits only at two places. At L4 it waits while $rl(a)$ is LOCKED; the owner is then between L17 and L21, where it takes no wait, so it ends in a bounded number of its own steps. At the end of L12, a transaction $A$ waits until the owner $B$ releases $wl(a)$, and only in two cases: $B$ was committing or aborted when $A$ read its status, or $A$ aborted $B$ by the CAS. In the second case the CAS succeeded on the exact status word that $A$ read, so $B$ was active with greedy timestamp $c_B$, and $c_A < c_B$. A timid transaction ($c = \infty$) never waits there, because the test $c_A \ge c_B$ at L12 makes it abort itself. A greedy timestamp never changes once set, so each wait edge between active transactions goes from a smaller timestamp to a larger one, and the waits-for graph has no cycle. Take the last transaction on a chain of waits. It does not wait. If it was aborted, its next status check (L2 or L9), its status CAS at L16 or its greedy switch at L13 fails, and its rollback releases its locks. If it is committing, it finishes. Either way it releases the lock, and the chain gets shorter. $\square$

The CAS at L12 must expect the full status word, timestamp included. If the CM read the owner's timestamp in one step and killed the owner in another, two transactions could each see the other as timid, each kill the other, and each wait for the other's lock. The tests of the page found exactly this run in an earlier version of the code, where the timestamp lived in a separate word.
