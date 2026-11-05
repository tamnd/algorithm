---
tag: 6NCXJM
kind: problem
slug: minimum-mean-cycle-problem
name: Minimum mean cycle problem
aliases:
- minimum average-weight cycle problem
area: graphs/paths-and-cycles
level: advanced
summary: Find a directed cycle whose average edge weight is minimum.
prereqs: [simple-cycle, weighted-graph, negative-cycle]
see_also: [karp-minimum-mean-cycle, negative-cycle-detection, cycle-canceling, min-cost-flow-problem, minimum-ratio-problem, policy-iteration, min-plus-matrix-multiplication, shortest-cycle-problem]
sources:
  - paper: doi:10.1016/0012-365X(78)90011-0
    title: Richard M. Karp, A characterization of the minimum cycle mean in a digraph, Discrete Mathematics 23(3), 309 to 311 (1978)
    locator: the definition of the minimum cycle mean, the characterization theorem and the O(nm) algorithm
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Prentice Hall, 1993
    locator: Chapter 5, Label-correcting algorithms (the minimum mean cycle problem), and Chapter 10 (minimum mean cycle canceling for minimum cost flow)
  - paper: Andrew V. Goldberg and Robert E. Tarjan, Finding minimum-cost circulations by canceling negative cycles, Journal of the ACM 36(4), 1989
    title: Goldberg and Tarjan, minimum mean cycle canceling
    locator: the minimum mean cycle canceling algorithm and its strongly polynomial bound
  - paper: Neal E. Young, Robert E. Tarjan and James B. Orlin, Faster parametric shortest path and minimum-balance algorithms, Networks 21(2), 1991
    title: Young, Tarjan and Orlin, parametric shortest paths
    locator: the O(nm + n^2 log n) algorithm for the minimum mean cycle
  - paper: Ali Dasdan, Experimental analysis of the fastest optimum cycle ratio and mean algorithms, ACM Transactions on Design Automation of Electronic Systems 9(4), 2004
    title: Dasdan, an experimental comparison of cycle mean algorithms
    locator: the comparison of Karp's algorithm, its variants and Howard's policy iteration
---

The minimum mean cycle problem asks, in a directed graph with arc weights, for a cycle whose weight divided by its number of arcs is as small as possible. The value $\lambda^*$ is the *minimum cycle mean*. It answers questions about repeated behaviour: the best long-run cost per step of a walk, the period of a cyclic schedule, and the best cycle to cancel in a minimum cost flow. Unlike the [longest path problem](/longest-path-problem/) or a shortest simple cycle with negative weights, it is solvable in polynomial time: [Karp's algorithm](/karp-minimum-mean-cycle/) finds $\lambda^*$ in $O(nm)$ time.

## In plain words

Each one-way road has a cost, possibly negative. You will drive around one loop of roads many times. Which loop has the smallest cost per road?

The cheapest loop overall is not the answer: a long loop with a small total can have a large cost per road, and a short loop with a medium total can be better. Dividing by the length makes the question fair between short and long loops.

The answer also tells you whether there is a loop with negative total cost: that happens exactly when the best cost per road is below zero.

## Definition

**Input.** A finite directed graph $G = (V, A)$ with $n = |V|$ vertices and $m = |A|$ arcs, and a weight $w(a) \in \mathbb{R}$ for each arc. Parallel arcs and self-loops are allowed; a self-loop is a cycle with one arc. Isolated vertices and vertices on no cycle are allowed. The graph need not be strongly connected.

**Output.** A directed cycle $C$ that minimizes the mean $\mu(C) = w(C)/|C|$, where $w(C)$ is the sum of the weights of its arcs and $|C|$ is their number, together with $\lambda^* = \mu(C)$; or the answer that $G$ has no directed cycle.

**Walks give the same answer.** A closed walk splits into [simple cycles](/simple-cycle/), and its mean is a weighted average of their means, with weights proportional to their lengths. So the minimum over closed walks equals the minimum over simple cycles, and the problem is the same whether cycles may repeat vertices or not. For the same reason, $\lambda^*$ is the least long-run average weight per arc of an infinite walk.

**Undirected graphs.** The problem is stated for directed graphs. An undirected graph read as a pair of opposite arcs per edge has the cycle $u \to v \to u$ of mean $w(\{u, v\})$, which is usually not intended.

## Variants

- **Maximum mean cycle.** Negate the weights. It is the same problem.
- **Minimum cost-to-time ratio cycle.** Each arc has a cost $c(a)$ and a positive time $t(a)$, and the goal is to minimize $c(C)/t(C)$. The mean cycle is the case $t = 1$. The same search on $\lambda$ applies, see the [minimum ratio problem](/minimum-ratio-problem/).
- **Minimum cycle mean of a strongly connected graph.** The usual setting in Karp's paper; a general graph reduces to its [strongly connected components](/strongly-connected-components/), since every cycle lies in one.
- **Min-plus eigenvalue.** For a strongly connected graph, $\lambda^*$ is the unique eigenvalue of its weight matrix in the min-plus algebra, see [min-plus matrix multiplication](/min-plus-matrix-multiplication/).
- **Minimum total weight cycle.** Without the division, the shortest cycle in total weight is a different problem; with negative weights allowed it is NP-hard for simple cycles, see the [shortest cycle problem](/shortest-cycle-problem/).

## Examples

**Short against long.** Arcs $0 \to 1$ (weight 2), $1 \to 0$ (4), $1 \to 2$ (1), $2 \to 3$ (1), $3 \to 1$ (4), $3 \to 0$ (0). The cycles are $0, 1$ with weight 6 and mean 3, $1, 2, 3$ with weight 6 and mean 2, and $0, 1, 2, 3$ with weight 4 and mean 1. The minimum mean is $\lambda^* = 1$, from the longest cycle, which is also the cheapest in total. Raise the weight of $3 \to 0$ to 3: the long cycle has weight 7 and mean $7/4$, still the best. Raise it to 6: the long cycle has mean $10/4 = 5/2$, and the best cycle is now $1, 2, 3$ with mean 2.

**Total and mean disagree.** Arcs $0 \to 0$ (weight 3), $1 \to 2$ (2), $2 \to 3$ (2), $3 \to 1$ (2). The loop has the least total weight, 3, but mean 3; the triangle has total 6 and mean 2, which is the minimum mean.

**Negative weights.** Arcs $0 \to 1$ (weight $-5$) and $1 \to 0$ (3), and a self-loop at 2 of weight $-1$. The 2-cycle has mean $-1$ and the loop has mean $-1$, so $\lambda^* = -1$ and both cycles are optimal. Since $\lambda^* < 0$, the graph has a [negative cycle](/negative-cycle/).

**No cycle.** A directed acyclic graph, for example arcs $0 \to 1$ and $1 \to 2$ with an isolated vertex 3, has no cycle and no answer.

**Parallel arcs.** Two arcs $0 \to 1$ of weights 5 and 1, and $1 \to 0$ of weight 1. A cycle uses one arc of each pair, so the best cycle uses the arc of weight 1 and has mean 1.

## Known algorithms

- **Karp's algorithm, $O(nm)$.** A table of least walk weights with exactly $k$ arcs, $k = 0, \ldots, n$, and the formula $\lambda^* = \min_v \max_k (D_n(v) - D_k(v))/(n - k)$. See [Karp's minimum mean cycle algorithm](/karp-minimum-mean-cycle/).
- **Search on $\lambda$.** $\lambda^* < \lambda$ if and only if the weights $w - \lambda$ have a negative cycle. A binary search with a [negative cycle detection](/negative-cycle-detection/) test by Bellman-Ford takes $O(nm \log(nW))$ time for integer weights with absolute value at most $W$, because two different cycle means differ by at least $1/n^2$.
- **Parametric shortest paths, $O(nm + n^2 \log n)$.** Young, Tarjan and Orlin (1991) follow the shortest path tree as $\lambda$ grows.
- **Howard's policy iteration.** Each vertex picks one outgoing arc, the cycles of this choice are evaluated, and the choice is improved. No polynomial bound is known in general, but in Dasdan's experiments (2004) it was among the fastest; see [policy iteration](/policy-iteration/).
- **Brute force.** Enumerate all simple cycles, for example with [Johnson's algorithm](/johnson-elementary-cycles-algorithm/). Exponential in the worst case, and useful only as a test oracle.

## Bounds

- **Upper bound.** $O(nm)$ by Karp's algorithm, and $O(nm + n^2 \log n)$ by parametric shortest paths, which is also $O(nm)$ when $m \ge n \log n$.
- **Lower bound.** Every arc must be read in the worst case, so $\Omega(n + m)$. No better lower bound is known.
- **Strongly polynomial.** Karp's bound does not depend on the weights, which is why the minimum mean cycle canceling algorithm for minimum cost flow is strongly polynomial (Goldberg and Tarjan, 1989).
- **Value.** With integer weights, $\lambda^*$ is a fraction $p/q$ with $1 \le q \le n$, so it is computed exactly with rational arithmetic.

## Reductions

- **To negative cycle detection.** For a fixed $\lambda$, deciding $\lambda^* < \lambda$ is the same as finding a negative cycle with weights $w - \lambda$, and deciding $\lambda^* \le \lambda$ is the same as finding a cycle of weight at most 0.
- **From negative cycle detection.** $G$ has a negative cycle if and only if $\lambda^* < 0$, so the minimum mean cycle is at least as hard as negative cycle detection.
- **To each strongly connected component.** $\lambda^*(G)$ is the minimum of $\lambda^*$ over the strongly connected components that contain a cycle.
- **Weights shift.** Adding a constant $c$ to every weight adds $c$ to every cycle mean and does not change the optimal cycles. So one may assume $\lambda^* = 0$ in proofs, as Karp's proof does.

## Applications

- **Minimum cost flow.** The algorithm of Goldberg and Tarjan cancels a minimum mean cycle of the residual graph in each step, and gets a strongly polynomial bound; see [cycle canceling](/cycle-canceling/) and the [minimum cost flow problem](/min-cost-flow-problem/).
- **Periodic schedules and circuits.** In a cyclic schedule or a synchronous circuit, the largest mean cycle of the delay graph is the shortest possible period, or the clock period limited by loops.
- **Discrete event systems.** The cycle time of a timed event graph is a maximum cycle mean, computed in the max-plus algebra.
- **Games and Markov decision processes.** The value of a one-player mean payoff game is a minimum or maximum cycle mean.
- **Feasibility of difference constraints with a slack.** The largest $\lambda$ such that the constraints $x_v - x_u \le w(u, v) - \lambda$ are feasible is $\lambda^*$.

## References
