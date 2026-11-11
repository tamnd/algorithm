---
title: TinySTM is opaque in write-back and in write-through mode
proves: [correctness, opacity]
status: full
---

We prove that each history of TinySTM, as given by the pseudocode of the page (lines L1 to L20), is [opaque](/opacity/), in both update modes. The proof follows the one for [TL2](/tl2/); the new parts are the locks taken at the first write, the snapshot extension, and the abort of a write-through transaction.

**Model.** The processes are asynchronous and may crash. The shared words are the data words, the clock CLOCK, and one lock word per stripe, holding (version, owner) with owner FREE or a transaction. The primitives are atomic read, write, compare-and-swap and fetch-and-add, under sequential consistency. Word $a$ has the stripe $s(a)$.

**Notation.** For a transaction $T$, $ub_T$ is its current snapshot bound (set at L1 and at L14). $T$ is an *update* transaction if it holds a lock when it reaches L15, and then $wv_T$ is the value of L16. $T$ is *effective* if it has passed L17; it cannot abort after that. An *abort version* is the value $nv$ that a write-through abort draws at L20. Every value drawn by FAA (a $wv$ or an $nv$) is distinct, and later draws give larger values.

**Lemma 1 (locks).** (a) Two transactions never own the same lock at the same time, and only the owner writes a lock word while it is owned. (b) A data word of stripe $s$ is written only by the owner of $s$: at L11 (write-through), at L18 (write-back), or at L20 (the undo of write-through). (c) When $T$ releases $s$, the version it writes is either the version $v_0$ that $s$ had when $T$ took it (a write-back abort, after which the data words of $s$ are as they were when $T$ took $s$, since $T$ wrote none), or a value drawn by FAA while $T$ owned $s$, hence larger than $v_0$ and than every version that $s$ had before.

*Proof.* (a) A lock is taken only by the CAS at L10, which needs owner FREE, and written otherwise only at L19 and L20 by the owner. (b) is read off the code. (c) $v_0$ is 0 or a value drawn by FAA before the owner that wrote it released $s$, so before $T$ took $s$; values drawn later are larger. In write-back mode an abort writes no data word. $\square$

So each lock version only grows, except that a write-back abort writes back the same version. In write-through mode, an abort always writes a new, larger version (L20). This is the point where the restore-the-old-version bug breaks the proof: a lock word that returns to an earlier value hides the in-place writes and their undo from a reader that sampled the lock before and after its load.

For $x \ge 0$ let $S(x)$ be the state obtained from the initial memory by the write sets of the effective transactions with $wv \le x$, applied in increasing order of $wv$.

**Lemma 2 (a free lock).** If at time $t$ the lock of $s$ is FREE with version $v$, then each data word $a$ of stripe $s$ holds $S(v)[a]$ at $t$, and every effective transaction that writes a word of $s$ and has not released $s$ before $t$ takes $s$ after $t$ and has $wv > v$.

*Proof.* By induction on the releases of $s$. Initially $v = 0$ and the memory is $S(0)$. Consider the release by $T$ that produced the current state of the lock, after $T$ took $s$ at version $v_0$ when (by induction) the stripe held $S(v_0)$. If $T$ is effective, it wrote its writes to $s$ (at L11 or L18) and released with $wv_T$. No other effective writer of $s$ has $wv$ in $(v_0, wv_T)$: one that released before $T$ took $s$ has $wv \le v_0$, and one that takes $s$ after $T$ draws its $wv$ later. So the stripe holds $S(wv_T)$ on $s$. If $T$ aborted in write-back mode, it wrote nothing and released with $v_0$. If $T$ aborted in write-through mode, the undo at L20 restored each word it wrote to its value when $T$ took $s$, which is $S(v_0)$, and $T$ released with $nv > v_0$; again no effective writer of $s$ has $wv$ in $(v_0, nv]$, so $S(v_0)$ and $S(nv)$ agree on $s$. A writer that takes $s$ after $t$ draws its $wv$ after $t$, and the clock at $t$ is at least $v$, so its $wv > v$. $\square$

**Lemma 3 (the read set).** For each live transaction $T$, at each moment between its operations, each entry $(s, ver)$ of its read set satisfies $ver \le ub_T$, and for each word $a$ of stripe $s$ that $T$ read through L3, the value that $T$ read equals $S(ub_T)[a]$. Moreover, for each stripe $s$ that $T$ owns, the words of $s$ that $T$ has not written hold $S(ub_T)$ on $s$.

*Proof.* By induction on the steps of $T$.

*A read through L3 to L8.* The lock sample $l_1 = (ver, \text{FREE})$ equals the sample $l_2$. If any transaction wrote a word of $s$ between the two samples, it owned $s$ then, so at $l_2$ the lock was owned, or released with a larger version (Lemma 1c); either way $l_2 \ne l_1$. So the load returned the value of $a$ at the time of $l_1$, which is $S(ver)[a]$ by Lemma 2. After L5, $ver \le ub_T$, and $ub_T$ was read from the clock before L3. An effective writer of $s$ with $wv$ in $(ver, ub_T]$ drew its $wv$ before $ub_T$ was read and took $s$ before that, so at $l_1$ it either owned $s$ (not FREE) or had released it with a version at least $wv > ver$; both contradict $l_1$. So $S(ver)[a] = S(ub_T)[a]$.

*An extension (L12 to L14).* Let $now$ be the clock read at L12, at time $t$. VALIDATE checks, after $t$, that each entry $(s, ver)$ is still FREE with version $ver$, or is owned by $T$, which took it at version $ver$. An effective writer of $s$ with $wv$ in $(ver, now]$ drew $wv$ before $t$ and took $s$ before that; at the check it would still own $s$ or would have raised its version, which the check excludes (if $T$ owns $s$, it took $s$ at version $ver$, so the other writer must have released before, with version at least $wv > ver$, a contradiction). So $S(now)$ agrees with $S(ver)$, hence with $S(ub_T)$, on each word that $T$ read, and setting $ub_T = now$ keeps the claim. For an owned stripe, no one else wrote it since $T$ took it at a version $v_0 \le ub_T$, and the same argument gives $S(now) = S(v_0)$ on its words.

*A write (L9 to L11).* If $T$ takes $s$ at version $v_0 > ub_T$, it must extend (or abort) at L10; after the extension $ub_T = now \ge v_0$, and no other effective writer of $s$ can have $wv$ in $(v_0, now]$, because $T$ owns $s$ from before $now$ was read. So the words of $s$ hold $S(ub_T)$ on $s$. A read of an owned stripe at L2 returns the own write or a word that holds $S(ub_T)$ by this claim. $\square$

**Lemma 4 (commit).** If $T$ is effective, then each value that $T$ read through L3 equals the value in $S(wv_T - 1)$, and the words of its owned stripes that it did not write hold $S(wv_T - 1)$.

*Proof.* If $ub_T = wv_T - 1$, this is Lemma 3, since $S(ub_T) = S(wv_T - 1)$. Otherwise VALIDATE at L17 runs after the FAA of $T$, and the argument of the extension case applies with $now$ replaced by $wv_T - 1$: an effective writer with $wv$ in $(ver, wv_T)$ drew $wv$ before the FAA of $T$, so before the check, and the check excludes it. $\square$

**Theorem (opacity).** Each finite history of TinySTM, in write-back or write-through mode, is opaque.

*Proof.* Complete the history: effective transactions without a commit event are completed as committed, and the other live or commit-pending transactions as aborted. Place each effective $T$ at position $wv_T$, and every other $T$ at $ub_T + \tfrac12$, with its final $ub_T$; break ties by the time of L1.

*Legality.* Only effective transactions take effect in the serial run, so the state before an effective $T$ is $S(wv_T - 1)$, and the state at $ub + \tfrac12$ is $S(ub)$. A read of a word that $T$ itself wrote returns its own last write: in write-back mode from W, in write-through mode from memory, which no other transaction can change while $T$ owns the stripe. Every other read returns a value of $S(ub_T)$ by Lemma 3, and, if $T$ is effective, of $S(wv_T - 1)$ by Lemma 4. A read of another transaction never returns a value that a write-through transaction wrote in place and later undid: such a value exists only while its writer owns the lock, and the reader's two samples then differ or show an owner (Lemma 1c). The read that ends in ABORT returns no value.

*Real-time order.* Let $T$ complete before $U$ begins. Every value of $ub_U$ and $wv_U$ comes from a clock read after $U$ began. If $T$ is effective, then $wv_T \le ub_U < wv_U$ for the first $ub_U$, and $ub_U$ only grows. If $T$ is not effective, its final $ub_T$ is a clock value read before $T$ completed, so $ub_T \le ub_U$, and $wv_U > ub_T$; a tie between non-effective transactions is broken by L1, where $T$ comes first.

So the completed history is equivalent to a legal serial history that respects real-time order. $\blacksquare$
