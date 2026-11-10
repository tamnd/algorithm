---
title: Optimal Available follows the optimal plan for the known work and meets every deadline
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The jobs are $(r_j, w_j, d_j)$ with $w_j > 0$ and $r_j < d_j$. At a time $t$, the set $R$ holds the released jobs that are not finished, and $\rho_j > 0$ is the remaining work of job $j \in R$. Sort $R$ by deadline, $d_1 \le d_2 \le \dots \le d_m$, with ties broken by index, and let $P_i = \rho_1 + \dots + \rho_i$.

## Part 1. The plan of line L5 is the optimal plan for the known work

Assume $d_i > t$ for each $i$ (Part 3 shows that this always holds). Define

$$g(t) = \max_{1 \le i \le m} \frac{P_i}{d_i - t}.$$

**Claim 1.** Every schedule that finishes the jobs of $R$ by their deadlines, starting at time $t$, runs at average speed at least $g(t)$ on some interval $[t, d_i]$. So with no more arrivals, the minimum energy schedule runs at speed $g(t)$ from $t$ until the last deadline $d_k$ that attains the maximum.

*Proof.* The jobs $1, \dots, i$ must get $P_i$ units of work in $[t, d_i]$, so the average speed there is at least $P_i / (d_i - t)$. Now let $k$ be the largest index with $P_k / (d_k - t) = g$. The interval $[t, d_k]$ is the densest interval of the YDS algorithm for these jobs, because each job is released by $t$ and every interval of the form $[t, b]$ has density at most $g$ (the work with deadline at most $b$ is some $P_i$ with $d_i \le b$, so its density is at most $P_i / (d_i - t) \le g$). For the remaining work, every job is available at $t$, so an interval that starts after $t$ contains no whole job and has density 0. So YDS first runs the jobs $1, \dots, k$ at speed $g$ on $[t, d_k]$. $\square$

**Claim 2.** EDF at speed $g$ from time $t$ finishes job $i$ by $d_i$ for each $i \le k$, and it finishes the jobs $1, \dots, k$ exactly at $d_k$.

*Proof.* EDF runs the jobs in the order $1, 2, \dots$, so it finishes job $i$ at $t + P_i / g$. Since $P_i \le g (d_i - t)$, this is at most $d_i$. For $i = k$ it is $t + P_k / g = d_k$. $\square$

## Part 2. The speed is constant on each piece

Let $e = \min(d_k, t')$ as in line L6, and let $t < u < e$. During $[t, u)$, EDF at speed $g$ has done $g (u - t)$ units of work, all on the first jobs in deadline order. So for each job $i$ that is not finished at $u$, the new prefix sum is $P_i(u) = P_i - g (u - t)$, and for the jobs that are finished it does not apply.

For $i \le k$ not finished at $u$:

$$\frac{P_i(u)}{d_i - u} = \frac{P_i - g (u - t)}{(d_i - t) - (u - t)} \le \frac{g (d_i - t) - g (u - t)}{(d_i - t) - (u - t)} = g,$$

with equality for $i = k$. For $i > k$, $P_i < g (d_i - t)$ by the choice of $k$, so the same computation gives a ratio strictly below $g$. So $g(u) = g$, and $k$ is still the largest index that attains it. This shows two things. First, the plan computed at any time in $[t, e)$ has the same speed, so the piece output in line L7 is the speed of the optimal plan for the known work at each moment of $[t, e)$, which is the definition of Optimal Available. Second, it does not matter for the speeds that the code makes a new plan only at the end of a piece.

## Part 3. Every deadline is met

We show by induction over the passes of line L4 that, at the start of each pass, every job $j \in R$ has $d_j > t$.

At a release time $t$, each new job has $d_j > r_j = t$. Each job that was in $R$ before satisfies $d_j > t$ by the induction hypothesis at the end of the last pass, shown next.

Consider one pass, from $t$ to $e$.

- If $e = d_k$, then by Claim 2 the jobs $1, \dots, k$ are finished at $d_k$, each by its own deadline. Each remaining job has index $i > k$. If $d_i = d_k$, then $P_i / (d_i - t) \ge P_k / (d_k - t) = g$, so $i$ also attains the maximum, which contradicts the choice of $k$ as the largest such index. So $d_i > d_k = e$.
- If $e = t' < d_k$, then each job $i \le k$ that is not finished at $t'$ has its planned completion time $t + P_i / g > t'$ and at most $d_i$, so $d_i > t'$. Each job $i > k$ has $d_i \ge d_k > t'$.

So at the start of the next pass all unfinished jobs have deadlines after the current time. A job finishes only inside some pass, and by Claim 2 it finishes by its deadline (for $i \le k$ when $e = d_k$), or by the same argument at the time it completes inside the piece (EDF finishes job $i$ at $t + P_i / g \le d_i$ when that time is before $e$). After the last release, the passes continue until $R$ is empty. So every job finishes by its deadline.

## Part 4. Termination

Each pass of line L4 ends at $e = d_k$ or at $e = t'$. In the first case at least the job $k$ finishes, so there are at most $n$ such passes. In the second case the loop moves to the next release time, so there are at most $n - 1$ such passes. So the algorithm makes at most $2n - 1$ passes and outputs at most $2n - 1$ pieces. The speed $g$ is positive in each pass, since $R$ is not empty and $\rho_j > 0$, so each pass does positive work and the loop over a release interval ends. $\blacksquare$
