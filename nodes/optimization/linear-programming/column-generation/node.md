---
tag: HBS1E6
kind: technique
slug: column-generation
name: Column generation
aliases:
- Dantzig-Wolfe column generation
- delayed column generation
- pricing out columns
area: optimization/linear-programming
level: advanced
summary: Solve a restricted master LP and price in new columns with a subproblem, avoiding explicit enumeration.
prereqs: [revised-simplex-method, reduced-cost, lp-duality]
see_also: [dantzig-wolfe-decomposition, cutting-stock-problem, branch-and-price, separation-oracle, lagrangian-relaxation, unbounded-knapsack, revised-simplex-method, vehicle-routing-problem]
sources:
  - paper: doi:10.1287/opre.9.6.849
    title: P. C. Gilmore and R. E. Gomory, A linear programming approach to the cutting-stock problem, Operations Research 9(6), 1961
    locator: pages 849 to 859, the pattern formulation and the knapsack pricing problem
  - paper: doi:10.1287/opre.11.6.863
    title: P. C. Gilmore and R. E. Gomory, A linear programming approach to the cutting stock problem, Part II, Operations Research 11(6), 1963
    locator: pages 863 to 888, computational experience and the early termination of the column generation
  - paper: doi:10.1287/opre.1050.0234
    title: Marco E. Lübbecke and Jacques Desrosiers, Selected topics in column generation, Operations Research 53(6), 2005
    locator: pages 1007 to 1023, the restricted master, pricing, lower bounds, tailing off and dual stabilization
  - paper: doi:10.1287/opre.38.5.922
    title: A. A. Farley, A note on bounding a class of linear programming problems, including cutting stock problems, Operations Research 38(5), 1990
    locator: pages 922 to 923, the lower bound from the pricing value
  - paper: doi:10.1007/0-387-25486-2_1
    title: Jacques Desrosiers and Marco E. Lübbecke, A primer in column generation, in Column Generation, Springer, 2005
    locator: pages 1 to 32, the template, the Lagrangian bound and the link with Dantzig-Wolfe decomposition
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 13, The cutting-stock problem (delayed column generation with a knapsack pricing problem)
---

Column generation is a way to solve a linear program with too many columns to write down. It keeps a small *restricted master problem* with a few of the columns, solves it, and uses its dual solution to ask a *pricing problem* for a column with negative [reduced cost](/reduced-cost/). If the pricing problem finds one, the column joins the master problem; if not, the current solution is optimal for the full program. It is the [revised simplex method](/revised-simplex-method/) with the choice of the entering column done by an optimization problem instead of a scan, and it is the engine of [Dantzig-Wolfe decomposition](/dantzig-wolfe-decomposition/) and of [branch-and-price](/branch-and-price/).

## In plain words

Some problems have a huge number of possible building blocks, for example every way to cut a long roll of paper into shorter pieces. Listing all of them is impossible, but most of them are useless.

Column generation starts with a handful of building blocks and finds the best way to combine them. The solution comes with a price for each requirement, which says how much meeting one more unit of it is worth. Then the method asks a separate question: is there a block, among all the blocks not yet listed, whose value at these prices is more than its cost? A smart search answers this without listing the blocks. If such a block exists, it is added and the process repeats. If none exists, the current combination is the best possible.

## When it applies

- **The master problem.** A linear program minimize $\sum_{a \in \mathcal{A}} c_a \lambda_a$ subject to $\sum_{a \in \mathcal{A}} a \lambda_a \ge b$ (or $= b$), $\lambda \ge 0$, where each column $a \in \mathbb{R}^m$ is a combinatorial object (a cutting pattern, a route, a schedule, a path) and the set $\mathcal{A}$ is very large, often exponential in the input size.
- **The pricing problem.** For a dual vector $y$, an algorithm that finds $\min_{a \in \mathcal{A}} (c_a - y^\top a)$ and a column that attains it, faster than a scan of $\mathcal{A}$. Typical pricing problems are knapsack problems, shortest paths with side constraints, and other combinatorial optimization problems.
- **Few rows.** The number of rows $m$ is moderate, so that each restricted master problem is easy, and an optimal basis has at most $m$ positive columns.

## The template

```pseudo id=main
COLUMN-GENERATION(c, b, PRICE)         ▷ min c^T λ, Σ a λ_a ≥ b, λ ≥ 0 over all columns a in 𝒜
L1  S ← a small set of columns that makes the restricted master feasible (or artificial columns with a large cost)
L2  loop
L3      solve the restricted master min Σ_{a∈S} c_a λ_a, Σ_{a∈S} a λ_a ≥ b, λ ≥ 0
L4      (λ*, y*) ← an optimal primal solution and an optimal dual solution of L3
L5      (a, κ) ← PRICE(y*)              ▷ a column with the least reduced cost κ = c_a − y*^T a
L6      if κ ≥ 0 then return λ*         ▷ y* is dual feasible for all of 𝒜, so λ* is optimal
L7      S ← S ∪ {a}                      ▷ re-solve L3 from the previous basis: a enters it
```

**Why it is correct.** At L6, $c_a - y^{*\top} a \ge 0$ for every $a \in \mathcal{A}$, and $y^* \ge 0$ because $y^*$ is dual optimal for the restricted master with $\ge$ rows. So $y^*$ is feasible for the dual of the full master problem. Its value $b^\top y^*$ equals the value of $\lambda^*$, so by [weak duality](/weak-duality/) $\lambda^*$, extended by zeros, is optimal for the full master.

**Why it stops.** Every column already in $S$ has reduced cost at least $0$ at an optimal dual solution of the restricted master, so a column with $\kappa < 0$ is new. $S$ grows at each round, so the method stops after at most $|\mathcal{A}|$ rounds; in practice far fewer are needed. With the old basis kept in L7, each round is a few pivots of the primal simplex method.

**Lower bounds on the way.** If every column has $c_a = 1$ and $y^* \ge 0$, let $v = \max_a y^{*\top} a = 1 - \kappa$. Then $y^*/v$ is dual feasible for the full master, so the optimal value $z^*$ satisfies $z^* \ge z_{\text{RMP}} / v$ (Farley, 1990). In general, if some $K$ bounds $\sum_a \lambda_a$ at an optimum, then $z^* \ge z_{\text{RMP}} + K\kappa$, the Lagrangian bound. These bounds allow an early stop with a known gap.

## Classic examples

**Cutting stock (Gilmore and Gomory, 1961).** Rolls of width $W = 100$ must be cut into $97$ pieces of width $45$, $610$ of width $36$, $395$ of width $31$ and $211$ of width $14$, with as few rolls as possible. A column is a cutting pattern $a \in \mathbb{Z}_{\ge 0}^4$ with $45a_1 + 36a_2 + 31a_3 + 14a_4 \le 100$, of cost $1$. The pricing problem is the [unbounded knapsack problem](/unbounded-knapsack/) $\max\{ y^\top a : w^\top a \le 100,\ a \in \mathbb{Z}_{\ge 0}^4\}$, solved by dynamic programming over the width. Start with the four one-width patterns $(2,0,0,0)$, $(0,2,0,0)$, $(0,0,3,0)$ and $(0,0,0,7)$:

| round | master value | duals $y^*$ | best pattern | $y^{*\top} a$ | Farley bound |
|---|---|---|---|---|---|
| 0 | $21643/42 \approx 515.31$ | $(1/2, 1/2, 1/3, 1/7)$ | $(0, 2, 0, 2)$ | $9/7$ | $400.80$ |
| 1 | $2911/6 \approx 485.17$ | $(1/2, 1/2, 1/3, 0)$ | $(0, 1, 2, 0)$ | $7/6$ | $415.86$ |
| 2 | $1809/4 = 452.25$ | $(1/2, 1/2, 1/4, 0)$ | none better than $1$ | $1$ | $452.25$ |

After two new columns no pattern has value above $1$, so $452.25$ is the LP optimum, with $48.5$ rolls of $(2,0,0,0)$, $100.75$ of $(0,2,0,0)$, $105.5$ of $(0,2,0,2)$ and $197.5$ of $(0,1,2,0)$. Rounding these down gives $450$ rolls that leave $1$, $3$, $1$ and $1$ pieces of the four widths, and [first fit decreasing](/first-fit-decreasing/) packs these into $3$ more rolls: $453$ rolls, which is optimal since every solution needs at least $\lceil 452.25 \rceil = 453$.

**Dantzig-Wolfe decomposition.** For a program with linking constraints and independent blocks, the columns are the vertices of the block polyhedra, and pricing is a small LP over one block. See [Dantzig-Wolfe decomposition](/dantzig-wolfe-decomposition/).

**Routing and scheduling.** In [vehicle routing](/vehicle-routing-problem/) and crew scheduling, the master problem is a set partitioning program over feasible routes or duties, and pricing is a [shortest path with resource constraints](/constrained-shortest-path/) on a time-expanded network, with the duals as negative arc costs.

**Multicommodity flow.** In the path formulation, a column is a path for one commodity, and the pricing problem is a shortest path for each commodity with arc lengths $c_e - y_e$ (the duals of the capacity rows are $y_e \le 0$), solvable by [Dijkstra's algorithm](/dijkstra/).

**Graph coloring.** A column is an independent set of the graph, the master covers every vertex, and pricing is a maximum weight independent set with the duals as weights, which is NP-hard but small in practice.

## Variations

- **Branch-and-price.** To get integer solutions, put column generation in every node of a branch-and-bound tree. The branching rules must keep the pricing problem tractable; see [branch-and-price](/branch-and-price/).
- **Many columns per round.** Return all columns with negative reduced cost that the pricing algorithm finds, not only the best, to cut the number of master solves.
- **Heuristic pricing.** Use a fast heuristic first and call the exact pricing only when the heuristic finds nothing; only the exact call can prove optimality.
- **Dual stabilization.** Keep the duals near a stability center with a penalty or a box, or use a convex combination of the current and the best duals. This reduces the oscillation of $y^*$ that causes slow convergence.
- **Cutting planes on the dual.** Column generation on the primal is Kelley's [cutting-plane method](/cutting-plane-method/) on the dual: each new column is a dual constraint that the current dual point violates, so pricing is the [separation problem](/separation-oracle/) of the dual.
- **Lagrangian view.** The pricing value gives the bound of a [Lagrangian relaxation](/lagrangian-relaxation/) of the linking rows, and the optimal master value equals the best such bound.

## Pitfalls

- **Tailing off.** The master value falls fast at first and then very slowly, with many rounds that improve it little. Stop early with the Farley or Lagrangian bound when the gap is small enough, as Gilmore and Gomory did.
- **Degeneracy.** The restricted master problem is often highly [degenerate](/lp-degeneracy/), so a new column can enter with step $0$ and the value does not move. The dual solution is then not unique, and an unlucky choice of $y^*$ gives poor columns.
- **The LP value is a bound, not an answer.** The final $\lambda^*$ is fractional. Rounding up can cost up to $m$ extra columns (a basic solution has at most $m$ positive entries), and a good integer solution needs branch-and-price or a repair heuristic.
- **Exact pricing at the end.** If pricing is a heuristic, a failure to find a column proves nothing. The last round must use an exact algorithm, or the claimed LP value can be wrong.
- **Tolerances.** In floating point, a reduced cost of $-10^{-9}$ can be noise. A loose tolerance stops too early, and a tight one can loop on columns that do not improve the value.
- **The start.** The first restricted master must be feasible. Artificial columns with a large cost, or trivial columns such as one-width patterns, fix this.

## Exercises

1. Prove the Farley bound: if all costs are $1$, $y^* \ge 0$ and $v = \max_a y^{*\top} a > 0$, then $z^* \ge b^\top y^* / v$. Check the three Farley bounds in the cutting-stock table.
2. With the duals $y = (1/2, 1/2, 1/4, 0)$ of the last round, show that no pattern of width at most $100$ has $y^\top a > 1$.
3. Show that a basic optimal solution of the cutting-stock master has at most $4$ fractional columns here, and deduce that rounding up costs at most $4$ extra rolls.
4. For the path formulation of multicommodity flow, write the dual of the restricted master and show that the pricing problem is a shortest path problem with nonnegative lengths.
5. Prove that column generation on a program is the same computation as Kelley's cutting-plane method on its dual: match the restricted master, the pricing step and the stop rule with the steps of the cutting-plane method.
6. Build a small program where the restricted master has two dual optimal solutions, one that makes pricing return a useful column and one that makes it return a column that enters with step $0$.

## References
