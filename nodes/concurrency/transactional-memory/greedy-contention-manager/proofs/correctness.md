---
title: Under Greedy, every transaction commits
proves: [correctness]
status: full
---

**Model.** There are $n$ threads. Each runs transactions one after another; a transaction opens a finite list of objects, one at a time, for exclusive access, and then commits. A step of a thread is one of: restart after an abort; open a free object; call RESOLVE (lines L3 to L6) against the active owner $B$ of the next object and then either abort $B$ and take the object (L4) or set its own waiting flag (L5); commit. Aborting $B$ is a compare-and-swap of the status of $B$ from active to aborted, and it frees all objects of $B$. The scheduler is fair: a thread whose current transaction is not committed takes infinitely many steps. No thread halts. Timestamps are distinct, are taken once per transaction (L1), and are kept on restart (L8). A transaction that begins later than another one, in real time, has a larger timestamp.

At any time, let the **leader** be the transaction with the smallest timestamp among the transactions that have begun and not committed.

**Lemma 1.** A transaction never waits for a younger one: if $A$ executes L5 against $B$, then $\mathrm{ts}(B) < \mathrm{ts}(A)$.

*Proof.* L5 runs only when the test of L3 fails, so $\mathrm{ts}(B) \le \mathrm{ts}(A)$, and $B \ne A$ because $A$ never conflicts with itself. Timestamps are distinct. $\square$

**Lemma 2.** Let $A$ be the leader at time $t$, and let $t' \ge t$ be the time of the first step of $A$ at or after $t$. While $A$ stays the leader, after $t'$, $A$ is never waiting and is never aborted.

*Proof.* We show by induction over the steps after $t'$ that the flag of $A$ is false and the status of $A$ is active after each step.

The step of $A$ at $t'$: if $A$ was aborted before it, the step is a restart and L8 clears the flag. Otherwise the step is an open (L7 clears the flag), a commit (and then $A$ is no longer the leader), or a call of RESOLVE against the active owner $B$ of an object. In the last case, $B$ has begun and is not committed, and $A$ is the leader, so $\mathrm{ts}(B) > \mathrm{ts}(A)$. The test of L3 holds, and $A$ aborts $B$, takes the object, and clears its flag. In each case the flag of $A$ is false after the step, and $A$ is active.

A later step of $A$: for the same reason every enemy of $A$ is younger, so RESOLVE always takes the branch of L4, and by Lemma 1 $A$ never runs L5. Its flag stays false.

A step of another transaction $C$ that aborts $A$: by L3, this needs $\mathrm{ts}(A) > \mathrm{ts}(C)$ or the flag of $A$ to be true. The first is false because $C$ is not committed and $A$ is the leader (a transaction that has not begun cannot take a step), and the second is false by the induction hypothesis. So $C$ does not abort $A$. $\square$

**Lemma 3 (pending commit).** If the leader $A$ opens $\ell$ objects, it commits within $\ell + 2$ of its own steps after it becomes the leader.

*Proof.* By Lemma 2, after its first step as leader, $A$ is never aborted and never waits. Each of its later steps is an open (possibly after aborting the owner, in the same step) or the commit, and the position of $A$ in its list grows by one at each open. So after the first step, at most $\ell$ opens and one commit remain. The first step is a restart, an open or the commit. In all cases $A$ commits within $\ell + 2$ of its own steps. $\square$

**Theorem (no livelock, no starvation).** Every transaction commits.

*Proof.* Take a transaction $A$ that begins at time $t_0$. At $t_0$, at most $n - 1$ other transactions have begun and not committed, one per other thread. Every transaction that begins after $t_0$ has a larger timestamp than $A$. So the set $O$ of transactions that are older than $A$ and could ever be the leader before $A$ commits has at most $n - 1$ members, all running at $t_0$.

While $A$ has not committed, the leader is $A$ or a member of $O$. By Lemma 3 and fairness, the current leader commits after finitely many steps of the whole system: its thread takes a step infinitely often, and it needs at most $\ell + 2$ of them. When it commits, it leaves $O$ for ever (a committed transaction is never the leader again). So after at most $n - 1$ such commits, $O$ has no member that is not committed, and $A$ is the leader. By Lemma 3, $A$ then commits. Since $A$ was arbitrary, every transaction commits: there is no livelock (some transaction always commits after finitely many steps) and no starvation (every transaction commits). $\blacksquare$

**Remark.** The theorem needs three things that the proof uses: timestamps kept across aborts (otherwise $O$ can grow for ever), the waiting rule of L3 (it is what prevents a waiting transaction from blocking a younger one; it is also what lets a leader with a stale flag be aborted once, which the bound $\ell + 2$ allows for), and fairness with no halted thread (a leader whose thread stops never commits, and the others wait for it).
