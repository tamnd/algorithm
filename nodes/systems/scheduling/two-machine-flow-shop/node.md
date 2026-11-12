---
tag: CN21V3
kind: problem
slug: two-machine-flow-shop
name: Two-machine flow shop
aliases:
- F2||Cmax
- two-stage flow shop
area: systems/scheduling
level: advanced
summary: "Jobs each run first on machine 1, then on machine 2; find the schedule that finishes all of them earliest, F2||Cmax. Johnson's rule solves it in O(n log n)."
prereqs: [flow-shop-scheduling, makespan]
see_also: [johnsons-rule, johnsons-rule-two-machine-flow-shop, three-machine-flow-shop, flow-shop-scheduling, job-shop-scheduling, open-shop-scheduling, makespan-lower-bounds, strong-np-hardness]
sources:
  - paper: doi:10.1002/nav.3800010110
    title: S. M. Johnson, Optimal two- and three-stage production schedules with setup times included, Naval Research Logistics Quarterly 1(1), 1954
    locator: pages 61 to 68 (the two-stage problem and its optimal rule)
  - paper: doi:10.1287/moor.1.2.117
    title: M. R. Garey, D. S. Johnson and Ravi Sethi, The complexity of flowshop and jobshop scheduling, Mathematics of Operations Research 1(2), 1976
    locator: pages 117 to 129 (strong NP-hardness of F2||ΣCj and of F3||Cmax)
  - paper: "doi:10.1016/S0167-5060(08)70743-X"
    title: Jan Karel Lenstra, Alexander H. G. Rinnooy Kan and Peter Brucker, Complexity of machine scheduling problems, Annals of Discrete Mathematics 1, 1977
    locator: pages 343 to 362 (strong NP-hardness of F2|rj|Cmax and F2||Lmax)
  - paper: doi:10.1287/opre.12.5.655
    title: P. C. Gilmore and R. E. Gomory, Sequencing a one state-variable machine, a solvable case of the traveling salesman problem, Operations Research 12(5), 1964
    locator: pages 655 to 679 (the polynomial algorithm that solves the two-machine no-wait flow shop)
  - paper: doi:10.1002/nav.3800030307
    title: James R. Jackson, An extension of Johnson's results on job lot scheduling, Naval Research Logistics Quarterly 3(3), 1956
    locator: pages 201 to 203 (the two-machine job shop)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 6, Section 6.1, Flow Shops with Unlimited Intermediate Storage
  - book: "Richard W. Conway, William L. Maxwell and Louis W. Miller, Theory of Scheduling, Addison-Wesley, 1967"
    locator: Chapter 5, the flow shop (permutation schedules are optimal for two and three machines)
---

The two-machine flow shop is the problem of scheduling $n$ jobs that each need one operation on machine 1 and then one operation on machine 2, so that the last job finishes as early as possible. In [Graham's notation](/scheduling-notation/) it is $F2 \| C_{\max}$, the case $m = 2$ of the [flow shop](/flow-shop-scheduling/). It is one of the few shop problems with a fast exact algorithm: [Johnson's rule](/johnsons-rule/) finds an optimal order in $O(n \log n)$ time. Adding one more machine, or changing the objective to the sum of completion times, makes it strongly NP-hard. This page is the problem as it appears in a two-stage pipeline; the [approximation-area page](/flow-shop-scheduling/) covers $m$ machines and their approximation algorithms.

## In plain words

Each job goes through two stations in the same order, for example a read from disk and then a computation on the processor. A station handles one job at a time, and a job can only start at the second station after it has left the first. Between the two stations there is room for as many waiting jobs as needed. You choose the order of the jobs. A bad order leaves the second station idle at the start, while it waits, or the first station busy at the end while the second one has nothing to do. The goal is the order that finishes all jobs earliest.

## Definition

**Input.** $n$ jobs. Job $j$ has a time $a_j \ge 0$ on machine 1 and a time $b_j \ge 0$ on machine 2.

**Schedule.** Start times $S_{1j}$ and $S_{2j}$ such that each machine runs at most one operation at a time, no operation is preempted, and $S_{2j} \ge S_{1j} + a_j$ for each job. The buffer between the machines has no limit.

**Goal.** Minimize the makespan $C_{\max} = \max_j (S_{2j} + b_j)$.

**Permutation schedules.** A schedule is a *permutation schedule* if both machines run the jobs in the same order. For two machines there is always an optimal permutation schedule: if machine 2 runs some job $j$ right before job $i$ while machine 1 runs $i$ before $j$, then run $j$ before $i$ on machine 1 instead, which does not delay anything on machine 2. So an instance is solved by an order $\pi$, and the jobs then run as early as possible:

$$C_{\max}(\pi) = \max_{1 \le k \le n} \Big( \sum_{l \le k} a_{\pi(l)} + \sum_{l \ge k} b_{\pi(l)} \Big).$$

The term for $k$ is the length of the path that runs on machine 1 up to job $\pi(k)$ and then on machine 2 from that job on. The same claim holds for three machines and fails for four; the [optimality page](/johnsons-rule-two-machine-flow-shop/) proves both.

## Variants

| problem | status | source |
|---|---|---|
| $F2 \| C_{\max}$ | $O(n \log n)$ | [Johnson's rule](/johnsons-rule/), Johnson 1954 |
| $F2 \mid \text{no-wait} \mid C_{\max}$ | polynomial | a special traveling salesman problem, Gilmore and Gomory 1964 |
| $F2 \| \sum C_j$ | strongly NP-hard | Garey, Johnson and Sethi 1976 |
| $F2 \mid r_j \mid C_{\max}$ | strongly NP-hard | Lenstra, Rinnooy Kan and Brucker 1977 |
| $F2 \| L_{\max}$ | strongly NP-hard | Lenstra, Rinnooy Kan and Brucker 1977 |
| $F3 \| C_{\max}$ | strongly NP-hard | Garey, Johnson and Sethi 1976; see [three machines](/three-machine-flow-shop/) |

In the no-wait variant a job must start on machine 2 at the moment it ends on machine 1, as in a pipeline with no buffer. The change of objective from $C_{\max}$ to $\sum C_j$ is enough to move the problem from one sort to strongly NP-hard.

## Examples

**A two-stage pipeline.** Four requests each read their data from disk (machine 1) and then compute on the processor (machine 2).

| request | $A$ | $B$ | $C$ | $D$ |
|---|---|---|---|---|
| read $a_j$ | 6 | 2 | 5 | 3 |
| compute $b_j$ | 3 | 5 | 4 | 1 |

In the input order $A, B, C, D$ the processor waits $6$ units for the first read, and the makespan is $19$. Johnson's rule puts $B$ first, since its read is short and its compute is long, and $D$ last, since its compute is shortest. The order $B, C, A, D$ gives this schedule:

| request | disk | processor |
|---|---|---|
| $B$ | 0 to 2 | 2 to 7 |
| $C$ | 2 to 7 | 7 to 11 |
| $A$ | 7 to 13 | 13 to 16 |
| $D$ | 13 to 16 | 16 to 17 |

The makespan is $17$. It is the unique optimum among the $24$ orders, and the worst order takes $23$. It meets the lower bound $\sum_j a_j + \min_j b_j = 16 + 1 = 17$: the disk is busy until $16$, and the last request still needs at least one unit on the processor after that.

**Two orders on two machines do not help.** Machine 2 may run the jobs in an order different from machine 1. By the argument in the definition, no such schedule is shorter than the best permutation schedule.

**Four machines.** Jobs $(1, 4, 4, 1)$ and $(4, 1, 1, 4)$ on four machines: the best permutation schedule takes $14$, but running the jobs in one order on machines 1 and 2 and in the other order on machines 3 and 4 takes $12$. So the reduction to one order is special to $m \le 3$.

## Known algorithms

- **[Johnson's rule](/johnsons-rule/).** Put first the jobs with $a_j \le b_j$ in increasing order of $a_j$, then the others in decreasing order of $b_j$. $O(n \log n)$ time, and optimal.
- **Johnson's original procedure.** Repeatedly take the smallest of the remaining $2n$ times; if it is on machine 1, the job goes to the front, if on machine 2, to the back. It gives an order of the same kind; see [the optimality page](/johnsons-rule-two-machine-flow-shop/).
- **Brute force.** All $n!$ orders with the formula above, $O(n! \, n)$ time. Only a test oracle.

## Bounds

- **Lower bounds on the makespan.** $C_{\max} \ge \max\big(\sum_j a_j + \min_j b_j,\ \min_j a_j + \sum_j b_j,\ \max_j (a_j + b_j)\big)$. The optimum can be above all three: with $a = (1, 2)$ and $b = (1, 2)$ each bound is $4$, and both orders take $5$, because the formula above has a middle term $a_1 + a_2 + b_2 = 5$ in one order and $a_2 + b_2 + b_1 = 5$ in the other. These bounds are the [makespan lower bounds](/makespan-lower-bounds/) of the shop setting.
- **Time.** $O(n \log n)$ by Johnson's rule, for any of the two forms.
- **Number of schedules.** Only $n!$ permutation schedules need to be considered, out of $(n!)^2$ pairs of machine orders.

## Reductions

- **To a sort.** Johnson's rule reduces the problem to sorting by the key $(a_j \le b_j,\ a_j \text{ or } -b_j)$.
- **A special case of two-machine job shops.** In a job shop each job has its own route. Jackson 1956 extended Johnson's rule to two machines with routes of length at most two: jobs that go 1 then 2 use Johnson's order on machine 1 first, and jobs that go 2 then 1 use the mirror order. See [job shop scheduling](/job-shop-scheduling/).
- **Reversal.** Swapping the roles of the machines and reversing time maps an instance $(a, b)$ to $(b, a)$, and an optimal order to its reverse, with the same makespan.
- **From three-partition, for the hard variants.** The strong NP-hardness proofs of $F2 \| \sum C_j$ and of $F3 \| C_{\max}$ reduce from [3-partition](/three-partition/).

## Applications

- **Two-stage pipelines.** Read then compute, compute then write back, decode then render, or transfer to a device then run a kernel: when the stages have a buffer between them and one worker each, ordering the batch by Johnson's rule gives the shortest batch time.
- **Production.** Johnson's own setting was a two-stage production line, such as printing then binding.
- **A bound for longer lines.** For $m$ machines, two-machine problems built from groups of machines give lower bounds and starting orders for heuristics, as in the reduction on the [three-machine page](/three-machine-flow-shop/).

## References
