---
tag: D732GH
kind: problem
slug: precedence-constrained-scheduling
name: Precedence-constrained scheduling
aliases:
- DAG scheduling
- P|prec|Cmax
- Task graph scheduling
- precedence-constrained scheduling
- scheduling a task graph on processors
- scheduling with precedence constraints
- task graph scheduling
- P|prec,p_j=1|Cmax
area: approximation/scheduling-approximation
level: advanced
summary: Jobs form a precedence DAG; a job starts only after its predecessors finish.
prereqs: [scheduling-notation, makespan, directed-acyclic-graph, np-hard]
see_also: [critical-path-lower-bound, list-scheduling, list-scheduling-bound, hu-algorithm, coffman-graham-algorithm, graham-anomalies, makespan-minimization, unique-games-conjecture]
sources:
  - paper: doi:10.1002/j.1538-7305.1966.tb01709.x
    title: "R. L. Graham, Bounds for certain multiprocessing anomalies, Bell System Technical Journal 45(9), 1966"
    locator: the bound 2 - 1/m for list scheduling with precedence constraints
  - paper: doi:10.1287/opre.26.1.22
    title: "J. K. Lenstra and A. H. G. Rinnooy Kan, Complexity of scheduling under precedence constraints, Operations Research 26(1), 1978"
    locator: the NP-completeness of deciding makespan at most 3 for unit jobs, which rules out ratios below 4/3
  - paper: doi:10.1016/S0022-0000(75)80008-0
    title: "J. D. Ullman, NP-complete scheduling problems, Journal of Computer and System Sciences 10(3), 1975"
    locator: the NP-completeness of unit-time scheduling with precedence constraints
  - paper: "O. Svensson, Conditional hardness of precedence constrained scheduling on identical machines, Proceedings of the 42nd ACM Symposium on Theory of Computing (STOC), 2010"
    locator: no ratio 2 - epsilon under a variant of the unique games conjecture
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Appendix A5.2, problem SS9 (Precedence constrained scheduling) and the open problem for a fixed number of processors
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.3 (list scheduling with precedence constraints)
---

In precedence-constrained scheduling, written $P \mid \text{prec} \mid C_{\max}$ in [three-field notation](/scheduling-notation/), $n$ jobs with processing times $p_j$ run on $m$ identical machines, and a directed acyclic graph says which jobs must end before others start. The goal is the least [makespan](/makespan/). Graham's [list scheduling](/list-scheduling/) gives ratio $2 - 1/m$ against the [critical path lower bound](/critical-path-lower-bound/), and this is still the best known ratio for general times. The problem is NP-hard even for unit jobs, no ratio below $4/3$ is possible unless P = NP (Lenstra and Rinnooy Kan 1978), and no ratio $2 - \varepsilon$ is possible under a variant of the [unique games conjecture](/unique-games-conjecture/) (Svensson 2010).

## In plain words

A project has many tasks and a few equal workers. Some tasks can start only when certain other tasks are done: you pour the walls before you put on the roof. Each worker does one task at a time. You want the whole project done as early as possible.

The simple rule is: whenever a worker is free, give them any task whose earlier tasks are all done. This is never worse than about twice the best plan. Better guarantees exist only in special cases, for example when all tasks take the same time and there are two workers, or when the task structure is a tree. In general, finding the best plan is hard, and a rule that is much better than twice the best may not exist.

## Definition

**Input.** An integer $m \ge 1$, $n$ jobs with processing times $p_j \ge 0$, and a directed acyclic graph $G$ on the jobs. An arc $i \to j$, also written $i \prec j$, means that job $j$ starts only after job $i$ ends.

**Output.** A start time $S_j \ge 0$ and a machine for each job, such that the jobs on one machine do not overlap, and $S_j \ge S_i + p_i$ for every arc $i \to j$.

**Goal.** Minimize $C_{\max} = \max_j (S_j + p_j)$. The least value is $\mathrm{OPT}$, and $\mathrm{ALG}$ is the makespan that an algorithm returns. With $m$ identical machines, a set of start times is feasible if and only if at most $m$ jobs run at each moment, so the machines can be assigned afterwards.

**Unit jobs.** The case $p_j = 1$ for all $j$ is written $P \mid \text{prec}, p_j = 1 \mid C_{\max}$. A schedule is then a slot $\sigma(j) \in \{1, 2, \ldots\}$ for each job, with at most $m$ jobs in each slot and $\sigma(i) < \sigma(j)$ for each arc.

*Ratio convention.* This is a minimization problem, and a ratio $\rho \ge 1$ means $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. All ratios on this page are absolute and worst case. $L$ is the length of a longest chain, and $P = \sum_j p_j$.

## Variants

- **Unit jobs, two machines, $P2 \mid \text{prec}, p_j = 1 \mid C_{\max}$.** Solvable in polynomial time, by matching (Fujii, Kasami and Ninomiya 1969) or by the [Coffman-Graham algorithm](/coffman-graham-algorithm/) (1972).
- **Unit jobs, trees, $P \mid \text{intree}, p_j = 1 \mid C_{\max}$.** Solvable for every $m$ by [Hu's algorithm](/hu-algorithm/) (1961). Out-trees reduce to in-trees by reversing time.
- **Unit jobs, a fixed number $m \ge 3$ of machines.** The complexity of $P3 \mid \text{prec}, p_j = 1 \mid C_{\max}$ is open; it is one of the open problems listed by Garey and Johnson.
- **Preemption, $P \mid \text{prec}, \text{pmtn} \mid C_{\max}$.** Jobs can be split. This is NP-hard as well (Ullman 1976), while it is polynomial for trees and for two machines.
- **Uniform machines, $Q \mid \text{prec} \mid C_{\max}$.** Machines have speeds. List scheduling has no constant ratio here. Chudak and Shmoys (1999) gave an $O(\log m)$-approximation, and later work improved it to $O(\log m / \log \log m)$.
- **Other objectives.** For the sum of weighted completion times, $1 \mid \text{prec} \mid \sum w_j C_j$ already has 2-approximations and a matching conditional hardness; see [weighted completion time scheduling](/weighted-completion-time-scheduling/).
- **No precedence.** With an empty graph the problem is [makespan minimization](/makespan-minimization/), $P \mid\mid C_{\max}$, which is strongly NP-hard and has a PTAS.

## Examples

**A list schedule that is late.** Take $m = 2$ and six unit jobs with arcs $0 \to 5$, $1 \to 3$, $2 \to 3$, $2 \to 4$ and $2 \to 5$. The list $0, 1, 2, 3, 4, 5$ runs $\{0, 1\}$, then $\{2\}$ alone (no other job is ready), then $\{3, 4\}$, then $\{5\}$: makespan 4. The schedule $\{1, 2\}, \{0, 4\}, \{3, 5\}$ has makespan 3, which is optimal since 6 jobs need 3 slots. The [Coffman-Graham algorithm](/coffman-graham-algorithm/) finds it.

**When the two lower bounds are not enough.** Take $m = 2$ and jobs $a, b, c, d, e$ with lengths $3, 2, 2, 1, 4$, arcs $a \to b$, $a \to c$, $b \to d$ and $c \to d$, and $e$ free. Then $L = 6$ and $P/m = 6$, but $\mathrm{OPT} = 7$, because $e$ does not fit in the gaps of any schedule of length 6. See the [critical path lower bound](/critical-path-lower-bound/).

## Known algorithms

| algorithm | problem | ratio $\rho$ | tight | time |
|---|---|---|---|---|
| [list scheduling](/list-scheduling/), any order | $P \mid \text{prec} \mid C_{\max}$ | $2 - 1/m$ | yes, for the algorithm | $O(n \log n + e)$ |
| [Coffman-Graham](/coffman-graham-algorithm/) | $P \mid \text{prec}, p_j = 1 \mid C_{\max}$ | $2 - 2/m$, and exact for $m = 2$ | yes, for the algorithm (Lam and Sethi) | $O(n (n + e))$ |
| [Hu's algorithm](/hu-algorithm/) | $P \mid \text{intree}, p_j = 1 \mid C_{\max}$ | exact | not applicable | $O(n \log n)$ |
| Gangal and Ranade (2008) | $P \mid \text{prec}, p_j = 1 \mid C_{\max}$ | $2 - 7/(3m + 1)$ | not known | polynomial |

Here $e$ is the number of arcs. **List scheduling** starts, at each moment when a machine is free, an available job, which means a job whose predecessors have all ended. Graham (1966) proved $\mathrm{ALG} \le P/m + (1 - 1/m) L$. Since $P/m \le \mathrm{OPT}$ and $L \le \mathrm{OPT}$, this gives $\mathrm{ALG} \le (2 - 1/m)\,\mathrm{OPT}$; the proof is on the page of the [critical path lower bound](/critical-path-lower-bound/). The ratio is tight for the algorithm already without arcs (see [Graham's bound](/list-scheduling-bound/)), and the analysis compares with $\max(L, P/m)$, which can itself be off by a factor near 2. List scheduling has strange effects with precedence constraints: shorter jobs or more machines can make the schedule longer; see [Graham anomalies](/graham-anomalies/).

For unit jobs and a fixed $m$, Levey and Rothvoss (2016) gave a $(1 + \varepsilon)$-approximation that runs in slightly more than quasi-polynomial time, and Garg (2018) brought the time down to quasi-polynomial.

## Bounds

- **Lower bounds on OPT.** $\mathrm{OPT} \ge \max(L, P/m)$ by the [critical path lower bound](/critical-path-lower-bound/), and for unit jobs $\mathrm{OPT} \ge \max_h \big(h - 1 + \lceil N(h)/m \rceil\big)$, where $N(h)$ counts the jobs that start a chain of at least $h$ jobs.
- **NP-hardness.** $P \mid \text{prec}, p_j = 1 \mid C_{\max}$ is NP-hard when $m$ is part of the input (Ullman 1975). It is in Garey and Johnson as problem SS9. With general times, the case without arcs already contains 3-partition, so the problem is strongly NP-hard.
- **No ratio below $4/3$.** Deciding whether $\mathrm{OPT} \le 3$ for unit jobs is NP-complete (Lenstra and Rinnooy Kan 1978), and $\mathrm{OPT}$ is an integer. A polynomial algorithm with ratio $\rho < 4/3$ would return a makespan below 4, so at most 3, whenever $\mathrm{OPT} = 3$, and so would decide the question. The reduction is below.
- **No ratio $2 - \varepsilon$ under a conjecture.** Svensson (2010) showed that, for every $\varepsilon > 0$, a $(2 - \varepsilon)$-approximation for $P \mid \text{prec} \mid C_{\max}$ would refute a variant of the [unique games conjecture](/unique-games-conjecture/) introduced by Bansal and Khot. So, under this conjecture, list scheduling is essentially best possible, and the threshold for the problem is $2$.
- **The gap between the bounds.** Unconditionally, the best known ratio is $2 - 1/m$ for general times (and slightly better for unit jobs), and the best known hardness is $4/3$.

## Reductions

**From clique: makespan 3 is NP-hard to decide.** This is the idea of Lenstra and Rinnooy Kan. Take a graph with $n_V$ vertices and $n_E$ edges and an integer $k$, and let $l = k(k-1)/2$. The question is whether the graph has a clique of $k$ vertices. Build unit jobs on $m = \max(k,\ l + n_V - k,\ n_E - l) + 1$ machines.

- One job for each vertex and one job for each edge, with an arc from each vertex to each edge that contains it.
- Three sets of filler jobs $X$, $Y$, $Z$ with $|X| = m - k$, $|Y| = m - l - n_V + k$ and $|Z| = m - n_E + l$, all nonempty by the choice of $m$, and an arc from each job of $X$ to each job of $Y$ and from each job of $Y$ to each job of $Z$.

The filler chains have 3 jobs, so $\mathrm{OPT} \ge 3$, and a schedule of makespan 3 must put $X$, $Y$, $Z$ in slots 1, 2, 3. The free places are then $k$, $l + n_V - k$ and $n_E - l$, in total $n_V + n_E$, which is the number of graph jobs. So every slot is full.

- If a clique $K$ of size $k$ exists, put $K$ in slot 1, the other vertices and the $l$ edges inside $K$ in slot 2, and the other edges in slot 3. Every edge comes after its two ends, so the makespan is 3.
- If the makespan is 3, slot 1 holds $k$ vertex jobs, because an edge job has predecessors. Slot 2 holds $l + n_V - k$ jobs, each a vertex outside slot 1 or an edge with both ends in slot 1. There are only $n_V - k$ such vertices, so slot 2 holds at least $l$ edges with both ends among the $k$ vertices of slot 1. A set of $k$ vertices spans at most $l$ edges, so it spans exactly $l$, and it is a clique.

The construction is polynomial, so deciding $\mathrm{OPT} \le 3$ is NP-hard, which gives the $4/3$ bound above.

**Special cases.** $P \mid\mid C_{\max}$ is the case of an empty graph, so all hardness of [makespan minimization](/makespan-minimization/) carries over. The single machine case $1 \mid \text{prec} \mid C_{\max}$ is trivial: any [topological order](/topological-sort/) gives makespan $P$.

## Applications

- Scheduling the tasks of a parallel program, given as a task graph, on the cores of a processor.
- Build systems and workflow engines that run steps on a pool of workers once their inputs are ready.
- Project planning with limited crews, where the [critical path method](/critical-path-method/) gives the bound for unlimited crews.
- Instruction scheduling in compilers, where the operations of a basic block form a DAG and the functional units are the machines.

## References
