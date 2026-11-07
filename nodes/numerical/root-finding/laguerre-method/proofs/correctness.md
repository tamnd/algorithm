---
title: Laguerre's method ends, converges monotonically for real-rooted polynomials, and converges cubically to simple roots
proves: [correctness, termination, global-convergence, local-convergence]
status: full
---

Let $p$ have degree $n \ge 2$ and roots $x_1, \ldots, x_n$ (for $n = 1$ the step is $p/p'$ and lands on the root at once). For $x$ not a root write $\beta_i = 1/(x - x_i)$, so $G = \sum_i \beta_i$ and $H = \sum_i \beta_i^2$. For a step $a$ write $\delta = 1/a$; the two candidate values of $\delta$ in lines L7 and L8 are the roots of
$$Q(\delta) = n\delta^2 - 2G\delta + G^2 - (n - 1)H,$$
since $Q(\delta) = (G - \delta)^2 - (n - 1)(H - \delta^2)$ and its roots are $(G \pm \sqrt{(n-1)(nH - G^2)})/n$.

## Claim 1: termination and the flags

Each pass returns or increases $k$, and $k \le k_{\max}$, so the loop ends after at most $k_{\max}$ passes and sweeps. The flags "root", "residual" and "converged" come only from lines L4, L5 and L11, whose tests they record.

## Claim 2: every root lies between the two Laguerre values (real roots)

Assume all roots are real and $x$ is real and not a root. Fix an index $j$. By the Cauchy-Schwarz inequality on the $n - 1$ numbers $\beta_i$, $i \ne j$,
$$(G - \beta_j)^2 = \Big(\sum_{i \ne j} \beta_i\Big)^2 \le (n - 1)\sum_{i \ne j}\beta_i^2 = (n - 1)(H - \beta_j^2),$$
that is $Q(\beta_j) \le 0$. Also $nH - G^2 \ge 0$ by Cauchy-Schwarz on all $n$ numbers, so $Q$ has two real roots $\delta_- \le \delta_+$, and $Q(\beta_j) \le 0$ means $\delta_- \le \beta_j \le \delta_+$ for every $j$.

## Claim 3: the step stops at or before the neighbouring root

Keep the assumptions of Claim 2. Line L8 picks the root of $Q$ of larger modulus, which is $\delta_+$ when $G > 0$ and $\delta_-$ when $G < 0$ (either one when $G = 0$, where $\delta_\pm = \pm\sqrt{(n-1)H/n}$ have equal modulus).

Suppose $G < 0$, so $\delta = \delta_- < 0$ and the new point $y = x - 1/\delta$ lies to the right of $x$. Some $\beta_j$ is negative, since their sum is, so there is a root to the right of $x$; let $x_R$ be the nearest one. Then $\beta_R = -1/(x_R - x)$ is the smallest $\beta_j$, and Claim 2 gives $\delta_- \le \beta_R < 0$, so $0 < y - x = 1/|\delta_-| \le x_R - x$. Thus $y \in (x, x_R]$. The case $G > 0$ is symmetric, with $y \in [x_L, x)$ for the nearest root $x_L$ to the left. When $G = 0$ there are roots on both sides and the same argument applies to whichever sign is taken.

## Claim 4: monotone global convergence for real roots

Keep the assumptions and suppose $G(x_0) < 0$ (the other case is symmetric). Let $x_R$ be the nearest root to the right of $x_0$. On the open interval $I$ between the root just left of $x_0$ (or $-\infty$) and $x_R$, the function $\log|p|$ is smooth with derivative $G$ and second derivative $-H < 0$, so $G$ is strictly decreasing on $I$. By Claim 3, $x_1 \in (x_0, x_R]$. If $x_1 = x_R$ we are done. Otherwise $x_1 \in I$, $x_1 > x_0$ and $G(x_1) < G(x_0) < 0$, so the next step again moves right and stays in $(x_1, x_R]$. By induction the iterates increase and are bounded by $x_R$, so they converge to some $z \le x_R$. If $z < x_R$, then $z \in I$ is not a root, $G$ and $H$ are continuous at $z$, and the step $a(x) = n/d(x)$ is continuous near $z$ with $|a(z)| > 0$, because $|d(z)| \le |G(z)| + \sqrt{(n-1)|nH(z) - G(z)^2|}$ is finite. Then $x_{k+1} - x_k = -a(x_k) \to -a(z) \ne 0$, which contradicts convergence. Hence $z = x_R$. Nothing here needs the roots to be simple.

## Claim 5: local cubic convergence at a simple root

Let $x^*$ be a simple root, $c_i = 1/(x^* - x_i)$ for the other roots, $S_j = \sum_i c_i^j$, and $e = x - x^*$ with $t = 1/e$. For small $e$,
$$\frac{1}{x - x_i} = \frac{c_i}{1 + e c_i} = c_i - e c_i^2 + O(e^2),$$
so $G = t + S_1 - e S_2 + O(e^2)$ and $H = t^2 + S_2 + O(e)$. Then $G^2 = t^2 + 2tS_1 + S_1^2 - 2S_2 + O(e)$ and
$$(n - 1)(nH - G^2) = (n-1)^2 t^2 \Big(1 + y\Big), \quad y = -\frac{2 S_1 e}{n - 1} + \frac{((n+2)S_2 - S_1^2)e^2}{n - 1} + O(e^3).$$
Since $|y|$ is small, $r = \pm(n - 1)t(1 + y/2 - y^2/8 + O(y^3))$, and the root with the plus sign gives $|G + r| \approx n|t|$ against $|G - r| \approx (n - 2)|t|$, so line L8 takes it. Expanding,
$$d = G + r = nt + \frac{n e}{2}\Big(S_2 - \frac{S_1^2}{n - 1}\Big) + O(e^2),$$
so with $K = S_2 - S_1^2/(n-1)$,
$$a = \frac{n}{d} = \frac{e}{1 + K e^2/2 + O(e^3)} = e - \frac{K}{2}e^3 + O(e^4).$$
The new error is $e - a = \frac{K}{2}e^3 + O(e^4) = C e^3 + O(e^4)$ with $C = ((n-1)S_2 - S_1^2)/(2(n-1))$. Hence there is $\rho > 0$ with $|e_{k+1}| \le (|C| + 1)|e_k|^3 \le \frac12|e_k|$ whenever $|e_k| \le \rho$, so starts within $\rho$ of $x^*$ converge with order 3. For real roots, $(n-1)S_2 \ge S_1^2$ by Cauchy-Schwarz, so $C \ge 0$, with equality exactly when all $c_i$ are equal.

## What is not proved

The behaviour at multiple roots, the pass counts of the examples, and convergence from general complex starts are observations, not theorems.
