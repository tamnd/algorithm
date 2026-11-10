---
tag: 5CS51K
kind: definition
slug: scheduling-notation
name: Three-field notation for scheduling problems
aliases:
- alpha|beta|gamma notation
- Graham notation
- Graham, Lawler, Lenstra and Rinnooy Kan notation
area: approximation/scheduling-approximation
level: core
summary: Graham's classification of machine environment, job constraints and objective.
prereqs: [scheduling-problem, machine-environments, makespan]
see_also: [machine-environments, makespan, makespan-minimization, preemptive-makespan-scheduling, single-machine-scheduling, graham-three-field-notation, lateness-and-tardiness, precedence-constrained-scheduling]
sources:
  - paper: doi:10.1016/S0167-5060(08)70356-X
    title: "R. L. Graham, E. L. Lawler, J. K. Lenstra and A. H. G. Rinnooy Kan, Optimization and approximation in deterministic sequencing and scheduling: a survey, Annals of Discrete Mathematics 5, 1979"
    locator: Section 2, the classification of problems (job data, machine environment, job characteristics, optimality criteria), pp. 287-326 for the whole paper
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 2, Section 2.1 (framework and notation) and Section 2.2 (examples)
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 1 (classification of scheduling problems, the three fields and the reduction graphs)
  - paper: "E. L. Lawler, J. K. Lenstra, A. H. G. Rinnooy Kan and D. B. Shmoys, Sequencing and scheduling: algorithms and complexity, in Handbooks in Operations Research and Management Science, Volume 4, North-Holland, 1993"
    title: Lawler, Lenstra, Rinnooy Kan and Shmoys 1993
    locator: Section 2, the problem classes and the notation used in the whole chapter
---

The three-field notation writes a deterministic [scheduling problem](/scheduling-problem/) as $\alpha \mid \beta \mid \gamma$, where $\alpha$ is the machine environment, $\beta$ is the list of job constraints, and $\gamma$ is the objective to minimize. Graham, Lawler, Lenstra and Rinnooy Kan introduced it in their 1979 survey, and every scheduling text since then uses it. For example, $P \mid\mid C_{\max}$ is [makespan minimization](/makespan-minimization/) on identical machines, and $1 \mid r_j \mid L_{\max}$ is the single machine with release dates and maximum lateness as the objective.

## Definition

**Data.** There are $n$ jobs $J_1, \ldots, J_n$ and $m$ machines $M_1, \ldots, M_m$. Job $j$ has a processing time $p_j$ (or $p_{ij}$ on machine $i$), and it can also have a release date $r_j$, a due date $d_j$ and a weight $w_j$. A schedule gives each job a completion time $C_j$. From $C_j$ we derive the lateness $L_j = C_j - d_j$, the tardiness $T_j = \max(0, C_j - d_j)$, and the unit penalty $U_j = 1$ if $C_j > d_j$, else $U_j = 0$.

A problem class is a string $\alpha \mid \beta \mid \gamma$.

**The field $\alpha$: machine environment.** $\alpha = \alpha_1 \alpha_2$.

| $\alpha_1$ | environment | meaning |
|---|---|---|
| $1$ | single machine | one machine, each job has one operation |
| $P$ | identical parallel machines | job $j$ takes $p_j$ on each machine |
| $Q$ | uniform (related) machines | machine $i$ has speed $s_i$, and job $j$ takes $p_j / s_i$ on it |
| $R$ | unrelated machines | job $j$ takes $p_{ij}$ on machine $i$, with no relation between the values |
| $F$ | flow shop | each job has one operation on each machine, in the order $M_1, M_2, \ldots, M_m$ |
| $J$ | job shop | each job has its own sequence of operations, each on a given machine |
| $O$ | open shop | each job has one operation on each machine, in any order |

The second part $\alpha_2$ is empty or a positive integer. If $\alpha_2 = m$, the number of machines is the constant $m$ and is not part of the input: $P3 \mid\mid C_{\max}$ has exactly three machines. If $\alpha_2$ is empty, the number of machines is part of the input. The page [machine environments](/machine-environments/) explains each environment in depth.

**The field $\beta$: job characteristics.** $\beta$ is a list of zero or more entries, separated by commas. An empty $\beta$ means: no preemption, no precedence, all release dates $0$, and arbitrary non-negative processing times. The common entries are these.

| entry | meaning |
|---|---|
| $\mathrm{pmtn}$ | preemption: a job can be stopped and resumed later, on any machine, at no cost |
| $\mathrm{prec}$ | precedence constraints: a directed acyclic graph, and $j \to k$ means that $k$ starts after $j$ ends |
| $\mathrm{tree}$, $\mathrm{chains}$, $\mathrm{intree}$, $\mathrm{outtree}$ | special forms of the precedence graph |
| $r_j$ | release dates: job $j$ cannot start before $r_j$ |
| $\bar d_j$ | deadlines: job $j$ must end by $\bar d_j$ (a hard constraint, not a due date) |
| $p_j = 1$, $p_j = p$, $p_{ij} = 1$ | all processing times are equal |
| $M_j$ | eligibility (restricted assignment): job $j$ may run only on the machines of the set $M_j$ |
| $s_{jk}$ | sequence-dependent setup times |
| $\mathrm{nwt}$ | no wait: in a shop, the operations of a job follow each other without a gap |
| $\mathrm{prmu}$ | permutation flow shop: each machine processes the jobs in the same order |

**The field $\gamma$: objective.** $\gamma$ is a function of the completion times, to be minimized. The usual ones are the [makespan](/makespan/) $C_{\max} = \max_j C_j$, the maximum lateness $L_{\max} = \max_j L_j$, the total (weighted) completion time $\sum C_j$ or $\sum w_j C_j$, the (weighted) number of late jobs $\sum U_j$ or $\sum w_j U_j$, and the total (weighted) tardiness $\sum T_j$ or $\sum w_j T_j$. Each of these objectives is *regular*: it does not decrease when one $C_j$ increases.

**Reading rule.** A class $\alpha \mid \beta \mid \gamma$ is the set of all instances with that environment and those constraints, and the task is to find a feasible schedule of minimum $\gamma$. An algorithm for a class must work for each instance in it, so a class with fewer entries in $\beta$ is a harder (more general) problem.

## Examples and non-examples

**Examples.** Each line gives a class, what it says, and its status.

- $1 \mid\mid \sum w_j C_j$: one machine, minimize the weighted sum of completion times. Smith's ratio rule (sort by $p_j / w_j$) is optimal; see [Smith's rule](/smiths-rule/) and [weighted completion time scheduling](/weighted-completion-time-scheduling/).
- $1 \mid\mid L_{\max}$: one machine, minimize the maximum lateness. [Earliest due date first](/earliest-due-date-first/) is optimal (Jackson 1955).
- $1 \mid \mathrm{prec} \mid f_{\max}$ for a non-decreasing cost $f_j$ of each job: [Lawler's algorithm](/lawler-algorithm/) schedules from the end, in $O(n^2)$ time.
- $1 \mid r_j \mid L_{\max}$: adding release dates makes the single-machine problem strongly NP-hard, while $1 \mid r_j, \mathrm{pmtn} \mid L_{\max}$ is solved by preemptive EDD.
- $1 \mid\mid \sum U_j$: the [Moore-Hodgson algorithm](/moore-hodgson-algorithm/) minimizes the number of late jobs; $1 \mid\mid \sum w_j U_j$ is NP-hard, because it contains knapsack.
- $P \mid\mid C_{\max}$: [makespan minimization](/makespan-minimization/) on identical machines, strongly NP-hard. $P2 \mid\mid C_{\max}$ is NP-hard in the ordinary sense, since it is the partition problem.
- $P \mid \mathrm{pmtn} \mid C_{\max}$: [preemptive makespan](/preemptive-makespan-scheduling/), solved in $O(n)$ time by [McNaughton's wrap-around rule](/mcnaughton-wrap-around/).
- $P \mid \mathrm{prec}, p_j = 1 \mid C_{\max}$: unit jobs with precedence. $P \mid \mathrm{tree}, p_j = 1 \mid C_{\max}$ is solved by [Hu's algorithm](/hu-algorithm/), and $P2 \mid \mathrm{prec}, p_j = 1 \mid C_{\max}$ by the [Coffman-Graham algorithm](/coffman-graham-algorithm/).
- $Q \mid\mid C_{\max}$ and $R \mid\mid C_{\max}$: [uniform](/uniform-machine-scheduling/) and [unrelated](/unrelated-machine-scheduling/) machines. The second has the 2-approximation of [Lenstra, Shmoys and Tardos](/lenstra-shmoys-tardos/).
- $P \mid M_j \mid C_{\max}$: [restricted assignment](/restricted-assignment-scheduling/), the special case of $R \mid\mid C_{\max}$ with $p_{ij} \in \{p_j, \infty\}$.
- $F2 \mid\mid C_{\max}$: the two-machine flow shop, solved by [Johnson's rule](/johnsons-rule/) in $O(n \log n)$ time. $F3 \mid\mid C_{\max}$ is strongly NP-hard.
- $O2 \mid\mid C_{\max}$ and $J2 \mid\mid C_{\max}$: the two-machine [open shop](/open-shop-scheduling/) is solvable in linear time; the two-machine [job shop](/job-shop-scheduling/) in general is NP-hard.

**A worked reading.** The string $P3 \mid r_j, \mathrm{pmtn} \mid \sum w_j C_j$ means: three identical machines, jobs with release dates, preemption allowed, and the objective $\sum_j w_j C_j$. The string $Q \mid p_j = 1 \mid \sum C_j$ means: uniform machines with speeds that are part of the input, unit jobs, and the sum of completion times.

**Non-examples.**

- $P \mid C_{\max}$ is not a valid class. There must be exactly three fields; with no constraints the middle field is empty and the string is $P \mid\mid C_{\max}$.
- $P \mid\mid C_{\max}$ and $Pm \mid\mid C_{\max}$ are different classes. In the first, $m$ is part of the input and the problem is strongly NP-hard. In the second, $m$ is a constant, and dynamic programming gives a pseudo-polynomial algorithm and an FPTAS.
- $1 \mid d_j \mid C_{\max}$ is not a standard class. A due date $d_j$ only enters through the objective (lateness, tardiness, late jobs). A hard limit is a deadline and is written $\bar d_j$.
- The notation does not describe online or stochastic arrival. Authors add a word such as "online" in $\beta$ or in the text, but it is outside the 1979 scheme.
- $\beta = \mathrm{pmtn}$ does not mean that a job can run on two machines at the same time. A preempted job can move to another machine, but at each moment it runs on at most one machine.

**Reductions between classes.** Each environment is a special case of the next in $1 \subset P \subset Q \subset R$: set $m = 1$, then set all speeds to $1$, then set $p_{ij} = p_j / s_i$. In the same way, $C_{\max}$ reduces to $L_{\max}$ (set all $d_j = 0$), $\sum C_j$ reduces to $\sum w_j C_j$, and $\sum U_j$ reduces to $\sum w_j U_j$. Brucker draws these relations as reduction graphs. A hardness result moves up the graph, and an algorithm moves down it.

## Related definitions

- [Machine environments](/machine-environments/): the meaning of each value of $\alpha$ in depth.
- [Makespan](/makespan/): the objective $C_{\max}$.
- [Lateness and tardiness](/lateness-and-tardiness/): the objectives $L_{\max}$, $\sum T_j$ and $\sum U_j$.
- [Preemption](/preemption/): the $\mathrm{pmtn}$ entry.
- [Precedence-constrained scheduling](/precedence-constrained-scheduling/): the $\mathrm{prec}$ entry.
- [Scheduling with release dates](/scheduling-with-release-dates/): the $r_j$ entry.
- [Graham three-field notation](/graham-three-field-notation/): the same notation as used in online scheduling.

## References
