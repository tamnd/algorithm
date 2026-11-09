---
tag: JCC0TF
kind: technique
slug: lift-and-project
name: Lift-and-project
aliases:
- Balas-Ceria-Cornuéjols cut generation
- lift-and-project cut
- sequential convexification
area: optimization/integer-programming
level: research
summary: Generates disjunctive cuts by solving an LP in a lifted higher-dimensional space.
prereqs: [disjunctive-cut, binary-integer-programming, lp-duality]
see_also: [disjunctive-cut, gomory-mixed-integer-cut, semidefinite-programming, binary-integer-programming, chvatal-gomory-finite-convergence, ideal-formulation, branch-and-cut, cutting-plane-method-integer-programming]
sources:
  - paper: "Egon Balas, Sebastián Ceria and Gérard Cornuéjols, A lift-and-project cutting plane algorithm for mixed 0-1 programs, Mathematical Programming 58 (1993), 295 to 324"
    locator: the lift-and-project procedure, the cut generating LP and the cutting plane algorithm
  - paper: "Egon Balas, Sebastián Ceria and Gérard Cornuéjols, Mixed 0-1 programming by lift-and-project in a branch-and-cut framework, Management Science 42 (1996), 1229 to 1246"
    locator: lift-and-project cuts inside branch and cut
  - paper: "Egon Balas, Disjunctive programming, Annals of Discrete Mathematics 5 (1979), 3 to 51"
    locator: the sequential convexification theorem for facial disjunctive programs
  - paper: "László Lovász and Alexander Schrijver, Cones of matrices and set-functions and 0-1 optimization, SIAM Journal on Optimization 1 (1991), 166 to 190"
    locator: the N and N+ operators
  - paper: "Hanif D. Sherali and Warren P. Adams, A hierarchy of relaxations between the continuous and convex hull representations for zero-one programming problems, SIAM Journal on Discrete Mathematics 3 (1990), 411 to 430"
    locator: the Sherali-Adams hierarchy
  - paper: "Egon Balas and Michael Perregaard, A precise correspondence between lift-and-project cuts, simple disjunctive cuts, and mixed integer Gomory cuts for 0-1 programming, Mathematical Programming 94 (2003), 221 to 245"
    locator: computing lift-and-project cuts by pivoting in the original tableau
---

Lift-and-project is a way to compute [disjunctive cuts](/disjunctive-cut/) for 0/1 variables. Pick a binary variable $x_j$ with a fractional LP value. Multiply every constraint by $x_j$ and by $1 - x_j$, which lifts the problem to a space with product variables. Use $x_j^2 = x_j$ to make the lifted system linear, and then project back to the original space. The projection is the convex hull of the two sides of the branch on $x_j$, and a cut that separates the LP point from it comes from a linear program. Balas, Ceria and Cornuéjols (1993) turned this into a practical cutting plane algorithm. The same lifting idea, applied with more products at once, gives the Sherali-Adams and Lovász-Schrijver hierarchies.

## In plain words

If a yes-or-no variable is $0.5$ in the relaxed answer, the solver could branch: solve once with the variable at 0 and once at 1. Lift-and-project does the work of this branch but keeps the result as one new linear rule.

It multiplies each rule of the problem by the variable, and by one minus the variable. The products are new unknowns, so the problem lives in a bigger space for a moment. One fact makes this useful: a yes-or-no variable times itself is the same variable. With that fact, the bigger problem describes exactly the points that are a mix of a "0" answer and a "1" answer. Projecting back to the original unknowns gives a smaller region, and a cut that removes the fractional point.

## When it applies

- Mixed 0/1 programs: $P = \{x : Ax \le b\}$ with the bounds $0 \le x_j \le 1$ among the rows for every binary $x_j$, and integrality only on these variables.
- An LP point $x^*$ with $0 < x^*_j < 1$ for some binary $x_j$.
- The cut is worth its cost when cheaper cuts, such as [GMI cuts](/gomory-mixed-integer-cut/), stall. The cut generating LP is about twice the size of the original LP, unless the tableau method of Balas and Perregaard is used.

## The template

```pseudo id=main
LIFT-AND-PROJECT(A, b, x*, j)                      ▷ 0 < x*_j < 1, x_j binary
L1  lift: multiply each row a_i x ≤ b_i by x_j and by (1 − x_j)
L2  linearize: replace x_j x_k by y_k for k ≠ j, and x_j² by x_j
        this gives M_j = { (x, y) : A y ≤ b x_j,  A (x − y) ≤ b (1 − x_j),  y_j = x_j }
L3  project: P_j = { x : (x, y) ∈ M_j for some y }
L4  solve the cut generating LP of the disjunction x_j ≤ 0 or x_j ≥ 1 at x*
L5  if its optimal value is positive then
L6      strengthen the cut with the integrality of other variables (optional)
L7      return the cut α x ≤ β
L8  return NONE                                        ▷ x* ∈ P_j
```

**Why the projection is the convex hull of the branch.** Let $x^1 = y$, $x^0 = x - y$, $\lambda_1 = x_j$ and $\lambda_0 = 1 - x_j$. Then $M_j$ reads

$$A x^1 \le \lambda_1 b, \quad A x^0 \le \lambda_0 b, \quad x = x^0 + x^1, \quad x^1_j = \lambda_1,\ x^0_j = 0, \quad \lambda_0 + \lambda_1 = 1.$$

This is Balas's formulation of $\operatorname{conv}\big((P \cap \{x_j = 0\}) \cup (P \cap \{x_j = 1\})\big)$ from the [disjunctive cut](/disjunctive-cut/) page. If $\lambda_1 > 0$, then $x^1 / \lambda_1 \in P$ with $j$-th entry 1. If $\lambda_1 = 0$, the bound rows $0 \le x_j \le 1$ inside $A$ force $x^1$ to be a recession direction of $P$ with $x^1_j = 0$, and similarly for $\lambda_0$. So $P_j = \operatorname{conv}\big((P \cap \{x_j = 0\}) \cup (P \cap \{x_j = 1\})\big)$ when both sides are nonempty, and in particular every 0/1-feasible point stays in $P_j$. The cut generating LP of line L4 is the dual of the LP that asks whether $x^* \in P_j$.

**Sequential convexification.** Let $B$ be the set of binary variables. Applying the operation once for each $j \in B$, in any order, gives

$$\big(\cdots\big((P_{j_1})_{j_2}\big)\cdots\big)_{j_p} = \operatorname{conv}\{x \in P : x_j \in \{0,1\},\ j \in B\}.$$

This is Balas's theorem for facial disjunctive programs (1979). So $|B|$ rounds of lift-and-project reach the hull of a mixed 0/1 program, while the Chvátal rank of 0/1 polytopes can grow like $n^2$.

**Cost and computation.** The cut generating LP for one variable has about $2m$ multipliers and $n + 1$ cut coefficients, so each cut costs about as much as two LP solves of the original size. Balas and Perregaard (2003) showed that lift-and-project cuts correspond to GMI cuts from bases of the original LP that may be infeasible, and that the cut generating LP can be solved by pivots in the original tableau. This makes the cuts cheap enough for solvers.

**Example.** For the stable set problem on a triangle, let $P = \{x \in [0,1]^3 : x_1 + x_2 \le 1,\ x_1 + x_3 \le 1,\ x_2 + x_3 \le 1\}$ and $x^* = (\tfrac12, \tfrac12, \tfrac12)$. Lift with $j = 1$, writing $y_k$ for $x_1 x_k$.

- $(x_1 + x_2 \le 1) \cdot x_1$ gives $x_1 + y_2 \le x_1$, so $y_2 \le 0$. With $(x_2 \ge 0) \cdot x_1$, that is $y_2 \ge 0$, this gives $y_2 = 0$. In the same way $y_3 = 0$.
- $(x_2 + x_3 \le 1) \cdot (1 - x_1)$ gives $(x_2 - y_2) + (x_3 - y_3) \le 1 - x_1$, so $x_1 + x_2 + x_3 \le 1$.

The projection contains the clique inequality $x_1 + x_2 + x_3 \le 1$, which $x^*$ breaks with left side $\tfrac32$. Here $P \cap \{x_1 = 1\} = \{(1,0,0)\}$ and $P \cap \{x_1 = 0\}$ is the triangle $(0,0,0)$, $(0,1,0)$, $(0,0,1)$, so $P_1$ is the stable set polytope: one step reaches the hull.

## Classic examples

- **Odd cycles.** For the 5-cycle with $x^* = (\tfrac12, \ldots, \tfrac12)$, one step on $x_1$ already removes $x^*$. Both $P \cap \{x_1 = 1\}$ and $P \cap \{x_1 = 0\}$ satisfy $\sum_v x_v \le 2$, because each is a path or a single edge after fixing, so the odd cycle inequality is valid for $P_1$.
- **The BCC algorithm.** Balas, Ceria and Cornuéjols (1993, 1996) solved hard mixed 0/1 instances by rounds of lift-and-project cuts at the root, followed by branch and cut.
- **Tableau-based cuts in solvers.** After Balas and Perregaard (2003), lift-and-project cuts are computed by improving GMI cuts through pivots, for example in the CglLandP generator of COIN-OR.

## Variations

- **Lovász-Schrijver.** Multiply by $x_j$ and $1 - x_j$ for all $j$ at once, with one product matrix $Y$ that must be symmetric. This is the $N$ operator. Asking also that $\begin{pmatrix} 1 & x^T \\ x & Y \end{pmatrix}$ be positive semidefinite gives the $N_+$ operator, a [semidefinite](/semidefinite-programming/) relaxation.
- **Sherali-Adams.** Multiply each row by all products $\prod_{i \in S} x_i \prod_{i \in T} (1 - x_i)$ with $|S| + |T| \le k$. Level $k$ is at least as strong as $k$ rounds of the Lovász-Schrijver $N$ operator, and level $n$ is the 0/1 hull.
- **Lasserre.** Adding semidefinite constraints on the moment matrix of all products gives the Lasserre hierarchy, the strongest of the three.
- **General integers and other disjunctions.** The same lift works for any two-term disjunction $\pi^T x \le \pi_0$ or $\pi^T x \ge \pi_0 + 1$, which gives split cuts, but $x_j^2 = x_j$ no longer holds, and the sequential convexification theorem fails.

## Pitfalls

- **Missing bounds.** The projection argument needs the rows $0 \le x_j \le 1$ in $A$. Without them, $M_j$ can contain points that do not come from the two sides of the branch.
- **Projection by elimination.** Computing $P_j$ explicitly, for example by [Fourier-Motzkin elimination](/fourier-motzkin-elimination/), is far too expensive. Use the cut generating LP, or the tableau method, to find one violated cut.
- **Hierarchy size.** Level $k$ of the Sherali-Adams or Lasserre hierarchy has $n^{O(k)}$ variables. These are tools for proofs and for small hard instances, not for routine cuts.
- **Normalization and numerics.** As for every disjunctive cut, the normalization of the cut generating LP decides which cut is found, and dense cuts with a large range of coefficients should be scaled or rejected.

## Exercises

1. For the 5-cycle example, find multipliers in the lifted system for $j = 1$ that prove $\sum_v x_v \le 2$.
2. Show that $P_j \subseteq P$ and that $P_j$ contains every point of $P$ with $x_j \in \{0, 1\}$.
3. Prove the sequential convexification theorem for two binary variables by applying the two-term result twice.
4. Show that one step of lift-and-project on $x_j$ gives the same polytope as the convex hull of the two branch nodes of branch and bound on $x_j$.

## References
