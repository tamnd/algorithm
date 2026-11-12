---
title: Phong shading covers the top-left pixels and lights each with the normalized barycentric normal
proves: [correctness]
status: full
---

Let $T$ be the triangle with vertices $v_0, v_1, v_2$, with nonzero area, and vertex normals $n_0, n_1, n_2$. Coordinates are exact rationals, and the normals are real vectors. Let $\lambda_k(p)$ be the screen barycentric coordinates of a point $p$ ([edge function](/edge-function/), property 6), and let $g(p) = \sum_k \lambda_k(p)\, n_k$. Each component of $g$ is the affine function of the plane with the values of that component at the vertices.

**Precondition.** There is a vector $u$ with $n_k \cdot u > 0$ for $k = 0, 1, 2$, that is, the three normals lie in one open half space. This holds for the normals of a smooth patch seen from one side.

**Claim.** PHONG-TRIANGLE writes pixel $(i, j)$ if and only if $T$ covers its center $p$ under the [top-left fill rule](/top-left-fill-rule/). It writes each such pixel once, and the value is $\mathrm{SHADE}(g(p)/\lVert g(p) \rVert)$, where SHADE is the reflection model of line L11. The vector $g(p)$ is never zero there.

**Coverage.** Lines L1, L2, L4, L5, L7 and L9 are the same tests as lines L1, L2, L4, L5, L7 and L9 of GOURAUD-TRIANGLE, on the same rational values $y_c$, $x_l$, $x_r$ and $x_c$. The values carried with them (an intensity there, a vector here) do not change any test. Lemmas 1 to 3 of [the Gouraud correctness proof](/gouraud-shading/) show that these tests accept the center $p$ if and only if $p + (\varepsilon, \varepsilon^2)$ is in the interior of $T$ for all small enough $\varepsilon > 0$, which is the top-left rule. The same proof shows that each pixel is written at most once.

**The interpolated vector.** Fix a component $q$ of the vectors. The function $g_q$ is affine with $g_q(v_k) = (n_k)_q$. On an edge from $a$ to $b$, $g_q(a + t(b - a)) = g_q(a) + t\,(g_q(b) - g_q(a))$, so line L3 gives $m = g(x, y_c)$ at both span ends, $m_l = g(x_l, y_c)$ and $m_r = g(x_r, y_c)$. On the row, $x \mapsto g(x, y_c)$ is affine, so

$$g(x, y_c) = m_l + (x - x_l)\,\frac{m_r - m_l}{x_r - x_l} = m_l + (x - x_l)\,\Delta m .$$

Line L8 sets $m = g(x_c, y_c)$ for the first center. If $m = g(x_c, y_c)$ before line L12, then after it $m = g(x_c + u_x, y_c)$, where $u_x$ is the pixel width, and $x_c$ has moved by $u_x$. By induction, $m = g(p)$ at line L10 for each center $p$ of the span.

**The vector is not zero.** A written center $p$ is covered, so it is in the closed triangle and $\lambda_k(p) \ge 0$ with $\sum_k \lambda_k(p) = 1$. Then

$$g(p) \cdot u = \sum_k \lambda_k(p)\,(n_k \cdot u) \ge \min_k (n_k \cdot u) > 0 ,$$

so $g(p) \ne 0$, and line L10 divides by a positive length. It gives the unit vector $g(p)/\lVert g(p) \rVert$, and line L11 writes SHADE of it.

**Termination.** Line L1 visits finitely many rows, and in each row the loop of line L9 adds a fixed positive width to $x_c$ until $x_c \ge x_r$ or the screen ends. $\blacksquare$
