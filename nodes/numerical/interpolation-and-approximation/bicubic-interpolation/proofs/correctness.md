---
title: Bicubic interpolation with three-point slopes is a C^1 interpolant, exact on biquadratics, and equals Keys cubic convolution with a = -1/2 on uniform grids
proves: [correctness, termination, error-bound]
status: full
---

We use the notation of the page. On one axis the nodes are $x_0 < \cdots < x_m$ with $m \ge 1$, $h_k = x_{k+1} - x_k$, and $S$ is the one-dimensional rule: slopes $d_k$ from three-point parabolas (the chord if $m = 1$), and the cubic Hermite interpolant on each cell.

## Claim 1: termination

Lines L1 and L2 are binary searches over sorted arrays with clamped results, so $0 \le i \le m - 1$ and $0 \le j \le n - 1$. Lines L3 and L4 compute a fixed number of quantities from at most five nodes, with nonzero denominators because the nodes are distinct. Lines L5 and L6 are sums over at most 4 by 4 indices.

## Claim 2: the 1-D rule interpolates, is C^1, and its weights live on i - 1 .. i + 2

On cell $i$, $S$ is $P_i(t) = h_{00}(\sigma) y_i + h_i h_{10}(\sigma) d_i + h_{01}(\sigma) y_{i+1} + h_i h_{11}(\sigma) d_{i+1}$ with $\sigma = (t - x_i)/h_i$. As shown for the [cubic Hermite spline](/cubic-hermite-spline/), $P_i(x_i) = y_i$, $P_i(x_{i+1}) = y_{i+1}$, $P_i'(x_i) = d_i$, $P_i'(x_{i+1}) = d_{i+1}$. The slope $d_k$ is defined from $k$ alone (the three nodes are $k - 1, k, k + 1$ inside, the first or last three at the ends), so the cubics on the two cells that meet at $x_k$ have the same value $y_k$ and the same slope $d_k$ there. Hence $S$ is continuous with a continuous derivative. The slope $d_i$ involves nodes among $i - 1, i, i + 1$ (or $0, 1, 2$ when $i = 0$) and $d_{i+1}$ nodes among $i, i + 1, i + 2$ (or the last three); in every case they lie in $\{i - 1, \ldots, i + 2\} \cap \{0, \ldots, m\}$. Since $P_i$ is linear in the data, $P_i(t) = \sum_k w_k(t) y_k$ with weights supported there, which are the weights of L3 and L4.

## Claim 3: exactness on quadratics

If $y_k = q(x_k)$ with $\deg q \le 2$, the parabola through any three nodes interpolates $q$ at three points and therefore equals $q$, so $d_k = q'(x_k)$ for every $k$ (also for $m = 1$ when $\deg q \le 1$). The cubic $q$ itself has the values and slopes that define $P_i$, and the Hermite cubic with given end values and slopes is unique, so $P_i = q$. Hence $S q = q$ for all quadratics.

## Claim 4: lines L5 and L6 compute the tensor product, which interpolates, is C^1, and reproduces Q_2

Line L5 computes $r_a = \sum_b \beta_b f_{ab} = (S_y f_{a, \cdot})(Y)$ for each needed row $a$, and line L6 computes $\sum_a \alpha_a r_a$, which is $S_x$ applied to the values $r_a$ at the nodes $x_a$. Together
$$p(X, Y) = \sum_a \sum_b w_a(X) w_b(Y) f_{ab}.$$
At a grid point $(x_i, y_j)$, Claim 2 gives $w_a(x_i) = [a = i]$ and $w_b(y_j) = [b = j]$ in exact arithmetic, so $p = f_{ij}$. For fixed $Y$, $p$ is $S_x$ applied to data, which is $C^1$ in $X$ by Claim 2; likewise in $Y$. For $f = x^a y^b$ with $a, b \le 2$, the double sum factors as $(S_x x^a)(X) \cdot (S_y y^b)(Y) = X^a Y^b$ by Claim 3, and by linearity every element of $Q_2$ is reproduced.

On cell $(i, j)$, each $w_a(X)$ is a cubic in $X$ and each $w_b(Y)$ a cubic in $Y$, so $p$ is a bicubic polynomial. Its value, $\partial_X$, $\partial_Y$ and $\partial_X \partial_Y$ at a corner $(x_k, y_l)$ are $f_{kl}$, $(D_x f)_{kl}$, $(D_y f)_{kl}$ and $(D_x D_y f)_{kl}$, where $D$ is the three-point slope operator on each axis; these numbers depend only on the corner, not on the cell. Along a shared vertical edge $X = x_k$ both patches are the cubic Hermite interpolant in $Y$ of the same values and $Y$-slopes, and their $X$-derivatives are the cubic Hermite interpolant in $Y$ of the same $D_x f$ and $D_x D_y f$. So the value and both partial derivatives agree across the edge: $p$ is $C^1$ in two variables.

## Claim 5: Keys's kernel on a uniform grid

Let $h_k = h$ for all $k$ and let cell $i$ be interior ($1 \le i \le m - 2$). Then $d_i = (y_{i+1} - y_{i-1})/(2h)$ and $d_{i+1} = (y_{i+2} - y_i)/(2h)$. Substituting into $P_i$ with $s = \sigma$:
$$w_{i-1} = -\tfrac12 h_{10} = -\tfrac12 s(1 - s)^2, \qquad w_{i+2} = \tfrac12 h_{11} = \tfrac12 s^2(s - 1),$$
$$w_i = h_{00} - \tfrac12 h_{11}, \qquad w_{i+1} = h_{01} + \tfrac12 h_{10}.$$
Expanding, $w_{i-1} = (-s^3 + 2s^2 - s)/2$, $w_i = (3s^3 - 5s^2 + 2)/2$, $w_{i+1} = (-3s^3 + 4s^2 + s)/2$, $w_{i+2} = (s^3 - s^2)/2$, which are the values of Keys's kernel with $a = -1/2$ at distances $1 + s$, $s$, $1 - s$, $2 - s$. At the left end, the one-sided slope is $d_0 = (-3y_0 + 4y_1 - y_2)/(2h)$, which is the central difference $(y_1 - y_{-1})/(2h)$ for the extended value $y_{-1} = 3y_0 - 3y_1 + y_2$, Keys's boundary rule; the right end is symmetric.

For interior cells, $w_{i-1}, w_{i+2} \le 0$ and $w_i, w_{i+1} \ge 0$ on $[0, 1]$ (the last two are $\frac12(1 - s)(2 + 2s - 3s^2)$ and $\frac12 s(1 + 4s - 3s^2)$, products of nonnegative factors there), and the weights sum to 1 by Claim 3 with $q = 1$. So $\sum |w_k| = 1 - 2(w_{i-1} + w_{i+2}) = 1 + s(1 - s)^2 + s^2(1 - s) = 1 + s(1 - s) \le \frac54$.

## Claim 6: the 1-D error bound on a uniform grid

Let $f \in C^4[x_0, x_m]$ and $y_k = f(x_k)$. Let $H$ be the cubic Hermite interpolant on cell $i$ with exact slopes $f'(x_i)$, $f'(x_{i+1})$; then $|f - H| \le \frac{h^4}{384}\|f^{(4)}\|_\infty$ on the cell ([Hermite interpolation](/hermite-interpolation/) error with double nodes at both ends). The slope error of the parabola through $x_a, x_b, x_c$ at one of its nodes $x_k$ is $\frac16 f'''(\xi)\,\omega'(x_k)$ with $\omega = (x - x_a)(x - x_b)(x - x_c)$, from differentiating the interpolation error $f[x_a, x_b, x_c, x]\,\omega(x)$ at $x_k$, where $\omega(x_k) = 0$. For an interior node $|\omega'(x_k)| = h^2$ and for an end node $|\omega'(x_0)| = h \cdot 2h$. So $|e_k| = |d_k - f'(x_k)| \le \frac{h^2}{6}\|f'''\|_\infty$ inside and $\le \frac{h^2}{3}\|f'''\|_\infty$ at the ends. Finally $P_i - H = h(h_{10} e_i + h_{11} e_{i+1})$ and $|h_{10}| + |h_{11}| = \sigma(1 - \sigma)^2 + \sigma^2(1 - \sigma) = \sigma(1 - \sigma) \le \frac14$, so
$$|f - P_i| \le \frac{h^4}{384}\|f^{(4)}\|_\infty + \frac{h}{4}\max(|e_i|, |e_{i+1}|) \le \frac{h^4}{384}\|f^{(4)}\|_\infty + \frac{h^3}{12}\|f'''\|_\infty,$$
with $h^3/24$ when both nodes of the cell are interior. In two variables, $f - p = (f - S_x f) + S_x(f - S_y f)$; the first term is bounded by the 1-D bound in $x$, and the second by $\Lambda$ times the 1-D bound in $y$, where $\Lambda = \max \sum_a |w_a|$, which is $\frac54$ for interior cells by Claim 5.
