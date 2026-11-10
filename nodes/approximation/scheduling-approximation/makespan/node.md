---
tag: FEC9RS
kind: definition
slug: makespan
name: Makespan
aliases:
- completion time of the schedule
- maximum completion time
- schedule length
- C_max
area: approximation/scheduling-approximation
level: intro
summary: The completion time of the last job in a schedule, the objective of most scheduling problems.
prereqs: [scheduling-problem]
see_also: [makespan-minimization, makespan-lower-bounds, scheduling-notation, preemptive-makespan-scheduling, machine-covering, bin-packing, list-scheduling, lateness-and-tardiness]
sources:
  - paper: doi:10.1016/S0167-5060(08)70356-X
    title: "R. L. Graham, E. L. Lawler, J. K. Lenstra and A. H. G. Rinnooy Kan, Optimization and approximation in deterministic sequencing and scheduling: a survey, Annals of Discrete Mathematics 5, 1979"
    locator: Section 2.4 (optimality criteria, the definition of C_max as the maximum completion time)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 2, Section 2.1 (the objective functions, makespan) and Section 2.3 (classes of schedules, non-delay schedules)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.3 (the makespan of a schedule on identical parallel machines)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 11.1 (the load of a machine and the makespan of an assignment)
---

The makespan of a schedule is the time at which its last job ends: $C_{\max} = \max_j C_j$, where $C_j$ is the completion time of job $j$. It is the length of the schedule when all jobs are available at time $0$, and it is the objective of [makespan minimization](/makespan-minimization/), of most approximation results in scheduling, and of the shop problems. On parallel machines without idle time, the makespan is the largest machine load.

## Definition

Let a schedule $S$ of $n$ jobs on $m$ machines be given, in any [machine environment](/machine-environments/). Each job $j$ has a completion time $C_j(S) \ge 0$, the time when its last part ends. The **makespan** of $S$ is

$$C_{\max}(S) = \max_{1 \le j \le n} C_j(S),$$

and $C_{\max}(S) = 0$ when $n = 0$. In the [three-field notation](/scheduling-notation/), the objective $\gamma = C_{\max}$ asks for a feasible schedule of minimum makespan; its value is written $C^*_{\max}$ or $\mathrm{OPT}$.

**Loads.** For an assignment $\sigma : \{1, \ldots, n\} \to \{1, \ldots, m\}$ of jobs to machines, the load of machine $i$ is $L_i = \sum_{j : \sigma(j) = i} p_{ij}$, where $p_{ij} = p_j$ on identical machines. A machine that runs its jobs one after another from time $0$, with no idle time, finishes at $L_i$. So for independent jobs without release dates,

$$C_{\max} = \max_{1 \le i \le m} L_i ,$$

and a schedule is the same thing as an assignment. This is the form used in [list scheduling](/list-scheduling/), [LPT](/longest-processing-time-first/) and the approximation schemes.

**Basic facts.**

1. *Regular.* If no $C_j$ goes up, the makespan does not go up. So it is never useful to delay a job without a reason, and for $P \mid\mid C_{\max}$ there is an optimal schedule with no idle time.
2. *Single machine.* On one machine with all jobs available at time $0$, every schedule without idle time has $C_{\max} = \sum_j p_j$. With release dates, $1 \mid r_j \mid C_{\max}$ is solved by taking the jobs in order of release date.
3. *Lower bounds.* On identical machines, $C_{\max} \ge \frac{1}{m} \sum_j p_j$ and $C_{\max} \ge \max_j p_j$ for every schedule. The page [makespan lower bounds](/makespan-lower-bounds/) proves these and stronger bounds.
4. *Bin packing duality.* On identical machines, there is a schedule with $C_{\max} \le C$ if and only if the numbers $p_j$ fit into $m$ bins of capacity $C$. So makespan minimization asks for the smallest capacity at which $m$ bins are enough, while [bin packing](/bin-packing/) asks for the smallest number of bins of a fixed capacity. [MULTIFIT](/multifit-algorithm/) is built on this duality.
5. *Relation to lateness.* With all due dates $d_j = 0$, $L_{\max} = \max_j (C_j - d_j) = C_{\max}$. So $C_{\max}$ is a special case of $L_{\max}$, and every algorithm for $L_{\max}$ also minimizes the makespan.
6. *Utilization.* The fraction of machine time that is busy is $\sum_j p_j / (m \, C_{\max})$ on identical machines. A small makespan is the same as a high utilization.

## Examples and non-examples

**Example.** Three identical machines and the jobs $p = (2, 3, 4, 6, 2, 2)$, taken in this order by [list scheduling](/list-scheduling/). Jobs 1, 2 and 3 start at time $0$ on machines 1, 2 and 3. Job 4 goes to machine 1 at time $2$ and ends at $8$. Job 5 goes to machine 2 at time $3$ and ends at $5$. Job 6 goes to machine 3 at time $4$ and ends at $6$. The completion times are $C = (2, 3, 4, 8, 5, 6)$, so $C_{\max} = 8$ and the loads are $(8, 5, 6)$. The optimal makespan is $7$, for example with the machines $\{6\}$, $\{4, 3\}$ and $\{2, 2, 2\}$.

**Example with idle time.** Two machines and two jobs of length $3$, with the precedence $1 \to 2$. Job 2 cannot start before time $3$, so $C_{\max} = 6$ for each schedule. If the jobs are on different machines, the loads are $3$ and $3$, and the largest load is smaller than the makespan. Under precedence constraints or release dates, $C_{\max} = \max_i L_i$ is false in general.

**Example with preemption.** Two machines and three jobs of length $1$. Without preemption, two jobs share a machine and $C_{\max} = 2$. With preemption, the optimum is $3/2$: machine 1 runs job 1 in $[0, 1)$ and the first half of job 2 in $[1, 3/2)$, and machine 2 runs the second half of job 2 in $[0, 1/2)$ and job 3 in $[1/2, 3/2)$. Job 2 never runs on both machines at once. See [McNaughton's wrap-around rule](/mcnaughton-wrap-around/).

**Non-examples.**

- The total completion time $\sum_j C_j$ is not the makespan. In the first example it is $2 + 3 + 4 + 8 + 5 + 6 = 28$. The two objectives can disagree: [shortest processing time first](/shortest-processing-time-first/) minimizes $\sum_j C_j$ on identical machines, but it can give a poor makespan.
- The average load $\frac{1}{m} \sum_j p_j$ is not the makespan. It is a lower bound, and in the first example it is $19/3$, while the optimum is $7$.
- The time from the first start to the last end is not the makespan when release dates are present. The makespan is measured from time $0$.
- The smallest load $C_{\min} = \min_i L_i$ is a different objective, which is maximized in [machine covering](/machine-covering/).

## Related definitions

- [Makespan minimization](/makespan-minimization/): the problem $P \mid\mid C_{\max}$ and the map of its results.
- [Makespan lower bounds](/makespan-lower-bounds/): the bounds that approximation proofs compare with.
- [Preemptive makespan scheduling](/preemptive-makespan-scheduling/): $C_{\max}$ when jobs can be split.
- [Lateness and tardiness](/lateness-and-tardiness/): the objectives built from due dates.
- [Scheduling notation](/scheduling-notation/): where $C_{\max}$ appears as the field $\gamma$.
- [Machine covering](/machine-covering/): the max-min objective $C_{\min}$.

## References
