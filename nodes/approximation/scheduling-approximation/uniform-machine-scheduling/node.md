---
tag: R5VHF0
kind: problem
slug: uniform-machine-scheduling
name: Scheduling on uniformly related machines
aliases:
- Q||Cmax
- related machines scheduling
- uniform processors scheduling
area: approximation/scheduling-approximation
level: core
summary: Machines have speeds; job j takes p_j divided by s_i on machine i; minimize makespan.
prereqs: [makespan-minimization, machine-environments, scheduling-notation, makespan]
see_also: [longest-processing-time-first, lpt-bound, hochbaum-shmoys-ptas, unrelated-machine-scheduling, preemptive-makespan-scheduling, online-makespan-minimization, eptas, bin-packing]
sources:
  - paper: doi:10.1137/0206013
    title: "T. Gonzalez, O. H. Ibarra and S. Sahni, Bounds for LPT schedules on uniform processors, SIAM Journal on Computing 6(1), 1977"
    locator: the bound 2m/(m+1) for LPT on uniform machines and the lower bound examples
  - paper: doi:10.1137/0217033
    title: "D. S. Hochbaum and D. B. Shmoys, A polynomial approximation scheme for scheduling on uniform processors: using the dual approximation approach, SIAM Journal on Computing 17(3), 1988"
    locator: the polynomial-time approximation scheme for Q||Cmax
  - paper: "K. Jansen, An EPTAS for scheduling jobs on uniform processors: using an MILP relaxation with a constant number of integral variables, SIAM Journal on Discrete Mathematics 24(2), 2010"
    locator: the efficient polynomial-time approximation scheme for Q||Cmax
  - paper: "E. Horowitz and S. Sahni, Exact and approximate algorithms for scheduling nonidentical processors, Journal of the ACM 23(2), 1976"
    locator: the dynamic programs and the fully polynomial schemes for a fixed number of uniform and unrelated machines
  - paper: "G. Dobson, Scheduling independent tasks on uniform processors, SIAM Journal on Computing 13(4), 1984"
    locator: the upper bound 19/12 for LPT on uniform machines
  - paper: "A. Kovács, New approximation bounds for LPT scheduling, Algorithmica 57(2), 2010"
    locator: the improved upper and lower bounds for LPT on uniform machines and the tight bound for two machines
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 5, Parallel Machine Models (Deterministic)
---

Scheduling on uniformly related machines, written $Q \mid\mid C_{\max}$, is [makespan minimization](/makespan-minimization/) on machines of different speeds. Machine $i$ has speed $s_i > 0$, and job $j$ with work $p_j$ takes time $p_j / s_i$ on it. The goal is an assignment of the jobs to the machines with the smallest [makespan](/makespan/). The problem lies between identical machines, where all speeds are equal, and [unrelated machines](/unrelated-machine-scheduling/), where the times are arbitrary. It keeps the good news of identical machines: it is strongly NP-hard, but the LPT rule has a constant ratio and there is a [PTAS](/hochbaum-shmoys-ptas/), and even an EPTAS.

## In plain words

You have tasks of different sizes and a team of workers, some of them faster than others. A fast worker does every task in less time, and the gain is the same factor for every task. You want to share the tasks so that the whole team is done as soon as possible.

Giving all the work to the fastest worker is often a bad plan, and so is giving the same amount to each worker. A good rule takes the big tasks first and gives each one to the worker who would finish it soonest. This rule is never far from the best plan. With more care, a plan as close to the best as you like can be found, at a higher cost.

## Definition

**Input.** An integer $m \ge 1$ and speeds $s_1 \ge s_2 \ge \cdots \ge s_m > 0$, and $n$ jobs with work $p_1, \ldots, p_n \ge 0$. Both $n$ and $m$ are part of the input.

**Output.** An assignment $\sigma : \{1, \ldots, n\} \to \{1, \ldots, m\}$. Machine $i$ runs its jobs one after another from time 0 and ends at $L_i = \frac{1}{s_i} \sum_{j : \sigma(j) = i} p_j$.

**Goal.** Minimize $C_{\max} = \max_i L_i$. The least value is $\mathrm{OPT}$.

**Decision version.** For a bound $T$, can the jobs be split into $m$ groups so that group $i$ has total work at most $s_i T$? This is bin packing with $m$ bins of different capacities.

*Ratio convention.* This is a minimization problem. An algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. All ratios here are absolute and worst case.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of jobs and the number of machines |
| $p_j$ | the work of job $j$ |
| $s_i$ | the speed of machine $i$, sorted so that $s_1$ is the largest |
| $L_i$, $C_{\max}$ | the end time of machine $i$, and $\max_i L_i$ |
| $P$, $S$ | $\sum_j p_j$ and $\sum_i s_i$ |
| $\mathrm{OPT}$, $\mathrm{ALG}$ | the optimal makespan, and the makespan of an algorithm |

## Variants

- **Identical machines, $P \mid\mid C_{\max}$.** All $s_i = 1$. See [makespan minimization](/makespan-minimization/).
- **Fixed number of machines, $Qm \mid\mid C_{\max}$.** With $m$ constant the problem is NP-hard only in the ordinary sense. Horowitz and Sahni (1976) gave a pseudo-polynomial dynamic program and an [FPTAS](/fptas/).
- **Preemption, $Q \mid \mathrm{pmtn} \mid C_{\max}$.** Jobs may be split and moved between machines, but no job may run on two machines at once. The optimum is the largest of the lower bounds below, and it can be found in polynomial time (Horvath, Lam and Sethi 1977; Gonzalez and Sahni 1978). See [preemptive makespan scheduling](/preemptive-makespan-scheduling/).
- **Precedence constraints, $Q \mid \mathrm{prec} \mid C_{\max}$.** Here list scheduling is poor, because a long chain may be put on a slow machine. Chudak and Shmoys (1999) gave an $O(\log m)$-approximation, and Li (2017) improved it to $O(\log m / \log \log m)$.
- **Online.** The jobs arrive one by one. The greedy rule that puts each job where it ends first is only $\Theta(\log m)$-competitive, and Aspnes, Azar, Fiat, Plotkin and Waarts (1997) gave a constant competitive algorithm by doubling a guess of $\mathrm{OPT}$. See [online makespan minimization](/online-makespan-minimization/).
- **Unrelated machines, $R \mid\mid C_{\max}$.** The time $p_{ij}$ of job $j$ on machine $i$ is arbitrary. The uniform case is $p_{ij} = p_j / s_i$. See [unrelated machine scheduling](/unrelated-machine-scheduling/).

## Examples

**LPT is not always optimal.** Take speeds $s = (3, 2)$ and work $p = (4, 3, 3)$, so $P/S = 10/5 = 2$. LPT takes the jobs in the order $4, 3, 3$ and puts each on the machine where it would end first:

| job | end on machine 1 | end on machine 2 | choice |
|---|---|---|---|
| 4 | $4/3$ | $2$ | machine 1 |
| 3 | $4/3 + 1 = 7/3$ | $3/2$ | machine 2 |
| 3 | $7/3$ | $3/2 + 3/2 = 3$ | machine 1 |

So LPT ends at $7/3$. The optimum puts both jobs of work 3 on machine 1, which ends at $6/3 = 2$, and the job of work 4 on machine 2, which ends at $4/2 = 2$. The ratio is $(7/3)/2 = 7/6$.

**The fastest machine alone is not enough.** Take speeds $(2, 1)$ and work $(4, 2)$. Both jobs on the fast machine end at $6/2 = 3$. The job of work 4 on the fast machine and the job of work 2 on the slow one both end at time 2, which meets the bound $P/S = 6/3 = 2$ and so is optimal.

## Known algorithms

| algorithm | ratio $\rho$ | tight for the algorithm | time |
|---|---|---|---|
| greedy list scheduling, each job where it ends first, any order | $\Theta(\log m)$ | yes, up to constants | $O(nm)$ |
| [LPT](/longest-processing-time-first/), the same greedy rule in decreasing order of work | at most $2m/(m + 1)$ (Gonzalez, Ibarra and Sahni 1977); at most $19/12$ (Dobson 1984); at most about $1.5773$ (Kovács 2010) | no; the worst ratio is known to lie between about $1.54$ and $1.5773$ | $O(n \log n + nm)$ |
| LPT on two machines | $(1 + \sqrt{17})/4 \approx 1.2808$ (Kovács 2010) | yes | $O(n \log n)$ |
| PTAS (Hochbaum and Shmoys 1988) | $1 + \varepsilon$ | not applicable | polynomial for fixed $\varepsilon$ |
| EPTAS (Jansen 2010) | $1 + \varepsilon$ | not applicable | $f(1/\varepsilon) \cdot \mathrm{poly}(n)$ |
| dynamic program, fixed $m$ (Horowitz and Sahni 1976) | exact | not applicable | pseudo-polynomial |
| FPTAS, fixed $m$ (Horowitz and Sahni 1976) | $1 + \varepsilon$ | not applicable | polynomial in $n$ and $1/\varepsilon$ |

The PTAS is the [dual approximation](/dual-approximation/) method of the [Hochbaum-Shmoys scheme](/hochbaum-shmoys-ptas/), with one change: a machine of speed $s_i$ is a bin of capacity $s_i T$, so the bins differ, and a job that is small for a fast machine can be large for a slow one. The rounding and the packing must deal with this, which makes the scheme for uniform machines more complex than the one for identical machines.

## Bounds

- **Lower bounds on OPT.** For each $k \le \min(n, m)$, the $k$ largest jobs have total work at least the sum of the $k$ largest $p_j$, and in any schedule they run on at most $k$ machines, whose speeds add up to at most $s_1 + \cdots + s_k$. So
$$\mathrm{OPT} \ge \max\left( \frac{P}{S},\ \max_{1 \le k < m} \frac{p_{(1)} + \cdots + p_{(k)}}{s_1 + \cdots + s_k} \right),$$
where $p_{(1)} \ge p_{(2)} \ge \cdots$ are the jobs in decreasing order. The case $k = 1$ is $\mathrm{OPT} \ge p_{(1)} / s_1$. The right side is exactly the preemptive optimum.
- **Strong NP-hardness.** The case of equal speeds is $P \mid\mid C_{\max}$, which is strongly NP-hard by the reduction from [3-partition](/three-partition/). So there is no FPTAS unless P = NP; see [no FPTAS for strongly NP-hard problems](/no-fptas-for-strongly-np-hard-problems/).
- **Tight for the problem.** A PTAS exists, so the best polynomial guarantee is $1 + \varepsilon$ for every fixed $\varepsilon > 0$, and no constant above 1 is a hardness threshold. The problem is not APX-hard unless P = NP, in contrast with [unrelated machines](/unrelated-makespan-inapproximability/).

## Reductions

**From identical machines.** Setting $s_i = 1$ for all $i$ gives $P \mid\mid C_{\max}$. So every hardness result for identical machines holds here, and in particular strong NP-hardness.

**To unrelated machines.** Setting $p_{ij} = p_j / s_i$ gives an instance of $R \mid\mid C_{\max}$ with the same schedules and the same makespans. So the [2-approximation of Lenstra, Shmoys and Tardos](/lenstra-shmoys-tardos/) applies, though LPT and the PTAS are better here.

**To bin packing with different bin sizes.** "Is $\mathrm{OPT} \le T$?" asks whether the items $p_j$ fit into $m$ bins of capacities $s_1 T, \ldots, s_m T$. A dual approximation test for this packing gives an approximation scheme for the scheduling problem by binary search over $T$.

## Applications

- Load balancing on a cluster with processors of different generations, where a newer processor runs all tasks faster by about the same factor.
- Assigning print or render jobs to machines with different throughput.
- Production lines that run the same products at different rates.

## References
