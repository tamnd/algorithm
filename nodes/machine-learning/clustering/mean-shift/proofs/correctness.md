---
title: Gaussian mean shift is a scaled gradient step that never lowers the density and always stops
proves: [correctness]
status: full
---

Let $x_1, \ldots, x_n \in \mathbb{R}^d$ be the data and $h > 0$ the bandwidth. Write $t_i(y) = \lVert y - x_i \rVert^2 / h^2$, the Gaussian profile $k(t) = e^{-t/2}$, and $g(t) = -k'(t) = \tfrac12 e^{-t/2}$. Up to a positive constant, which changes none of the statements, the kernel density estimate is

$$f(y) = \sum_{i=1}^n k(t_i(y)).$$

Put $g_i = g(t_i(y))$ and $G = \sum_i g_i > 0$. Lines L4 and L5 compute $y' = \sum_i g_i x_i / G$, because the weights $e^{-t_i/2}$ of line L4 are $2 g_i$ and the factor cancels. The mean shift vector is $m(y) = y' - y$.

**Lemma 1 (the step is a scaled gradient).** $m(y) = h^2 \, \nabla f(y) / f(y)$.

*Proof.* $\nabla t_i(y) = 2 (y - x_i) / h^2$, so $\nabla f(y) = \sum_i k'(t_i) \cdot 2 (y - x_i)/h^2 = (2/h^2) \sum_i g_i (x_i - y) = (2/h^2) \, G \, m(y)$. For the Gaussian profile $k = 2g$, so $f(y) = 2G$. Dividing gives $\nabla f / f = m / h^2$. $\square$

So $m(y)$ points uphill, and its length is large where the density is low and small near a mode. This is the adaptive step size that Cheng (1995) and Comaniciu and Meer (2002) describe.

**Lemma 2 (the density does not decrease).** $f(y') - f(y) \ge (G / h^2) \lVert y' - y \rVert^2$. In particular $f(y') \ge f(y)$, with equality only if $y' = y$.

*Proof.* The profile $k$ is convex, so $k(s) \ge k(t) + k'(t)(s - t) = k(t) - g(t)(s - t)$ for all $s, t \ge 0$. Apply this with $t = t_i(y)$ and $s = t_i(y')$ and add over $i$:

$$f(y') - f(y) \ge \sum_i g_i \big(t_i(y) - t_i(y')\big) = \frac{1}{h^2} \sum_i g_i \big(\lVert y - x_i \rVert^2 - \lVert y' - x_i \rVert^2\big).$$

Each bracket equals $\lVert y \rVert^2 - \lVert y' \rVert^2 - 2 (y - y') \cdot x_i$. With $\sum_i g_i x_i = G y'$, the sum is

$$G \big(\lVert y \rVert^2 - \lVert y' \rVert^2\big) - 2 G (y - y') \cdot y' = G \lVert y - y' \rVert^2. \qquad \square$$

This is Theorem 1 of Comaniciu and Meer (2002), in the special case of the Gaussian kernel. The same argument works for any kernel with a convex and decreasing profile.

**Lemma 3 (the iterates stay in the convex hull).** Each $y'$ is a convex combination of the data, so after the first step all points of the sequence lie in the convex hull $H$ of $x_1, \ldots, x_n$.

**Theorem (termination).** For each start and each $\tau > 0$, the loop of lines L3 to L7 ends after finitely many steps. The point $y$ it returns has $\lVert \nabla f(y) \rVert < f(y) \, \tau / h^2$ at the point before the last step.

*Proof.* Let $\Delta$ be the diameter of $H$, and let $y_1, y_2, \ldots$ be the sequence after the first step. By Lemma 3 each $t_i(y_j) \le \Delta^2 / h^2$, so $G(y_j) \ge \tfrac{n}{2} e^{-\Delta^2 / (2 h^2)} =: G_0 > 0$. By Lemma 2, $f(y_{j+1}) - f(y_j) \ge (G_0 / h^2) \lVert y_{j+1} - y_j \rVert^2$. The values $f(y_j)$ do not decrease and are at most $n$, so

$$\sum_j \lVert y_{j+1} - y_j \rVert^2 \le \frac{h^2 \, n}{G_0} < \infty,$$

and the steps tend to 0. So a step shorter than $\tau$ occurs, and line L7 stops the loop. At the point $y$ where that step starts, $\lVert m(y) \rVert < \tau$, and Lemma 1 gives the bound on the gradient. $\square$

**What is not claimed.** Every limit point of the infinite sequence is a stationary point of $f$, by Lemma 1 and the continuity of $m$. Comaniciu and Meer (2002) also state that the whole sequence converges. Li, Hu and Wu (2007) pointed out a gap in that proof. Convergence of the sequence was later shown for the one-dimensional case (Ghassabeh 2013) and under extra conditions in general. The algorithm does not depend on it, because it stops by the length of the step. A walk can also stop near a stationary point that is not a mode, such as a saddle point. This is rare in practice, and a small random push followed by more steps moves the point away.

**The clustering.** Lines L9 to L12 put each end point into the first earlier center within the merge distance, or start a new center. Two points share a label only if their end points are joined by such links. When the ends of the walks that reach one mode lie within the merge distance of each other, and the distinct modes lie farther apart than the merge distance plus these errors, the labels are exactly the basins of attraction of the modes that the walks reach.

**Cost.** One step costs $\Theta(n d)$, and line L1 starts one walk at each point. With at most $T$ steps for each walk, the time is $O(T n^2 d)$ and the extra space is $O(n d)$ for the modes. Near a mode the step shrinks in proportion to the distance to the mode, so the convergence is linear, and $T$ grows like $\log(1/\tau)$ times a factor that depends on the shape of the density at the mode.
