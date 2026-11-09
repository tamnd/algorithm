---
tag: M7M3DM
kind: concept
slug: subadditive-duality
name: Subadditive duality for integer programming
aliases:
- Gomory-Johnson group problem
- group relaxation
- superadditive duality
- corner polyhedron
area: optimization/integer-programming
level: research
summary: Dual problem over subadditive functions that gives an exact duality theory for integer programs.
prereqs: [lp-duality, chvatal-gomory-finite-convergence, gomory-mixed-integer-cut]
see_also: [lp-duality, weak-duality, strong-duality, chvatal-gomory-finite-convergence, gomory-mixed-integer-cut, lagrangian-relaxation, chvatal-closure, integrality-gap]
sources:
  - paper: "Ralph E. Gomory, On the relation between integer and noninteger solutions to linear programs, Proceedings of the National Academy of Sciences 53 (1965), 260 to 265"
    locator: the group relaxation and the condition under which it solves the integer program
  - paper: "Ralph E. Gomory, Some polyhedra related to combinatorial problems, Linear Algebra and its Applications 2 (1969), 451 to 558"
    locator: corner polyhedra and their facets
  - paper: "Ralph E. Gomory and Ellis L. Johnson, Some continuous functions related to corner polyhedra, Mathematical Programming 3 (1972), 23 to 85 and 359 to 389"
    locator: the infinite group relaxation, minimal functions and the two-slope theorem
  - paper: "Laurence A. Wolsey, Integer programming duality: price functions and sensitivity analysis, Mathematical Programming 20 (1981), 173 to 195"
    locator: superadditive dual, strong duality with Chvátal functions
  - paper: "Charles E. Blair and Robert G. Jeroslow, The value function of an integer program, Mathematical Programming 23 (1982), 237 to 273"
    locator: the value function as a Gomory function
  - book: isbn:9780471828198
    title: George L. Nemhauser and Laurence A. Wolsey, Integer and Combinatorial Optimization, Wiley, 1988
    locator: Part II, the chapter on the theory of valid inequalities (superadditive duality)
  - paper: "Amitabh Basu, Robert Hildebrand and Matthias Köppe, Light on the infinite group relaxation I: foundations and taxonomy, 4OR 14 (2016), 1 to 40"
    locator: survey of the Gomory-Johnson theory
---

Subadditive duality is the exact duality theory of integer programming. In [LP duality](/lp-duality/), the dual prices the right side with a linear function. For an integer program, linear prices give only the bound of the [LP relaxation](/lp-relaxation/). If the prices may be any nondecreasing function that does not lose value when two right sides are added, the dual bound becomes exact: the best such function gives the integer optimum. The rounding functions of [Chvátal-Gomory cuts](/chvatal-gomory-cut/) are enough. The same functions describe the valid inequalities of Gomory's group relaxation and corner polyhedron, which is where the [Gomory mixed-integer cut](/gomory-mixed-integer-cut/) comes from.

## In plain words

In a linear program, each resource has a price, and the price of a bundle of resources is the sum of the prices. The dual problem finds prices under which no product looks profitable, and its best value equals the best profit. With whole-number decisions, this fails: the best prices give a bound that can be too high.

The fix is to let the price of a bundle be any function that is at least the sum of the prices of its parts, and that never drops when you add resources. Rounding down is such a function. With these more general prices, the dual bound is exactly the best whole-number profit. The price of the actual resources is then a proof that no better answer exists.

## The idea

**The dual.** Take the pure integer program

$$z^* = \max\{c^T x : Ax \le b,\ x \in \mathbb{Z}^n_+\}$$

with rational data and columns $a_1, \ldots, a_n$ of $A$. A function $F : \mathbb{R}^m \to \mathbb{R}$ is *superadditive* if $F(u) + F(v) \le F(u + v)$ for all $u, v$. The superadditive dual is

$$w^* = \min\{F(b) : F(a_j) \ge c_j \text{ for all } j,\ F \text{ superadditive and nondecreasing},\ F(0) = 0\}.$$

For the form $\min\{c^T x : Ax \ge b,\ x \in \mathbb{Z}^n_+\}$, the same theory uses subadditive functions, which gives the name. The map $F(d) \mapsto -F(-d)$ turns one form into the other. The linear functions $F(d) = y^T d$ with $y \ge 0$ are a special case, and for them the dual is the LP dual.

**Weak duality.** If $x$ is feasible and $F$ is feasible for the dual, then

$$c^T x \le \sum_j F(a_j) x_j \le F\Big(\sum_j a_j x_j\Big) = F(Ax) \le F(b).$$

The first step uses $x \ge 0$. The second uses superadditivity, applied $x_j$ times to each column, which needs $x_j$ to be a nonnegative integer. The last step uses that $F$ is nondecreasing. So $z^* \le w^*$.

**Strong duality.** If $z^*$ is finite, then $w^* = z^*$, and some Chvátal function attains it. A *Chvátal function* is built from linear functions with nonnegative coefficients by nonnegative combinations and the round-down operation $\lfloor \cdot \rfloor$. Each such function is superadditive and nondecreasing, because $\lfloor s \rfloor + \lfloor t \rfloor \le \lfloor s + t \rfloor$.

*Proof sketch for a bounded feasible region.* Let $P = \{x : Ax \le b,\ x \ge 0\}$ be a polytope. For $x \ge 0$, the Chvátal-Gomory cuts of a system $Gx \le h$ can be taken in the form $\lfloor u^T G \rfloor x \le \lfloor u^T h \rfloor$ with $u \ge 0$. By induction on $k$, each row of the $k$-th closure $P^{(k)}$ is then $F_i(A) x \le F_i(b)$ for a Chvátal function $F_i$, applied column by column. By the [finite convergence theorem](/chvatal-gomory-finite-convergence/), $P^{(k)} = P_I$ for some $k$. LP duality on $P^{(k)}$ gives $y \ge 0$ with $\sum_i y_i F_i(a_j) \ge c_j$ for all $j$ and $\sum_i y_i F_i(b) = z^*$. So $F = \sum_i y_i F_i$ is an optimal dual solution. Wolsey (1981) and Blair and Jeroslow (1982) prove the general case.

**Complementary slackness.** If $x^*$ is optimal and $F$ is optimal for the dual, all inequalities in the weak duality chain hold with equality. In particular $F(a_j) = c_j$ for every $j$ with $x^*_j > 0$.

**The value function.** The function $z(d) = \max\{c^T x : Ax \le d,\ x \in \mathbb{Z}^n_+\}$ is itself superadditive and nondecreasing where it is finite, since the sum of feasible points for $u$ and $v$ is feasible for $u + v$. Weak duality with the right side $d$ shows that every dual feasible $F$ satisfies $F(d) \ge z(d)$ wherever the program is feasible, so the value function is the smallest dual feasible function there. Blair and Jeroslow (1982) showed that the value function of a pure integer program with rational data is a Gomory function, the minimum of finitely many Chvátal functions. So sensitivity analysis for integer programs needs these functions, while LP sensitivity needs only linear ones.

**The group relaxation.** Let $B$ be an optimal basis of the LP relaxation of $\max\{c^T x : Ax = b,\ x \in \mathbb{Z}^n_+\}$, with nonbasic set $N$. Gomory (1965) dropped the constraint $x_B \ge 0$ but kept $x_B$ integral. What remains is

$$\max\Big\{c_B^T B^{-1} b - \sum_{j \in N} \bar c_j x_j : \sum_{j \in N} B^{-1} a_j x_j \equiv B^{-1} b \pmod{\mathbb{Z}^m},\ x_N \in \mathbb{Z}^N_+\Big\},$$

where $\bar c_j \ge 0$ are the [reduced costs](/reduced-cost/). For integral $A$, the congruences live in the finite group $\mathbb{Z}^m / B\mathbb{Z}^m$ of order $|\det B|$, and the problem is a shortest path problem on this group. If $B^{-1} b$ lies far enough inside the cone of the basis, its solution keeps $x_B \ge 0$ and solves the integer program. The convex hull of its solutions is the *corner polyhedron* (Gomory, 1969).

**Valid functions.** Take one row, $\sum_{j \in N} f_j x_j \equiv f_0 \pmod 1$, with $f_0 \in (0, 1)$. Let $\pi : [0, 1) \to \mathbb{R}_+$ be subadditive modulo 1, with $\pi(0) = 0$ and $\pi(f_0) = 1$. Then $\sum_j \pi(f_j) x_j \ge 1$ holds for every solution, because

$$1 = \pi(f_0) = \pi\Big(\sum_j f_j x_j \bmod 1\Big) \le \sum_j \pi(f_j)\, x_j.$$

Gomory and Johnson (1972) studied the *infinite group relaxation*, where every $r \in [0, 1)$ may appear. A valid $\pi$ is minimal if and only if it is subadditive, $\pi(0) = 0$, and $\pi(r) + \pi(f_0 - r) = 1$ for all $r$. Their two-slope theorem says that a continuous piecewise linear minimal function with only two slopes is extreme. The function of the GMI cut,

$$\pi(r) = \min\Big\{\frac{r}{f_0},\ \frac{1 - r}{1 - f_0}\Big\},$$

has two slopes and is the best known example.

## Examples

**A Chvátal function certificate.** Take $\max x_2$ subject to $3x_1 + 2x_2 \le 6$, $-3x_1 + 2x_2 \le 0$, $x \in \mathbb{Z}^2_+$. The integer points are $(0,0)$, $(1,0)$, $(2,0)$ and $(1,1)$, so $z^* = 1$. The LP optimum is $(1, \tfrac32)$ with value $\tfrac32$, and the best linear dual is $F(d) = \tfrac14 d_1 + \tfrac14 d_2$, with value $F(6, 0) = \tfrac32$. Round it down:

$$F(d) = \Big\lfloor \tfrac14 d_1 + \tfrac14 d_2 \Big\rfloor.$$

Then $F(a_1) = F(3, -3) = 0 \ge c_1 = 0$, $F(a_2) = F(2, 2) = 1 \ge c_2 = 1$, and $F(b) = F(6, 0) = \lfloor 3/2 \rfloor = 1 = z^*$. So $F$ is an optimal dual solution and proves that $z^* = 1$. Both columns satisfy $F(a_j) = c_j$, as complementary slackness requires at the optimum $(1, 1)$.

**The group relaxation of a row.** In the same example, with slacks $s_1, s_2$, the optimal tableau row of $x_2$ is $x_2 + \tfrac14 s_1 + \tfrac14 s_2 = \tfrac32$. Dropping $x_2 \ge 0$ leaves $\tfrac14(s_1 + s_2) \equiv \tfrac12 \pmod 1$, that is, $s_1 + s_2 \equiv 2 \pmod 4$. The GMI function with $f_0 = \tfrac12$ gives $\pi(\tfrac14) = \tfrac12$ and the cut $\tfrac12 s_1 + \tfrac12 s_2 \ge 1$, that is, $s_1 + s_2 \ge 2$. In the original variables, this is $x_2 \le 1$.

**A valid function that is not minimal.** The function $\pi(r) = r / f_0$ gives Gomory's fractional cut. It is subadditive modulo 1 and valid, but for $r > f_0$ it is larger than $(1 - r)/(1 - f_0)$, so $\pi(r) + \pi(f_0 - r \bmod 1) > 1$ for such $r$, and it is not minimal. The GMI function is smaller everywhere, so its cut is stronger.

## Where it is used

- **Certificates of optimality.** A Chvátal function with $F(b) = z^*$ is a proof of optimality for an integer program, in the same way as an LP dual solution. Cutting plane proofs and branch and bound trees can both be turned into such certificates.
- **Sensitivity analysis.** Wolsey (1981) used optimal dual functions as price functions that bound the optimal value for other right sides.
- **Cut generation.** Valid functions of the group relaxation are cut generating functions. Applied to the rows of a simplex tableau, they give the GMI cut and many stronger one-row and multi-row cuts studied since the 2000s.
- **Algorithms.** Gomory's group relaxation gave early algorithms for integer programs with a large right side, and it led to the asymptotic results that connect integer and linear optima.
- **Comparison with Lagrangian duality.** [Lagrangian relaxation](/lagrangian-relaxation/) prices only some constraints and keeps a linear price. It gives a bound between the LP bound and $z^*$. The superadditive dual has no [integrality gap](/integrality-gap/), but its functions can be complex.

## References
