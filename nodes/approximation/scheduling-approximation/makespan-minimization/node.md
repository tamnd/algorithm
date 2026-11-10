---
tag: 5MX7DT
kind: problem
slug: makespan-minimization
name: Makespan minimization on identical machines
aliases:
- P||Cmax
- multiprocessor scheduling
- identical-machine scheduling
- load balancing on identical machines
area: approximation/scheduling-approximation
level: core
summary: Assign jobs to m identical machines to minimize the makespan.
prereqs: [makespan, scheduling-notation, np-hard, three-partition]
see_also: [makespan-lower-bounds, list-scheduling, longest-processing-time-first, multifit-algorithm, hochbaum-shmoys-ptas, preemptive-makespan-scheduling, machine-covering, bin-packing]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Appendix A5.2, problem SS8 (Multiprocessor scheduling); Section 4.2 (strong NP-completeness and 3-partition)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.3 (list scheduling and the LPT rule) and Section 3.2 (the polynomial-time approximation scheme)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 10 (Minimum makespan scheduling)
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 1, L. A. Hall, Approximation algorithms for scheduling (identical parallel machines)
  - paper: "D. S. Hochbaum and D. B. Shmoys, Using dual approximation algorithms for scheduling problems: theoretical and practical results, Journal of the ACM 34(1), 1987"
    title: Hochbaum and Shmoys 1987
    locator: the polynomial-time approximation scheme for identical machines
---

Makespan minimization on identical machines, written $P \mid\mid C_{\max}$, asks to assign $n$ jobs with processing times $p_j$ to $m$ identical machines so that the largest machine load, the [makespan](/makespan/), is as small as possible. It is the basic problem of approximation for scheduling: it is strongly NP-hard, the simple greedy rules [list scheduling](/list-scheduling/) and [LPT](/longest-processing-time-first/) have ratios $2 - 1/m$ and $4/3 - 1/(3m)$, and it has a [PTAS](/hochbaum-shmoys-ptas/) but no FPTAS unless P = NP. The same problem, read as a decision question, is [bin packing](/bin-packing/) with a fixed number of bins.

## In plain words

You have a set of tasks and a team of equal workers. Each task has a length, and one worker must do it from start to end. You want to give the tasks out so that the whole team is done as soon as possible, which means the worker with the most work should have as little as possible.

With two workers this is the old puzzle of splitting a pile of numbers into two halves of equal sum, and with many workers it is harder. No fast method is known that always finds the best plan. But simple rules come close: give each task to the worker who is free first, and do the long tasks first. The rules never end much later than the best plan.

## Definition

**Input.** An integer $m \ge 1$, the number of machines, and $n$ jobs with processing times $p_1, \ldots, p_n \ge 0$. Here $n$ is the number of jobs and $m$ is the number of machines, and both are part of the input.

**Output.** An assignment $\sigma : \{1, \ldots, n\} \to \{1, \ldots, m\}$. Machine $i$ has the load $L_i = \sum_{j : \sigma(j) = i} p_j$, and it runs its jobs one after another from time $0$, so job $j$ ends at a completion time $C_j \le L_{\sigma(j)}$.

**Goal.** Minimize $C_{\max} = \max_i L_i$. The least value is $\mathrm{OPT}$, and $\mathrm{ALG}$ is the makespan that an algorithm returns.

**Decision version.** Given also a bound $T$, is there an assignment with $C_{\max} \le T$? This is the same as asking whether the numbers $p_j$ fit into $m$ bins of capacity $T$.

*Ratio convention.* This is a minimization problem. An algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ for every instance. All ratios on this page are absolute, with no additive term, and are worst case.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of jobs and the number of machines |
| $p_j$ | the processing time of job $j$ |
| $C_j$, $C_{\max}$ | the completion time of job $j$, and $\max_j C_j$ |
| $L_i$ | the load of machine $i$ |
| $\mathrm{OPT}$, $\mathrm{ALG}$ | the optimal makespan, and the makespan of the algorithm |
| $\rho$, $\varepsilon$ | an approximation ratio, and the accuracy of a scheme |

## Variants

- **Fixed number of machines, $Pm \mid\mid C_{\max}$.** If $m$ is a constant, the problem is NP-hard only in the ordinary sense. A dynamic program over the loads solves it in pseudo-polynomial time, and Sahni (1976) gave an [FPTAS](/fptas/).
- **Preemption, $P \mid \mathrm{pmtn} \mid C_{\max}$.** Jobs can be split. The optimum is $\max(\frac1m \sum_j p_j, \max_j p_j)$, and [McNaughton's wrap-around rule](/mcnaughton-wrap-around/) builds it in $O(n)$ time. See [preemptive makespan scheduling](/preemptive-makespan-scheduling/).
- **Uniform and unrelated machines, $Q \mid\mid C_{\max}$ and $R \mid\mid C_{\max}$.** The machines have speeds, or the times depend on the machine. See [uniform machine scheduling](/uniform-machine-scheduling/) and [unrelated machine scheduling](/unrelated-machine-scheduling/); the second has the [2-approximation of Lenstra, Shmoys and Tardos](/lenstra-shmoys-tardos/).
- **Precedence constraints, $P \mid \mathrm{prec} \mid C_{\max}$.** A job starts after its predecessors end. List scheduling still gives $2 - 1/m$; see [precedence-constrained scheduling](/precedence-constrained-scheduling/).
- **Online.** The jobs arrive one by one and must be assigned at once. List scheduling is $(2 - 1/m)$-competitive; see [online makespan minimization](/online-makespan-minimization/).
- **Machine covering, $P \mid\mid C_{\min}$.** Maximize the smallest load instead. See [machine covering](/machine-covering/).

## Examples

**A small instance.** Take $m = 3$ and $p = (2, 3, 4, 6, 2, 2)$, with total $19$. The lower bound $\lceil 19/3 \rceil = 7$ is met by the machines $\{6\}$, $\{4, 3\}$ and $\{2, 2, 2\}$, so $\mathrm{OPT} = 7$. [List scheduling](/list-scheduling/) in the given order puts $2, 3, 4$ on the three machines, then $6$ on the machine with load $2$, and ends with makespan $8$. [LPT](/longest-processing-time-first/) takes the order $6, 4, 3, 2, 2, 2$ and gets the loads $6, 6, 7$, which is optimal.

**Where LPT is not optimal.** Take $m = 2$ and $p = (3, 3, 2, 2, 2)$. The optimum is $6$, with $\{3, 3\}$ and $\{2, 2, 2\}$. LPT puts the two jobs of length $3$ on different machines, and then the three jobs of length $2$ make one machine reach $3 + 2 + 2 = 7$. The ratio is $7/6 = 4/3 - 1/6$, which is the [LPT bound](/lpt-bound/) for $m = 2$.

**Two machines as partition.** With $m = 2$ and integer times, $\mathrm{OPT} = \frac12 \sum_j p_j$ if and only if the times can be split into two sets of equal sum. For $p = (6, 4, 3, 3)$ the total is $16$, no subset sums to $8$, and the optimum is $9$.

## Known algorithms

| algorithm | ratio $\rho$ | tight for the algorithm | time |
|---|---|---|---|
| [list scheduling](/list-scheduling/), any order | $2 - 1/m$ | yes; [Graham's bound](/list-scheduling-bound/) | $O(n \log m)$, online |
| [LPT](/longest-processing-time-first/) | $4/3 - 1/(3m)$ | yes; [LPT bound](/lpt-bound/) | $O(n \log n)$ |
| [Sorted-Balance](/sorted-balance/) | $3/2 - 1/(2m)$ by a short proof | no; it is LPT, so $4/3 - 1/(3m)$ holds | $O(n \log n + nm)$ |
| [MULTIFIT](/multifit-algorithm/), $k$ rounds | $13/11 + 2^{-k}$ | $13/11$ is tight; [MULTIFIT bound](/multifit-bound/) | $O(n \log n + k n \log m)$ |
| [Hochbaum-Shmoys PTAS](/hochbaum-shmoys-ptas/) | $1 + \varepsilon$ | not applicable | $n^{O(1/\varepsilon^2)}$ |
| EPTAS (Alon, Azar, Woeginger and Yadid 1998) | $1 + \varepsilon$ | not applicable | $f(1/\varepsilon) + O(n)$ |
| dynamic program over loads, fixed $m$ | exact | not applicable | $O(n \cdot P^{m-1})$ with $P = \sum_j p_j$ |
| Sahni 1976, fixed $m$ | $1 + \varepsilon$ (FPTAS) | not applicable | polynomial in $n$ and $1/\varepsilon$ for fixed $m$ |

The approximation schemes rely on [dual approximation](/dual-approximation/): for a guess $T$ of the optimum, either find a schedule of makespan at most $(1 + \varepsilon) T$ or prove that $\mathrm{OPT} > T$, and do a binary search over $T$. The page [Hochbaum-Shmoys makespan PTAS](/hochbaum-shmoys-makespan-ptas/) gives the details.

## Bounds

- **Lower bounds on OPT.** $\mathrm{OPT} \ge \frac1m \sum_j p_j$, $\mathrm{OPT} \ge \max_j p_j$, and $\mathrm{OPT} \ge p_m + p_{m+1}$ for times sorted in decreasing order. These are proved on [makespan lower bounds](/makespan-lower-bounds/), and every analysis in the table compares with them.
- **Strong NP-hardness.** The decision version is strongly NP-complete when $m$ is part of the input (Garey and Johnson, problem SS8). The proof is in the next section.
- **No FPTAS, no pseudo-polynomial algorithm.** Because of strong NP-hardness, there is no pseudo-polynomial exact algorithm and no FPTAS unless P = NP. With integer times, $\mathrm{OPT} \le \sum_j p_j$, so an FPTAS run with $\varepsilon = 1/(\sum_j p_j + 1)$ would be an exact pseudo-polynomial algorithm; see [no FPTAS for strongly NP-hard problems](/no-fptas-for-strongly-np-hard-problems/).
- **Tight for the problem.** Since a PTAS exists, no constant $\rho > 1$ is a hardness threshold, and the problem is not APX-hard. The best possible polynomial guarantee is $1 + \varepsilon$ for each fixed $\varepsilon > 0$, unless P = NP. Under the exponential time hypothesis, Chen, Jansen and Zhang (2014) showed that the running time of a scheme must grow at least like $2^{(1/\varepsilon)^{1 - \delta}}$ for each $\delta > 0$.
- **Two machines.** $P2 \mid\mid C_{\max}$ is NP-hard because it contains [partition](/partition-problem/), but it is not strongly NP-hard, since the dynamic program runs in time $O(n \sum_j p_j)$.
- **Harder environments.** For unrelated machines no ratio below $3/2$ is possible unless P = NP; see [scheduling makespan inapproximability](/scheduling-makespan-inapproximability/).

## Reductions

**From 3-partition (strong NP-hardness).** An instance of [3-partition](/three-partition/) is a bound $B$ and $3q$ positive integers $a_1, \ldots, a_{3q}$ with $\sum_j a_j = qB$ and $B/4 < a_j < B/2$. The question is whether they split into $q$ triples, each of sum $B$. Build the scheduling instance with $m = q$ machines, one job of time $p_j = a_j$ for each number, and the bound $T = B$.

- If a 3-partition exists, put each triple on one machine. Each load is $B$, so $C_{\max} = B$.
- If $C_{\max} \le B$, then the loads add up to $qB$ and none is above $B$, so each load is exactly $B$. Since each $a_j$ is strictly between $B/4$ and $B/2$, a load of $B$ has exactly three jobs, and the machines give a 3-partition.

The reduction takes linear time and keeps the numbers unchanged. Since 3-partition is NP-complete even when the numbers are bounded by a polynomial in $q$ ([strong NP-hardness](/strong-np-hardness/)), so is $P \mid\mid C_{\max}$.

**From partition ($m = 2$).** An instance $a_1, \ldots, a_n$ of [partition](/partition-problem/) with even total $2S$ has a solution if and only if two machines reach $C_{\max} \le S$. This shows that $P2 \mid\mid C_{\max}$ is NP-hard, in the weak sense only.

**To and from bin packing.** "Is $\mathrm{OPT} \le T$?" is the same as "do the items $p_j / T$ fit into $m$ unit bins?" So a bin packing heuristic tested at several capacities is a scheduling algorithm. [MULTIFIT](/multifit-algorithm/) uses [first fit decreasing](/first-fit-decreasing/) in this way, and the Hochbaum-Shmoys scheme uses an exact packing of the large jobs.

**Special case of more general problems.** $P \mid\mid C_{\max}$ is the case $s_i = 1$ of $Q \mid\mid C_{\max}$, the case $p_{ij} = p_j$ of $R \mid\mid C_{\max}$, and the case of an empty graph in $P \mid \mathrm{prec} \mid C_{\max}$. Its hardness carries over to all of them.

## Applications

- Load balancing of independent tasks on the cores of a processor or the servers of a cluster.
- Splitting a batch of print, render or test jobs among equal workers so that the batch ends early.
- Assigning work to identical production lines in a factory.
- A subproblem inside the approximation of shop scheduling and of scheduling with precedence constraints.

## References
