---
title: Correctness of Lamport's fast mutual exclusion algorithm
proves: [correctness]
status: full
---

This proof shows mutual exclusion and deadlock freedom, and gives a run in which a process starves.

**Model.** The registers are atomic and the memory is sequentially consistent, so a run is a sequence of steps, and each step is one read or one write of one process. Steps happen at distinct times. The processes have the names $1, \ldots, n$, and the value 0 in $y$ means "free". A run is *fair* if each process that is not in its remainder section takes infinitely many steps, and each process leaves its critical section after a finite time.

## Notation

Consider the round of the loop in which process $p$ enters. In it, $p$ writes $b[p] \leftarrow$ true at L2, writes $x \leftarrow p$ at time $a_p$ (L3), reads $y = 0$ at time $r_p$ (L4), and writes $y \leftarrow p$ at time $c_p$ (L8). Then:

- on the *fast path*, $p$ reads $x = p$ at L9 and enters at once;
- on the *slow path*, $p$ reads $x \ne p$ at L9, writes $b[p] \leftarrow$ false at L10, reads each $b[j]$ false at L11, and reads $y = p$ at L12 and enters.

Let $E_p$ be the time of the read that ends the entry section: the read at L9 on the fast path, and the read at L12 on the slow path. Process $p$ is in the critical section from $E_p$ on, and $a_p < r_p < c_p < E_p$.

**Facts.**

- (F1) Only L16 writes 0 to $y$, and a process does L16 only right after its critical section.
- (F2) Only $p$ writes the value $p$ to $x$ or $y$. A read of $x = p$ at time $d$ after the write $a_p$ means that no process writes $x$ in $(a_p, d)$.
- (F3) On the fast path, $b[p]$ is true from L2 of the entering round until L17. On the slow path, $b[q]$ is true from L2 to L10 of each round of $q$ that gets past L4.

## The invariant

Let **J** be the statement: *at each time at which some process is in the critical section, $y \ne 0$*. Let **ME** be mutual exclusion. We show that J and ME both hold at all times. Suppose not, and let $s$ be the first time at which one of them fails. We get a contradiction in each case below.

## Lemma 1 (J holds at $s$)

*Suppose ME holds at all times up to $s$ and J holds at all times before $s$. Then J holds at $s$.*

*Proof.* Let $z$ be in the critical section at $s$. By F1, a write of 0 to $y$ at time $e$ is an L16 by some process $w$ that was in the critical section just before $e$.

- A write of 0 in $(E_z, s)$: then $w \ne z$, and $w$ and $z$ are both in the critical section just before $e$, against ME.
- If $z$ took the slow path, it read $y = z \ne 0$ at $E_z$, so by the first point $y \ne 0$ at $s$.

Now let $z$ take the fast path, and suppose some $w$ writes 0 to $y$ at $e \in (c_z, E_z)$. Then $w$ was in the critical section on $[E_w, e)$, and $E_w < e < E_z$.

- *$w$ took the fast path.* By F2, no write of $x$ is in $(a_z, E_z)$ or in $(a_w, E_w)$. Since $a_w < E_w < E_z$, we get $a_w < a_z$, and then $a_z > E_w$. So $E_w < a_z < r_z < c_z < e$, and $w$ is in the critical section at $r_z$. But $z$ reads $y = 0$ at $r_z$, so J fails at $r_z < s$.
- *$w$ took the slow path.* At L11, $w$ read $b[z]$ false at some time $k < E_w < E_z$. By F3, $b[z]$ is true from L2 of $z$ to after $E_z$, so $k$ is before L2 of $z$. The write $y \leftarrow w$ of $w$ is before $k$, so it is before $r_z$. If $E_w > r_z$, then $y$ changed from 0 at $r_z$ to $w$ at $E_w$ with no write of $w$ in between, against F2. So $E_w < r_z < e$, and $w$ is in the critical section at $r_z$, when $z$ reads $y = 0$. So J fails at $r_z < s$.

So $y$ is not written 0 in $(c_z, s)$, and $y \ne 0$ at $s$. $\square$

## Lemma 2 (ME holds at $s$)

*Suppose ME and J hold at all times before $s$. Then ME holds at $s$.*

*Proof.* Suppose two processes are in the critical section at $s$. Since ME holds before $s$, one of them, $q$, enters at $s$, so $E_q = s$, and the other, $p$, entered at $E_p < s$ and is in the critical section on $[E_p, s]$. By J, $y \ne 0$ on $[E_p, s)$.

*Case 1: $q$ took the fast path.* It read $y = 0$ at $r_q < s$, so $r_q < E_p$ by J.

- If $p$ took the fast path: by F2 there is no write of $x$ in $(a_q, E_q)$, and $a_p < E_p < E_q$, so $a_p < a_q$. But $a_q < r_q < E_p$, so $a_q \in (a_p, E_p)$, against F2 for $p$.
- If $p$ took the slow path: it read $b[q]$ false at L11 at some time $k < E_p < s$. By F3, $b[q]$ is true from L2 of $q$ to after $s$, so $k$ is before L2 of $q$, and $c_p < k < r_q$. Then $y$ goes from 0 at $r_q$ to $p$ at $E_p > r_q$ with no write of $p$ in between, against F2.

*Case 2: $q$ took the slow path.* It reads $y = q$ at $E_q$.

- If $p$ took the fast path: $q$ read $b[p]$ false at L11 at some time $k < E_q$. By F3, $b[p]$ is true from L2 of $p$ to after $s$, so $k$ is before L2 of $p$, and $c_q < k < c_p$. Then $y$ goes from $p$ at $c_p$ to $q$ at $E_q$ with no write of $q$ in between, against F2.
- If $p$ took the slow path: $y = p$ at $E_p$ and $y = q$ at $E_q$, so the last write $c_q$ of $q$ to $y$ is in $(E_p, E_q)$. If $r_q > E_p$, then $q$ reads $y = 0$ while $p$ is in the critical section, against J. So $r_q < E_p$, and since $y = 0$ at $r_q$ and $y = p$ at $E_p$, we get $r_q < c_p < E_p$. Process $p$ read $b[q]$ false at L11 at some time $k \in (c_p, E_p)$. But by F3, $b[q]$ is true from L2 of $q$, which is before $r_q$, until L10 of $q$, which is after $c_q > E_p$. So $b[q]$ is true at $k$, which is a contradiction.

Each case gives a contradiction. $\square$

By Lemmas 1 and 2, the time $s$ cannot exist. So J and ME hold at all times.

## Theorem 1 (mutual exclusion)

*At no time are two processes in the critical section.* This is ME. $\square$

## Theorem 2 (deadlock freedom)

*In a fair run, if some process is in its entry section at some time, then later some process enters the critical section.*

*Proof.* Suppose not. Then from some time $t_0$ on, no process enters. The exit section has no wait, so from some time $t_1 \ge t_0$ on, a fixed nonempty set $T$ of processes is in the entry section forever, and every other process is in the remainder with its $b$ false. After $t_1$ no process does L16, so by F1 no write of 0 to $y$ happens after $t_1$.

*Case A: $y \ne 0$ at some time $t_2 \ge t_1$.* Then $y \ne 0$ forever after $t_2$. Each round that starts after $t_2$ reads $y \ne 0$ at L4 and never reaches L8. So there are only finitely many writes to $y$, and from some time $t_3$ on, $y = v$ for a fixed $v \ne 0$. The last write to $y$ is the L8 of $v$, and $v$ did not do L16 after it, so $v \in T$ and $v$ is in the round of that write. After $t_3$, no process is between its read at L4 and its write at L8, and each process in $T$ other than $v$ ends with $b$ false forever: a process at L2 to L4 reads $y \ne 0$, goes to L5 and waits at L6 forever; a process at L9 does not enter, so it writes $b$ false at L10, and if it passes L11 it reads $y = v$ at L12 and waits at L13 forever; a process at L11 to L13 already has $b$ false. Process $v$ does not enter at L9, so it writes $b[v] \leftarrow$ false at L10. So from some time on, all $b$ are false, $v$ passes L11, reads $y = v$ at L12 and enters. This is a contradiction.

*Case B: $y = 0$ at all times after $t_1$.* Then no L8 happens after $t_1$. A round that starts after $t_1$ reads $y = 0$ at L4 and does L8, so no round starts after $t_1$. The waits at L6 and L13 end when $y = 0$, and then a new round starts, so no process waits there after some time. A process at L2 to L8 would do L8 after $t_1$, so no process is there. So every process in $T$ is at L9 to L12. None enters at L9, so each writes $b$ false at L10, and then all $b$ are false. Each passes L11, reads $y = 0$ at L12, which is not its name, goes to L13, reads $y = 0$ and starts a new round. This is a contradiction. $\square$

## Theorem 3 (starvation)

*The algorithm is not starvation free.*

*Proof.* For $n = 2$ with the names 1 and 2, start in the state $S$ in which process 1 is in the critical section after the fast path, $x = 2$, $y = 1$, and process 2 waits at L6 with $b[2]$ false. Then:

1. process 1 leaves: $y \leftarrow 0$, $b[1] \leftarrow$ false;
2. process 2 reads $y = 0$ at L6 and goes back to L2;
3. process 1 enters again by the fast path: $b[1] \leftarrow$ true, $x \leftarrow 1$, reads $y = 0$, $y \leftarrow 1$, reads $x = 1$;
4. process 2 writes $b[2] \leftarrow$ true and $x \leftarrow 2$, reads $y = 1$, writes $b[2] \leftarrow$ false and waits at L6.

This gives the state $S$ again. Both processes take steps in each round, so repeating it forever gives a fair run in which process 2 never enters. The test file runs this cycle and checks that it returns to the same state. $\blacksquare$
