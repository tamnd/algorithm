---
tag: 7VB7QV
kind: algorithm
slug: hu-algorithm
name: Hu's algorithm
aliases:
- Hu's level algorithm
- critical path rule for in-trees
- highest level first for in-trees
area: approximation/scheduling-approximation
level: advanced
summary: Optimal schedule for unit-time jobs with in-tree precedence on identical machines.
solves: [precedence-constrained-scheduling]
model: word-ram
complexity:
  vars: {n: the number of jobs, m: the number of machines}
  time: {worst: O(n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1961
  people: [T. C. Hu]
  note: Hu gave the level rule and the matching lower bound for assembly line problems with tree precedence in 1961.
prereqs: [precedence-constrained-scheduling, critical-path-lower-bound, list-scheduling, rooted-tree]
see_also: [coffman-graham-algorithm, critical-path-lower-bound, list-scheduling-bound, graham-anomalies, dag-longest-path, topological-sort]
sources:
  - paper: doi:10.1287/opre.9.6.841
    title: "T. C. Hu, Parallel sequencing and assembly line problems, Operations Research 9(6), 1961"
    locator: the level rule and the proof that it is optimal for tree precedence and unit times
  - paper: doi:10.1016/S0022-0000(75)80008-0
    title: "J. D. Ullman, NP-complete scheduling problems, Journal of Computer and System Sciences 10(3), 1975"
    locator: the NP-completeness of unit-time scheduling with general precedence constraints
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 5 (parallel machines), the section on unit jobs with tree precedence
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 5, Section 5.1 (the critical path rule for in-trees and unit jobs)
  - book: isbn:9781584883975
    title: Joseph Y.-T. Leung (editor), Handbook of Scheduling, Algorithms, Models, and Performance Analysis
    locator: Chapter 3, Some basic scheduling algorithms (Hu's algorithm)
---

Hu's algorithm finds a schedule of least [makespan](/makespan/) for unit-time jobs whose precedence constraints form an in-tree (or an in-forest), on $m$ identical machines. This is the problem $P \mid \text{intree}, p_j = 1 \mid C_{\max}$ in [three-field notation](/scheduling-notation/), a polynomial special case of [precedence-constrained scheduling](/precedence-constrained-scheduling/). It gives each job a *level*, the number of jobs on its path to the root, and at each time step it starts the available jobs of highest level. Hu (1961) proved that the result meets a counting form of the [critical path lower bound](/critical-path-lower-bound/), so it is optimal.

## In plain words

Think of an assembly. Each part goes into exactly one bigger part, and the finished product is at the top. Each step of work takes one hour, and a few workers can each do one step in an hour. A step can start only when all the parts that go into it are ready.

The level of a step is the number of steps that must still happen after it, the step itself included. A step with a high level sits at the bottom of a long chain, so a delay there delays the finish. Hu's rule is: in each hour, give the workers the ready steps with the highest levels. For tree-shaped assemblies, this greedy rule is always optimal. For other shapes it can fail.

## The problem

There are $n$ jobs and $m \ge 1$ identical machines. Each job takes one time unit. Each job $j$ has at most one successor $s(j)$, so the precedence graph is an in-forest; a job with no successor is a root. A schedule assigns each job a slot $\sigma(j) \in \{1, 2, \ldots\}$ (the job runs in $[\sigma(j) - 1, \sigma(j))$) such that at most $m$ jobs share a slot and $\sigma(j) < \sigma(s(j))$ for each job with a successor. The goal is to minimize $C_{\max} = \max_j \sigma(j)$. We write $\mathrm{OPT}$ for the least makespan and $\mathrm{ALG}$ for the makespan of Hu's schedule.

The *level* is $\ell(j) = 1$ for a root and $\ell(j) = 1 + \ell(s(j))$ otherwise. For $h \ge 1$ let $N(h)$ be the number of jobs with $\ell(j) \ge h$.

## The algorithm

```pseudo id=main
HU(jobs, s, m)                             ▷ s(j) is the successor of j, or NIL
L1  compute ℓ(j) for each job, from the roots down
L2  w(j) ← the number of jobs i with s(i) = j
L3  A ← the jobs with w(j) = 0               ▷ the available jobs
L4  t ← 0
L5  while A is not empty do
L6      t ← t + 1
L7      B ← the min(m, |A|) jobs of A with the highest levels; remove them from A
L8      σ(j) ← t for each j in B
L9      for each j in B with s(j) ≠ NIL: w(s(j)) ← w(s(j)) − 1, and add s(j) to A if it is 0
L10 return σ
```

Line L1 computes the levels: a root has level 1, and each other job has one more than its successor. Lines L2 and L3 count the predecessors that each job waits for, and collect the jobs that wait for none. Each pass of the loop is one time slot. Line L7 is the level rule. A job enters $A$ in line L9 in the slot after its last predecessor runs, so line L8 never starts a job before its predecessors finish. Ties between jobs of equal level can be broken in any way.

## Example

Take $m = 3$ and the in-tree on 12 jobs below; the arrow points to the successor.

| job | successor | level |
|---|---|---|
| r | none | 1 |
| p, q | r | 2 |
| a, b, c | p | 3 |
| d | q | 3 |
| e, f | a | 4 |
| g | d | 4 |
| h | e | 5 |
| i | g | 5 |

| slot | available at the start | started (highest levels) |
|---|---|---|
| 1 | b 3, c 3, f 4, h 5, i 5 | h, i, f |
| 2 | b 3, c 3, e 4, g 4 | e, g, b |
| 3 | a 3, c 3, d 3 | a, c, d |
| 4 | p 2, q 2 | p, q |
| 5 | r 1 | r |

The makespan is 5. The lower bound of the correctness proof gives the same value: 9 jobs have level at least 3, so each schedule needs $3 - 1 + \lceil 9/3 \rceil = 5$ slots. On $m = 2$ machines the algorithm takes 7 slots, and the bound for $h = 1$ is $0 + \lceil 12/2 \rceil = 6$, for $h = 3$ it is $2 + \lceil 9/2 \rceil = 7$.

## Correctness

The output is feasible, by the remark after the pseudocode. Optimality has two parts.

- **Lower bound.** A job of level $\ell$ has $\ell - 1$ jobs after it on its path to the root, each in a later slot. So in a schedule of makespan $C$, every job of level at least $h$ runs in one of the slots $1, \ldots, C - h + 1$, and $N(h) \le m (C - h + 1)$. Hence $\mathrm{OPT} \ge \max_h \big(h - 1 + \lceil N(h)/m \rceil\big)$.
- **Upper bound.** Hu's schedule meets this bound. The key fact is that in an in-forest, each finished job frees at most one new job, so the number of available jobs never grows. Once a slot has an idle machine, every later slot runs all available jobs, and the highest remaining level drops by exactly one per slot. A short induction on the level threshold then finds an $h$ with $\mathrm{ALG} = h - 1 + \lceil N(h)/m \rceil$.

So $\mathrm{OPT} = \max_h \big(h - 1 + \lceil N(h)/m \rceil\big)$, and Hu's algorithm reaches it. The full proof is in the proofs section.

## Complexity

- Line L1 visits each job once if it follows successor pointers and stops at the first job whose level is known: $O(n)$ time.
- Lines L2 and L3 take $O(n)$ time.
- Each job enters and leaves $A$ once. With a binary heap keyed by level, each operation costs $O(\log n)$, so the loop takes $O(n \log n)$ time in the worst case.
- The extra space is $O(n)$ for the levels, the counters and the heap.

The levels are integers from 1 to $n$, so one bucket for each level also works. A job that enters $A$ in line L9 has a lower level than the job that freed it, so the highest level in $A$ never increases from one slot to the next. A pointer to the highest nonempty bucket then moves down at most $n$ times, and the loop takes $O(n)$ time.

## Properties

- **Exact.** The schedule is optimal for every in-forest, every $m$ and every tie-breaking rule among jobs of equal level.
- **A list schedule.** It is [list scheduling](/list-scheduling/) with the priority list sorted by level, so it never leaves a machine idle while a job is available.
- **A closed formula.** The proof gives $\mathrm{OPT} = \max_h \big(h - 1 + \lceil N(h)/m \rceil\big)$, so the optimal makespan can be computed in $O(n)$ time without the schedule.

## Variants and improvements

- **Out-trees.** If each job has at most one predecessor, reverse all arcs to get an in-forest, run Hu's algorithm, and reverse time: job $j$ goes to slot $C + 1 - \sigma(j)$. A schedule and its reverse have the same makespan and respect reversed constraints, so the result is optimal for $P \mid \text{outtree}, p_j = 1 \mid C_{\max}$.
- **General precedence, two machines.** The level rule fails for general DAGs (see the pitfalls). The [Coffman-Graham algorithm](/coffman-graham-algorithm/) breaks ties by a lexicographic labeling and is optimal for $P2 \mid \text{prec}, p_j = 1 \mid C_{\max}$.
- **General precedence, many machines.** $P \mid \text{prec}, p_j = 1 \mid C_{\max}$ is NP-hard (Ullman 1975), and with the level rule or any list rule the makespan is at most $(2 - 1/m)\,\mathrm{OPT}$ by [Graham's bound](/list-scheduling-bound/). See [precedence-constrained scheduling](/precedence-constrained-scheduling/).
- **Arbitrary processing times.** With tree precedence and arbitrary $p_j$, the problem is strongly NP-hard, because it contains $P \| C_{\max}$ (no arcs at all).

## When to use it

Use Hu's algorithm when the constraints are a forest and the jobs have equal length, for example in assembly lines and in the evaluation of expression trees on parallel units. For general DAGs on two machines use the Coffman-Graham algorithm. For general DAGs on more machines, the level rule is still a good list order in practice, but it is only a $(2 - 1/m)$-approximation in the worst case.

## Pitfalls

- **Using it on a DAG that is not a forest.** Take $m = 2$, jobs $0, \ldots, 5$ and arcs $0 \to 5$, $1 \to 3$, $2 \to 3$, $2 \to 4$, $2 \to 5$. Jobs 0, 1 and 2 all have level 2. If line L7 breaks the tie in favour of 0 and 1, the schedule is $\{0, 1\}, \{2\}, \{3, 4\}, \{5\}$ with makespan 4, but $\{1, 2\}, \{0, 4\}, \{3, 5\}$ has makespan 3. The proof fails because job 2 frees three jobs at once.
- **Counting levels from the wrong end.** The level is the length of the path *to the root* (to the end of the work), not the depth from the leaves. Line L1 must start at the roots.
- **Starting a job too early.** A job enters $A$ only when its counter $w$ reaches 0 in line L9, and then it can run at the earliest in the next slot. Adding it to the batch of the current slot breaks the constraint $\sigma(j) < \sigma(s(j))$.
- **Unequal processing times.** The optimality proof needs unit jobs. With $p_j$ of different sizes, the level rule is only a list schedule with the bound $2 - 1/m$.

## Implementations

## History

T. C. Hu published the level rule and its proof of optimality in 1961, in a study of assembly lines in Operations Research. His paper also asks for the least number of workers that can finish a tree of unit tasks by a given time, and answers it with the same level counts. The rule is often called the critical path rule, because the level of a job is the number of jobs on the longest chain that starts at it. The same rule is not optimal for general DAGs, and Ullman (1975) proved that the problem with general DAGs and unit jobs is NP-hard when $m$ is part of the input.

## References
