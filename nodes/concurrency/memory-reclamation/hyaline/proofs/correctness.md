---
title: Hyaline-1 and Hyaline-1S free each batch once, never while a process that may use it is still inside its operation, and Hyaline-1S bounds what a stopped process holds back
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent shared memory with atomic reads, writes, swap, fetch-and-add and compare-and-swap. Process $q$ owns slot $q$ with a head word $H[q] = (HRef, HPtr)$ and, in Hyaline-1S, an access era $A[q]$. A batch $\beta$ is a set of $n + 1$ retired nodes: one counter node $ref_\beta$ with the field $NRef$, and $n$ list nodes, one for each slot. We use the lines L1 to L12 of the page. The client follows three rules.

1. **Use only inside an operation.** A process accesses a node $x$ only between its L1 and its next L5, and only if $x$ was reachable from a root at the read that returned it. In Hyaline-1S that read is a call of PROTECT (L2 to L4). The client makes sure that $x$ was reachable: the stack reads $x$ from the root, and the dequeue reads the head again before it uses $head.next$.
2. **Retire after unlink.** RETIRE($x$) is called once per allocation of $x$, after the step that removed the last link to $x$.
3. **No resurrection.** A retired node is not linked again before it is freed.

Only process $q$ writes $HRef$ of $H[q]$: it sets it to 1 at L1 and to 0 at L5. A retiring process changes only $HPtr$, with the CAS at L11, which keeps $HRef$.

**Lemma 1 (each insert is matched by one decrement, after the owner leaves).** If a list node $y$ of batch $\beta$ is put into $H[q]$ at L11, then $y$ is in the list that $q$ takes with the swap at its next L5, and $q$ subtracts 1 from $NRef$ of $\beta$ once for it at L7, after that swap. No other step subtracts from $NRef$ of $\beta$ for $y$.

*Proof.* The CAS at L11 succeeded on a head with $HRef = 1$, so it is after the L1 of the current operation of $q$ and before its next L5. Later inserts put new nodes in front and link to the old head through $blink$, which is written before the CAS. So the swap at L5 returns a list that contains $y$. The walk at L6 and L7 visits each node of the list once. The list node $y$ belongs to one slot, so no other walk visits it. $\square$

**Lemma 2 (one free per batch).** Let $I$ be the number of successful inserts of $\beta$. Exactly one step frees $\beta$, and it is after the add at L12 and after all $I$ decrements.

*Proof.* $NRef$ starts at 0. Before the add, it holds minus the number of decrements done, which is at most 0, so no decrement returns 1 and none frees. The add at L12 sets it to $I - d$, where $d \le I$ by Lemma 1, and it frees exactly when $d = I$. If $d < I$, each later decrement lowers it by 1, and the decrement that returns 1 is the last of the $I$ decrements; it frees. In both cases exactly one step sees the value that makes the count 0 after the add. $\square$

**Theorem 1 (safety of Hyaline-1).** No process accesses a node after it is freed, and no node is freed twice.

*Proof.* Let $q$ access $x$ at time $t$, inside an operation that started with L1 at time $t_e$, and let $x$ be in batch $\beta$. By rule 1, $x$ was reachable at a read at time $t_1$ with $t_e < t_1 < t$, so by rules 2 and 3, the retire of $x$ and so the loop for slot $q$ at L8 start after $t_1$. In that loop, each read of $H[q]$ at L9 that comes before the next L5 of $q$ sees $HRef = 1$. The loop for slot $q$ ends in one of two ways. (a) The CAS at L11 succeeds before the L5 of $q$. Then by Lemma 1, $q$ decrements for $\beta$ only after its L5, which is after $t$, and by Lemma 2, $\beta$ is freed only after that decrement. (b) The read at L9 sees $HRef = 0$. That read is after the L5 of $q$, so after $t$, and the free comes after the add at L12, after that. In both cases the free is after $t$. Lemma 2 gives one free per batch, and each node is in one batch per incarnation by rule 2. $\square$

**Theorem 2 (safety of Hyaline-1S).** The same holds for Hyaline-1S.

*Proof.* The only new case is a skip at L10. Let $q$ access $x$ in $\beta$ at time $t$ as above, where PROTECT returned $x$ after the read of $x$ at L2 at time $t_1$. As in hazard eras, the value $e$ in $A[q]$ was written before $t_1$, after a read of the era that gave $e$, and the era equals $e$ at the check after $t_1$. The era never decreases, so it was $e$ at $t_1$. The node $x$ was reachable at $t_1$, so it was allocated before $t_1$, and its birth era $b_x \le e$. The value in $A[q]$ only grows, since each write stores a value of the era read after the last one. The read of $A[q]$ at L10 for $\beta$ is after the retire of $x$, so after $t_1$, and it returns at least $e \ge b_x \ge \min_{y \in \beta} b_y$. So L10 does not skip slot $q$, and the proof of Theorem 1 applies. $\square$

**Theorem 3 (bound for Hyaline-1S).** Let process $q$ stop for good with access era $a$. Then the batches that $q$ holds back each contain a node born at or before $a$. If at most $B$ nodes are born at or before $a$, $q$ holds back at most $B$ batches, that is at most $(n + 1) B$ nodes, however long the others run. Besides these, each process has at most $n$ nodes in its unfinished batch.

*Proof.* A batch is held back by $q$ only if it was inserted into $H[q]$. The insert happened after a read of $A[q]$ at L10 that returned a value at least the minimum birth era of the batch. Since $A[q]$ only grows and is $a$ at the end, that minimum is at most $a$, so the batch has a node born at or before $a$. Different batches have different nodes, so there are at most $B$ of them. A batch that is not inserted into $H[q]$ does not wait for $q$, by Lemma 2. $\square$

The other running processes also hold batches until they leave. The number of these depends on how many retires happen during one operation, which the client controls. In Hyaline-1, without L10, a stopped process holds back every batch retired after its L1, so the garbage grows without bound.

**Theorem 4 (cost).** L1 is one write and L5 is one swap, both wait free. L5 to L7 cost 3 steps per batch in the list. RETIRE costs $O(n)$ steps per batch of $n + 1$ nodes, plus the retries of the CAS at L11, which fail only when another process inserted into the same slot or the owner left. PROTECT in Hyaline-1S is lock free, as in hazard eras. $\square$

Theorems 1 to 4 give the correctness of the method. $\blacksquare$
