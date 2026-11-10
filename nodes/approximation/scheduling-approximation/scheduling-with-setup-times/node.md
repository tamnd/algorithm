---
tag: KEC6PH
kind: problem
slug: scheduling-with-setup-times
name: Scheduling with setup times
aliases:
- sequence-dependent setup scheduling
- 1|s_ij|Cmax
- changeover times
- family setup times
area: approximation/scheduling-approximation
level: advanced
summary: The machine needs a setup between jobs, which may depend on both jobs. On one machine the makespan is then a shortest Hamiltonian path, an asymmetric TSP, solved by Held-Karp for small n.
prereqs: [scheduling-notation, makespan, traveling-salesman-problem]
see_also: [asymmetric-tsp, held-karp-algorithm, hamiltonian-path-problem, bitmask-dp, christofides-algorithm, strong-np-hardness, flow-shop-scheduling, weighted-completion-time-scheduling]
sources:
  - paper: "Paul C. Gilmore and Ralph E. Gomory, Sequencing a one state-variable machine: a solvable case of the traveling salesman problem, Operations Research 12(5), 1964"
    locator: pages 655 to 679 (setups given by the states of the machine, solved in polynomial time)
  - paper: "Clyde L. Monma and Chris N. Potts, On the complexity of scheduling with batch setup times, Operations Research 37(5), 1989"
    locator: pages 798 to 804 (family setups, with dynamic programs and NP-hardness results)
  - paper: "Michael Held and Richard M. Karp, A dynamic programming approach to sequencing problems, Journal of the Society for Industrial and Applied Mathematics 10(1), 1962"
    locator: pages 196 to 210 (the dynamic program over subsets)
  - paper: "Ali Allahverdi, C. T. Ng, T. C. E. Cheng and Mikhail Y. Kovalyov, A survey of scheduling problems with setup times or costs, European Journal of Operational Research 187(3), 2008"
    locator: pages 985 to 1032 (a survey by machine model and kind of setup)
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 9, Changeover Times and Transportation Times
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 4, Advanced Single Machine Models (Deterministic), sequence-dependent setup times
---

Scheduling with setup times is the family of scheduling problems in which a machine needs time to get ready between two jobs: to clean, change a tool, or heat up. If the setup depends only on the next job, it can be added to the processing time and nothing changes. If it depends on the class of the job, the jobs form **families** and it pays to run each family in one batch. If it depends on both the job before and the job after, the setups are **sequence-dependent**, written $s_{ij}$, and the order of the jobs decides how much time is lost. For the [makespan](/makespan/) on one machine, $1 \mid s_{ij} \mid C_{\max}$, the problem is then the same as a shortest Hamiltonian path in a directed graph, the path version of the [asymmetric TSP](/asymmetric-tsp/). So it is strongly NP-hard, it has no approximation ratio at all without the triangle inequality, and the [Held-Karp](/held-karp-algorithm/) dynamic program solves it exactly in $O(2^n n^2)$ time. Gilmore and Gomory (1964) found an important special case that is solvable in polynomial time.

## In plain words

A painting line paints cars in different colors. Going from white to black is quick, but going from black to white needs a long cleaning. The total time is the painting time, which is fixed, plus the cleaning time between cars, which depends on the order. Finding the order with the least cleaning is the same as finding the shortest route that visits every color once, where the road from one color to the next has the length of the cleaning. That is the traveling salesman problem with one-way roads.

## Definition

**Input.** Jobs $1, \ldots, n$ with processing times $p_j \ge 0$, initial setups $s_{0j} \ge 0$ for the first job, and setups $s_{ij} \ge 0$ for running $j$ right after $i$.

**Output.** An order $\sigma(1), \ldots, \sigma(n)$ of the jobs on one machine.

**Goal.** Minimize the makespan

$$C_{\max} = \sum_j p_j + s_{0 \sigma(1)} + \sum_{k=1}^{n-1} s_{\sigma(k) \sigma(k+1)}.$$

The first sum does not depend on the order. So the problem is to find a Hamiltonian path that starts at the node 0 of the complete directed graph on $\{0, 1, \ldots, n\}$ with arc lengths $s_{ij}$, of least length. If the machine must also return to its initial state at the end, with setups $s_{j0}$, the problem is the asymmetric TSP itself.

**Kinds of setups.**

- *Sequence-independent*, $s_{ij} = t_j$: add $t_j$ to $p_j$; every order has the same setups.
- *Family setups*, $s_{ij} = 0$ if $i$ and $j$ are in the same family and $f_c$ if $j$ is in family $c$ and $i$ is not: written $s_f$ or $s_c$.
- *Sequence-dependent*, $s_{ij}$ arbitrary: written $s_{ij}$ or $s_{jk}$.
- *Setups that satisfy the triangle inequality*, $s_{ik} \le s_{ij} + s_{jk}$: going through a third job never saves time. Most physical setups behave this way.

## Variants

| problem | status |
|---|---|
| $1 \mid s_j \mid C_{\max}$, sequence-independent | trivial: every order is optimal |
| $1 \mid s_f \mid C_{\max}$, family setups | $O(n)$: run each family as one batch |
| $1 \mid s_{ij} \mid C_{\max}$ | strongly NP-hard; no finite ratio in general; Held-Karp $O(2^n n^2)$ |
| $1 \mid s_{ij} \mid C_{\max}$, triangle inequality | constant-factor approximations, from the [ATSP](/asymmetric-tsp/) path version |
| $1 \mid s_{ij} \mid C_{\max}$, symmetric with triangle inequality | factor $3/2$ for a path with one fixed end (Hoogeveen 1991) |
| $1 \mid s_{ij} \mid C_{\max}$, Gilmore-Gomory setups | polynomial (Gilmore and Gomory 1964) |
| $1 \mid s_f \mid \sum w_j C_j$ and $1 \mid s_f \mid L_{\max}$ | polynomial for a fixed number of families (Monma and Potts 1989); harder in general, see the survey of Allahverdi and others (2008) |
| $P \mid s_{ij} \mid C_{\max}$ | contains both $P \| C_{\max}$ and the TSP path |

## Examples

**Four jobs.** Take the jobs below, numbered from 0, with initial setups $s_{0j}$ and the setup matrix $s_{ij}$ (row $i$ is the job before, column $j$ the job after).

| | job 0 | job 1 | job 2 | job 3 |
|---|---|---|---|---|
| $p_j$ | 3 | 2 | 4 | 1 |
| $s_{0j}$ | 2 | 5 | 1 | 4 |
| after job 0 | | 1 | 6 | 3 |
| after job 1 | 4 | | 2 | 7 |
| after job 2 | 5 | 3 | | 1 |
| after job 3 | 9 | 6 | 4 | |

The processing times add up to 10. The order $0, 1, 2, 3$ has setups $2 + 1 + 2 + 1 = 6$, so $C_{\max} = 16$, and a search over all 24 orders shows that this is optimal. The nearest neighbor rule, which always runs next the job with the smallest setup, starts with job 2 ($s_{02} = 1$), then job 3 ($1$), then job 1 ($6$, since $s_{30} = 9$), then job 0 ($4$). Its setups add up to 12 and $C_{\max} = 22$. A cheap first step led to an expensive later one.

**Families.** Jobs in three families with setups $f_1, f_2, f_3$: any order has at least one setup into each family that appears, because the first job of a family follows a job of another family or the initial state. Running each family as one batch pays exactly one setup per family, so it is optimal, with $C_{\max} = \sum_j p_j + \sum_c f_c$.

**Hardness.** Given a directed graph $G$ on $n$ nodes, make a job for each node with $p_j = 0$, $s_{0j} = 0$, $s_{ij} = 0$ for an arc $(i, j)$ and $s_{ij} = 1$ otherwise. Then $C_{\max} = 0$ is possible if and only if $G$ has a [Hamiltonian path](/hamiltonian-path-problem/). So the problem is strongly NP-hard. An algorithm with any finite ratio would find a schedule of value 0 whenever one exists, so no such algorithm runs in polynomial time unless P = NP.

## Known algorithms

**Held-Karp for setups.** Let $D(S, j)$ be the least total setup of an order that runs exactly the jobs of the set $S$ and ends with $j \in S$.

```pseudo id=main
HELD-KARP-SETUP(p[1 .. n], s0[1 .. n], s[1 .. n][1 .. n])
L1  D(S, j) ← ∞ for all sets S and jobs j
L2  for each job j: D({j}, j) ← s0[j]
L3  for each set S, by increasing size, and each j ∈ S with D(S, j) < ∞ do
L4      for each job k ∉ S: D(S ∪ {k}, k) ← min(D(S ∪ {k}, k), D(S, j) + s[j][k])
L5  pick the last job ℓ with the least D(all jobs, ℓ), and follow the choices back to get the order
L6  return the order and Cmax = D(all jobs, ℓ) + p[1] + ... + p[n]
```

*Correctness.* By induction on $|S|$, $D(S, j)$ is the least setup of an order of $S$ that ends with $j$. For $|S| = 1$ this is line L2. For larger $S$, an optimal order of $S$ that ends with $k$ consists of an optimal order of $S - \{k\}$ that ends with some $j$, followed by $k$. Line L4 tries every such $j$. The implementation runs over the sets in increasing order of their bitmasks, which also works, since $S$ is smaller than $S \cup \{k\}$ as a number.

*Cost.* There are $2^n n$ states and $n$ choices for each, so the time is $O(2^n n^2)$ and the space is $O(2^n n)$. This is practical up to about 20 jobs. See [bitmask DP](/bitmask-dp/).

The tests of this page compare HELD-KARP-SETUP with a search over all orders on seeded random instances with up to 7 jobs, and check that sequence-independent setups do not matter and that batching is optimal for family setups.

**Other algorithms.**

- **Gilmore and Gomory (1964).** Each job $j$ has a start state $a_j$ and an end state $b_j$, for example a temperature, and the setup from $i$ to $j$ is the cost of moving the machine from state $b_i$ to state $a_j$, given by integrals of cost functions. Gilmore and Gomory solve this special case of the TSP in polynomial time, by a matching of the states followed by a patching of the cycles.
- **Approximation with the triangle inequality.** Then the problem is the path version of the [asymmetric TSP](/asymmetric-tsp/), which has constant-factor approximation algorithms. If the setups are also symmetric, the path version of [Christofides' algorithm](/christofides-algorithm/) gives $3/2$ for a path with one fixed end (Hoogeveen 1991).
- **Heuristics.** Nearest neighbor, insertion, and local search such as 2-opt and Or-opt are common in practice, as for the TSP. The example above shows that nearest neighbor can be far from optimal.
- **Family setups with other objectives.** Inside a family, jobs run in the order of the objective without setups, for example by [Smith's rule](/smith-rule/) for $\sum w_j C_j$. It can still pay to split a family into several batches, so the number of setups is part of the choice. Monma and Potts (1989) give dynamic programs that are polynomial when the number of families is fixed.

## Bounds

- **Exact.** $O(2^n n^2)$ time for $1 \mid s_{ij} \mid C_{\max}$ by Held-Karp. The problem contains the Hamiltonian path problem, so under the exponential time hypothesis no algorithm runs in time $2^{o(n)}$.
- **Approximation.** No finite ratio for arbitrary setups unless P = NP, by the hardness example above. With the triangle inequality, constant factors exist.
- **A simple upper bound.** Any order has $C_{\max} \le \sum_j p_j + n \max_{i, j} s_{ij}$, and every order has $C_{\max} \ge \sum_j p_j$. So when setups are small compared to processing times, every order is close to optimal.

## Reductions

- **To and from the TSP path.** $1 \mid s_{ij} \mid C_{\max}$ is the shortest Hamiltonian path from node 0 with arc lengths $s_{ij}$. With a return to the initial state it is the asymmetric TSP. See [TSP](/traveling-salesman-problem/).
- **From Hamiltonian path.** As in the example with 0 and 1 setups, which gives strong NP-hardness and the lack of a ratio.
- **Two-machine flow shop with no wait.** In a [flow shop](/flow-shop-scheduling/) in which a job must start on the second machine as soon as it ends on the first, the makespan is a sum of sequence-dependent gaps, and the problem is a Gilmore-Gomory TSP.

## Applications

- **Paint shops and printing.** Colors run from light to dark to keep cleaning short.
- **Chemical and food plants.** Batches of different products need cleaning in between, often more in one direction than in the other.
- **Steel and paper mills.** The width, thickness or temperature of the product must change gradually, so the setup depends on the state the machine is in, as in the case of Gilmore and Gomory.
- **Machine tools.** Changing tools between operations costs time that depends on which tools are already loaded.

## References
