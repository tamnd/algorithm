---
title: Filon-Simpson integrates the piecewise quadratic interpolant times e^(i omega x) exactly, and its error is at most min of an h^3 bound and an h / omega^2 bound
proves: [correctness, error, termination]
status: full
---

Let $f \in C[a, b]$ be real, $\omega$ real, $m \ge 2$ even, $h = (b - a)/m$ (negative when $b < a$), $x_k = a + kh$, $f_k = f(x_k)$ and $\theta = \omega h$. We prove one complex identity; its real and imaginary parts are the two outputs, $C \approx \int_a^b f\cos\omega x\,dx$ and $S \approx \int_a^b f\sin\omega x\,dx$.

## Claim 1: the rule integrates the interpolant exactly

Let $p$ be the continuous function that on each panel pair $[x_{2j}, x_{2j+2}]$ is the quadratic interpolating $f$ at $x_{2j}, x_{2j+1}, x_{2j+2}$. We show that the code returns exactly $\int_a^b p(x)e^{i\omega x}\,dx = C + iS$ in exact arithmetic, with

$$C + iS = h\Bigl[-i\alpha\bigl(f_m e^{i\omega b} - f_0 e^{i\omega a}\bigr) + \beta\Bigl(\sum_{k \text{ even}} f_k e^{i\omega x_k} - \tfrac12 f_0e^{i\omega a} - \tfrac12 f_me^{i\omega b}\Bigr) + \gamma\sum_{k \text{ odd}} f_k e^{i\omega x_k}\Bigr], \tag{1}$$

$$\alpha = \frac{\theta^2 + \theta\sin\theta\cos\theta - 2\sin^2\theta}{\theta^3},\quad \beta = \frac{2\bigl(\theta(1 + \cos^2\theta) - 2\sin\theta\cos\theta\bigr)}{\theta^3},\quad \gamma = \frac{4(\sin\theta - \theta\cos\theta)}{\theta^3}.$$

The real part of (1) is line L5's $C$ and the imaginary part is its $S$, because $\operatorname{Re}(-i\alpha z) = \alpha\operatorname{Im}z$ and $\operatorname{Im}(-i\alpha z) = -\alpha\operatorname{Re}z$ for real $\alpha$.

*One panel pair.* Take the pair with midpoint $c = x_{2j+1}$ and write $x = c + hu$, $u \in [-1, 1]$. With values $g_{-1}, g_0, g_1$ the interpolant is $g_{-1}\frac{u^2 - u}{2} + g_0(1 - u^2) + g_1\frac{u^2 + u}{2}$, and
$$\int_{x_{2j}}^{x_{2j+2}} p\,e^{i\omega x}\,dx = h e^{i\omega c}\bigl(W_{-1}g_{-1} + W_0g_0 + W_1g_1\bigr),\quad W_0 = \mu_0 - \mu_2,\ W_{\pm1} = \tfrac12(\mu_2 \pm \mu_1),$$
where $\mu_k = \int_{-1}^1 u^ke^{i\theta u}\,du$. (The substitution is valid for $h < 0$ too: $dx = h\,du$ and the orientation is carried by the sign of $h$.) Integrating by parts, for $\theta \ne 0$,
$$\mu_0 = \frac{2\sin\theta}{\theta},\quad \mu_1 = 2i\,\frac{\sin\theta - \theta\cos\theta}{\theta^2},\quad \mu_2 = \frac{2\bigl((\theta^2 - 2)\sin\theta + 2\theta\cos\theta\bigr)}{\theta^3}.$$
Then $W_0 = \frac{2\theta^2\sin\theta - 2(\theta^2 - 2)\sin\theta - 4\theta\cos\theta}{\theta^3} = \gamma$. Next, with $s = \sin\theta$, $c_\theta = \cos\theta$, multiply $W_1 = \frac{(\theta^2 - 2)s + 2\theta c_\theta}{\theta^3} + i\,\frac{s - \theta c_\theta}{\theta^2}$ by $e^{-i\theta} = c_\theta - is$:
$$\operatorname{Re}(W_1e^{-i\theta}) = \frac{(\theta^2 - 2)sc_\theta + 2\theta c_\theta^2 + \theta s^2 - \theta^2 sc_\theta}{\theta^3} = \frac{\theta(1 + c_\theta^2) - 2sc_\theta}{\theta^3} = \frac\beta2,$$
$$\operatorname{Im}(W_1e^{-i\theta}) = \frac{\theta sc_\theta - \theta^2c_\theta^2 - \theta^2s^2 + 2s^2 - 2\theta sc_\theta}{\theta^3} = -\alpha.$$
So $he^{i\omega c}W_1 = h(\frac\beta2 - i\alpha)e^{i\omega(c + h)}$. Since $\mu_1$ is purely imaginary and $\mu_0, \mu_2$ are real, $W_{-1} = \overline{W_1}$, and the same computation gives $he^{i\omega c}W_{-1} = h(\frac\beta2 + i\alpha)e^{i\omega(c - h)}$.

*Summing the pairs.* Each odd node is a midpoint and receives $h\gamma f_ke^{i\omega x_k}$. Each interior even node is the right end of one pair and the left end of the next, and receives $h(\frac\beta2 - i\alpha + \frac\beta2 + i\alpha)f_ke^{i\omega x_k} = h\beta f_ke^{i\omega x_k}$: the $\alpha$ terms cancel. The node $a$ receives $h(\frac\beta2 + i\alpha)f_0e^{i\omega a}$ and the node $b$ receives $h(\frac\beta2 - i\alpha)f_me^{i\omega b}$. Collecting terms gives (1).

*The coefficients at small $\theta$.* $\alpha, \beta, \gamma$ extend to entire functions of $\theta$ (the numerators are entire and vanish to third order at $0$), and line L3 evaluates them by their Taylor series for $\lvert\theta\rvert \le 1$. The code computes the series coefficients exactly in rational arithmetic by expanding the numerators, using $\sin\theta\cos\theta = \frac12\sin 2\theta$ and $\cos^2\theta = \frac12(1 + \cos 2\theta)$, and dividing by $\theta^3$; it asserts that the coefficients of $\theta^0, \theta^1, \theta^2$ vanish. The series kept are $\alpha = \frac{2\theta^3}{45} - \frac{2\theta^5}{315} + \cdots$, $\beta = \frac23 + \frac{2\theta^2}{15} - \cdots$, $\gamma = \frac43 - \frac{2\theta^2}{15} + \cdots$ through $\theta^{31}$. At $\theta = 0$ they give $\alpha = 0$, $\beta = \frac23$, $\gamma = \frac43$, so (1) becomes the composite Simpson rule; this is also the limit of the panel formula as $\theta \to 0$.

**Consequence.** If $f$ is a polynomial of degree at most 2 then $p = f$, and the rule returns $\int_a^b f e^{i\omega x}$ exactly, for every $\omega$. For $\omega \ne 0$ it is not exact for $x^3$: on $[-1, 1]$ with $m = 2$ the rule cannot tell $u^3$ from $u$ at the nodes, and $\int u^3e^{i\theta u} - \int ue^{i\theta u} = i\theta(\frac25 - \frac23) + O(\theta^3) \ne 0$. The test file checks both statements as identities between power series with rational coefficients.

## Claim 2: the error bounds

Let $f \in C^3$ between $a$ and $b$, $M_3 = \max\lvert f'''\rvert$, and $e = f - p$. The error of (1) is $E = \int_a^b e(x)e^{i\omega x}\,dx$, and $\lvert E_C\rvert, \lvert E_S\rvert \le \lvert E\rvert$ for the real and imaginary parts.

**Bound uniform in $\omega$.** On a pair with nodes $x_0, x_1, x_2$, $e(x) = \frac{f'''(\xi_x)}{6}(x - x_0)(x - x_1)(x - x_2)$, and the cubic has maximum modulus $\frac{2\lvert h\rvert^3}{3\sqrt3}$ on the pair. So $\lvert e\rvert \le \frac{M_3\lvert h\rvert^3}{9\sqrt3}$ and, since $\lvert e^{i\omega x}\rvert = 1$,
$$\lvert E\rvert \le \frac{\lvert b - a\rvert\,M_3\,\lvert h\rvert^3}{9\sqrt3}.$$

**Bound that improves with $\omega$.** Let $\omega \ne 0$. On one pair, $e(x_0) = e(x_2) = 0$, so integrating by parts twice,
$$\int_{x_0}^{x_2} e\,e^{i\omega x}\,dx = -\frac{1}{i\omega}\int_{x_0}^{x_2} e'e^{i\omega x}\,dx = -\frac{1}{i\omega}\Bigl(\Bigl[\frac{e'e^{i\omega x}}{i\omega}\Bigr]_{x_0}^{x_2} - \frac{1}{i\omega}\int_{x_0}^{x_2}e''e^{i\omega x}\,dx\Bigr),$$
so the pair contributes at most $\omega^{-2}\bigl(\lvert e'(x_0)\rvert + \lvert e'(x_2)\rvert + \int\lvert e''\rvert\bigr)$. Write $e(x) = f[x_0, x_1, x_2, x]\,\pi(x)$ with $\pi(x) = (x - x_0)(x - x_1)(x - x_2)$; since $\pi(x_0) = 0$, $e'(x_0) = f[x_0, x_1, x_2, x_0]\,\pi'(x_0) = \frac{f'''(\xi)}{6}\cdot 2h^2$, so $\lvert e'(x_0)\rvert \le \frac{M_3h^2}{3}$, and likewise at $x_2$. Next, $p''$ is the constant $2f[x_0, x_1, x_2] = f''(\eta)$ for some $\eta$ in the pair, so $\lvert e''(x)\rvert = \lvert f''(x) - f''(\eta)\rvert \le 2\lvert h\rvert M_3$ and $\int\lvert e''\rvert \le 4h^2M_3$. Each pair contributes at most $\frac{14}{3}\frac{M_3h^2}{\omega^2}$, and there are $m/2 = \frac{\lvert b - a\rvert}{2\lvert h\rvert}$ pairs:
$$\lvert E\rvert \le \frac{7}{3}\,\frac{\lvert b - a\rvert\,M_3\,\lvert h\rvert}{\omega^2}.$$

Both bounds are proved. Together, $\lvert E\rvert \le M_3\lvert b - a\rvert\min\bigl(\frac{\lvert h\rvert^3}{9\sqrt3}, \frac{7\lvert h\rvert}{3\omega^2}\bigr)$, which the test file checks on 500 random exponentials $e^{cx}$. The faster rate $O(h^4)$ at fixed $\omega$ as $h \to 0$, which the measurements show (ratios of 16 per halving of $h$), is an asymptotic statement that needs $f \in C^4$ and a finer cancellation argument between neighbouring pairs, as for Simpson's rule; it is cited (Davis and Rabinowitz, Section 2.10), not proved here.

## Claim 3: floating point, and the driver

The closed forms for $\alpha$ subtract quantities of size $\theta^2$ to obtain a result of size $\theta^5$ in the numerator, so their relative error grows like $u\,\theta^{-3}$ for unit roundoff $u$; at $\theta = 10^{-4}$ every digit is lost. The series has no cancellation for $\lvert\theta\rvert \le 1$ (its terms decrease in magnitude after the first), and the first omitted terms are below $10^{-28}$ there. For $\lvert\theta\rvert > 1$ the closed forms lose at most a few units in the last place. The sums in L4 and L5 use `math.fsum`.

The driver evaluates $f$ at the $3$ nodes for $m = 2$ and then, for $m \to 2m$, only at the $m$ new odd nodes, since $x_k^{(m)} = x_{2k}^{(2m)}$. After the rule with $m$ panels it has used exactly $m + 1$ evaluations. The loop doubles $m$ while $2m \le$ `max_m`, so it stops after at most $\log_2(\texttt{max\_m}/2)$ iterations, returning "ok" when two successive results differ by at most $\tau$ and "limit" otherwise. That the difference bounds the error is a heuristic, and the test file shows a case where it does not. $\blacksquare$
