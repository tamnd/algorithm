---
tag: 8P17R0
kind: problem
slug: graph-partitioning-problem
name: Graph partitioning problem
aliases:
- minimum bisection
- balanced graph partition
- graph bisection
- balanced k-way partitioning
area: optimization/combinatorial-optimization
level: core
summary: Split vertices into balanced parts while minimizing the number of cut edges.
prereqs: [graph, cut, np-hard]
see_also: [kernighan-lin, fiduccia-mattheyses, min-cut-problem, sparsest-cut-problem, maximum-cut, spectral-clustering, normalized-cut, quadratic-assignment-problem]
sources:
  - paper: doi:10.1016/0304-3975(76)90059-1
    title: M. R. Garey, D. S. Johnson and L. Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1(3), 237 to 267, 1976
    locator: the NP-completeness of simple max cut and of minimum bisection
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A2.2, Network design (the entries Graph Partitioning and Minimum Cut into Bounded Sets)
  - paper: doi:10.1002/j.1538-7305.1970.tb01770.x
    title: B. W. Kernighan and S. Lin, An efficient heuristic procedure for partitioning graphs, Bell System Technical Journal 49(2), 291 to 307, 1970
    locator: the problem statement and the pair-swap heuristic
  - paper: doi:10.1007/s00224-006-1350-7
    title: Konstantin Andreev and Harald Räcke, Balanced graph partitioning, Theory of Computing Systems 39(6), 929 to 939, 2006
    locator: the result that exact balanced k-partitioning has no finite approximation ratio for k at least 3 unless P = NP, and the bicriteria algorithm
  - paper: doi:10.1137/S0097539701387660
    title: Uriel Feige and Robert Krauthgamer, A polylogarithmic approximation of the minimum bisection, SIAM Journal on Computing 31(4), 1090 to 1118, 2002
    locator: main theorem
  - paper: doi:10.1137/S1064827595287997
    title: George Karypis and Vipin Kumar, A fast and high quality multilevel scheme for partitioning irregular graphs, SIAM Journal on Scientific Computing 20(1), 359 to 392, 1998
    locator: the coarsening, initial partitioning and refinement phases of the multilevel method
---

The graph partitioning problem asks to split the vertices of a graph into $k$ parts of (nearly) equal size so that the total weight of the edges between different parts is as small as possible. Its basic case, *minimum bisection*, splits the vertices into two halves. Minimum bisection is [NP-hard](/np-hard/) (Garey, Johnson and Stockmeyer, 1976), even on unweighted graphs, while the same problem without the balance condition is the [minimum cut](/min-cut-problem/) problem and is solvable in polynomial time. For exact balance and $k \ge 3$ parts, no polynomial-time algorithm has any finite approximation ratio unless P = NP (Andreev and Räcke, 2006). In practice the problem is solved by heuristics such as [Kernighan-Lin](/kernighan-lin/), [Fiduccia-Mattheyses](/fiduccia-mattheyses/), spectral methods and multilevel methods.

## In plain words

A large job must be split among two computers. The job has many small tasks, and some pairs of tasks must talk to each other. Each computer should get the same amount of work. Talk inside one computer is cheap, but talk between the two computers is slow. So you want to split the tasks into two equal groups with as few talking pairs across the split as possible.

Without the rule of equal groups, the task is easy: put everything on one side, or cut off a small loose piece. The rule of equal groups is what makes the problem hard. No fast exact method is known, but good fast methods exist that improve a split step by step.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n = |V|$, non-negative edge weights $w(e)$ (all 1 in the unweighted case), a number of parts $k \ge 2$, and an imbalance $\varepsilon \ge 0$.

**Output.** A partition of $V$ into parts $V_1, \ldots, V_k$ with $|V_i| \le (1 + \varepsilon) \lceil n / k \rceil$ for each $i$ that minimizes the *cut*

$$ \mathrm{cut}(V_1, \ldots, V_k) = \sum_{\{u, v\} \in E, \ u \in V_i, \ v \in V_j, \ i \ne j} w(u, v). $$

**Minimum bisection** is the case $k = 2$, $\varepsilon = 0$ with $n$ even: find $S \subseteq V$ with $|S| = n/2$ that minimizes the weight of the edges between $S$ and $V \setminus S$. The least such weight is the *bisection width* of $G$. The decision version asks whether some bisection has cut at most a bound $K$.

With vertex weights, the balance condition limits the total vertex weight of each part instead of the number of vertices.

## Variants

- **Imbalance.** With $\varepsilon > 0$ the parts may differ a little in size. This makes the problem easier to approximate, and many heuristics need some slack to move single vertices.
- **k-way partitioning.** Split into $k > 2$ parts, often by repeated bisection or by direct $k$-way refinement.
- **Hypergraph partitioning.** The edges are nets that join any number of vertices, as in circuits. A [hypergraph](/hypergraph/) net is cut when its vertices are in different parts. The [Fiduccia-Mattheyses](/fiduccia-mattheyses/) heuristic was designed for this case.
- **Ratio objectives.** The [sparsest cut](/sparsest-cut-problem/), ratio cut and [normalized cut](/normalized-cut/) divide the cut weight by a measure of the sizes of the sides, so they reward balance instead of forcing it.
- **Maximum bisection.** Maximize the cut over all bisections. It is the balanced form of [maximum cut](/maximum-cut/).
- **No balance.** With no size condition, the best split is a [minimum cut](/min-cut-problem/), found in polynomial time, for example by the [Stoer-Wagner algorithm](/stoer-wagner/).

## Examples

Take the graph on the vertices $a, b, c, d, e, f$ with the 8 edges $ab, ac, bc$ (a triangle), $de, df, ef$ (a second triangle) and the two links $cd$ and $be$. All edges have weight 1. There are 10 bisections.

| side containing $a$ | cut edges | cut |
| --- | --- | --- |
| $\{a, b, c\}$ | $cd, be$ | 2 |
| $\{a, b, d\}$ | $ac, bc, be, cd, de, df$ | 6 |
| $\{a, c, d\}$ | $ab, bc, de, df$ | 4 |
| $\{a, b, e\}$ | $ac, bc, de, ef$ | 4 |

The other 6 bisections have cut 5 or 6. The minimum bisection is $\{a, b, c\}, \{d, e, f\}$ with width 2. The [Kernighan-Lin](/kernighan-lin/) page starts from $\{a, b, d\}$, cut 6, and reaches the optimum in one pass by swapping $d$ and $c$.

The [Laplacian matrix](/laplacian-matrix/) of this graph has second smallest eigenvalue $\lambda_2 = 1$, so the spectral bound below gives a width of at least $n \lambda_2 / 4 = 1.5$, so at least 2. Here the bound proves that the bisection found is optimal.

## Known algorithms

- **Exact methods.** [Branch and bound](/knapsack-branch-and-bound/) with lower bounds from [semidefinite programming](/semidefinite-programming/), from eigenvalues, or from linear programming. They solve general instances with some hundreds of vertices, and larger sparse instances in special classes. Trees and graphs of bounded [treewidth](/treewidth/) admit dynamic programming in polynomial time.
- **Local search.** The [Kernighan-Lin](/kernighan-lin/) heuristic (1970) swaps pairs of vertices in passes and keeps the best prefix of each pass. The [Fiduccia-Mattheyses](/fiduccia-mattheyses/) heuristic (1982) moves single vertices with a bucket structure and runs each pass in time linear in the size of the graph. [Simulated annealing](/simulated-annealing/) also works well on some graph classes.
- **Spectral methods.** Split the vertices by the order of their entries in an eigenvector for $\lambda_2$ of the Laplacian (the Fiedler vector), at the median. The idea goes back to Donath and Hoffman (1973) and Fiedler (1973), and it is also the basis of [spectral clustering](/spectral-clustering/).
- **Multilevel methods.** Contract a matching of the graph again and again to get a small graph, partition the small graph, then project the partition back level by level and refine it with Kernighan-Lin or Fiduccia-Mattheyses at each level. METIS (Karypis and Kumar, 1998) and similar tools use this scheme. It is the standard method for large sparse graphs.
- **Approximation.** Feige and Krauthgamer (2002) gave an $O(\log^{1.5} n)$-approximation for minimum bisection, and Räcke (2008) improved it to $O(\log n)$. Balanced separators, where each side needs only a constant fraction of the vertices, have bicriteria algorithms based on the [sparsest cut](/sparsest-cut-problem/) relaxations of Leighton and Rao and of Arora, Rao and Vazirani.

## Bounds

- **NP-hardness.** Minimum bisection is NP-complete as a decision problem, also for unweighted graphs (Garey, Johnson and Stockmeyer, 1976). The reduction is shown below.
- **No finite ratio for exact balance.** For $k \ge 3$ and $\varepsilon = 0$, no polynomial-time algorithm approximates the balanced $k$-partition within any finite factor, unless P = NP (Andreev and Räcke, 2006). The reduction is from 3-partition: a cut of weight 0 exists exactly when the 3-partition instance has a solution, so any finite ratio would decide it.
- **Bisection.** The best known ratio for minimum bisection is $O(\log n)$. No PTAS exists under a complexity assumption slightly stronger than P $\ne$ NP (Khot, 2006). The gap between these bounds is open.
- **Spectral lower bound.** If $n$ is even and $\lambda_2$ is the second smallest eigenvalue of the Laplacian $L$, then every bisection has cut at least $n \lambda_2 / 4$. For a bisection $S$, let $x_v = 1$ for $v \in S$ and $x_v = -1$ otherwise. Then $x^{\top} L x = \sum_{\{u, v\} \in E} w(u, v) (x_u - x_v)^2 = 4 \, \mathrm{cut}(S)$, $x$ is orthogonal to the all-ones vector, and $x^{\top} x = n$, so $4 \, \mathrm{cut}(S) \ge \lambda_2 n$.

## Reductions

- **From maximum cut.** Garey, Johnson and Stockmeyer showed that simple [maximum cut](/maximum-cut/) (unit weights) is NP-complete. Two steps lead to minimum bisection.
  - *Max cut to max bisection.* Add $n$ isolated vertices to $G$. A cut $(S, V \setminus S)$ of $G$ becomes a bisection of the new graph with the same cut, by adding $n - |S|$ isolated vertices to $S$ and the rest to the other side. So the maximum bisection of the new graph equals the maximum cut of $G$.
  - *Max bisection to min bisection.* Let $\bar G$ be the complement of a graph $G$ with $n$ vertices, $n$ even. Each of the $(n/2)^2$ pairs across a bisection is an edge of exactly one of $G$ and $\bar G$, so $\mathrm{cut}_G(S) + \mathrm{cut}_{\bar G}(S) = n^2 / 4$. A minimum bisection of $\bar G$ is a maximum bisection of $G$.
- **To the [quadratic assignment problem](/quadratic-assignment-problem/).** Take the adjacency matrix of $G$ as the flow matrix and a 0-1 distance matrix with distance 1 between the two halves of the locations. The cost of an assignment is twice the cut of the bisection it gives.
- **To ratio cuts.** The [sparsest cut](/sparsest-cut-problem/) and the [normalized cut](/normalized-cut/) replace the hard balance rule by a division by the side sizes or volumes. An approximation algorithm for sparsest cut, applied again and again to the larger side, gives a cut in which each side has at least a third of the vertices, at a cost of at most a constant times its ratio times the bisection width (Leighton and Rao). This is a bicriteria result: the balance is weaker than in a bisection.
- **To quadratic and semidefinite programs.** With $x \in \{-1, 1\}^n$ and $\sum_v x_v = 0$, the cut is $\frac14 x^{\top} L x$. Relaxing $x$ to unit vectors gives a [semidefinite program](/semidefinite-programming/) whose value is a lower bound.

## Applications

- **Circuit design.** Split the cells of a circuit between chips or regions of a chip with few wires between them. This was the motivation of Kernighan and Lin and of Fiduccia and Mattheyses.
- **Parallel computing.** Divide a finite element mesh or a sparse matrix among processors, so that the work is balanced and the communication is small.
- **Sparse linear algebra.** [Nested dissection](/nested-dissection/) orders a [sparse matrix](/sparse-matrix/) for elimination by finding small balanced separators again and again, which reduces fill-in.
- **Clustering and segmentation.** Community detection in networks and image segmentation by [normalized cuts](/normalized-cut/).
- **Distributed data.** Placing the parts of a large graph or database on several machines so that most queries stay on one machine.

## References
