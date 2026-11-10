---
tag: D4MGPF
kind: algorithm
slug: list-scheduling
name: List scheduling
aliases:
- Graham's greedy algorithm
- Graham's list scheduling
- greedy load balancing
- Greedy-Balance
area: approximation/scheduling-approximation
level: core
summary: Assign each job in a given order to the currently least-loaded machine.
solves: [makespan-minimization]
model: real-ram
complexity:
  vars: {n: the number of jobs, m: the number of machines}
  time: {worst: Θ(m + n log m), average: Θ(m + n log m), best: Θ(m + n log m)}
  space: {extra: Θ(m)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1966
  people: [Ronald L. Graham]
  note: Graham proved the bound 2 - 1/m in 1966, for jobs with precedence constraints as well, and studied its anomalies in 1969.
prereqs: [makespan-minimization, makespan-lower-bounds, binary-heap]
see_also: [list-scheduling-bound, graham-anomalies, longest-processing-time-first, sorted-balance, online-makespan-minimization, list-scheduling-competitive-ratio, precedence-constrained-scheduling, greedy-algorithm]
sources:
  - paper: doi:10.1002/j.1538-7305.1966.tb01709.x
    title: "R. L. Graham, Bounds for certain multiprocessing anomalies, Bell System Technical Journal 45(9), 1966"
    locator: the definition of list schedules and the bound 2 - 1/m (pp. 1563-1581 for the paper)
  - paper: doi:10.1137/0117039
    title: "R. L. Graham, Bounds on multiprocessing timing anomalies, SIAM Journal on Applied Mathematics 17(2), 1969"
    locator: list schedules with precedence constraints, the anomalies, and the bound for the LPT order (pp. 416-429 for the paper)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.3 (the list scheduling algorithm and its factor 2 analysis)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 11.1 (Greedy-Balance and its factor 2 analysis)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 10 (Minimum makespan scheduling, the factor 2 algorithm)
---

List scheduling is the [greedy algorithm](/greedy-algorithm/) for [makespan minimization](/makespan-minimization/) that takes the jobs in a given order, the list, and gives each job to a machine whose load is the smallest at that moment. Graham introduced it in 1966 and proved that its makespan is at most $2 - 1/m$ times the optimum for every order, which makes it one of the first approximation algorithms with a proved ratio. It is an [online algorithm](/online-algorithm/): the choice for a job depends only on the jobs before it. With a [binary heap](/binary-heap/) of machine loads, it runs in $O(m + n \log m)$ time.

## In plain words

Jobs come one at a time, and you have a few equal workers. Each time a job comes, you look at who has the least work so far, and you give the job to that worker. You never move a job after you give it out, and you do not need to know which jobs will come later.

This rule is not always the best, but it is never far off. The worker who ends last got the last of his jobs at a moment when everyone else was at least as busy as he was. So, before that last job, the whole team was full, and the last job itself is no longer than the longest job. Both of these amounts are at most the best possible finish time, so the rule finishes within twice the best.

## The problem

The input is a number $m \ge 1$ of identical machines and a list of $n$ jobs with processing times $p_1, \ldots, p_n \ge 0$, in a given order. The output is an assignment of each job to a machine and a start time, where each machine runs its jobs one after another with no idle time. The goal is a small [makespan](/makespan/) $C_{\max}$, the largest load. This is $P \mid\mid C_{\max}$. Here $n$ is the number of jobs and $m$ is the number of machines.

*Ratio convention.* This is a minimization problem, and an algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. For list scheduling $\rho = 2 - 1/m$. The bound is absolute, it holds for every list order, and it is tight for the algorithm. The analysis compares with the two [lower bounds](/makespan-lower-bounds/) $\mathrm{OPT} \ge \frac1m \sum_j p_j$ and $\mathrm{OPT} \ge \max_j p_j$. The problem itself is not hard to approximate below $2 - 1/m$: a [PTAS](/hochbaum-shmoys-ptas/) exists.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of jobs and the number of machines |
| $p_j$ | the processing time of job $j$ |
| $S_j$, $C_j$ | the start and completion time of job $j$, with $C_j = S_j + p_j$ |
| $L_i$ | the current load of machine $i$ |
| $C_{\max}$, $\mathrm{OPT}$, $\mathrm{ALG}$ | the makespan, its optimum, and the makespan of list scheduling |

## The algorithm

```pseudo id=main
LIST-SCHEDULING(p[1 .. n], m)
L1  H ← a min-heap of the pairs (0, i) for i = 1 .. m, ordered by load, then by index
L2  for j ← 1 to n do
L3      (t, i) ← extract the pair with the smallest load from H
L4      σ(j) ← i, S[j] ← t
L5      insert (t + p[j], i) into H
L6  return σ, S, and C_max ← the largest load in H
```

The heap holds one pair (load, machine) for each machine. Line L3 finds a least loaded machine, line L4 starts job $j$ at the end of its current work, and line L5 puts the machine back with its new load.

## Example

Take $m = 3$ and the list $p = (2, 3, 4, 6, 2, 2)$, with ties broken by the smallest machine index.

| job $j$ | $p_j$ | loads before | machine | start $S_j$ | loads after |
|---|---|---|---|---|---|
| 1 | 2 | 0, 0, 0 | 1 | 0 | 2, 0, 0 |
| 2 | 3 | 2, 0, 0 | 2 | 0 | 2, 3, 0 |
| 3 | 4 | 2, 3, 0 | 3 | 0 | 2, 3, 4 |
| 4 | 6 | 2, 3, 4 | 1 | 2 | 8, 3, 4 |
| 5 | 2 | 8, 3, 4 | 2 | 3 | 8, 5, 4 |
| 6 | 2 | 8, 5, 4 | 3 | 4 | 8, 5, 6 |

The makespan is $8$. The optimum is $7$, with the machines $\{6\}$, $\{4, 3\}$ and $\{2, 2, 2\}$, and the ratio $8/7$ is below $2 - 1/3 = 5/3$. The long job $6$ came late, when all machines were already busy. [LPT](/longest-processing-time-first/) sorts the list first and gets $7$ on this input.

## Correctness

The invariant of the loop L2 to L5 is: before job $j$, the heap $H$ holds each machine exactly once, paired with the total time of the jobs $1, \ldots, j - 1$ that are on it. So line L4 starts job $j$ at the time when its machine becomes free, no two jobs of one machine overlap, and the output is a feasible schedule without idle time.

For the ratio, let job $l$ end last. At line L3 for job $l$, every machine had load at least $S_l$, so $m S_l \le \sum_{j \ne l} p_j$. Then

$$C_{\max} = S_l + p_l \le \frac1m \sum_j p_j + \left(1 - \frac1m\right) p_l \le \mathrm{OPT} + \left(1 - \frac1m\right)\mathrm{OPT}.$$

The full proofs are in [the correctness proof](proofs/correctness.md), and the theorem with its tight example is on [Graham's bound for list scheduling](/list-scheduling-bound/).

## Complexity

- **Time.** Line L1 builds the heap in $\Theta(m)$ time. Each of the $n$ rounds does one extract and one insert, each $\Theta(\log m)$, so the total is $\Theta(m + n \log m)$ in the [real RAM](/real-ram/) model. Line L6 reads $m$ loads.
- **Space.** $\Theta(m)$ extra space for the heap, plus $\Theta(n)$ for the output.
- **Without a heap.** A linear scan for the smallest load gives $\Theta(nm)$ time, which is fine for a few machines.

## Properties

| claim | statement | status |
|---|---|---|
| feasible | each job runs once, and each machine runs one job at a time | proved in the correctness proof |
| ratio | $\mathrm{ALG} \le (2 - 1/m)\,\mathrm{OPT}$ for every list | proved in the correctness proof |
| tight for the algorithm | $m(m - 1)$ jobs of length $1$, then one job of length $m$: $\mathrm{ALG} = 2m - 1$, $\mathrm{OPT} = m$ | proved on [Graham's bound](/list-scheduling-bound/) |
| online | job $j$ is placed using only $p_1, \ldots, p_j$ | by the pseudocode |
| online competitive ratio | $2 - 1/m$, optimal among deterministic online algorithms for $m = 2$ and $m = 3$ (Faigle, Kern and Turán 1989) | cited |
| with precedence | the same bound $2 - 1/m$ holds for $P \mid \mathrm{prec} \mid C_{\max}$ | cited from Graham 1966; see [Graham's bound](/list-scheduling-bound/) |
| anomalies | with precedence, more machines or shorter jobs can make the schedule longer | shown on [Graham's anomalies](/graham-anomalies/) |

## Variants and improvements

- **Sorted lists.** Sorting the list by decreasing time gives [LPT](/longest-processing-time-first/), with ratio $4/3 - 1/(3m)$. The same algorithm, with a linear scan in place of the heap, is called [Sorted-Balance](/sorted-balance/) by Kleinberg and Tardos.
- **Precedence constraints.** When a machine becomes idle, it takes the first job in the list whose predecessors are all done. This is Graham's original form, and it keeps the bound $2 - 1/m$ because the idle periods can be charged to a chain of jobs. See [precedence-constrained scheduling](/precedence-constrained-scheduling/) and the [critical path lower bound](/critical-path-lower-bound/).
- **Better online algorithms.** For large $m$, algorithms that keep some machines lightly loaded beat $2 - 1/m$: Bartal, Fiat, Karloff and Vohra (1995) reached $1.986$, Albers (1999) $1.923$, and Fleischer and Wahl (2000) $1.9201$. See [online makespan minimization](/online-makespan-minimization/) and the [competitive ratio of list scheduling](/list-scheduling-competitive-ratio/).
- **Uniform machines.** Putting each job on the machine where it would end first is the natural extension to $Q \mid\mid C_{\max}$. Its ratio grows with $m$, like $\log m$, so better methods are used there; see [uniform machine scheduling](/uniform-machine-scheduling/).

## When to use it

Use list scheduling when the jobs arrive over time and must be placed at once, or when the order of the jobs is fixed by the application. It needs no knowledge of the future, it runs in $O(\log m)$ time per job, and the guarantee $2 - 1/m$ holds for every order. When all jobs are known in advance, sort them first and use [LPT](/longest-processing-time-first/), which costs only the sort and has a much better worst case. For a guarantee close to $1$, use [MULTIFIT](/multifit-algorithm/) or the [PTAS](/hochbaum-shmoys-ptas/).

## Pitfalls

- **Returning the wrong makespan at line L6.** The machine that got the last job is not always the one that ends last. In the example, job 6 ends at $6$, but the makespan is $8$. Line L6 must take the largest load of all machines.
- **Choosing by the number of jobs at line L3.** Choosing the machine with the fewest jobs, or the next machine in turn, is a different rule, and its ratio can be close to $m$. With two machines and the list $(1, M, 1, M)$, the turn rule puts both jobs of length $M$ on machine 2 and ends at $2M$, while the optimum is $M + 1$. Line L3 must use the smallest load.
- **Ties at line L3.** The bound holds for every tie rule, but the schedule itself depends on it. Fix a rule, such as the smallest index, so that runs can be repeated and tested.
- **Idle machines with precedence.** In the precedence version, a machine must take a ready job whenever one exists. A rule that waits for a better job is not a list schedule, and the proof of $2 - 1/m$ does not apply to it.

## Implementations

## History

Graham (1966) defined list schedules for jobs with precedence constraints on identical processors and proved that any two list schedules differ by a factor of at most $2 - 1/m$. This is now read as the first worst-case analysis of an approximation algorithm. In the same paper and in his 1969 paper he showed the [anomalies](/graham-anomalies/) of list scheduling, and in 1969 he proved the bound $4/3 - 1/(3m)$ for the sorted list. Kleinberg and Tardos present the rule as Greedy-Balance, and the online scheduling literature uses it as the base line.

## References
