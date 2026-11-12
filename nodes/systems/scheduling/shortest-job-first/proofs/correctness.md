---
title: SJF runs, at each free moment, the arrived process with the least predicted burst
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Process $i$ has arrival $a_i$, burst $b_i > 0$ and predicted burst $\tau_i$, and its key is $\kappa_i = (\tau_i, a_i, i)$, compared in lexicographic order. Line L1 lists the processes as $Q[1], \ldots, Q[n]$ in order of $(a_i, i)$.

**Claim.** SJF returns start times $S$ and completion times $C = S + b$ such that:

1. the intervals $[S_i, C_i)$ do not overlap, and $S_i \ge a_i$ for each $i$;
2. the schedule is work-conserving: the CPU is idle at time $\theta$ only if every process with $a_i \le \theta$ has finished by $\theta$;
3. at each dispatch time $t = S_i$, process $i$ has the least key among the processes that have arrived by $t$ and have not started.

*Proof.* Call a process *admitted* once line L5 has inserted it into $H$, and *placed* once line L7 has set its start. We show that the loop of line L2 keeps this invariant.

> **(I)** At the test of line L2: (a) the placed processes satisfy 1 and 3, and $t$ is the largest completion time among them, or $t = 0$ if none is placed; (b) $H$ holds exactly the admitted processes that are not placed; (c) the admitted processes are $Q[1], \ldots, Q[k-1]$, and they are exactly the processes with $a_i \le t$ or with $a_i \le$ some earlier value of $t$; (d) the CPU was idle at time $\theta < t$ only if every process with $a_i \le \theta$ had finished by $\theta$.

*Initialization.* Before the first test, $t = 0$, $H$ is empty and $k = 1$. Nothing is admitted or placed, and (a) to (d) hold with empty sets and the empty interval $[0, 0)$.

*Maintenance.* Assume (I) and that the loop body runs, so $k \le n$ or $H$ is not empty.

- Line L3. If $H$ is empty and $t < a_{Q[k]}$, the clock jumps to $a_{Q[k]}$. By (b), every admitted process is placed, so by (a) it has finished by $t$. By (c) and the order of $Q$, every process not admitted has $a_i \ge a_{Q[k]}$. So at each $\theta \in [t, a_{Q[k]})$ no unfinished process has arrived, and (d) still holds. If $H$ is empty, then $k \le n$, and after line L3 we have $a_{Q[k]} \le t$.
- Lines L4 and L5 admit $Q[k], Q[k+1], \ldots$ while their arrival is at most $t$. Since $Q$ is sorted by arrival, after the loop the admitted processes are exactly those with $a_i \le t$, which keeps (c), and (b) holds because each one goes into $H$. Now $H$ is not empty: either it was not empty, or line L3 made $Q[k]$ arrive by $t$.
- Line L6 removes the process $i$ with the least key in $H$. By (b) and (c), $H$ holds exactly the processes that have arrived by $t$ and have not started, so part 3 holds for $i$.
- Line L7 sets $S_i = t \ge a_i$ and $C_i = t + b_i$, and moves $t$ to $C_i$. By (a), every earlier interval ends by the old $t$, so the new interval does not overlap them, and part 1 holds. The CPU is busy on $[S_i, C_i)$, so (d) holds for the new $t$. So (I) holds at the next test.

*Termination.* Each pass of the loop removes one process from $H$ at line L6, and a process enters $H$ only once, because $k$ only grows. So the loop body runs exactly $n$ times; after it, $k = n + 1$ and $H$ is empty, and the test of line L2 fails. At that point all $n$ processes are placed, so (a) gives parts 1 and 3, and (d) gives part 2 up to the last completion time, after which no process is unfinished. $\square$

**Cost.** Line L1 sorts in $O(n \log n)$ time. Each process is inserted into and removed from the binary heap once, at $O(\log n)$ each. All other lines take $O(1)$ per pass. So the time is $O(n \log n)$ in the worst case, and the extra space is $O(n)$.

**The exponential average.** Let $t_0, t_1, \ldots$ be the measured bursts of one process and $\tau_0$ the initial guess. The rule $\tau_{n+1} = \alpha t_n + (1 - \alpha)\tau_n$ unrolls, for each $n \ge 0$, to

$$\tau_{n+1} = \sum_{j=0}^{n} \alpha (1 - \alpha)^{j}\, t_{n-j} + (1 - \alpha)^{n+1}\, \tau_0 .$$

*Base, $n = 0$.* The right side is $\alpha t_0 + (1 - \alpha)\tau_0 = \tau_1$.

*Step.* Assume the formula for $n$. Then $\tau_{n+2} = \alpha t_{n+1} + (1 - \alpha)\tau_{n+1}$. Multiplying the formula for $\tau_{n+1}$ by $1 - \alpha$ turns the term $\alpha(1-\alpha)^j t_{n-j}$ into $\alpha(1-\alpha)^{j+1} t_{(n+1)-(j+1)}$ and $(1-\alpha)^{n+1}\tau_0$ into $(1-\alpha)^{n+2}\tau_0$. With the new term $\alpha t_{n+1}$ for $j = 0$, this is the formula for $n + 1$.

For $0 \le \alpha \le 1$ the weights $\alpha(1-\alpha)^j$ and $(1-\alpha)^{n+1}$ are nonnegative, and they sum to $\alpha \sum_{j=0}^{n} (1-\alpha)^j + (1-\alpha)^{n+1} = 1$. So $\tau_{n+1}$ is a weighted mean of $\tau_0, t_0, \ldots, t_n$, and lies between the least and the largest of them. $\blacksquare$
