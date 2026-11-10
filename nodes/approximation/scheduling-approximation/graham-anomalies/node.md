---
tag: ZZDCCK
kind: concept
slug: graham-anomalies
name: Graham's scheduling anomalies
aliases:
- scheduling anomalies
- multiprocessing anomalies
- timing anomalies
area: approximation/scheduling-approximation
level: advanced
summary: Adding machines or relaxing constraints can increase the list-schedule makespan.
prereqs: [list-scheduling, list-scheduling-bound, precedence-constrained-scheduling]
see_also: [list-scheduling-bound, list-scheduling, precedence-constrained-scheduling, critical-path-lower-bound, makespan-lower-bounds, coffman-graham-algorithm, multifit-bound, makespan]
sources:
  - paper: doi:10.1002/j.1538-7305.1966.tb01709.x
    title: "R. L. Graham, Bounds for certain multiprocessing anomalies, Bell System Technical Journal 45(9), 1966"
    locator: the anomalies of list schedules under precedence constraints and the bound 1 + (m - 1)/m' on their effect (pp. 1563-1581 for the paper)
  - paper: doi:10.1137/0117039
    title: "R. L. Graham, Bounds on multiprocessing timing anomalies, SIAM Journal on Applied Mathematics 17(2), 1969"
    locator: the example with nine tasks on three processors and its four changes, and the general bound on the ratio of two list schedules (pp. 416-429 for the paper)
---

Graham's scheduling anomalies are instances in which a change that should help a [list schedule](/list-scheduling/) makes it longer: more machines, shorter jobs, fewer precedence constraints, or a different list. Graham found them in 1966 for jobs with [precedence constraints](/precedence-constrained-scheduling/) on identical machines, and gave a nine-job example on three machines in which each of the four changes increases the [makespan](/makespan/). He also proved that the damage is bounded: after any such change, the makespan grows by a factor of at most $1 + \frac{m - 1}{m'}$, where $m$ and $m'$ are the old and new numbers of machines.

## In plain words

A list schedule follows a fixed rule: when a worker is free, he takes the first task in the list that is ready. This rule does not plan ahead. If one task ends early, or a new worker joins, a worker may take a task earlier than before. Then he is busy at the moment when an important task becomes ready, and that task must wait. The important task may be the start of a long line of tasks, so the whole plan ends later.

The best plan does not have this problem. With more workers or shorter tasks, the best plan can always do at least as well as before. Only the simple rule is fooled.

## The idea

There are $n$ jobs with times $p_j \ge 0$, $m$ identical machines, a precedence order on the jobs, and a priority list. Here $n$ is the number of jobs and $m$ the number of machines. The list schedule starts, whenever a machine is free, the first job of the list whose predecessors are all done. Write $\omega$ for its makespan.

**Monotone and not monotone.** The optimal makespan $\mathrm{OPT}$ is monotone: it does not increase if a machine is added, if a job time decreases, or if a precedence constraint is removed, because the old optimal schedule stays feasible, or, after a decrease of times, can run each job in its old start time with a shorter length. The list schedule $\omega$ is a heuristic, and it has none of these properties. An anomaly is an instance and a change in which $\omega$ increases.

**The bound on the anomalies.** Let the first system have $m$ machines, times $p_j$, precedence order $\prec$ and any list, with makespan $\omega$. Let the second have $m'$ machines, times $p'_j \le p_j$, an order $\prec'$ contained in $\prec$, and any other list, with makespan $\omega'$. Then

$$\frac{\omega'}{\omega} \le 1 + \frac{m - 1}{m'} .$$

*Proof.* By part 2 of [Graham's bound](/list-scheduling-bound/), applied to the second system, $m' \omega' \le \sum_j p'_j + (m' - 1) L'$, where $L'$ is the largest total time of a chain under $\prec'$. Every schedule of the first system runs all jobs on $m$ machines and runs each chain in sequence, so $\sum_j p_j \le m \omega$ and the largest chain $L$ is at most $\omega$. A chain of $\prec'$ is a chain of $\prec$ and its times are not larger, so $L' \le L \le \omega$, and $\sum_j p'_j \le \sum_j p_j \le m\omega$. Hence $m'\omega' \le m\omega + (m' - 1)\omega$, which is the claim. $\square$

The proof uses only the [lower bounds](/makespan-lower-bounds/) of the first system, average load and [critical path](/critical-path-lower-bound/), so it holds when the first schedule is optimal too. For $m' = m$, it says that two list schedules of the same instance differ by a factor of at most $2 - \frac1m$. The family of part 3 of [Graham's bound](/list-scheduling-bound/) reaches this factor for a change of the list only. Graham showed that the bound is the best possible in general (cited, not proved here).

*Ratio convention.* All the problems here are minimization problems. A ratio $\rho \ge 1$ means $\omega' \le \rho \cdot \omega$, or $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ when the first schedule is optimal. The bound $1 + \frac{m - 1}{m'}$ is absolute.

## Examples

The jobs $T_1, \ldots, T_9$ have times $p = (3, 2, 2, 2, 4, 4, 4, 4, 9)$. The precedence constraints are $T_1 \to T_9$ and $T_4 \to T_5, T_6, T_7, T_8$. The list is $T_1, T_2, \ldots, T_9$. All values below come from the list rule and are checked by the tests of the [list scheduling](/list-scheduling/) code.

**The base case: 3 machines, makespan 12.**

| machine | jobs and intervals |
|---|---|
| $M_1$ | $T_1$ $[0, 3)$, $T_9$ $[3, 12)$ |
| $M_2$ | $T_2$ $[0, 2)$, $T_4$ $[2, 4)$, $T_5$ $[4, 8)$, $T_7$ $[8, 12)$ |
| $M_3$ | $T_3$ $[0, 2)$, idle $[2, 4)$, $T_6$ $[4, 8)$, $T_8$ $[8, 12)$ |

This is optimal: the chain $T_1 \to T_9$ takes $12$, and the total time $34$ on $3$ machines needs at least $\frac{34}{3}$, so at least $12$ with integer times.

**Change the list: makespan 14.** With the list $T_1, T_2, T_4, T_5, T_6, T_3, T_9, T_7, T_8$, machine $M_1$ is free at time $3$ and takes $T_3$, which comes before $T_9$ in the list. So $T_9$ runs in $[5, 14)$.

**Add a machine: makespan 15.** With 4 machines and the base list, $T_1, T_2, T_3, T_4$ start at time $0$. At time $2$, three machines are free and take $T_5, T_6, T_7$. At time $3$, $M_1$ is free and $T_8$ and $T_9$ are both ready; $T_8$ comes first in the list. $T_9$ starts at $6$, when $T_5$ ends, and ends at $15$.

**Make every job shorter: makespan 13.** With all times minus $1$, $p = (2, 1, 1, 1, 3, 3, 3, 3, 8)$ on 3 machines, $T_4$ ends at $2$, and the three free machines take $T_5, T_6, T_7$ at time $2$. $T_8$ starts at $5$ on $M_1$, and $T_9$ starts at $5$ on the next machine that is free. $T_9$ ends at $13$.

**Remove constraints: makespan 16.** Without $T_4 \to T_5$ and $T_4 \to T_6$, the jobs $T_5$ and $T_6$ are ready early, and $T_6$ takes $M_1$ at time $3$. $T_9$ waits until $T_6$ ends at $7$ and ends at $16$.

In each case, a machine becomes free a little earlier or a job becomes ready a little earlier, and the rule fills a machine at the moment when $T_9$, the start of the long chain, would need it. The bound of the previous section allows these values: for example, $\frac{15}{12} \le 1 + \frac{2}{4}$ and $\frac{16}{12} \le 1 + \frac23$.

## Where it is used

- **Analysis of list scheduling.** The anomalies show that list scheduling cannot be analyzed by monotone arguments, such as "a faster machine never hurts". Proofs such as [Graham's bound](/list-scheduling-bound/) compare directly with lower bounds instead.
- **Real-time systems.** If a task can end early, a schedule that is built online by a list rule can end later than the schedule with the worst-case times. So testing a system with the worst-case time of each task does not give a safe bound on its finish time, and analysis must use bounds such as $1 + \frac{m - 1}{m'}$ or a rule without anomalies.
- **Design of priority lists.** [Hu's algorithm](/hu-algorithm/) and the [Coffman-Graham algorithm](/coffman-graham-algorithm/) choose the list from the precedence graph, so that jobs at the start of long chains come early. With unit times, they are optimal for in-trees and for two machines.
- **Bin packing and MULTIFIT.** The same effect occurs in packing: first fit decreasing can succeed with a bin capacity $C$ and fail with a larger one. [MULTIFIT](/multifit-bound/) is analyzed so that its search does not need monotone behavior.

## References
