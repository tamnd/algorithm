---
title: QSBR never frees a node that a process may still access, and frees every retired node when all processes keep passing quiescent states
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent shared memory with atomic reads, writes and compare-and-swap. The shared word $G$ is the global counter, and $C[p]$ is the counter of process $p$, the value of $G$ that $p$ read at its last quiescent state. At the start $G = 0$ and $C[p] = 0$ for every $p$; we treat time 0 as a quiescent state of every process. We use the lines L1 to L8 of the page. A *quiescent state* of $p$ is a call of QUIESCENT, made of the read at L1 at a time $t_1$ and the write at L2 at a time $t_2 > t_1$. The client follows three rules.

1. **No reference across a quiescent state.** If $p$ accesses a node $x$ at a time $t$, and the last quiescent state of $p$ before $t$ wrote $C[p]$ at time $t_2$, then $x$ was not retired before $t_2$.
2. **Retire after unlink.** A process calls RETIRE($x$) once per allocation of $x$, after the step that removed the last link to $x$.
3. **No resurrection.** A retired node is not linked again before it is freed.

For the [Treiber stack](/treiber-stack/) and the [Michael and Scott queue](/michael-scott-queue/) with a quiescent state after each operation, rule 1 holds: inside one operation a process reads only nodes that it reached from a root inside that operation, and such a node was linked after the previous quiescent state.

**Lemma 1 (monotone counter).** $G$ only grows, by one at a time, and $C[p] \le G$ at all times.

*Proof.* The only write to $G$ is the compare-and-swap at L6 from $e$ to $e + 1$. $C[p]$ is written at L2 with a value of $G$ read earlier at L1, and $G$ does not decrease. $\square$

**Lemma 2 (a process between quiescent states holds the counter).** Let the last quiescent state of $p$ before a time $t$ read $G = e$ at L1 at time $t_1$ and write $C[p] = e$ at L2 at time $t_2 \le t$. Then $G \le e + 1$ at every time in $[t_1, t]$, and $G \ge e$ at $t_2$.

*Proof.* The second claim follows from Lemma 1 and $t_1 < t_2$. For the first, $G$ goes from $f$ to $f + 1$ only after an attempt reads $G = f$ at L4 and then reads $C[p] = f$ at L5. Consider the first time in $[t_1, t]$ when $G$ becomes $e + 2$, by a compare-and-swap from $e + 1$ at a time $t_c$. Its read of $C[p]$ at L5 came after its read of $G = e + 1$ at L4, which came after $t_1$ (where $G = e$). Between $t_1$ and $t$, $C[p]$ holds its value before $t_2$ and then $e$. Before $t_2$, $C[p]$ is the value written by an earlier quiescent state, read from $G$ before $t_1$, so by Lemma 1 it is at most $e$. So the read at L5 returned a value at most $e$, not $e + 1$, and the attempt fails. Hence $G \le e + 1$ in $[t_1, t]$. $\square$

**Theorem 1 (safety).** No process accesses a node after it is freed.

*Proof.* Let $p$ access $x$ at a time $t$, and let $t_1 < t_2 \le t$ and $e$ be as in Lemma 2 for the last quiescent state of $p$ before $t$. By rule 1, $x$ was retired after $t_2$, so its tag $r$, read at L3 after the retire, is at least $G(t_2) \ge e$. Suppose that $q$ frees this incarnation of $x$ at L8 at a time $t_f$. The test at L7 found $g \ge r + 2 \ge e + 2$, where $g$ is a value of $G$ that $q$ read or wrote at L4 or L6 at a time $t_g < t_f$. Since $G(t_1) = e$, Lemma 1 gives $t_g > t_1$, and Lemma 2 gives $t_g > t$. So $t_f > t$. $\square$

**Theorem 2 (no double free).** A node is freed at most once per incarnation.

*Proof.* It enters the limbo list of the process that retired it once per incarnation (rule 2), and L8 removes it when it frees it. $\square$

**Theorem 3 (progress).** If every process passes a quiescent state infinitely often, and some process keeps retiring nodes, then every retired node is freed eventually.

*Proof.* Let $G = e$ at some time. Each process then passes a quiescent state, and while $G = e$ it writes $C[p] = e$. After all of them have done so, an attempt that reads $G = e$ at L4 sees $C[q] = e$ for all $q$ and tries the compare-and-swap; either it succeeds or $G$ has already moved. So $G$ grows without bound, and a node with tag $r$ is freed at the first attempt of its owner that sees $G \ge r + 2$. $\square$

**Theorem 4 (no bound under a stall).** If one process stops forever, or stops passing quiescent states, then $G$ grows by at most one more, and no node retired after that is ever freed.

*Proof.* Let its last write be $C[p] = e$. By the argument of Lemma 2, $G \le e + 1$ forever. A later node has a tag $r \ge e$ and needs $G \ge e + 2$. $\square$

Theorems 1 to 3 give the correctness of the method, and Theorem 4 shows why it is not robust. $\blacksquare$
