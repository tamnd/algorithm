---
tag: 137WN4
kind: theorem
slug: sjf-optimality
name: Optimality of shortest-job-first for average waiting time
aliases:
- SJF optimality
area: systems/scheduling
level: intro
summary: "When all processes are present at time 0 and their bursts are known, shortest-job-first gives the least average waiting time of all schedules; with later arrivals it does not."
prereqs: [shortest-job-first, exchange-argument, scheduling-metrics]
see_also: [srpt-optimality, shortest-processing-time-first, smith-rule, smiths-rule, fcfs-scheduling, srpt, flow-time-minimization, preemption]
sources:
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5, Section 5.3.2 (SJF is provably optimal for the average waiting time of a given set of processes)
  - paper: doi:10.1002/nav.3800030106
    title: Wayne E. Smith, Various optimizers for single-stage production, Naval Research Logistics Quarterly 3(1 to 2), 1956
    locator: pages 59 to 66 (the ratio rule, whose unit-weight case is the shortest-first order)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition, Springer, 2016
    locator: Chapter 3, Single Machine Models (Deterministic), the total weighted completion time and the WSPT rule
  - paper: "Jan Karel Lenstra, Alexander H. G. Rinnooy Kan and Peter Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977"
    locator: pages 343 to 362 (1|r_j|sum C_j is strongly NP-hard)
---

The optimality of shortest-job-first says that on one CPU, when all processes are present at time 0 and their CPU bursts are known, running them in order of increasing burst gives the least total, and so the least average, waiting time of all schedules, preemptive or not. It is the reason why [shortest-job-first](/shortest-job-first/) is the benchmark of [CPU scheduling](/cpu-scheduling/), and the proof is the standard [exchange argument](/exchange-argument/). The theorem fails as soon as processes arrive at different times, unless the scheduler may preempt; then [SRPT](/srpt/) is optimal for the total turnaround time, by [Schrage's theorem](/srpt-optimality/).

## Statement

One CPU runs $n$ processes. Process $i$ arrives at time $0$ and needs one CPU burst of known length $b_i > 0$. A schedule gives process $i$ CPU time of total length $b_i$ in pieces that do not overlap with those of other processes; it may leave the CPU idle and, if it is preemptive, may split a burst into several pieces. Process $i$ completes at $C_i$, and its waiting time is $W_i = C_i - b_i$ (see [scheduling metrics](/scheduling-metrics/)).

**Theorem.** Let $q_1, \ldots, q_n$ be an order with $b_{q_1} \le b_{q_2} \le \cdots \le b_{q_n}$, and let $S^\ast$ run the processes in this order without preemption or idle time. Then for every schedule $S$, preemptive or not,

$$\sum_{i=1}^{n} W_i(S^\ast) = \sum_{k=1}^{n} (n - k)\, b_{q_k} \le \sum_{i=1}^{n} W_i(S).$$

Moreover, a nonpreemptive schedule without idle time is optimal if and only if it runs the processes in order of nondecreasing burst.

Since $\sum_i W_i = \sum_i C_i - \sum_i b_i$ and $\sum_i b_i$ is fixed, the same order minimizes the total completion time and the total turnaround time. In the [three-field notation](/scheduling-notation/) the theorem says that the shortest-first order solves $1 \mid\mid \sum C_j$, and that $1 \mid \mathrm{pmtn} \mid \sum C_j$ has the same optimum.

## In plain words

Suppose all the jobs are waiting at the start and you know how long each one takes. Each job makes every job behind it wait for its whole length. So the first job's length is counted once for each job behind it, the second job's length once less, and so on. To make the total small, the longest lengths should be counted the fewest times, so they go at the end. Putting the shortest job first is best.

Stopping a job in the middle does not help either. Whatever order the jobs finish in, the job that finishes first had to get all of its time before that moment, and the same goes for the second, and so on.

## Proof

**Step 1: a formula for orders.** In the schedule that runs $q_1, \ldots, q_n$ back to back from time 0, process $q_k$ waits for exactly the bursts before it, so $W_{q_k} = \sum_{l < k} b_{q_l}$. Each $b_{q_l}$ appears in the waiting times of the $n - l$ processes after it, so

$$\sum_{k=1}^{n} W_{q_k} = \sum_{k=1}^{n} (n - k)\, b_{q_k}. \tag{1}$$

**Step 2: an adjacent exchange.** Take any order and swap the processes at positions $k$ and $k + 1$, say $x = q_k$ and $y = q_{k+1}$. In (1), the coefficient of $b_x$ falls from $n - k$ to $n - k - 1$, the coefficient of $b_y$ rises from $n - k - 1$ to $n - k$, and the other terms do not change. So the total changes by exactly $b_y - b_x$. If $b_x > b_y$, the swap lowers the total strictly.

**Step 3: the best order.** There are finitely many orders, so one of them, $p$, has the least value of (1). By Step 2, $p$ has no adjacent pair with $b_{p_k} > b_{p_{k+1}}$, so $p$ is nondecreasing in $b$. All nondecreasing orders have the same value of (1): they place the same sorted sequence of lengths $b_{(1)} \le \cdots \le b_{(n)}$ at positions $1, \ldots, n$, and (1) depends only on these lengths. So every nondecreasing order is optimal among orders, and Step 2 shows that every other order is strictly worse. This proves the "if and only if" part.

**Step 4: any schedule.** Let $S$ be any schedule, with idle time or preemption allowed. Number the processes $p_1, \ldots, p_n$ in order of their completion times in $S$, ties in any way. By time $C_{p_k}(S)$, each of $p_1, \ldots, p_k$ has finished, so it has received all of its $b$ units of CPU time before $C_{p_k}(S)$, and the CPU runs one process at a time. Hence

$$C_{p_k}(S) \ge \sum_{l=1}^{k} b_{p_l},$$

which is the completion time of $p_k$ when the order $p$ runs back to back. Summing over $k$ and subtracting $\sum_i b_i$, the total waiting time of $S$ is at least the value of (1) for the order $p$, which is at least the value for $q$ by Step 3. $\blacksquare$

## Consequences

- **SJF as a benchmark.** With exact bursts and all processes present, no policy beats the mean waiting time of [shortest-job-first](/shortest-job-first/). For the bursts 6, 8, 7 and 3 of Silberschatz, the minimum is $(3 \cdot 3 + 2 \cdot 6 + 1 \cdot 7 + 0 \cdot 8)/4 = 7$, and FCFS in the given order gets 10.25.
- **FCFS can be arbitrarily worse.** By formula (1), the mean waiting time of [FCFS](/fcfs-scheduling/) over that of SJF has no bound; the bursts 24, 3, 3 give 17 against 3.
- **Preemption is useless at time 0.** Step 4 shows that preemption cannot lower the total waiting time when all processes are present. It helps only when a short process arrives while a long one runs.
- **Weights.** With a weight $w_i$ per process the same exchange gives the order of increasing $b_i / w_i$, [Smith's rule](/smith-rule/) (also [Smith's rule](/smiths-rule/) in this area). The offline rule without weights is [shortest processing time first](/shortest-processing-time-first/), whose page covers the case of several machines.

## Tightness

**With arrivals, SJF is not optimal.** Let process A arrive at 0 with burst 10 and B arrive at 1 with burst 1.

| schedule | runs | waiting A | waiting B | total |
|---|---|---|---|---|
| nonpreemptive SJF | A on $[0,10)$, B on $[10,11)$ | 0 | 9 | 9 |
| nonpreemptive, idle first | idle on $[0,1)$, B on $[1,2)$, A on $[2,12)$ | 2 | 0 | 2 |
| preemptive, SRPT | A on $[0,1)$, B on $[1,2)$, A on $[2,11)$ | 1 | 0 | 1 |

At time 0 only A has arrived, so SJF, which never leaves the CPU idle, must start A. The best nonpreemptive schedule waits for B, and the problem of finding it, $1 \mid r_j \mid \sum C_j$, is strongly NP-hard (Lenstra, Rinnooy Kan and Brucker 1977); see [flow time minimization](/flow-time-minimization/). With preemption, SRPT is optimal for every input with arrivals; the statement and the proof are on [optimality of SRPT](/srpt-optimality/) and are not repeated here.

**With predicted bursts, SJF is not optimal.** The theorem needs the true $b_i$. The pitfalls of [shortest-job-first](/shortest-job-first/) show a wrong prediction that makes SJF worse than FCFS.

**The order is unique up to ties.** By Step 2, any order with $b_{q_k} > b_{q_{k+1}}$ is worse by exactly $b_{q_k} - b_{q_{k+1}}$, so for distinct bursts the shortest-first order is the only optimal one.

## History

Smith (1956) proved that ordering jobs by processing time divided by weight minimizes the weighted sum of completion times on one machine; the case of equal weights is the shortest-first order. The operating-systems textbooks state the result for the mean waiting time of a set of processes and give the exchange argument (Silberschatz, Galvin and Gagne, Section 5.3.2). Schrage (1968) proved the optimality of the preemptive rule SRPT for jobs with arrivals.

## References
