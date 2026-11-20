---
title: The bbFMM equals direct summation with the kernel replaced by its Chebyshev interpolant on each far pair, and it converges for kernels analytic away from the diagonal
proves: [correctness]
status: full
---

We use exact arithmetic. The tree is uniform, with leaves at level $L \ge 2$, and the lists are those of the [fast multipole method](/fast-multipole-method/). Let $\bar x_1, \ldots, \bar x_n$ be the Chebyshev nodes $\cos((2m - 1)\pi / (2n))$ on $[-1, 1]$ and $S_n(\bar x_m, t) = \frac{1}{n} + \frac{2}{n} \sum_{k=1}^{n-1} T_k(\bar x_m) T_k(t)$. For a box $B$ with center $c_B$ and side $w_B$, let $\xi_B(x) = 2 (x - c_B) / w_B \in [-1, 1]^2$, and for $m = (m_1, m_2)$ let $S_B(m, x) = S_n(\bar x_{m_1}, \xi_{B,1}(x)) \, S_n(\bar x_{m_2}, \xi_{B,2}(x))$, with the node $\bar x^B_m = c_B + \frac{w_B}{2} (\bar x_{m_1}, \bar x_{m_2})$.

**Lemma 1 (Lagrange basis).** $S_n(\bar x_m, \cdot)$ is the polynomial of degree at most $n - 1$ that is 1 at $\bar x_m$ and 0 at the other nodes. Hence, for every polynomial $f$ of degree at most $n - 1$, $\sum_m f(\bar x_m) S_n(\bar x_m, t) = f(t)$, and the same holds in 2D for polynomials of degree at most $n - 1$ in each coordinate.

*Proof.* The degree is clear. With $\theta_j = (2j - 1)\pi / (2n)$, $T_k(\bar x_j) = \cos(k \theta_j)$, and the discrete orthogonality of the cosines at these angles gives $\sum_{k=0}^{n-1}{}' \cos(k\theta_m) \cos(k\theta_j) = \frac{n}{2} [m = j]$, where the prime halves the term $k = 0$. Multiply by $2/n$: this is $S_n(\bar x_m, \bar x_j) = [m = j]$. A polynomial of degree at most $n - 1$ is fixed by its values at $n$ points, which gives the reproduction. The 2D statement follows by applying the 1D one in each coordinate. $\square$

**Lemma 2 (the shifts are exact).** (a) If $C$ is a child of $B$, the upward shift of line L2 maps the weights $W_C(m') = \sum_{i \in C} q_i S_C(m', y_i)$ to $\sum_{i \in C} q_i S_B(m, y_i)$. (b) If $g$ is a vector of values at the nodes of $B$, the downward shift of line L4 gives values $g'$ at the nodes of a child $D$ with $\sum_{k} g'(k) S_D(k, x) = \sum_m g(m) S_B(m, x)$ for every $x \in D$.

*Proof.* (a) The shift computes $\sum_{m'} S_B(m, \bar x^C_{m'}) W_C(m') = \sum_i q_i \sum_{m'} S_B(m, \bar x^C_{m'}) S_C(m', y_i)$. As a function of $y \in C$, $S_B(m, y)$ is a polynomial of degree $n - 1$ in each coordinate, also in the coordinates $\xi_C$ of the child, so by Lemma 1 the inner sum is $S_B(m, y_i)$. (b) The shift sets $g'(k) = \sum_m g(m) S_B(m, \bar x^D_k)$, and $\sum_k g'(k) S_D(k, x) = \sum_m g(m) \sum_k S_B(m, \bar x^D_k) S_D(k, x) = \sum_m g(m) S_B(m, x)$ by Lemma 1 in the same way. $\square$

**Lemma 3 (the output).** Let $j$ be a charge in leaf $t$, and for a box $C$ in the interaction list of an ancestor $T$ of $t$ let

$$\tilde K_{T,C}(x, y) = \sum_{m} \sum_{m'} S_T(m, x) \, K(\bar x^T_m, \bar x^C_{m'}) \, S_C(m', y),$$

the tensor Chebyshev interpolant of $K$ on $T \times C$ with $n$ nodes in each of the four coordinates. Then the output is

$$u_j = \sum_{i \text{ near}} q_i K(z_j, z_i) + \sum_{(T, C)} \sum_{i \in C} q_i \tilde K_{T,C}(z_j, z_i),$$

where the first sum is over the charges $i \ne j$ in the near neighbours of $t$ and the second over the pairs of Lemma 1 of the FMM proof, which split the far charges into disjoint boxes.

*Proof.* By Lemma 2(a) and induction from the leaves up, after line L2 every box $C$ holds $W_C(m') = \sum_{i \in C} q_i S_C(m', z_i)$. Line L3 adds $\sum_{m'} K(\bar x^T_m, \bar x^C_{m'}) W_C(m')$ to the value of $T$ at the node $m$. By Lemma 2(b) and induction from the root down, the values $g_t$ of the leaf satisfy $\sum_k g_t(k) S_t(k, x) = \sum_{(T, C)} \sum_m S_T(m, x) \sum_{m'} K(\bar x^T_m, \bar x^C_{m'}) W_C(m')$ for $x \in t$. Line L5 evaluates this at $z_j$, and substituting $W_C$ gives the second sum. Line L6 adds the first. That the pairs split the far charges is Lemma 1 of the FMM proof, which uses only the tree and the lists. $\square$

So the error is $\sum_{(T, C)} \sum_{i \in C} q_i (\tilde K_{T,C} - K)(z_j, z_i)$, and

$$|u_j - u(z_j)| \le \Big( \sum_i |q_i| \Big) \max_{(T, C)} \sup_{T \times C} |K - \tilde K_{T,C}|.$$

**Theorem (convergence).** Let $K(x, y)$, for $x \in T$ and $y \in C$, be the restriction of a function that, as a function of each one of the four coordinates with the others fixed and real, extends to an analytic function bounded by $M$ in the Bernstein ellipse $E_\rho$ (in the scaled coordinate) for a fixed $\rho > 1$, for all pairs $(T, C)$ of the interaction lists. Then $\sup |K - \tilde K_{T,C}| \le 4 (1 + \Lambda_n)^4 \frac{2 M \rho^{1-n}}{\rho - 1}$, where $\Lambda_n$ is the Lebesgue constant of the $n$ Chebyshev nodes, and the error of the bbFMM tends to 0 as $n \to \infty$.

*Proof.* Write $\tilde K = I_1 I_2 I_3 I_4 K$, where $I_d$ is 1D interpolation in coordinate $d$ at the scaled nodes; these operators commute. Then $K - \tilde K = (K - I_1 K) + I_1 (K - I_2 K) + I_1 I_2 (K - I_3 K) + I_1 I_2 I_3 (K - I_4 K)$. In the sup norm, $\|I_d f\| \le \Lambda_n \|f\|$, and $\|f - I_d f\| \le (1 + \Lambda_n) E_d$, where $E_d$ is the largest, over the other coordinates, best approximation error of $f$ by polynomials of degree $n - 1$ in coordinate $d$. The Chebyshev coefficients of a function analytic and bounded by $M$ in $E_\rho$ satisfy $|a_k| \le 2 M \rho^{-k}$ (Trefethen, Theorem 8.1), so truncating the Chebyshev series after degree $n - 1$ gives $E_d \le E := \sum_{k \ge n} 2 M \rho^{-k} = 2 M \rho^{1-n} / (\rho - 1)$. Each term of the decomposition applies some operators $I_d$ to an error $K - I_e K$ of $K$ itself, so only the analyticity of $K$ in each coordinate is used. The four terms are at most $(1 + \Lambda_n) E (1 + \Lambda_n + \Lambda_n^2 + \Lambda_n^3) \le 4 (1 + \Lambda_n)^4 E$. Since $\Lambda_n = O(\log n)$ for Chebyshev nodes, the bound tends to 0. $\square$

**The kernels of the page satisfy the hypothesis.** For $K = \log|x - y|$, $1/|x - y|$ or $(|x - y|^2 + c^2)^{-1/2}$, fix all coordinates but one, say $x_1$. The function depends on $x_1$ through $(x_1 - y_1)^2 + \delta^2$ with $\delta = |x_2 - y_2|$ (and $c^2$ added), and it is analytic in $x_1$ except where $(x_1 - y_1)^2 = -\delta^2$ (or $-\delta^2 - c^2$). Two boxes of side $w$ in an interaction list are at least $w$ apart in one coordinate. If that coordinate is $x_1$, the singular points have real part at least $w$ from the interval of $x_1$, which has half-length $w / 2$, so they are at least at the scaled distance 2 from $[-1, 1]$ along the real axis. Otherwise $\delta \ge w$, and they are at the scaled imaginary distance at least 2. In both cases they lie outside the open ellipse $E_\rho$ with $\rho = 2 + \sqrt{5}$, whose semi-axes are $\sqrt{5} < 3$ and 2. The ellipse is simply connected and $(x_1 - y_1)^2 + \delta^2$ (plus $c^2$) has no zero in it, so a branch of the log and of the square root is analytic there, and the function is bounded on the closed ellipse $E_{\rho'}$ for any $\rho' < \rho$. The offsets of the interaction list and the levels are finitely many, so one $\rho' > 1$ and one $M$ serve all pairs. For the log kernel the scaling changes the kernel only by a constant, which the interpolation reproduces, so the bound is the same at every level. $\square$
