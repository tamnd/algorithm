---
tag: YHS6SD
kind: problem
slug: open-shop-scheduling
name: Open shop scheduling
aliases:
- O||Cmax
- openshop scheduling
area: approximation/scheduling-approximation
level: advanced
summary: Each job needs all machines in any order; minimize makespan.
prereqs: [scheduling-notation, machine-environments, makespan, np-hard]
see_also: [flow-shop-scheduling, job-shop-scheduling, edge-coloring, konig-theorem, birkhoff-von-neumann-decomposition, preemptive-makespan-scheduling, bipartite-matching, makespan-lower-bounds]
sources:
  - paper: "T. Gonzalez and S. Sahni, Open shop scheduling to minimize finish time, Journal of the ACM 23(4), 1976, pages 665 to 679"
    locator: the linear time algorithm for two machines, the NP-hardness for three machines, and the preemptive algorithm
  - paper: "D. P. Williamson, L. A. Hall, J. A. Hoogeveen, C. A. J. Hurkens, J. K. Lenstra, S. V. Sevast'janov and D. B. Shmoys, Short shop schedules, Operations Research 45(2), 1997, pages 288 to 294"
    locator: the NP-hardness of deciding makespan at most 4, which rules out ratios below 5/4
  - paper: "S. V. Sevastianov and G. J. Woeginger, Makespan minimization in open shops: a polynomial time approximation scheme, Mathematical Programming 82, 1998"
    locator: the PTAS for a fixed number of machines
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 6, Shop Scheduling Problems (open shop problems)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 8, Open Shops (Deterministic)
---

Open shop scheduling, written $O \mid\mid C_{\max}$, is the shop problem where each job has one operation on each machine and the operations of a job may run in any order. Each machine runs one operation at a time, and each job is on one machine at a time. The goal is the least [makespan](/makespan/). Two simple lower bounds, the largest machine load and the largest job length, control the problem. For two machines the optimum always equals the larger of the two (Gonzalez and Sahni 1976), and with preemption it does for any number of machines. Without preemption, three machines already make the problem NP-hard, and any *dense* schedule, which never leaves a machine idle when it could work, is within a factor 2 of the optimum.

## In plain words

Think of a medical check-up. Each patient must see every doctor once, in any order, and each doctor sees one patient at a time. You plan who sees whom when, so that the last patient leaves as early as possible.

Two things always limit you. The busiest doctor needs all of their appointments, and the patient with the most appointments needs all of theirs, one after another. With two doctors, a careful plan always meets the larger of these two limits. With more doctors, perfect plans are hard to find. But a simple rule is never worse than twice the best: whenever a doctor is free and some patient who still needs that doctor is free too, start the visit.

## Definition

**Input.** Integers $m \ge 1$ and $n \ge 1$, and times $p_{ij} \ge 0$ for each machine $i$ and job $j$. Job $j$ has one operation on each machine $i$, of length $p_{ij}$, and operations of length 0 can be ignored.

**Output.** A start time $S_{ij}$ for each operation, such that no two operations on the same machine overlap and no two operations of the same job overlap. The order of the operations of a job is free.

**Goal.** Minimize $C_{\max} = \max_{i, j} (S_{ij} + p_{ij})$. The least value is $\mathrm{OPT}$.

*Ratio convention.* This is a minimization problem. An algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. All ratios here are absolute and worst case.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of jobs and the number of machines |
| $p_{ij}$ | the time of the operation of job $j$ on machine $i$ |
| $\Pi_i$, $\Pi_{\max}$ | the load $\sum_j p_{ij}$ of machine $i$, and $\max_i \Pi_i$ |
| $P_j$, $P_{\max}$ | the length $\sum_i p_{ij}$ of job $j$, and $\max_j P_j$ |
| $\mathrm{LB}$ | $\max(\Pi_{\max}, P_{\max})$ |
| $\mathrm{OPT}$, $\mathrm{ALG}$ | the optimal makespan, and the makespan of an algorithm |

## Variants

- **Two machines, $O2 \mid\mid C_{\max}$.** Polynomial: $\mathrm{OPT} = \mathrm{LB}$, and Gonzalez and Sahni (1976) build such a schedule in $O(n)$ time.
- **Three machines, $O3 \mid\mid C_{\max}$.** NP-hard (Gonzalez and Sahni 1976), but only in the ordinary sense as far as is known: whether it is strongly NP-hard is a well known open question.
- **Preemption, $O \mid \mathrm{pmtn} \mid C_{\max}$.** Polynomial with $\mathrm{OPT} = \mathrm{LB}$ for every $m$. The matrix $(p_{ij})$ can be padded to a matrix with all row and column sums equal to $\mathrm{LB}$, and a [Birkhoff-von Neumann decomposition](/birkhoff-von-neumann-decomposition/) of it into weighted matchings gives the schedule.
- **Unit times, $O \mid p_{ij} = 1 \mid C_{\max}$.** The operations are the edges of a bipartite graph between machines and jobs. By [König's edge coloring theorem](/konig-theorem/), the edges can be colored with $\Delta = \mathrm{LB}$ colors, and color $t$ gives the operations of time slot $t$. See [edge coloring](/edge-coloring/).
- **Other objectives.** $O2 \mid\mid L_{\max}$ and $O2 \mid\mid \sum C_j$ are NP-hard.

## Examples

**Two machines.** Take these times, with rows for the machines:

| | job 1 | job 2 | job 3 | load |
|---|---|---|---|---|
| machine 1 | 3 | 2 | 4 | 9 |
| machine 2 | 2 | 5 | 1 | 8 |
| job length | 5 | 7 | 5 | |

So $\mathrm{LB} = \max(9, 7) = 9$. The schedule below meets it, so $\mathrm{OPT} = 9$:

| | 0 to 3 | 3 to 5 | 5 to 7 | 7 to 8 | 8 to 9 |
|---|---|---|---|---|---|
| machine 1 | job 1 | job 3 | job 3 | job 2 | job 2 |
| machine 2 | job 2 | job 2 | job 1 | job 3 | idle |

**Three machines, a gap above LB.** Take these times:

| | job 1 | job 2 | job 3 | load |
|---|---|---|---|---|
| machine 1 | 3 | 0 | 1 | 4 |
| machine 2 | 0 | 3 | 3 | 6 |
| machine 3 | 3 | 0 | 1 | 4 |
| job length | 6 | 3 | 5 | |

Here $\mathrm{LB} = 6$, but $\mathrm{OPT} = 7$. In a schedule of makespan 6, machine 2 must work all the time, so job 3 is on machine 2 during $[0, 3]$ or during $[3, 6]$. Job 1 also has length 6, so it is on machines 1 and 3 all the time, one in $[0, 3]$ and the other in $[3, 6]$. Job 3 must use machines 1 and 3 in the half where it is not on machine 2. In that half, job 1 uses one of these machines for the whole half, so there is no room for job 3. So no schedule of makespan 6 exists, and a schedule of makespan 7 does.

**A dense schedule that is not optimal.** Take two machines with times $(2, 2, 3)$ on machine 1 and $(1, 3, 3)$ on machine 2, so $\mathrm{LB} = 7$, which is also the optimum. The dense rule that always starts the free job with the lowest number runs, on machine 1, job 1 in $[0, 2]$, job 3 in $[2, 5]$ and job 2 in $[5, 7]$, and on machine 2, job 2 in $[0, 3]$, job 1 in $[3, 4]$, then waits, and runs job 3 in $[5, 8]$. Its makespan is 8.

## Known algorithms

| algorithm | ratio $\rho$ | tight for the algorithm | time |
|---|---|---|---|
| any dense schedule | below 2 | the proved bound | $O(nm \log(nm))$ with an event queue |
| Gonzalez and Sahni 1976, $m = 2$ | exact | not applicable | $O(n)$ |
| Gonzalez and Sahni 1976, preemptive | exact | not applicable | polynomial |
| edge coloring, unit times | exact | not applicable | polynomial |
| Sevastianov and Woeginger 1998, fixed $m$ | $1 + \varepsilon$ (PTAS) | not applicable | polynomial for fixed $m$ and $\varepsilon$ |

**Dense schedules are within 2.** Let the last operation to finish be $O_{ij}$, ending at $C_{\max}$. At each moment before it starts, either machine $i$ is busy, or job $j$ is busy on another machine, since otherwise the dense rule would start $O_{ij}$. The first kind of moment has total length at most $\Pi_i - p_{ij}$, and the second at most $P_j - p_{ij}$. So
$$C_{\max} \le (\Pi_i - p_{ij}) + (P_j - p_{ij}) + p_{ij} \le \Pi_{\max} + P_{\max} - p_{ij} < 2\,\mathrm{LB} \le 2\,\mathrm{OPT}$$
when $p_{ij} > 0$.

**The two-machine algorithm (sketch only).** Write $a_j$ and $b_j$ for the times of job $j$ on machines 1 and 2. Gonzalez and Sahni split the jobs into the set with $a_j \le b_j$ and the set with $a_j > b_j$, treat one job with a largest operation on its own, and build from the two sets two blocks that each run on the two machines without conflict. Joining the blocks in the right way gives a schedule of makespan $\mathrm{LB}$. The construction and its case analysis are in the paper and are not given here.

## Bounds

- **Lower bound.** $\mathrm{OPT} \ge \mathrm{LB} = \max(\Pi_{\max}, P_{\max})$, since a machine runs one operation at a time and a job is on one machine at a time. The bound is exact for two machines and for preemptive schedules, but not in general, as the three-machine example shows. Since dense schedules end before $2\,\mathrm{LB}$, the ratio $\mathrm{OPT}/\mathrm{LB}$ is always below 2.
- **No ratio below 5/4 when $m$ is part of the input.** Williamson, Hall, Hoogeveen, Hurkens, Lenstra, Sevast'janov and Shmoys (1997) showed that deciding $\mathrm{OPT} \le 4$ is NP-hard for the open shop with integer times, while $\mathrm{OPT} \le 3$ is polynomial.
- **Fixed $m$.** For each fixed $m$ there is a PTAS (Sevastianov and Woeginger 1998). For $m$ part of the input, a ratio strictly below 2 that holds for all instances is a long standing open question, and the factor 2 of dense schedules is the best known guarantee in general.

## Reductions

**Preemptive case to matchings.** Pad the $m \times n$ matrix $(p_{ij})$ with extra rows and columns so that every row and column sums to $\mathrm{LB}$. By the [Birkhoff-von Neumann theorem](/birkhoff-von-neumann-decomposition/), the padded matrix is a sum of permutation matrices with positive weights. Each permutation matrix is a set of operations with distinct machines and distinct jobs, so it can run at once, and its weight is the length of that slot. The slots add up to $\mathrm{LB}$.

**Unit times to edge coloring.** A schedule of makespan $T$ with unit times is a proper coloring of the edges of the bipartite graph of operations with $T$ colors. [König's theorem](/konig-theorem/) says that a bipartite graph of maximum degree $\Delta$ has such a coloring with $\Delta$ colors, and $\Delta = \mathrm{LB}$ here.

**From partition, three machines.** Gonzalez and Sahni reduce [partition](/partition-problem/) to $O3 \mid\mid C_{\max}$, which gives NP-hardness in the ordinary sense.

## Applications

- Medical check-ups, school examinations and teacher-class timetables, where each person must meet each station once and the order is free.
- Testing and repair, where each unit must pass a set of tests in any order.
- Communication in networks, where each pair of nodes must exchange a message and each node can talk to one other node at a time; the unit time case is then edge coloring.

## References
