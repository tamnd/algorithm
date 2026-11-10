---
tag: 0P56MZ
kind: algorithm
slug: lenstra-shmoys-tardos
name: Lenstra-Shmoys-Tardos rounding
aliases:
- 2-approximation for R||Cmax
- LP rounding for unrelated machines
- LST 2-approximation
- LST rounding
- Lenstra-Shmoys-Tardos rounding algorithm
- LST algorithm
area: approximation/scheduling-approximation
level: advanced
summary: Parametric LP with rounding on a bipartite pseudoforest, giving a 2-approximation for makespan on unrelated machines.
solves: [unrelated-machine-scheduling, unrelated-machine-scheduling-makespan]
model: word-ram
complexity:
  vars: {n: the number of jobs, m: the number of machines, P: the largest finite processing time, L: the time to find a vertex of a linear program with n m variables and n + m constraints}
  time: {worst: O(L log(n P) + n m)}
  space: {extra: O(n m)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1990
  people: [Jan Karel Lenstra, David B. Shmoys, Éva Tardos]
  note: The conference version appeared at FOCS 1987, and the journal paper in Mathematical Programming in 1990, with the 2-approximation and the 3/2 hardness bound.
prereqs: [unrelated-machine-scheduling, linear-programming-problem, basic-feasible-solution, lp-relaxation, bipartite-matching]
see_also: [unrelated-machine-scheduling-makespan, unrelated-makespan-inapproximability, shmoys-tardos-gap, generalized-assignment-problem, restricted-assignment-scheduling, dual-approximation, extreme-point, iterative-rounding]
sources:
  - paper: doi:10.1007/BF01585745
    title: "J. K. Lenstra, D. B. Shmoys and É. Tardos, Approximation algorithms for scheduling unrelated parallel machines, Mathematical Programming 46, 1990"
    locator: the parametric linear program, the rounding of a vertex solution, the 2-approximation, and the 3/2 hardness bound
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 11.1 (the generalized assignment problem, which contains this rounding as the case without costs)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 17 (Scheduling on unrelated parallel machines)
  - paper: "C. N. Potts, Analysis of a linear programming heuristic for scheduling unrelated parallel machines, Discrete Applied Mathematics 10, 1985"
    locator: the earlier LP based 2-approximation, with running time exponential in m
  - paper: "E. V. Shchepin and N. Vakhania, An optimal rounding gives a better approximation for scheduling unrelated machines, Operations Research Letters 33(2), 2005"
    locator: the improved ratio 2 - 1/m by a finer rounding of the same linear program
---

The Lenstra-Shmoys-Tardos algorithm is a 2-approximation for makespan on unrelated machines, $R \mid\mid C_{\max}$, where job $j$ takes time $p_{ij}$ on machine $i$. It guesses a bound $T$, writes a linear program that allows job $j$ on machine $i$ only if $p_{ij} \le T$, and takes the least $T$ for which the program has a solution. A vertex of this program has a very sparse support: as a bipartite graph between jobs and machines, each connected component has at most one cycle. Each job that the vertex splits can then get its own machine by a matching, so each machine gets at most one extra job, of time at most $T$, and the makespan is at most $2T \le 2\,\mathrm{OPT}$. The same paper proved that no ratio below $3/2$ is possible unless P = NP.

## In plain words

Some tasks must go to a few workers, but the workers are all different: a task can be quick for one worker and slow for another, or impossible. You want the last worker to finish early.

First guess a finishing time and solve an easier version where a task may be split among several workers in pieces. Never let a worker take a piece of a task that alone would take them longer than the guess. Find the smallest guess for which the split version works. A good split solution splits only a few tasks, and they can be given out so that each worker gets at most one of them in full. Each worker then finishes within twice the guess, and the best plan cannot beat the guess.

## The problem

There are $n$ jobs and $m$ machines. Job $j$ takes $p_{ij} \in \{1, 2, \ldots\} \cup \{\infty\}$ time units on machine $i$, where $\infty$ means that $j$ cannot run on $i$. A schedule is an assignment $\sigma$ of each job to a machine; the load of machine $i$ is $\sum_{j : \sigma(j) = i} p_{ij}$, and the makespan is the largest load. $\mathrm{OPT}$ is the least makespan and $\mathrm{ALG}$ the makespan of the algorithm. See [unrelated machine scheduling](/unrelated-machine-scheduling/) for the problem and its variants.

For a number $T$, let $S_T = \{(i, j) : p_{ij} \le T\}$. The program $\mathrm{LP}(T)$ has a variable $x_{ij}$ for each pair in $S_T$:

$$\sum_{i : (i,j) \in S_T} x_{ij} = 1 \ \text{for each job } j, \qquad \sum_{j : (i,j) \in S_T} p_{ij} x_{ij} \le T \ \text{for each machine } i, \qquad x \ge 0.$$

There is no objective; the question is only whether a solution exists. The value $x_{ij}$ is the fraction of job $j$ that machine $i$ does.

## The algorithm

```pseudo id=main
LST(p)                                ▷ p[i][j] is the time of job j on machine i, or ∞
L1  T ← the least integer such that LP(T) has a solution     ▷ binary search
L2  x ← a vertex of the polytope LP(T)
L3  σ(j) ← i for each job j with x_ij = 1
L4  H ← the bipartite graph on the machines and the other jobs, with the edges where 0 < x_ij < 1
L5  while H has a job do
L6      if some machine i has degree 1 in H then
L7          j ← the job next to i; σ(j) ← i; delete i and j from H
L8      else take a job j of H; it lies on a cycle of H
L9          i ← one of the two machines next to j; σ(j) ← i; delete i and j from H
L10 return σ
```

Line L1 is a [dual approximation](/dual-approximation/) step. If $\mathrm{LP}(T)$ has a solution, so does $\mathrm{LP}(T')$ for each $T' > T$, so a binary search works. It runs between $\max_j \min_i p_{ij}$ and $\sum_j \min_i p_{ij}$, where the second value is feasible because it admits the schedule that puts each job on its fastest machine. Line L2 needs a vertex, also called a [basic feasible solution](/basic-feasible-solution/); the [simplex method](/simplex-method/) returns one, and a solution from the [ellipsoid method](/ellipsoid-method/) or an [interior point method](/interior-point-method/) can be moved to a vertex in polynomial time. Lines L4 to L9 compute a matching in $H$ that covers all its jobs. At line L8 there is no machine of degree 1, and the proof shows that then each part of $H$ that still has a job is a cycle.

## Example

Take $m = 3$ machines and $4$ jobs. Job 0 takes time 3 on every machine, and job $k \in \{1, 2, 3\}$ takes time 2 on machine $k - 1$ and cannot run elsewhere.

- For $T \le 2$, job 0 has no allowed machine, so $\mathrm{LP}(T)$ has no solution. For $T = 3$, machine $i$ has load $2 + 3 x_{i0} \le 3$, so $x_{i0} \le 1/3$, and the sum is 1 only if $x_{i0} = 1/3$ for all three machines. So $T = 3$, and $x$ is this unique solution, which is a vertex.
- Line L3 puts each private job on its machine. The graph $H$ is a star: job 0 with the three machines. Every machine has degree 1, so line L7 gives job 0 to machine 0.
- The loads are $5, 2, 2$. The optimum is also 5, because job 0 must share a machine with a private job. So $\mathrm{ALG} = 5 \le 2T = 6$.

The same instance with $m$ machines, job 0 of time $m$ and private jobs of time $m - 1$, has $T = m$ and $\mathrm{OPT} = 2m - 1$. So $\mathrm{OPT}/T$ tends to 2: the bound $T \le \mathrm{OPT}$ cannot prove a ratio below 2, and the analysis is tight for this lower bound.

## Correctness

The proof has four steps. The full proof is in the proofs section.

1. **The guess is a lower bound.** An optimal schedule uses only pairs with $p_{ij} \le \mathrm{OPT}$, and as a 0-1 vector it is a solution of $\mathrm{LP}(\mathrm{OPT})$. $\mathrm{OPT}$ is an integer, so the least integer $T$ in line L1 satisfies $T \le \mathrm{OPT}$.
2. **A vertex has a sparse support.** A vertex of $\mathrm{LP}(T)$ satisfies at least as many independent constraints with equality as there are variables, and only $n + m$ constraints are not of the form $x_{ij} \ge 0$, so at most $n + m$ entries are positive. The same count, applied to each connected component of the support graph, shows that each component has at most as many edges as vertices. Such a graph is a *pseudoforest*: each component has at most one cycle.
3. **The fractional jobs have a matching.** In $H$ each job has at least two edges, because its values sum to 1 and none is 1. In a pseudoforest where each job has degree at least 2, every leaf is a machine, and a component with no leaf is an even cycle. Lines L5 to L9 peel the leaves and break the cycles, and they give each job of $H$ its own machine, joined to it by an edge of $H$.
4. **The loads.** On machine $i$, the jobs from line L3 have total time $\sum_{j : x_{ij} = 1} p_{ij} \le \sum_j p_{ij} x_{ij} \le T$. Lines L7 and L9 add at most one job, along an edge of $S_T$, so of time at most $T$. Hence $\mathrm{ALG} \le 2T \le 2\,\mathrm{OPT}$.

## Complexity

- Line L1 solves $O(\log (n p_{\max}))$ linear programs, one for each step of the binary search, each with at most $nm$ variables and $n + m$ constraints other than $x \ge 0$. With the ellipsoid method or an interior point method, each takes time polynomial in $n$, $m$ and $\log p_{\max}$.
- Line L2 is one more of these programs, or the last one of the search.
- Lines L3 to L9 take $O(nm)$ time: $H$ has at most $n + m$ edges, and each pass of the loop deletes a job.
- The extra space is $O(nm)$ for the program.

The reference implementation uses an exact simplex method with rational numbers, which is fine for small instances but not polynomial in the worst case.

## Properties

- **Ratio 2, absolute.** $\mathrm{ALG} \le 2\,\mathrm{OPT}$ on every instance, measured against the lower bound $T \le \mathrm{OPT}$. A finer statement is $\mathrm{ALG} \le T + \max\{p_{ij} : 0 < x_{ij} < 1\}$.
- **Tight for this lower bound.** The example shows $\mathrm{OPT}/T \to 2$, so no rounding of the same program can prove a ratio below 2 against $T$. Shchepin and Vakhania (2005) showed that a finer rounding of the same program reaches $2 - 1/m$, which matches the gap of the example.
- **Not tight for the problem.** The best lower bound for the problem is $3/2$: no polynomial algorithm has ratio below $3/2$ unless P = NP, by a reduction from three-dimensional matching. See [the 3/2 hardness for unrelated machines](/unrelated-makespan-inapproximability/).
- **Deterministic and offline.** The algorithm needs all jobs and times in advance.
- **The pruning is needed.** Without the rule $x_{ij} = 0$ for $p_{ij} > T$, the program can be far from $\mathrm{OPT}$: one job of time $m$ on each of $m$ machines has a fractional solution of makespan 1, while $\mathrm{OPT} = m$.

## Variants and improvements

- **Costs, the generalized assignment problem.** Shmoys and Tardos (1993) add a cost $c_{ij}$ for each pair and keep the cost at most the LP cost with the same makespan bound. See [the Shmoys-Tardos algorithm](/shmoys-tardos-gap/) and the [generalized assignment problem](/generalized-assignment-problem/).
- **Fixed $m$.** For a constant number of machines, $Rm \mid\mid C_{\max}$ has a PTAS, and Horowitz and Sahni (1976) gave an FPTAS. The 1990 paper also gives a PTAS for fixed $m$ that uses the same linear program, with a running time polynomial in the number of jobs.
- **Restricted assignment.** If $p_{ij} \in \{p_j, \infty\}$, the problem is [scheduling with eligibility restrictions](/restricted-assignment-scheduling/). The same rounding gives 2, and better *estimates* of $\mathrm{OPT}$ are known: Svensson (2012) showed that the [configuration LP](/configuration-lp/) estimates the optimum within a factor $33/17$, with later improvements.
- **Graph balancing.** If each job can run on at most two machines, with the same time on both, Ebenlendr, Krčál and Sgall (2008) gave a $1.75$-approximation.
- **Iterative rounding.** The same pseudoforest structure can be found by [iterative rounding](/iterative-rounding/): solve, fix the integral values, drop a machine constraint that can no longer be violated by much, and repeat.

## When to use it

Use this algorithm when machines differ in arbitrary ways, for example when some jobs run only on some machines, or when each machine is fast for some kinds of jobs and slow for others. It needs a linear program solver. For identical machines, list scheduling, LPT or the [Hochbaum-Shmoys PTAS](/hochbaum-shmoys-ptas/) are simpler and better. For uniform machines (speeds only), the guarantee of LPT and the PTAS for [uniform machines](/uniform-machine-scheduling/) are also better.

## Pitfalls

- **Rounding a non-vertex solution.** An arbitrary solution of $\mathrm{LP}(T)$ can split every job, and then the matching step fails. The support of the solution must be a pseudoforest, which a vertex guarantees.
- **Forgetting the pruning by $T$.** The constraint that $x_{ij} = 0$ when $p_{ij} > T$ is what bounds the extra job on each machine. A plain LP with makespan as the objective has an unbounded gap.
- **A real-valued search.** With integer times, the search can be over integers, because $\mathrm{OPT}$ is an integer. With rational times, search over a finite list of candidate values or stop the search when the interval is small.
- **Rounding errors.** The matching depends on which values are exactly 0 or 1. A floating point solver can report $10^{-12}$ instead of 0. Use exact arithmetic or clean the solution to a vertex first.

## Implementations

## History

Potts (1985) gave an LP based 2-approximation for $R \mid\mid C_{\max}$ whose running time is exponential in $m$. Lenstra, Shmoys and Tardos presented their algorithm at FOCS 1987 and published it in Mathematical Programming in 1990. The paper has three results: a PTAS for a fixed number of machines, the 2-approximation for $m$ in the input, and the proof that no ratio below $3/2$ is possible unless P = NP. Shmoys and Tardos (1993) extended the rounding to the generalized assignment problem. The gap between 2 and $3/2$ has stayed open for general unrelated machines, and Shchepin and Vakhania (2005) improved the ratio only to $2 - 1/m$.

## References
