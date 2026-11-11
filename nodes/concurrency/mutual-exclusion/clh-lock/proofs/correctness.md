---
title: The CLH lock gives mutual exclusion, FIFO order and starvation freedom, with at most 5 remote references per passage in the CC model
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent memory, with $n + 1$ nodes that each have one atomic flag $locked$. $tail$ supports atomic fetch-and-store (swap). At the start process $p$ owns node $p$ as $my$, every flag is false, and $tail$ points to node $n$. We use the lines L1 to L5 of the page. L5 is a local step, so we treat L4 and L5 as one step. Critical sections are finite, and a fair run gives infinitely many steps to every process that is not in its remainder section.

**The queue.** Let $Q$ be the sequence of processes that have done L2 and not yet L4, in the order of their L2 steps. Its first process is the *head*.

**Lemma 1 (invariant).** At every time:

1. The nodes $my_p$ of the $n$ processes are distinct. The one other node is called the *gate*, and its flag is false.
2. If $Q$ is empty, $tail$ points to the gate. If $Q = (p_1, \ldots, p_k)$ with $k \ge 1$, then $tail$ points to $my_{p_k}$, $pred_{p_1}$ is the gate, and $pred_{p_i} = my_{p_{i - 1}}$ for $2 \le i \le k$.
3. For every process $p$ that has done L1 and not yet L4, $my_p.locked$ is true.
4. No process reads or writes the node $my_p$ of a process $p$ that is not in $Q$, except $p$ itself and, if $p$ has just left $Q$, nobody.

*Proof.* By induction on the steps. At the start the nodes $0, \ldots, n - 1$ are owned, node $n$ is the gate with flag false, $Q$ is empty and $tail$ points to node $n$.

- *L1 of $p$.* $p$ is not in $Q$, so by part 4 nobody else uses $my_p$. The write makes part 3 hold for $p$, and does not touch the gate or a node that a process in $Q$ reads.
- *L2 of $p$.* The swap returns the old $tail$ and writes $my_p$. If $Q$ was empty, the old $tail$ was the gate, so $pred_p$ is the gate and $Q = (p)$. Otherwise the old $tail$ was $my_{p_k}$, so $pred_p = my_{p_k}$ and $p$ joins as $p_{k + 1}$. Part 2 holds, and $tail$ now points to $my_p$.
- *A read of L3* changes nothing.
- *L4 and L5 of $p$.* Only a process past L3 runs L4, and by Lemma 2 below (which uses the invariant before this step) that process is the head $p_1$. It writes false to $my_{p_1}$ and sets $my_{p_1} \leftarrow pred_{p_1}$, which is the gate. Now $p_1$ leaves $Q$. Its old node has flag false and becomes the new gate: if $k = 1$, $tail$ points to it, and if $k \ge 2$, it is $pred_{p_2}$, and $p_2$ is the new head. The old gate is now owned by $p_1$; nobody else reads it, since only $p_1$ had it as $pred$. So all four parts hold. $\square$

**Lemma 2 (only the head passes L3).** If a process $p$ reads false at L3, then $p$ is the head of $Q$.

*Proof.* $p$ is in $Q$, say $p = p_i$. If $i \ge 2$, then $pred_p = my_{p_{i - 1}}$, and $p_{i - 1}$ has done L1 and not L4, so the flag is true by part 3 of Lemma 1. So a read of false means $i = 1$. $\square$

**Lemma 3 (mutual exclusion).** At most one process is in its critical section at any time.

*Proof.* A process in its critical section has passed L3 and not done L4, so it is in $Q$, and it was the head when it passed L3 (Lemma 2). It stays the head until its own L4, since only the head leaves $Q$. $Q$ has one head. $\square$

**Lemma 4 (FIFO order).** Processes enter in the order of their L2 steps.

*Proof.* Only the head enters (Lemma 2), and the head leaves $Q$ only at its L4, after which the next process in L2 order is the head. $\square$

**Lemma 5 (starvation freedom).** In a fair run, every process that does L2 enters its critical section.

*Proof.* The head $p_1$ has the gate as $pred$, whose flag is false by part 1 of Lemma 1, and only the next L4 can change which node is the gate. So the next read of L3 by $p_1$ returns false, and $p_1$ enters, leaves after a finite critical section, and runs L4. Then $p_2$ is the head. By induction along $Q$, every process in $Q$ enters. $\square$

**Lemma 6 (remote references in the CC model).** A passage makes at most 5 remote references in the CC model.

*Proof.* L1, L2 and L4 are at most one RMR each. Let $p$ wait on the node $x = pred_p$. Which steps write $x$ between the L2 of $p$ and its last read of L3? If $x$ is the gate, nobody writes it (it is written only by an L1 of its owner, and it has no owner while it is the gate). Otherwise $x = my_q$ for the process $q$ just before $p$ in $Q$; $q$ did L1 before its L2, which came before the L2 of $p$, so the only later write is the L4 of $q$. So the reads of L3 miss at most twice: at the first read and after that L4. The total is at most $3 + 2 = 5$. $\square$

**Lemma 7 (DSM model).** In the DSM model, with node $i$ in the module of process $i$ for $i < n$, a passage has no bound on its remote references.

*Proof.* Let process 0 do L1 and L2 and enter, and then let process 1 do L1 and L2. Then $pred_1 = my_0$, which is node 0, in the module of process 0. Let process 0 stay in its critical section while process 1 takes any number $m$ of steps. Each of them is a read of node 0 at L3, which is remote for process 1, so the passage of process 1 makes at least $m$ remote references. The test file finds an unbounded passage for two processes. (Spinning on the own node would need a pointer from the predecessor to the successor, which is what the MCS lock adds.) $\square$

Lemmas 3, 4 and 5 show that the CLH lock solves the mutual exclusion problem with FIFO order and starvation freedom, and Lemmas 6 and 7 give its RMR costs. $\blacksquare$
