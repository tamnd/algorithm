---
tag: HMRNWE
kind: problem
slug: unrelated-machine-scheduling
name: Scheduling on unrelated machines
aliases:
- R||Cmax
- unrelated parallel machine scheduling
- makespan on unrelated machines
area: approximation/scheduling-approximation
level: advanced
summary: Each job has a machine-dependent processing time; minimize makespan.
prereqs: [makespan-minimization, uniform-machine-scheduling, machine-environments, scheduling-notation]
see_also: [lenstra-shmoys-tardos, unrelated-makespan-inapproximability, restricted-assignment-scheduling, unrelated-machine-scheduling-makespan, generalized-assignment-problem, shmoys-tardos-gap, configuration-lp, online-restricted-assignment-load-balancing]
sources:
  - paper: doi:10.1007/BF01585745
    title: "J. K. Lenstra, D. B. Shmoys and É. Tardos, Approximation algorithms for scheduling unrelated parallel machines, Mathematical Programming 46, 1990"
    locator: the 2-approximation by rounding a vertex of the linear program, the 3/2 hardness, and the scheme for a fixed number of machines
  - paper: "E. Horowitz and S. Sahni, Exact and approximate algorithms for scheduling nonidentical processors, Journal of the ACM 23(2), 1976"
    locator: the dynamic programs and the fully polynomial schemes for a fixed number of machines
  - paper: "C. N. Potts, Analysis of a linear programming heuristic for scheduling unrelated parallel machines, Discrete Applied Mathematics 10(2), 1985"
    locator: the 2-approximation for a fixed number of machines by a linear program and enumeration
  - paper: "E. V. Shchepin and N. Vakhania, An optimal rounding gives a better approximation for scheduling unrelated machines, Operations Research Letters 33(2), 2005"
    locator: the improvement of the ratio to 2 - 1/m
  - paper: "O. Svensson, Santa Claus schedules jobs on unrelated machines, SIAM Journal on Computing 41(5), 2012"
    locator: the configuration linear program and the estimate 33/17 for restricted assignment
  - paper: "E. L. Lawler and J. Labetoulle, On preemptive scheduling of unrelated parallel processors by linear programming, Journal of the ACM 25(4), 1978"
    locator: the polynomial algorithm for the preemptive problem
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 11.1 (the generalized assignment problem and the rounding for unrelated machines)
---

Scheduling on unrelated machines, written $R \mid\mid C_{\max}$, is [makespan](/makespan/) minimization when the time of a job depends on the machine in an arbitrary way: job $j$ takes $p_{ij}$ on machine $i$, and $p_{ij} = \infty$ means that it may not run there. It is the most general of the three classic [machine environments](/machine-environments/), after identical and [uniform](/uniform-machine-scheduling/) machines. The problem is NP-hard to approximate within any ratio below $3/2$, and the best ratio known is about 2, from the [rounding of Lenstra, Shmoys and Tardos](/lenstra-shmoys-tardos/). The gap between $3/2$ and 2 is one of the main open questions of scheduling theory.

## In plain words

You have tasks and a team of workers, but each worker has their own skills. One worker may do a task in an hour that takes another worker a day, and some workers cannot do some tasks at all. You must give each task to one worker so that the last worker finishes as early as possible.

Giving each task to the worker who is best at it can be a poor plan, because one worker may end up with too many tasks. The best known methods first solve a relaxed version in which tasks may be split, and then repair the splits. They end at most about twice as late as the best plan, and nobody knows a fast method that is always much better.

## Definition

**Input.** An integer $m \ge 1$, $n$ jobs, and times $p_{ij} \in \{0, 1, 2, \ldots\} \cup \{\infty\}$ for each machine $i$ and job $j$. Each job has at least one finite time. Both $n$ and $m$ are part of the input.

**Output.** An assignment $\sigma : \{1, \ldots, n\} \to \{1, \ldots, m\}$ with $p_{\sigma(j) j} < \infty$ for each $j$. Machine $i$ has the load $L_i = \sum_{j : \sigma(j) = i} p_{ij}$.

**Goal.** Minimize $C_{\max} = \max_i L_i$. The least value is $\mathrm{OPT}$.

**Decision version.** For a bound $T$, is there an assignment with $C_{\max} \le T$?

*Ratio convention.* This is a minimization problem. An algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. All ratios here are absolute and worst case, and the number of machines is part of the input unless the text says otherwise.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of jobs and the number of machines |
| $p_{ij}$ | the time of job $j$ on machine $i$, possibly $\infty$ |
| $L_i$, $C_{\max}$ | the load of machine $i$, and $\max_i L_i$ |
| $\mathrm{OPT}$, $\mathrm{ALG}$ | the optimal makespan, and the makespan of an algorithm |

## Variants

- **Uniform machines, $Q \mid\mid C_{\max}$.** $p_{ij} = p_j / s_i$. This case has a PTAS; see [uniform machine scheduling](/uniform-machine-scheduling/).
- **Restricted assignment, $P \mid M_j \mid C_{\max}$.** Each job has one time $p_j$ and a set $M_j$ of allowed machines, so $p_{ij} \in \{p_j, \infty\}$. It is still hard to approximate below $3/2$, but better estimates are known; see [restricted assignment scheduling](/restricted-assignment-scheduling/).
- **Fixed number of machines, $Rm \mid\mid C_{\max}$.** For constant $m$ the problem is NP-hard only in the ordinary sense. Horowitz and Sahni (1976) gave a pseudo-polynomial dynamic program and an [FPTAS](/fptas/).
- **Preemption, $R \mid \mathrm{pmtn} \mid C_{\max}$.** Jobs may be split among machines, but not run on two machines at once. Lawler and Labetoulle (1978) solved it exactly with a linear program and an [open shop](/open-shop-scheduling/) step.
- **Costs, the generalized assignment problem.** Each pair also has a cost $c_{ij}$, and one wants a cheap assignment with small makespan. Shmoys and Tardos (1993) find a schedule of cost at most $C$ and makespan at most $2T$ whenever one of cost $C$ and makespan $T$ exists. See [the generalized assignment problem](/generalized-assignment-problem/) and [the Shmoys-Tardos rounding](/shmoys-tardos-gap/).
- **Online.** Jobs arrive one by one. Greedy is $m$-competitive, and Aspnes, Azar, Fiat, Plotkin and Waarts (1997) gave an $O(\log m)$-competitive algorithm, which is best possible up to constants already for restricted assignment; see [online restricted assignment](/online-restricted-assignment-load-balancing/).
- **Max-min fairness.** Maximize the smallest load instead of minimizing the largest. This is the Santa Claus problem; the identical case is [machine covering](/machine-covering/).

## Examples

**A small instance.** Take $m = 2$ and three jobs with these times:

| | job 1 | job 2 | job 3 |
|---|---|---|---|
| machine 1 | 2 | 3 | 4 |
| machine 2 | 4 | 1 | 3 |

Of the eight assignments, the best puts job 1 on machine 1 and jobs 2 and 3 on machine 2, with loads 2 and 4, so $\mathrm{OPT} = 4$. The simple lower bounds give only 3: the largest of the best times, $\max_j \min_i p_{ij} = \max(2, 1, 3)$, and the average of the best times, $(2 + 1 + 3)/2$.

**The best machine for each job is a bad rule.** Take $m$ machines and $m$ jobs. Each job takes time 1 on machine 1 and time $1 + \delta$ on every other machine, for a small $\delta > 0$. If each job goes to the machine where it is fastest, all jobs go to machine 1 and the makespan is $m$. One job on each machine gives $1 + \delta$. So this rule has ratio close to $m$.

## Known algorithms

| algorithm | ratio $\rho$ | tight for the algorithm | time |
|---|---|---|---|
| each job on its fastest machine | $m$ | yes | $O(nm)$ |
| greedy, each job where it ends first | $m$ | yes | $O(nm)$, online |
| Potts 1985, fixed $m$ | 2 | 2 is the proved bound | polynomial for fixed $m$, exponential in $m$ |
| [Lenstra, Shmoys and Tardos 1990](/lenstra-shmoys-tardos/) | 2 | no; $2 - 1/m$ is known | polynomial, one linear program for each step of a search |
| Shchepin and Vakhania 2005 | $2 - 1/m$ | yes for the linear program of Lenstra, Shmoys and Tardos | polynomial |
| Horowitz and Sahni 1976, fixed $m$ | $1 + \varepsilon$ (FPTAS) | not applicable | polynomial in $n$ and $1/\varepsilon$ for fixed $m$ |
| Lenstra, Shmoys and Tardos 1990, fixed $m$ | $1 + \varepsilon$ (PTAS) | not applicable | polynomial for fixed $m$ and $\varepsilon$ |

The 2-approximation solves the linear program with $x_{ij} \ge 0$, $\sum_i x_{ij} = 1$ for each job and $\sum_j p_{ij} x_{ij} \le T$ for each machine, where $x_{ij} = 0$ is forced whenever $p_{ij} > T$. This pruning is the key step: without it, one job of time $m$ on every machine has the fractional value 1, and the gap is $m$. With the pruning, the gap of this program is $2 - 1/m$, so no rounding of it can do better. The [configuration LP](/configuration-lp/), which has a variable for each set of jobs that fits on a machine, is stronger for restricted assignment, but Verschae and Wiese (2014) showed that its gap is still 2 for general unrelated machines.

The page [unrelated machine scheduling makespan](/unrelated-machine-scheduling-makespan/) treats the same problem from the point of view of linear programming rounding.

## Bounds

- **Lower bounds on OPT.** $\mathrm{OPT} \ge \max_j \min_i p_{ij}$, since each job runs somewhere, and $\mathrm{OPT} \ge \frac1m \sum_j \min_i p_{ij}$, since the loads add up to at least this. Both can be far from $\mathrm{OPT}$; the linear program above gives a much better bound.
- **Strong NP-hardness.** The case $p_{ij} = p_j$ is $P \mid\mid C_{\max}$, which is strongly NP-hard.
- **No ratio below 3/2.** It is NP-hard to decide whether $\mathrm{OPT} \le 2$, even with times in $\{1, 2, \infty\}$, so no polynomial algorithm has ratio below $3/2$ unless P = NP; see [the 3/2 hardness theorem](/unrelated-makespan-inapproximability/). So the problem has no PTAS, and it is APX-hard.
- **The open gap.** The best ratio is $2 - 1/m$ and the best hardness is $3/2$. Closing this gap is one of the ten open problems in the survey of Schuurman and Woeginger (1999). See also [scheduling makespan inapproximability](/scheduling-makespan-inapproximability/).
- **Estimation for restricted assignment.** In the restricted assignment case, Svensson (2012) showed that the configuration LP estimates $\mathrm{OPT}$ within a factor $33/17 \approx 1.94$. His proof does not give a polynomial algorithm that finds a schedule of this quality. No such estimate below 2 is known for general unrelated machines.

## Reductions

**From three-dimensional matching.** [Three-dimensional matching](/three-dimensional-matching/) reduces to the question "is $\mathrm{OPT} \le 2$?" with a machine for each triple, a job of time 1 for each element of two of the sets, and dummy jobs of time 2. This gives the $3/2$ hardness.

**From identical and uniform machines.** Setting $p_{ij} = p_j$ or $p_{ij} = p_j / s_i$ embeds $P \mid\mid C_{\max}$ and $Q \mid\mid C_{\max}$, so their hardness holds here.

**To the generalized assignment problem.** $R \mid\mid C_{\max}$ is the generalized assignment problem with all costs zero. The [Shmoys-Tardos rounding](/shmoys-tardos-gap/) extends the 2-approximation to that problem.

**To bipartite matching for unit loads.** With times in $\{1, \infty\}$, "is $\mathrm{OPT} \le 1$?" asks for a [bipartite matching](/bipartite-matching/) that covers every job, which is polynomial. More generally, $\mathrm{OPT} \le T$ with times in $\{1, \infty\}$ is a flow problem.

## Applications

- Assigning tasks to a cluster of different processors, such as CPUs, GPUs and special chips, where each kind of task runs well on some kinds of hardware and badly on others.
- Assigning work to people with different skills, where some people cannot do some tasks.
- Scheduling jobs in a factory whose machines differ in their tools.

## References
