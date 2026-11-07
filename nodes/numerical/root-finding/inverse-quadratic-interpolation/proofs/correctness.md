---
title: Error equation, local convergence and order of inverse quadratic interpolation
proves: [correctness, termination, convergence-rate]
status: full
---

We work in exact real arithmetic. Let $x^*$ be a simple root: $f(x^*) = 0 \ne f'(x^*)$, and let $f$ be $C^3$ on an interval $I = [x^* - \rho, x^* + \rho]$ on which $f' \ne 0$. Then $f$ is strictly monotone on $I$, $J = f(I)$ is an interval that holds 0 in its interior, and the inverse $g = f^{-1} : J \to I$ is $C^3$ with $g(0) = x^*$.

**Lemma 1 (the step).** If $x_0, x_1, x_2 \in I$ have distinct values $f_i = f(x_i)$, line L4 returns $p(0)$, where $p$ is the polynomial of degree at most 2 with $p(f_i) = x_i$.

*Proof.* The values are distinct, so $p$ exists and is unique. Newton's form of $p$ at the nodes $f_2, f_1, f_0$ is $p(y) = x_2 + x[f_2, f_1](y - f_2) + x[f_2, f_1, f_0](y - f_2)(y - f_1)$, and at $y = 0$ this is the expression of L4. The Lagrange form is the same polynomial. $\square$

**Lemma 2 (error equation).** Under the hypotheses of Lemma 1, there are $\eta \in J$ and $\xi_0, \xi_1, \xi_2 \in I$ with

$$e_3 = x_3 - x^* = \frac{g'''(\eta)}{6}\, f'(\xi_0) f'(\xi_1) f'(\xi_2)\; e_0 e_1 e_2.$$

*Proof.* Since $x_i = g(f_i)$, $p$ interpolates $g$ at $f_0, f_1, f_2$. The interpolation error formula gives, for $y = 0$, $g(0) - p(0) = \frac{g'''(\eta)}{6}(0 - f_0)(0 - f_1)(0 - f_2)$ for some $\eta$ in the smallest interval that holds $0, f_0, f_1, f_2$, which lies in $J$. So $x_3 - x^* = p(0) - g(0) = \frac{g'''(\eta)}{6} f_0 f_1 f_2$. By the mean value theorem $f_i = f(x_i) - f(x^*) = f'(\xi_i) e_i$. $\square$

Differentiating $g(f(x)) = x$ three times gives $g' = 1/f'$, $g'' = -f''/f'^3$ and $g''' = (3f''^2 - f'f''')/f'^5$, all at matching points. So, as the points tend to $x^*$, the factor in Lemma 2 tends to

$$C = \frac{3f''(x^*)^2 - f'(x^*)f'''(x^*)}{6 f'(x^*)^2}.$$

**Theorem 1 (local convergence).** Let $K = \frac16 \max_J |g'''| \cdot (\max_I |f'|)^3$ and choose $0 < r \le \rho$ with $K r^2 \le 1/2$. If $x_0, x_1, x_2$ are distinct points with $|e_i| \le r$, then either some iterate is exactly $x^*$, or all iterates are defined, $|e_{k+1}| \le \frac12 \max(|e_k|, |e_{k-1}|, |e_{k-2}|)$, and $e_k \to 0$. Moreover $e_{k+1}/(e_k e_{k-1} e_{k-2}) \to C$.

*Proof.* Distinct points of $I$ have distinct values since $f$ is injective on $I$, so the first step is defined, and by Lemma 2, $|e_3| \le K|e_0||e_1||e_2| \le K r^2 \max|e_i| \le \frac12 \max|e_i| \le r/2$. So $x_3 \in I$. If $e_3 = 0$ the method has hit the root (L6). Otherwise $x_3$ differs from $x_0, x_1, x_2$: for instance $x_3 = x_2$ would give $|e_2| = |e_3| \le K r^2 |e_2| \le |e_2|/2$, so $e_2 = 0$, and then $f_2 = 0$ and L6 would have stopped earlier; the same argument applies to $x_1$ and $x_0$. So the next three points are distinct and in the ball, and induction gives the bound at every step. Let $M_j = \max(|e_{3j}|, |e_{3j+1}|, |e_{3j+2}|)$. The bound gives $M_{j+1} \le M_j/2$, so $e_k \to 0$. The limit of the ratio follows from Lemma 2, since $\eta \to 0$ and $\xi_i \to x^*$ and the derivatives are continuous. $\square$

**Theorem 2 (order).** Under Theorem 1, if $C \ne 0$ and no iterate is exact, then $\log|e_{k+1}| / \log|e_k| \to q$, where $q \approx 1.8393$ is the real root of $q^3 = q^2 + q + 1$.

*Proof.* Let $\ell_k = \log|e_k|$. By Theorem 1, $\ell_{k+1} = \ell_k + \ell_{k-1} + \ell_{k-2} + c_k$ with $c_k = \log|C_k| \to \log|C|$, so $|c_k| \le c$ for some $c$. The characteristic polynomial $t^3 - t^2 - t - 1$ has the real root $q > 1$ and two complex roots $\lambda, \bar\lambda$ with $q|\lambda|^2 = 1$ (the product of the roots is 1), so $|\lambda| = q^{-1/2} < 1$. Write the recurrence in the basis of these roots: the components along $\lambda$ and $\bar\lambda$ satisfy $u_{k+1} = \lambda u_k + O(c)$, so they stay bounded, and the component along $q$ satisfies $v_{k+1} = q v_k + O(c)$, so $v_k = A q^k + O(1)$ with $A = \lim v_k / q^k$, which exists because the series $\sum O(c) q^{-k}$ converges. Hence $\ell_k = A q^k + O(1)$. Since $\ell_k \to -\infty$, $A < 0$, and $\ell_{k+1}/\ell_k \to q$. $\square$

In the language of the root-finding pages, the method has order $q = 1.839$ with one evaluation in each step, so its efficiency index is $1.839$. Both theorems are local: they need the three starting points close to $x^*$.

**Termination.** The loop of lines L2 to L7 runs at most $k_{\max}$ times, and each pass returns at L3 or L6 or goes on, so IQI always ends, after at most $k_{\max} + 3$ evaluations. The stop at L6 on a short step is not an error bound; under Theorem 1, $|e_2| \le |x_3 - x_2| + |e_3| \le |x_3 - x_2| + \frac12 \max(|e_0|, |e_1|, |e_2|)$, which bounds the error only together with the earlier errors, and only near the root. $\blacksquare$
