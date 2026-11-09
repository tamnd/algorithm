---
tag: RVD82H
kind: technique
slug: disjunctive-cut
name: Disjunctive cut
aliases:
- Balas disjunctive cut
- split cut
- disjunctive programming cut
area: optimization/integer-programming
level: advanced
summary: Cut valid for the union of two polyhedra obtained by branching on a variable.
prereqs: [lp-duality, farkas-lemma, ideal-formulation, lp-relaxation]
see_also: [lift-and-project, gomory-mixed-integer-cut, mixed-integer-rounding-inequality, ideal-formulation, chvatal-gomory-finite-convergence, cutting-plane-method-integer-programming, branch-and-cut, farkas-lemma]
sources:
  - paper: "Egon Balas, Disjunctive programming, Annals of Discrete Mathematics 5 (1979), 3 to 51"
    locator: the characterization of valid inequalities for a union of polyhedra and the cut generating LP
  - paper: "Egon Balas, Disjunctive programming: properties of the convex hull of feasible points, Discrete Applied Mathematics 89 (1998), 3 to 44"
    locator: the extended formulation of the convex hull of a union of polyhedra (first circulated as a 1974 report)
  - paper: "Egon Balas, Intersection cuts, a new type of cutting planes for integer programming, Operations Research 19 (1971), 19 to 39"
    locator: cuts from a simplex cone and a convex set with no integer point inside
  - paper: doi:10.1007/BF01580858
    title: William Cook, Ravi Kannan and Alexander Schrijver, Chvátal closures for mixed integer programming problems, Mathematical Programming 47, 1990
    locator: split cuts, the split closure is a polyhedron, and a mixed-integer example of infinite split rank
  - paper: "Egon Balas and Robert G. Jeroslow, Strengthening cuts for mixed integer programs, European Journal of Operational Research 4 (1980), 224 to 234"
    locator: monoidal strengthening of disjunctive cuts
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 4 (union of polyhedra) and Chapter 5 (split cuts and intersection cuts)
---

A disjunctive cut is a valid inequality derived from a logical "or" that every feasible point satisfies. The most common case is the split disjunction of branching: an integer variable with a fractional LP value $x^*_j$ satisfies $x_j \le \lfloor x^*_j \rfloor$ or $x_j \ge \lceil x^*_j \rceil$. A cut that is valid for both sides of the split, and that removes $x^*$, is a split cut. Balas built the theory in the 1970s under the name disjunctive programming. It shows that the valid cuts for a union of polyhedra are exactly the solutions of a linear program, the cut generating LP. [Gomory mixed-integer cuts](/gomory-mixed-integer-cut/), [MIR inequalities](/mixed-integer-rounding-inequality/) and [lift-and-project](/lift-and-project/) cuts are all disjunctive cuts.

## In plain words

Branching splits a problem into two smaller problems, for example "$x$ at most 2" and "$x$ at least 3", and solves both. A disjunctive cut uses the same split, but it keeps one problem. It looks for a single linear rule that holds in both halves. Every whole-number answer lies in one of the halves, so it keeps the rule. The fractional answer, with $x = 2.5$, lies in neither half, so a good rule can remove it.

Finding the rule is itself a linear program. For each half, the rule must be a weighted sum of the constraints of that half, with nonnegative weights. The cut generating LP looks for weights for both halves that give the same rule and make the rule cut off the current point by as much as possible.

## When it applies

- The feasible set lies in a union $\bigcup_{k=1}^q D_k$ of polyhedra that is known in advance, and the LP relaxation $P = \{x : Ax \le b\}$ has an optimal point $x^*$ outside $\operatorname{conv} \bigcup_k (P \cap D_k)$.
- Split disjunctions $\pi^T x \le \pi_0$ or $\pi^T x \ge \pi_0 + 1$, with $\pi$ integral on the integer variables, zero on the continuous ones, and $\pi_0 \in \mathbb{Z}$. The variable disjunction $x_j \le \lfloor x^*_j \rfloor$ or $x_j \ge \lceil x^*_j \rceil$ is the case $\pi = e_j$.
- Other logical structure: $x_j \in \{0\} \cup [l_j, u_j]$ for [semicontinuous variables and indicator constraints](/indicator-constraint/), complementarity $x_i x_j = 0$, special ordered sets, and the leaves of a branch and bound tree.
- The cut is worth its cost when the LP of the union is small enough to solve, or when a closed form exists, as for GMI cuts.

## The template

Write the term $k$ as $P_k = P \cap D_k = \{x : A^k x \le b^k\}$, where $A^k x \le b^k$ is $Ax \le b$ together with the constraints of $D_k$.

```pseudo id=main
DISJUNCTIVE-CUT(A, b, D_1, ..., D_q, x*)        ▷ returns a cut α x ≤ β or NONE
L1  for k = 1 to q do
L2      A^k, b^k ← the rows of A x ≤ b together with the rows of D_k
L3  solve the cut generating LP (CGLP) in α, β, u^1, ..., u^q:
        maximize    α·x* − β
        subject to  α = (A^k)^T u^k,  β ≥ (b^k)^T u^k,  u^k ≥ 0   for k = 1, ..., q
                    Σ_k Σ_i u^k_i = 1                                ▷ normalization
L4  if the optimal value is positive then return α x ≤ β
L5  return NONE                                        ▷ x* is in the hull of the union
```

**Why the cut is valid.** Let $x$ be feasible, so $x \in P_k$ for some $k$. Then $\alpha^T x = (u^k)^T A^k x \le (u^k)^T b^k \le \beta$, because $u^k \ge 0$. So $\alpha^T x \le \beta$ holds on every $P_k$, hence on their union and on the convex hull of the union.

**Why no cut is missed.** Assume each $P_k$ is nonempty. By LP duality, an inequality $\alpha^T x \le \beta$ is valid for $P_k$ if and only if there is $u^k \ge 0$ with $\alpha = (A^k)^T u^k$ and $(b^k)^T u^k \le \beta$. So the feasible $(\alpha, \beta)$ of the CGLP, without the normalization, are exactly the inequalities valid for $\bigcup_k P_k$. These are the inequalities valid for the closed convex hull of the union, and $x^*$ lies outside this hull if and only if some of them is violated. The normalization only scales $(\alpha, \beta)$ and keeps the LP bounded. Balas also gave the equivalent primal form: the closed convex hull is the projection onto $x$ of

$$\Big\{(x, x^1, \ldots, x^q, \lambda) : x = \sum_k x^k,\ A^k x^k \le \lambda_k b^k,\ \sum_k \lambda_k = 1,\ \lambda \ge 0\Big\},$$

and the CGLP is the dual of the LP that tests whether $x^*$ lies in this projection. The same formulation is the union formulation on the [ideal formulation](/ideal-formulation/) page.

**Cost.** For a split, $q = 2$ and the CGLP has about twice as many rows and columns as the LP relaxation. So one exact disjunctive cut costs about as much as solving two LPs of the original size. Balas and Perregaard showed how to run the CGLP steps as pivots in the original tableau, which is how solvers compute [lift-and-project](/lift-and-project/) cuts.

**Example.** Let $P = \{x \ge 0 : -3x_1 + x_2 \le 0,\ x_1 + x_2 \le 2\}$, with vertices $(0,0)$, $(2,0)$ and $(\tfrac12, \tfrac32)$. Maximizing $x_2$ gives $x^* = (\tfrac12, \tfrac32)$. Split on $x_1 \le 0$ or $x_1 \ge 1$.

- $P_1 = P \cap \{x_1 \le 0\} = \{(0, 0)\}$. The rows $-3x_1 + x_2 \le 0$ with weight 1 and $x_1 \le 0$ with weight 2 add up to $-x_1 + x_2 \le 0$.
- $P_2 = P \cap \{x_1 \ge 1\}$ is the triangle with vertices $(1,0)$, $(2,0)$ and $(1,1)$. The rows $x_1 + x_2 \le 2$ with weight 1 and $-x_1 \le -1$ with weight 2 also add up to $-x_1 + x_2 \le 0$.

So $-x_1 + x_2 \le 0$ is a split cut. At $x^*$, its left side is $1 > 0$. The hull of $P_1 \cup P_2$ is the triangle $(0,0)$, $(2,0)$, $(1,1)$. The integer points of $P$ are $(0,0)$, $(1,0)$, $(2,0)$ and $(1,1)$, so this hull is the [integer hull](/integer-hull/), and one split cut has closed the whole gap.

## Classic examples

- **Gomory mixed-integer cuts.** The GMI cut of a tableau row is the split cut for the disjunction on the basic variable, computed in closed form from the cone of the optimal basis. It is the intersection cut of that cone with the split.
- **Intersection cuts.** Balas (1971) took the cone $C$ of an optimal basis and a convex set $S$ that has $x^*$ in its interior but no integer point there. The points where the extreme rays of $C$ leave $S$ define a hyperplane, which gives a valid cut. A split gives the GMI cut, and other lattice-free sets give the multi-row cuts.
- **Lift-and-project cuts.** For a 0/1 variable, the disjunction $x_j = 0$ or $x_j = 1$ gives the [lift-and-project](/lift-and-project/) cuts of Balas, Ceria and Cornuéjols, with the CGLP as above.
- **MIR inequalities.** Each [MIR inequality](/mixed-integer-rounding-inequality/) is a split cut for a split on an aggregated integer expression.
- **Indicator and complementarity constraints.** Disjunctive cuts for $y = 0 \Rightarrow x = 0$ give the perspective cuts and the convex hull of [indicator constraints](/indicator-constraint/).

## Variations

- **Split closure.** The set of points that satisfy all split cuts of $P$ is the split closure. Cook, Kannan and Schrijver (1990) showed that it is a polyhedron for rational $P$. It equals the MIR closure, and it is contained in the [Chvátal closure](/chvatal-closure/) for pure integer programs.
- **Monoidal strengthening.** Balas and Jeroslow (1980) showed how to use the integrality of the other variables to lower the coefficients of a disjunctive cut, for free, after the CGLP is solved.
- **Multi-term disjunctions.** Disjunctions with more than two terms, such as $t$-branch splits or the set of leaves of a branch and bound tree, give stronger cuts at the price of a larger CGLP.
- **Normalizations.** The choice of normalization changes which cut the CGLP returns. Besides the sum of all multipliers, common choices bound $\beta$ or bound the multipliers of the disjunction rows only.

## Pitfalls

- **Empty terms.** Every inequality is valid on an empty $P_k$, but the CGLP still asks that $\alpha = (A^k)^T u^k$, which can exclude good cuts. The exactness proof above needs each $P_k$ to be nonempty, so detect empty terms first, with an LP or by bound propagation, and drop them.
- **No normalization.** Without a normalization the CGLP is a cone, so its optimum is 0 or unbounded.
- **Splits are not enough for mixed-integer programs.** For pure integer programs, repeated split closures reach the integer hull, since they contain the Chvátal closures. For mixed-integer programs they may not: Cook, Kannan and Schrijver (1990) gave a small mixed-integer example where no finite number of rounds of split cuts reaches the hull.
- **Numerics and density.** Cuts from a CGLP are often dense, and their coefficients come from floating-point LPs. Solvers scale them, reject cuts with a large range of coefficients, and weaken the right side slightly.

## Exercises

1. For the example above, find the split cut for the disjunction $x_2 \le 1$ or $x_2 \ge 2$, and compare it with the cut $-x_1 + x_2 \le 0$.
2. Prove that every Chvátal-Gomory cut $c^T x \le \lfloor \delta \rfloor$ of a pure integer program is a split cut for the split $c^T x \le \lfloor \delta \rfloor$ or $c^T x \ge \lfloor \delta \rfloor + 1$.
3. Write the CGLP for the disjunction $x_j = 0$ or $x_j = 1$ of a 0/1 program, and show that it has about twice as many variables as the original LP.
4. Show by an example that the convex hull of the union of two polyhedra need not be closed, and explain why the CGLP describes its closure.

## References
