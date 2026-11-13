---
title: Each Lucas-Kanade step is the unique least-squares solution when the window has texture in two directions, and an exact translation is a fixed point
proves: [correctness]
status: full
---

Fix the current shift $d$ and, for each pixel $x$ of the window $\Omega$, the gradient $g(x) = (g_1(x), g_2(x))$ of line L5 and the difference $e(x)$ of line L6. The step solves the linear least-squares problem

$$
\min_{\Delta \in \mathbb{R}^2} \phi(\Delta), \qquad \phi(\Delta) = \sum_{x \in \Omega} \big( g(x) \cdot \Delta + e(x) \big)^2, \tag{1}
$$

which is the sum of squared differences of the problem after the linearization $E^2(x + d + \Delta) \approx E^2(x + d) + g(x) \cdot \Delta$. Line L7 builds $G = \sum_x g(x) g(x)^{\mathsf T}$ and $b = -\sum_x g(x) e(x)$.

**Claim 1 (the step is a least-squares minimizer).** $\phi$ is minimized exactly by the solutions of $G \Delta = b$. If $\det G > 0$, the solution is unique and equals the closed form of line L9, and the residual $r(x) = g(x) \cdot \Delta + e(x)$ is orthogonal to both gradient components: $\sum_x r(x) g_1(x) = \sum_x r(x) g_2(x) = 0$.

*Proof.* Expanding, $\phi(\Delta) = \Delta^{\mathsf T} G \Delta - 2 b^{\mathsf T} \Delta + \sum_x e(x)^2$. For any $\Delta$ and $h$,

$$
\phi(\Delta + h) - \phi(\Delta) = 2 h^{\mathsf T} (G \Delta - b) + h^{\mathsf T} G h,
$$

and $h^{\mathsf T} G h = \sum_x (g(x) \cdot h)^2 \ge 0$. If $G \Delta = b$, the first term vanishes, so $\phi(\Delta + h) \ge \phi(\Delta)$ for every $h$, and $\Delta$ is a minimizer. Conversely, if $G \Delta \ne b$, take $h = -t (G\Delta - b)$ with small $t > 0$; the change is $-2t |G\Delta - b|^2 + O(t^2) < 0$, so $\Delta$ is not a minimizer. The condition $G \Delta = b$ is $\sum_x g(x) (g(x) \cdot \Delta + e(x)) = 0$, the orthogonality of the residual. If $\det G > 0$, $G$ is invertible and $\Delta = G^{-1} b$ is the only solution. For $G = \begin{pmatrix} a & \beta \\ \beta & c \end{pmatrix}$ and $b = (p, q)$, the inverse is $\frac{1}{ac - \beta^2} \begin{pmatrix} c & -\beta \\ -\beta & a \end{pmatrix}$, which gives $\Delta = \big( (cp - \beta q), (aq - \beta p) \big) / (ac - \beta^2)$, the formula of line L9. $\square$

**Claim 2 (when $G$ is singular).** $G$ is symmetric positive semidefinite, so $\det G \ge 0$. $\det G = 0$ exactly when all vectors $g(x)$, $x \in \Omega$, lie on one line through the origin (including the case where all are zero). In that case, $\phi$ does not change along the direction perpendicular to that line, so the minimizer is not unique.

*Proof.* $h^{\mathsf T} G h = \sum_x (g(x) \cdot h)^2 \ge 0$ for all $h$, so both eigenvalues are at least 0 and their product $\det G$ is at least 0. By the Cauchy-Schwarz inequality for the vectors $(g_1(x))_x$ and $(g_2(x))_x$,

$$
\det G = \Big( \sum_x g_1^2 \Big) \Big( \sum_x g_2^2 \Big) - \Big( \sum_x g_1 g_2 \Big)^2 \ge 0,
$$

with equality exactly when the two vectors are linearly dependent, that is when there is a nonzero $h$ with $g(x) \cdot h = 0$ for every $x$. Such an $h$ is perpendicular to every gradient, so all gradients lie on the line perpendicular to $h$. For this $h$, $G h = \sum_x g(x)\,(g(x) \cdot h) = 0$, so $\phi(\Delta + t h) = \phi(\Delta)$ for every real $t$: a motion along $h$, which is along the edge, does not change the fit. This is the aperture problem. $\square$

The eigenvalues of $G$ are $\lambda_\pm = \frac{1}{2}\big( a + c \pm \sqrt{(a - c)^2 + 4 \beta^2} \big)$, and $\lambda_- = \min_{|h| = 1} \sum_x (g(x) \cdot h)^2$ is the weakest texture over all directions. A test $\lambda_- > \varepsilon$ in line L8 rejects windows that are singular or close to singular, and it bounds the effect of an error $\delta b$ on the step by $|G^{-1} \delta b| \le |\delta b| / \lambda_-$.

**Claim 3 (an exact translation is a fixed point).** Suppose that for an integer shift $t$, $E^2(y + t) = E^1(y)$ for every pixel $y$ whose value line L6 reads, and that $d = t$. Then lines L3 to L9 give $\Delta = 0$ if $\det G > 0$, so the iteration stops at $d = t$ in line L10.

*Proof.* With $d = t$ an integer vector, each position $x + d$ is a pixel, and bilinear interpolation at a pixel returns its value, because the fractional parts are 0 and the weights are $1, 0, 0, 0$. So line L6 gives $e(x) = E^2(x + t) - E^1(x) = 0$ for every $x \in \Omega$. Then $b = -\sum_x g(x) e(x) = 0$, and by Claim 1 the unique solution of $G \Delta = 0$ is $\Delta = 0$. Line L9 leaves $d = t$, and line L10 returns it because $|\Delta| = 0 < \tau$. $\square$

Claim 3 does not say that the iteration reaches $t$ from $d = 0$. The loop is the Gauss-Newton method for the nonlinear sum of squares $\varepsilon(d)$, with the Jacobian of the residuals at $d$ being the rows $g(x)^{\mathsf T}$. Gauss-Newton converges locally to a minimizer with zero residual when the Jacobian has full rank there, which is $\det G > 0$ at $t$; the region of convergence depends on the image, and a start too far from $t$ can lead to a different local minimum.
