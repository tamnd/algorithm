---
tag: NWT4PF
kind: problem
slug: assignment-problem
name: Assignment problem
aliases:
- optimal assignment
- weighted bipartite matching
area: graphs/matching
level: core
summary: Match workers to jobs at minimum total cost in a complete bipartite graph.
prereqs: [bipartite-matching, weighted-graph]
see_also: [hungarian-algorithm, jonker-volgenant-algorithm, auction-algorithm, min-cost-flow-problem, minimum-weight-perfect-matching, maximum-weight-matching, bottleneck-matching, lp-duality]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 25.3, The Hungarian algorithm for the assignment problem
  - book: isbn:9780898716634
    title: Rainer Burkard, Mauro Dell'Amico and Silvano Martello, Assignment Problems, SIAM (2009)
    locator: Chapter 4, Linear sum assignment problem (formulation, duality, the Hungarian, shortest path, auction and pseudoflow algorithms), and Chapter 6, Other types of linear assignment problems
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 17, Weighted bipartite matching and the assignment problem (Sections 17.1 to 17.3, the complexity survey in 17.5a and the historical notes in 17.5c), and Section 18.1, The matching and the perfect matching polytope
  - paper: doi:10.1002/nav.3800020109
    title: Harold W. Kuhn, The Hungarian method for the assignment problem, Naval Research Logistics Quarterly 2(1 and 2), 83 to 97 (1955)
    locator: the whole paper
---

The assignment problem asks for a one-to-one assignment of $n$ workers to $n$ jobs that has the least total cost, when assigning worker $i$ to job $j$ costs $c_{ij}$. In graph terms it is a minimum-cost [perfect matching](/perfect-matching/) in the complete [bipartite graph](/bipartite-graph/) $K_{n,n}$ with [edge weights](/weighted-graph/). It is the weighted form of [bipartite matching](/bipartite-matching/). Its linear programming relaxation always has an integer optimum, so it is solved exactly in $O(n^3)$ time by the [Hungarian algorithm](/hungarian-algorithm/), even though there are $n!$ possible assignments.

## In plain words

A manager has the same number of workers and jobs. Each worker can do each job, but at a different cost: one worker is fast at welding and slow at painting, another the other way round. Each worker gets exactly one job, and each job gets exactly one worker. The goal is the plan with the smallest total cost.

Trying every plan is hopeless: with twenty workers there are more than two billion billion plans. The useful fact is that a plan can be proved best by a short certificate: a "price" for each worker and each job such that no worker-job pair costs less than the sum of its two prices, while the chosen pairs cost exactly that sum. Good algorithms build such prices and the plan together.

## Definition

**Input.** An integer $n \ge 0$ and a cost matrix $C = (c_{ij})$ with $1 \le i, j \le n$ and real entries.

**Output.** A permutation $\sigma$ of $\{1, \ldots, n\}$ that minimizes

$$c(\sigma) = \sum_{i=1}^{n} c_{i\,\sigma(i)}.$$

For $n = 0$ the empty permutation is the answer, with cost 0. In graph terms, $X = \{1, \ldots, n\}$ are the rows, $Y = \{1, \ldots, n\}$ the columns, the edge $ij$ has weight $c_{ij}$, and $\sigma$ is the perfect matching $\{ i\sigma(i) \}$.

**Linear program.** With a variable $x_{ij}$ for each pair,

$$\min \sum_{i,j} c_{ij} x_{ij} \quad \text{subject to} \quad \sum_{j} x_{ij} = 1 \;\; (\forall i), \quad \sum_{i} x_{ij} = 1 \;\; (\forall j), \quad x_{ij} \ge 0.$$

Its [dual](/lp-duality/) has a free variable $u_i$ for each row and $v_j$ for each column:

$$\max \sum_i u_i + \sum_j v_j \quad \text{subject to} \quad u_i + v_j \le c_{ij} \;\; (\forall i, j).$$

**Optimality certificate.** If $(u, v)$ is dual feasible and $\sigma$ is a permutation, then $c(\sigma) = \sum_i c_{i\sigma(i)} \ge \sum_i (u_i + v_{\sigma(i)}) = \sum_i u_i + \sum_j v_j$, since $\sigma$ meets each column once. So $\sigma$ is optimal when every chosen pair is *tight*, $u_i + v_{\sigma(i)} = c_{i\sigma(i)}$. Such a pair $(\sigma, (u, v))$ always exists, because the constraint matrix is the incidence matrix of a bipartite graph, which is [totally unimodular](/total-unimodularity/): every vertex of the feasible region is a permutation matrix, and by [strong duality](/strong-duality/) the optimal values are equal. This is the Birkhoff and von Neumann theorem in LP form.

## Variants

- **Maximization.** Maximize $\sum_i w_{i\sigma(i)}$. Use $c_{ij} = -w_{ij}$, or $c_{ij} = W - w_{ij}$ with $W = \max w$ to keep the costs non-negative. Every permutation has $n$ terms, so the shift does not change the optimal $\sigma$.
- **Rectangular.** $n$ rows and $m \ge n$ columns, each row assigned to a distinct column. Pad with $m - n$ rows of zeros, or use an algorithm that handles the rectangular case directly.
- **Forbidden pairs.** Only the pairs in an edge set $E$ are allowed: a minimum-cost perfect matching in a sparse bipartite graph. A cost $M > 2\sum_{ij \in E} |c_{ij}|$ on each forbidden pair reduces it to the complete case; the answer is infeasible if the optimum uses such a pair.
- **Maximum-weight matching, not perfect.** Any number of pairs may be chosen: [maximum weight matching](/maximum-weight-matching/). Only pairs of positive weight help.
- **Bottleneck.** Minimize the largest cost $\max_i c_{i\sigma(i)}$ instead of the sum: [bottleneck matching](/bottleneck-matching/).
- **General graphs.** Pair up the vertices of a non-bipartite graph at least cost: [minimum-weight perfect matching](/minimum-weight-perfect-matching/), solved by Edmonds' weighted blossom algorithm.
- **Many-to-one and transportation.** Rows and columns have supplies and demands: the transportation problem, a case of the [min cost flow problem](/min-cost-flow-problem/).
- **Quadratic assignment.** The cost depends on pairs of assignments. This problem is NP-hard and much harder in practice.

## Examples

**A 4 by 4 instance.**

$$C = \begin{pmatrix} 9 & 2 & 7 & 8 \\ 6 & 4 & 3 & 7 \\ 5 & 8 & 1 & 8 \\ 7 & 6 & 9 & 4 \end{pmatrix}$$

Of the $4! = 24$ permutations, the cheapest is $\sigma = (2, 1, 3, 4)$: row 1 to column 2, row 2 to column 1, row 3 to column 3 and row 4 to column 4, with cost $2 + 6 + 1 + 4 = 13$. The next cheapest costs 14. The dual solution $u = (4, 6, 4, 4)$, $v = (0, -2, -3, 0)$ is feasible: the reduced costs $c_{ij} - u_i - v_j$ are

$$\begin{pmatrix} 5 & 0 & 6 & 4 \\ 0 & 0 & 0 & 1 \\ 1 & 6 & 0 & 4 \\ 3 & 4 & 8 & 0 \end{pmatrix},$$

all non-negative, and the four chosen pairs have reduced cost 0. Its value is $18 - 5 = 13$, so it proves that 13 is optimal.

**Greedy fails.** Taking the cheapest entry first, 1 at row 3 and column 3, then the cheapest entry in the remaining rows and columns, 2 at row 1 and column 2, then 4 at row 4 and column 4, leaves row 2 with column 1 at cost 6. Here the greedy plan happens to cost 13 too. With $C = \begin{pmatrix} 1 & 2 \\ 2 & 100 \end{pmatrix}$, greedy takes 1 and is forced to 100, for 101, while the optimum is $2 + 2 = 4$.

**Edge cases.** For $n = 0$ the cost is 0. For $n = 1$ the only assignment costs $c_{11}$. If all entries are equal to $c$, every permutation costs $nc$. Negative costs are allowed; adding a constant to a whole row or column changes every assignment cost by the same amount and keeps the optimal set.

## Known algorithms

- [Hungarian algorithm](/hungarian-algorithm/) (Kuhn 1955, Munkres 1957): a primal-dual method that grows [alternating trees](/alternating-path/) in the subgraph of tight pairs. $O(n^3)$ time in the version with shortest augmenting paths.
- [Jonker-Volgenant algorithm](/jonker-volgenant-algorithm/): shortest augmenting paths with an initialization by column reduction and auction-like steps, $O(n^3)$ and among the fastest codes for dense matrices.
- [Successive shortest paths](/successive-shortest-path/) on the [min cost flow](/min-cost-flow-problem/) network with potentials and [Dijkstra's algorithm](/dijkstra/): $n$ augmentations, $O(n(m + n\log n))$ time with a Fibonacci heap on a graph with $m$ allowed pairs.
- [Auction algorithm](/auction-algorithm/) (Bertsekas): persons bid for objects; with $\varepsilon$-scaling it is weakly polynomial and runs well in parallel.
- [Cost scaling](/cost-scaling/) (Gabow and Tarjan, 1989): $O(m\sqrt n \log(nN))$ time for integer costs of absolute value at most $N$.
- [Network simplex](/network-simplex/) and general linear programming solvers, which return an integer optimum by total unimodularity.
- Brute force over the $n!$ permutations, only for checking small cases.

## Bounds

- **Upper bounds.** $O(n^3)$ for a dense $n \times n$ matrix with real costs. $O(nm + n^2 \log n)$ for $m$ allowed pairs with real costs, by Fredman and Tarjan's Fibonacci heaps in the shortest augmenting path method. $O(m\sqrt n \log(nN))$ for integer costs bounded by $N$, by Gabow and Tarjan. Schrijver's Section 17.5a lists further bounds.
- **Lower bound.** $\Omega(n^2)$ for a dense matrix in the worst case: an algorithm that does not read some entry $c_{ij}$ cannot tell whether that entry is very small, which would put the pair $ij$ in every optimum.
- **Value.** The optimum equals the maximum of the dual, $\min_\sigma c(\sigma) = \max \{ \sum u_i + \sum v_j : u_i + v_j \le c_{ij} \}$.

## Reductions

- **To min-cost flow.** A source with arcs of capacity 1 to each row, an arc of capacity 1 and cost $c_{ij}$ from row $i$ to column $j$, and arcs of capacity 1 from each column to a sink; send $n$ units at least cost. Integrality of min-cost flows gives a permutation.
- **To minimum-weight perfect matching** in a general graph, since $K_{n,n}$ is a graph.
- **From bipartite matching.** Give cost 0 to the edges of a bipartite graph and cost 1 to the missing pairs. The optimum cost is $n - \nu(G)$.
- **From bottleneck matching.** Sort the distinct costs and use costs that grow fast enough, such as powers of $n + 1$ by rank; then minimizing the sum also minimizes the largest cost. Direct threshold methods are faster.

## Applications

- Assigning workers to jobs, machines to tasks, or vehicles to requests at least total cost.
- Data association in tracking: matching the detections of one frame to the tracks of the previous frame by distance.
- Distances between equal-size point sets, such as the earth mover's distance between two sets of $n$ points with unit mass.
- A relaxation for harder problems: dropping the subtour constraints of the travelling salesman problem leaves an assignment problem, used as a lower bound in branch and bound.
- The training loss of some object detection networks, which match the predicted objects to the true objects of an image by the [Hungarian algorithm](/hungarian-algorithm/).

## References
