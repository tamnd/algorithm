---
tag: 5ZXB86
kind: theorem
slug: multifit-bound
name: MULTIFIT approximation bound
aliases:
- 13/11 bound
- MULTIFIT ratio
area: approximation/scheduling-approximation
level: advanced
summary: MULTIFIT achieves ratio 13/11 on identical machines.
prereqs: [multifit-algorithm, first-fit-decreasing]
see_also: [multifit-algorithm, first-fit-decreasing, lpt-bound, list-scheduling-bound, dual-approximation, hochbaum-shmoys-ptas, bin-packing, makespan-minimization]
sources:
  - paper: doi:10.1137/0207001
    title: "E. G. Coffman Jr., M. R. Garey and D. S. Johnson, An application of bin-packing to multiprocessor scheduling, SIAM Journal on Computing 7(1), 1978"
    locator: the theorem that first fit decreasing succeeds at 1.22 OPT, the bound 1.22 + 2^-k, and the values for small m (pp. 1-17 for the paper)
  - paper: "D. K. Friesen, Tighter bounds for the MULTIFIT processor scheduling algorithm, SIAM Journal on Computing 13, 1984"
    title: Friesen 1984
    locator: the bound 1.2 + 2^-k and the example with ratio 13/11
  - paper: "M. Yue, On the exact upper bound for the MULTIFIT processor scheduling algorithm, Annals of Operations Research 24, 1990, pp. 233-259"
    title: Yue 1990
    locator: the main theorem, the bound 13/11
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 1, L. A. Hall, Approximation algorithms for scheduling (MULTIFIT and its bounds)
---

The MULTIFIT bound states that [MULTIFIT](/multifit-algorithm/) with $k$ search steps returns a schedule of makespan at most $\left(\frac{13}{11} + 2^{-k}\right)\mathrm{OPT}$ on identical machines, and that the constant $\frac{13}{11} \approx 1.182$ cannot be lowered. The bound has two parts: the binary search adds $2^{-k}$ to a threshold $r$, the factor above the optimum at which [first fit decreasing](/first-fit-decreasing/) always fits the jobs into $m$ bins, and the threshold itself is $\frac{13}{11}$. Coffman, Garey and Johnson (1978) proved $r \le 1.22$, Friesen (1984) gave $1.2$ and the example that shows $r \ge \frac{13}{11}$, and Yue (1990) proved $r \le \frac{13}{11}$. This page proves the reduction to the threshold, the threshold $\frac43 - \frac1{3m}$, and the lower bound; the constants $1.22$ and $\frac{13}{11}$ are cited.

## Statement

There are $n$ jobs with times $p_j \ge 0$ and $m \ge 1$ identical machines; $n$ is the number of jobs and $m$ the number of machines. $\mathrm{OPT}$ is the optimal makespan, and $\mathrm{MF}_k$ the makespan of MULTIFIT with $k$ steps. A capacity $C$ *succeeds* if first fit decreasing packs all jobs into at most $m$ bins of capacity $C$. Let $r_m$ be the least number such that, on every instance with $m$ machines, every capacity $C \ge r_m \cdot \mathrm{OPT}$ succeeds.

*Ratio convention.* This is a minimization problem, and a ratio $\rho \ge 1$ means $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance.

**Theorem.**

1. *(Reduction, proved here.)* $\mathrm{MF}_k \le (r_m + 2^{-k})\,\mathrm{OPT}$ for every instance and every $k \ge 0$.
2. *(A simple threshold, proved here.)* $r_m \le \frac43 - \frac1{3m}$.
3. *(The threshold, cited.)* $r_m \le 1.22$ (Coffman, Garey and Johnson 1978), $r_m \le 1.2$ (Friesen 1984), and $r_m \le \frac{13}{11}$ (Yue 1990), for every $m$.
4. *(Lower bound, proved here.)* For every $m \ge 13$, there is an instance with $\mathrm{OPT} = 66$ on which no capacity below $78$ succeeds, so $r_m \ge \frac{13}{11}$ and $\mathrm{MF}_k \ge \frac{13}{11}\,\mathrm{OPT}$ for every $k$.
5. *(Two machines.)* $r_2 = \frac87$; the upper bound is cited from Coffman, Garey and Johnson, and the lower bound is proved here.

So, for $m \ge 13$, the best constant in a bound of the form $\mathrm{MF}_k \le (r + 2^{-k})\,\mathrm{OPT}$ is exactly $r = \frac{13}{11}$. The bound is absolute. It is tight for the algorithm by part 4. It is not tight for the problem, which has a [PTAS](/hochbaum-shmoys-ptas/). The proof of part 1 compares with the [lower bounds](/makespan-lower-bounds/) $\mathrm{OPT} \ge \frac1m \sum_j p_j$ and $\mathrm{OPT} \ge \max_j p_j$.

## In plain words

MULTIFIT guesses a finish time, tests the guess with a packing rule, and halves the range of guesses after each test. Two things decide how good the answer is. One is how many tests you make: each test halves the leftover error. The other is how much room the packing rule needs above the best finish time before it never fails. That room is the main question.

A simple argument shows that the rule never fails with one third extra room. Long and careful work showed that about eighteen percent extra room is always enough. A clever example with thirteen workers shows that less room is not enough, so the answer cannot be improved by a better analysis.

## Proof

Sort the jobs so that $p_1 \ge \cdots \ge p_n$, and write $A = \frac1m \sum_j p_j$. Two facts about first fit decreasing are used throughout.

- *Prefix property.* The bins of the call on the jobs $1, \ldots, l$ are the bins of the full call restricted to these jobs, because each step depends only on the earlier steps.
- *Final loads.* If $C$ succeeds and the largest bin load is $M \le C$, then $M$ succeeds with the same bins. Each test "load plus $p_j$ at most $C$" that was true stays true at $M$, since the left side is at most a final load. Each test that was false stays false, since $M \le C$.

**Part 1.** MULTIFIT starts with $\mathrm{lo} = \max(A, \max_j p_j)$ and $\mathrm{hi} = \max(2A, \max_j p_j)$. The capacity $\mathrm{hi}$ succeeds: in first fit at most one bin has load at most half the capacity, because a job of a later such bin would have fit into the earlier one; so a failure would need more total size than $mA$. The search keeps three facts: $\mathrm{hi}$ succeeds, $\mathrm{lo} \le r_m \cdot \mathrm{OPT}$, and each step halves $\mathrm{hi} - \mathrm{lo}$. The first holds by line L5 of the algorithm. The second holds at the start, since $\mathrm{lo} \le \mathrm{OPT}$, and is kept because a failure at $C$ means $C < r_m \cdot \mathrm{OPT}$. The first interval has length at most $A \le \mathrm{OPT}$. So after $k$ steps

$$\mathrm{MF}_k \le \mathrm{hi} \le \mathrm{lo} + 2^{-k} A \le (r_m + 2^{-k})\,\mathrm{OPT}.$$

The detailed version of this argument is in [the correctness proof of MULTIFIT](/multifit-algorithm/).

**Part 2.** Let $C \ge (\frac43 - \frac1{3m})\,\mathrm{OPT}$ and suppose that the call fails at job $x$. By the prefix property, it fails at $x$ on $J' = (1, \ldots, x)$, where $x$ is a shortest job. Let $T = \mathrm{OPT}(J') \le \mathrm{OPT}$. Since $p_x \le T \le C$, all $m$ bins are open and each has load more than $C - p_x$.

If $p_x \le T/3$, adding the loads gives $\sum_{j \in J'} p_j - p_x > m(C - p_x)$, so $C < T + (1 - \frac1m)p_x \le (\frac43 - \frac1{3m})\,T$, which is false. If $p_x > T/3$, every job of $J'$ is longer than $T/3$, so an optimal schedule of $J'$ has at most $2$ jobs per machine. A bin that holds a single job $y$ has $p_y > C - p_x \ge T - p_x$, so $y$ cannot share a machine with any other job in that schedule. If $a$ bins hold one job, the other $m - a$ bins hold at least two, so $|J'| - 1 \ge a + 2(m - a)$. But the optimal schedule puts the $a$ single jobs alone and the other $|J'| - a$ jobs on $m - a$ machines with at most two each, so $|J'| - a \le 2(m - a)$. This is a contradiction.

**Part 3 (sketch, cited).** Coffman, Garey and Johnson take a counterexample with the fewest jobs, in which first fit decreasing fails at capacity $r \cdot \mathrm{OPT}$. They show that its smallest job is the one that fails and that it is not too small, as in part 2, and then they give each job a weight that depends on its size and on its bin in the optimal schedule. A case analysis shows that the total weight of the bins of first fit decreasing is too large to fit the optimal schedule when $r = 1.22$. Friesen and Yue refine the weights and the cases; Yue's proof of $\frac{13}{11}$ is a long case analysis. This part is not proved here.

**Part 4.** Take $m = 13$ and the jobs: $40$ eight times, $25$ eight times, $24$ twice, $17$ twice, $16$ three times, and $13$ sixteen times. The total is $858 = 13 \cdot 66$. The triples $\{40, 13, 13\}$ eight times, $\{25, 25, 16\}$ three times and $\{25, 24, 17\}$ twice all have sum $66$, so $\mathrm{OPT} = 66$.

Let $66 \le C < 78$. First fit decreasing runs as follows.

- The eight jobs of $40$ open bins $1$ to $8$, since $80 > C$.
- Each job of $25$ joins one job of $40$, since $65 \le C$ and $90 > C$. Bins $1$ to $8$ have load $65$.
- The jobs of $24$ do not fit there, since $89 > C$, so they open bin $9$ with load $48$.
- The first job of $17$ goes to bin $9$, with load $65$. The second does not fit into any bin, since $82 > C$, and opens bin $10$.
- The three jobs of $16$ do not fit into bins $1$ to $9$, since $81 > C$, and join bin $10$, which reaches $17 + 48 = 65$.
- The jobs of $13$ do not fit into bins $1$ to $10$, since $78 > C$. They open new bins, and a bin holds at most $5$ of them, since $78 > C$. Sixteen jobs need $4$ bins.

So $14$ bins are needed, and $C$ fails. For $m > 13$, add $m - 13$ jobs of length $66$: they come first, each opens its own bin, and no other job fits with them, so the same run needs $m + 1$ bins, while the optimum stays $66$. Hence $r_m \ge \frac{78}{66} = \frac{13}{11}$.

MULTIFIT returns the bins of a capacity that succeeds. By the final loads fact, the largest load $M$ of these bins also succeeds, so $M \ge 78$. Hence $\mathrm{MF}_k \ge 78 = \frac{13}{11}\,\mathrm{OPT}$ for every $k$. At $C = 78$ the run is the same up to the jobs of $13$; then each of bins $1$ to $10$ takes one, and the last six fill bin $11$ to $78$, so $78$ succeeds.

**Part 5.** Take $m = 2$ and $p = (3, 3, 2, 2, 2, 2)$, with $\mathrm{OPT} = 7$, the sets $\{3, 2, 2\}$ twice. For $7 \le C < 8$, both jobs of $3$ go into bin $1$, the jobs of $2$ do not fit there, since $8 > C$, and bin $2$ holds at most three of them, since $8 > C$. A third bin is needed. So no capacity below $8$ succeeds, $r_2 \ge \frac87$, and MULTIFIT never returns less than $8$ on this instance. The matching bound $r_2 \le \frac87$ is cited from Coffman, Garey and Johnson. $\blacksquare$

## Consequences

- **A better constant than LPT.** For $k = 7$, $\frac{13}{11} + 2^{-7} < 1.19$, against $\frac43 - \frac1{3m}$ for [LPT](/longest-processing-time-first/). The cost is $k$ runs of first fit decreasing.
- **The analysis cannot be improved.** Part 4 shows that $\frac{13}{11}$ is not an artifact of the proof: the algorithm itself returns $\frac{13}{11}\,\mathrm{OPT}$ on that instance.
- **The search adds only $2^{-k}$.** The binary search does not need first fit decreasing to be monotone in the capacity, which it is not.
- **Small numbers of machines.** For small $m$ the threshold is smaller; Coffman, Garey and Johnson give $\frac87$ for $m = 2$, and the example of part 4 needs $13$ machines.

## Tightness

- **For the algorithm.** Part 4 gives $\mathrm{MF}_k \ge \frac{13}{11}\,\mathrm{OPT}$ for every $k$ when $m \ge 13$, and Yue's bound gives $\mathrm{MF}_k \le (\frac{13}{11} + 2^{-k})\,\mathrm{OPT}$. So the constant $\frac{13}{11}$ is tight.
- **For the problem.** $P \mid\mid C_{\max}$ has a [PTAS](/hochbaum-shmoys-ptas/), so $\frac{13}{11}$ is not a hardness threshold. With a different packing rule inside the search, Friesen and Langston (1986) proved $\frac{72}{61} + 2^{-k}$, with $\frac{72}{61} \approx 1.180$.

## History

Coffman, Garey and Johnson (1978) defined MULTIFIT, proved $r_m \le 1.22$, and found the exact value for a few small $m$. Friesen (1984) proved $1.2$ and gave the example that shows $r_m \ge \frac{13}{11}$ for $m \ge 13$. Yue (1990) proved $r_m \le \frac{13}{11}$, which closed the question with a long case analysis. Friesen and Langston (1986) studied a modified algorithm with $\frac{72}{61}$.

## References
