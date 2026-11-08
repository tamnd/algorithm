---
title: The n-point Newton-Cotes rule is interpolatory, with degree n - 1 for even n and n for odd n
proves: [correctness]
status: full
---

Write $I(f) = \int_0^1 f(t)\,dt$ on the reference interval. The closed nodes are $t_i = (i - 1)/(n - 1)$ for $i = 1, \ldots, n$ with $n \ge 2$, and the open nodes are $t_i = i/(n + 1)$ with $n \ge 1$. In both cases the nodes are distinct and symmetric about $\tfrac12$.

**Step 1 (the weights exist, are unique and give the interpolatory rule).** Line L2 solves $\sum_{i=1}^n W_i t_i^k = 1/(k + 1)$ for $k = 0, \ldots, n - 1$. The matrix is the transpose of the Vandermonde matrix of distinct nodes, so it is nonsingular and the solution is unique. The interpolatory weights $I(\ell_i)$, with $\ell_i$ the Lagrange basis polynomials, satisfy the same equations, because $\sum_i I(\ell_i) t_i^k = I\big(\sum_i t_i^k \ell_i\big) = I(t^k)$ for $k \le n - 1$. So $W_i = I(\ell_i)$ and the reference rule $R(f) = \sum_i W_i f(t_i)$ is exact for every polynomial of degree at most $n - 1$. The Gauss-Jordan elimination is exact in rational arithmetic, so the computed weights are these numbers.

**Step 2 (symmetry).** The map $t \mapsto 1 - t$ permutes the nodes, and $f(1 - t)$ has the same integral and the same degree as $f$. By uniqueness in Step 1, $W_i = W_{n+1-i}$. Hence $R(p) = I(p)$ for every $p$ that is odd about $\tfrac12$, since both sides are 0.

**Lemma (the sign of the node polynomial).** Rescale so that the spacing is 1: the nodes are the integers $q, q + 1, \ldots, q + n - 1$ in $[0, L]$, with $q = 0$, $L = n - 1$ (closed) or $q = 1$, $L = n + 1$ (open), and let $c = L/2$ and $\omega(x) = \prod_{i=0}^{n-1} (x - q - i)$. For integers $j \ge 0$ let $A_j = \int_j^{j+1} \omega$. Then:

(a) $\omega$ has no zero inside any $(j, j + 1)$, so each $A_j \ne 0$.

(b) For $0 \le x < c - \tfrac12$, $\omega(x + 1) = -\rho(x)\,\omega(x)$ with $0 < \rho(x) < 1$. Indeed $\omega(x + 1)/\omega(x) = (x + 1 - q)/(x + 1 - q - n)$; its numerator is at least 0 and its denominator is negative, and $|x + 1 - q| < |x + 1 - q - n|$ is the condition $x < (n - 2 + 2q)/2 = c - \tfrac12$. (For $q = 1$ and $x = 0$, $\rho = 0$ and $\omega(1) = 0$; the inequality $|\omega(x+1)| < |\omega(x)|$ still holds except at isolated points, which is all the integrals below need.)

(c) Consequently, for $j + 1 \le c - \tfrac12$, $A_{j+1} = \int_j^{j+1} \omega(x + 1)\,dx$ has the sign opposite to $A_j$ and $|A_{j+1}| < |A_j|$.

Let $\Omega(x) = \int_0^x \omega$. On $[0, c]$, the values $\Omega(j)$ at integers $j \le c$ are partial sums of the alternating series $A_0 + A_1 + \cdots$ whose terms decrease strictly in absolute value, so each is nonzero with the sign of $A_0$. Between consecutive integers $\Omega$ is monotone, since $\omega$ has one sign there, so $\Omega$ has the sign of $A_0$ on all of $(0, c']$, where $c'$ is the largest integer at most $c$.

**Step 3 (odd $n$: degree exactly $n$).** Now $c$ is an integer and $\omega$ is odd about $c$, because the reflection $x \mapsto L - x$ permutes the nodes and multiplies the product of $n$ factors by $(-1)^n = -1$. So $I(\omega) = 0$ by Step 2, and by the theorem of Jacobi on [interpolatory rules](/interpolatory-quadrature/) (exactness for degree $n - 1 + k$ if and only if $\omega$ is orthogonal to all polynomials of degree below $k$), the degree is at least $n$. For degree $n + 1$ we would also need $\int_0^L (x - c)\,\omega(x)\,dx = 0$. Oddness of $\omega$ gives $\Omega(c + y) = \Omega(c - y)$ for $0 \le y \le c$, and $\Omega(L) = 0$. Integrating by parts,

$$\int_0^L (x - c)\,\omega(x)\,dx = \big[(x - c)\,\Omega(x)\big]_0^L - \int_0^L \Omega(x)\,dx = -\int_0^L \Omega(x)\,dx = -2 \int_0^c \Omega(x)\,dx.$$

By the Lemma ($c' = c$), $\Omega$ has one sign on $(0, c]$ and is not identically zero, so this is nonzero. The degree is exactly $n$.

**Step 4 (even $n$: degree exactly $n - 1$).** Now $c$ is a half-integer and $\omega$ is even about $c$, so $I(\omega) = 2\int_0^c \omega = 2\,\Omega(c)$. Write $c = c' + \tfrac12$. By the Lemma $\Omega(c')$ is nonzero with the sign of $A_0$ (or zero when $c' = 0$). The remaining piece $B = \int_{c'}^{c} \omega$ has the sign that alternation assigns to $A_{c'}$, the opposite of the sign of $A_{c'-1}$ when $c' \ge 1$, and $|B| = \int_{c'-1}^{c'-1/2} |\omega(x + 1)|\,dx < \int_{c'-1}^{c'-1/2} |\omega(x)|\,dx \le |A_{c'-1}|$ by (b), since $x \le c' - \tfrac12 < c - \tfrac12$ there. So $\Omega(c) = A_0 + \cdots + A_{c'-1} + B$ is still a partial sum of an alternating series with strictly decreasing terms and is nonzero. If $c' = 0$ (closed $n = 2$), $\Omega(c) = \int_0^{1/2} x(x - 1)\,dx = -\tfrac{1}{12} \ne 0$ directly. So $I(\omega) \ne 0$ and the rule is not exact for degree $n$, while Step 1 gives degree $n - 1$.

**Step 5 (the algorithm computes the composite rule).** Lines L3 to L8 return

$$Q(f) = H \sum_{j=0}^{m-1} \sum_{i=1}^{n} W_i\, f\big(a + (j + t_i) H\big), \qquad H = \frac{b - a}{m}.$$

For one panel $[a + jH, a + (j + 1)H]$, the substitution $x = a + (j + t) H$ turns the panel integral into $H\, I(g)$ with $g(t) = f(a + (j + t) H)$, and $g$ is a polynomial of the same degree as $f$. So each panel term equals the panel integral for every polynomial of degree at most $d$, and so does the sum, which is $\int_a^b f$. A polynomial of degree $d + 1$ with positive leading coefficient has, on each panel, an error equal to $H^{d+2}$ times the reference error of $t^{d+1}$ (lower-degree parts are integrated exactly), which is nonzero and the same on all panels, so the composite rule also has degree exactly $d$. The implementation merges the shared end nodes of adjacent closed panels by adding their two coefficients, which changes no sum. $\blacksquare$

**Termination and cost.** Line L2 is Gauss-Jordan elimination on an $n \times (n + 1)$ rational matrix, $O(n^3)$ operations. The double loop runs $m n$ times. Each distinct node is evaluated once: $m(n - 1) + 1$ evaluations for closed rules, whose panels share $m - 1$ end nodes, and $m n$ for open rules.

**Error formula (cited, not proved here).** By Steffensen's theorem the Peano kernel of the basic rule does not change sign, so for $f \in C^{d+1}$ on one panel of node spacing $h$ the error is $C_n h^{d+2} f^{(d+1)}(\xi)$, with $C_n = E(t^{d+1})/((d + 1)!\, h^{d+2})$ computed from Step 1. A proof is in Davis and Rabinowitz, Section 2.5, and in Isaacson and Keller, Analysis of Numerical Methods, Chapter 7. The test file checks the constants $C_n$ in exact arithmetic.
