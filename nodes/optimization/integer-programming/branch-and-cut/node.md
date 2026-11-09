---
tag: VWTP19
kind: technique
slug: branch-and-cut
name: Branch-and-cut
aliases:
- branch and cut
- cut-and-branch
area: optimization/integer-programming
level: advanced
summary: Branch-and-bound in which cutting planes are generated at nodes of the search tree.
prereqs: [land-doig-algorithm, cutting-plane-method-integer-programming, lp-relaxation, dual-simplex-method]
see_also: [branch-and-price, gomory-mixed-integer-cut, cover-inequality, separation-oracle, traveling-salesman-problem, strong-branching, presolve, mixed-integer-programming]
sources:
  - paper: "Manfred Padberg and Giovanni Rinaldi, A branch-and-cut algorithm for the resolution of large-scale symmetric traveling salesman problems, SIAM Review 33(1), 1991, 60 to 100"
    locator: the name branch and cut, cut generation at every node, the cut pool, and local and global validity of cuts
  - paper: "Harlan Crowder, Ellis L. Johnson and Manfred Padberg, Solving large-scale zero-one linear programming problems, Operations Research 31(5), 1983, 803 to 834"
    locator: lifted cover inequalities added at the root before branch and bound (cut-and-branch)
  - paper: "Tobias Achterberg and Roland Wunderling, Mixed integer programming: analyzing 12 years of progress, in Facets of Combinatorial Optimization, Springer, 2013, 449 to 481"
    locator: Section 3.2 and Table 6 (CPLEX 12.5 with cutting planes disabled; the bracket of models that take at least 10 seconds)
  - book: isbn:9780691129938
    title: David L. Applegate, Robert E. Bixby, Vašek Chvátal and William J. Cook, The Traveling Salesman Problem, A Computational Study, Princeton University Press, 2006
    locator: Chapter 5 (the cutting plane loop) and the chapters on branching and the Concorde code (chapter numbers unsure)
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming, Wiley, 1998
    locator: Chapter 9 (strong valid inequalities, and branch and cut, section unsure)
---

Branch-and-cut is LP-based [branch and bound](/land-doig-algorithm/) in which the [LP relaxation](/lp-relaxation/) of each node is made tighter with cutting planes before the node is branched. A node is branched only when the cut loop stops making progress, so the tree is smaller than in plain branch and bound and the LP bound at each node is stronger. Padberg and Rinaldi gave the method its name in 1991 for the traveling salesman problem, and today every general solver for [mixed integer programs](/mixed-integer-programming/) uses it.

## In plain words

Branch and bound splits a problem into smaller problems and uses the fractional relaxation of each one to throw away parts that cannot contain a better answer. A cutting plane is a new rule that every whole-number answer obeys but the current fractional answer breaks.

Branch-and-cut joins the two ideas. At each part of the search, the solver first adds cutting planes to make the fractional relaxation closer to the whole-number problem. This raises or lowers the bound, so more parts can be thrown away. When new cuts stop helping, the solver splits the part in two and continues on each half. Some cuts are true for the whole problem and can be shared. Others use the choices made on the path to the current part and are true only below it.

## When it applies

- A mixed integer program $\max\{c^\top x : A x \le b,\ x \ge 0,\ x_j \in \mathbb{Z} \text{ for } j \in I\}$, with bounded integer variables, whose LP relaxation can be solved.
- One or more separation routines. Each takes a fractional point $\bar{x}$ and returns inequalities valid for the integer points of the current node that $\bar{x}$ breaks, or nothing. General routines give [Gomory mixed integer cuts](/gomory-mixed-integer-cut/), [cover inequalities](/cover-inequality/) and similar families. Problem-specific routines give, for example, subtour elimination constraints for the [traveling salesman problem](/traveling-salesman-problem/). A family can be exponentially large if a [separation oracle](/separation-oracle/) finds its violated members.
- An LP solver that can add rows and change bounds and restart from the last basis, usually the [dual simplex method](/dual-simplex-method/).

## The template

The holes are SELECT-NODE (the [node selection rule](/node-selection-rule/)), SEPARATE (the cut families), STOP-CUTTING (the rule that ends the cut loop) and BRANCH (the [branching rule](/branching-rule/)). Each node $N$ is the original problem with tighter bounds on some integer variables, plus the local cuts of $N$.

```pseudo id=main
BRANCH-AND-CUT(A, b, c, I)                       ▷ max c x over the mixed integer set
L1  pool ← ∅;  z* ← −∞;  x* ← none
L2  L ← { root node with the original bounds }
L3  while L is not empty do
L4      N ← SELECT-NODE(L);  remove N from L
L5      loop
L6          solve the LP of N with the cuts of N and the cuts in pool
L7          if the LP is infeasible or its value is at most z* then discard N; continue at L3
L8          x̄ ← an optimal vertex of the LP
L9          if x̄_j is integral for all j ∈ I then
L10             z* ← c x̄;  x* ← x̄;  discard N; continue at L3
L11         C ← SEPARATE(x̄, N)                     ▷ cuts valid for the integer points of N
L12         if C is empty or STOP-CUTTING(N) then exit the loop
L13         add the globally valid cuts of C to pool and the others to N
L14     (N⁻, N⁺) ← BRANCH(N, x̄)                     ▷ e.g. x_j ≤ ⌊x̄_j⌋ and x_j ≥ ⌈x̄_j⌉
L15     add N⁻ and N⁺ to L, each with the local cuts of N
L16 return x*, z*                                   ▷ x* = none means infeasible
```

**Why the answer is right.** Let $S(N)$ be the set of mixed integer points that satisfy the bounds of node $N$. Every cut of the pool is valid for all of $S(\text{root})$, and every local cut of $N$ is valid for $S(N)$ and so for the sets of its descendants, because $S(N^-) \cup S(N^+) = S(N)$ and both are subsets of $S(N)$. So at line L6 the LP of $N$ contains $S(N)$, and its value is an upper bound on $c^\top x$ over $S(N)$. A node is discarded at line L7 only if $S(N)$ is empty or holds no point better than $z^*$. A node is discarded at line L10 only after its best point, which is $\bar{x}$, has been recorded. Branching at line L14 splits $S(N)$ into two sets that cover it. So, at every moment, every point of $S(\text{root})$ better than $z^*$ lies in $S(N)$ for some $N$ in $L$, and when $L$ is empty, $x^*$ is optimal, or no feasible point exists if $x^*$ is none.

**Why it ends.** STOP-CUTTING must end the loop at each node after finitely many rounds, for example after a fixed number of rounds. Each branching splits the range of one integer variable, and the ranges are bounded, so every path in the tree has finite length and the tree is finite.

**Example.** Take $\max\ x_1 + x_2$ subject to $2x_1 + 2x_2 \le 3$ and $0 \le x_1, x_2 \le 1$ integer. The integer optimum is 1.

| method | node | LP optimum | LP value | action |
|---|---|---|---|---|
| branch and bound | root | $(1, \tfrac12)$ | $\tfrac32$ | branch on $x_2$ |
| | $x_2 \le 0$ | $(1, 0)$ | 1 | integral, $z^* = 1$ |
| | $x_2 \ge 1$ | $(\tfrac12, 1)$ | $\tfrac32$ | branch on $x_1$ |
| | $x_2 \ge 1, x_1 \le 0$ | $(0, 1)$ | 1 | not better, discard |
| | $x_2 \ge 1, x_1 \ge 1$ | none | | infeasible, discard |
| branch-and-cut | root | $(1, \tfrac12)$ | $\tfrac32$ | add the cut $x_1 + x_2 \le 1$ |
| | root | $(1, 0)$ | 1 | integral, $z^* = 1$, done |

The cut is the [Chvátal-Gomory cut](/chvatal-gomory-cut/) obtained from $\tfrac12 (2x_1 + 2x_2 \le 3)$ by rounding down the right side. It holds for every integer point, so it is valid in the whole tree and goes into the pool. Branch-and-cut solves the instance at the root, where plain branch and bound needs five nodes.

## Classic examples

- **Symmetric traveling salesman.** Padberg and Rinaldi separated subtour elimination, comb and other inequalities at every node and kept the cuts in a pool. The Concorde code of Applegate, Bixby, Chvátal and Cook follows the same plan with many more cut families and solved instances with tens of thousands of cities.
- **Zero-one programs.** Crowder, Johnson and Padberg (1983) added lifted cover inequalities for each knapsack row at the root and then ran branch and bound. This form, with cuts only at the root, is called cut-and-branch.
- **General solvers.** Commercial and academic solvers for mixed integer programs separate Gomory mixed integer, mixed integer rounding, cover, flow cover, clique and other cuts, mostly at the root and with fewer rounds deeper in the tree. In the tests of Achterberg and Wunderling (2013), turning off cutting planes in CPLEX 12.5 made the harder models of their test set about 6 times slower on average, and many more models hit the time limit. This is a measured result for one solver and one test set, not a theorem.

## Variations

- **Cut-and-branch.** Cuts are generated only at the root. The LP at each node stays small, at the price of weaker bounds deeper in the tree.
- **Local cuts.** A cut derived with the tighter bounds of a node is valid only in its subtree. It is stored with the node, not in the pool.
- **Cut pool.** Global cuts that become slack are removed from the LP but kept in a pool. SEPARATE first checks the pool, which is cheap, before it calls the expensive routines.
- **Cut selection.** Solvers generate many candidate cuts per round and keep a few, chosen by efficacy (the distance by which the cut separates $\bar{x}$), by the angle to the objective and by the angle to the cuts already chosen.
- **Branch-cut-and-price.** If the LP has too many columns to list, the node LP is also solved by [column generation](/column-generation/), as in [branch-and-price](/branch-and-price/). Cuts then change the pricing problem.

## Pitfalls

- **Local cuts in the global pool.** A cut that uses the bounds of a node, such as a Gomory cut from a node tableau, can remove the optimum if it is applied at other nodes.
- **Tailing off.** The bound gain per round falls fast. Without a STOP-CUTTING rule that measures this gain, the solver spends its time on cut rounds that hardly move the bound.
- **Large LPs.** Every cut adds a row. Dense cuts make each LP solve slower and the basis less stable. Remove cuts that stay slack, and limit the number of cuts per round.
- **Numerical errors.** Cuts computed in floating point arithmetic can be slightly invalid. Solvers scale the cuts, reject cuts with a large ratio between their largest and smallest coefficients, and relax the right side a little.
- **Cuts and branching interact.** A cut that makes the LP optimum integral at one node can also change which variable is fractional. Measurements of a branching rule are therefore not portable between settings with and without cuts.

## Exercises

1. In the example, find the integer optimum and the five nodes of plain branch and bound when the first branch is on $x_1$ instead of $x_2$.
2. Give an inequality that is valid for the node $x_2 \ge 1$ of the example but not for the root. Show which feasible point of the root it removes.
3. Prove that if every node runs at most $r$ cut rounds and every integer variable has range $\{0, \dots, u\}$, the tree has at most $2 (u + 1)^{|I|}$ nodes.
4. Explain why a Gomory mixed integer cut from the optimal tableau of a node, computed with the node bounds, need not be valid at the root.
5. Design a STOP-CUTTING rule that ends the loop when the bound improves by less than a fraction $\varepsilon$ of the gap between the bound and $z^*$ over two rounds. What does it do when $z^* = -\infty$?

## References
