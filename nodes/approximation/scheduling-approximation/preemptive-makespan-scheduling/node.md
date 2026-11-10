---
tag: XFVFMK
kind: problem
slug: preemptive-makespan-scheduling
name: Preemptive makespan scheduling
aliases:
- P|pmtn|Cmax
- Q|pmtn|Cmax
- R|pmtn|Cmax
area: approximation/scheduling-approximation
level: core
summary: Jobs may be interrupted and resumed; minimize makespan on identical machines.
prereqs: [makespan, preemption, machine-environments]
see_also: [mcnaughton-wrap-around, makespan-minimization, makespan-lower-bounds, uniform-machine-scheduling, unrelated-machine-scheduling, birkhoff-von-neumann-decomposition, linear-programming-problem, lenstra-shmoys-tardos]
sources:
  - paper: doi:10.1287/mnsc.6.1.1
    title: "R. McNaughton, Scheduling with deadlines and loss functions, Management Science 6(1), 1959"
    locator: the wrap-around construction for identical machines with preemption and its optimal value (pp. 1-12 for the paper)
  - paper: "T. Gonzalez and S. Sahni, Preemptive scheduling of uniform processor systems, Journal of the ACM 25(1), 1978, pp. 92-101"
    title: Gonzalez and Sahni 1978
    locator: the optimal value for uniform machines and the algorithm with at most 2(m - 1) preemptions
  - paper: "E. L. Lawler and J. Labetoulle, On preemptive scheduling of unrelated parallel processors by linear programming, Journal of the ACM 25(4), 1978, pp. 612-619"
    title: Lawler and Labetoulle 1978
    locator: the linear program for R|pmtn|Cmax and the construction of the schedule from its solution
  - paper: doi:10.1016/S0167-5060(08)70356-X
    title: "R. L. Graham, E. L. Lawler, J. K. Lenstra and A. H. G. Rinnooy Kan, Optimization and approximation in deterministic sequencing and scheduling: a survey, Annals of Discrete Mathematics 5, 1979"
    locator: the sections on parallel machines with preemption (P, Q and R with pmtn)
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 5 (parallel machines, the problems P|pmtn|Cmax, Q|pmtn|Cmax and R|pmtn|Cmax)
---

Preemptive makespan scheduling, written $P \mid \mathrm{pmtn} \mid C_{\max}$, asks for a schedule of $n$ jobs on $m$ identical machines with the smallest [makespan](/makespan/), where a job may be stopped and resumed later, on the same or on another machine, at no cost. Unlike the nonpreemptive problem [makespan minimization](/makespan-minimization/), which is strongly NP-hard, it is solved exactly in $O(n)$ time by [McNaughton's wrap-around rule](/mcnaughton-wrap-around/), with optimal value $\max(\frac1m \sum_j p_j, \max_j p_j)$. The versions for uniform machines, $Q \mid \mathrm{pmtn} \mid C_{\max}$, and for unrelated machines, $R \mid \mathrm{pmtn} \mid C_{\max}$, are also polynomial: the first has a closed formula, and the second is a linear program.

## In plain words

You have a set of tasks and a team of equal workers. A worker may stop a task at any moment and another worker may go on with it later, but two workers cannot work on the same task at the same time. You want the whole team to be done as soon as possible.

Two simple facts limit how fast you can be. The total work must be shared, so the team needs at least the total divided by the number of workers. And the longest task must be done by one worker at a time, so the team needs at least its length. Because tasks can be cut, there is always a plan that meets the larger of these two limits, so this problem is easy.

## Definition

**Input.** An integer $m \ge 1$, the number of machines, and $n$ jobs with processing times $p_1, \ldots, p_n \ge 0$. Here $n$ is the number of jobs and $m$ is the number of machines.

**Output.** A preemptive schedule: for each job, a finite set of pieces, each a time interval on one machine, with total length $p_j$. A machine runs at most one piece at a time, and the pieces of one job do not overlap in time.

**Goal.** Minimize the makespan, the end of the last piece. $\mathrm{OPT}$ is the smallest possible makespan.

*Ratio convention.* This is a minimization problem, and a ratio $\rho \ge 1$ means $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. The offline problems on this page are solved exactly, with $\rho = 1$.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of jobs and the number of machines |
| $p_j$ | the processing time of job $j$ on identical machines |
| $s_i$ | the speed of machine $i$ on uniform machines |
| $p_{ij}$ | the time that job $j$ needs if it runs only on machine $i$, on unrelated machines |
| $P_k$, $S_k$ | the sum of the $k$ largest $p_j$ and the sum of the $k$ largest $s_i$ |
| $C^*$ | the optimal preemptive makespan |

## Variants

- **Identical machines, $P \mid \mathrm{pmtn} \mid C_{\max}$.** $\mathrm{OPT} = \max(\frac1m \sum_j p_j, \max_j p_j)$, reached by the [wrap-around rule](/mcnaughton-wrap-around/) with at most $m - 1$ preemptions.
- **Uniform machines, $Q \mid \mathrm{pmtn} \mid C_{\max}$.** Machine $i$ does $s_i$ units of work per unit of time. Sort $p_1 \ge \cdots \ge p_n$ and $s_1 \ge \cdots \ge s_m$, and add jobs of length $0$ so that $n \ge m$. Then
$$\mathrm{OPT} = \max\Big( \max_{1 \le k \le m - 1} \frac{P_k}{S_k},\ \frac{P_n}{S_m} \Big).$$
Horvath, Lam and Sethi (1977) reached this value with the level algorithm, and Gonzalez and Sahni (1978) with at most $2(m - 1)$ preemptions. See [uniform machine scheduling](/uniform-machine-scheduling/).
- **Unrelated machines, $R \mid \mathrm{pmtn} \mid C_{\max}$.** Job $j$ needs time $p_{ij}$ on machine $i$, and a piece of length $t$ on machine $i$ does the fraction $t / p_{ij}$ of the job. The optimum is the value of a linear program (Lawler and Labetoulle 1978); see Bounds. See also [unrelated machine scheduling](/unrelated-machine-scheduling/).
- **Online.** Jobs arrive one by one and must be scheduled at once, without later changes. Chen, van Vliet and Woeginger (1995) gave the best deterministic ratio for identical machines, $1/(1 - (1 - \frac1m)^m)$, which tends to $\frac{e}{e - 1} \approx 1.582$ (cited, not proved here).
- **Precedence constraints.** With precedence constraints, $P \mid \mathrm{pmtn}, \mathrm{prec} \mid C_{\max}$ is NP-hard (Ullman 1976, cited); see [precedence-constrained scheduling](/precedence-constrained-scheduling/).

## Examples

**Identical machines.** Take $m = 2$ and $p = (3, 3, 2)$. The bound is $\max(\frac82, 3) = 4$. The wrap-around rule puts job 1 on $M_1$ in $[0, 3)$, job 2 on $M_1$ in $[3, 4)$ and on $M_2$ in $[0, 2)$, and job 3 on $M_2$ in $[2, 4)$. The two pieces of job 2 do not overlap in time, and the makespan is $4$. Without preemption, two of the three jobs share a machine, so the best makespan is $5$.

**Uniform machines.** Take $m = 2$, speeds $s = (2, 1)$ and $p = (3, 3)$. The formula gives $\max(\frac32, \frac63) = 2$. In $[0, 1)$, job 1 runs on $M_1$ and does $2$ units, and job 2 runs on $M_2$ and does $1$ unit. In $[1, 2)$, the jobs change machines, and each job gets the rest of its work. Both jobs end at $2$. Without preemption, the best makespan is $3$, either with both jobs on $M_1$ or with job 2 alone on $M_2$.

## Known algorithms

| problem | method | time | result |
|---|---|---|---|
| $P \mid \mathrm{pmtn} \mid C_{\max}$ | [wrap-around rule](/mcnaughton-wrap-around/) (McNaughton 1959) | $O(n + m)$ | exact, at most $m - 1$ preemptions |
| $Q \mid \mathrm{pmtn} \mid C_{\max}$ | level algorithm (Horvath, Lam and Sethi 1977) | polynomial | exact |
| $Q \mid \mathrm{pmtn} \mid C_{\max}$ | Gonzalez and Sahni 1978 | polynomial | exact, at most $2(m - 1)$ preemptions |
| $R \mid \mathrm{pmtn} \mid C_{\max}$ | [linear program](/linear-programming-problem/) and decomposition (Lawler and Labetoulle 1978) | polynomial | exact |
| online $P \mid \mathrm{pmtn} \mid C_{\max}$ | Chen, van Vliet and Woeginger 1995 | polynomial | ratio $1/(1 - (1 - \frac1m)^m)$ |

The rule for $P$ and the method for $R$ are proved on this page and on the page of the rule. The methods for $Q$ and the online ratio are cited.

## Bounds

All bounds below are absolute.

**Identical machines (proved).** Every preemptive schedule has makespan at least $\frac1m \sum_j p_j$, since the machines give $mC$ units of time by time $C$, and at least $\max_j p_j$, since a job runs on one machine at a time. These are the [makespan lower bounds](/makespan-lower-bounds/), and they hold with preemption. The wrap-around rule reaches the larger one; its [correctness proof](/mcnaughton-wrap-around/) is full.

**Uniform machines, the lower bound (proved).** Let a schedule have makespan $C$, and fix $k \le m - 1$. At each moment, the $k$ longest jobs run on at most $k$ different machines, whose speeds add up to at most $S_k$. So by time $C$ they have received at most $S_k C$ units of work, and they need $P_k$. Hence $C \ge P_k / S_k$. The same argument with all jobs and all machines gives $C \ge P_n / S_m$. That the largest of these bounds can always be reached is cited from Horvath, Lam and Sethi, and from Gonzalez and Sahni; it also follows from the linear program below, with $p_{ij} = p_j / s_i$.

**Unrelated machines (proved, with the Birkhoff-von Neumann theorem).** Let $x_{ij} \ge 0$ be the total time that job $j$ runs on machine $i$. The linear program is

$$\begin{aligned} \text{minimize } & C \\ \text{subject to } & \textstyle\sum_i x_{ij} / p_{ij} = 1 && \text{for each job } j, \\ & \textstyle\sum_j x_{ij} \le C && \text{for each machine } i, \\ & \textstyle\sum_i x_{ij} \le C && \text{for each job } j, \\ & x_{ij} \ge 0, \end{aligned}$$

where $x_{ij} = 0$ is forced if job $j$ cannot run on machine $i$. Every preemptive schedule of makespan $C$ gives a feasible solution: the first constraint says that each job is done, the second that a machine works at most $C$, and the third that the pieces of a job, which do not overlap in time, fit into $[0, C)$. So the value $C^*$ of the program is a lower bound.

To reach it, let $X$ be the $m \times n$ matrix $(x_{ij})$ of an optimal solution, and let $r_i$ and $c_j$ be its row and column sums, all at most $C^*$. Build the square matrix of size $m + n$

$$Y = \begin{pmatrix} X & \operatorname{diag}(C^* - r_i) \\ \operatorname{diag}(C^* - c_j) & X^{\mathsf T} \end{pmatrix}.$$

Every row and every column of $Y$ has sum $C^*$, so $Y / C^*$ is doubly stochastic. By the [Birkhoff-von Neumann decomposition](/birkhoff-von-neumann-decomposition/), $Y = C^* \sum_t \lambda_t \Pi_t$ with permutation matrices $\Pi_t$, weights $\lambda_t \ge 0$ and $\sum_t \lambda_t = 1$. Each $\Pi_t$, restricted to the block $X$, pairs some machines with some jobs, with each machine and each job in at most one pair. Run these pairings one after another, the $t$-th for time $\lambda_t C^*$. Then machine $i$ runs job $j$ for exactly $x_{ij}$, no machine runs two jobs at once, no job runs on two machines at once, and the schedule ends at $C^*$. The program has polynomial size, and the decomposition has at most $(m + n)^2$ terms and is found in polynomial time, so the whole method is polynomial. $\square$

**The gap to the nonpreemptive optimum (proved).** Let $C^*$ be the preemptive optimum on identical machines and $\mathrm{OPT}_{np}$ the nonpreemptive one. A [list schedule](/list-scheduling-bound/) has makespan at most $\frac1m \sum_j p_j + (1 - \frac1m)\max_j p_j \le (2 - \frac1m) C^*$, so $C^* \le \mathrm{OPT}_{np} \le (2 - \frac1m) C^*$. With $m + 1$ jobs of length $1$, $C^* = \frac{m + 1}{m}$ and $\mathrm{OPT}_{np} = 2$, so the gap can be $\frac{2m}{m + 1}$, which tends to $2$.

**For the problem.** The offline problems are solved exactly, so no approximation threshold applies. The online ratio $1/(1 - (1 - \frac1m)^m)$ is tight among deterministic online algorithms (cited).

## Reductions

- **A relaxation of makespan minimization.** Every nonpreemptive schedule is preemptive, so $C^*$ is a lower bound for [makespan minimization](/makespan-minimization/), and the gap above bounds the loss.
- **To linear programming.** $R \mid \mathrm{pmtn} \mid C_{\max}$ reduces to one linear program and one decomposition of a doubly stochastic matrix, the same method that solves preemptive [open shop scheduling](/open-shop-scheduling/).
- **Rounding for nonpreemptive problems.** A related program, with fractional assignments of jobs to machines, and with job $j$ kept off machine $i$ when $p_{ij}$ is larger than the guess of the optimum, is the relaxation that [Lenstra, Shmoys and Tardos](/lenstra-shmoys-tardos/) round to get a factor $2$ for $R \mid\mid C_{\max}$.

## Applications

- **Time sharing.** An operating system can stop a process and resume it on another processor, so the preemptive optimum is the target when the cost of a switch is small.
- **Divisible work.** Work that can be split at any point, such as batch computation or production that can move between lines, fits the preemptive model.
- **Lower bounds.** The preemptive optimum is a fast and exact lower bound for the nonpreemptive problems, and it is used in the analysis of algorithms such as [list scheduling](/list-scheduling/).

## References
