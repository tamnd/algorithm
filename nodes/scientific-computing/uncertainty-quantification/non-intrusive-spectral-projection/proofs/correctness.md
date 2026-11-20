---
title: The Golub-Welsch rule is exact to degree 2m - 1, so NISP recovers every polynomial of low enough degree and its error is pure aliasing
proves: [correctness, termination]
status: full
---

We assume exact arithmetic, including an exact symmetric eigendecomposition in line L1. Each input $\xi_k$ has a law $\rho_k$ that is symmetric about 0 with all moments finite and with infinitely many points in its support, the inputs are independent, and $\psi_0 = 1, \psi_1, \psi_2, \ldots$ are the orthonormal polynomials of one law, with $\deg \psi_n = n$. For the two laws of the reference code they satisfy the three term recurrence

$$x\, \psi_{n-1}(x) = b_n \psi_n(x) + b_{n-1} \psi_{n-2}(x), \qquad n \ge 1,$$

with $\psi_{-1} = 0$ and $b_n > 0$: $b_n = \sqrt{n}$ for the standard normal law, from $x \mathrm{He}_{n-1} = \mathrm{He}_n + (n - 1) \mathrm{He}_{n-2}$ and $\psi_n = \mathrm{He}_n / \sqrt{n!}$, and $b_n = n / \sqrt{(2n-1)(2n+1)}$ for the uniform law on $[-1, 1]$, from $n P_n = (2n - 1) x P_{n-1} - (n - 1) P_{n-2}$ and $\psi_n = \sqrt{2n+1}\, P_n$. Both follow by direct substitution.

**Lemma 1 (Golub-Welsch).** Let $J$ be the symmetric tridiagonal $m \times m$ matrix with zero diagonal and off-diagonal $b_1, \ldots, b_{m-1}$, and let $(x_j, v_j)$, $j = 1, \ldots, m$, be its eigenpairs with $\|v_j\| = 1$. Then each $x_j$ is a zero of $\psi_m$, the $x_j$ are distinct, and $w_j = (v_j)_1^2 = 1 / \sum_{n=0}^{m-1} \psi_n(x_j)^2$.

*Proof.* Write $\Psi(x) = (\psi_0(x), \ldots, \psi_{m-1}(x))^{\mathsf T}$. The recurrence for $n = 1, \ldots, m$ reads $x \Psi(x) = J \Psi(x) + b_m \psi_m(x)\, e_m$. Take an eigenpair $(\lambda, v)$. Row $i < m$ of $J v = \lambda v$ is $b_{i-1} v_{i-1} + b_i v_{i+1} = \lambda v_i$; since $b_i > 0$, it determines $v_{i+1}$ from $v_1, \ldots, v_i$, by the same rule as the recurrence determines $\psi_i(\lambda)$. So $v = v_1 \Psi(\lambda)$, and $v_1 \ne 0$ because $v \ne 0$. Then row $m$ gives $b_m \psi_m(\lambda) v_1 = 0$, so $\psi_m(\lambda) = 0$. The eigenspace of $\lambda$ is spanned by $\Psi(\lambda)$, so it has dimension 1; as $J$ is symmetric, its $m$ eigenvalues are then distinct. Finally $1 = \|v\|^2 = v_1^2\, \|\Psi(\lambda)\|^2$. $\square$

**Lemma 2 (discrete orthonormality).** For $0 \le a, b \le m - 1$, $\sum_{j} w_j\, \psi_a(x_j)\, \psi_b(x_j) = \delta_{ab}$.

*Proof.* By Lemma 1, $(v_j)_{a+1} = \sqrt{w_j}\, \psi_a(x_j)$ up to the common sign of $v_j$. The matrix $V = [v_1, \ldots, v_m]$ is orthogonal, so its rows are orthonormal as well: $\sum_j (v_j)_{a+1} (v_j)_{b+1} = \delta_{ab}$. $\square$

**Lemma 3 (Gauss exactness).** For every polynomial $f$ of degree at most $2m - 1$, $\sum_j w_j f(x_j) = \mathbb{E}[f(\xi)]$.

*Proof.* Divide: $f = \psi_m s + r$ with $\deg s \le m - 1$ and $\deg r \le m - 1$. Since $s$ is a combination of $\psi_0, \ldots, \psi_{m-1}$, orthogonality gives $\mathbb{E}[\psi_m s] = 0$, so $\mathbb{E}[f] = \mathbb{E}[r]$. Write $r = \sum_{a < m} r_a \psi_a$; then $\mathbb{E}[r] = r_0$. On the quadrature side, $\psi_m(x_j) = 0$ by Lemma 1, so $\sum_j w_j f(x_j) = \sum_a r_a \sum_j w_j \psi_a(x_j) \psi_0(x_j) = r_0$ by Lemma 2 with $b = 0$. $\square$

With $f = 1$, the weights sum to 1.

**Lemma 4 (tensor exactness).** Let $Q_m[g] = \sum_{j_1, \ldots, j_d} w^1_{j_1} \cdots w^d_{j_d}\, g(x^1_{j_1}, \ldots, x^d_{j_d})$ be the tensor rule of lines L3 to L5. If $g$ is a polynomial whose degree in each variable is at most $2m - 1$, then $Q_m[g] = \mathbb{E}[g(\xi)]$.

*Proof.* $Q_m$ and $\mathbb{E}$ are both linear, so it suffices to take $g = \prod_k g_k(\xi_k)$ with $\deg g_k \le 2m - 1$. Then $Q_m[g] = \prod_k \sum_j w^k_j g_k(x^k_j) = \prod_k \mathbb{E}[g_k(\xi_k)]$ by Lemma 3, and this equals $\mathbb{E}[g]$ by independence. $\square$

**Lemma 5 (what line L5 computes).** After the loop, $\tilde c_\alpha = Q_m[q\, \Psi_\alpha]$ for every $\alpha \in \Lambda$.

*Proof.* Each node of the tensor grid is visited exactly once in line L3, with its product weight, and line L5 adds $w\, q(x)\, \Psi_\alpha(x)$ to $\tilde c_\alpha$. The sum over all nodes is the definition of $Q_m[q \Psi_\alpha]$. $\square$

**Lemma 6 (aliasing).** Let $m \ge p + 1$, and let $q = \sum_{\beta \in B} c_\beta \Psi_\beta$ be a polynomial, with $B$ finite and $c_\beta = \mathbb{E}[q \Psi_\beta]$. Then for $\alpha \in \Lambda$,

$$\tilde c_\alpha = c_\alpha + \sum_{\beta \in B,\ \beta_k \ge 2m - \alpha_k \text{ for some } k} c_\beta\, Q_m[\Psi_\alpha \Psi_\beta].$$

*Proof.* By Lemma 5 and linearity, $\tilde c_\alpha = \sum_{\beta \in B} c_\beta Q_m[\Psi_\alpha \Psi_\beta]$. If $\alpha_k + \beta_k \le 2m - 1$ for every $k$, then Lemma 4 and orthonormality give $Q_m[\Psi_\alpha \Psi_\beta] = \mathbb{E}[\Psi_\alpha \Psi_\beta] = \delta_{\alpha\beta}$. The term $\beta = \alpha$ is of this kind, because $2 \alpha_k \le 2p \le 2m - 2$. The other terms of this kind are 0, and the terms left are the ones in the sum. $\square$

**Lemma 7 (moments and Sobol indices of the result).** Let $\tilde q = \sum_{\alpha \in \Lambda} \tilde c_\alpha \Psi_\alpha$. Then $\mathbb{E}[\tilde q] = \tilde c_0$ and $\mathrm{Var}[\tilde q] = \sum_{\alpha \ne 0} \tilde c_\alpha^2$. For a nonempty set $u$ of inputs, the Sobol variance of $\tilde q$ for $u$ is $\sum_{\alpha : \{k : \alpha_k > 0\} = u} \tilde c_\alpha^2$.

*Proof.* $\mathbb{E}[\Psi_\alpha] = \mathbb{E}[\Psi_\alpha \Psi_0] = \delta_{\alpha 0}$ and $\mathbb{E}[\tilde q^2] = \sum_\alpha \tilde c_\alpha^2$ by orthonormality. For the Sobol part, group the terms by their set of active inputs: $\tilde q = \sum_u f_u$ with $f_u = \sum_{\{k : \alpha_k > 0\} = u} \tilde c_\alpha \Psi_\alpha$. Each $f_u$ depends only on $\xi_u$, and the integral of $f_u$ over any one $\xi_k$ with $k \in u$ is 0, because $\mathbb{E}[\psi_n] = 0$ for $n \ge 1$. By uniqueness of the Hoeffding-Sobol decomposition, these $f_u$ are its terms, and $\mathrm{Var}[f_u] = \sum \tilde c_\alpha^2$ over its indices by orthonormality. $\square$

**Theorem.** NISP stops after exactly $m^d$ model runs. It returns $\tilde c_\alpha = Q_m[q \Psi_\alpha]$, and the mean and variance of the line L6 are those of $\tilde q$. If $q$ is a polynomial whose degree in each variable is at most $2m - 1 - p$, then $\tilde c_\alpha = c_\alpha$ for every $\alpha \in \Lambda$. In particular, if $m \ge p + 1$ and $q$ has total degree at most $p$, then $\tilde q = q$.

*Proof.* Termination: line L1 runs $d$ eigendecompositions of $m \times m$ matrices, line L2 lists the finite set $\Lambda$, and the loop of line L3 has $m^d$ passes, each with one model run and $|\Lambda|$ updates. The value of $\tilde c_\alpha$ is Lemma 5, and the moments are Lemma 7. If $q$ has degree at most $2m - 1 - p$ in each variable, then $q \Psi_\alpha$ has degree at most $2m - 1$ in each variable, since $\alpha_k \le p$; Lemma 4 gives $\tilde c_\alpha = \mathbb{E}[q \Psi_\alpha] = c_\alpha$. If $m \ge p + 1$ and $q$ has total degree at most $p$, then its degree in each variable is at most $p \le 2m - 1 - p$, and $q = \sum_{\alpha \in \Lambda} c_\alpha \Psi_\alpha$, so $\tilde q = q$. $\blacksquare$

The reference code computes the eigendecomposition by cyclic Jacobi rotations, which converge but do not stop in finitely many steps in exact arithmetic. The code stops at a relative off-diagonal tolerance of $10^{-15}$ or after 100 sweeps, whichever comes first, so it terminates; the nodes and weights are then correct to rounding, and the test checks exactness to degree $2m - 1$ to a relative $10^{-12}$.
