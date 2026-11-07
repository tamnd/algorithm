---
title: Muller's method ends, satisfies the cubic error relation, and converges locally with order 1.839
proves: [correctness, termination, local-convergence]
status: full
---

We write $x_{k-2}, x_{k-1}, x_k$ for the three points at the start of a pass and $x_{k+1}$ for the new point $x_3$ of line L9; $e_j = x_j - x^*$. Divided differences of an analytic $f$ at points in a convex set $D$ satisfy the Hermite-Genocchi formula
$$f[z_0, \ldots, z_r] = \int_{\Sigma_r} f^{(r)}(t_0 z_0 + \cdots + t_r z_r)\, dt,$$
over the simplex $\Sigma_r = \{t_i \ge 0, \sum t_i = 1\}$ of volume $1/r!$. It holds for complex points because it follows from integrating derivatives along straight segments, and it gives $|f[z_0, \ldots, z_r]| \le \max_D |f^{(r)}|/r!$.

## Claim 1: termination and the flags

Each pass returns or increases $k$, so the loop ends after at most $k_{\max}$ passes, with 3 evaluations at line L1 and one per pass at line L10. The flags record the tests of lines L1, L10 and L11.

## Claim 2: the error relation

Let $P$ be the parabola of the pass, which interpolates $f$ at $x_{k-2}, x_{k-1}, x_k$, and let $x_{k+1}$ be a root of $P$. The Newton form of the interpolation error gives, for any $x$,
$$f(x) - P(x) = f[x_{k-2}, x_{k-1}, x_k, x](x - x_{k-2})(x - x_{k-1})(x - x_k).$$
At $x = x_{k+1}$, $P(x_{k+1}) = 0$. On the other side, $f(x_{k+1}) = f(x_{k+1}) - f(x^*) = f[x^*, x_{k+1}]\,e_{k+1}$ with $f[x^*, x_{k+1}] = \int_0^1 f'(x^* + t e_{k+1})\,dt$. Hence
$$f[x^*, x_{k+1}]\,e_{k+1} = f[x_{k-2}, x_{k-1}, x_k, x_{k+1}]\,(x_{k+1} - x_{k-2})(x_{k+1} - x_{k-1})(x_{k+1} - x_k).$$
As all points tend to $x^*$, the left factor tends to $f'(x^*)$, the divided difference tends to $f'''(x^*)/6$, and $x_{k+1} - x_j = e_{k+1} - e_j$ with $e_{k+1} = o(e_j)$, so $e_{k+1} \approx -\frac{f'''(x^*)}{6f'(x^*)}e_k e_{k-1}e_{k-2}$.

## Claim 3: local convergence

Let $f$ be analytic on the closed disc $B_R = \{|x - x^*| \le R\}$ with $f(x^*) = 0$ and $\mu = |f'(x^*)| > 0$. Let $M_j = \max_{B_R}|f^{(j)}|/j!$ for $j = 2, 3$. Choose $\rho > 0$ with $7\rho \le R$, with $|f'(x) - f'(x^*)| \le \mu/4$ on $B_{7\rho}$, with $2\rho M_2 \le \mu/4$, and with $\frac{4 \cdot 343\, M_3}{3\mu}\rho^2 \le \frac12$.

Suppose the three current points are distinct and lie in $B_\rho$, and let $\varepsilon = \max(|e_{k-2}|, |e_{k-1}|, |e_k|) \le \rho$.

*The step is defined and short.* By line L5, $b = f[x_{k-1}, x_k] + (x_k - x_{k-1}) f[x_{k-2}, x_{k-1}, x_k]$. The first term is the mean of $f'$ over a segment in $B_\rho$, so it is within $\mu/4$ of $f'(x^*)$. The second has modulus at most $2\rho M_2 \le \mu/4$. So $|b| \ge \mu/2$. Since $|b + s|^2 + |b - s|^2 = 2|b|^2 + 2|s|^2 \ge 2|b|^2$, the denominator chosen in line L7 has $|E| \ge |b| \ge \mu/2$, so line L8 does not fail, and $|h| = 2|f_k|/|E| \le 4|f_k|/\mu$. As $|f_k| = |f[x^*, x_k]|\,|e_k| \le \frac54\mu|e_k|$, we get $|h| \le 5|e_k|$ and $|e_{k+1}| \le 6\varepsilon$.

*The new error is small.* All four points lie in $B_{6\rho}$. By Claim 2, with $|f[x^*, x_{k+1}]| \ge \frac34\mu$, $|f[x_{k-2}, x_{k-1}, x_k, x_{k+1}]| \le M_3$ and $|x_{k+1} - x_j| \le |e_{k+1}| + |e_j| \le 7\varepsilon$,
$$|e_{k+1}| \le \frac{4M_3}{3\mu}\,343\,\varepsilon^3 \le \tfrac12\varepsilon .$$
So the new point is again in $B_\rho$, with error at most half the largest of the three previous errors. By induction all iterates stay in $B_\rho$ and the largest error over three consecutive points halves at least every three passes, so $e_k \to 0$. Once $|e_{k+1}| \le |e_j|$ for the three previous $j$, the factors satisfy $|x_{k+1} - x_j| \le 2|e_j|$, which gives $|e_{k+1}| \le K|e_k||e_{k-1}||e_{k-2}|$ with $K = 32M_3/(3\mu)$.

If two of the three points coincide, line L3 stops; if $f_{k+1} = 0$ the program returns an exact root.

## Claim 4: the order

Let $\epsilon_k = \log(1/|e_k|)$. Claim 2 gives $\epsilon_{k+1} = \epsilon_k + \epsilon_{k-1} + \epsilon_{k-2} + c + o(1)$ with $c = \log|6f'(x^*)/f'''(x^*)|$ when $f'''(x^*) \ne 0$. The solutions of this linear recurrence grow like $q^k$ where $q$ is the dominant root of $q^3 = q^2 + q + 1$, $q = 1.8392867552\ldots$, and then $\epsilon_{k+1}/\epsilon_k \to q$, which is order $q$.

## What is not proved

Global behaviour, the behaviour at multiple roots and the iteration counts of the examples are observations.
