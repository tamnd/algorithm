---
title: For a ball touching two planes the pencil path is a line parallel to the edge at the distance r over sin of half the opening angle, and the tracer follows it exactly
proves: [correctness]
status: full
---

**Setting.** Two planes $P_i = \{x : n_i \cdot x = d_i\}$, $i = 1, 2$, have unit normals $n_1, n_2$ that are not parallel, so $e = n_1 \times n_2 \ne 0$. The free region, where the tool may be, is the wedge $W = \{x : n_1 \cdot x \ge d_1,\ n_2 \cdot x \ge d_2\}$, so the normals point into the free side, and the edge $E = P_1 \cap P_2$ is a concave edge of the part. The opening angle $\alpha \in (0°, 180°)$ of the wedge satisfies $\cos\alpha = -n_1 \cdot n_2$. The tool is a ball of radius $r > 0$. The offset functions of the code are $g_i(x) = n_i \cdot x - d_i - r$.

**Lemma 1.** The closed ball $B(c, r)$ lies in the half-space $n_i \cdot x \ge d_i$ if and only if $n_i \cdot c - d_i \ge r$. It lies in it and touches $P_i$ if and only if $n_i \cdot c - d_i = r$, and then the only common point is $c - r n_i$.

*Proof.* The smallest value of $n_i \cdot x$ on the ball is $n_i \cdot c - r$, taken only at $x = c - r n_i$, because $n_i \cdot (x - c) \ge -|x - c| \ge -r$ with equality only when $x - c = -r n_i$. $\square$

**Theorem.** The centers $c$ of the balls that lie in $W$ and touch both planes form the line
$$
\ell = \Big\{\, p + \frac{r}{1 + n_1 \cdot n_2}(n_1 + n_2) + t\, e \;:\; t \in \mathbb{R} \,\Big\},
$$
where $p$ is any point of $E$. The line is parallel to the edge, at the distance $r/\sin(\alpha/2)$ from it, and the contact points are $c - r n_1 \in P_1$ and $c - r n_2 \in P_2$. Every center of a ball that lies in $W$, whether it touches the planes or not, is at least as far from $E$ as $\ell$.

*Proof.* By Lemma 1 the centers are the solutions of the two linear equations $n_i \cdot c = d_i + r$. The normals are independent, so the solutions form a line whose direction is orthogonal to both, that is parallel to $e$. Since $n_1 \ne -n_2$, $1 + n_1 \cdot n_2 > 0$. Let $w = r(n_1 + n_2)/(1 + n_1 \cdot n_2)$. Then $n_1 \cdot w = r(1 + n_1 \cdot n_2)/(1 + n_1 \cdot n_2) = r$, and in the same way $n_2 \cdot w = r$. So $p + w$ is a solution, which gives $\ell$. The edge $E$ is the line $p + t e$, and $w$ is orthogonal to $e$, so the distance from $\ell$ to $E$ is $|w|$. Now $|n_1 + n_2|^2 = 2 + 2\, n_1 \cdot n_2$, so
$$
|w|^2 = \frac{2r^2}{1 + n_1 \cdot n_2} = \frac{2r^2}{1 - \cos\alpha} = \frac{r^2}{\sin^2(\alpha/2)} .
$$
The contacts come from Lemma 1. For the last claim, let $x$ be the center of a ball in $W$, and write $x = p + w + v + t e$ with $v \perp e$. By Lemma 1, $n_i \cdot x - d_i \ge r$, so $n_i \cdot v \ge 0$ for both $i$. Then $w \cdot v = r(n_1 \cdot v + n_2 \cdot v)/(1 + n_1 \cdot n_2) \ge 0$, and the squared distance from $x$ to $E$ is $|w + v|^2 = |w|^2 + 2\, w \cdot v + |v|^2 \ge |w|^2$. $\square$

So the pencil path for a concave edge between two planes is the straight line $\ell$, and its ball is the one that goes deepest into the corner. With the tip of the tool as the reference point, the path of a vertical tool is $\ell$ moved down by $r$.

**The tracer on two planes.** Line L1 and line L6 call the corrector. For linear $g = (g_1, g_2)$ with the matrix $J$ of rows $n_1, n_2$, one corrector step maps $x$ to $x' = x - J^{\mathsf T}(J J^{\mathsf T})^{-1} g(x)$. The matrix $J J^{\mathsf T}$ has the determinant $1 - (n_1 \cdot n_2)^2 = |e|^2 > 0$, so it is invertible, and $g(x') = g(x) + J(x' - x) = g(x) - g(x) = 0$. So every point that the corrector returns is on $\ell$, after one step and with no error in exact arithmetic. Line L4 gives the tangent $\nabla g_1 \times \nabla g_2 = e$, so line L5 moves along $\ell$, and the corrector leaves the point unchanged. Successive points are $h$ apart along $\ell$, or $h|e|$ apart when the tangent is not normalized. The tests check, in rational arithmetic with unit normals from Pythagorean quadruples, that every traced point is on the closed-form line at the squared distance $2r^2/(1 + n_1 \cdot n_2)$ and that the contacts lie on the planes. A brute force search over random points checks that no admissible center is closer to the edge.

**Curved surfaces.** When the $g_i$ are signed distances to smooth surfaces with independent gradients along the curve, the pencil curve $g_1 = g_2 = 0$ is a smooth curve by the implicit function theorem, and the corrector is a Newton method for an underdetermined system, which converges fast from a point close enough to it. This is a local statement. No global result is claimed: the tracer can jump to another branch with a long step, it stops where the gradients become parallel, and it does not check the ball against other surfaces. On a floor and a concave cylinder wall of radius $\rho$, the pencil curve is the circle of radius $\rho - r$ at height $r$, and the tests measure that the traced points stay on it to $10^{-9}$ and go once round.
