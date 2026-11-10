---
tag: EH3JRT
kind: problem
slug: flow-shop-scheduling
name: Flow shop scheduling
aliases:
- permutation flow shop
- F||Cmax
- flowshop scheduling
area: approximation/scheduling-approximation
level: advanced
summary: Every job visits all machines in the same order.
prereqs: [scheduling-notation, machine-environments, makespan, np-hard]
see_also: [johnsons-rule, two-machine-flow-shop, three-machine-flow-shop, job-shop-scheduling, open-shop-scheduling, three-partition, strong-np-hardness, makespan-lower-bounds]
sources:
  - paper: "S. M. Johnson, Optimal two- and three-stage production schedules with setup times included, Naval Research Logistics Quarterly 1(1), 1954, pages 61 to 68"
    locator: the optimal rule for two machines and the special cases with three machines
  - paper: "M. R. Garey, D. S. Johnson and R. Sethi, The complexity of flowshop and jobshop scheduling, Mathematics of Operations Research 1(2), 1976, pages 117 to 129"
    locator: the strong NP-hardness of the three-machine flow shop by a reduction from 3-partition
  - paper: "D. P. Williamson, L. A. Hall, J. A. Hoogeveen, C. A. J. Hurkens, J. K. Lenstra, S. V. Sevast'janov and D. B. Shmoys, Short shop schedules, Operations Research 45(2), 1997, pages 288 to 294"
    locator: the NP-hardness of deciding makespan at most 4, which rules out ratios below 5/4
  - paper: "L. A. Hall, Approximability of flow shop scheduling, Mathematical Programming 82, 1998"
    locator: the polynomial-time approximation scheme for a fixed number of machines
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 6, Shop Scheduling Problems (flow shop problems)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 6, Flow Shops and Flexible Flow Shops (Deterministic)
---

Flow shop scheduling, written $F \mid\mid C_{\max}$, is the shop problem where all jobs visit the machines in the same order: first machine 1, then machine 2, up to machine $m$. Each machine runs one job at a time, and each job is on one machine at a time. The goal is the least [makespan](/makespan/). For two machines, [Johnson's rule](/johnsons-rule/) of 1954 finds an optimal schedule in $O(n \log n)$ time, which is one of the first results of scheduling theory. For three machines the problem is already strongly NP-hard. It sits between the [open shop](/open-shop-scheduling/), where the order of the operations is free, and the [job shop](/job-shop-scheduling/), where each job has its own order.

## In plain words

Think of a production line. Every product goes through the same stations in the same order: cutting, then painting, then packing. Each station handles one product at a time, and each product spends a known time at each station. You choose the order in which the products enter the line, and you want the last product to leave as early as possible.

The trouble is waiting. If a product that is slow at the second station follows one that is slow there too, the line jams, and the first station may sit idle later. With two stations there is a simple, perfect rule: put first the products that are quick at the first station, and put last the products that are quick at the second station. With three or more stations, no fast perfect rule is expected to exist.

## Definition

**Input.** Integers $m \ge 1$ and $n \ge 1$, and times $p_{ij} \ge 0$ for each machine $i$ and job $j$. Job $j$ has the operations $O_{1j}, O_{2j}, \ldots, O_{mj}$, and $O_{ij}$ must run on machine $i$ for time $p_{ij}$ without interruption.

**Output.** A start time $S_{ij}$ for each operation, such that the operations of a job run in the order $1, 2, \ldots, m$ ($S_{i+1, j} \ge S_{ij} + p_{ij}$), and no two operations on the same machine overlap.

**Goal.** Minimize $C_{\max} = \max_j (S_{mj} + p_{mj})$. The least value is $\mathrm{OPT}$.

**Permutation schedules.** A schedule is a *permutation schedule* if the jobs pass every machine in the same order. The problem restricted to such schedules is the *permutation flow shop*, written $F \mid \mathrm{prmu} \mid C_{\max}$. For $m \le 3$ some optimal schedule is a permutation schedule, but for $m \ge 4$ the best permutation schedule may be worse.

*Ratio convention.* This is a minimization problem. An algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. All ratios here are absolute and worst case.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of jobs and the number of machines |
| $p_{ij}$ | the time of the operation of job $j$ on machine $i$ |
| $\Pi_{\max}$ | the largest machine load, $\max_i \sum_j p_{ij}$ |
| $P_{\max}$ | the largest job length, $\max_j \sum_i p_{ij}$ |
| $\mathrm{OPT}$, $\mathrm{ALG}$ | the optimal makespan, and the makespan of an algorithm |

## Variants

- **Two machines, $F2 \mid\mid C_{\max}$.** Solvable in $O(n \log n)$ by Johnson's rule; see [the two-machine flow shop](/two-machine-flow-shop/).
- **Three machines, $F3 \mid\mid C_{\max}$.** Strongly NP-hard. Johnson's rule is optimal only in special cases, for example when the middle machine is dominated by one of the others; see [the three-machine flow shop](/three-machine-flow-shop/).
- **Other objectives.** $F2 \mid\mid \sum C_j$ is already strongly NP-hard (Garey, Johnson and Sethi 1976).
- **No wait.** A job must go from one machine to the next without waiting. $F2 \mid \text{no-wait} \mid C_{\max}$ becomes a special traveling salesman problem that Gilmore and Gomory (1964) solved in polynomial time.
- **Flexible flow shop.** Each stage has several parallel machines. It contains [makespan minimization](/makespan-minimization/) as the case of one stage.
- **Preemption.** $F2 \mid \mathrm{pmtn} \mid C_{\max}$ has the same optimum as $F2 \mid\mid C_{\max}$, but $F3 \mid \mathrm{pmtn} \mid C_{\max}$ is NP-hard (Gonzalez and Sahni 1978).

## Examples

**Johnson's rule on five jobs.** Take two machines and these times:

| job | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| machine 1, $a_j$ | 3 | 5 | 1 | 6 | 7 |
| machine 2, $b_j$ | 6 | 2 | 2 | 6 | 5 |

The jobs with $a_j \le b_j$ are 1, 3 and 4; in increasing order of $a_j$ they give $3, 1, 4$. The jobs with $a_j > b_j$ are 2 and 5; in decreasing order of $b_j$ they give $5, 2$. The order is $3, 1, 4, 5, 2$:

| job | machine 1 | machine 2 |
|---|---|---|
| 3 | 0 to 1 | 1 to 3 |
| 1 | 1 to 4 | 4 to 10 |
| 4 | 4 to 10 | 10 to 16 |
| 5 | 10 to 17 | 17 to 22 |
| 2 | 17 to 22 | 22 to 24 |

The makespan is 24. It is optimal: machine 1 is busy for $3 + 5 + 1 + 6 + 7 = 22$, and after it ends, the last job still needs at least $\min_j b_j = 2$ on machine 2. The order $1, 2, 3, 4, 5$ gives 27.

## Known algorithms

| algorithm | ratio $\rho$ | tight for the algorithm | time |
|---|---|---|---|
| any permutation without idle time that is not forced | $m$ | the proved bound | $O(nm)$ |
| [Johnson's rule](/johnsons-rule/), $m = 2$ | exact | not applicable | $O(n \log n)$ |
| Gonzalez and Sahni 1978, Johnson's rule on pairs of machines | $\lceil m/2 \rceil$ | the proved bound | $O(mn \log n)$ |
| Hall 1998, fixed $m$ | $1 + \varepsilon$ (PTAS) | not applicable | polynomial for fixed $m$ and $\varepsilon$ |
| methods for the [job shop](/job-shop-scheduling/) (Shmoys, Stein and Wein 1994) | $O(\log^2 m / \log \log m)$ for this case | no | polynomial, randomized |
| NEH heuristic (Nawaz, Enscore and Ham 1983) | none proved | not applicable | $O(n^2 m)$ with a careful update |

The table compares with $\mathrm{OPT}$; most proofs compare with the lower bound $\max(\Pi_{\max}, P_{\max})$. The first row holds because the makespan of a permutation schedule without unforced idle time is the length of a path that moves through the machines in order and uses on each machine $i$ only operations of machine $i$, so it is at most $\sum_i \Pi_i \le m \Pi_{\max}$, where $\Pi_i$ is the load of machine $i$. For the permutation flow shop, Potts, Shmoys and Williamson (1991) showed that the best permutation schedule can be a factor of order $\sqrt{m}$ above the best schedule. In practice the NEH heuristic and local search on permutations are the standard tools, and the Taillard instances of 1993 are the usual benchmark.

## Bounds

- **Lower bounds on OPT.** $\mathrm{OPT} \ge \Pi_{\max}$, since a machine runs one operation at a time, and $\mathrm{OPT} \ge P_{\max}$, since a job runs one operation at a time. For two machines, $\mathrm{OPT} \ge \sum_j a_j + \min_j b_j$ and $\mathrm{OPT} \ge \min_j a_j + \sum_j b_j$.
- **Strong NP-hardness for three machines.** Garey, Johnson and Sethi (1976) reduced [3-partition](/three-partition/) to $F3 \mid\mid C_{\max}$. So there is no pseudo-polynomial algorithm and no FPTAS unless P = NP.
- **No ratio below 5/4 when $m$ is part of the input.** Williamson, Hall, Hoogeveen, Hurkens, Lenstra, Sevast'janov and Shmoys (1997) showed that deciding $\mathrm{OPT} \le 4$ is NP-hard when $m$ is part of the input and all times are integers, while $\mathrm{OPT} \le 3$ can be decided in polynomial time. So no polynomial algorithm has ratio below $5/4$ unless P = NP.
- **Fixed $m$.** For each fixed $m$ there is a PTAS (Hall 1998), so for fixed $m$ the problem is not APX-hard.

## Reductions

**From 3-partition (sketch only).** Garey, Johnson and Sethi build, from a 3-partition instance with $q$ triples of sum $B$, a three-machine instance and a target makespan. Extra jobs fill the machines so that only $q$ windows of equal length stay free, and the jobs made from the numbers can meet the target only if they fill these windows exactly, three numbers of sum $B$ in each. The numbers stay polynomial in size, which gives strong NP-hardness. The full construction and its proof are long and are not given here; see [the three-machine flow shop](/three-machine-flow-shop/) and the paper.

**To the job shop.** Every flow shop instance is a [job shop](/job-shop-scheduling/) instance in which all jobs have the order $1, 2, \ldots, m$. So job shop algorithms apply, and flow shop hardness holds for the job shop.

**Two machines and sequencing.** For two machines, the makespan of an order is $\max_k \left( \sum_{j \le k} a_{\pi(j)} + \sum_{j \ge k} b_{\pi(j)} \right)$. Johnson's rule minimizes this maximum by an exchange argument; see [Johnson's rule](/johnsons-rule/).

## Applications

- Production lines in which each product passes the same stations, such as machining, assembly and painting.
- Pipelines of computing stages, such as reading, processing and writing a batch of files.
- Printing and binding of books, and other two-stage processes, which is the setting of Johnson's paper.

## References
