---
title: SPT minimizes the total completion time on m identical machines
proves: [correctness]
status: full
---

**Statement.** Let $m \ge 1$ and let jobs $1, \ldots, n$ have processing times $p_j \ge 0$, all available at time 0. Among all non-preemptive schedules on $m$ identical machines, the schedule that SPT returns has the least $\sum_j C_j$, and this least value is

$$\sum_{i=1}^{n} \left\lceil \frac{i}{m} \right\rceil q_i,$$

where $q_1 \ge q_2 \ge \cdots \ge q_n$ are the processing times sorted from the longest down. For $m = 1$ this is the statement that SPT is optimal for $1 \| \sum C_j$.

**Setup.** Take any schedule. If a machine is idle before one of its jobs, starting that job and all later jobs of the machine earlier keeps the schedule feasible and does not increase any completion time. So it is enough to compare schedules in which each machine $i$ runs a list $j_1, \ldots, j_r$ back to back from time 0. Then $C_{j_s} = p_{j_1} + \cdots + p_{j_s}$.

**Step 1 (coefficients).** On a machine with list $j_1, \ldots, j_r$,
$$\sum_{s=1}^{r} C_{j_s} = \sum_{s=1}^{r} \sum_{t=1}^{s} p_{j_t} = \sum_{t=1}^{r} (r - t + 1)\, p_{j_t},$$
because $p_{j_t}$ appears in the completion times of $j_t, j_{t+1}, \ldots, j_r$, which are $r - t + 1$ jobs. Call $c_j = r - t + 1$ the coefficient of the job $j = j_t$. Summing over the machines, $\sum_j C_j = \sum_j c_j p_j$. On one machine the coefficients are $1, 2, \ldots, r$, each used once.

**Step 2 (the coefficients are large enough).** Let $u_1 \le u_2 \le \cdots \le u_n$ be the coefficients of a schedule, sorted. We show $u_i \ge \lceil i/m \rceil$ for each $i$. The jobs with the $i$ smallest coefficients all have a coefficient at most $u_i$. A machine holds at most one job with each coefficient value, so at most $m$ jobs have coefficient $v$ for each $v$, and at most $m\, u_i$ jobs have a coefficient in $\{1, \ldots, u_i\}$. Hence $i \le m\, u_i$, so $u_i \ge i/m$, and as $u_i$ is an integer, $u_i \ge \lceil i/m \rceil$.

**Step 3 (rearrangement).** Let $u_1 \le \cdots \le u_n$ be reals, and let $x_1, \ldots, x_n$ be the values $q_1, \ldots, q_n$ in some order. We show $\sum_i u_i x_i \ge \sum_i u_i q_i$. If $x$ is not in non-increasing order, there is an index $i$ with $x_i < x_{i+1}$. Swapping $x_i$ and $x_{i+1}$ changes the sum by
$$u_i x_{i+1} + u_{i+1} x_i - u_i x_i - u_{i+1} x_{i+1} = (u_i - u_{i+1})(x_{i+1} - x_i) \le 0,$$
since $u_i \le u_{i+1}$ and $x_i < x_{i+1}$. The swap lowers the number of pairs $a < b$ with $x_a < x_b$ by exactly one, because only the pair at positions $i, i+1$ changes its relative order. That number is at most $\binom{n}{2}$, so after finitely many swaps $x$ is non-increasing, that is, $x = q$ as a sequence of values. The sum never increased, so $\sum_i u_i x_i \ge \sum_i u_i q_i$.

**Step 4 (the lower bound).** Take any schedule, with its coefficients sorted as $u_1 \le \cdots \le u_n$, and let $x_i$ be the processing time of the job with the $i$-th smallest coefficient. By Step 1, Step 3, Step 2 and $q_i \ge 0$,
$$\sum_j C_j = \sum_i u_i x_i \ge \sum_i u_i q_i \ge \sum_i \left\lceil \frac{i}{m} \right\rceil q_i .$$

**Step 5 (SPT meets the bound).** Number the jobs in the SPT order of line L1 as ranks $k = 1, \ldots, n$, so the job of rank $k$ has processing time $q_{n+1-k}$. Line L4 puts rank $k$ on machine $((k-1) \bmod m) + 1$, after the ranks $k - m, k - 2m, \ldots$ of the same machine. The jobs after it on its machine are the ranks $k + m, k + 2m, \ldots$ that are at most $n$. There are $\lfloor (n-k)/m \rfloor$ of them, so its coefficient is $1 + \lfloor (n-k)/m \rfloor$. For an integer $a \ge 0$, write $a = bm + r$ with $0 \le r < m$; then $1 + \lfloor a/m \rfloor = b + 1$ and $\lceil (a+1)/m \rceil = b + \lceil (r+1)/m \rceil = b + 1$, since $0 < (r+1)/m \le 1$. With $a = n - k$ and $i = n + 1 - k$, the job of rank $k$, which has processing time $q_i$, gets the coefficient $\lceil i/m \rceil$. By Step 1, the SPT schedule has $\sum_j C_j = \sum_i \lceil i/m \rceil q_i$.

**End.** By Step 4 every schedule has a total completion time of at least $\sum_i \lceil i/m \rceil q_i$, and by Step 5 the SPT schedule has exactly this value. So SPT is optimal, and the formula gives the optimum. ∎

**Cost.** Line L1 is a sort of $n$ keys, $\Theta(n \log n)$ comparisons with a comparison sort in the worst case. Each of the $n$ rounds of lines L3 to L6 does $O(1)$ arithmetic, with the machine lists stored as arrays with appends in $O(1)$ amortized time. The space is $\Theta(n + m)$.
