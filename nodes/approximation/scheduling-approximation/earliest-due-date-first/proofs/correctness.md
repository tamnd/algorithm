---
title: The earliest due date order minimizes the maximum lateness on one machine
proves: [correctness]
status: full
---

**Statement.** Let jobs $1, \ldots, n$, with $n \ge 1$, have processing times $p_j \ge 0$ and real due dates $d_j$, all available at time 0. Let $\pi$ be any order with $d_{\pi_1} \le \cdots \le d_{\pi_n}$, run back to back from time 0, as EDD does. Then for every schedule $\sigma$ of the jobs on one machine, preemptive or not and with or without idle time, $L_{\max}(\sigma) \ge L_{\max}(\pi)$. So EDD is optimal for $1 \| L_{\max}$ and for $1 \mid pmtn \mid L_{\max}$.

**Setup.** For a set $A$ of jobs, write $p(A) = \sum_{j \in A} p_j$. In a schedule, job $j$ completes at $C_j$, the time when its last piece ends. The machine processes at most one job at each moment and starts at time 0.

**Step 1 (the value of EDD).** Lines L3 to L5 run the jobs of $\pi$ back to back, so the job in position $i$ completes at $C_{\pi_i} = p_{\pi_1} + \cdots + p_{\pi_i}$. Choose a position $k$ with $C_{\pi_k} - d_{\pi_k} = L_{\max}(\pi)$, and let $A = \{\pi_1, \ldots, \pi_k\}$. Then $L_{\max}(\pi) = p(A) - d_{\pi_k}$. Because the order is sorted by due date, $d_j \le d_{\pi_k}$ for each $j \in A$.

**Step 2 (a lower bound for any set).** Let $B$ be a nonempty set of jobs and $\sigma$ any schedule. Let $j^*$ be a job of $B$ with the largest completion time in $\sigma$. At time $C_{j^*}$ every job of $B$ is complete, so the machine has spent $p(B)$ units of time on $B$ within $[0, C_{j^*}]$. It processes at most one job at a time, so $C_{j^*} \ge p(B)$. Hence
$$L_{\max}(\sigma) \ge C_{j^*} - d_{j^*} \ge p(B) - \max_{j \in B} d_j .$$

**Step 3 (the bound for the EDD prefix).** Apply Step 2 to $B = A$. By Step 1, $\max_{j \in A} d_j = d_{\pi_k}$. So $L_{\max}(\sigma) \ge p(A) - d_{\pi_k} = L_{\max}(\pi)$.

**End.** Every schedule has a maximum lateness of at least $L_{\max}(\pi)$, and $\pi$ is itself a schedule, so $\pi$ is optimal. The argument does not depend on how ties between equal due dates are broken, so every EDD order is optimal. Since $T_{\max} = \max(0, L_{\max})$ is a nondecreasing function of $L_{\max}$, EDD also minimizes $T_{\max}$, and all due dates can be met if and only if $L_{\max}(\pi) \le 0$. ∎

**Cost.** Line L1 sorts the $n$ due dates in $\Theta(n \log n)$ comparisons in the worst case. Each round of lines L3 to L5 does $O(1)$ work, so the loop takes $\Theta(n)$ time. The order and the completion times use $\Theta(n)$ space.
