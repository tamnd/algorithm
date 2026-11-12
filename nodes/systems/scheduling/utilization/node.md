---
tag: KNYA42
kind: definition
slug: utilization
name: Processor utilization
aliases:
- CPU utilization
- processor utilization factor
- server utilization
area: systems/scheduling
level: intro
summary: "The fraction of time a processor is busy. For periodic tasks it is U = sum of C_i/T_i, for a queue rho = lambda/mu; Little's law L = lambda W links it to delay."
prereqs: [scheduling-metrics, work-conserving-scheduling]
see_also: [liu-layland-utilization-bound, periodic-task-model, hyperperiod, earliest-deadline-first, rate-monotonic-scheduling, schedulability-analysis, real-time-scheduling, cpu-scheduling]
sources:
  - paper: doi:10.1287/opre.9.3.383
    title: John D. C. Little, A proof for the queuing formula L = lambda W, Operations Research 9(3), 1961
    locator: pages 383 to 387
  - paper: "C. L. Liu and James W. Layland, Scheduling algorithms for multiprogramming in a hard-real-time environment, Journal of the ACM 20(1), 1973"
    locator: pages 46 to 61 (the processor utilization factor U = sum C_i / T_i of a set of periodic tasks)
  - paper: "Peter J. Denning and Jeffrey P. Buzen, The operational analysis of queueing network models, ACM Computing Surveys 10(3), 1978"
    locator: pages 225 to 261 (the utilization law U = X S and Little's law as operational laws on measured quantities)
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5, Section 5.2 (scheduling criteria, CPU utilization from about 40 percent on a lightly loaded system to 90 percent on a heavily loaded one) and Section 5.8.2 (queueing models and Little's formula)
---

## Definition

**Measured utilization.** Let a processor run a schedule, and let $B(t_0, t_1)$ be the time in the interval $[t_0, t_1)$ during which it runs some job. The *utilization* over the interval is

$$U = \frac{B(t_0, t_1)}{t_1 - t_0}, \qquad 0 \le U \le 1.$$

On $m$ processors, the utilization is the total busy time divided by $m(t_1 - t_0)$. Let $X$ be the number of jobs completed in the interval divided by its length, the *throughput*, and $S$ the busy time per completed job, the *mean service time*. Then $B = (t_1 - t_0) \cdot X \cdot S$, which is the *utilization law*

$$U = X \cdot S.$$

**Offered load of a queue.** In a queue with one server, jobs arrive at rate $\lambda$ and need service of mean $1/\mu$. The *offered load* or *traffic intensity* is

$$\rho = \frac{\lambda}{\mu} = \lambda\, E[S].$$

If $\rho < 1$ and the queue reaches a steady state, the server is busy a fraction $\rho$ of the time, so the long-run utilization is $\rho$. If $\rho > 1$, work arrives faster than it can be done and the queue grows without bound.

**Utilization of a periodic task set.** In the [periodic task model](/periodic-task-model/), task $i$ releases a job of worst-case execution time $C_i$ every $T_i$ time units. The *processor utilization factor* of the task set (Liu and Layland 1973) is

$$U = \sum_{i=1}^{n} \frac{C_i}{T_i}.$$

It is the fraction of processor time that the tasks need in the worst case. Over one [hyperperiod](/hyperperiod/) $H = \operatorname{lcm}(T_1, \ldots, T_n)$, the jobs released need exactly $\sum_i (H/T_i)\,C_i = U \cdot H$ units of time. So $U \le 1$ is necessary for any schedule on one processor to meet all deadlines.

**Little's law.** In a system where jobs arrive at rate $\lambda$ and each stays a mean time $W$, the mean number of jobs in the system is

$$L = \lambda W$$

(Little 1961). On a finite trace, it is an exact identity. Let every job $j$ arrive at $a_j$ and leave at $c_j$, both in $[t_0, t_1)$, and let $N(t)$ be the number of jobs present. Each job adds 1 to $N$ for exactly $c_j - a_j$ time units, so

$$\int_{t_0}^{t_1} N(t)\,dt = \sum_{j} (c_j - a_j).$$

Dividing by $t_1 - t_0$ gives $L = \lambda W$, with $L$ the time average of $N$, $\lambda = n/(t_1 - t_0)$ and $W$ the mean time in system. Applied to the server alone, where at most one job is present, the same identity gives $U = \lambda S$, the utilization law.

## Examples and non-examples

**A measured trace.** Jobs arrive at times 0, 1, 2, 10 and 11 with work 4, 2, 1, 2 and 1, and run under FCFS. The processor is busy on $[0, 7)$ and $[10, 13)$, so over $[0, 13)$ it is busy 10 units and $U = 10/13$. Five jobs complete, so $X = 5/13$, and $S = 10/5 = 2$; indeed $X \cdot S = 10/13$. Every [work-conserving](/work-conserving-scheduling/) scheduler has the same busy periods, so the same $U$.

The completion times under FCFS are 4, 6, 7, 12 and 13, and the times in system are 4, 5, 5, 2 and 2, with sum 18. So $\int N\,dt = 18$, $L = 18/13$, $\lambda = 5/13$ and $W = 18/5$, and $\lambda W = 18/13 = L$. Preemptive priority to jobs 3, 4 and 5 gives the times in system 5, 6, 1, 2 and 2, with sum 16: $L$ and $W$ change, $U$ and the identity $L = \lambda W$ do not.

**A queue.** Requests arrive at rate $\lambda = 0.8$ per second and need 1 second of service on average, so $\rho = 0.8$. If the queue is M/M/1, the mean number in the system is $\rho/(1 - \rho) = 4$, and Little's law gives the mean time in system $W = L/\lambda = 5$ seconds. At $\rho = 0.9$ the mean number is 9, so the delay grows fast as the utilization nears 1.

**A periodic task set.** Tasks $(C_i, T_i) = (1, 4), (2, 6), (3, 12)$ have $U = 1/4 + 1/3 + 1/4 = 5/6$. The hyperperiod is 12, and the jobs released in it need $3 \cdot 1 + 2 \cdot 2 + 1 \cdot 3 = 10 = (5/6) \cdot 12$ units. Since $U \le 1$, [earliest deadline first](/earliest-deadline-first/) meets all deadlines when the deadlines equal the periods. The [Liu and Layland bound](/liu-layland-utilization-bound/) for three tasks under [rate-monotonic scheduling](/rate-monotonic-scheduling/) is $3(2^{1/3} - 1) \approx 0.780$, below $5/6$, so that test does not decide, and an exact [schedulability analysis](/schedulability-analysis/) is needed.

**Non-examples.**

- *A sum above 1 is not a fraction of time.* A task set with $\sum_i C_i/T_i = 1.2$ has no utilization of 120 percent; it asks for more time than one processor has, and some deadline is missed in every schedule. On $m$ processors, the need is $U \le m$.
- *Busy is not useful.* A process that spins in a loop while it waits for a lock keeps the processor busy and raises $U$ without doing work. Context-switch time also counts as busy time in most measurements.
- *The load average is not utilization.* The Unix load average is a decaying average of the number of processes that are running or ready, so it can be above 1 on one processor; it is closer to $L$ than to $U$.
- *Utilization is not a delay.* Two systems with the same $U$ can have very different waiting times, since the delay depends on the variability of arrivals and service, as in the Pollaczek and Khinchine formula, and on the order of service.

## Related definitions

- **Throughput** $X$ is the number of completions per time unit; see [scheduling metrics](/scheduling-metrics/). Over an interval in which the system starts and ends empty, the throughput equals the arrival rate.
- **Busy period**: a maximal interval in which the processor is busy. On one processor, all work-conserving schedulers have the same busy periods, so they have the same measured utilization; see [work-conserving scheduling](/work-conserving-scheduling/).
- **Load** is used for both $\rho$ and $U$, and sometimes for the number of ready processes. *Offered load* is the work that arrives, *carried load* the work done; they differ when work is lost or dropped.
- **Utilization bounds** are values $U_{\mathrm{lub}}$ such that every task set with $U \le U_{\mathrm{lub}}$ is schedulable under a given policy: $n(2^{1/n} - 1)$ for rate-monotonic scheduling and 1 for EDF on one processor; see [Liu and Layland bound](/liu-layland-utilization-bound/).
- **Density** $\sum_i C_i / \min(D_i, T_i)$ replaces $T_i$ by the deadline when deadlines are shorter than periods. Density at most 1 is sufficient for EDF, but not necessary.

## References
