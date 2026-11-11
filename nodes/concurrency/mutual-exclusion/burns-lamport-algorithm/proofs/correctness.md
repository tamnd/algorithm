---
title: Correctness of the Burns-Lamport algorithm
proves: [correctness]
status: full
---

This proof shows mutual exclusion and deadlock freedom, shows that process 0 cannot starve, and gives a run in which process 1 starves.

**Model.** The registers are atomic and the memory is sequentially consistent, so a run is a sequence of steps, and each step is one read or one write of one process. Only process $i$ writes $x[i]$. A run is *fair* if each process that is not in its remainder section takes infinitely many steps, and each process leaves its critical section after a finite time.

**Fact F.** In one passage, process $i$ makes its *last* write of true at L2 at some time $w_i$, and then reads every lower flag false at L3 and L4 without a write of false at L5. So $x[i]$ is true from $w_i$ until the write of false at L10, after the critical section.

## Theorem 1 (mutual exclusion)

*At no time are two processes in the critical section.*

*Proof.* Suppose $p < q$ are both in the critical section at time $t$. By Fact F, $x[p]$ is true on $[w_p, t]$ and $x[q]$ is true on $[w_q, t]$. After $w_q$, process $q$ read $x[p]$ false at L4, at some time $r_q$ with $w_q < r_q < t$. Since $x[p]$ is true on $[w_p, t]$, we get $r_q < w_p$. After $w_p$, process $p$ read $x[q]$ false at L9, at some time $r_p$ with $w_p < r_p < t$. Then $w_q < r_q < w_p < r_p < t$, so $x[q]$ is true at $r_p$. This is a contradiction. $\square$

## Theorem 2 (deadlock freedom)

*In a fair run, if some process is in its entry section at some time, then later some process enters the critical section.*

*Proof.* Suppose not. Then from some time $t_0$ on, no process enters the critical section. A process in its exit section finishes it in one step, and a process that starts its entry section after $t_0$ stays in it forever. So from some time $t_1 \ge t_0$ on, there is a fixed nonempty set $T$ of processes that are in their entry sections forever, and every other process is in its remainder section with its flag false forever.

Let $m$ be the smallest process in $T$. Every flag $x[j]$ with $j < m$ is false after $t_1$. So if $m$ waits at L6, the wait ends, and in its next round $m$ reads every lower flag false and goes on to L8. From then on, $x[m]$ is true forever, since $m$ does not enter.

Call a process *past* if it is at L8 or L9. A past process stays past, because it can only leave L9 by entering. So the set $P$ of past processes only grows, and from some time $t_2$ on it is fixed. It holds $m$. Let $h$ be the largest process in $P$. Process $h$ waits at L9 forever on some flag $x[j]$ with $j > h$. Then $j \in T$, since otherwise $x[j]$ is false forever, and $j \notin P$, since $j > h$.

Process $j$ is never past after $t_2$, so each round of $j$ that starts at L2 after $t_2$ ends at L5 and L6. In such a round, $j$ reads the lower flags in increasing order. Flags below $m$ are false and $x[m]$ is true, so the first true flag that $j$ finds is $x[m]$. So $j$ writes $x[j]$ false and waits at L6 on $x[m]$, which is true forever. The round of $j$ that is in progress at $t_2$ also ends at L6, since $j$ does not become past, and that wait either never ends, or it ends and $j$ starts such a round. In each case, $x[j]$ is false forever from some time on. Then $h$ reads $x[j]$ false, which is a contradiction. $\square$

## Theorem 3 (process 0)

*In a fair run, process 0 does not starve, and after its write of true at L2, at most $n - 1$ other entries come before its own entry.*

*Proof.* Process 0 has no lower process, so it writes true once at time $w_0$ and goes to L8. By Fact F, $x[0]$ is true from $w_0$ until its exit. Let $q \ne 0$ enter after $w_0$ and before 0 enters. In the round in which $q$ enters, it read $x[0]$ false, so that read came before $w_0$. In each later passage, the first read of $q$ at L4 is of $x[0]$, which is true, so $q$ waits at L6 until 0 leaves. So each other process enters at most once in this interval, which gives at most $n - 1$ entries. After them, no other process can enter before 0 does. By Theorem 2, some process enters, so process 0 enters. $\square$

## Theorem 4 (starvation)

*For $n = 2$ there is a fair run in which process 1 is in its entry section forever.*

*Proof.* Start in the state $S$ in which process 0 is in its critical section with $x[0]$ true, and process 1 waits at L6 on $x[0]$ with $x[1]$ false. The example on the page reaches $S$ from the initial state. Now run these steps:

1. Process 0 leaves: it writes $x[0] \leftarrow$ false.
2. Process 1 reads $x[0]$ false at L6 and goes back to L2.
3. Process 0 starts a new passage and writes $x[0] \leftarrow$ true.
4. Process 1 writes $x[1] \leftarrow$ true, reads $x[0]$ true at L4, writes $x[1] \leftarrow$ false and goes to L6.
5. Process 0 reads $x[1]$ false at L9 and enters.

After step 5 the run is in state $S$ again. Repeating these steps forever gives a fair run, since both processes take steps in each round, and process 1 never enters. The test file runs this cycle and checks that it returns to the same state. $\blacksquare$
