---
title: Correctness of Fischer's algorithm
proves: [correctness]
status: full
---

This proof shows mutual exclusion when $D > \Delta$, deadlock freedom, and a run in which a process starves.

**Model.** A run is a sequence of atomic steps, and each step is one read or one write of the register $x$ by one process. Each step has a real time, and the times do not decrease along the sequence. Several steps can have the same time; then they happen in the order of the sequence. The processes have the names $1, \ldots, n$. The timing assumptions are:

- (T1) a process that reads $x = 0$ at L2 writes $x \leftarrow i$ at L3 at most $\Delta$ time units later;
- (T2) a process that writes $x$ at L3 reads $x$ at L5 at least $D$ time units later;
- (T3) every step other than a step in the remainder or the critical section comes at most a finite time after the step before it of the same process, and each critical section ends after a finite time.

We write "before" and "after" for the order of the sequence, and $\tau(e)$ for the time of a step $e$. If $e$ is before $f$, then $\tau(e) \le \tau(f)$.

## Facts

- (F1) Only L6 writes 0 to $x$, and a process does L6 only right after its critical section.
- (F2) Only process $p$ writes the value $p$, and it writes $x$ at most once in a round of the loop. So if $p$ writes $x$ at the step $w$ and reads $x = p$ at the step $c$ of the same round, then no process writes $x$ between $w$ and $c$.

## Theorem 1 (mutual exclusion)

*If $D > \Delta$, then at no point of a run are two processes in the critical section.*

*Proof.* Suppose not, and take the first step $c_q$ after which two processes are in the critical section. It is the check at L5 by which some process $q$ enters, while some process $p \ne q$ is in the critical section. Let $c_p$ be the check by which $p$ entered; it is before $c_q$. Let $r_p, w_p$ and $r_q, w_q$ be the read of $x = 0$ at L2 and the write at L3 in the round in which $p$ and $q$ enter. So $r_p$ is before $w_p$, which is before $c_p$, and the same holds for $q$.

*Step 1: $w_q$ is after $c_p$.* By F2, no write of $x$ is between $w_p$ and $c_p$, and none is between $w_q$ and $c_q$. If $w_q$ were before $w_p$, then $w_p$ would be between $w_q$ and $c_q$, since $w_p$ is before $c_p$ and $c_p$ is before $c_q$. This is not possible, so $w_q$ is after $w_p$. Since $w_q$ is not between $w_p$ and $c_p$, it is after $c_p$.

*Step 2: $x \ne 0$ from $w_p$ to $c_q$.* From $w_p$ to $c_p$, $x = p$ by F2. After $c_p$ and before $c_q$, process $p$ is in the critical section. A write of 0 in this part is an L6 by a process $z$ that was in the critical section right before it, by F1. Then $z \ne p$, and $z$ and $p$ were both in the critical section before $c_q$. This is against the choice of $c_q$. So no write of 0 happens from $w_p$ to $c_q$.

*Step 3: the times.* Process $q$ reads $x = 0$ at $r_q$, which is before $w_q$ and so before $c_q$. By Step 2, $r_q$ is before $w_p$. Then

$$\tau(w_q) \le \tau(r_q) + \Delta \le \tau(w_p) + \Delta < \tau(w_p) + D \le \tau(c_p) \le \tau(w_q).$$

The first inequality is T1, the second holds because $r_q$ is before $w_p$, the third is $D > \Delta$, the fourth is T2, and the last holds because $w_q$ is after $c_p$ by Step 1. This is a contradiction. $\square$

*Remark.* The only strict inequality in the chain is $\Delta < D$. If $D = \Delta$, the chain allows $\tau(w_q) = \tau(c_p)$, that is, $q$ writes $x$ at the same time at which $p$ checks it, but after the check. The test file finds such a run. If no two steps can have the same time, then $\tau(c_p) < \tau(w_q)$ and $D \ge \Delta$ is enough.

## Theorem 2 (deadlock freedom)

*In a run that meets T1 to T3, if some process is in its entry section at some time, then later some process enters the critical section.* This holds for all $D$ and $\Delta$.

*Proof.* Suppose not. Then from some step on, no process enters. Each process in the critical section or in the exit section at that point leaves it after a finite time by T3, so from some step $t_1$ on, no process is in the critical section or in the exit section, and a fixed nonempty set $T$ of processes is in the entry section forever. By F1, no write of 0 happens after $t_1$. By T3, the processes in $T$ take infinitely many steps.

*Case A: $x \ne 0$ at some step $t_2$ after $t_1$.* Then $x \ne 0$ after $t_2$, so each read at L2 after $t_2$ fails. A write at L3 comes right after a read of $x = 0$ at L2 of the same process, so each process writes $x$ at most once after $t_2$. So there is a last write of $x$, by some process $v$. Then $v$ reads $x$ at L5 after this write, by T2 and T3. No write comes in between, so $v$ reads $x = v$ and enters. This is a contradiction.

*Case B: $x = 0$ at each step after $t_1$.* Take a process $u \in T$. If $u$ is at L2, it reads $x = 0$ and then writes $x \leftarrow u \ne 0$ at L3. If it is at L3, it writes $x \leftarrow u$. If it is at L5, it reads $x = 0 \ne u$, goes back to L2, and then reads $x = 0$ and writes $x \leftarrow u$. In each case $x \ne 0$ after some step after $t_1$, which is a contradiction. $\square$

## Theorem 3 (starvation)

*The algorithm is not starvation free, even when $D > \Delta$.*

*Proof.* Take $n = 2$, $\Delta = 1$ and $D = 2$. Let $S$ be the state at a time $t$ in which process 1 is in the critical section, $x = 1$, and process 2 has just read $x = 1 \ne 2$ at L5 and is back at L2. Then:

1. at time $t$, process 1 leaves the critical section, writes $x \leftarrow 0$, starts its entry section again and reads $x = 0$ at L2;
2. at time $t + 1$, process 2 reads $x = 0$ at L2 and writes $x \leftarrow 2$; then, at the same time, process 1 writes $x \leftarrow 1$, which is 1 time unit after its read;
3. at time $t + 3$, process 2 reads $x = 1 \ne 2$ at L5 and goes back to L2; then process 1 reads $x = 1$ at L5 and enters.

Each step meets T1 and T2: both writes are at most 1 time unit after the reads, and both checks are 2 time units after the writes. The state at time $t + 3$ is $S$ again. Both processes take steps in each round, so repeating the round forever gives a run that meets T1 to T3 in which process 2 never enters. The test file replays this run for five rounds and checks that each round ends in the same state. $\blacksquare$
