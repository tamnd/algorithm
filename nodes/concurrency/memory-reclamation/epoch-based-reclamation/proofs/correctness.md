---
title: Epoch-based reclamation never frees a node that an active operation may still access, and frees every retired node when no operation runs forever
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent shared memory with atomic reads, writes and compare-and-swap. The shared word $G$ is the global epoch, and $A[p]$ is the announcement of process $p$, either $\bot$ or an epoch. We use the lines L1 to L10 of the page. An *operation* of $p$ runs from the end of its BEGIN (the read at L3 that returns, at a time $t_3$) to its END (the write at L4, at a time $t_4$). The client follows three rules.

1. **Access inside an operation.** A process accesses a node only between $t_3$ and $t_4$ of one of its operations, and only a node that was not retired before $t_3$.
2. **Retire after unlink.** A process calls RETIRE($x$) once per allocation of $x$, after the step that removed the last link to $x$, and inside an operation.
3. **No resurrection.** A retired node is not linked again before it is freed.

For the [Treiber stack](/treiber-stack/) and the [Michael and Scott queue](/michael-scott-queue/), rule 1 holds because every node that an operation reads is reached from a root or from the queue head inside the operation, and a node reached in this way was linked at some time after $t_3$.

**Lemma 1 (monotone epoch).** $G$ only grows, by one at a time.

*Proof.* The only write to $G$ is the compare-and-swap at L8, which replaces $e$ by $e + 1$. $\square$

**Lemma 2 (an active operation holds the epoch).** Let an operation of $p$ announce $e$, so that $A[p] = e$ is written at L2 at a time $t_2$ and the read at L3 at time $t_3 > t_2$ returns $G = e$. Then $G \le e + 1$ at every time in $[t_3, t_4]$.

*Proof.* By Lemma 1, $G$ goes above $e + 1$ only through a successful compare-and-swap at L8 from $e + 1$ to $e + 2$, by some process $q$ at a time $t_c$. That attempt read $G = e + 1$ at L6 at a time $t_6 < t_c$, and it read $A[p]$ at L7 at a time $t_7$ with $t_6 < t_7 < t_c$. Since $G = e$ at $t_3$ and $G = e + 1$ at $t_6$, Lemma 1 gives $t_3 < t_6$, so $t_2 < t_7$. If $t_7 < t_4$, then $A[p] = e$ at $t_7$, because $p$ writes $A[p]$ only at L2 and L4. Then L7 sees $A[p] \ne \bot$ and $A[p] \ne e + 1$, and the attempt returns without the compare-and-swap, a contradiction. So $t_c > t_7 > t_4$. $\square$

**Lemma 3 (the tag is late enough).** If RETIRE($x$) runs at L5 inside an operation of $q$ and reads $G = r$, and if $x$ is accessed by an operation of $p$ that announced $e$, then $r \ge e$.

*Proof.* By rule 1 the access is to a node not retired before $t_3$ of $p$, so the retire of $x$, and hence its read at L5, comes after $t_3$, when $G = e$. By Lemma 1, $r \ge e$. $\square$

**Theorem 1 (safety).** No process accesses a node after it is freed.

*Proof.* Let $p$ access $x$ at a time $t$ in an operation that announced $e$, so $t_3 \le t \le t_4$. Suppose the incarnation of $x$ that $p$ accesses is freed at L10 by $q$ at a time $t_f$. $q$ freed it because the test at L9 found $g \ge r + 2$, where $r$ is the tag of $x$ and $g$ is a value of $G$ that $q$ read or wrote at L6 or L8 at a time $t_g < t_f$. By Lemma 3, $g \ge e + 2$. By Lemma 2, $G \le e + 1$ during $[t_3, t_4]$, and $G = e$ at $t_3$, so $t_g > t_4 \ge t$. Hence $t_f > t$, and the access comes before the free. $\square$

**Theorem 2 (no double free).** A node is freed at most once per incarnation.

*Proof.* A node enters the limbo list of the process that retired it, once per incarnation by rule 2, and L10 removes it from the list when it frees it. $\square$

**Theorem 3 (progress).** If from some time on no operation lasts forever, and some process keeps retiring nodes, then every retired node is freed eventually.

*Proof.* Let $G = e$ at some time. Each operation that is active then ends, and every later operation announces a value read from $G$. While $G = e$, every operation that begins later announces $e$. So after all operations that were active at the first time have ended, every attempt at L6 to L8 that reads $G = e$ sees only $\bot$ or $e$ at L7 and tries the compare-and-swap; either it succeeds or another process advanced $G$. Hence $G$ grows without bound. A node with tag $r$ in the limbo list of $q$ is freed at the first scan of $q$ that sees $G \ge r + 2$. $\square$

**Theorem 4 (no bound under a stall).** If one process stops forever inside an operation, $G$ grows by at most one more, and no node retired after that is ever freed.

*Proof.* Let the stopped operation announce $e$. By Lemma 2, $G \le e + 1$ forever. A node retired later has tag $r \ge e$, and it would need $G \ge r + 2 \ge e + 2$. $\square$

Theorems 1 to 3 give the correctness of the method, and Theorem 4 shows why it is not robust. $\blacksquare$
