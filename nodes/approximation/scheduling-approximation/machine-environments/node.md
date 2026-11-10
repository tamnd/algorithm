---
tag: ZWQH8W
kind: concept
slug: machine-environments
name: Machine environments (identical, uniform, unrelated)
aliases:
- identical, uniform and unrelated machines
- machine environment
- shop environments
area: approximation/scheduling-approximation
level: intro
summary: 'Speed models: identical machines, machines with speeds, and machine-dependent processing times.'
prereqs: [scheduling-problem, makespan]
see_also: [scheduling-notation, identical-machines, uniform-machines, unrelated-machines, makespan-minimization, open-shop-scheduling, flow-shop-scheduling, job-shop-scheduling]
sources:
  - paper: doi:10.1016/S0167-5060(08)70356-X
    title: "R. L. Graham, E. L. Lawler, J. K. Lenstra and A. H. G. Rinnooy Kan, Optimization and approximation in deterministic sequencing and scheduling: a survey, Annals of Discrete Mathematics 5, 1979"
    locator: Section 2.2 (machine environment) and the sections on parallel machines and on open, flow and job shops
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 2, Section 2.1 (machine environments); Chapters 5 and 6 (parallel machines), Chapters 6 to 8 (flow shops, job shops and open shops)
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 1 (machine environments and reduction graphs), Chapter 5 (parallel machines), Chapter 6 (shop scheduling problems)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.3 (identical machines), Section 3.2 (identical machines, the approximation scheme), Section 11.1 (unrelated machines and the generalized assignment problem)
---

A machine environment is the part of a [scheduling problem](/scheduling-problem/) that says what the machines are and how a job uses them. It is the field $\alpha$ of the [three-field notation](/scheduling-notation/). The four one-stage environments are a single machine ($1$), identical machines ($P$), uniform machines with speeds ($Q$) and unrelated machines ($R$), in order of growing generality. The three shop environments are the flow shop ($F$), the job shop ($J$) and the open shop ($O$), where each job has several operations on different machines.

## In plain words

Think of a print shop with several printers. If all printers are the same model, a job takes the same time on each one: these are identical machines. If some printers are just faster, say twice as fast, every job runs twice as fast on them: these are uniform machines. If each printer is good at some jobs and bad at others, so that the time depends on the pair of job and printer in any way, these are unrelated machines.

In a shop, each job needs several steps on different machines, like a car that goes through painting and then drying. In a flow shop all jobs visit the machines in the same order. In a job shop each job has its own route. In an open shop the steps can come in any order, but two steps of one job never run at the same time.

## The idea

There are $n$ jobs and $m$ machines. The notation is the one of the [three-field notation](/scheduling-notation/) page.

**One-stage environments.** Each job is one operation, done on one machine (or on several machines in turn, if [preemption](/preemption/) is allowed).

- **Single machine, $1$.** Job $j$ takes $p_j$. The order of the jobs is the only decision.
- **Identical machines, $P$.** Job $j$ takes $p_j$ on each machine. A schedule without idle time is an assignment of the jobs to machines, and machine $i$ has the load $\sum_{j \text{ on } i} p_j$. See [identical machines](/identical-machines/).
- **Uniform machines, $Q$.** Machine $i$ has a speed $s_i > 0$, and job $j$ takes $p_{ij} = p_j / s_i$ on it. A faster machine is faster for every job by the same factor. See [uniform machines](/uniform-machines/) and [uniform machine scheduling](/uniform-machine-scheduling/).
- **Unrelated machines, $R$.** Job $j$ takes $p_{ij} \ge 0$ on machine $i$, and the matrix $(p_{ij})$ is arbitrary. The value $p_{ij} = \infty$ forbids job $j$ on machine $i$. See [unrelated machines](/unrelated-machines/) and [unrelated machine scheduling](/unrelated-machine-scheduling/).
- **Restricted assignment, $P \mid M_j \mid \cdot$.** A special case of $R$ that sits between $P$ and $R$: $p_{ij} = p_j$ if $i \in M_j$ and $p_{ij} = \infty$ otherwise. See [restricted assignment scheduling](/restricted-assignment-scheduling/).

These form a chain of special cases:

$$1 \;\subset\; P \;\subset\; Q \;\subset\; R .$$

A $P$ instance is a $Q$ instance with all $s_i = 1$, and a $Q$ instance is an $R$ instance with $p_{ij} = p_j / s_i$. So an algorithm for $R$ solves $Q$ and $P$, and a hardness result for $P$ holds for $Q$ and $R$. The matrix of a $Q$ instance has rank one; the matrix of an $R$ instance can be any non-negative matrix.

**Shop environments.** Job $j$ has operations $O_{1j}, O_{2j}, \ldots$, each on a given machine with a given time. Two operations of one job never run at the same time, and a machine runs one operation at a time.

- **Flow shop, $F$.** Each job has exactly one operation on each machine, and visits the machines in the order $M_1, M_2, \ldots, M_m$. See [flow shop scheduling](/flow-shop-scheduling/). In a *permutation* flow shop ($\mathrm{prmu}$ in $\beta$), each machine also takes the jobs in the same order.
- **Job shop, $J$.** Each job has its own sequence of operations, and each operation names its machine. A job can visit a machine more than once (recirculation) or skip it. See [job shop scheduling](/job-shop-scheduling/).
- **Open shop, $O$.** Each job has one operation on each machine (some of length $0$), and the order of the operations of a job is free. See [open shop scheduling](/open-shop-scheduling/).

The flow shop is a job shop in which all routes are the same. The open shop is not a special case of the job shop, because its routes are part of the decision.

**The number of machines.** In the notation, $P$ means that $m$ is part of the input, and $Pm$ (for example $P2$) means that $m$ is a fixed constant. The difference matters for complexity. Makespan on $P2$ is the partition problem, which is weakly NP-hard and has a pseudo-polynomial algorithm. Makespan on $P$ with $m$ in the input is strongly NP-hard, by a reduction from [3-partition](/three-partition/).

**Makespan in each environment.** The table gives the status of $C_{\max}$, without and with preemption.

| environment | $\alpha \mid\mid C_{\max}$ | $\alpha \mid \mathrm{pmtn} \mid C_{\max}$ |
|---|---|---|
| $1$ | trivial: $C_{\max} = \sum_j p_j$ | the same |
| $P$ | strongly NP-hard; [list scheduling](/list-scheduling/) $2 - 1/m$, [LPT](/longest-processing-time-first/) $4/3 - 1/(3m)$, a [PTAS](/hochbaum-shmoys-ptas/) | $O(n)$ by [McNaughton](/mcnaughton-wrap-around/) |
| $Q$ | strongly NP-hard; a PTAS (Hochbaum and Shmoys 1988) | polynomial (Horvath, Lam and Sethi 1977; Gonzalez and Sahni 1978) |
| $R$ | strongly NP-hard; [2-approximation](/lenstra-shmoys-tardos/), no $3/2 - \varepsilon$ unless P = NP | polynomial by a linear program (Lawler and Labetoulle 1978) |
| $F$ | $F2$: $O(n \log n)$ by [Johnson's rule](/johnsons-rule/); $F3$: strongly NP-hard | $F2$ polynomial; $F3$ strongly NP-hard |
| $J$ | $J2$ NP-hard; $J$ strongly NP-hard | $J2$ NP-hard |
| $O$ | $O2$: linear time; $O3$: NP-hard | polynomial (Gonzalez and Sahni 1976) |

The preemptive results are on the page [preemptive makespan scheduling](/preemptive-makespan-scheduling/).

## Examples

**One instance in four environments.** Take $n = 4$ jobs and $m = 2$ machines, with $p = (6, 4, 3, 3)$, total $16$.

- On one machine, $C_{\max} = 16$ for each order.
- On $P2$, a load of $8$ would need a subset of sum $8$, and none exists. The best split is $\{6, 3\}$ and $\{4, 3\}$, so the optimum is $9$.
- On $Q2$ with speeds $s = (2, 1)$, a set of total size $x$ on the fast machine takes $x / 2$, and the rest takes $16 - x$. The split $\{6, 4\}$ and $\{3, 3\}$ gives $\max(5, 6) = 6$, and $\{6, 3, 3\}$ and $\{4\}$ also gives $6$. The optimum is $6$: the reachable values of $x$ near $32/3$ are $10$ and $12$, and both give $6$.
- On $R2$ with $p_{1j} = (6, 4, 3, 3)$ on machine 1 and $p_{2j} = (2, 8, 1, 6)$ on machine 2, the optimum is $7$. Jobs 2 and 4 go to machine 1 (load $7$), and jobs 1 and 3 go to machine 2 (load $3$). Here job 2 is fast on machine 1, and job 1 is fast on machine 2, which no speed vector can express.

**One instance in two shops.** Take four jobs, each with an operation of length $a_j$ on $M_1$ and $b_j$ on $M_2$: $(a, b) = (3, 2), (1, 4), (2, 2), (4, 1)$.

- As a flow shop $F2$, Johnson's rule puts first the jobs with $a_j \le b_j$ in increasing $a_j$, then the others in decreasing $b_j$: the order is job 2, job 3, job 1, job 4. Its makespan is $11$, and this is optimal: $M_1$ is busy for $\sum a_j = 10$, and the last job still needs at least $\min_j b_j = 1$ on $M_2$.
- As an open shop $O2$, the optimum is $\max(\sum a_j, \sum b_j, \max_j (a_j + b_j)) = \max(10, 9, 5) = 10$. The freedom to choose the order of the two operations saves one unit.

## Where it is used

- [Scheduling notation](/scheduling-notation/) uses these symbols as the field $\alpha$.
- [Makespan minimization](/makespan-minimization/) is the problem $P \mid\mid C_{\max}$; [uniform machine scheduling](/uniform-machine-scheduling/) and [unrelated machine scheduling](/unrelated-machine-scheduling/) treat $Q$ and $R$.
- [Lenstra, Shmoys and Tardos](/lenstra-shmoys-tardos/) and [unrelated machine scheduling by LP rounding](/unrelated-machine-scheduling-makespan/) round a linear program that only makes sense for $R$.
- [Preemptive makespan scheduling](/preemptive-makespan-scheduling/) shows how the answer changes with the environment: a formula for $P$, a sorted formula for $Q$, a linear program for $R$.
- [Machine covering](/machine-covering/) uses the same environments with the objective of the smallest load.

## References
