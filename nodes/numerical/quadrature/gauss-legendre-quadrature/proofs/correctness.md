---
title: The safeguarded Newton iteration finds each zero of P_n, and the weight formula 2/((1 - x^2) P_n'(x)^2) gives the Gauss-Legendre weights
proves: [correctness, termination]
status: full
---

We use the notation of the page: $P_n$ is the Legendre polynomial with $P_n(1) = 1$, $\int_{-1}^1 P_m P_n\,dx = \frac{2}{2n+1}\delta_{mn}$, and leading coefficient $k_n = \frac{(2n)!}{2^n (n!)^2}$. The nodes are the zeros $x_1 < \cdots < x_n$ of $P_n$, and the Gauss weights are $\lambda_i = \int_{-1}^1 \ell_i(x)\,dx$, where $\ell_i$ is the Lagrange basis polynomial of the nodes. By the [Gauss quadrature theorem](/gauss-quadrature-theorem/), the rule is exact on polynomials of degree at most $2n - 1$.

## Claim 1: the recurrence and the derivative

Line L4 uses Bonnet's recurrence $(k + 1)P_{k+1} = (2k + 1)x P_k - k P_{k-1}$ with $P_0 = 1$, $P_1 = x$, which defines the Legendre polynomials. Line L5 uses

$$(x^2 - 1)\,P_n'(x) = n\bigl(x P_n(x) - P_{n-1}(x)\bigr).$$

*Proof.* Let $q = (x^2 - 1)P_n' - n x P_n$. The coefficients of $x^{n+1}$ cancel ($n k_n - n k_n = 0$), and $q$ has the parity of $n + 1$, so its coefficient of $x^n$ is $0$ and $\deg q \le n - 1$. For $m \le n - 2$, integration by parts gives $\int_{-1}^1 (x^2 - 1)P_n' P_m = -\int_{-1}^1 P_n \bigl((x^2 - 1)P_m\bigr)' = 0$, because the boundary term vanishes at $\pm 1$ and $((x^2 - 1)P_m)'$ has degree $m + 1 < n$; also $\int x P_n P_m = 0$ since $\deg(x P_m) < n$. So $q$ is orthogonal to $P_0, \ldots, P_{n-2}$, and $q = c P_{n-1}$. At $x = 1$: $q(1) = -n P_n(1) = -n$ and $P_{n-1}(1) = 1$, so $c = -n$. $\square$

## Claim 2: the weight formula

For each node, $\lambda_i = \dfrac{2}{(1 - x_i^2)\,P_n'(x_i)^2}$.

*Proof.* Let $g(x) = P_{n-1}(x)\,P_n(x)/(x - x_i)$, a polynomial of degree $2n - 2$. The rule integrates it exactly. At a node $x_j \ne x_i$, $g(x_j) = 0$; at $x_i$, $g(x_i) = P_{n-1}(x_i)P_n'(x_i)$. So $\int g = \lambda_i P_{n-1}(x_i) P_n'(x_i)$. On the other side, $P_n(x)/(x - x_i)$ has degree $n - 1$ and leading coefficient $k_n$, so it equals $\frac{k_n}{k_{n-1}} P_{n-1} + r$ with $\deg r \le n - 2$, and

$$\int_{-1}^1 g = \frac{k_n}{k_{n-1}} \cdot \frac{2}{2n - 1} = \frac{2n - 1}{n} \cdot \frac{2}{2n - 1} = \frac{2}{n}.$$

Hence $\lambda_i = 2/(n P_{n-1}(x_i) P_n'(x_i))$. At a zero of $P_n$, Claim 1 gives $n P_{n-1}(x_i) = (1 - x_i^2) P_n'(x_i)$, and substituting gives the formula. $\square$

## Claim 3: the brackets

Write the nodes in decreasing order as $\cos\theta_1 > \cdots > \cos\theta_n$ with $0 < \theta_1 < \cdots < \theta_n < \pi$. Bruns' inequality (Szegő, Orthogonal Polynomials, Chapter 6) states

$$\frac{(i - \tfrac12)\pi}{n + \tfrac12} < \theta_i < \frac{i\pi}{n + \tfrac12}, \qquad i = 1, \ldots, n.$$

We use this inequality without proof; the test file checks it for $n$ up to 200. The $n$ intervals are disjoint. Each contains $\theta_i$, and since all zeros of $P_n$ are simple, $P_n$ changes sign exactly once in each bracket $[\cos(i\pi/(n + \frac12)), \cos((i - \frac12)\pi/(n + \frac12))]$ of line L2. The starting point $\cos((i - \frac14)\pi/(n + \frac12))$ is inside it.

## Claim 4: the iteration of lines L3 to L7

*Invariant.* $P_n(lo)$ and $P_n(hi)$ have opposite signs (or one is zero), $lo < hi$, and the $i$-th largest zero lies in $[lo, hi]$. Line L6 keeps this: it replaces $lo$ or $hi$ by the current $x \in (lo, hi)$ according to the sign of $P_n(x)$. The next point is the Newton point when it lies strictly inside $(lo, hi)$ and the midpoint otherwise, so $x$ stays inside the bracket, and every iterate is closer to the zero than the far end of the bracket.

*Convergence.* Near a simple zero, Newton's method converges quadratically, so once $x$ is close enough every step is a Newton step and the number of correct digits roughly doubles per step. Before that, each step shrinks the bracket, and a bisection step halves it. The loop stops when the Newton correction is below $2u|x|$ (line L7), and in any case after at most `max_iter` steps, so it terminates. The returned node is within a few units of rounding of the zero, up to the accuracy with which the recurrence evaluates $P_n$ near the zero.

*Symmetry.* $P_n(-x) = (-1)^n P_n(x)$, so the zeros come in pairs $\pm x$ with equal weights by Claim 2 (line L9). For odd $n$, $P_n(0) = 0$ and line L10 sets the middle node to $0$, with the weight $2/P_n'(0)^2$ from Claim 2.

By Claims 2 to 4, the routine returns the $n$ zeros of $P_n$ in increasing order with their Gauss weights. $\blacksquare$
