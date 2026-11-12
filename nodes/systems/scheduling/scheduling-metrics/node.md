---
tag: NMZMS9
kind: concept
slug: scheduling-metrics
name: Scheduling metrics
aliases:
- waiting time
- scheduling criteria
area: systems/scheduling
level: intro
summary: "Measures that compare CPU schedulers: turnaround, waiting and response time per job, and throughput, CPU utilization, fairness and stretch for the whole run."
prereqs: [scheduling-problem]
see_also: [cpu-scheduling, flow-time, stretch, utilization, round-robin, fcfs-scheduling, work-conserving-scheduling, makespan]
sources:
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5, Section 5.2 (scheduling criteria, CPU utilization, throughput, turnaround, waiting and response time)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces, version 1.10
    locator: Chapter 7, Scheduling, Introduction (turnaround time as completion minus arrival, response time as first run minus arrival)
  - book: isbn:9781107027503
    title: Mor Harchol-Balter, Performance Modeling and Design of Computer Systems, Queueing Theory in Action, Cambridge University Press, 2013
    locator: Chapter 6 (Little's law and the operational laws) and Part VII, Chapter 28 (performance metrics for scheduling, response time and slowdown)
  - paper: "Raj Jain, Dah-Ming Chiu and William R. Hawe, A quantitative measure of fairness and discrimination for resource allocation in shared computer systems, DEC Research Report TR-301, 1984"
    locator: the fairness index (sum x)^2 / (n sum x^2) and its properties
---

Scheduling metrics are the numbers that say how good a [CPU schedule](/cpu-scheduling/) is. Per job they are the turnaround time (completion minus arrival), the waiting time (turnaround minus burst) and the response time (first run minus arrival), and the [stretch](/stretch/) (turnaround divided by burst). For the whole run they are the throughput, the CPU [utilization](/utilization/) and the fairness. A scheduler cannot make all of them best at once, so a policy is a choice of which ones to favor.

## In plain words

When you compare two ways to run the same jobs, you need numbers. For each job you can ask: how long from the moment it arrived until it was done? How much of that time did it spend standing in line? How long did it wait before it ran at all, even for a moment? A person at a keyboard cares about the last question most.

For the whole machine you can ask: how many jobs did it finish per second? What fraction of the time was the processor busy? Did every job get a fair part of the processor?

A scheduler that is very good on one of these numbers is often worse on another. Running each job a little in turn makes the first answer come quickly, but the last job ends later.

## The idea

Take one CPU and $n$ jobs. Job $j$ arrives at $a_j$, needs a CPU burst of $b_j > 0$, first gets the CPU at $s_j$ and completes at $C_j$. In a schedule with I/O, $b_j$ is the total CPU time of the job.

### Per-job metrics

| metric | definition | what it shows |
|---|---|---|
| turnaround time | $T_j = C_j - a_j$ | the time in the system; in scheduling theory, the [flow time](/flow-time/) $F_j$ |
| waiting time | $W_j = T_j - b_j$ | the time spent ready but not running |
| response time | $R_j = s_j - a_j$ | the delay before the first run |
| stretch, or slowdown | $S_j = T_j / b_j$ | the factor by which the job ran slower than alone on the CPU |

Some facts follow at once from the definitions:

- $0 \le R_j \le W_j$, because the job is ready and not running from $a_j$ to $s_j$. In a nonpreemptive schedule of single-burst jobs, $R_j = W_j$.
- $S_j \ge 1$, with equality if and only if the job never waits.
- For a job with I/O, Silberschatz defines the waiting time as the total time in the ready queue. That equals $T_j - b_j$ minus the time in I/O, so the formula $T_j - b_j$ is right only for jobs with no I/O.

Silberschatz defines the response time as the time from a request to the first output. The definition $s_j - a_j$ of Arpaci-Dusseau measures the time to the first run, which is a lower bound on it and is what a simulator can measure.

### Metrics of the whole run

Let the run cover the interval $[t_0, t_1]$, from the first arrival to the last completion.

- **Throughput** $X = n / (t_1 - t_0)$, the jobs completed per unit of time.
- **CPU utilization** $U = B / (t_1 - t_0)$, where $B$ is the time the CPU runs jobs. Time in the dispatcher and idle time do not count. See [utilization](/utilization/).
- **Averages and tails.** The mean of $T_j$, $W_j$ or $R_j$; also the maximum, the variance, or a high percentile. Silberschatz notes that an interactive system may prefer a small variance of the response time to a small mean.
- **Fairness.** There is no single definition. Two common measures are the maximum stretch, which treats short and long jobs alike, and Jain's index $J(x) = (\sum_i x_i)^2 / (n \sum_i x_i^2)$ of the shares $x_i$ of the CPU that comparable processes receive. $J$ is 1 when all shares are equal and $1/n$ when one process gets everything.

### Relations between them

- Over a single-burst trace, the sum of the turnarounds equals the area under the number of jobs in the system, $\int_{t_0}^{t_1} N(t)\,dt = \sum_j T_j$. Dividing by $t_1 - t_0$ gives Little's law $\bar N = X \bar T$ as an exact identity; see [utilization](/utilization/).
- The mean waiting time and the mean turnaround differ by the mean burst, $\bar T = \bar W + \bar b$, which does not depend on the schedule. So a policy that minimizes one minimizes the other.
- Every [work-conserving](/work-conserving-scheduling/) policy has the same busy periods on the same single-burst trace, so the same $U$ and the same $t_1$. On such a trace the throughput and utilization do not tell these policies apart; the per-job metrics do.

## Examples

Four jobs with times in milliseconds: P1 arrives at 0 with burst 8, P2 at 1 with 4, P3 at 2 with 9, P4 at 3 with 5. Under [round robin](/round-robin/) with quantum 4, the schedule is P1 on $[0,4)$, P2 on $[4,8)$, P3 on $[8,12)$, P4 on $[12,16)$, P1 on $[16,20)$, P3 on $[20,24)$, P4 on $[24,25)$ and P3 on $[25,26)$.

| job | arrival | burst | first run | completion | turnaround | waiting | response | stretch |
|---|---|---|---|---|---|---|---|---|
| P1 | 0 | 8 | 0 | 20 | 20 | 12 | 0 | 5/2 |
| P2 | 1 | 4 | 4 | 8 | 7 | 3 | 3 | 7/4 |
| P3 | 2 | 9 | 8 | 26 | 24 | 15 | 6 | 8/3 |
| P4 | 3 | 5 | 12 | 25 | 22 | 17 | 9 | 22/5 |
| mean | | | | | 18.25 | 11.75 | 4.5 | |

Under [FCFS](/fcfs-scheduling/) the same jobs run on $[0,8)$, $[8,12)$, $[12,21)$ and $[21,26)$. The turnarounds are 8, 11, 19 and 23, with mean 15.25. The waiting times are 0, 7, 10 and 18, with mean 8.75, and the response times are the same as the waiting times. The maximum stretch is $23/5 = 4.6$, against $22/5 = 4.4$ for round robin.

| metric | round robin, quantum 4 | FCFS |
|---|---|---|
| mean turnaround | 18.25 | 15.25 |
| mean waiting | 11.75 | 8.75 |
| mean response | 4.5 | 8.75 |
| maximum stretch | 4.4 | 4.6 |
| throughput | 4/26 per ms | 4/26 per ms |
| CPU utilization | 100% | 100% |

Round robin almost halves the mean response time, and FCFS wins on turnaround and waiting by 3 ms each. The throughput and the utilization are equal, because both policies are work-conserving and the jobs have no I/O. In both schedules the area under the number of jobs in the system is the sum of the turnarounds (73 and 61), and the identity $\bar N = X \bar T$ holds: $73/26 = (4/26)(73/4)$.

Jain's index of the shares $(8, 4, 4, 0)$ is $16^2 / (4 \cdot 96) = 2/3$, and of four equal shares it is 1.

## Where it is used

- [CPU scheduling](/cpu-scheduling/) and its policies: [FCFS](/fcfs-scheduling/) is simple and has poor waiting times, [shortest-job-first](/shortest-job-first/) has the least mean waiting time ([proof](/sjf-optimality/)), and [round robin](/round-robin/) has a good response time.
- Scheduling theory uses the same quantities under other names: [flow time](/flow-time/) for turnaround, [stretch](/stretch/), and the [makespan](/makespan/), which is $t_1$ when all jobs arrive at 0.
- Queueing theory gives the means of these metrics for random arrivals, and the [work-conserving](/work-conserving-scheduling/) and [utilization](/utilization/) pages give the laws that tie them together.
- Real-time systems replace these metrics by a yes or no answer: does each job meet its deadline? See [real-time scheduling](/real-time-scheduling/).

## References
