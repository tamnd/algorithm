---
title: LPC by the autocorrelation method gives the optimal predictor and a stable synthesis filter
proves: [correctness]
status: full
---

Let $s[n] = w[n]\, x[n]$ for $0 \le n \le N - 1$ and $s[n] = 0$ otherwise, as in line L1, and assume that $s$ is not identically zero. For every integer $k \ge 0$ let $r[k] = \sum_{n} s[n]\, s[n-k]$, summed over all integers $n$; for $0 \le k \le p$ this is the value of line L2, because the other terms are zero. Write $R_m = (r[|i - j|])_{i,j=1}^{m}$ and $\rho_m = (r[1], \ldots, r[m])^T$. We work in exact real arithmetic, as in the real RAM.

**Lemma 1 (positive definiteness).** For every $m \ge 1$, $R_m$ is positive definite. The same holds for the Hermitian form $c^H R_m c$ with complex $c \ne 0$.

*Proof.* For $c \in \mathbb{C}^m$, let $g[n] = \sum_{j=1}^{m} c_j\, s[n - j]$, a sequence with finite support. Then

$$\sum_n |g[n]|^2 = \sum_{j,l} \bar c_j c_l \sum_n s[n-j]\, s[n-l] = \sum_{j,l} \bar c_j c_l\, r[|j - l|] = c^H R_m c,$$

because $\sum_n s[n-j]\, s[n-l] = r[|j-l|]$ after the change of index $n \to n + \min(j, l)$. So $c^H R_m c \ge 0$. If it is zero, then $g = 0$. In terms of polynomials in $z^{-1}$, $g$ is the product of $C(z) = \sum_j c_j z^{-j}$ and $S(z) = \sum_n s[n] z^{-n}$, and the product of two nonzero polynomials is not zero. As $S \ne 0$, we get $C = 0$, that is $c = 0$. $\square$

**Lemma 2 (the error as a quadratic form).** For $a \in \mathbb{C}^p$ let $e_a[n] = s[n] - \sum_{k=1}^{p} a_k\, s[n-k]$ and $E(a) = \sum_n |e_a[n]|^2$. Let $a^\ast$ be the solution of $R_p a^\ast = \rho_p$, which exists and is real by Lemma 1. Then

$$E(a) = r[0] - \rho_p^T a^\ast + (a - a^\ast)^H R_p (a - a^\ast).$$

So $a^\ast$ is the unique minimizer of $E$ over $\mathbb{C}^p$, and the minimum is $E_p = r[0] - \rho_p^T a^\ast$.

*Proof.* Expanding as in Lemma 1, $E(a) = r[0] - a^H \rho_p - \rho_p^T a + a^H R_p a$. Substitute $\rho_p = R_p a^\ast$ and complete the square: $a^H R_p a - a^H R_p a^\ast - a^{\ast T} R_p a = (a - a^\ast)^H R_p (a - a^\ast) - a^{\ast T} R_p a^\ast$, and $a^{\ast T} R_p a^\ast = \rho_p^T a^\ast$. Uniqueness follows from Lemma 1. $\square$

**Lemma 3 (one pass of the loop).** Let $1 \le i \le p$. Suppose that before pass $i$, the vector $a = (a_1, \ldots, a_{i-1})$ solves $R_{i-1} a = \rho_{i-1}$ (empty for $i = 1$) and $E = r[0] - \rho_{i-1}^T a$. Then $E > 0$, and after lines L6 to L8 the new vector $a'$ solves $R_i a' = \rho_i$ and the new value is $E' = r[0] - \rho_i^T a' = (1 - k_i^2) E$, again positive, so $|k_i| < 1$.

*Proof.* Let $J$ be the reversal matrix of size $i - 1$. A symmetric Toeplitz matrix satisfies $J R_{i-1} J = R_{i-1}$. Block $R_i$ as

$$R_i = \begin{bmatrix} R_{i-1} & J \rho_{i-1} \\ \rho_{i-1}^T J & r[0] \end{bmatrix}.$$

First, $E = r[0] - \rho_{i-1}^T R_{i-1}^{-1} \rho_{i-1}$ is the Schur complement of $R_{i-1}$ in $R_i$ (using $J R_{i-1}^{-1} J = R_{i-1}^{-1}$), so $\det R_i = E \det R_{i-1}$, and Lemma 1 gives $E > 0$. Line L6 sets $k_i = (r[i] - \rho_{i-1}^T J a)/E$, since $\sum_{j=1}^{i-1} a_j\, r[i-j] = \rho_{i-1}^T J a$. Line L7 sets $a' = (a - k_i J a,\ k_i)$. The first $i - 1$ rows of $R_i a'$ are

$$R_{i-1}(a - k_i J a) + k_i J \rho_{i-1} = \rho_{i-1} - k_i J R_{i-1} a + k_i J \rho_{i-1} = \rho_{i-1},$$

using $R_{i-1} J = J R_{i-1}$ and $R_{i-1} a = \rho_{i-1}$. The last row is $\rho_{i-1}^T J (a - k_i J a) + k_i r[0] = \rho_{i-1}^T J a + k_i (r[0] - \rho_{i-1}^T a) = \rho_{i-1}^T J a + k_i E = r[i]$, by the choice of $k_i$. So $R_i a' = \rho_i$. Finally

$$r[0] - \rho_i^T a' = r[0] - \rho_{i-1}^T a + k_i\, \rho_{i-1}^T J a - k_i\, r[i] = E - k_i (r[i] - \rho_{i-1}^T J a) = E - k_i^2 E,$$

which is the value of line L8. It is positive by the first part of the argument applied to $R_{i+1}$, which is positive definite by Lemma 1 for every size. As $E > 0$ and $(1 - k_i^2) E > 0$, $|k_i| < 1$. $\square$

**Theorem 1 (the analysis).** If $s \ne 0$, LPC-ANALYZE returns the unique minimizer $a$ of $E(a)$ over $\mathbb{C}^p$, the minimum $E_p > 0$, and reflection coefficients with $|k_i| < 1$ for all $i$. If $s = 0$, it returns at line L3.

*Proof.* If $s = 0$ then $r[0] = \sum_n s[n]^2 = 0$, and conversely $r[0] = 0$ forces $s = 0$; so line L3 returns exactly for the silent frames. Otherwise line L4 sets $a$ to the empty vector and $E = r[0] > 0$, which is the hypothesis of Lemma 3 for $i = 1$. By induction on $i$ with Lemma 3, after pass $p$ the vector $a$ solves $R_p a = \rho_p$ and $E = r[0] - \rho_p^T a > 0$, with $|k_i| < 1$ at each pass. By Lemma 2 this $a$ is the unique minimizer and $E = E_p$. $\square$

**Theorem 2 (stability).** If $s \ne 0$, every zero $z_0 \in \mathbb{C}$ of $A(z) = 1 - \sum_{k=1}^{p} a_k z^{-k}$, that is every root of $z^p - \sum_k a_k z^{p-k}$, satisfies $|z_0| < 1$.

*Proof.* Let $z_0$ be a root. Divide: $A(z) = (1 - z_0 z^{-1})\, C(z)$ with $C(z) = 1 + \sum_{k=1}^{p-1} c_k z^{-k}$ and complex $c_k$ (for $p = 1$, $C = 1$). For $\beta \in \mathbb{C}$, the polynomial $A_\beta(z) = (1 - \beta z^{-1})\, C(z)$ is also of the form $1 - \sum_{k=1}^{p} b_k z^{-k}$ for some $b \in \mathbb{C}^p$, and $A_{z_0} = A$. Let $g$ be the sequence with $z$-transform $C(z) S(z)$; it has finite support, and $g \ne 0$ because $C \ne 0$ and $S \ne 0$. The error sequence of $A_\beta$ is $g[n] - \beta\, g[n-1]$, so its energy is

$$f(\beta) = \sum_n |g[n] - \beta g[n-1]|^2 = \gamma_0 (1 + |\beta|^2) - 2\,\mathrm{Re}(\bar\beta\, \gamma_1), \qquad \gamma_0 = \sum_n |g[n]|^2 > 0,\quad \gamma_1 = \sum_n g[n]\, \overline{g[n-1]}.$$

Completing the square, $f(\beta) = \gamma_0 |\beta - \gamma_1/\gamma_0|^2 + \gamma_0 - |\gamma_1|^2/\gamma_0$, so $f$ has the unique minimizer $\beta^\ast = \gamma_1/\gamma_0$. By Theorem 1 and Lemma 2, the coefficient vector of $A = A_{z_0}$ is the unique minimizer of the error energy over all of $\mathbb{C}^p$, so $f(z_0) \le f(\beta)$ for every $\beta$, and the minimizer of $f$ is $z_0$. Hence $z_0 = \gamma_1/\gamma_0$.

By the Cauchy-Schwarz inequality, $|\gamma_1| \le (\sum_n |g[n]|^2)^{1/2} (\sum_n |g[n-1]|^2)^{1/2} = \gamma_0$. Equality would need the sequences $(g[n])_n$ and $(g[n-1])_n$ to be parallel, $g[n] = \lambda\, g[n-1]$ for all $n$ and some $\lambda$ (the second sequence is not zero). Let $n_1$ be the largest index with $g[n_1] \ne 0$; then $0 = g[n_1 + 1] = \lambda\, g[n_1]$ gives $\lambda = 0$, and then $g = 0$, a contradiction. So $|\gamma_1| < \gamma_0$, and $|z_0| < 1$. $\blacksquare$

**Synthesis.** Line L12 is the difference equation of $G/A(z)$ with zero initial state. Its impulse response is causal, and because all poles of $1/A(z)$, the zeros of $A$, lie in $|z| < 1$ by Theorem 2, the impulse response is absolutely summable, so the filter is BIBO stable. If the excitation is $e = e_a / G$ for the residual $e_a$ of Lemma 2, line L12 gives $\hat s[n] = e_a[n] + \sum_k a_k \hat s[n-k]$, and by induction on $n$, $\hat s = s$: the synthesis inverts the analysis filter.
