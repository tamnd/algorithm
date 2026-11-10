---
tag: AR3HAW
kind: problem
slug: unrelated-machine-scheduling-makespan
name: Unrelated machine scheduling (makespan)
aliases:
- R||Cmax
- makespan on unrelated machines, LP view
- LP(T) for unrelated machines
area: approximation/lp-rounding
level: advanced
summary: Assign jobs with machine-dependent times to minimize the largest load; each vertex of the LP for a target T has a pseudo-forest support, so rounding adds at most one job per machine.
model: word-ram
complexity:
  vars: {m: the number of machines, n: the number of jobs}
  time: {worst: O(m^n (n + m))}
prereqs: [makespan, lp-relaxation, extreme-point, basic-feasible-solution, bipartite-matching]
see_also: [lenstra-shmoys-tardos, unrelated-machine-scheduling, generalized-assignment-problem, shmoys-tardos-gap, restricted-assignment-scheduling, unrelated-makespan-inapproximability, configuration-lp, dual-approximation]
sources:
  - paper: doi:10.1007/BF01585745
    title: Jan Karel Lenstra, David B. Shmoys and Éva Tardos, Approximation algorithms for scheduling unrelated parallel machines, Mathematical Programming 46, 1990
    locator: the LP for a target T, the pseudo-forest structure of its vertices, the factor 2, and the 3/2 hardness
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 17 (scheduling on unrelated parallel machines)
  - book: isbn:9781107007512
    title: Lap Chi Lau, R. Ravi and Mohit Singh, Iterative Methods in Combinatorial Optimization, Cambridge University Press, 2011
    locator: Chapter 3 (the generalized assignment problem, with makespan as the case without costs)
  - title: Evgeny V. Shchepin and Nodari Vakhania, An optimal rounding gives a better approximation for scheduling unrelated machines, Operations Research Letters 33(2), 2005
    locator: the ratio 2 - 1/m from the same LP
---

In unrelated machine scheduling, written $R \| C_{\max}$, job $j$ takes time $p_{ij}$ on machine $i$, with no relation between the machines, and the task is to assign each job to one machine so that the largest load, the *makespan*, is as small as possible. This page treats the problem through the linear program of Lenstra, Shmoys and Tardos (1990). For a target $T$, the program $\text{LP}(T)$ asks for a fractional assignment with all loads at most $T$, and it forbids a job on a machine where it alone takes more than $T$. The main fact is structural: the support of each vertex of $\text{LP}(T)$ is a *pseudo-forest*, a graph in which each component has at most one cycle. So the fractional jobs can be matched to distinct machines, and each machine gets at most one extra job, of time at most $T$. This gives makespan at most $2T$, which is the [Lenstra-Shmoys-Tardos algorithm](/lenstra-shmoys-tardos/). The general page on the problem is [scheduling on unrelated machines](/unrelated-machine-scheduling/).

## In plain words

Machines of different kinds must do a list of jobs, and a job can be fast on one machine and slow on another. Each job goes to one machine, and you want the busiest machine to finish as early as possible.

Guess a finish time $T$, and first allow jobs to be split between machines. If even the split version cannot finish by $T$, the guess is too low. If it can, look at a corner of the split solution. Few jobs are split, and they form a sparse pattern, so each machine can take one of the split jobs in full. Each such job fits within $T$ by itself, so no machine goes past $2T$.

## Definition

**Input.** Machines $i = 1, \ldots, m$, jobs $j = 1, \ldots, n$, and times $p_{ij} \ge 0$, where $p_{ij} = \infty$ means that job $j$ cannot run on machine $i$.

**Output.** A map $\sigma$ from jobs to machines with the least makespan $\max_i \sum_{j : \sigma(j) = i} p_{ij}$.

**The LP for a target.** For $T \ge 0$, let $S_T = \{(i, j) : p_{ij} \le T\}$, and let $\text{LP}(T)$ be the system

$$\sum_{i : (i, j) \in S_T} x_{ij} = 1 \text{ for each job } j, \qquad \sum_{j : (i, j) \in S_T} p_{ij} x_{ij} \le T \text{ for each machine } i, \qquad x \ge 0,$$

with a variable only for each pair in $S_T$. If some schedule has makespan $T$, its 0-1 point is feasible, since no job in it takes more than $T$. So the least $T^*$ for which $\text{LP}(T)$ is feasible is a lower bound on OPT. The plain LP that minimizes $T$ without the rule $x_{ij} = 0$ for $p_{ij} > T$ has a gap as large as $m$, so this rule is essential.

**Support graph.** For a point $x$, the support graph $G(x)$ is the bipartite graph on the jobs and the machines with an edge $ij$ when $x_{ij} > 0$.

**Lemma (pseudo-forest).** If $x$ is a vertex of $\text{LP}(T)$, each component of $G(x)$ has at most as many edges as vertices.

*Proof.* $\text{LP}(T)$ has $n + m$ rows besides $x \ge 0$. At a vertex, the tight rows have rank equal to the number of variables, so at most $n + m$ variables can be nonzero. For one component $K$, with $n_K$ jobs and $m_K$ machines, the restriction of $x$ to the edges of $K$ is a vertex of the same system written only for the jobs and machines of $K$, with the edges of $K$ as its variables. If it were not, it would be the midpoint of two feasible points of that system, and extending both by $x$ outside $K$ would show that $x$ is not a vertex. So $K$ has at most $n_K + m_K$ edges. $\square$

**Rounding.** A job with $x_{ij} = 1$ goes to $i$. Each other job has degree at least 2 in $G(x)$. In the part of $G(x)$ on the fractional jobs, a pseudo-forest in which every job has degree at least 2, there is a matching that covers all of these jobs: take a machine of degree 1, match it to its job, delete both, and repeat; what is left is a set of even cycles, where every other edge works. Each machine gets at most one matched job, with $p_{ij} \le T$ since $(i, j) \in S_T$, and its integral load is at most its fractional load $T$. So the makespan is at most $2T$.

## Variants

- **Restricted assignment.** $p_{ij} \in \{p_j, \infty\}$, so each job has a fixed time and a set of allowed machines. See [restricted assignment](/restricted-assignment-scheduling/).
- **Graph balancing.** Each job may run on at most two machines, with the same time on both. Ebenlendr, Krčál and Sgall gave ratio $1.75$, and the $3/2$ hardness still holds.
- **Fixed number of machines.** For constant $m$, dynamic programming gives a fully polynomial scheme (Horowitz and Sahni 1976), and Lenstra, Shmoys and Tardos also gave a scheme from the same LP.
- **With costs.** Adding a cost $c_{ij}$ for each assignment gives the [generalized assignment problem](/generalized-assignment-problem/), where the same LP with a cost row gives cost at most OPT and makespan at most $2T$.
- **Max-min (Santa Claus).** Maximize the smallest load instead. Here the support structure gives only weak bounds, and the [configuration LP](/configuration-lp/) is used instead.
- **Related machines.** If $p_{ij} = p_j / s_i$ for machine speeds $s_i$, the problem $Q \| C_{\max}$ has a PTAS (Hochbaum and Shmoys 1988).

## Examples

Take two machines and three jobs.

| | $j_1$ | $j_2$ | $j_3$ |
|---|---|---|---|
| $p_{1j}$ | 2 | 3 | 4 |
| $p_{2j}$ | 4 | 3 | 2 |

Every schedule puts two jobs on one machine, and two jobs on one machine take at least $2 + 3 = 5$. So OPT $= 5$, for example with $j_1, j_2 \to 1$ and $j_3 \to 2$. Each job takes at least its least time, so the total load is at least $2 + 3 + 2 = 7$, and some machine has fractional load at least $7/2$. At $T = 7/2$, the pairs $(2, j_1)$ and $(1, j_3)$ are not in $S_T$, and the vertex $x_{1 1} = 1$, $x_{2 3} = 1$, $x_{1 2} = x_{2 2} = 1/2$ has both loads equal to $7/2$. So $T^* = 7/2$.

The support graph has the edges $1 j_1$, $1 j_2$, $2 j_2$, $2 j_3$, a path on 5 vertices with 4 edges, so it is a tree. The only fractional job is $j_2$, and the rounding gives it to one machine, for makespan $5 \le 2 \cdot 7/2$.

**The gap of $\text{LP}(T)$.** Give each of $m$ machines its own job of time $m - 1$ that can run only there, and one more job of time $m$ on every machine. $\text{LP}(m)$ is feasible: put $1/m$ of the long job on each machine. Every schedule has a machine with the long job and its own job, of load $2m - 1$. So the ratio $\text{OPT}/T^*$ can be $2 - 1/m$.

## Known algorithms

| algorithm | type | guarantee |
|---|---|---|
| brute force over all maps | exact | time $O(m^n (n + m))$ |
| Horowitz and Sahni (1976) | dynamic programming, fixed $m$ | fully polynomial scheme |
| Potts (1985) | LP and enumeration, fixed $m$ | ratio 2 |
| [Lenstra, Shmoys and Tardos](/lenstra-shmoys-tardos/) (1990) | search over $T$, vertex of $\text{LP}(T)$, matching on the pseudo-forest | ratio 2 |
| [Shmoys and Tardos](/shmoys-tardos-gap/) (1993) | slots and min-cost matching | ratio 2, also with costs |
| Shchepin and Vakhania (2005) | a better rounding of the same LP | ratio $2 - 1/m$ |

The search over $T$ can be a binary search over the integers when the times are integers, or over the values $p_{ij}$ and the breakpoints of the LP, as in the [dual approximation](/dual-approximation/) framework.

## Bounds

- **Lower bound used.** $T^*$, the least $T$ for which $\text{LP}(T)$ is feasible.
- **Integrality gap.** $\text{OPT}/T^*$ can be $2 - 1/m$, by the example above, and Shchepin and Vakhania match this. So no rounding of $\text{LP}(T)$ alone can beat $2 - 1/m$.
- **Hardness.** Deciding whether makespan 2 is possible is NP-hard, even for restricted assignment with times 1 and 2, so no ratio below $3/2$ is possible unless P = NP. See [the inapproximability page](/unrelated-makespan-inapproximability/).
- **Stronger LPs.** The [configuration LP](/configuration-lp/) also has gap 2 for $R \| C_{\max}$ (Verschae and Wiese 2014). For restricted assignment it estimates OPT within $33/17$ (Svensson 2012) and $11/6$ (Jansen and Rohwedder 2017), but these estimates do not yet give fast algorithms with the same ratio.

## Reductions

- **Optimization to decision.** A 2-approximation for the decision form, which either reports that $\text{LP}(T)$ is infeasible or returns a schedule of makespan $2T$, gives a 2-approximation for makespan by search over $T$.
- **A case of GAP.** $R \| C_{\max}$ with target $T$ is the [generalized assignment problem](/generalized-assignment-problem/) with zero costs and all limits $T$.
- **From three-dimensional matching.** The $3/2$ hardness reduces three-dimensional matching to restricted assignment with times 1 and 2.
- **To bipartite matching.** The rounding step is a [bipartite matching](/bipartite-matching/) in the support graph that covers the fractional jobs.

## Applications

- **Heterogeneous computing.** Tasks run on processors of different types, such as CPUs and GPUs, where the speed of a task depends on both.
- **Manufacturing.** Orders go to machines that differ in tooling, so the time of an order depends on the machine.
- **Load balancing.** Requests go to servers where some data is local and some is far, so the time depends on the server.

## References
