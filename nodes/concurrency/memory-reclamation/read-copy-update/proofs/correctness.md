---
title: Correctness of read-copy-update with a global counter
proves: [correctness]
status: full
---

We prove that the template frees a version only when no reader can still use it, and that readers never wait. We then state what happens when a reader stops.

**Model.** Processes run asynchronously on a sequentially consistent shared memory. $G$ is an integer that starts at 1 and is changed only at L6, by a fetch-and-add of 1, so it never decreases. $R[t]$ is written only by reader $t$: at L2 with a value it read from $G$, and at L3 with 0. Updaters exclude each other, so the steps of one UPDATE are in the order old, L8, L9, L6, L7, L10, and two updates do not overlap. A read-side section of $t$ is the time from its L2 to its next L3. The rules for readers are: a reader uses a pointer that it read at L4 only inside the same section, and it reaches a version only through $cfg$.

**Lemma 1.** If reader $q$ reads the version $A$ at L4 in a section $S$, and the update that replaces $A$ writes $cfg$ at time $t_9$, then the read at L4 came before $t_9$, and the value $s$ that $q$ wrote at L2 in $S$ satisfies $1 \le s \le g - 1$, where $g$ is the value computed at L6 of that update.

*Proof.* Each version is a new allocation that is published once, at the L9 of the update that made it, and it stays in $cfg$ until the next L9, which is $t_9$ for $A$. (A later version can get the address of $A$ after $A$ is freed, but it is a different version.) So the read at L4 that returned $A$ came before $t_9$. In $S$, L1 comes before L2, which comes before L4, so $q$ read $G$ at L1 before $t_9$, and so before the L6 of this update. $G$ starts at 1 and does not decrease, so $s \ge 1$. Just before the L6 of this update, $G = g - 1$, and $q$ read $G$ earlier, so $s \le g - 1$. $\square$

**Lemma 2 (the grace period).** Let the updater finish its wait for $q$ at L7 by reading $R[q]$ at time $\tau$, with $R[q] = 0$ or $R[q] \ge g$. Then every section of $q$ in which $q$ read the old version $A$ ended before $\tau$.

*Proof.* Let $S$ be such a section, with the value $s$ written at its L2. By Lemma 1, $s \le g - 1$, and the read at L4 in $S$ came before $t_9 < \tau$. Look at the value of $R[q]$ at $\tau$, and suppose that $S$ had not ended at $\tau$. If the L2 of $S$ came before $\tau$, then $R[q] = s$ at $\tau$, because only $q$ writes $R[q]$ and its next write is the L3 that ends $S$. But $s \ne 0$ and $s < g$, so the wait would not end. If the L2 of $S$ came after $\tau$, then the L4 of $S$ came after $\tau > t_9$, which contradicts Lemma 1. So $S$ ended before $\tau$. $\square$

**Theorem 1 (safety).** No reader accesses a version after it is freed.

*Proof.* An updater frees the old version $A$ at L10, after L7 ended for every reader $q$. By Lemma 2, every section in which $q$ read $A$ ended before that. By the rules, $q$ uses $A$ only inside such a section. A section of $q$ that starts later reads $cfg$ after $t_9$, so by Lemma 1 it does not read $A$. So after L10, no reader uses $A$. $\square$

**Theorem 2 (readers do not wait).** READ-LOCK, READ-UNLOCK and READER finish in a fixed number of their own steps, whatever the other processes do.

*Proof.* They contain no loop and no wait: L1 to L5 are single reads and writes. $\square$

**Theorem 3 (progress of updates).** If every read-side section ends, every SYNCHRONIZE ends.

*Proof.* L7 waits for each $q$ in turn. While $q$ is in a section, the section ends, and then $R[q] = 0$ until $q$ starts a new section, which writes a value read from $G$ after L6, so at least $g$. Either way the condition holds at some read of the updater. With a fair scheduler, the updater makes that read. $\square$

**Remark (a stopped reader).** If a reader stops forever inside a section that began before an update's L6, then by Lemma 2 that update's L7 never ends. In the synchronous form the updater blocks, and the garbage stays at one version per waiting updater. In the deferred form (call_rcu), updaters do not wait, but no batch that was retired after the reader stopped can ever pass its check, so the unfreed versions grow with the number of updates. The tests show both cases.

**The stack and the queue.** The scheme class runs each operation of the Treiber stack or the Michael and Scott queue as one read-side section, retires the removed node after its CAS, and runs SYNCHRONIZE after its own READ-UNLOCK. A process that starts a section after the removal CAS cannot reach the removed node from the root, which plays the part of Lemma 1. The rest of the proof is the same, with "the update" replaced by "the removal CAS" and $t_9$ by the time of that CAS. Several updaters may run at once here, so $G$ can grow by more than 1 between L1 and L6; Lemma 1 still holds, because it only needs $s \le g - 1$, and the condition at L7 accepts any value of at least $g$. $\blacksquare$
