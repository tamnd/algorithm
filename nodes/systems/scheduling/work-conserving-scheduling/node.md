---
tag: VBE4E8
kind: concept
slug: work-conserving-scheduling
name: Work-conserving scheduler
aliases:
- work-conserving
- work-conserving discipline
- non-idling scheduler
area: systems/scheduling
level: intro
summary: "A scheduler that never idles while work waits. On one server, all such schedulers have the same unfinished work and busy periods; the order only moves waiting time between jobs."
prereqs: [cpu-scheduling, scheduling-metrics]
see_also: [utilization, fcfs-scheduling, priority-scheduling, round-robin, sjf-optimality, generalized-processor-sharing, packet-scheduling, disk-scheduling]
sources:
  - paper: "Leonard Kleinrock, A conservation law for a wide class of queueing disciplines, Naval Research Logistics Quarterly 12(2), 1965"
    locator: pages 181 to 192 (the conservation law for nonpreemptive work-conserving disciplines in M/G/1)
  - book: "Leonard Kleinrock, Queueing Systems, Volume 2, Computer Applications, Wiley, 1976"
    locator: Chapter 3, Priority Queueing (the M/G/1 conservation law and priority queues)
  - paper: "Alan Cobham, Priority assignment in waiting line problems, Operations Research 2(1), 1954"
    locator: pages 70 to 76 (mean waiting times of nonpreemptive priority classes)
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5, Section 5.3 (the scheduling algorithms FCFS, SJF, RR and priority, all of which keep the CPU busy while a process is ready)
---

A work-conserving scheduler never leaves a server idle while some job is waiting for it. On one server, this simple rule has a strong consequence, the *work conservation law*: for a given stream of arrivals, every work-conserving scheduler has the same unfinished work at every moment, and so the same busy periods and idle periods. [FCFS](/fcfs-scheduling/), [shortest-job-first](/shortest-job-first/), [round robin](/round-robin/) and [priority scheduling](/priority-scheduling/) are all work-conserving, so they differ only in which job gets the server, not in how much work is done. The order of service moves waiting time from one job to another, and Kleinrock's conservation law for M/G/1 queues says exactly how much can be moved.

## In plain words

A bakery has one oven and a pile of orders. A rule for the oven is work-conserving if the oven is never cold while an order is waiting. Under any such rule, the oven is busy at exactly the same times, and the pile of unbaked dough has the same total weight at every moment. The rule changes only which customer gets bread first.

So if one customer gets bread sooner, someone else gets it later. Giving priority to short orders makes the average wait short, but it does not make the oven finish the whole pile any earlier.

A rule that lets the oven go cold while orders wait, for example to wait for a better order, is not work-conserving.

## The idea

**Definition.** One server serves jobs at rate 1. Job $j$ arrives at time $a_j$ and needs work $b_j$. A scheduler is *work-conserving* if, at every moment when an arrived job is unfinished, the server is serving some job. We also assume that the scheduler does not create or destroy work: switches cost nothing, a preempted job resumes where it stopped, and the work of a job does not depend on the order. Preemption is allowed. On $m$ servers, work-conserving means that no server is idle while a job waits that could use it.

**The work conservation law.** Let $V(t)$ be the unfinished work at time $t$: the work that has arrived by $t$ minus the work done by $t$. On one server, $V$ is the same function for every work-conserving scheduler.

*Proof.* Order the arrivals $a_1 \le a_2 \le \cdots \le a_n$. Between two arrivals no work enters. A work-conserving server works at rate 1 whenever $V > 0$, and it cannot do work that has not arrived, so $V$ falls at rate 1 until it reaches 0 and then stays at 0. At an arrival, $V$ jumps by the work of the new job. So, with $V(a_0) = 0$ and $a_0 = a_1$,

$$V(a_k) = \max\bigl(0,\; V(a_{k-1}) - (a_k - a_{k-1})\bigr) + b_k, \qquad V(t) = \max\bigl(0,\; V(a_k) - (t - a_k)\bigr) \text{ for } a_k \le t < a_{k+1}.$$

This determines $V$ from the input alone, by induction on $k$, without reference to the order of service. $\square$

The server is busy exactly when $V(t) > 0$, so all work-conserving schedulers have the same busy periods, the same idle time, the same amount of work done by each time, and the same time at which all work is done. A busy period starts at an arrival when $V = 0$ and ends when the work that arrived in it is done. Other quantities do differ: the completion times of single jobs, the number of jobs in the system, and the mean waiting time.

**A weighted sum that is conserved.** For nonpreemptive work-conserving schedulers there is more. While job $j$ waits, its whole work $b_j$ is part of $V$; while it is served, its remaining work falls from $b_j$ to 0. So

$$\int_0^\infty V(t)\,dt = \sum_j b_j W_j + \sum_j \frac{b_j^2}{2},$$

where $W_j$ is the waiting time of $j$. The left side is the same for all work-conserving schedulers, and the last sum does not depend on the scheduler, so $\sum_j b_j W_j$ is the same for all nonpreemptive work-conserving schedulers. A scheduler can lower the plain sum $\sum_j W_j$ by serving short jobs first, as SJF does, but only by making long jobs wait more, in such a way that the sum weighted by work does not change. This sample-path form holds for any arrival stream; Schrage (1970) gave a proof for the G/G/1 queue.

**Kleinrock's conservation law.** Kleinrock (1965) stated the law for queues. Its hypotheses are:

1. one server, M/G/1: jobs come in $P$ classes, class $p$ arrives as a Poisson process of rate $\lambda_p$, and its service times are independent with the same distribution, with mean $E[S_p]$ and second moment $E[S_p^2]$, independent of the arrivals;
2. the load is $\rho = \sum_p \rho_p < 1$, where $\rho_p = \lambda_p E[S_p]$;
3. the discipline is work-conserving and nonpreemptive;
4. the choice of the next job may use the class, but within a class it does not depend on the service times, so that the waiting time of a job is independent of its own service time.

Then, with $W_p$ the mean waiting time of class $p$ in steady state,

$$\sum_{p=1}^{P} \rho_p W_p = \frac{\rho\, W_0}{1 - \rho}, \qquad W_0 = \sum_{p=1}^{P} \frac{\lambda_p E[S_p^2]}{2}.$$

$W_0$ is the mean remaining work of the job in service, as seen by an arriving job. The right side is the value for FCFS, where every class has the mean wait $W_0/(1 - \rho)$ of the Pollaczek and Khinchine formula. So any nonpreemptive discipline that ranks classes can only redistribute the load-weighted waiting time. Hypothesis 4 is needed: within one class, SJF uses the service times, and then the mean wait $W_p$ is lower than the law would allow, because the jobs that wait long are those with large $S$. The conserved quantity is the mean of $S \cdot W$, and it equals $E[S]\,E[W]$ only when $S$ and $W$ are independent.

## Examples

**Five jobs and five schedulers.** Jobs 1 to 5 arrive at times 0, 1, 2, 10 and 11 with work 4, 2, 1, 2 and 1. The unfinished work is $V(0) = 4$, $V(1) = 3 + 2 = 5$, $V(2) = 4 + 1 = 5$, then it falls to 0 at time 7; then $V(10) = 2$, $V(11) = 1 + 1 = 2$, and it falls to 0 at 13. So the busy periods are $[0, 7)$ and $[10, 13)$ for every work-conserving scheduler: FCFS, LCFS, nonpreemptive SJF, priority with or without preemption, and round robin with any quantum.

| scheduler | order in $[0,7)$ | waits of jobs 1 to 5 | $\sum_j W_j$ | $\sum_j b_j W_j$ |
|---|---|---|---|---|
| FCFS | 1, 2, 3 | 0, 3, 4, 0, 1 | 8 | 11 |
| nonpreemptive SJF | 1, 3, 2 | 0, 4, 2, 0, 1 | 7 | 11 |

SJF lowers the total wait from 8 to 7, and the weighted sum stays at 11.

**The convoy example.** Three jobs at time 0 with work 24, 3 and 3. FCFS gives waits 0, 24 and 27, SJF gives 6, 0 and 3. The totals are 51 and 9, but the weighted sums are $24 \cdot 0 + 3 \cdot 24 + 3 \cdot 27 = 153$ and $24 \cdot 6 + 3 \cdot 0 + 3 \cdot 3 = 153$. Both schedules end at time 30.

**Two priority classes.** Let $\lambda_1 = \lambda_2 = 1/4$ and let all service times be exponential with mean 1, so $E[S^2] = 2$, $\rho_1 = \rho_2 = 1/4$, $\rho = 1/2$ and $W_0 = (1/4 \cdot 2 + 1/4 \cdot 2)/2 = 1/2$. FCFS gives both classes the mean wait $W_0/(1 - \rho) = 1$. Nonpreemptive priority to class 1 gives, by Cobham's formulas $W_1 = W_0/(1 - \rho_1)$ and $W_2 = W_0/((1 - \rho_1)(1 - \rho))$, the waits $2/3$ and $4/3$. The weighted sums agree: $\frac14 \cdot \frac23 + \frac14 \cdot \frac43 = \frac12 = \frac14 \cdot 1 + \frac14 \cdot 1$.

**Non-examples.**

- *Inserted idle time.* Job A arrives at 0 with work 10, B at 1 with work 1. The schedule that idles on $[0,1)$ to serve B first has total wait 2, against 9 for the work-conserving nonpreemptive schedule (see [optimality of SJF](/sjf-optimality/)), but its busy period is $[1, 12)$ instead of $[0, 11)$. Optimal nonpreemptive schedules with arrivals are often not work-conserving.
- *Anticipatory disk scheduling.* After a read, the disk scheduler waits a short time for the next nearby read of the same process instead of moving the head at once; see [disk scheduling](/disk-scheduling/).
- *Rate limits and shapers.* A CPU quota that stops a group of processes after its share, or a traffic shaper that holds packets to a fixed rate, leaves the resource idle while work waits, on purpose.

**More than one server.** On two machines, the law fails. Three jobs at time 0 with work 4, 1 and 1: if the long job starts at once, all work ends at 4; if the two short jobs start first, the long one starts at 1 and ends at 5. Both schedules keep the machines busy while a job waits. One job cannot use two machines, so the rate at which work is done depends on how many jobs are left, and that depends on the order. This is why [makespan](/makespan/) on several machines is a hard problem and on one machine is not.

## Where it is used

- **CPU scheduling.** The classic policies are work-conserving, so the busy time of the CPU, and so its [utilization](/utilization/), do not depend on the policy. The policy decides only who waits. This is why [scheduling metrics](/scheduling-metrics/) such as waiting and response time, not throughput over a busy period, are what policies are judged by.
- **Queueing analysis.** The conservation law gives the mean waits of priority classes from one another, and it is the starting point of the analysis of priority queues and of optimal ranking of classes, such as the $c\mu$ rule.
- **Packet scheduling.** [Generalized processor sharing](/generalized-processor-sharing/), [weighted fair queueing](/weighted-fair-queueing/) and [deficit round robin](/deficit-round-robin/) are work-conserving: a link that has a packet to send is never idle. Shapers and some rate-controlled schedulers in [packet scheduling](/packet-scheduling/) are not, and they trade link use for smooth output.
- **Proofs of optimality.** Many exchange proofs first remove idle time, using the fact that a work-conserving version of a schedule is no worse; the proof on [optimality of SJF](/sjf-optimality/) begins in this way when all jobs are present at time 0.

## References
