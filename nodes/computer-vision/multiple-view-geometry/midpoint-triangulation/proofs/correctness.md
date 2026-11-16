---
title: The midpoint of the common perpendicular is the unique point closest to two skew rays, and it is the true point on exact data
proves: [correctness]
status: full
---

We use the notation of the page. The two rays are the lines $L_1 = \{\mathbf{C}_1 + \lambda_1\mathbf{d}_1\}$ and $L_2 = \{\mathbf{C}_2 + \lambda_2\mathbf{d}_2\}$ in $\mathbb{R}^3$, with $\mathbf{d}_1, \mathbf{d}_2 \ne \mathbf{0}$. Put $\mathbf{w} = \mathbf{C}_1 - \mathbf{C}_2$, $a = \mathbf{d}_1\cdot\mathbf{d}_1$, $b = \mathbf{d}_1\cdot\mathbf{d}_2$, $c = \mathbf{d}_2\cdot\mathbf{d}_2$, $d = \mathbf{d}_1\cdot\mathbf{w}$, $e = \mathbf{d}_2\cdot\mathbf{w}$ and $D = ac - b^2$. The arithmetic is exact (real RAM).

**Claim.** Assume that $\mathbf{d}_1$ and $\mathbf{d}_2$ are not parallel. Then (a) $D > 0$, so line L3 does not stop; (b) the values $\lambda_1$, $\lambda_2$ of line L4 give the unique pair of points $\mathbf{Q}_1 \in L_1$, $\mathbf{Q}_2 \in L_2$ at least distance, and $\mathbf{Q}_1 - \mathbf{Q}_2$ is perpendicular to both directions; (c) the output $\mathbf{M} = (\mathbf{Q}_1 + \mathbf{Q}_2)/2$ is the unique minimizer of $g(\mathbf{X}) = \operatorname{dist}(\mathbf{X}, L_1)^2 + \operatorname{dist}(\mathbf{X}, L_2)^2$; (d) if the two lines meet at a point $\mathbf{X}$, the output is $\mathbf{X}$; (e) if the rays come from calibrated cameras, $\mathbf{d}_i = R_i^{\mathsf T}(u_i, v_i, 1)^{\mathsf T}$ and $\mathbf{C}_i = -R_i^{\mathsf T}\mathbf{t}_i$, then $\lambda_i$ is the depth of $\mathbf{Q}_i$ in camera $i$.

**Proof of part (a).** By the Cauchy-Schwarz inequality $b^2 \le ac$, with equality only if $\mathbf{d}_1$ and $\mathbf{d}_2$ are parallel. So $D > 0$. $\square$

**Proof of part (b).** The squared distance between the points with parameters $\lambda_1$ and $\lambda_2$ is
$$f(\lambda_1, \lambda_2) = \|\mathbf{w} + \lambda_1\mathbf{d}_1 - \lambda_2\mathbf{d}_2\|^2 .$$
This is a quadratic function with Hessian $2\begin{pmatrix} a & -b \\ -b & c\end{pmatrix}$, whose determinant is $4D > 0$ and whose first entry is $2a > 0$. So the Hessian is positive definite, $f$ is strictly convex, and its unique minimizer is the unique zero of its gradient. Half the gradient is
$$\left(\mathbf{d}_1\cdot\mathbf{g},\; -\mathbf{d}_2\cdot\mathbf{g}\right), \qquad \mathbf{g} = \mathbf{w} + \lambda_1\mathbf{d}_1 - \lambda_2\mathbf{d}_2 = \mathbf{Q}_1 - \mathbf{Q}_2 .$$
So at the minimizer $\mathbf{g}$ is perpendicular to $\mathbf{d}_1$ and $\mathbf{d}_2$. Written out, the two conditions are $a\lambda_1 - b\lambda_2 = -d$ and $b\lambda_1 - c\lambda_2 = -e$. Cramer's rule, with the determinant $-D$ of this system, gives
$$\lambda_1 = \frac{(-d)(-c) - (-b)(-e)}{-D} = \frac{be - cd}{D}, \qquad \lambda_2 = \frac{a(-e) - b(-d)}{-D} = \frac{ae - bd}{D},$$
which are the values of line L4. $\square$

**Proof of part (c).** Put $\delta = \|\mathbf{Q}_1 - \mathbf{Q}_2\|$, the least distance between the lines. Take any $\mathbf{X}$, and let $\mathbf{P}_1$, $\mathbf{P}_2$ be its nearest points on $L_1$, $L_2$, at distances $r_1$, $r_2$. By the triangle inequality and part (b),
$$r_1 + r_2 \ge \|\mathbf{P}_1 - \mathbf{P}_2\| \ge \delta .$$
Then $g(\mathbf{X}) = r_1^2 + r_2^2 \ge (r_1 + r_2)^2/2 \ge \delta^2/2$. The midpoint $\mathbf{M}$ reaches this bound: the vector $\mathbf{M} - \mathbf{Q}_1 = (\mathbf{Q}_2 - \mathbf{Q}_1)/2$ is perpendicular to $\mathbf{d}_1$, so the nearest point of $L_1$ to $\mathbf{M}$ is $\mathbf{Q}_1$ and $r_1 = \delta/2$; in the same way $r_2 = \delta/2$, and $g(\mathbf{M}) = \delta^2/2$. For uniqueness, let $g(\mathbf{X}) = \delta^2/2$. Then all the inequalities are equalities: $r_1 = r_2$, $r_1 + r_2 = \delta$, and $\|\mathbf{P}_1 - \mathbf{P}_2\| = \delta$. By part (b) the pair at distance $\delta$ is unique, so $\mathbf{P}_1 = \mathbf{Q}_1$ and $\mathbf{P}_2 = \mathbf{Q}_2$. Equality in the triangle inequality puts $\mathbf{X}$ on the segment from $\mathbf{Q}_1$ to $\mathbf{Q}_2$, and $r_1 = r_2$ makes it the midpoint. If $\delta = 0$ the bound gives $\mathbf{X} \in L_1 \cap L_2$, which is the single point $\mathbf{Q}_1 = \mathbf{Q}_2 = \mathbf{M}$. $\square$

**Proof of part (d).** If $\mathbf{X} = \mathbf{C}_1 + \mu_1\mathbf{d}_1 = \mathbf{C}_2 + \mu_2\mathbf{d}_2$, then $f(\mu_1, \mu_2) = 0$, which is the least possible value. By the uniqueness in part (b), $(\lambda_1, \lambda_2) = (\mu_1, \mu_2)$, so $\mathbf{Q}_1 = \mathbf{Q}_2 = \mathbf{X}$ and the output is $\mathbf{X}$. Two lines that are not parallel meet in at most one point, so this is the only point on both rays. $\square$

**Proof of part (e).** The point $\mathbf{Q}_i = \mathbf{C}_i + \lambda_i\mathbf{d}_i$ has the camera coordinates
$$R_i\mathbf{Q}_i + \mathbf{t}_i = (R_i\mathbf{C}_i + \mathbf{t}_i) + \lambda_i R_i\mathbf{d}_i = \mathbf{0} + \lambda_i(u_i, v_i, 1)^{\mathsf T},$$
because $R_iR_i^{\mathsf T} = I$. Its third coordinate, the depth, is $\lambda_i$. $\square$

**Remark (similarity invariance).** Let $T(\mathbf{X}) = sQ\mathbf{X} + \mathbf{T}$ with $Q$ a rotation and $s > 0$. The new rays have the centers $T(\mathbf{C}_i)$ and the directions $Q\mathbf{d}_i$. Then $a$, $b$, $c$ do not change, $\mathbf{w}$ becomes $sQ\mathbf{w}$, and $d$, $e$ are multiplied by $s$. So $\lambda_1$, $\lambda_2$ are multiplied by $s$, the new $\mathbf{Q}_i$ is $T(\mathbf{Q}_i)$, and the new output is $T(\mathbf{M})$. A general affine map does not keep right angles, so the common perpendicular of the new lines is in general not the image of the old one. For example, the shear $(x, y, z) \mapsto (x, y + 2z, z)$ moves the output of the noisy example of the page away from the image of the old output. On exact data part (d) holds in every frame, so the output is invariant under all affine maps there.

**Remark (scale of the directions).** Multiplying $\mathbf{d}_i$ by a nonzero number $k$ divides $\lambda_i$ by $k$ and leaves the points $\mathbf{Q}_i$ unchanged, so the output does not depend on the length or sign of the directions.

**Remark (floating point).** The test $D \le \varepsilon\,ac$ in line L3 rejects pairs whose angle $\theta$ has $\sin^2\theta \le \varepsilon$, because $D = ac\sin^2\theta$. For nearly parallel rays the formulas of line L4 lose accuracy in proportion to $1/\sin^2\theta$; this is a property of the problem, whose answer moves far when the rays turn a little.
