---
title: PVL with q Lanczos steps matches 2q moments of the transfer function
proves: [correctness]
status: full
---

We use the notation of the page. The circuit is $(G + sC)x = b\,u$ with output $y = l^{\mathsf T} x$. For the expansion point $s_0$ with $K = G + s_0 C$ nonsingular, put $A = -K^{-1} C$ and $r = K^{-1} b$. Then for $s = s_0 + \sigma$,

$$H(s) = l^{\mathsf T} (K + \sigma C)^{-1} b = l^{\mathsf T} (I - \sigma A)^{-1} r = \sum_{k \ge 0} m_k \sigma^k, \qquad m_k = l^{\mathsf T} A^k r,$$

for $|\sigma|$ below $1/\rho(A)$, where $\rho(A)$ is the spectral radius. The $m_k$ are the moments at $s_0$.

**The process.** Take nonzero scalars $\rho_1, \eta_1$ and set $v_1 = r/\rho_1$, $w_1 = l/\eta_1$, $d_1 = w_1^{\mathsf T} v_1$. For $k = 1, 2, \ldots$, while $d_k \ne 0$:

$$\alpha_k = \frac{w_k^{\mathsf T} A v_k}{d_k}, \qquad \beta_k = \frac{\eta_k d_k}{d_{k-1}}, \qquad \gamma_k = \frac{\rho_k d_k}{d_{k-1}} \quad (\beta_1 = \gamma_1 = 0),$$

$$\rho_{k+1} v_{k+1} = A v_k - \alpha_k v_k - \beta_k v_{k-1}, \qquad \eta_{k+1} w_{k+1} = A^{\mathsf T} w_k - \alpha_k w_k - \gamma_k w_{k-1}, \qquad d_{k+1} = w_{k+1}^{\mathsf T} v_{k+1},$$

with any nonzero scale factors $\rho_{k+1}, \eta_{k+1}$ (the code uses the largest entry). PVL returns $H_q(s_0 + \sigma) = (l^{\mathsf T} r)\, e_1^{\mathsf T} (I - \sigma T_q)^{-1} e_1$, where $T_q$ is the $q \times q$ tridiagonal matrix with diagonal $\alpha_1, \ldots, \alpha_q$, subdiagonal $\rho_2, \ldots, \rho_q$ and superdiagonal $\beta_2, \ldots, \beta_q$. We assume $d_1, \ldots, d_q \ne 0$, which is the condition that no breakdown occurs.

## The case q = 1

**Theorem 1.** If $l^{\mathsf T} r \ne 0$, then $H_1$ matches $m_0$ and $m_1$.

*Proof.* $T_1 = (\alpha_1)$ with $\alpha_1 = w_1^{\mathsf T} A v_1 / d_1 = l^{\mathsf T} A r / l^{\mathsf T} r$, since the scale factors cancel. So

$$H_1(s_0 + \sigma) = \frac{l^{\mathsf T} r}{1 - \sigma \alpha_1} = l^{\mathsf T} r + (l^{\mathsf T} r)\alpha_1 \sigma + (l^{\mathsf T} r)\alpha_1^2 \sigma^2 + \cdots,$$

whose first two coefficients are $l^{\mathsf T} r = m_0$ and $(l^{\mathsf T} r)\alpha_1 = l^{\mathsf T} A r = m_1$. $\square$

The third coefficient is $m_1^2/m_0$, which is not $m_2$ in general: in the example of the page, $m_0, m_1, m_2 = 1, -3, 8$ and $m_1^2/m_0 = 9$. At $s_0 = 0$ the one pole of the model is $\sigma = 1/\alpha_1 = m_0/m_1$. For an RC circuit with $m_0 = 1$, $T_D = -m_1$ is the [Elmore delay](/elmore-delay/), so the pole is $-1/T_D$.

## The general case

The full result is Feldmann and Freund's (1995). We give a complete proof for the version above, which has no look-ahead.

**Lemma 1 (biorthogonality).** If $d_1, \ldots, d_q \ne 0$, then $w_i^{\mathsf T} v_j = 0$ for all $i \ne j$ with $i, j \le q + 1$.

*Proof.* Induction on $k$: suppose the claim holds for all indices up to $k \le q$; we show $w_i^{\mathsf T} v_{k+1} = 0$ for $i \le k$ (the claim for $w_{k+1}$ against $v_i$ is the same argument with $A^{\mathsf T}$ and $\gamma$). Up to the factor $\rho_{k+1}$,

$$w_i^{\mathsf T} \rho_{k+1} v_{k+1} = w_i^{\mathsf T} A v_k - \alpha_k w_i^{\mathsf T} v_k - \beta_k w_i^{\mathsf T} v_{k-1}.$$

For $i = k$ it is $w_k^{\mathsf T} A v_k - \alpha_k d_k = 0$ by the choice of $\alpha_k$. For $i < k$ write $w_i^{\mathsf T} A v_k = (A^{\mathsf T} w_i)^{\mathsf T} v_k = (\eta_{i+1} w_{i+1} + \alpha_i w_i + \gamma_i w_{i-1})^{\mathsf T} v_k$. If $i = k - 1$, the hypothesis leaves $\eta_k d_k$, and the sum is $\eta_k d_k - \beta_k d_{k-1} = 0$ by the choice of $\beta_k$. If $i \le k - 2$, every index on the right is below $k$, so every term is 0. $\square$

**Matrix form.** With $V_q = (v_1, \ldots, v_q)$, $W_q = (w_1, \ldots, w_q)$ and $D_q = \operatorname{diag}(d_1, \ldots, d_q)$, the recurrences read

$$A V_q = V_q T_q + \rho_{q+1} v_{q+1} e_q^{\mathsf T}, \qquad A^{\mathsf T} W_q = W_q \tilde T_q + \eta_{q+1} w_{q+1} e_q^{\mathsf T},$$

where $\tilde T_q$ has the same diagonal, subdiagonal $\eta_2, \ldots, \eta_q$ and superdiagonal $\gamma_2, \ldots, \gamma_q$. By Lemma 1, $W_q^{\mathsf T} V_q = D_q$, $W_q^{\mathsf T} v_{q+1} = 0$ and $V_q^{\mathsf T} w_{q+1} = 0$. Multiply the first identity by $W_q^{\mathsf T}$ and the transpose of the second by $V_q$:

$$W_q^{\mathsf T} A V_q = D_q T_q = \tilde T_q^{\mathsf T} D_q. \tag{1}$$

**Lemma 2.** For $0 \le j \le q - 1$, $A^j v_1 = V_q T_q^j e_1$, and $A^q v_1 = V_q T_q^q e_1 + c\, v_{q+1}$ for a scalar $c$. In the same way $(A^{\mathsf T})^i w_1 = W_q \tilde T_q^i e_1$ for $0 \le i \le q - 1$.

*Proof.* $T_q$ is tridiagonal, so $T_q^j e_1$ is zero below entry $j + 1$. Suppose $A^j v_1 = V_q T_q^j e_1$ for some $j \le q - 1$. Then $A^{j+1} v_1 = A V_q T_q^j e_1 = V_q T_q^{j+1} e_1 + \rho_{q+1} v_{q+1} (e_q^{\mathsf T} T_q^j e_1)$. The last factor is 0 when $j + 1 \le q - 1$, and it is some scalar when $j + 1 = q$. The case $j = 0$ is $v_1 = V_q e_1$. $\square$

**Theorem 2 (moment matching).** If $d_1, \ldots, d_q \ne 0$, then $m_k = (l^{\mathsf T} r)\, e_1^{\mathsf T} T_q^k e_1$ for $0 \le k \le 2q - 1$. Hence $H(s_0 + \sigma) - H_q(s_0 + \sigma) = O(\sigma^{2q})$.

*Proof.* Write $k = i + j$ with $0 \le i \le q - 1$ and $0 \le j \le q$. By Lemma 2,

$$m_k = \rho_1 \eta_1\, \big((A^{\mathsf T})^i w_1\big)^{\mathsf T} \big(A^j v_1\big) = \rho_1 \eta_1\, e_1^{\mathsf T} (\tilde T_q^{\mathsf T})^i\, W_q^{\mathsf T} \big(V_q T_q^j e_1 + c\, v_{q+1}\big) = \rho_1 \eta_1\, e_1^{\mathsf T} (\tilde T_q^{\mathsf T})^i D_q T_q^j e_1,$$

with $c = 0$ unless $j = q$, and $W_q^{\mathsf T} v_{q+1} = 0$. By (1), $\tilde T_q^{\mathsf T} D_q = D_q T_q$, so $(\tilde T_q^{\mathsf T})^i D_q = D_q T_q^i$, and $m_k = \rho_1 \eta_1 d_1\, e_1^{\mathsf T} T_q^{i+j} e_1$. Finally $\rho_1 \eta_1 d_1 = l^{\mathsf T} r$. The expansion $e_1^{\mathsf T} (I - \sigma T_q)^{-1} e_1 = \sum_k \sigma^k e_1^{\mathsf T} T_q^k e_1$ gives the second claim. $\square$

**Corollary 1 (it is the Padé approximant).** By Cramer's rule, $e_1^{\mathsf T}(I - \sigma T_q)^{-1} e_1 = \det(I - \sigma T_q')/\det(I - \sigma T_q)$, where $T_q'$ is $T_q$ without its first row and column. So $H_q$ is a rational function with a numerator of degree at most $q - 1$ and a denominator of degree at most $q$ with value 1 at $\sigma = 0$, and it matches $2q$ moments. When the $[q-1/q]$ [Padé approximant](/pade-approximation/) of $H$ at $s_0$ exists, it is the unique such function, so $H_q$ is that approximant: the same model that AWE computes from the explicit moments. The two methods differ only in rounding. The poles of $H_q$ are $s_0 + 1/\lambda$ for the nonzero eigenvalues $\lambda$ of $T_q$.

**Corollary 2 (q = N is exact).** If $d_1, \ldots, d_N \ne 0$ for the order $N$ of $A$, then $H_N = H$.

*Proof.* $W_N^{\mathsf T} V_N = D_N$ is nonsingular, so $V_N$ and $W_N$ are. Then $W_N^{\mathsf T} \rho_{N+1} v_{N+1} = 0$ forces the vector $\rho_{N+1} v_{N+1}$ to vanish, so $A V_N = V_N T_N$, and $A = V_N T_N V_N^{-1}$. With $V_N^{-1} r = \rho_1 e_1$ and $l^{\mathsf T} V_N = \eta_1 w_1^{\mathsf T} V_N = \eta_1 d_1 e_1^{\mathsf T}$, $l^{\mathsf T}(I - \sigma A)^{-1} r = \rho_1 \eta_1 d_1\, e_1^{\mathsf T}(I - \sigma T_N)^{-1} e_1$. $\square$

## What is not proved

- **Breakdown.** If some $d_k = 0$ while $v_k, w_k \ne 0$, the process stops; the $[q-1/q]$ approximant may then not exist, or may need a look-ahead variant of the Lanczos process, which Feldmann and Freund use. The code reports the breakdown.
- **Rounding.** In floating point the vectors lose their biorthogonality, as in every Lanczos process. The tests measure the accuracy on two lines; they do not prove a bound.
- **Stability and passivity.** A Padé model of a stable or passive circuit can have poles in the right half plane, or fail to be passive. The theorem says nothing about that; PRIMA, a congruence method, was designed to keep passivity.
