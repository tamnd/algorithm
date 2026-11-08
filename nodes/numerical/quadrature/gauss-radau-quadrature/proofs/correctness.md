---
title: The modified Jacobi matrix has the Radau nodes as eigenvalues, the eigenvector formula gives the Radau weights, and the rule has degree 2n-2 with a definite error term
proves: [correctness, error]
status: full
---

We use the notation of the page. The weight $w$ on $(a, b)$ satisfies the hypotheses of the [Gauss quadrature theorem](/gauss-quadrature-theorem/); $\pi_k$ are its monic orthogonal polynomials with $\pi_{k+1} = (x - \alpha_k)\pi_k - \beta_k\pi_{k-1}$ and $\beta_0 = \int w$. The fixed node $c$ is the left end $a$ (finite). The case of the right end is the same with the signs noted at the end. Let $n \ge 2$; for $n = 1$ the rule is $Q_1(f) = \beta_0 f(c)$, exact on constants.

## Claim 1: the node polynomial

All zeros of $\pi_k$ lie in $(a, b)$, so $\pi_k(c) \ne 0$ for every $k$ and line L2 is well defined. Let $\tilde\pi_n = (x - \alpha')\pi_{n-1} - \beta_{n-1}\pi_{n-2}$ with $\alpha'$ from line L3. Then $\tilde\pi_n(c) = 0$ by the choice of $\alpha'$, and $\tilde\pi_n = \pi_n + (\alpha_{n-1} - \alpha')\pi_{n-1}$, so $\tilde\pi_n$ is orthogonal to every polynomial of degree at most $n - 2$. Write $\tilde\pi_n = (x - c)\,q(x)$ with $q$ monic of degree $n - 1$. For every $r$ of degree at most $n - 2$,

$$\int_a^b q(x)\, r(x)\, (x - c)\, w(x)\,dx = \langle \tilde\pi_n, r \rangle = 0.$$

So $q$ is the monic orthogonal polynomial of degree $n - 1$ for the weight $(x - c)w(x)$, which is nonnegative on $(a, b)$ and satisfies the same hypotheses. By part 1 of the theorem, the zeros of $q$ are real, simple and lie in $(a, b)$. Hence $\tilde\pi_n$ has $n$ simple zeros: $c$ and the $n - 1$ zeros of $q$.

## Claim 2: degree of precision $2n - 2$

Let $Q$ be the interpolatory rule on the zeros of $\tilde\pi_n$. For $f$ of degree at most $2n - 2$, divide: $f = \tilde\pi_n s + t$ with $\deg s \le n - 2$ and $\deg t \le n - 1$. Then $I(\tilde\pi_n s) = 0$ by Claim 1, $Q(\tilde\pi_n s) = 0$ because $\tilde\pi_n$ vanishes at every node, and $Q(t) = I(t)$ because $Q$ is interpolatory. So $Q(f) = I(f)$.

The degree is not $2n - 1$: $g = (x - c)q^2$ has degree $2n - 1$, vanishes at all nodes, and $I(g) = \int (x - c) q^2 w > 0$.

## Claim 3: positive weights

For a free node $x_j$, the square $\ell_j^2$ of its Lagrange basis polynomial has degree $2n - 2$, so $\lambda_j = Q(\ell_j^2) = I(\ell_j^2) > 0$. For the fixed node, $q^2$ has degree $2n - 2$ and vanishes at the free nodes, so $\lambda_c\, q(c)^2 = I(q^2) > 0$ with $q(c) \ne 0$.

## Claim 4: the matrix computation

The modified matrix $\tilde J$ of line L4 equals $J_n$ except in the last diagonal entry, which is $\alpha'$. Expanding $\det(xI - \tilde J)$ along the last row, as for $J_n$, gives $(x - \alpha')\pi_{n-1} - \beta_{n-1}\pi_{n-2} = \tilde\pi_n$. So the eigenvalues of $\tilde J$ are the nodes of Claim 1. $\tilde J$ is symmetric tridiagonal with nonzero off-diagonal entries, so Sturm-count bisection finds its eigenvalues (as on the [Gaussian quadrature](/gaussian-quadrature/) page).

For each eigenvalue $x_j$, the first $n - 1$ rows of $\tilde J v = x_j v$ do not contain $\alpha'$; with $v_0 = 1$ they determine $v_1, \ldots, v_{n-1}$ by the recurrence that the code runs, and the last row holds because $x_j$ is an eigenvalue. Let $V$ be the orthogonal matrix of unit eigenvectors $\hat v_j = v^{(j)}/\|v^{(j)}\|$, and put $\mu_j = \beta_0/\|v^{(j)}\|^2$, the weight of line L5. The components satisfy $v_k^{(j)} = \sqrt{\beta_0}\, p_k(x_j)$ for $k < n$, where $p_k$ are the orthonormal polynomials, because both satisfy the same recurrence and $v_0 = 1 = \sqrt{\beta_0}\,p_0$. The rows of $V$ are orthonormal, so for $k, m < n$,

$$\sum_j \mu_j\, p_k(x_j)\, p_m(x_j) = \sum_j \frac{v^{(j)}_k v^{(j)}_m}{\|v^{(j)}\|^2} = (V V^T)_{km} = \delta_{km} = \langle p_k, p_m \rangle.$$

So the rule with nodes $x_j$ and weights $\mu_j$ integrates every product $p_k p_m$ with $k, m < n$ exactly. These products span all polynomials of degree at most $2n - 2$, and in particular all Lagrange basis polynomials of the nodes, so $\mu_j = \lambda_j$. Line L6 replaces the computed eigenvalue nearest $c$ by $c$ itself, which removes the rounding error in the fixed node.

## Claim 5: the error term

Let $[a, b]$ be finite and $f \in C^{2n-1}[a, b]$. Let $h$ be the polynomial of degree at most $2n - 2$ that interpolates $f$ at $c$ and $f, f'$ at the $n - 1$ free nodes. Then $f - h = f[c, x_1, x_1, \ldots, x_{n-1}, x_{n-1}, x]\,(x - c)q(x)^2$, the divided difference is a continuous function of $x$, and $(x - c)q^2 \ge 0$ on $[a, b]$. The rule is exact on $h$ and $Q(f) = Q(h)$, so by the mean value theorem for integrals and the mean value property of divided differences,

$$E_n(f) = \frac{f^{(2n-1)}(\xi)}{(2n-1)!} \int_a^b (x - c)\,q(x)^2\,w(x)\,dx, \qquad \xi \in [a, b].$$

For $w = 1$ on $[-1, 1]$ and $c = -1$, applying this to $f = x^{2n-1}$ gives the constant $c_n = \frac{2^{2n-1}\,n\,((n-1)!)^4}{((2n-1)!)^3}$ of the page, which the test file checks for $n \le 12$.

*Right endpoint.* For $c = b$ the factor $x - c$ is $\le 0$, so the weight $(c - x)w$ is used in Claim 1, and the error constant in Claim 5 is negative. $\blacksquare$
