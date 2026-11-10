---
tag: EZHVTD
kind: problem
slug: machine-covering
name: Machine covering
aliases:
- max-min machine covering
- P||Cmin
- maximizing the minimum machine completion time
area: approximation/scheduling-approximation
level: advanced
summary: Maximize the minimum load over the machines.
prereqs: [makespan-minimization, longest-processing-time-first]
see_also: [makespan-minimization, longest-processing-time-first, lpt-bound, bin-covering, three-partition, strong-np-hardness, ptas, makespan-lower-bounds]
sources:
  - paper: "B. L. Deuermeyer, D. K. Friesen and M. A. Langston, Scheduling to maximize the minimum processor finish time in a multiprocessor system, SIAM Journal on Algebraic and Discrete Methods 3(2), 1982, pp. 190-196"
    title: Deuermeyer, Friesen and Langston 1982
    locator: the theorem that LPT gives at least 3/4 of the optimal minimum load
  - paper: "J. Csirik, H. Kellerer and G. Woeginger, The exact LPT-bound for maximizing the minimum completion time, Operations Research Letters 11(5), 1992, pp. 281-287"
    title: Csirik, Kellerer and Woeginger 1992
    locator: the main theorem, the bound (3m - 1)/(4m - 2) for LPT, and the instances that reach it
  - paper: "G. J. Woeginger, A polynomial-time approximation scheme for maximizing the minimum machine completion time, Operations Research Letters 20(4), 1997, pp. 149-154"
    title: Woeginger 1997
    locator: the approximation scheme for P||Cmin
  - paper: "N. Alon, Y. Azar, G. J. Woeginger and T. Yadid, Approximation schemes for scheduling on parallel machines, Journal of Scheduling 1(1), 1998"
    title: Alon, Azar, Woeginger and Yadid 1998
    locator: the linear-time approximation schemes for a class of objectives that includes the minimum machine load
---

Machine covering, written $P \mid\mid C_{\min}$, asks to assign $n$ jobs to $m$ identical machines so that the smallest machine load is as large as possible. It is the max-min twin of [makespan minimization](/makespan-minimization/): the same jobs and machines, but the goal is to keep every machine busy for a long time instead of making every machine finish early. It is strongly NP-hard, [LPT](/longest-processing-time-first/) gives at least $\frac{3m - 1}{4m - 2} \ge \frac34$ of the optimum, and Woeginger (1997) gave a PTAS.

## In plain words

You have a set of tasks and a team of equal workers, and every task goes to one worker. This time you want the least busy worker to have as much work as possible. You can think of each worker as a lamp and of each task as a battery: the room is lit only while every lamp is on, so you want the lamp that goes out first to last as long as possible.

Finding the best split is hard, for the same reason as for the usual problem. But the rule "give the longest task left to the worker with the least work so far" always gets at least three quarters of the best value.

## Definition

**Input.** An integer $m \ge 1$, the number of machines, and $n$ jobs with processing times $p_1, \ldots, p_n \ge 0$. Here $n$ is the number of jobs and $m$ is the number of machines.

**Output.** An assignment $\sigma$ of each job to a machine. The load of machine $i$ is $\ell_i = \sum_{j : \sigma(j) = i} p_j$.

**Goal.** Maximize $C_{\min} = \min_i \ell_i$. $\mathrm{OPT}$ is the largest possible value.

*Ratio convention.* This is a maximization problem. A ratio $\alpha \le 1$ means $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ on every instance, and a larger $\alpha$ is better.

**Upper bounds on the optimum.** The proofs compare with upper bounds, not lower bounds, since the problem is a maximization. The *average load bound* is $\mathrm{OPT} \le \frac1m \sum_j p_j$, because the smallest load is at most the average. If $n < m$, some machine is empty and $\mathrm{OPT} = 0$.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of jobs and the number of machines |
| $p_j$ | the processing time of job $j$ |
| $\ell_i$ | the load of machine $i$ |
| $C_{\min}$ | the smallest load $\min_i \ell_i$ |
| $\mathrm{OPT}$ | the largest possible $C_{\min}$ |

## Variants

- **Decision version and bin covering.** "Is there an assignment with $C_{\min} \ge T$?" is the question whether the jobs cover $m$ bins of threshold $T$. [Bin covering](/bin-covering/) asks for the largest number of covered bins for a fixed $T$, so machine covering is to bin covering what makespan minimization is to [bin packing](/bin-packing/).
- **Two machines.** For $m = 2$, the question $C_{\min} \ge \frac12 \sum_j p_j$ is the [partition problem](/partition-problem/). It is NP-hard in the weak sense and is solved by a dynamic program in time $O(n \sum_j p_j)$.
- **Fixed $m$.** A dynamic program over the vector of loads solves the problem exactly in pseudopolynomial time when $m$ is fixed.
- **Online.** Jobs arrive one by one and must be assigned at once. No deterministic online algorithm has ratio better than $\frac1m$; the proof is in the section Bounds.
- **Other machine models.** On uniform and on unrelated machines the problem is also studied. The unrelated version, with job times that depend on the machine, is known as the Santa Claus problem in fair allocation.

## Examples

**Two machines.** Take $p = (3, 3, 2, 2, 2)$. LPT gives $3$ to $M_1$, $3$ to $M_2$, then $2$ to $M_1$, $2$ to $M_2$, and the last $2$ to $M_1$. The loads are $7$ and $5$, so $C_{\min} = 5$. The split $\{3, 3\}$ and $\{2, 2, 2\}$ gives $6$ and $6$, so $\mathrm{OPT} = 6$, which is also the average load. The ratio is $\frac56 = \frac{3m - 1}{4m - 2}$ for $m = 2$.

**Three machines.** Take $p = (5, 5, 4, 4, 3, 3, 3, 3)$, with total $30$. LPT puts $5, 5, 4$ on $M_1, M_2, M_3$, the second $4$ on $M_3$ (load $8$), and the first two jobs of $3$ on $M_1$ and $M_2$ (loads $8$). The last two jobs of $3$ go to two of the three machines, and one machine stays at $8$. So $C_{\min} = 8$. The split $\{5, 5\}$, $\{4, 3, 3\}$, $\{4, 3, 3\}$ gives $10$ on every machine, so $\mathrm{OPT} = 10$, and the ratio is $\frac{8}{10} = \frac{3m - 1}{4m - 2}$ for $m = 3$.

## Known algorithms

| algorithm | ratio $\alpha$ | tight for the algorithm | time |
|---|---|---|---|
| [LPT](/longest-processing-time-first/) | $\frac34$ (Deuermeyer, Friesen and Langston 1982) | no; the exact value is $\frac{3m - 1}{4m - 2}$ | $O(n \log n)$ |
| LPT, exact analysis | $\frac{3m - 1}{4m - 2}$ (Csirik, Kellerer and Woeginger 1992) | yes; the family below | $O(n \log n)$ |
| Woeginger's PTAS | $1 - \varepsilon$ | not applicable | polynomial for each fixed $\varepsilon$ |
| Alon, Azar, Woeginger and Yadid 1998 | $1 - \varepsilon$ | not applicable | linear in $n$ for each fixed $\varepsilon$ |
| dynamic program over loads, fixed $m$ | exact | not applicable | pseudopolynomial |

The LPT upper bounds and the schemes are cited, not proved here; the lower side of the exact LPT value is proved in the section Bounds. The schemes round the long jobs to few sizes and treat the short jobs as divisible, as in the [PTAS](/ptas/) for makespan.

## Bounds

All bounds below are absolute.

**Strong NP-hardness (proved).** Take an instance of [3-partition](/three-partition/): $3m$ positive integers $a_j$ with $\sum_j a_j = mB$ and $\frac B4 < a_j < \frac B2$. Make one job of time $a_j$ for each number, and use $m$ machines. Then $\mathrm{OPT} \ge B$ if and only if the numbers split into $m$ triples of sum $B$. If $\mathrm{OPT} \ge B$, every load is at least $B$ and the total is $mB$, so every load is exactly $B$. A machine with load $B$ has exactly $3$ jobs, since two jobs give less than $B$ and four give more. The converse is clear. The times are the numbers of the 3-partition instance, which is NP-hard in the strong sense, so $P \mid\mid C_{\min}$ is [strongly NP-hard](/strong-np-hardness/).

**No FPTAS unless P = NP (proved).** For integer times, $\mathrm{OPT}$ is an integer at most $P = \sum_j p_j$. An algorithm with ratio $1 - \frac{1}{P + 1}$ returns a value larger than $\mathrm{OPT} - 1$, so the optimum. An FPTAS with this $\varepsilon$ would run in time polynomial in $n$ and $P$, which would solve the strongly NP-hard problem in pseudopolynomial time.

**The tight family for LPT (proved).** Let $m \ge 2$. Take two jobs each of length $2m - 1, 2m - 2, \ldots, m + 1$, and $m + 1$ jobs of length $m$. Then $\mathrm{OPT} = 4m - 2$ and LPT gives $C_{\min} = 3m - 1$.

*Proof.* The total is $2 \sum_{x = m+1}^{2m-1} x + m(m + 1) = 3m(m - 1) + m^2 + m = m(4m - 2)$, so $\mathrm{OPT} \le 4m - 2$ by the average load bound. For $m = 2$, the split $\{3, 3\}$ and $\{2, 2, 2\}$ reaches $6$. For $m \ge 3$, use the sets $\{2m - 1, 2m - 1\}$, two sets $\{2m - 2, m, m\}$, and for each $x$ from $m + 1$ to $2m - 3$ the set $\{x, 3m - 2 - x, m\}$. Each set has sum $4m - 2$. The values $x$ and $3m - 2 - x$ both run over $m + 1, \ldots, 2m - 3$, so each such length is used twice, and the $m$ jobs used are $4 + (m - 3) = m + 1$. There are $1 + 2 + (m - 3) = m$ sets, so $\mathrm{OPT} = 4m - 2$.

The $2m - 2$ long jobs are the long jobs of the tight family in the proof of the [LPT bound](/lpt-bound/), and LPT runs on them in the same way: machines $1$ and $2$ end with load $2m - 1$ and the other $m - 2$ machines with load $3m - 1$. The next two jobs of length $m$ go to machines $1$ and $2$, and all loads are $3m - 1$. The last $m - 1$ jobs of length $m$ go to $m - 1$ different machines, since each raises a load to $4m - 1$ and a machine of load $3m - 1$ is still free. One machine stays at $3m - 1$, so $C_{\min} = 3m - 1$. $\square$

So $\frac{\mathrm{LPT}}{\mathrm{OPT}} = \frac{3m - 1}{4m - 2}$, which decreases to $\frac34$ as $m$ grows. With the upper bound of Csirik, Kellerer and Woeginger, this value is tight for LPT for each $m$, and $\frac34$ is the best constant for LPT over all $m$.

**Online lower bound (proved).** Let $m \ge 2$. For any deterministic online algorithm, give $m$ jobs of length $1$. If two of them go to the same machine, stop: some machine is empty, so $\mathrm{ALG} = 0$ while $\mathrm{OPT} = 1$. Otherwise each machine has one of them, and $m - 1$ jobs of length $m$ follow. Some machine gets none of these, so $\mathrm{ALG} \le 1$. The schedule with each long job alone and the $m$ unit jobs on the last machine has $C_{\min} = m$. So $\mathrm{ALG} \le \frac1m\,\mathrm{OPT}$.

**For the problem.** The PTAS shows that no constant $\alpha < 1$ is a hardness threshold, and the strong NP-hardness shows that $\alpha = 1$ cannot be reached in polynomial time unless P = NP.

## Reductions

- **From 3-partition.** The reduction above shows strong NP-hardness. It uses the same instances as the reduction for [makespan minimization](/makespan-minimization/), since a 3-partition instance has a schedule with every load equal to $B$ in both problems.
- **To bin covering.** The decision version is a [bin covering](/bin-covering/) question with $m$ bins of threshold $T$, and a binary search over $T$ turns an exact method for it into one for machine covering.
- **Relation with makespan.** The two problems have the same feasible schedules but different goals, and a schedule that is good for one need not be good for the other. With $m = 2$ they are the same, since $\ell_1 + \ell_2$ is fixed, and the larger load is small exactly when the smaller load is large.

## Applications

- **Keeping machines busy.** A system that works only while all its processors have work should make the first processor to run out of work do so as late as possible.
- **Fair allocation.** Split indivisible goods among people who value them the same way, so that the person with the least value gets as much as possible.
- **Sequencing of parts and supplies.** Distribute spare parts, batteries or fuel units among identical units so that the unit that stops first runs as long as possible.

## References
