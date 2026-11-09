---
tag: H7E5HR
kind: technique
slug: dantzig-wolfe-decomposition
name: Dantzig-Wolfe decomposition
aliases:
- Dantzig-Wolfe
- Dantzig-Wolfe decomposition
- Dantzig-Wolfe reformulation
- decomposition principle
area: optimization/linear-programming
level: research
summary: Reformulate a block-structured LP with a master problem over extreme points of the subproblems.
prereqs: [column-generation, polyhedron, lp-duality, reduced-cost]
see_also: [column-generation, benders-decomposition, lagrangian-relaxation, lagrangian-duality, branch-and-price, revised-simplex-method, polyhedron, cutting-plane-method]
sources:
  - paper: doi:10.1287/opre.8.1.101
    title: George B. Dantzig and Philip Wolfe, Decomposition principle for linear programs, Operations Research 8(1), 1960
    locator: pages 101 to 111, the master program over extreme points and the subprograms with modified costs
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Chapter 6, Large scale optimization (delayed column generation and Dantzig-Wolfe decomposition, with the bounds on the optimal cost)
  - paper: doi:10.1007/0-387-25486-2_1
    title: Jacques Desrosiers and Marco E. Lübbecke, A primer in column generation, in Column Generation, Springer, 2005
    locator: pages 1 to 32, the reformulation, the Lagrangian bound and the equivalence with Lagrangian relaxation
  - paper: doi:10.1287/opre.1050.0234
    title: Marco E. Lübbecke and Jacques Desrosiers, Selected topics in column generation, Operations Research 53(6), 2005
    locator: pages 1007 to 1023, decomposition of integer programs, convexification and discretization, and stabilization
---

Dantzig-Wolfe decomposition is a way to solve a linear program whose constraints split into independent blocks joined by a few *linking* constraints. It writes every point of each block polyhedron as a convex combination of its vertices, which turns the program into a *master problem* with one variable for each vertex, few rows and a huge number of columns. The master problem is solved by [column generation](/column-generation/): its duals change the costs of each block, and a small LP over each block finds the vertex to add. Dantzig and Wolfe published it in 1960; today it is mostly used to reformulate integer programs, where it gives stronger bounds than the plain LP relaxation.

## In plain words

Think of a company with several factories that share a few resources, such as one budget and one warehouse. Each factory has many rules of its own, but only the shared resources tie the factories together.

The method lets a head office and the factories talk. The head office sets a price on each shared resource. Each factory then plans its best production under its own rules, as if it had to pay these prices, and sends the plan to the head office. The head office mixes the plans it has received so far into the best overall plan that respects the shared limits, and from this mix it computes new prices. When no factory can offer a plan that beats the current mix at the current prices, the mix is optimal for the whole company. The head office never needs to know the rules of the factories.

## When it applies

- **Block-angular structure.** The program is
$$\min \sum_{k=1}^{K} c_k^\top x^k \quad \text{s.t.} \quad \sum_{k=1}^{K} D_k x^k \le b_0, \qquad x^k \in P_k = \{x : A_k x \le b_k,\ x \ge 0\} \ (k = 1, \ldots, K),$$
with $m_0$ linking rows and $K$ blocks with their own constraints. Multicommodity flow, multi-period planning and problems with one block per vehicle, machine or crew have this form.
- **Easy blocks.** Optimizing a linear function over each $P_k$ is much easier than the whole program, because the blocks are small, or because they have a special structure (a shortest path, a knapsack, a flow).
- **Few linking rows.** The master problem has $m_0 + K$ rows instead of $m_0 + \sum_k m_k$, so the reformulation pays off when $m_0$ is small.

**The reformulation.** By the Minkowski-Weyl theorem, each nonempty [polyhedron](/polyhedron/) $P_k$ is the set of convex combinations of its vertices $V_k$ plus nonnegative combinations of its extreme rays $R_k$. Substituting $x^k = \sum_{v \in V_k} \lambda_{kv} v + \sum_{r \in R_k} \mu_{kr} r$ gives the master problem
$$\min \sum_k \Big( \sum_{v} (c_k^\top v) \lambda_{kv} + \sum_{r} (c_k^\top r) \mu_{kr} \Big) \quad \text{s.t.} \quad \sum_k \Big( \sum_v (D_k v) \lambda_{kv} + \sum_r (D_k r) \mu_{kr} \Big) \le b_0, \quad \sum_{v \in V_k} \lambda_{kv} = 1 \ \forall k, \quad \lambda, \mu \ge 0,$$
which has the same optimal value as the original program, and whose solutions map back to optimal $x^k$.

## The template

```pseudo id=main
DANTZIG-WOLFE(c_k, D_k, P_k, b_0)        ▷ K blocks, m_0 linking rows; P_k bounded here
L1  for each block k: S_k ← {one vertex of P_k} (add artificial columns with a large cost if the linking rows fail)
L2  loop
L3      solve the restricted master over the columns S_1, ..., S_K
L4      π ← duals of the linking rows (π ≤ 0); μ_k ← dual of the convexity row of block k
L5      for each block k: v_k ← a vertex minimizing (c_k − D_k^T π)^T x over P_k; κ_k ← (c_k − D_k^T π)^T v_k − μ_k
L6      LB ← z_master + Σ_k min(0, κ_k)            ▷ a lower bound on the optimum
L7      if κ_k ≥ 0 for all k then return x^k = Σ_{v ∈ S_k} λ_{kv} v for each k
L8      add v_k to S_k for every k with κ_k < 0
```

**Why the pricing is right.** The column of a vertex $v$ of block $k$ is $(D_k v, e_k)$ with cost $c_k^\top v$, so its [reduced cost](/reduced-cost/) is $c_k^\top v - \pi^\top D_k v - \mu_k = (c_k - D_k^\top \pi)^\top v - \mu_k$. Its minimum over all vertices is the LP of line L5, because a linear function attains its minimum over a bounded polyhedron at a vertex. If $P_k$ is unbounded and the LP of L5 is unbounded, the pricing returns an extreme ray $r$ with $(c_k - D_k^\top\pi)^\top r < 0$, and the ray column, without a convexity coefficient, enters instead.

**Why the bound holds.** For any $\pi \le 0$, relaxing the linking rows with the multipliers $-\pi$ gives the [Lagrangian](/lagrangian-relaxation/) bound $\pi^\top b_0 + \sum_k \min_{x \in P_k} (c_k - D_k^\top\pi)^\top x \le z^*$. With the dual values of L4, $z_{\text{master}} = \pi^\top b_0 + \sum_k \mu_k$, so this bound is $z_{\text{master}} + \sum_k \kappa_k$ when all $\kappa_k \le 0$, which is line L6. At the stop, all $\kappa_k = 0$ for the best vertices, so the bound equals the master value, and the solution is optimal. Termination follows as for column generation: each added column is new, and each block has finitely many vertices.

## Classic examples

**Two blocks with two linking rows.** Maximize $3x_1 + 2x_2 + 4x_3 + 3x_4$, written as minimize $-3x_1 - 2x_2 - 4x_3 - 3x_4$, subject to the linking rows $x_1 + x_3 \le 4$ and $x_2 + x_4 \le 4$, block 1: $x_1 + x_2 \le 4$, $x_1 \le 3$, and block 2: $x_3 + x_4 \le 5$, $x_3 \le 3$, $x_4 \le 3$, all variables nonnegative. Start with the origin of each block.

| round | master value | $\pi$ | $\mu$ | block 1 vertex, $\kappa_1$ | block 2 vertex, $\kappa_2$ | lower bound |
|---|---|---|---|---|---|---|
| 0 | $0$ | $(0, 0)$ | $(0, 0)$ | $(3, 1)$, $-11$ | $(3, 2)$, $-18$ | $-29$ |
| 1 | $-65/3$ | $(-11/3, 0)$ | $(0, -7)$ | $(0, 4)$, $-8$ | $(2, 3)$, $-8/3$ | $-97/3$ |
| 2 | $-25$ | $(-3, -2)$ | $(0, -5)$ | $(3, 1)$, $0$ | $(2, 3)$, $0$ | $-25$ |

In round 0 the prices are zero, so each block proposes its own best vertex: $(3, 1)$ with value $-11$ and $(3, 2)$ with value $-18$. Together they break the first linking row ($3 + 3 > 4$), so the master mixes $\frac13$ of $(3, 1)$ with $\frac23$ of the origin and prices the first linking row at $-11/3$. In round 2 no block can improve, and the master value $-25$ meets the lower bound. The master solution is $\frac14 (0, 0) + \frac13 (3, 1) + \frac{5}{12} (0, 4) = (1, 2)$ for block 1 and $(3, 2)$ for block 2, so $x = (1, 2, 3, 2)$ with the value $3 + 4 + 12 + 6 = 25$, the optimum of the original program. The point $(1, 2)$ is not a vertex of block 1: the master can choose interior points of the blocks by mixing vertices.

**Multicommodity flow.** Each commodity is a block whose polyhedron is a flow polyhedron, the linking rows are the arc capacities, and pricing is a min-cost flow, or a shortest path when each commodity has one source and one sink. This was one of the first uses, by Ford and Fulkerson, before the general method.

**Integer programs.** For an integer program with block constraints $x^k \in P_k \cap \mathbb{Z}^{n_k}$, use the integer points of $P_k$ as columns. The LP of the master then optimizes over $\operatorname{conv}(P_k \cap \mathbb{Z}^{n_k})$ for each block, and its value equals the [Lagrangian dual](/lagrangian-duality/) bound, which is at least the LP relaxation bound and often much stronger. Cutting stock, vehicle routing, crew scheduling and generalized assignment are solved in this way with [branch-and-price](/branch-and-price/).

## Variations

- **Aggregated and disaggregated masters.** One convexity row per block (disaggregated) gives more columns but a stronger and faster master than one combined row. With $K$ identical blocks, one aggregated block with the row $\sum_v \lambda_v = K$ removes the symmetry.
- **Convexification and discretization.** For integer programs, the master can use the convex hull of the integer points (convexification) or keep integrality on the original variables, or require $\lambda$ integral over the integer points (discretization); these differ when branching.
- **Partial decomposition.** Only some constraints go to the blocks, and the rest stay in the master. The choice decides how strong the bound is and how hard pricing is.
- **Benders decomposition.** [Benders decomposition](/benders-decomposition/) is Dantzig-Wolfe decomposition applied to the dual: it fixes the linking variables instead of pricing the linking rows, and it adds rows instead of columns.
- **Stabilization.** As in column generation, keeping $\pi$ near a good point with a box or a penalty reduces the oscillation of the prices.

## Pitfalls

- **The bound is not monotone.** The Lagrangian bound of line L6 can get worse from one round to the next: in the example it goes from $-29$ to $-97/3$. Keep the best bound seen so far.
- **Slow convergence.** The master value improves fast at first and then slowly, and the prices oscillate. For pure LPs a direct solver is often faster; the decomposition pays off for large structured LPs and for integer programs.
- **Recovering $x$.** The answer is $x^k = \sum_v \lambda_{kv} v$, not one of the vertices, and for integer programs this point can be fractional even when all columns are integral.
- **Unbounded blocks.** If a block polyhedron is unbounded, pricing must return extreme rays, which enter the master without a convexity coefficient. Forgetting them gives a wrong optimum.
- **The start.** The first restricted master must be feasible for the linking rows. Artificial columns with a large cost, or a phase one on the master, handle this.

## Exercises

1. Prove that the master problem and the original program have the same optimal value, using the Minkowski-Weyl theorem for each block.
2. In round 1 of the example, compute the reduced cost of the vertex $(0, 4)$ of block 1 from $\pi = (-11/3, 0)$ and $\mu_1 = 0$, and check that it is $-8$.
3. Check that the lower bound $-97/3$ of round 1 is the Lagrangian bound with multipliers $(11/3, 0)$ on the linking rows, by solving the two block problems directly.
4. Show that if all blocks are identical, the disaggregated master has many optimal solutions that differ only by a permutation of the blocks, and write the aggregated master.
5. Write Benders decomposition for the dual of a block-angular program and show that its cuts correspond to the columns of Dantzig-Wolfe decomposition.
6. For an integer program with one block, give an example where the master LP bound is strictly better than the LP relaxation bound.

## References
