---
title: The C-BO-MCS cohort lock gives mutual exclusion and deadlock freedom, and passes locally at most B times in a row
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent memory. Each process $p$ belongs to one NUMA node $c(p)$ and owns one MCS node with the fields $next$ and $state$. $G$ is a test-and-set bit, false at the start. For each node $c$, $tail[c]$ supports swap and compare-and-swap and is $nil$ at the start, and $count[c]$ is a register. We use the lines L1 to L9 of the page; `GLOBAL-ACQUIRE` repeats a read of $G$ until it is false, a TAS, and a finite backoff, until a TAS returns false. Critical sections are finite, and a fair run gives infinitely many steps to every process that is not in its remainder section.

**Local queues.** For each node $c$, let $Q_c$ be the sequence of processes of node $c$ that joined at L2 and have not yet left, in the order of their L2 steps. A process leaves $Q_c$ at its write $succ.state \leftarrow GLOBAL$ at L7, at its write $succ.state \leftarrow ACQ$ at the end of L9, or at its successful compare-and-swap at L9. The first process of $Q_c$ is its *head*.

The entry and exit sections on $tail[c]$ and the $next$ fields are those of the [MCS lock](/mcs-lock/), with "$state \ne WAIT$" in place of "$locked = false$", and with one write to the successor in each exit section that has a successor. The extra test $tail[c] \ne I$ at L6 only makes the holder wait for a link that the MCS exit section would also wait for. So the invariant of the MCS proof holds for each $Q_c$, by the same induction:

- **(Q1)** $tail[c]$ is the last process of $Q_c$, or $nil$ if $Q_c$ is empty.
- **(Q2)** If $q$ directly follows $p$ in $Q_c$, then $p.next$ is $q$ once $q$ has linked in L3, and $nil$ before. So a value $succ \ne nil$ that $p$ reads at L6 or L9 is the process that follows $p$ in $Q_c$.
- **(Q3)** A process of $Q_c$ other than the head has $state = WAIT$ and waits in L3. Its state is written only by its predecessor, once, when the predecessor leaves $Q_c$. Only the head can be at L4 or later.

**Ownership of $G$.** Call a process the *owner* from its TAS at L4 that returns false, or from the write that sets its state to $GLOBAL$, until its write $succ.state \leftarrow GLOBAL$ at L7 or its write $G \leftarrow$ false at L8.

**Lemma 1 (one owner).** At every time, $G$ is true if and only if there is an owner, and there is at most one owner. Every process in its critical or exit section, before L7 or L8, is the owner.

*Proof.* By induction on the steps. At the start $G$ is false and there is no owner. The steps that matter:

- *A TAS at L4 that returns false.* It happens only when $G$ is false, so by induction there is no owner. Now $G$ is true and the caller is the only owner. It then runs L5 and enters, still the owner.
- *A TAS that returns true* changes nothing.
- *A write $succ.state \leftarrow GLOBAL$ at L7.* It is made by a process in its exit section, which is the owner by induction. Ownership moves to $succ$, and $G$ stays true. By (Q2) and (Q3), $succ$ was waiting in L3 with $state = WAIT$, so it was not the owner before, and it now returns from LOCK and enters as the owner.
- *A write $G \leftarrow$ false at L8.* It is made by the owner, in its exit section. Now $G$ is false and there is no owner.
- *A write $succ.state \leftarrow ACQ$* gives no ownership; the successor goes to L4.

A process enters its critical section only after a winning TAS or after it sees $GLOBAL$ in L3, so it is the owner when it enters, and it stays the owner until its own L7 pass or L8. $\square$

**Lemma 2 (mutual exclusion).** At most one process is in its critical section at any time.

*Proof.* By Lemma 1, each process in its critical section is the owner, and there is at most one owner. $\square$

**Lemma 3 (bounded local passing).** Between two consecutive TAS steps on $G$ that return false, at most $B$ local passes happen, so at most $B + 1$ processes enter.

*Proof.* Let $p_0$ win a TAS on $G$, and let $p_1, \ldots, p_j$ be the processes that get ownership by passes before the next winning TAS. By Lemma 1 they form a chain: $p_{i + 1}$ gets ownership from $p_i$. By (Q2) each pass goes to the successor in the same local queue, so all of them belong to the node $c = c(p_0)$. The register $count[c]$ is written only at L5, right after a winning TAS, and at L7, during a pass; in both cases by the owner. So while $p_0, \ldots, p_j$ own $G$, only they write $count[c]$, one at a time: $p_0$ writes 0 at L5 before it enters, and $p_i$ for $i < j$ reads $count[c] = i$ at L7 and writes $i + 1$. A pass needs the value read to be below $B$, so $j - 1 < B$, which gives $j \le B$. $\square$

**Lemma 4 (deadlock freedom).** In a fair run, if some process is in its entry section at time $t$, then some process enters its critical section after $t$.

*Proof.* Assume that no process enters after $t$. The exit section waits only at L6 and L9, for a process that has done L2 and has not yet linked; that process links after a bounded number of its own steps, since there is no loop between L2 and the link in L3. So every exit section finishes. If the owner at time $t$, if any, passed at L7, its successor would enter. So from some time $t_1$ on there is no owner, and by Lemma 1, $G$ is false from $t_1$ on, because a new owner would enter.

Take a node $c$ with a process in its entry section after $t_1$; then $Q_c$ is not empty. Let $h$ be its head. If $h$ had a predecessor, the predecessor left $Q_c$ by writing $ACQ$ to $h$ (a write of $GLOBAL$ would make $h$ enter), so $h$ leaves L3 and goes to L4; otherwise $h$ got $pred = nil$ and goes to L4 at once. At L4, $h$ reads $G$ false after a finite backoff, and its TAS returns false, unless the TAS of another head comes first. Either way some TAS returns false after $t_1$, and its caller enters. This contradicts the assumption. $\square$

**Lemma 5 (no starvation freedom).** There is a fair run with one process on each of two nodes in which the process on node 0 never enters.

*Proof.* With one process per node, every local queue has at most one process, so no pass happens and every entry needs a winning TAS on $G$. Both processes are heads and run `GLOBAL-ACQUIRE`, which is the TTAS lock with backoff. By Lemma 4 of the [spin lock](/spin-lock/) proof, there is a fair run in which process 1 always takes $G$ again before process 0 tries its TAS on a free $G$. The test file finds this cycle in the state graph for two processes that run forever. Inside one node there is no such run: the local queue is FIFO, and the test file finds no starvation for two processes on one node. $\square$

Lemmas 2 and 4 show that the C-BO-MCS lock solves the mutual exclusion problem with deadlock freedom, Lemma 3 gives the may-pass-local bound of $B + 1$ critical sections per acquisition of $G$, and Lemma 5 shows that the lock is not starvation free with a backoff global lock. $\blacksquare$
