---
title: The Chebyshev bound on the error of CG
proves: [matvecs.worst]
status: full
---

Exact arithmetic, notation of the correctness proof. $0 < \lambda_{\min} \le \lambda_{\max}$ are the extreme eigenvalues of $A$ and $\kappa = \lambda_{\max}/\lambda_{\min}$. $\mathcal{P}_k^1$ is the set of real polynomials $q$ of degree at most $k$ with $q(0) = 1$.

**Lemma 1.** As long as CG has not stopped, $\|e_k\|_A = \min_{q \in \mathcal{P}_k^1} \|q(A) e_0\|_A$.

*Proof.* $y \in x_0 + \mathcal{K}_k(A, r_0)$ exactly when $x - y = e_0 - s(A) r_0$ for a polynomial $s$ of degree at most $k - 1$. Since $r_0 = A e_0$, this is $x - y = q(A) e_0$ with $q(t) = 1 - t s(t)$, and the map $s \mapsto q$ is a bijection onto $\mathcal{P}_k^1$. Corollary 1 of the correctness proof says that $x_k$ minimizes $\|x - y\|_A$ over these $y$. $\square$

**Lemma 2.** For each $q$, $\|q(A) e_0\|_A \le \max_{\lambda \in [\lambda_{\min}, \lambda_{\max}]} |q(\lambda)| \, \|e_0\|_A$.

*Proof.* Let $A = V \Lambda V^T$ with $V$ orthogonal and $e_0 = V c$. Then $\|q(A) e_0\|_A^2 = \sum_i \lambda_i q(\lambda_i)^2 c_i^2 \le \max_i q(\lambda_i)^2 \sum_i \lambda_i c_i^2$, and $\sum_i \lambda_i c_i^2 = \|e_0\|_A^2$. Each $\lambda_i$ lies in the interval. $\square$

**Theorem.** $\|e_k\|_A \le 2 \left( \frac{\sqrt\kappa - 1}{\sqrt\kappa + 1} \right)^k \|e_0\|_A$. Consequently $\|e_k\|_A \le \varepsilon \|e_0\|_A$ for each $k \ge \tfrac12 \sqrt\kappa \ln(2/\varepsilon)$, $0 < \varepsilon \le 1$.

*Proof.* If $\kappa = 1$ then $A = \lambda I$, $r_1 = 0$ and the bound holds for $k \ge 1$ (and for $k = 0$ trivially). Let $\kappa > 1$. Let $T_k$ be the Chebyshev polynomial of degree $k$: $T_k(\cos\theta) = \cos(k\theta)$, so $|T_k(t)| \le 1$ on $[-1, 1]$, and for $|t| \ge 1$, $T_k(t) = \tfrac12 \bigl[(t + \sqrt{t^2 - 1})^k + (t - \sqrt{t^2 - 1})^k\bigr]$. Put $\sigma = (\lambda_{\max} + \lambda_{\min})/(\lambda_{\max} - \lambda_{\min}) = (\kappa + 1)/(\kappa - 1) > 1$ and
$$q(\lambda) = \frac{T_k\bigl((\lambda_{\max} + \lambda_{\min} - 2\lambda)/(\lambda_{\max} - \lambda_{\min})\bigr)}{T_k(\sigma)}.$$
Then $q(0) = 1$, $q$ has degree $k$, and the argument of $T_k$ in the numerator lies in $[-1, 1]$ for $\lambda$ in the interval. So $\max |q| \le 1/T_k(\sigma)$ there. Both terms of the formula for $T_k(\sigma)$ are positive, so $T_k(\sigma) \ge \tfrac12 (\sigma + \sqrt{\sigma^2 - 1})^k$. Now $\sigma^2 - 1 = 4\kappa/(\kappa - 1)^2$, so
$$\sigma + \sqrt{\sigma^2 - 1} = \frac{\kappa + 1 + 2\sqrt\kappa}{\kappa - 1} = \frac{(\sqrt\kappa + 1)^2}{(\sqrt\kappa - 1)(\sqrt\kappa + 1)} = \frac{\sqrt\kappa + 1}{\sqrt\kappa - 1}.$$
Lemmas 1 and 2 give the first claim.

For the second, let $t = 1/\sqrt\kappa \in (0, 1)$. Then $\ln\frac{\sqrt\kappa + 1}{\sqrt\kappa - 1} = \ln\frac{1 + t}{1 - t} = 2(t + t^3/3 + t^5/5 + \cdots) \ge 2t$. So $2 \bigl(\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}\bigr)^k \le 2 e^{-2k/\sqrt\kappa} \le \varepsilon$ when $k \ge \tfrac12 \sqrt\kappa \ln(2/\varepsilon)$. $\blacksquare$

**Cost.** Each pass of line L2 does one product with $A$, and the start does one more. So reducing the $A$-norm of the error by $\varepsilon$ takes at most $\lceil \tfrac12 \sqrt\kappa \ln(2/\varepsilon) \rceil + 1$ products in exact arithmetic, and $O((z + n)\sqrt\kappa \log(2/\varepsilon))$ flops for a matrix with $z$ nonzeros.
