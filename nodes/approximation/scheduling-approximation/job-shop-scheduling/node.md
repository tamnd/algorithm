---
tag: A35V3B
kind: problem
slug: job-shop-scheduling
name: Job shop scheduling
aliases:
- JSP
- J||Cmax
- job-shop problem
area: approximation/scheduling-approximation
level: advanced
summary: Each job visits the machines in its own fixed order; minimize makespan.
prereqs: [scheduling-notation, machine-environments, makespan, flow-shop-scheduling]
see_also: [open-shop-scheduling, critical-path-method, randomized-rounding, chernoff-bound, lovasz-local-lemma, makespan-lower-bounds, strong-np-hardness, three-partition]
sources:
  - paper: "D. B. Shmoys, C. Stein and J. Wein, Improved approximation algorithms for shop scheduling problems, SIAM Journal on Computing 23(3), 1994, pages 617 to 632"
    locator: the random delays technique and the polylogarithmic approximation for the job shop
  - paper: "L. A. Goldberg, M. Paterson, A. Srinivasan and E. Sweedyk, Better approximation guarantees for job-shop scheduling, SIAM Journal on Discrete Mathematics 14(1), 2001"
    locator: the improvement by a factor log log of the Shmoys-Stein-Wein bound
  - paper: "D. P. Williamson, L. A. Hall, J. A. Hoogeveen, C. A. J. Hurkens, J. K. Lenstra, S. V. Sevast'janov and D. B. Shmoys, Short shop schedules, Operations Research 45(2), 1997, pages 288 to 294"
    locator: the NP-hardness of deciding makespan at most 4, which rules out ratios below 5/4
  - paper: "M. R. Garey, D. S. Johnson and R. Sethi, The complexity of flowshop and jobshop scheduling, Mathematics of Operations Research 1(2), 1976, pages 117 to 129"
    locator: the strong NP-hardness of the flow shop and the job shop with few machines
  - paper: "J. K. Lenstra, A. H. G. Rinnooy Kan and P. Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977"
    locator: the NP-hardness of the job shop with two machines and at most three operations per job
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 6, Shop Scheduling Problems (job shop problems and the disjunctive graph)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 7, Job Shops (Deterministic)
---

Job shop scheduling, written $J \mid\mid C_{\max}$, is the shop problem where each job is a chain of operations, each on a given machine, to be done in a given order that differs from job to job. Each machine runs one operation at a time. The goal is the least [makespan](/makespan/). The job shop contains the [flow shop](/flow-shop-scheduling/), where all jobs have the same route, and it is one of the hardest classic scheduling problems in practice: a $10 \times 10$ instance of Fisher and Thompson from 1963 stayed unsolved until 1989. In theory, the best ratio known grows slowly with the input, from the random delays method of Shmoys, Stein and Wein (1994), and no constant ratio is known.

## In plain words

Think of a workshop with a lathe, a drill and a saw. Each order has its own recipe: one goes to the drill, then the lathe, then the saw; another goes to the saw first. Each machine handles one piece at a time, and a piece must finish one step before it starts the next. You decide, for each machine, the order of the pieces that wait for it, and you want all orders done as early as possible.

Two limits are easy to see: the busiest machine needs all its work, and the longest recipe needs all its steps. But unlike simpler shops, the best plan can be well above both limits, because the routes cross and block each other. Finding the best plan is very hard, and the best methods that come with a proof only promise a result within a slowly growing factor of the best.

## Definition

**Input.** Integers $m \ge 1$ and $n \ge 1$. Job $j$ is a sequence of $\mu_j$ operations $O_{1j}, O_{2j}, \ldots, O_{\mu_j j}$. Operation $O_{kj}$ must run on machine $m_{kj}$ for time $p_{kj} \ge 0$, without interruption. Let $\mu = \max_j \mu_j$.

**Output.** A start time $S_{kj}$ for each operation, such that the operations of each job run in their order ($S_{k+1, j} \ge S_{kj} + p_{kj}$) and no two operations on the same machine overlap.

**Goal.** Minimize $C_{\max} = \max_j (S_{\mu_j j} + p_{\mu_j j})$. The least value is $\mathrm{OPT}$.

*Ratio convention.* This is a minimization problem. An algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. All ratios here are absolute and worst case, and the ratio of a randomized algorithm bounds its makespan with high probability.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of jobs and the number of machines |
| $\mu_j$, $\mu$ | the number of operations of job $j$, and the largest one |
| $m_{kj}$, $p_{kj}$ | the machine and the time of the $k$-th operation of job $j$ |
| $\Pi_{\max}$ | the largest machine load, the maximum over machines $i$ of the total time of the operations on $i$ |
| $P_{\max}$ | the largest job length, $\max_j \sum_k p_{kj}$ |
| $\mathrm{LB}$ | $\max(\Pi_{\max}, P_{\max})$ |
| $\mathrm{OPT}$, $\mathrm{ALG}$ | the optimal makespan, and the makespan of an algorithm |

## Variants

- **Flow shop.** All jobs have the route $1, 2, \ldots, m$; see [flow shop scheduling](/flow-shop-scheduling/).
- **Two machines, at most two operations per job, $J2 \mid \mu_j \le 2 \mid C_{\max}$.** Jackson (1956) solved it by splitting the jobs by route and applying Johnson's rule to each group. With at most three operations per job and two machines, the problem is NP-hard (Lenstra, Rinnooy Kan and Brucker 1977).
- **Unit times.** $J2 \mid p_{kj} = 1 \mid C_{\max}$ is polynomial, but $J3 \mid p_{kj} = 1 \mid C_{\max}$ is strongly NP-hard (Lenstra and Rinnooy Kan 1979).
- **Acyclic job shop.** Each job visits each machine at most once. Packet routing on a network is the case with unit times, where Leighton, Maggs and Rao (1994) showed that a schedule of length $O(\mathrm{LB})$ always exists.
- **Preemption.** $J2 \mid \mathrm{pmtn} \mid C_{\max}$ is still NP-hard.
- **Flexible job shop.** Each operation may choose among several machines. It contains [unrelated machine scheduling](/unrelated-machine-scheduling/).

## Examples

**OPT can exceed both lower bounds.** Take two machines and three jobs:

| job | first operation | second operation | length |
|---|---|---|---|
| 1 | machine 1, time 3 | machine 2, time 3 | 6 |
| 2 | machine 1, time 2 | machine 2, time 2 | 4 |
| 3 | machine 2, time 1 | machine 1, time 1 | 2 |

Both machines have load 6, so $\mathrm{LB} = 6$. A schedule of makespan 6 would keep job 1 busy all the time, on machine 1 in $[0, 3]$ and on machine 2 in $[3, 6]$. Then the operation of job 2 on machine 1 starts at 3 or later, so its operation on machine 2 starts at 5 or later and overlaps job 1 there. So $\mathrm{OPT} > 6$, and in fact $\mathrm{OPT} = 8$, met by this schedule:

| machine | operations |
|---|---|
| machine 1 | job 1 in $[0, 3]$, job 2 in $[3, 5]$, job 3 in $[5, 6]$ |
| machine 2 | job 3 in $[0, 1]$, idle, job 1 in $[3, 6]$, job 2 in $[6, 8]$ |

## Known algorithms

| algorithm | ratio $\rho$ | tight for the algorithm | time |
|---|---|---|---|
| any schedule without unforced idle time | $\mu$ | the proved bound | polynomial |
| Shmoys, Stein and Wein 1994, random delays | $O\!\left(\frac{\log^2(m \mu)}{\log \log (m \mu)}\right)$ | no | polynomial, randomized, and derandomized |
| Goldberg, Paterson, Srinivasan and Sweedyk 1997 | $O\!\left(\frac{\log^2(m \mu)}{(\log \log (m \mu))^2}\right)$ | no | polynomial |
| Shmoys, Stein and Wein 1994, fixed $m$ | $2 + \varepsilon$ | no | polynomial for fixed $m$ and $\varepsilon$ |
| Jansen, Solis-Oba and Sviridenko, fixed $m$ and $\mu$ | $1 + \varepsilon$ (PTAS) | not applicable | polynomial for fixed $m$, $\mu$ and $\varepsilon$ |
| branch and bound on the disjunctive graph | exact | not applicable | exponential |

**The random delays idea.** Assume first that all operations have unit time. Give each job a random delay, chosen uniformly from $\{0, 1, \ldots, \Pi_{\max} - 1\}$, and then run every job without waiting, as if machines could run several operations at once. A [Chernoff bound](/chernoff-bound/) shows that, with high probability, no machine has more than $O(\log(m\mu)/\log\log(m\mu))$ operations at one time step. Spreading each time step into that many steps gives a legal schedule of length $O(\mathrm{LB} \cdot \log(m\mu)/\log\log(m\mu))$ when all operations have unit time. General times cost one more logarithmic factor in the analysis. This is only a sketch; the full argument, with the reduction from general times and the derandomization, is in the paper.

## Bounds

- **Lower bound.** $\mathrm{OPT} \ge \mathrm{LB} = \max(\Pi_{\max}, P_{\max})$, since each machine runs one operation at a time and each job runs one operation at a time. Every ratio in the table is proved against this bound.
- **The lower bound is weak.** Feige and Scheideler (1998) gave instances where $\mathrm{OPT}$ is larger than $\mathrm{LB}$ by a factor of order $\log \mathrm{LB} / \log \log \mathrm{LB}$. So methods that compare only with $\mathrm{LB}$ cannot give a constant ratio.
- **Strong NP-hardness.** The job shop contains the three-machine flow shop, which is strongly NP-hard (Garey, Johnson and Sethi 1976). So there is no FPTAS unless P = NP.
- **No ratio below 5/4.** Williamson, Hall, Hoogeveen, Hurkens, Lenstra, Sevast'janov and Shmoys (1997) showed that deciding $\mathrm{OPT} \le 4$ is NP-hard for the job shop with integer times, while $\mathrm{OPT} \le 3$ is polynomial. So no polynomial algorithm has ratio below $5/4$ unless P = NP.
- **Stronger hardness.** Mastrolilli and Svensson (2011) showed that, under a complexity assumption stronger than P ≠ NP, no polynomial algorithm has a constant ratio for the job shop when $m$ and $\mu$ are part of the input. Whether a constant ratio is NP-hard to reach is open.

## Reductions

**From the flow shop.** A flow shop instance is a job shop instance in which all routes are $1, 2, \ldots, m$. So the strong NP-hardness of $F3 \mid\mid C_{\max}$ carries over to $J3 \mid\mid C_{\max}$.

**To the disjunctive graph.** Make a node for each operation, a *conjunctive* arc from each operation to the next one of its job, and a *disjunctive* pair of arcs between any two operations on the same machine. A schedule chooses one arc of each pair so that the graph has no cycle, and its makespan is the length of the longest path, with the times as node weights. So the problem is to choose the orientation with the shortest longest path, and every exact method works on this graph; the longest path is a [critical path](/critical-path-method/).

**To unrelated machines (flexible job shop).** If each job has one operation that may run on several machines, the job shop becomes [unrelated machine scheduling](/unrelated-machine-scheduling/).

## Applications

- Workshops that make parts to order, where each part has its own route through the machines.
- Scheduling of tasks in manufacturing systems, chemical plants and steel mills.
- Packet routing in networks, where each packet follows its own path and each link carries one packet at a time.

## References
