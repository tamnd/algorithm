---
title: The Gauss quadrature theorem, with the zeros, the degree 2n - 1, positive weights, uniqueness and the error term
proves: [statement]
status: full
---

We use the hypotheses and notation of the statement: $w \ge 0$ is measurable on $(a, b)$, $w > 0$ on a set of positive measure, all moments $\int_a^b |x|^k w$ are finite, and $\langle f, g \rangle = \int_a^b f g\, w$. $\mathcal{P}_k$ is the set of real polynomials of degree at most $k$, and $I(f) = \langle f, 1 \rangle$.

**Lemma.** If $s$ is a polynomial, $s \ge 0$ on $(a, b)$ and $s \ne 0$, then $\int_a^b s\, w > 0$. *Proof.* $s w \ge 0$, so $\int s w = 0$ would force $s w = 0$ almost everywhere. A nonzero polynomial has finitely many zeros, so $s > 0$ almost everywhere, and then $w = 0$ almost everywhere, which contradicts the hypothesis. $\square$ In particular $\langle p, p \rangle > 0$ for each nonzero polynomial $p$.

**Step 0: $p_n$ exists and is unique.** Gram-Schmidt applied to $1, x, x^2, \ldots$ with the inner product $\langle \cdot, \cdot \rangle$ gives monic $p_0, p_1, \ldots$ with $\langle p_j, p_k \rangle = 0$ for $j \ne k$; it never divides by zero because $\langle p, p \rangle > 0$ for $p \ne 0$ (lemma). Since $p_0, \ldots, p_{n-1}$ span $\mathcal{P}_{n-1}$, $p_n$ is orthogonal to $\mathcal{P}_{n-1}$. If $\tilde p$ is another monic polynomial of degree $n$ orthogonal to $\mathcal{P}_{n-1}$, then $r = p_n - \tilde p \in \mathcal{P}_{n-1}$ and $\langle r, r \rangle = \langle p_n, r \rangle - \langle \tilde p, r \rangle = 0$, so $r = 0$.

**Step 1: the zeros.** Let $z_1 < \cdots < z_k$ be the points of $(a, b)$ where $p_n$ changes sign; $k \le n$. Suppose $k < n$ and set $q(x) = \prod_{j=1}^{k}(x - z_j)$ ($q = 1$ if $k = 0$). Then $q \in \mathcal{P}_{n-1}$, and $p_n q$ does not change sign on $(a, b)$, so $p_n q$ or $-p_n q$ is a nonzero polynomial that is nonnegative on $(a, b)$. By the lemma, $\langle p_n, q \rangle \ne 0$, which contradicts the orthogonality of $p_n$ to $\mathcal{P}_{n-1}$. Hence $k = n$: $p_n$ changes sign at $n$ distinct points of $(a, b)$, and as it has degree $n$ these are all its zeros, each simple. Call them $x_1 < \cdots < x_n$.

**Step 2: interpolatory weights.** Let $\ell_i(x) = \prod_{j \ne i} (x - x_j)/(x_i - x_j)$ and $\lambda_i = \int_a^b \ell_i w$. For $r \in \mathcal{P}_{n-1}$, $r = \sum_i r(x_i)\ell_i$ (Lagrange interpolation is exact on $\mathcal{P}_{n-1}$), so $I(r) = \sum_i \lambda_i r(x_i) = Q_n(r)$.

**Step 3: degree $2n - 1$.** Let $f \in \mathcal{P}_{2n-1}$. Division by $p_n$ gives $f = q p_n + r$ with $q, r \in \mathcal{P}_{n-1}$. Then $I(f) = \langle q, p_n \rangle + I(r) = I(r)$ by orthogonality, and $Q_n(f) = \sum_i \lambda_i (q(x_i) p_n(x_i) + r(x_i)) = Q_n(r)$ because $p_n(x_i) = 0$. By Step 2, $Q_n(r) = I(r)$. So $Q_n(f) = I(f)$.

**Step 4: positive weights.** $\ell_i^2 \in \mathcal{P}_{2n-2}$, so by Step 3, $I(\ell_i^2) = Q_n(\ell_i^2) = \sum_j \lambda_j \ell_i(x_j)^2 = \lambda_i$. The left side is positive by the lemma. With $f = 1$, $\sum_i \lambda_i = I(1)$.

**Step 5: no $n$-node rule has degree $2n$.** For any distinct $y_1, \ldots, y_n$ and any weights, $s(x) = \prod_i (x - y_i)^2 \in \mathcal{P}_{2n}$ gives $Q(s) = 0 < I(s)$.

**Step 6: uniqueness.** Let a rule with distinct nodes $y_1, \ldots, y_n$ and weights $v_i$ be exact on $\mathcal{P}_{2n-1}$. Set $\omega(x) = \prod_i (x - y_i)$. For $q \in \mathcal{P}_{n-1}$, $\omega q \in \mathcal{P}_{2n-1}$, so $\langle \omega, q \rangle = I(\omega q) = \sum_i v_i \omega(y_i) q(y_i) = 0$. So $\omega$ is monic of degree $n$ and orthogonal to $\mathcal{P}_{n-1}$, and Step 0 gives $\omega = p_n$: the nodes are the $x_i$. The rule is exact on $\mathcal{P}_{n-1}$, and on distinct nodes the weights of such a rule are unique (the Vandermonde system is nonsingular), so $v_i = \lambda_i$.

**Step 7: the error term.** Let $[a, b]$ be finite and $f \in C^{2n}[a, b]$. Let $h \in \mathcal{P}_{2n-1}$ be the Hermite interpolant with $h(x_i) = f(x_i)$ and $h'(x_i) = f'(x_i)$. Its error is $f(x) - h(x) = f[x_1, x_1, \ldots, x_n, x_n, x]\, p_n(x)^2$, where the divided difference $g(x) = f[x_1, x_1, \ldots, x_n, x_n, x]$ is a continuous function of $x$ on $[a, b]$ and equals $f^{(2n)}(\xi_x)/(2n)!$ for some $\xi_x \in (a, b)$ (the Hermite-Genocchi formula; Atkinson, Chapter 3). By Step 3, $Q_n(h) = I(h)$, and $Q_n(h) = Q_n(f)$ because $h = f$ at the nodes. So

$$E_n(f) = I(f - h) = \int_a^b g(x)\, p_n(x)^2 w(x)\, dx.$$

Since $p_n^2 w \ge 0$ and $g$ is continuous, the mean value theorem for integrals gives $\eta \in [a, b]$ with $E_n(f) = g(\eta) \langle p_n, p_n \rangle$. The value $g(\eta)$ lies between the minimum and the maximum of $f^{(2n)}/(2n)!$ on $[a, b]$, so by the intermediate value theorem it equals $f^{(2n)}(\xi)/(2n)!$ for some $\xi \in [a, b]$. This is the error formula. $\blacksquare$
