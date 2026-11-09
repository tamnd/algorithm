---
tag: 0DD3FW
kind: technique
slug: branch-and-price
name: Branch-and-price
aliases:
- column generation inside branch-and-bound
- branch and price
area: optimization/integer-programming
level: advanced
summary: Branch-and-bound where the LP at each node is solved by column generation.
prereqs: [column-generation, dantzig-wolfe-decomposition, land-doig-algorithm, reduced-cost]
see_also: [branch-and-cut, column-generation, dantzig-wolfe-decomposition, cutting-stock-problem, vehicle-routing-problem, generalized-assignment-problem, graph-coloring, lagrangian-relaxation]
sources:
  - paper: doi:10.1287/opre.46.3.316
    title: Cynthia Barnhart, Ellis L. Johnson, George L. Nemhauser, Martin W. P. Savelsbergh and Pamela H. Vance, Branch-and-price, column generation for solving huge integer programs, Operations Research 46(3), 1998
    locator: pp. 316 to 329 (the method, why standard branching fails, branching rules compatible with pricing)
  - paper: "David M. Ryan and Brian A. Foster, An integer programming approach to scheduling, in Computer Scheduling of Public Transport, North-Holland, 1981, 269 to 280"
    locator: the branching rule on pairs of rows for set partitioning masters
  - paper: "Anuj Mehrotra and Michael A. Trick, A column generation approach for graph coloring, INFORMS Journal on Computing 8(4), 1996, 344 to 354"
    locator: the independent set master for vertex coloring and branching by merging vertices or adding an edge
  - paper: "Jacques Desrosiers and Marco E. Lübbecke, A primer in column generation, in Column Generation, Springer, 2005, 1 to 32"
    locator: the restricted master, pricing, lower bounds during column generation, and branching on original variables
---

Branch-and-price is [branch and bound](/land-doig-algorithm/) for integer programs with a huge number of columns, in which the LP relaxation at every node is solved by [column generation](/column-generation/). The master problem usually comes from a [Dantzig-Wolfe decomposition](/dantzig-wolfe-decomposition/) and has one column per feasible pattern, route or schedule. The main difficulty is branching: the branching rule must keep the pricing problem solvable at every node, so it usually acts on the original variables or on pairs of rows instead of on single master columns.

## In plain words

Some problems are easiest to write as a choice among patterns, such as the routes of trucks or the ways to cut one roll of paper. There are far too many patterns to list, so the solver keeps a short list and asks a separate routine, the pricing step, for a new pattern that would improve the fractional answer. When no such pattern exists, the fractional answer for all patterns is known, and it gives a bound.

Branch-and-price does this at every part of a branch and bound search. The care is in how it splits a part in two. If it said "do not use this pattern", the pricing step would often just find the same pattern again. So it splits on a decision that the pricing step can respect, such as "these two items go together" or "these two items stay apart".

## When it applies

- An integer program whose LP relaxation is a master problem $\min\{\sum_{j} c_j \lambda_j : \sum_j a_j \lambda_j \ge b,\ \lambda \ge 0\}$ over a set of columns $a_j$ that is too large to list, with $\lambda$ integer in the problem to be solved.
- A pricing routine: given dual values $\pi$, it finds a column with negative [reduced cost](/reduced-cost/) $c_j - \pi^\top a_j$, or proves that none exists. Typical pricing problems are knapsack problems, shortest paths with resource constraints, and maximum weight independent sets.
- A branching rule whose branches can be enforced inside the pricing problem, so that pricing stays a problem of the same kind at every node.
- The relaxation is worth the effort. The master LP bound equals the Lagrangian bound for the constraints kept in the master, so it is at least as strong as the LP bound of the compact formulation. It can be strictly stronger only when the LP relaxation of the pricing problem has fractional vertices.

## The template

The holes are SELECT-NODE, PRICE, BRANCH and HEURISTIC. The problem is a minimization with integer costs, and a node $N$ is the root plus a list of branching decisions.

```pseudo id=main
BRANCH-AND-PRICE(master, PRICE)
L1  z* ← +∞;  L ← { root }
L2  while L is not empty do
L3      N ← SELECT-NODE(L);  remove N from L
L4      R ← columns that satisfy the decisions of N, plus artificial columns of high cost
L5      loop
L6          solve the restricted master LP of N over R; let λ̄ be optimal and π its duals
L7          a ← PRICE(π, N)                        ▷ a column allowed at N with c_a − π a < 0, or none
L8          if a is none then exit the loop
L9          R ← R ∪ { a }
L10     v ← value of λ̄                            ▷ the master LP value of N over all allowed columns
L11     if λ̄ uses an artificial column or ⌈v⌉ ≥ z* then discard N; continue at L2
L12     if λ̄ is integral then z* ← v; record λ̄; discard N; continue at L2
L13     update z* with HEURISTIC(R, N)             ▷ e.g. the integer program over the columns in R
L14     add the children BRANCH(N, λ̄) to L         ▷ decisions that PRICE can respect
L15 return z* and the recorded solution
```

**Why the answer is right.** The loop at lines L5 to L9 ends only when PRICE finds no column of negative reduced cost among the columns allowed at $N$. Then the duals $\pi$ are feasible for the dual of the master LP over all these columns, and $v$ equals the optimum of that LP, by [LP duality](/lp-duality/). This LP contains every integer solution of $N$, so $v$ is a lower bound, and with integer costs so is $\lceil v \rceil$. A node is discarded only if it is infeasible (an artificial column is still needed, with costs large enough), cannot beat $z^*$, or has been solved. BRANCH must split the integer solutions of $N$ among the children and remove $\bar\lambda$ from each child, so the search covers every solution and the tree is finite when the number of possible decisions is finite.

**Why branching on a master variable is a bad rule.** The branch $\lambda_j \le \lfloor \bar\lambda_j \rfloor$ forbids or limits column $j$. The pricing routine must then avoid returning $j$, which turns a knapsack or shortest path problem into a problem of finding the second best solution, and deeper in the tree the $k$-th best. The branch $\lambda_j \ge \lceil \bar\lambda_j \rceil$ fixes much of the solution, while the other branch changes almost nothing, so the tree is unbalanced.

**The Ryan-Foster rule.** For a set partitioning master, in which each $a_j$ is the incidence vector of a set $S_j$ and every row must be covered exactly once, a fractional $\bar\lambda$ always has two rows $r \ne s$ with
$$0 < \sum_{j : r, s \in S_j} \bar\lambda_j < 1.$$
*Proof.* Take $k$ with $\bar\lambda_k$ fractional and a row $r \in S_k$. Row $r$ is covered exactly once, so some $\ell \ne k$ has $r \in S_\ell$ and $\bar\lambda_\ell > 0$. The sets are different, so some row $s$ lies in exactly one of $S_k$ and $S_\ell$. The sum over the sets that contain both $r$ and $s$ includes one of $\bar\lambda_k$ and $\bar\lambda_\ell$, so it is positive. It is at most the sum over the sets that contain $r$, which is 1, minus the other one, so it is less than 1. $\square$

The branches are "$r$ and $s$ are in the same set" and "$r$ and $s$ are in different sets". Both are conditions on a single column, so pricing respects them by changing its own problem, and every integer solution falls in one branch.

**Example.** Color the 5-cycle with vertices $0, \dots, 4$ and edges $\{i, i+1 \bmod 5\}$ with as few colors as possible. The master has one column per independent set $S$, with cost 1, and the rows say that each vertex is covered. PRICE solves a maximum weight independent set problem with weights $\pi$, and a column has negative reduced cost when its weight is more than 1. The trace starts with the five single vertices.

| round | LP value | duals $\pi$ | column found | weight |
|---|---|---|---|---|
| 0 | 5 | $(1, 1, 1, 1, 1)$ | $\{0, 2\}$ | 2 |
| 1 | 4 | $(1, 1, 0, 1, 1)$ | $\{0, 3\}$ | 2 |
| 2 | 4 | $(0, 1, 1, 1, 1)$ | $\{1, 3\}$ | 2 |
| 3 | 3 | $(1, 1, 0, 0, 1)$ | $\{1, 4\}$ | 2 |
| 4 | 3 | $(0, 0, 1, 1, 1)$ | $\{2, 4\}$ | 2 |
| 5 | $\tfrac52$ | $(\tfrac12, \tfrac12, \tfrac12, \tfrac12, \tfrac12)$ | none | 1 |

The LP optimum puts $\tfrac12$ on each of the five sets $\{i, i+2\}$, and the bound is $\lceil \tfrac52 \rceil = 3$. The integer program over the columns in $R$ finds the coloring $\{0, 2\}, \{1, 3\}, \{4\}$ with 3 colors, so the root node is solved without branching. If a gap had remained, the Ryan-Foster rule could branch on the rows 0 and 2, whose sum is $\tfrac12$: in one child, vertices 0 and 2 are merged into one vertex, and in the other an edge between them is added. Both children are again coloring problems, so PRICE does not change.

## Classic examples

- **Cutting stock and bin packing.** Columns are cutting patterns of one roll and pricing is a [knapsack problem](/knapsack-problem/), as in the column generation of Gilmore and Gomory. In the [cutting stock problem](/cutting-stock-problem/) the master LP bound is very close to the integer optimum in practice.
- **Vehicle routing.** Columns are routes of one vehicle and pricing is a shortest path problem with resource constraints. Branching is on the arcs of the original graph. Most exact codes for the [vehicle routing problem](/vehicle-routing-problem/) also add cuts, which gives branch-cut-and-price.
- **Generalized assignment.** Savelsbergh (1997) used one column per feasible assignment of jobs to one machine, with a knapsack pricing problem, and branched on the original assignment variables of the [generalized assignment problem](/generalized-assignment-problem/).
- **Vertex coloring.** Mehrotra and Trick (1996) used independent sets as columns and branched by merging two vertices or adding an edge, as in the example. See [graph coloring](/graph-coloring/).
- **Crew scheduling.** Airline crew pairing and rostering problems have set partitioning masters whose columns are pairings or rosters; this is where the Ryan-Foster rule comes from.

## Variations

- **Branching on original variables.** For a Dantzig-Wolfe master, $x = \sum_j \lambda_j x^j$ maps the master solution back to the compact variables. If some $x_e$ is fractional, the branches $x_e \le \lfloor \bar x_e \rfloor$ and $x_e \ge \lceil \bar x_e \rceil$ are bounds in the pricing problem.
- **Early termination with a Lagrangian bound.** If PRICE returns the most negative reduced cost $\bar c$ and every solution uses at most $K$ columns, then $v_R + K \bar c$ is a lower bound, where $v_R$ is the value of the restricted master. A node can be pruned before column generation ends, which helps against tailing off. The bound is the [Lagrangian relaxation](/lagrangian-relaxation/) bound at $\pi$.
- **Dual stabilization.** The duals of the restricted master jump between rounds. Stabilized methods keep the duals near a center point, which reduces the number of rounds.
- **Branch-cut-and-price.** Cuts are added to the master. Cuts in the original variables keep the pricing problem; cuts on the master variables, such as subset row cuts, change it and need care in PRICE.
- **Price-and-branch.** Column generation runs only at the root, and branch and bound then works on the fixed column set. This is a heuristic, because columns needed for the optimum may be missing.

## Pitfalls

- **Heuristic pricing as a bound.** If PRICE is a heuristic and returns no column, columns of negative reduced cost may still exist, and $v$ is not a lower bound. Use heuristic pricing first and exact pricing before the node is discarded.
- **Branching on master variables.** It makes PRICE harder at every depth and gives unbalanced trees, as explained above.
- **Infeasible restricted masters.** At a node, the inherited columns may not satisfy the new decisions. Without artificial columns or a Farkas pricing step, the restricted master looks infeasible although the node is not.
- **Tailing off.** The last rounds of column generation often improve the LP value very little. A Lagrangian bound or stabilization ends them early.
- **Symmetry.** If identical vehicles or machines get separate subproblems, many master solutions describe the same plan. Aggregate identical subproblems into one, with a convexity row equal to their number.

## Exercises

1. In the example, show that $\pi = (\tfrac12, \dots, \tfrac12)$ is optimal for the dual of the full master LP, by checking that no independent set of the 5-cycle has more than two vertices.
2. Write the two children of the Ryan-Foster branch on rows 0 and 2 of the example as coloring problems, and give the master LP value of each.
3. Prove that with the Ryan-Foster rule every path in the tree has length at most $\binom{m}{2}$, where $m$ is the number of rows.
4. Show that branching on $\lambda_j \le 0$ in a cutting stock master makes the pricing problem "find the best knapsack solution different from pattern $j$". Give a small instance where the best and second best patterns differ in value.
5. Derive the Lagrangian bound $v_R + K \bar c$ from weak duality.

## References
