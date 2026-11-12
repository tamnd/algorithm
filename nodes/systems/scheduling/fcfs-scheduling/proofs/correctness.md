---
title: FCFS produces the first-come, first-served schedule, and its waiting times
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The input is $n$ processes, process $i$ with arrival $a_i \ge 0$ and burst $b_i > 0$. Line L1 lists them as $q_1, \ldots, q_n$ in order of $(a_i, i)$.

**Claim.** FCFS returns start times $S$ and completion times $C$ such that:

1. each process runs once, without a break, on $[S_i, C_i)$ with $C_i = S_i + b_i$ and $S_i \ge a_i$;
2. the intervals do not overlap, and the processes run in the order $q_1, \ldots, q_n$;
3. the CPU is idle at time $t$ only if no process that has arrived by $t$ is still unfinished (the schedule is work-conserving);
4. $S_{q_1} = a_{q_1}$ and $S_{q_k} = \max(C_{q_{k-1}}, a_{q_k})$ for $k \ge 2$.

*Proof.* We use this invariant of the loop of line L3.

> **(I)** Before the iteration for $q_k$, with $1 \le k \le n + 1$: (a) the processes $q_1, \ldots, q_{k-1}$ have intervals that satisfy 1, 2 and 4 among themselves; (b) $t = C_{q_{k-1}}$ when $k \ge 2$, and $t = 0$ when $k = 1$; (c) no process other than $q_1, \ldots, q_{k-1}$ has started, and at each time in $[0, t)$ at which the CPU is idle, no process with arrival at most that time is unfinished.

*Initialization.* For $k = 1$, line L2 sets $t = 0$. Parts (a) and (c) hold because there are no intervals and $[0, 0)$ is empty.

*Maintenance.* Assume (I) for $k \le n$, and let $i = q_k$. Lines L4 and L5 set $S_i = \max(t, a_i)$, so $S_i \ge a_i$. Line L6 and L7 set $C_i = S_i + b_i$. By (b), $S_i \ge C_{q_{k-1}}$ for $k \ge 2$, so the new interval starts after all earlier ones end, and part 4 holds for $q_k$. So (a) holds for $k + 1$, and line L6 makes (b) true. For (c), the CPU is idle in $[t, S_i)$ only when $t < a_i$. Every process $q_l$ with $l \ge k$ has $a_{q_l} \ge a_i$ by the order of line L1, and each $q_l$ with $l < k$ has finished by $t$. So at each time $\tau \in [t, a_i)$ no unfinished process has arrived by $\tau$. On $[S_i, C_i)$ the CPU is busy. So (c) holds for $k + 1$.

*Termination.* The loop runs exactly $n$ times, once per element of the finite list $Q$. With $k = n + 1$, (a) gives parts 1, 2 and 4 for all processes, and (c) gives part 3 on $[0, C_{q_n})$. After $C_{q_n}$ every process is finished, so part 3 holds there too. $\square$

**Waiting times.** In a nonpreemptive schedule of single-burst processes the waiting time is $W_i = C_i - a_i - b_i = S_i - a_i$. If all processes arrive at time 0, then part 4 gives $S_{q_1} = 0$ and $S_{q_k} = C_{q_{k-1}} = S_{q_{k-1}} + b_{q_{k-1}}$. By induction on $k$,

$$W_{q_k} = \sum_{l=1}^{k-1} b_{q_l}, \qquad \sum_{k=1}^{n} W_{q_k} = \sum_{k=1}^{n} (n - k)\, b_{q_k}.$$

For the bursts $24, 3, 3$ this gives $0 + 24 + 27 = 51$, a mean of 17. For the order $3, 3, 24$ it gives $0 + 3 + 6 = 9$, a mean of 3.

**Unbounded ratio.** Let one process of burst $L$ come first and $k$ processes of burst $s$ follow, all at time 0. FCFS has mean waiting time $(kL + s\,k(k-1)/2)/(k+1)$. The order with the short processes first has mean waiting time $s\,k(k+1)/2 \,/\, (k+1)$. The quotient is

$$\frac{kL + s\,k(k-1)/2}{s\,k(k+1)/2} = \frac{2L}{s(k+1)} + \frac{k-1}{k+1},$$

which grows without bound as $L/s$ grows with $k$ fixed. So FCFS has no constant-factor guarantee for the mean waiting time. $\blacksquare$
