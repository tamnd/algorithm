---
title: Sturm counts are exact for a nearby matrix, and bisection keeps the k-th eigenvalue bracketed
proves: [correctness, termination]
status: full
---

Notation of the page: $T$ is real symmetric tridiagonal of order $n$ with diagonal $a_1, \dots, a_n$ and off-diagonal $b_1, \dots, b_{n-1}$; its eigenvalues in increasing order are $\mu_1 \le \dots \le \mu_n$ (so $\mu_k = \lambda_{n+1-k}$ in the decreasing order of the area); $c(x) = \#\{i : \mu_i < x\}$. The pivots are $d_1 = a_1 - x$ and $d_i = (a_i - x) - b_{i-1}^2 / d_{i-1}$.

**Lemma 1 (pivots and minors).** Let $p_0 = 1$ and $p_i(x) = \det(T_i - x I)$ for the leading $i \times i$ block $T_i$. Then $p_i = (a_i - x) p_{i-1} - b_{i-1}^2 p_{i-2}$, and if $p_1, \dots, p_{i-1} \ne 0$, then $d_i = p_i / p_{i-1}$.

*Proof.* Expanding $\det(T_i - xI)$ along the last row gives the recurrence. Then $p_i / p_{i-1} = (a_i - x) - b_{i-1}^2 p_{i-2}/p_{i-1} = (a_i - x) - b_{i-1}^2 / d_{i-1}$ by induction. $\square$

**Theorem 1 (the count).** If all pivots $d_1, \dots, d_n$ are nonzero, then the number of negative pivots equals $c(x)$.

*Proof.* When all $d_i \ne 0$, Gaussian elimination without pivoting gives $T - xI = L D L^T$ with $L$ unit lower bidiagonal ($l_{i+1,i} = b_i / d_i$) and $D = \operatorname{diag}(d_1, \dots, d_n)$, which is checked entry by entry: the $(i+1, i)$ entry is $l_{i+1,i} d_i = b_i$ and the $(i+1, i+1)$ entry is $l_{i+1,i}^2 d_i + d_{i+1} = b_i^2/d_i + d_{i+1} = a_{i+1} - x$. By Sylvester's law of inertia, $T - xI$ and $D$ have the same number of negative eigenvalues. The eigenvalues of $T - xI$ are $\mu_i - x$, so that number is $c(x)$. $\square$

If $x$ is not an eigenvalue of any leading block, all pivots are nonzero. The implementation replaces a pivot with $|d_i| < \pi_{\min}$ by $-\pi_{\min}$, where $\pi_{\min} = \text{SAFMIN} \cdot \max(1, \max_i b_i^2)$. In exact arithmetic this is the count for $x$ replaced by a point within a distance of order $\pi_{\min}$, and it keeps $b_i^2 / d_i$ finite: $b_i^2 / \pi_{\min} \le 1 / \text{SAFMIN}$ does not overflow.

**Theorem 2 (floating point, Kahan 1966).** In IEEE arithmetic, the computed count at $x$ is the exact count $\tilde c(x)$ of a matrix $\tilde T$ with the same diagonal and off-diagonal entries $\tilde b_i = b_i (1 + \eta_i)$, $|\eta_i| \le 2.5 u + O(u^2)$, up to the replacement of tiny pivots described above.

*Proof.* Write $\epsilon_j$ for rounding errors with $|\epsilon_j| \le u$. Step $i$ computes $t = (a_i - x)(1 + \epsilon_1)$, $s = b_{i-1}^2 (1 + \epsilon_2)$, $q = (s / \hat d_{i-1})(1 + \epsilon_3)$ and $\hat d_i = (t - q)(1 + \epsilon_4)$. Define the scaled pivots $d'_i = \hat d_i / ((1 + \epsilon_1)(1 + \epsilon_4))$, which have the signs of $\hat d_i$. Then $\hat d_{i-1} = d'_{i-1} (1 + \epsilon'_1)(1 + \epsilon'_4)$ with the errors of step $i - 1$, and
$$d'_i = (a_i - x) - \frac{b_{i-1}^2 (1 + \epsilon_2)(1 + \epsilon_3)}{(1 + \epsilon_1)(1 + \epsilon'_1)(1 + \epsilon'_4)} \cdot \frac{1}{d'_{i-1}}.$$
So the $d'_i$ are the exact pivots of the matrix with the same diagonal and $\tilde b_{i-1}^2 = b_{i-1}^2 \cdot (1 + \epsilon_2)(1 + \epsilon_3) / ((1 + \epsilon_1)(1 + \epsilon'_1)(1 + \epsilon'_4))$. This is five factors of the form $1 + O(u)$, so $\tilde b_{i-1} = b_{i-1}(1 + \eta_{i-1})$ with $|\eta_{i-1}| \le 2.5 u + O(u^2)$. The computed and the exact pivots have the same signs, so the counts agree (Kahan 1966; Demmel, Section 5.3.4). $\square$

By [Weyl's inequality](/weyls-inequality/), $|\tilde\mu_k - \mu_k| \le \|\tilde T - T\|_2 \le 2 \cdot 2.5 u \max_i |b_i| + O(u^2)$, an absolute error of order $u \|T\|_2$. For classes of matrices whose eigenvalues are determined to high relative accuracy by relative changes of the $b_i$ (for example zero diagonal, the case of a bidiagonal SVD), the eigenvalues of $\tilde T$ are relatively close to those of $T$ and bisection gives high relative accuracy (Demmel and Kahan 1990). In IEEE arithmetic the computed count is also a monotone function of $x$ (Demmel, Dhillon and Ren 1995), which the bracketing argument below uses.

**Theorem 3 (bisection invariant).** Let the loop start with $c(\ell) < k \le c(h)$ for $\ell < h$. If each step sets $h \leftarrow x$ when $c(x) \ge k$ and $\ell \leftarrow x$ otherwise, then $c(\ell) < k \le c(h)$ holds after each step, and so $\mu_k \in [\ell, h)$.

*Proof.* The update keeps the two inequalities by construction. $c(\ell) < k$ means fewer than $k$ eigenvalues lie below $\ell$, so $\mu_k \ge \ell$. $c(h) \ge k$ means at least $k$ eigenvalues lie below $h$, so $\mu_k < h$. $\square$

**The start.** By the [Gershgorin theorem](/gershgorin-circle-theorem/), every eigenvalue lies in $[g_\ell, g_h]$ with $g_\ell = \min_i (a_i - |b_{i-1}| - |b_i|)$ and $g_h = \max_i (a_i + |b_{i-1}| + |b_i|)$. The code widens this interval by $2 n u \max(|g_\ell|, |g_h|) + 2\pi_{\min}$, which covers the perturbations of Theorem 2 and the pivot replacement, so that the computed counts satisfy $c(\ell) = 0 < k \le n = c(h)$.

**Termination and the result.** Each step halves $h - \ell$, as long as the midpoint is a floating-point number strictly between $\ell$ and $h$. So after $s$ steps $h - \ell = 2^{-s}(h_0 - \ell_0)$, and the loop stops after at most $\lceil \log_2((h_0 - \ell_0)/\tau) \rceil$ steps for an absolute tolerance $\tau > 0$. With $\tau = 0$ it stops when the relative width reaches $2u$ or no floating-point number lies strictly between $\ell$ and $h$, which happens after at most about $2100$ steps (the exponent range plus the 53 binary digits of the significand). The returned midpoint is within $(h - \ell)/2$ of the $k$-th eigenvalue of the matrix $\tilde T$ of Theorem 2.
