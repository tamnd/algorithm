---
tag: HXX03C
kind: problem
slug: quadratic-assignment-problem
name: Quadratic assignment problem
aliases:
- QAP
- Koopmans-Beckmann problem
area: optimization/combinatorial-optimization
level: advanced
summary: Assign facilities to locations minimizing a sum of pairwise flow-distance products.
prereqs: [assignment-problem, combinatorial-optimization-problem, np-hard]
see_also: [assignment-problem, gilmore-lawler-bound, traveling-salesman-problem, graph-partitioning-problem, tabu-search, simulated-annealing, semidefinite-programming, facility-location-problem]
sources:
  - book: isbn:9780898716634
    title: Rainer Burkard, Mauro Dell'Amico and Silvano Martello, Assignment Problems, SIAM, 2009
    locator: Chapter 7, Quadratic assignment problems, formulations and bounds; Chapter 8, Quadratic assignment problems, algorithms
  - paper: doi:10.2307/1907742
    title: Tjalling C. Koopmans and Martin Beckmann, Assignment problems and the location of economic activities, Econometrica 25(1), 53 to 76, 1957
    locator: the definition of the problem with flows and distances
  - paper: doi:10.1145/321958.321975
    title: Sartaj Sahni and Teofilo Gonzalez, P-complete approximation problems, Journal of the ACM 23(3), 555 to 565, 1976
    locator: the result that the quadratic assignment problem has no polynomial-time approximation with a constant ratio unless P = NP
  - paper: doi:10.1137/0110022
    title: P. C. Gilmore, Optimal and suboptimal algorithms for the quadratic assignment problem, Journal of the Society for Industrial and Applied Mathematics 10(2), 305 to 313, 1962
    locator: the lower bound by linear assignment problems
  - paper: doi:10.1287/mnsc.9.4.586
    title: Eugene L. Lawler, The quadratic assignment problem, Management Science 9(4), 586 to 599, 1963
    locator: the general form with four-index costs and the lower bound
  - paper: "Kurt Anstreicher, Nathan Brixius, Jean-Pierre Goux and Jeff Linderoth, Solving large quadratic assignment problems on computational grids, Mathematical Programming 91(3), 563 to 588, 2002"
    locator: the exact solution of the instance nug30
  - paper: "Éric Taillard, Robust taboo search for the quadratic assignment problem, Parallel Computing 17(4 to 5), 443 to 455, 1991"
    locator: the robust tabu search method
---

The quadratic assignment problem (QAP) asks for a one-to-one assignment of $n$ facilities to $n$ locations that minimizes the sum, over all pairs of facilities, of the flow between them times the distance between their locations. It contains the [traveling salesman problem](/traveling-salesman-problem/) as a special case, so it is strongly [NP-hard](/np-hard/), and Sahni and Gonzalez (1976) showed that it has no polynomial-time approximation algorithm with any constant ratio unless P = NP. It is also very hard in practice: exact methods based on [branch and bound](/knapsack-branch-and-bound/) with lower bounds such as the [Gilmore-Lawler bound](/gilmore-lawler-bound/) reach only about $n = 30$, and larger instances are attacked with [tabu search](/tabu-search/) and other metaheuristics.

## In plain words

A hospital has $n$ departments and $n$ rooms. Some departments exchange many patients or files with each other, and the rooms are at different walking distances. You want to put each department in its own room so that the total walking is smallest. A pair of departments with a lot of traffic should be close.

The [assignment problem](/assignment-problem/) also places $n$ things in $n$ slots, but there each placement has its own cost, and fast methods exist. Here the cost of a placement depends on where all the other departments go. This is what makes the problem so hard: even with 30 departments, proving the best plan took a large computer network.

## Definition

**Input (Koopmans-Beckmann form).** An integer $n$, a *flow* matrix $F = (f_{ij})$ between facilities, and a *distance* matrix $D = (d_{kl})$ between locations, both $n \times n$ with non-negative entries. Optionally a linear cost matrix $C = (c_{ik})$ for placing facility $i$ at location $k$.

**Output.** A permutation $\pi$ of $\{1, \ldots, n\}$, where $\pi(i)$ is the location of facility $i$, that minimizes

$$ \sum_{i=1}^n \sum_{j=1}^n f_{ij} \, d_{\pi(i) \pi(j)} + \sum_{i=1}^n c_{i \pi(i)}. $$

With a permutation matrix $X$ ($x_{ik} = 1$ when $\pi(i) = k$), the objective is $\mathrm{tr}(F X D X^{\top}) + \mathrm{tr}(C^{\top} X)$, a quadratic function over the assignment polytope's vertices. Lawler's (1963) *general form* has a cost $q_{ijkl}$ for each pair of placements $(i \to k, j \to l)$ and minimizes $\sum_{i,j} q_{i j \pi(i) \pi(j)}$.

There are $n!$ permutations. With $F = 0$ the problem is the linear [assignment problem](/assignment-problem/), solved in $O(n^3)$ time by the [Hungarian algorithm](/hungarian-algorithm/).

## Variants

- **Symmetric QAP.** $F$ and $D$ are symmetric, as in most layout problems. Then each unordered pair is counted twice.
- **Lawler QAP.** Four-index costs $q_{ijkl}$, the most general form.
- **Bottleneck QAP.** Minimize the largest term $f_{ij} d_{\pi(i)\pi(j)}$ instead of the sum.
- **Special structures.** For some matrix classes (for example, when one matrix is a Toeplitz or Monge matrix of a special kind and the other has a matching structure), the optimum has a fixed form and can be found fast. Burkard, Dell'Amico and Martello (Chapter 8) survey these cases.
- **Generalized and multi-dimensional QAP.** Several facilities per location with capacities, or three-index versions.

## Examples

Four facilities A, B, C, D have flows A-B 5, A-C 2, B-C 3, C-D 4 (in both directions) and no other flows. The locations are the points 0, 1, 2 and 4 on a line, with $d_{kl} = |k - l|$. The objective counts every ordered pair, so each unordered pair twice.

| assignment (A, B, C, D) | cost |
| --- | --- |
| (0, 1, 2, 4) | $2(5 \cdot 1 + 2 \cdot 2 + 3 \cdot 1 + 4 \cdot 2) = 40$ |
| (1, 0, 2, 4) | $2(5 \cdot 1 + 2 \cdot 1 + 3 \cdot 2 + 4 \cdot 2) = 42$ |
| (4, 2, 1, 0) | 46 |
| (2, 0, 4, 1) | 76 |

Checking all $4! = 24$ assignments shows that 40 is the optimum and 76 the worst. The optimum puts the chain A-B-C-D in order along the line, with the heaviest flow, A-B, on a short gap and the lonely facility D at the far point. Swapping only A and B costs 2 more, which shows how one move changes several terms at once.

## Known algorithms

- **Branch and bound.** Fix the location of one facility at a time, and bound the rest from below. The [Gilmore-Lawler bound](/gilmore-lawler-bound/) (1962, 1963) solves a linear assignment problem whose costs are themselves small assignment problems. For the Koopmans-Beckmann form, sorting the rows of $F$ and $D$ gives it in $O(n^3)$ time per node, and for the Lawler form it takes $O(n^5)$. Stronger bounds come from eigenvalues of $F$ and $D$, from [semidefinite programming](/semidefinite-programming/), and from the reformulation-linearization technique, at a higher cost per node. Anstreicher, Brixius, Goux and Linderoth (2002) solved the classic instance nug30, with $n = 30$, by branch and bound with convex quadratic bounds on a computational grid.
- **Linearizations.** Mixed integer programs with $O(n^4)$ variables (Lawler) or $O(n^2)$ extra variables (Kaufman-Broeckx and others). They are exact but their LP bounds are weak.
- **Local search.** Pairwise exchange of the locations of two facilities. The change in cost of one swap can be computed in $O(n)$ time, and in $O(1)$ time from stored values of the previous iteration.
- **Metaheuristics.** Robust [tabu search](/tabu-search/) (Taillard, 1991), [simulated annealing](/simulated-annealing/), [GRASP](/grasp/), [ant colony optimization](/ant-colony-optimization/) and hybrid genetic methods. They find the best known solutions of the QAPLIB benchmark instances, but without a proof of optimality.

## Bounds

- **Strong NP-hardness.** The TSP reduction below uses small numbers, so QAP is NP-hard in the strong sense.
- **No constant ratio.** Sahni and Gonzalez (1976): unless P = NP, no polynomial-time algorithm for QAP has a constant approximation ratio. The proof is a gap reduction from Hamiltonian cycle, in the same way as for the general TSP.
- **Lower bounds.** The cheap bounds, such as Gilmore-Lawler, are often far from the optimum. This is the main reason why branch and bound is slow on the QAP.
- **Exact time.** We do not know an algorithm with worst-case time $c^n$ for a constant $c$. Dynamic programming over subsets, which gives $O(n^2 2^n)$ for the TSP, does not apply directly, because the cost of a placement depends on the locations of all other facilities.

## Reductions

- **From [TSP](/traveling-salesman-problem/).** Let $F$ be the adjacency matrix of the cycle $1, 2, \ldots, n, 1$ and $D$ the matrix of distances between cities. Then $\sum_{i,j} f_{ij} d_{\pi(i)\pi(j)}$ is twice the length of the tour $\pi(1), \ldots, \pi(n)$, so an optimal assignment is an optimal tour.
- **From [graph partitioning](/graph-partitioning-problem/).** Let $F$ be the adjacency matrix of the graph and $D$ the matrix with $d_{kl} = 1$ when $k$ and $l$ are in different halves of a fixed split of the locations, and 0 otherwise. Then the cost is twice the number of cut edges of the bisection given by $\pi$.
- **From maximum [clique](/maximum-clique/) and [graph isomorphism](/graph-isomorphism-problem/).** Use the maximization version. With $F$ the adjacency matrix of a $k$-clique, padded with zeros to size $n$, and $D$ the adjacency matrix of a graph $G$, the maximum is $k(k-1)$ exactly when $G$ has a $k$-clique. With $F$ and $D$ the adjacency matrices of two graphs with $m$ edges each, the maximum is $2m$ exactly when the graphs are isomorphic.
- **To the linear assignment problem.** Only as a relaxation: the Gilmore-Lawler bound replaces the quadratic term by a linear assignment problem.

## Applications

- **Facility layout.** Departments in a hospital or a factory, gates in an airport, and machines on a shop floor (Koopmans and Beckmann, 1957).
- **Electronics.** Placement of components on a board to shorten the total wire length.
- **Keyboard design.** Letters to keys, with flows given by how often two letters follow each other and distances by the time to move between keys.
- **Other problems.** Scheduling, image processing and the balancing of turbine runners have been modeled as QAPs (Burkard, Dell'Amico and Martello, Chapter 7).

## References
