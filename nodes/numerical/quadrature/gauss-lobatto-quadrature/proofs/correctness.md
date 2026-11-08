---
title: The doubly modified Jacobi matrix has the Lobatto nodes as eigenvalues, the eigenvector formula gives the Lobatto weights, and the rule has degree 2n-3 with a definite error term
proves: [correctness, error]
status: full
---

We use the notation of the page. The weight $w$ on $(a, b)$ satisfies the hypotheses of the [Gauss quadrature theorem](/gauss-quadrature-theorem/) with $a < b$ finite; $\pi_k$ are its monic orthogonal polynomials with $\pi_{k+1} = (x - \alpha_k)\pi_k - \beta_k\pi_{k-1}$, $\pi_{-1} = 0$, $\pi_0 = 1$ and $\beta_0 = \int w$. The fixed nodes are $l = a$ and $r = b$. Let $n \ge 2$ and $m = n - 1$.

## Claim 1: the ratios and the modified coefficients

All zeros of every $\pi_k$ lie in $(a, b)$. Hence $\pi_k(a) \ne 0$ and $\pi_k(b) \ne 0$, and since $\pi_k$ is monic, $\operatorname{sign} \pi_k(b) = 1$ and $\operatorname{sign} \pi_k(a) = (-1)^k$. The ratios $r_k(c) = \pi_k(c)/\pi_{k-1}(c)$ satisfy $r_1 = c - \alpha_0$ and, dividing the recurrence by $\pi_k(c)$, $r_{k+1} = (c - \alpha_k) - \beta_k / r_k$; this is what line L1 computes, and no division is by zero. By the signs, $r_a := r_m(a) < 0 < r_b := r_m(b)$.

Line L2 and line L3 solve the two linear conditions

$$(a - \alpha')\pi_m(a) - \beta'\pi_{m-1}(a) = 0, \qquad (b - \alpha')\pi_m(b) - \beta'\pi_{m-1}(b) = 0.$$

Dividing by $\pi_{m-1}(c)$ gives $a - \alpha' = \beta'/r_a$ and $b - \alpha' = \beta'/r_b$. Subtracting, $a - b = \beta'(1/r_a - 1/r_b)$. Both sides are negative ($1/r_a < 0 < 1/r_b$), so $\beta' > 0$ is well defined and positive, and $\alpha' = a - \beta'/r_a$.

## Claim 2: the node polynomial

Let $\tilde\pi_n = (x - \alpha')\pi_m - \beta'\pi_{m-1}$. It is monic of degree $n$ and vanishes at $a$ and $b$ by Claim 1. Also $\tilde\pi_n = \pi_n + (\alpha_m - \alpha')\pi_m + (\beta_m - \beta')\pi_{m-1}$, so $\tilde\pi_n$ is orthogonal to every polynomial of degree at most $n - 3$. Write $\tilde\pi_n = (x - a)(x - b)\,q(x)$ with $q$ monic of degree $n - 2$. For every $s$ of degree at most $n - 3$,

$$\int_a^b q(x)\, s(x)\, (x - a)(b - x)\, w(x)\,dx = -\langle \tilde\pi_n, s \rangle = 0.$$

So $q$ is the monic orthogonal polynomial of degree $n - 2$ for the weight $(x - a)(b - x)w(x)$, which is nonnegative on $(a, b)$, positive on a set of positive measure, and has finite moments. By part 1 of the theorem, the zeros of $q$ are real, simple and lie in $(a, b)$. Hence $\tilde\pi_n$ has $n$ simple zeros: $a$, $b$ and the $n - 2$ zeros of $q$. (For $n = 2$, $q = 1$.)

## Claim 3: degree of precision $2n - 3$

Let $Q$ be the interpolatory rule on the zeros of $\tilde\pi_n$. For $f$ of degree at most $2n - 3$, divide: $f = \tilde\pi_n s + t$ with $\deg s \le n - 3$ and $\deg t \le n - 1$ (for $n = 2$, $s = 0$). Then $I(\tilde\pi_n s) = 0$ by Claim 2, $Q(\tilde\pi_n s) = 0$ because $\tilde\pi_n$ vanishes at all nodes, and $Q(t) = I(t)$ because $Q$ is interpolatory. So $Q(f) = I(f)$.

The degree is not $2n - 2$: $g = (x - a)(x - b)q^2$ has degree $2n - 2$, vanishes at all nodes, and $I(g) = -\int (x - a)(b - x) q^2 w < 0$.

## Claim 4: positive weights

For an interior node $x_j$, the polynomial $(x - a)(b - x)\,\ell_j(x)^2 / ((x_j - a)(b - x_j))$, where $\ell_j$ is the Lagrange basis polynomial of the $n - 2$ interior nodes, has degree $2n - 4 \le 2n - 3$, equals $1$ at $x_j$ and $0$ at every other node, and is nonnegative on $[a, b]$ and positive off a finite set. Its integral is positive and equals $\lambda_j$. For the node $a$, the polynomial $(b - x)\,q(x)^2$ has degree $2n - 3$, vanishes at every node except $a$, and is positive on $[a, b)$ off finitely many points, so $\lambda_a (b - a) q(a)^2 = I((b - x) q^2) > 0$. The node $b$ is the same with $x - a$.

## Claim 5: the matrix computation

The modified matrix $\tilde J$ of line L4 is $J_n$ with last diagonal entry $\alpha'$ and last off-diagonal entry $\sqrt{\beta'}$; it is symmetric tridiagonal with positive off-diagonal entries because $\beta' > 0$. Expanding $\det(xI - \tilde J)$ along the last row gives $(x - \alpha')\det(xI - J_m) - \beta'\det(xI - J_{m-1}) = (x - \alpha')\pi_m - \beta'\pi_{m-1} = \tilde\pi_n$. So the eigenvalues of $\tilde J$ are the nodes of Claim 2, and Sturm-count bisection finds them in increasing order.

For each eigenvalue $x_j$, rows $0$ to $n - 2$ of $\tilde J v = x_j v$ do not contain $\alpha'$, and they contain $\sqrt{\beta'}$ only in row $n - 2$, as the coefficient of $v_{n-1}$. With $v_0 = 1$ these rows determine $v_1, \ldots, v_{n-1}$ by the recurrence that the code runs, and the last row holds because $x_j$ is an eigenvalue. Let $V$ be the orthogonal matrix of unit eigenvectors and $\mu_j = \beta_0/\|v^{(j)}\|^2$, the weight of line L5. For $k \le n - 2$ the components are $v_k^{(j)} = \sqrt{\beta_0}\,p_k(x_j)$ with $p_k$ the orthonormal polynomials, because both follow the same recurrence. The last component is $v_{n-1}^{(j)} = \sqrt{\beta_0}\,\tilde p(x_j)$ with $\tilde p = ((x - \alpha_{m-1})p_{m-1} - \sqrt{\beta_{m-1}}\,p_{m-2})/\sqrt{\beta'}$, which equals $\sqrt{\beta_m/\beta'}\;p_m$, a polynomial of degree $n - 1$.

The rows of $V$ are orthonormal. Rows $0$ to $n - 2$ give, for $k, l \le n - 2$,

$$\sum_j \mu_j\, p_k(x_j)\, p_l(x_j) = (VV^T)_{kl} = \delta_{kl} = \langle p_k, p_l \rangle,$$

so the rule $(x_j, \mu_j)$ integrates exactly every polynomial of degree at most $2n - 4$. Row $n - 1$ against row $0$ gives $\sum_j \mu_j\, p_m(x_j) = 0 = \langle p_m, p_0 \rangle$, and against row $k$ with $1 \le k \le n - 2$ gives the same for $p_m p_k$. So the rule is also exact for $p_m p_k$ with $k \le n - 2$, which together with the above spans all polynomials of degree at most $2n - 3$. The Lagrange basis polynomials of the $n$ nodes have degree $n - 1 \le 2n - 3$, so $\mu_j = \lambda_j$. Line L6 replaces the computed first and last eigenvalues by $a$ and $b$; by Claim 2 these are exactly the smallest and largest eigenvalues.

## Claim 6: the error term

Let $f \in C^{2n-2}[a, b]$. Let $h$ be the polynomial of degree at most $2n - 3$ that interpolates $f$ at $a$ and $b$ and $f, f'$ at the $n - 2$ interior nodes ($2 + 2(n - 2) = 2n - 2$ conditions). Then

$$f(x) - h(x) = f[a, b, x_1, x_1, \ldots, x_{n-2}, x_{n-2}, x]\,(x - a)(x - b)\,q(x)^2,$$

the divided difference is continuous in $x$, and $(x - a)(x - b)q^2 \le 0$ on $[a, b]$. The rule is exact on $h$ by Claim 3 and $Q(f) = Q(h)$ because $f = h$ at the nodes. By the mean value theorem for integrals and the mean value property of divided differences,

$$E_n(f) = \frac{f^{(2n-2)}(\xi)}{(2n-2)!} \int_a^b (x - a)(x - b)\,q(x)^2\,w(x)\,dx, \qquad \xi \in [a, b].$$

The integral is negative. For $w = 1$ on $[-1, 1]$, applying this to $f = x^{2n-2}$ (for which $f^{(2n-2)} = (2n-2)!$ is constant) gives $E_n(x^{2n-2}) = \int (x^2 - 1) q^2$, and for Legendre-Lobatto the classical evaluation of this integral, which we do not reproduce here, gives the constant $c_n = -\frac{n(n-1)^3\, 2^{2n-1}\,((n-2)!)^4}{(2n-1)\,((2n-2)!)^3}$ of the page, which the test file checks against the computed rule for $n \le 12$. For $n = 3$, $c_3 = -\frac{1}{90}$, the error constant of Simpson's rule on $[-1, 1]$. $\blacksquare$
