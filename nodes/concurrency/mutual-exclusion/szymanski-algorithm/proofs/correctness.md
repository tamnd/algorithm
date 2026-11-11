---
title: Mutual exclusion of Szymański's algorithm
proves: [correctness]
status: full
---

This proof shows mutual exclusion for the algorithm on the page, with one stated assumption about L2. It does not prove deadlock freedom, starvation freedom or the linear wait bound; the page cites them.

**Model.** The registers are atomic and the memory is sequentially consistent, so a run is a sequence of steps, and each step is one read or one write of one process. Each $flag[i]$ has one writer, process $i$.

**Assumption A.** The wait at L2 ends with one atomic test: at an instant $g$, every $flag[j]$ with $j \ne i$ is less than 3. The implementation and the tests read the flags one at a time. For that form, this proof does not apply; the tests check it by exhaustive search for 2 and 3 processes only.

## Notation

In one passage, process $x$ writes its flag in this order: 1 at L1, 3 at L3, 2 at L5 (only if the test at L4 finds a 1), 4 at L7, and 0 at L10. So the value of $flag[x]$ is 1 from the L1 write to the L3 write, it is 3 or 2 from the L3 write to the L7 write, and it is 4 from the L7 write to the L10 write. For one passage of $x$ we write

- $a_x$ for the L1 write, $g_x$ for the instant of Assumption A, $b_x$ for the L3 write,
- $e_x$ for the L7 write and $f_x$ for the L10 write,

so $a_x < g_x < b_x < e_x < f_x$. "$x$ holds 4 at $t$" means $flag[x] = 4$ at time $t$. A *violation* is an L3 write by some process $y$ at a time when another process holds 4.

**Fact F.** If a read of $flag[v]$ at time $d$ returns 4, then the last write by $v$ before $d$ is an L7 write at some time $e_v < d$, and $v$ makes no write in $(e_v, d)$.

## Claim H

*Let $x$ write 3 at $b_x$ at a time when no other process holds 4. Suppose $x$ then writes 2 at L5, and the read at L6 that ends its wait returns $flag[v] = 4$ at time $d$. Then $b_x < e_v < d$, and $v$ holds 4 at every time in $[e_v, e_x]$.*

*Proof.* By Fact F, $v$ holds 4 on $[e_v, d]$. If $e_v < b_x$, then $v$ holds 4 at $b_x$, which is against the hypothesis. So $b_x < e_v < d$. Process $v$ removes its 4 only at $f_v$, which comes after its reads at L8 and at L9. On $[b_x, e_x)$ the value of $flag[x]$ is 3 or 2.

- If $x > v$: at L9, $v$ waits until it reads $flag[x] < 2$ or $flag[x] = 4$. Every read of $flag[x]$ by $v$ in $(e_v, e_x)$ returns 3 or 2, so the read that ends this wait is at a time $h > e_x$. So $f_v > h > e_x$.
- If $x < v$: at L8, $v$ waits until it reads $flag[x] < 2$. On $[b_x, f_x)$ the value of $flag[x]$ is 3, 2 or 4, and $e_v > b_x$, so the read that ends this wait is at a time $k > f_x > e_x$. So $f_v > k > e_x$.

In both cases $v$ makes no write in $(e_v, e_x]$, so it holds 4 on $[e_v, e_x]$. $\square$

## Lemma 1 (the door)

*There is no violation: no process writes 3 at a time when another process holds 4.*

*Proof.* Suppose there is a violation, and take the earliest one. Process $y$ writes 3 at $u = b_y$, and process $w \ne y$ holds 4 at $u$. At $g_y$, every other flag is less than 3 by Assumption A, so $w$ does not hold 4 at $g_y$. So $w$ writes 4 at some time in $(g_y, u)$. Let $e_x$ be the first L7 write in $(g_y, u)$, by some process $x$. On $[a_y, u)$ the value of $flag[y]$ is 1, so $x \ne y$. The write $b_x$ comes before $e_x < u$, so it is not a violation, since $u$ is the earliest one. So no other process holds 4 at $b_x$.

*Case 1: the test at L4 of $x$ finds no 1.* Then $x$ reads every other flag at L4, and $flag[x] = 3$ on $[b_x, e_x)$. Let $r \in (b_x, e_x)$ be the time of its read of $flag[y]$. If $r \ge a_y$, then $r \in [a_y, u)$, so the read returns 1, which is against the case. So $r < a_y$, and $b_x < r < a_y < g_y < e_x$. Then $flag[x] = 3$ at $g_y$, which is against Assumption A.

*Case 2: the test at L4 of $x$ finds a 1.* Then $x$ writes 2, and its wait at L6 ends with a read at time $d < e_x$ that returns $flag[v] = 4$. By Claim H, $b_x < e_v < d < e_x$. If $e_v > g_y$, then $e_v$ is an L7 write in $(g_y, e_x)$, against the choice of $e_x$. So $e_v < g_y < e_x$, and by Claim H, $v$ holds 4 at $g_y$. Since $flag[y] = 1$ at $g_y$, we have $v \ne y$, and this is against Assumption A.

Both cases give a contradiction, so there is no violation. $\square$

## Theorem 1 (mutual exclusion)

*At no time are two processes in the critical section.*

*Proof.* Suppose $p < q$ are both in the critical section at time $t$. Each one holds 4 from its L7 write until its L10 write, which comes after its critical section, so both hold 4 at $t$. Before $q$ entered, its L8 wait read $flag[p] < 2$ at some time $r$ with $e_q < r < t$. At $t$, $p$ holds 4. A flag goes from a value less than 2 to the value 4 only through an L3 write, so $p$ writes 3 at some time $b \in (r, t)$. Process $q$ holds 4 on all of $[e_q, t]$, and $e_q < r < b$, so $q$ holds 4 at $b$. So the write at $b$ is a violation, which is against Lemma 1. $\blacksquare$
