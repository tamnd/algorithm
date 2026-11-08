---
title: The Stieltjes solve is triangular, the Kronrod extension has degree at least 3n+1 (3n+2 for odd n), and the adaptive driver keeps a partition and terminates
proves: [correctness, error, termination]
status: full
---

We use the notation of the page: $P_k$ is the Legendre polynomial of degree $k$, the weight is $w = 1$ on $[-1, 1]$, $n \ge 1$, and $E_{n+1} = \sum_{j=0}^{n+1} c_j P_j$ with $c_{n+1} = 1$ is the Stieltjes polynomial. The Kronrod rule $K_{2n+1}$ has the $n$ zeros of $P_n$ and the $n + 1$ zeros of $E_{n+1}$ as nodes. We separate what is proved here, what is a cited theorem that the code checks at run time, and what is a heuristic.

## Claim 1: the conditions on $E_{n+1}$ are triangular and have a unique solution

The defining conditions are $\int_{-1}^1 E_{n+1}(x)\,P_n(x)\,x^k\,dx = 0$ for $k = 0, \ldots, n$. Since $P_0, \ldots, P_n$ span the polynomials of degree at most $n$, they are equivalent to

$$\sum_{j=0}^{n+1} c_j\,T(k, n, j) = 0 \qquad (k = 0, \ldots, n), \qquad T(l, m, j) = \int_{-1}^1 P_l P_m P_j\,dx.$$

$P_k P_n$ has degree $k + n$ and is orthogonal to every polynomial of degree below $n - k$: indeed, for $\deg q < n - k$ the product $q P_k$ has degree below $n$, so $\int P_n (q P_k) = 0$. Hence $T(k, n, j) = 0$ for $j < n - k$, and condition $k$ involves only $c_{n-k}, \ldots, c_{n+1}$. By Adams' formula (Adams 1878; the test file checks it against exact monomial integration for all indices up to $8$),

$$T(l, m, j) = \frac{2}{l + m + j + 1}\,\frac{A(s - l)\,A(s - m)\,A(s - j)}{A(s)}, \qquad s = \tfrac{l + m + j}{2},\quad A(r) = \binom{2r}{r}4^{-r} > 0,$$

when $l + m + j$ is even and the triangle inequalities hold, and $T = 0$ otherwise. For $j = n - k$ the sum $k + n + j = 2n$ is even and the triangle inequalities hold, so the pivot $T(k, n, n - k)$ is positive. Processing $k = 0, 1, \ldots, n$ therefore fixes $c_n, c_{n-1}, \ldots, c_0$ one at a time, uniquely, which is what `stieltjes_coefficients` does in exact rational arithmetic. So $E_{n+1}$ exists, is unique given $c_{n+1} = 1$, and has degree exactly $n + 1$.

Parity: $T(k, n, j) = 0$ when $k + n + j$ is odd. By induction on $k$, if every $c_j$ already fixed with $j \not\equiv n + 1 \pmod 2$ is $0$, then condition $k$ gives $c_{n-k} = 0$ when $n - k \not\equiv n + 1$, because every nonzero term pairs $c_j$ with $j \equiv n - k$. So $E_{n+1}(-x) = (-1)^{n+1}E_{n+1}(x)$.

## Claim 2: the nodes (cited theorem, checked at run time)

For the Legendre weight, the zeros of $E_{n+1}$ are real, simple, lie in $(-1, 1)$ and interlace with the zeros of $P_n$ (Szegő 1935; see also Monegato 1982 for a survey). The code does not assume this. It brackets each of the $n + 1$ gaps $(-1, x_1), (x_1, x_2), \ldots, (x_n, 1)$ between the Gauss nodes and the endpoints and bisects on a sign change of $E_{n+1}$; if some gap shows no sign change it raises an error. If it returns, each of the $n + 1$ disjoint open gaps contains a zero of $E_{n+1}$ by the intermediate value theorem (up to the rounding in evaluating $E_{n+1}$ by the Legendre recurrence), and since $E_{n+1}$ has degree $n + 1$ these are all its zeros. They are distinct from the Gauss nodes, so the $2n + 1$ nodes are distinct. The symmetrization $y \mapsto \frac12(y_i - y_{n-i})$ uses the parity of Claim 1 and cannot move a computed zero further from the exact one than the worse of the pair.

## Claim 3: the weights exist and the rule has degree $3n + 1$, or $3n + 2$ for odd $n$

The weights solve $\sum_i W_i P_k(y_i) = \int_{-1}^1 P_k = 2\,\delta_{k0}$ for $k = 0, \ldots, 2n$. The matrix $(P_k(y_i))$ is the Vandermonde matrix of the $2n + 1$ distinct nodes multiplied on the left by the invertible change of basis from monomials to Legendre polynomials, so it is nonsingular and the weights are unique. By linearity the rule is then exact on every polynomial of degree at most $2n$: it is the interpolatory rule on these nodes.

Let $s = P_n E_{n+1}$, of degree $2n + 1$, which vanishes at every node. Let $f$ be a polynomial of degree at most $3n + 1$. Divide: $f = q\,s + r$ with $\deg q \le n$ and $\deg r \le 2n$. Then $f(y_i) = r(y_i)$, so

$$K(f) = K(r) = \int_{-1}^1 r = \int_{-1}^1 f - \int_{-1}^1 q\,P_n\,E_{n+1} = \int_{-1}^1 f,$$

since $\deg q \le n$ and $E_{n+1} P_n$ is orthogonal to such $q$ by construction. So the degree is at least $3n + 1$.

If $n$ is odd, $3n + 2$ is odd. The node set is symmetric (Claim 2) and the reflected weights $W_{2n+2-i}$ solve the same nonsingular system (each $P_k$ has parity $k$, and the right side vanishes for odd $k$), so the weights are symmetric. A symmetric rule integrates every odd monomial exactly, to $0$, so $x^{3n+2}$ is exact too. The code averages each pair $W_i, W_{2n+2-i}$ to make this hold exactly in floating point.

The degree is no larger, provided $\int s\,x^{k} \ne 0$ at the first $k$ above $n$ allowed by parity ($k = n + 1$ for even $n$, $k = n + 2$ for odd $n$): the polynomial $s\,x^k$, of degree $3n + 2$ or $3n + 3$, vanishes at every node, so $K(s x^k) = 0 \ne \int s x^k$. That this integral is nonzero for every $n$ is a cited result (Rabinowitz 1980, on the exact degree of Kronrod extensions), not proved here; the test file checks it in exact arithmetic for $n \le 6$ and checks the failure of the computed rule numerically for $n \le 10$.

The embedded rule $G_n$ (Gauss weights at the Gauss nodes, $0$ elsewhere) is the Gauss-Legendre rule with degree $2n - 1$ by the [Gauss quadrature theorem](/gauss-quadrature-theorem/).

**Positivity (cited, checked).** For the Legendre weight all Kronrod weights are positive (Monegato 1978); the tests check positivity for $n \le 30$. Positivity is not needed for the degree, but it bounds the rounding: $\lvert K(\hat f) - K(f) \rvert \le \max_i \lvert \hat f_i - f_i \rvert \sum W_i = 2\max_i \lvert \hat f_i - f_i \rvert$.

## Claim 4: the panel and the error estimate

On $[a, b]$ the panel uses $c = \frac{a + b}{2}$, $h = \frac{b - a}{2}$ and returns $h\sum_i W_i f(c + h y_i)$. The map $y \mapsto c + h y$ is affine, so $p(c + h y)$ has the same degree as $p$, and the panel is exact on $\int_a^b p$ for $\deg p \le 3n + 1$ (or $3n + 2$). For $b < a$ the factor $h$ is negative and the oriented integral is returned. All nodes satisfy $-1 < y_i < 1$, so $f$ is never evaluated at $a$ or $b$.

**Asymptotic error.** If $f \in C^{d+1}[a, b]$ with $d$ the degree, the interpolatory error representation gives $\lvert \int_a^b f - K \rvert \le C_n \lvert b - a \rvert^{d+2}\max\lvert f^{(d+1)} \rvert$ with a constant $C_n$ that depends only on the rule (the [Peano kernel](/peano-kernel-theorem/) bound, scaled to the panel). So under bisection the panel error falls like $(b - a)^{d+2}$; the tests observe the exponents $7$ for $n = 1$ and $9$ for $n = 2$.

**The estimate is a heuristic.** QUADPACK sets $e = \rho\min(1, (200\lvert K - G \rvert/\rho)^{3/2})$, where $\rho = \lvert h \rvert\sum_i W_i \lvert f_i - K/(2h) \rvert$, and raises $e$ to at least $50\,\epsilon_{\text{mach}}\lvert h \rvert\sum_i W_i\lvert f_i \rvert$. No theorem says $e \ge \lvert \int f - K \rvert$: the value $\lvert K - G \rvert$ measures the error of $G$, not of $K$, and an integrand that vanishes at all $2n + 1$ nodes, such as $s(x)$ itself mapped to the panel, gives $K = G = 0$ and $e = 0$ against a nonzero integral. The $3/2$ power encodes the hope that the error of $K$ is much smaller than that of $G$ once $G$ is accurate; the factor $200$ and the floor are empirical (Piessens et al. 1983, Chapter 2). The page states only measured behaviour for it.

## Claim 5: the adaptive driver

Invariants at the top of the loop on line L8:

1. The panels in the heap are closed intervals with pairwise disjoint interiors whose union is the segment between $a$ and $b$, and each carries its own value $K$, estimate $e$ and floor flag.
2. `total` and `errsum` equal the sums of the stored values and estimates up to rounding in the running updates.

Initially the heap holds the single panel $[a, b]$. An iteration that does not stop removes one panel $[l, r]$ and inserts $[l, m]$ and $[m, r]$ with $m = \frac{l + r}{2}$, and the guard on line L9 checks $\min(l, r) < m < \max(l, r)$ in floating point, so both halves are nonempty and the partition property is preserved; lines L10 update both sums by the difference. The final sums on line L11 are recomputed with `fsum`, so the returned value and estimate are the correctly rounded sums over the final partition.

**Termination.** Each iteration either stops (status "limit" or "roundoff") or increases the number of panels by exactly one; the loop stops with "limit" as soon as there are `limit` panels. So there are at most `limit` $- 1$ bisections and at most $(2\,\text{limit} - 1)(2n + 1)$ evaluations, whatever $f$ and $\tau$ are. If the loop ends because the running estimate is at most $\max(\tau, \text{rel}\cdot\lvert\text{total}\rvert)$, the status is "ok".

**Conditional accuracy.** By additivity of the integral over the partition, $\int_a^b f - \text{value} = \sum_{\text{panels}} (\int f - K)$ up to rounding. If every panel's true error is at most its estimate, then $\lvert\int_a^b f - \text{value}\rvert \le \sum e = \text{errsum}$, and on status "ok" this is at most the tolerance. The hypothesis is the heuristic of Claim 4, so "ok" is a statement about the estimates, not a proved error bound. $\blacksquare$
