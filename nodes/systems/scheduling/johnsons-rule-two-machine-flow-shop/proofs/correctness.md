---
title: Johnson's smallest-time procedure is optimal, and one order suffices for at most three machines
proves: [correctness]
status: full
---

We prove four claims. Claim 1 is for flow shops with $m$ machines, where $p_{ij}$ is the time of job $j$ on machine $i$ and every job visits machines $1, 2, \ldots, m$ in this order. Claims 2 to 4 are for $m = 2$, with $a_j = p_{1j}$ and $b_j = p_{2j}$. In a schedule, a machine *order* is the sequence in which that machine runs the jobs.

**Claim 1 (permutation dominance).** Every schedule can be changed, without raising the makespan, so that machines 1 and 2 have the same order, and also so that machines $m - 1$ and $m$ have the same order. For $m \le 3$ this gives an optimal schedule with one order on all machines.

*Proof.* (Front.) Suppose machine 1 runs $i$ right before $j$, from time $s$, and machine 2 runs $j$ before $i$. Move $j$ to $[s, s + p_{1j}]$ and $i$ to $[s + p_{1j}, s + p_{1i} + p_{1j}]$ on machine 1. Job $j$ leaves machine 1 earlier. Job $i$ leaves machine 1 at $s + p_{1i} + p_{1j}$, the time at which $j$ left it before. Machine 2 started $j$ no earlier than that, and started $i$ after $j$, so $i$ is still ready in time on machine 2. Nothing on machines $2, \ldots, m$ moves.

(Back.) Suppose machine $m$ runs $i$ right before $j$, from time $s$, and machine $m - 1$ runs $j$ before $i$. Move $j$ to $[s, s + p_{mj}]$ and $i$ to $[s + p_{mj}, s + p_{mi} + p_{mj}]$ on machine $m$. Job $j$ left machine $m - 1$ before $i$ did there, and $i$ left it by $s$, since $i$ started on machine $m$ at $s$; so $j$ may start at $s$. Job $i$ now starts later, so it is ready. Job $i$ now ends at the old end of $j$, and job $j$ ends earlier, so no completion time grows. Nothing on machines $1, \ldots, m - 1$ moves.

Each swap of the front kind lowers by one the number of pairs that machines 1 and 2 order differently, and the machine 2 order never changes; if the orders differ, a pair adjacent on machine 1 is ordered differently on machine 2, so the swaps continue until the orders agree. The back kind does the same for machines $m - 1$ and $m$, with the order of machine $m - 1$ fixed. For $m = 2$ the front swaps alone finish. For $m = 3$, first apply back swaps until machine 3 has the order of machine 2, then front swaps until machine 1 has it too; the front swaps do not touch machines 2 and 3. $\square$

So for $m = 2$ we only compare orders $\sigma$, each run as early as possible. As on the [two-list page](/johnsons-rule/), the makespan is $\max_k T_k(\sigma)$ with $T_k(\sigma) = \sum_{l \le k} a_{\sigma(l)} + \sum_{l \ge k} b_{\sigma(l)}$: the completion time on machine 2 of the job in position $k$ is the longest of the paths that use machine 1 up to some position $l \le k$ and machine 2 from $l$ to $k$.

**Claim 2 (adjacent swap).** Let $\sigma$ have $i$ in position $k$ and $j$ in position $k + 1$, and let $\sigma'$ swap them. If $\min(a_i, b_j) \le \min(a_j, b_i)$, then $C_{\max}(\sigma) \le C_{\max}(\sigma')$.

*Proof.* The terms $T_q$ with $q \ne k, k + 1$ are equal for $\sigma$ and $\sigma'$, because each depends only on which jobs are before, at and after position $q$, and the pair is on one side of $q$ in both orders. With $A$ the machine 1 time before position $k$ and $B$ the machine 2 time after position $k + 1$, the two remaining terms of $\sigma$ are $A + B + a_i + b_i + b_j$ and $A + B + a_i + a_j + b_j$. Their maximum is $A + B + a_i + b_j + \max(b_i, a_j)$. For $\sigma'$ it is $A + B + a_j + b_i + \max(b_j, a_i)$. Using $x + y = \max(x, y) + \min(x, y)$, the first is $S - \min(a_j, b_i)$ and the second is $S - \min(a_i, b_j)$, with $S = A + B + a_i + a_j + b_i + b_j$. $\square$

**Claim 3 (the output satisfies the condition).** Line L8 returns an order $\pi$ of all $n$ jobs, and for every pair with $i$ before $j$ in $\pi$, $\min(a_i, b_j) \le \min(a_j, b_i)$.

*Proof.* Each job has two triples in $T$, and line L4 skips the second, so each job is placed exactly once, either at the next free front position or at the next free back position. After $q$ placements, $lo - 1 + n - hi = q$, so after $n$ placements all positions are filled exactly once. Every front position is left of every back position, front positions are filled from left to right, and back positions from right to left.

Let $i$ come before $j$ in $\pi$. Among the four triples of $i$ and $j$, let $x$ be the first one in $T$. When the loop reaches $x$, neither job is placed, since each job is placed at its first triple. So $x$ places its own job, and that job is placed before the other one.

- If $x$ is $(a_j, 1, j)$, job $j$ takes the next front position, and $i$, placed later, goes to a later front position or to a back position; both are right of $j$. This contradicts $i$ before $j$.
- If $x$ is $(b_i, 2, i)$, job $i$ takes the next back position, and $j$, placed later, goes to a front position or to an earlier back position; both are left of $i$. Again a contradiction.

So $x$ is $(a_i, 1, i)$ or $(b_j, 2, j)$. Since $x$ is first in sorted order among the four, its value is the least of $a_i, b_i, a_j, b_j$. If $x$ is $a_i$, then $\min(a_i, b_j) = a_i \le \min(a_j, b_i)$. If $x$ is $b_j$, then $\min(a_i, b_j) = b_j \le \min(a_j, b_i)$. $\square$

**Claim 4 (optimality).** The order $\pi$ has the least makespan over all schedules.

*Proof.* By Claim 1, some optimal schedule uses one order $\sigma$ on both machines. If $\sigma \ne \pi$, then some adjacent pair of $\sigma$, $j$ then $i$, has $i$ before $j$ in $\pi$. By Claim 3, $\min(a_i, b_j) \le \min(a_j, b_i)$, so by Claim 2 swapping the pair in $\sigma$ does not raise the makespan. The swap lowers the number of pairs that $\sigma$ and $\pi$ order differently by exactly one. So after at most $\binom{n}{2}$ swaps, $\sigma$ becomes $\pi$, with makespan at most the optimum. $\blacksquare$

**Four machines.** Claim 1 cannot be extended to all machines when $m = 4$. Let job 1 have times $(1, 4, 4, 1)$ and job 2 have times $(4, 1, 1, 4)$. In the order $1, 2$ on all machines, job 2 waits for job 1 on each machine and ends at $1 + 4 + 4 + 1 + 4 = 14$ (machine 4 runs job 1 from $9$ to $10$ and job 2 from $10$ to $14$). The order $2, 1$ is the mirror image and also ends at $14$. The schedule with order $1, 2$ on machines 1 and 2 and order $2, 1$ on machines 3 and 4 runs job 1 on machines 1 to 4 in $[0, 1]$, $[1, 5]$, $[7, 11]$, $[11, 12]$ and job 2 in $[1, 5]$, $[5, 6]$, $[6, 7]$, $[7, 11]$. Each machine runs one job at a time and each job visits the machines in order, and it ends at $12 < 14$.
