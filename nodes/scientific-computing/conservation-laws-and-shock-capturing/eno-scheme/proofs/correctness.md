---
title: ENO reconstruction is exact for polynomials of degree r - 1, has error O(dx^r) for smooth data, and keeps stencils away from isolated jumps; the scheme is conservative
proves: [correctness]
status: full
---

**Setting.** The cell averages $v_i$ live on cells $[x_{i-1/2}, x_{i+1/2}]$ of width $h$. Lines L2 and L3 of the page choose, for each cell $i$, a stencil of $r$ consecutive cells $\{s, s+1, \dots, s+r-1\}$ that contains $i$. They start with $\{i\}$ and, $r - 1$ times, add one cell on the left or on the right of the current stencil $\{s, \dots, s+l-1\}$. The left cell is added if

$$|\Delta^l v_{s-1}| < |\Delta^l v_s|, \qquad \Delta^l v_a = \sum_{n=0}^{l} (-1)^{l-n}\binom{l}{n} v_{a+n},$$

and the right cell otherwise. Here $\Delta^l v_a$ is the $l$-th undivided difference over the cells $a, \dots, a + l$. Line L4 sets $k = i - s$ and computes the face values

$$v^-_{i+1/2} = \sum_{n=0}^{r-1} w^R_{r,k,n}\,v_{s+n}, \qquad v^+_{i-1/2} = \sum_{n=0}^{r-1} w^L_{r,k,n}\,v_{s+n},$$

where the weights come from the Newton form described in Lemma 1. Since $\Delta^l v_a$ is $(l+1)!\,h^l$ times the divided difference of order $l + 1$ of the primitive function on the $l + 2$ faces $x_{a-1/2}, \dots, x_{a+l+1/2}$, the rule compares divided differences of the primitive, as in Harten, Engquist, Osher and Chakravarthy (1987).

**Lemma 1 (exact for polynomials).** If $v_n$ are the averages of a polynomial $p$ of degree at most $r - 1$, then the face values are $p(x_{i+1/2})$ and $p(x_{i-1/2})$ for every stencil.

*Proof.* Let $V(x) = \int_{x_{s-1/2}}^{x} p$, a polynomial of degree at most $r$. At the $r + 1$ faces of the stencil, $V(x_{s+m-1/2}) = h\sum_{n<m} v_{s+n}$, so these values are known from the averages. The interpolating polynomial of degree at most $r$ through $r + 1$ points is unique, so the Newton interpolant of these values is $V$ itself, and its derivative at a face is $V' = p$ there. The code computes the derivative of the Newton interpolant on unit spaced nodes, with $h = 1$, for each unit vector $v = e_n$; by linearity this gives the weights, and they do not depend on $h$ because the face value of a constant is the constant and the map commutes with scaling of $x$. $\square$

The test compares the weights for $r \le 4$ with a direct fit of a polynomial to the cell averages by Gaussian elimination in `Fraction` arithmetic, and checks Lemma 1 on random polynomials of degree $r - 1$ for $r = 2, 3, 4$.

**Theorem 1 (order r).** If $u$ has $r$ bounded derivatives near $x_{i+1/2}$ and $v_n$ are its cell averages, then $|v^-_{i+1/2} - u(x_{i+1/2})| \le C h^r$, with $C$ depending only on $r$ and $\max|u^{(r)}|$, for every stencil the rule can choose.

*Proof.* Let $p$ be the Taylor polynomial of $u$ of degree $r - 1$ at $x_{i+1/2}$, and $e = u - p$, so $|e(x)| \le \max|u^{(r)}|\,|x - x_{i+1/2}|^r/r!$. Every stencil cell lies within $rh$ of the face, so every average of $e$ over a stencil cell is at most $\max|u^{(r)}|(rh)^r/r!$ in size. The face value is linear in the averages, so by Lemma 1 it equals $p(x_{i+1/2}) = u(x_{i+1/2})$ plus the weighted sum of the averages of $e$. There are finitely many weight vectors (one for each $k$), so $\sum_n |w_{r,k,n}|$ is bounded by a constant that depends only on $r$. $\square$

So the choice of stencil does not affect the order; it only decides which of the $r$ candidates of order $r$ is used.

**Lemma 2 (stencils avoid isolated jumps).** Let the data be piecewise constant, with any two jumps at least $r$ cells apart. Then every chosen stencil lies inside one constant piece, and every face value equals the cell average of its cell.

*Proof.* By induction on $l$, the stencil $\{s, \dots, s+l-1\}$ after $l - 1$ choices is constant with value $a$. For $l = 1$ this is clear. The left candidate $\{s-1, \dots, s+l-1\}$ is constant, so $\Delta^l = 0$, unless cell $s - 1$ has another value $b$. Then all but the first of its $l + 1$ values are $a$, and $\Delta^l v_{s-1} = (-1)^l(b - a) \ne 0$. In the same way, the right candidate has $\Delta^l = 0$ or $\Delta^l = b' - a \ne 0$. Both candidates cannot cross a jump, because then two jumps would have only the $l \le r - 1$ cells of the stencil between them. If the left candidate crosses a jump, its difference is nonzero and the right one is zero, so the strict test adds the right cell. If the right one crosses, the left difference is zero and strictly smaller, so the left cell is added. If neither crosses, either choice is constant. So the final stencil is constant. The weights add up to 1 by Lemma 1 with $p = 1$, so both face values are $a$. $\square$

The test `test_stencils_avoid_jumps` checks Lemma 2 for $r = 2, 3, 4$ exactly. A fixed centered stencil would put a jump inside the stencil and give overshoots at the faces.

**Lemma 3 (conservation and consistency).** With the Rusanov face flux $H_{i+1/2} = \frac12(f(v^-) + f(v^+)) - \frac{a}{2}(v^+ - v^-)$ and the rate $L_i = -(H_{i+1/2} - H_{i-1/2})/h$, on a periodic grid $\sum_i L_i = 0$, so the SSP RK3 step keeps $\sum_i v_i$. For constant data $H = f(v)$.

*Proof.* The sum telescopes. Each SSP RK3 stage adds multiples of $\Delta t L(\cdot)$ to convex combinations of earlier stages. For constant data the face values are the constant by Lemma 1, and the diffusion term is zero. $\square$

The test checks Lemma 3 exactly in `Fraction` arithmetic for Burgers' equation with $r = 1, 2, 3$.

**What is not proved here.** ENO schemes are not TVD. The test on a square wave with $r = 3$ measures a new maximum of about $2.6 \times 10^{-5}$ above the old one. No bound on the growth of the total variation is proved here. The order of the full scheme is measured: with SSP RK3 and Courant number 0.5, the $L^1$ orders for $r = 3$ are 2.97 and 2.99 on smooth advection and 2.98 and 3.00 on a smooth Euler wave. Positivity for the Euler equations is not proved.
