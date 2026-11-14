---
title: What simplicial approximation guarantees on a convex region, and how it fails on a nonconvex one
proves: [correctness]
status: full
---

**Setting.** $R \subset \mathbb{R}^n$ is a compact convex set with a nonempty interior, the acceptable region. For $x \in R$ and a direction $d \ne 0$, the line search returns $\mathrm{exit}(x, d) = x + t^* d$ with $t^* = \max\{t \ge 0 : x + t d \in R\}$. Because $R$ is convex and closed, $\{t \ge 0 : x + td \in R\} = [0, t^*]$. The method starts from an interior point $x_0$. $S_k$ is the set of boundary points after round $k$, $P_k = \operatorname{conv}(S_k)$, and $(c_k, r_k)$ is the optimum of the linear program of line L4 for $P_k$. The inscribed radius of a set $A$ is $r(A) = \sup\{r : B(c, r) \subseteq A \text{ for some } c\}$.

**Lemma 1 (the largest ball is a linear program).** Let $P = \{x : n_f \cdot x \le b_f,\ f = 1, \ldots, m\}$ with $\|n_f\|_2 = 1$. Then $B(c, r) \subseteq P$ if and only if $n_f \cdot c + r \le b_f$ for every $f$. So $r(P)$ is the optimum of

$$ \max\ r \quad\text{subject to}\quad n_f \cdot c + r \le b_f \ (f = 1, \ldots, m), $$

a [linear program](/linear-programming-problem/) in the $n + 1$ variables $(c, r)$.

*Proof.* The largest value of $n_f \cdot x$ over $x \in B(c, r)$ is $n_f \cdot c + r \|n_f\|_2 = n_f \cdot c + r$, reached at $x = c + r n_f$. The ball lies in the half-space of face $f$ if and only if this value is at most $b_f$, and it lies in $P$ if and only if it lies in every half-space. $\square$

The center $c$ of an optimal ball is often called a Chebyshev center of $P$. If the norms are not normalized, the constraint reads $n_f \cdot c + r \|n_f\|_2 \le b_f$, which is still linear in $(c, r)$.

**Lemma 2 (the start).** $P_0$ has a nonempty interior and contains $x_0$ in its interior.

*Proof.* $x_0$ is interior, so each of the $2n$ line searches along $\pm e_j$ returns $x_0 \pm t_j^{\pm} e_j$ with $t_j^{\pm} > 0$. The hull of these points contains the cross-polytope $\{x_0 + \sum_j y_j e_j : \sum_j |y_j| / \min(t_j^+, t_j^-) \le 1\}$, which contains a ball around $x_0$. $\square$

**Theorem 1 (inclusion, nesting and monotone radius).** For every round $k$:

1. $B(c_k, r_k) \subseteq P_k \subseteq R$.
2. $P_k \subseteq P_{k+1}$.
3. $r_0 \le r_1 \le \cdots \le r_k \le r(R)$.

*Proof.* Every point of $S_k$ is in $R$, and $R$ is convex, so the convex hull $P_k$ of $S_k$ is in $R$. The ball is in $P_k$ by Lemma 1. Points are only added, so $S_k \subseteq S_{k+1}$ and $P_k \subseteq P_{k+1}$. The optimal ball of round $k$ lies in $P_{k+1}$, so it is feasible for the program of round $k + 1$, and $r_{k+1} \ge r_k$. Finally, $B(c_k, r_k) \subseteq R$ gives $r_k \le r(R)$. $\square$

So each center is a feasible design with a safety margin of at least $r_k$ in every direction, and the margin never shrinks from one round to the next.

**Lemma 3 (the stop test).** Let $F$ be a facet of $P_k$ with outward unit normal $n_F$ and hyperplane $n_F \cdot x = b_F$, and let $q$ be a point in the relative interior of $F$. If $\mathrm{exit}(q, n_F) = q$, then $R \subseteq \{x : n_F \cdot x \le b_F\}$, so the hyperplane of $F$ supports $R$.

*Proof.* $F \subseteq P_k \subseteq R$, so $q \in R$ and the line search is defined. Suppose some $y \in R$ has $\alpha = n_F \cdot y - b_F > 0$. Write $y - q = \alpha n_F + w$, where $w$ is parallel to the hyperplane of $F$. Since $q$ is in the relative interior of $F$ and the affine hull of $F$ is that hyperplane, $q - \delta w \in F$ for some small $\delta > 0$. Let $\varepsilon = \delta / (1 + \delta)$, so that $\varepsilon / (1 - \varepsilon) = \delta$. The point

$$ z = (1 - \varepsilon)(q - \delta w) + \varepsilon y = q + \varepsilon \alpha n_F $$

is a convex combination of points of $R$, so $z \in R$. Then $t^* \ge \varepsilon \alpha > 0$ for the search from $q$ along $n_F$, which contradicts $\mathrm{exit}(q, n_F) = q$. $\square$

In the plane, a facet is an edge and the center of the largest $(n-1)$-ball in it is its midpoint, which is in its relative interior. In higher dimensions the center of the largest ball inscribed in a facet is also in its relative interior when the facet has a nonempty relative interior.

**Theorem 2 (a fixed point is optimal).** Suppose that at round $k$ every face that touches the optimal ball, that is with $n_f \cdot c_k + r_k = b_f$, supports $R$. Then $r_k = r(R)$, and $B(c_k, r_k)$ is a largest ball in $R$. In particular, when the method stops at line L11, every tangent face was marked by Lemma 3, and the returned ball is a largest ball in $R$.

*Proof.* The dual of the program of Lemma 1 is

$$ \min \sum_f \lambda_f b_f \quad\text{subject to}\quad \sum_f \lambda_f n_f = 0,\ \ \sum_f \lambda_f = 1,\ \ \lambda \ge 0 . $$

The primal is feasible and bounded, so by [strong duality](/strong-duality/) the dual has an optimal $\lambda$ with $\sum_f \lambda_f b_f = r_k$, and by [complementary slackness](/complementary-slackness/) $\lambda_f > 0$ only for faces that touch the optimal ball. Take any ball $B(c', r') \subseteq R$. For each touching face $f$, $R$ lies in its half-space, so by Lemma 1 $n_f \cdot c' + r' \le b_f$. Multiply by $\lambda_f \ge 0$ and add:

$$ r' = \sum_f \lambda_f r' = \sum_f \lambda_f (n_f \cdot c' + r') - \Big(\sum_f \lambda_f n_f\Big) \cdot c' \le \sum_f \lambda_f b_f = r_k . $$

So no ball in $R$ is larger than $r_k$, and with Theorem 1, $r_k = r(R)$. A mark set in an earlier round stays valid, because a supporting hyperplane of $R$ stays a supporting hyperplane. $\square$

The proof shows more: the optimal ball needs only the faces that touch it to lie on supporting hyperplanes of $R$. The polytope can be far from $R$ elsewhere. On the triangle of the page, the method stops with the exact inscribed disc while the hull covers only 83 percent of the triangle.

**What is not proved here.** Two natural claims are not given a proof on this page.

- *Convergence of the polytope to $R$.* The rule refines only faces that touch the ball, so the polytope need not fill $R$. On the ellipse $x^2/4 + y^2 \le 1$ the tests measure that the area of $P_k$ stays at 88.0 percent of the area of $R$ from round 20 to round 60, while $r_k$ has reached $r(R) = 1$. The variant that refines the longest edge of the whole hull adds points with gaps that shrink along the whole boundary, and in the same test it reaches 99.8 percent.
- *Convergence of $r_k$ to $r(R)$ when the method never stops.* The tests measure it on a disc (0.998 after 60 rounds) and an ellipse, but the general statement is not proved here. Director and Hachtel (1977) give the method and their own discussion of its convergence for convex regions, and the reader should consult the paper for its exact statement.

**Theorem 3 (failure on a nonconvex region).** Let $R$ be the L-shaped region $[0,4] \times [0,2] \,\cup\, [0,2] \times [0,4]$ and $x_0 = (1, 1)$. Then $P_0 \not\subseteq R$, and the optimal ball of $P_0$ is not contained in $R$.

*Proof.* The four line searches from $(1, 1)$ return $(4, 1)$, $(1, 4)$, $(0, 1)$ and $(1, 0)$. Their hull is the quadrilateral bounded by $x + y \ge 1$, $x - 3y \le 1$, $x + y \le 5$ and $y - 3x \le 1$. The point $(2.4, 2.4)$ satisfies all four inequalities, but it lies in the removed square $(2, 4] \times (2, 4]$, so it is not in $R$. By the symmetry in $x$ and $y$, the program of Lemma 1 has an optimal center $(a, a)$ that touches $x + y = 5$, $x - 3y = 1$ and $y - 3x = 1$, so $(5 - 2a)/\sqrt{2} = (1 + 2a)/\sqrt{10}$. This gives $a = (5\sqrt{5} - 1)/(2 + 2\sqrt{5}) \approx 1.5729$ and $r_0 = (5 - 2a)/\sqrt{2} \approx 1.3110$. The ball contains $c_0 + r_0 (1, 1)/\sqrt{2} = (2.5, 2.5)$, which is not in $R$. $\square$

The run goes on to stop with a radius of 1.4645, while every disc in $R$ has radius at most $2\sqrt{2}/(1 + \sqrt{2}) \approx 1.1716$. It stops because the midpoint $(2.5, 2.5)$ of a tangent edge is outside $R$, so the line search has no valid start, and the implementation reads this as a face on the boundary. So on a nonconvex region the method can report a center whose ball holds infeasible designs, and a radius that no ball in $R$ reaches.
