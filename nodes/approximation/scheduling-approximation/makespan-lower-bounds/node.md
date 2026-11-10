---
tag: PVWW9F
kind: concept
slug: makespan-lower-bounds
name: Makespan lower bounds
aliases:
- average load bound
- largest job bound
- pair bound
area: approximation/scheduling-approximation
level: intro
summary: Average load and the largest job give lower bounds on the optimal makespan.
prereqs: [makespan, approximation-ratio]
see_also: [list-scheduling-bound, lpt-bound, sorted-balance, multifit-algorithm, mcnaughton-wrap-around, critical-path-lower-bound, bin-packing-lower-bound, dual-approximation]
sources:
  - paper: doi:10.1002/j.1538-7305.1966.tb01709.x
    title: "R. L. Graham, Bounds for certain multiprocessing anomalies, Bell System Technical Journal 45(9), 1966"
    locator: the proof of the bound 2 - 1/m, which compares with the average load and the longest job (pp. 1563-1581 for the paper)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.3 (the two lower bounds on the optimal makespan, used for local search, list scheduling and LPT)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 11.1 (the bounds T* >= (1/m) sum t_j, T* >= max t_j, and T* >= 2 t_(m+1) for Sorted-Balance)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 10 (minimum makespan scheduling, the lower bounds of the factor 2 algorithm)
---

A makespan lower bound is a number, computed fast from the instance, that the optimal [makespan](/makespan/) $\mathrm{OPT}$ can never go below. Every approximation proof for makespan scheduling needs one, because $\mathrm{OPT}$ itself is NP-hard to compute: the proof shows that the algorithm is at most $\rho$ times the bound, and so at most $\rho \cdot \mathrm{OPT}$. For $P \mid\mid C_{\max}$ the two basic bounds are the average load $\frac{1}{m}\sum_j p_j$ and the largest job $\max_j p_j$. The pair bound $p_m + p_{m+1}$ adds the fact that two of the $m + 1$ largest jobs share a machine.

## In plain words

You have some jobs to share among a few equal workers, and you want everyone done as early as possible. Even before you plan anything, you know two things. First, the total work must be done by the workers together, so the last worker cannot finish before the total divided by the number of workers. Second, a job cannot be split, so nobody finishes before the longest job is done.

A third fact helps when the jobs are long. If there are more jobs than workers, two of the longest ones go to the same worker. So that worker is busy for at least the sum of two long jobs. These quick facts are what the proofs of the scheduling rules compare against.

## The idea

We use the notation of [makespan minimization](/makespan-minimization/): $n$ jobs with processing times $p_1 \ge p_2 \ge \cdots \ge p_n \ge 0$ (sorted for this page), $m$ identical machines, and $\mathrm{OPT}$ the optimal makespan. Let $A = \frac{1}{m} \sum_j p_j$ be the average load.

**Theorem.** For every instance of $P \mid\mid C_{\max}$:

1. $\mathrm{OPT} \ge A$ (the average load bound);
2. $\mathrm{OPT} \ge p_1 = \max_j p_j$ (the largest job bound);
3. if $n \ge m + 1$, then $\mathrm{OPT} \ge p_m + p_{m+1}$ (the pair bound), and so $\mathrm{OPT} \ge 2 p_{m+1}$;
4. more generally, if $n \ge km + 1$ for an integer $k \ge 1$, then $\mathrm{OPT} \ge p_{km+1} + p_{km} + \cdots + p_{km+1-k}$, the sum of the $k + 1$ smallest of the $km + 1$ largest jobs, and so $\mathrm{OPT} \ge (k + 1)\, p_{km+1}$;
5. if all $p_j$ are integers, then $\mathrm{OPT} \ge \lceil A \rceil$.

*Proof.* Fix an optimal schedule, and let $L_i$ be the load of machine $i$, so $\mathrm{OPT} = \max_i L_i$.

1. The loads add up to the total work: $\sum_i L_i = \sum_j p_j = mA$. The largest of $m$ numbers is at least their mean, so $\max_i L_i \ge A$.
2. Job 1 runs on some machine $i$, so $L_i \ge p_1$.
3. This is case $k = 1$ of item 4.
4. The $km + 1$ jobs $1, \ldots, km + 1$ are spread over $m$ machines. By the pigeonhole principle some machine $i$ gets at least $k + 1$ of them. Any $k + 1$ jobs of this set have total time at least the sum of the $k + 1$ smallest times in the set, which is $p_{km+1-k} + \cdots + p_{km+1}$, because the set is sorted. So $L_i$ is at least this sum. Each of its $k + 1$ terms is at least $p_{km+1}$, which gives the second form.
5. With integer times, the loads are integers, and an integer that is at least $A$ is at least $\lceil A \rceil$. $\blacksquare$

**The basic bound is the preemptive optimum.** Let $\mathrm{LB} = \max(A, p_1)$. [McNaughton's wrap-around rule](/mcnaughton-wrap-around/) builds a preemptive schedule of length exactly $\mathrm{LB}$. So $\mathrm{LB}$ is the optimum of the relaxation $P \mid \mathrm{pmtn} \mid C_{\max}$, and no argument that uses only the total work and the longest job can give more. The pair bound uses the fact that jobs are not split, and this is why it can be larger than $\mathrm{LB}$.

**How far the bounds can be from the optimum.** [List scheduling](/list-scheduling/) builds a schedule of length at most $(2 - 1/m)\,\mathrm{LB}$, so

$$\mathrm{LB} \;\le\; \mathrm{OPT} \;\le\; \left(2 - \tfrac{1}{m}\right) \mathrm{LB}.$$

The factor almost $2$ can happen: with $m + 1$ jobs of length $1$, $\mathrm{LB} = (m+1)/m$ and $\mathrm{OPT} = 2$, so $\mathrm{OPT}/\mathrm{LB} = 2m/(m+1)$. The pair bound gives $2$ on this instance, which is exact. All the bounds together can still be below $\mathrm{OPT}$; otherwise $P \mid\mid C_{\max}$ would be easy.

**Other environments.** On uniform machines with speeds $s_1 \ge \cdots \ge s_m$, the bounds become $\sum_j p_j / \sum_i s_i$ and $\sum_{j \le k} p_j / \sum_{i \le k} s_i$ for $k < m$; together they give the preemptive optimum of $Q \mid \mathrm{pmtn} \mid C_{\max}$. On unrelated machines no simple formula works, and the bound is the value of a linear program, as in [Lenstra, Shmoys and Tardos](/lenstra-shmoys-tardos/). With precedence constraints, the length of the longest chain is a lower bound; see the [critical path lower bound](/critical-path-lower-bound/).

## Examples

**Six jobs on three machines.** Take $p = (6, 4, 3, 2, 2, 2)$ and $m = 3$. The total is $19$, so $A = 19/3$ and $\lceil A \rceil = 7$. The largest job gives $6$. The pair bound gives $p_3 + p_4 = 3 + 2 = 5$. The best bound is $7$, and the schedule $\{6\}, \{4, 3\}, \{2, 2, 2\}$ has makespan $7$, so $\mathrm{OPT} = 7$ and the integer average bound is exact.

**Where the pair bound wins.** Take $m = 2$ and $p = (5, 4, 3)$. Then $A = 6$ and $p_1 = 5$, but the pair bound gives $p_2 + p_3 = 7$. Some machine gets two jobs, and the two smallest add up to $7$, so $\mathrm{OPT} = 7$.

**Where all bounds fail.** Take $m = 2$ and $p = (9, 7, 7, 7)$. Then $A = 15$, $p_1 = 9$, the pair bound is $p_2 + p_3 = 14$, and item 4 does not apply for $k = 2$, since $n = 4 < 5$. The best bound is $15$. But a load of $15$ needs a subset of sum $15$, and the subset sums are $7, 9, 14, 16, 21, 23, 30$ and their complements, so none is $15$. The optimum is $16$, with $\{9, 7\}$ and $\{7, 7\}$.

**The general pigeonhole bound.** Take $m = 2$ and $p = (5, 5, 4, 4, 4)$. With $k = 2$, the $5$ largest jobs are on $2$ machines, so some machine has $3$ of them, and $\mathrm{OPT} \ge p_3 + p_4 + p_5 = 12$. The average bound gives only $11$, and the pair bound gives $9$. The schedule $\{5, 5\}, \{4, 4, 4\}$ shows $\mathrm{OPT} = 12$.

## Where it is used

- [Graham's bound for list scheduling](/list-scheduling-bound/) compares the start time of the last job with $A$ and its length with $p_1$, and gets $2 - 1/m$.
- [Sorted-Balance](/sorted-balance/) uses $\mathrm{OPT} \ge 2 p_{m+1}$ to prove the ratio $3/2$.
- [The LPT bound](/lpt-bound/) uses $A$ for small last jobs and a counting argument in the spirit of item 4 when all jobs are longer than $\mathrm{OPT}/3$.
- [MULTIFIT](/multifit-algorithm/) starts its binary search at $\max(A, p_1)$, and [dual approximation](/dual-approximation/) and the [Hochbaum-Shmoys PTAS](/hochbaum-shmoys-ptas/) search for a target makespan in the interval $[\mathrm{LB}, 2\,\mathrm{LB}]$.
- [McNaughton's wrap-around rule](/mcnaughton-wrap-around/) shows that $\max(A, p_1)$ is exactly the preemptive optimum.
- [Bin packing](/bin-packing-lower-bound/) has the matching size bound $\lceil \sum s_i \rceil$ for the number of bins.

## References
