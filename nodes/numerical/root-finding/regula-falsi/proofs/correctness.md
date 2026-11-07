---
title: Regula falsi keeps its bracket, converges for every continuous f, and is linear with one end fixed
proves: [correctness, termination, invariant, convergence, rate]
status: full
---

We write $[a_k, b_k]$ for the bracket at the start of pass $k + 1$ of the loop of lines L5 to L11, so $[a_0, b_0]$ is the input, and $c_{k+1}$ for the cut point computed in that pass. When one end is fixed we write $x_k = a_k$ and $e_k = x_k - x^*$. Divided differences are written $f[u, v]$ and $f[u, v, w]$.

**Claim 1 (termination and the invariant).** REGULA-FALSI returns after at most $k_{\max}$ passes and $k_{\max} + 2$ evaluations of $f$. If line L3 passes, then at the start of every pass $a_k < b_k$, $[a_k, b_k] \subseteq [a_0, b_0]$, and $f(a_k)$, $f(b_k)$ are finite, nonzero and of opposite signs. This holds in floating point for the computed values of $f$.

*Proof.* Line L1 makes two evaluations and each pass one (line L7); the loop runs at most $k_{\max}$ times. The invariant holds for $k = 0$ by lines L2 and L3. Assume it for $k$. Line L6 gives a point $c$ with $a_k < c < b_k$: either the computed chord zero passes the test, or $c$ is the computed midpoint. (In floating point, when $a_k$ and $b_k$ are adjacent numbers, the computed midpoint equals an end; then line L8 replaces that end by itself, the invariant still holds, and the next pass computes the same $c$, so line L10 returns.) Line L7 returns unless $f(c)$ is finite and nonzero. Line L8 replaces the end whose value has the sign of $f(c)$, so the new ends still have values of opposite signs, and the new bracket lies inside the old one. $\square$

In exact arithmetic the chord zero always lies strictly inside: with $f(a_k) < 0 < f(b_k)$ (the other case is symmetric),
$$c = \frac{a_k f(b_k) - b_k f(a_k)}{f(b_k) - f(a_k)} = a_k + \frac{-f(a_k)}{f(b_k) - f(a_k)}\,(b_k - a_k),$$
and the fraction lies in $(0, 1)$. So the guard of line L6 is never used, and $c_{k+1}$ is the chord zero.

**Claim 2 (convergence for continuous f).** Let $f$ be continuous on $[a_0, b_0]$ with $f(a_0) < 0 < f(b_0)$, and run the method in exact arithmetic with $\delta = 0$ and $k_{\max} = \infty$. If it does not return at line L7, then $a_k \uparrow \alpha$, $b_k \downarrow \beta$ with $\alpha \le \beta$, $f(\alpha) \le 0 \le f(\beta)$, every end that moves infinitely often tends to a zero of $f$, and every limit point of $(c_k)$ is a zero of $f$.

*Proof.* By Claim 1, $(a_k)$ is non-decreasing and $(b_k)$ non-increasing, with $a_k < b_k$, so the limits exist and $\alpha \le \beta$. Since $f(a_k) < 0 < f(b_k)$ and $f$ is continuous, $f(\alpha) \le 0 \le f(\beta)$.

Suppose $a$ moves in infinitely many passes, say in passes $k \in K$, so that $a_{k+1} = c_{k+1}$ for $k \in K$. For those $k$,
$$c_{k+1}\,\big(f(b_k) - f(a_k)\big) = a_k f(b_k) - b_k f(a_k).$$
Let $k \to \infty$ in $K$: $c_{k+1} \to \alpha$, $a_k \to \alpha$, $b_k \to \beta$, and by continuity
$$\alpha\,\big(f(\beta) - f(\alpha)\big) = \alpha f(\beta) - \beta f(\alpha), \quad\text{that is}\quad f(\alpha)\,(\beta - \alpha) = 0.$$
If $\alpha < \beta$ this gives $f(\alpha) = 0$. If $\alpha = \beta$, then $f(\alpha) \le 0 \le f(\beta) = f(\alpha)$ gives $f(\alpha) = 0$ as well. The case of $b$ is the same with the roles exchanged, giving $f(\beta)(\beta - \alpha) = 0$.

Each pass moves exactly one end, so at least one end moves infinitely often. Each $c_{k+1}$ equals $a_{k+1}$ or $b_{k+1}$. A limit point of $(c_k)$ is the limit of a subsequence that lies, after passing to a further subsequence, entirely in the moves of $a$ or entirely in the moves of $b$; it is then $\alpha$ with $a$ moving infinitely often, or $\beta$ with $b$ moving infinitely often, and in both cases a zero. $\square$

The width $b_k - a_k$ tends to $\beta - \alpha$, which may be positive; Claim 3 shows that this is the usual case.

**Claim 3 (one end fixed).** Let $f \in C^2$ on $[a_0, b_0]$ with $f'' > 0$ there and $f(a_0) < 0 < f(b_0)$. Then $f$ has exactly one zero $x^*$ in $(a_0, b_0)$, and in exact arithmetic $f(c_k) < 0$ for every $k$, so $b_k = b_0$ and $a_k = c_k$ for all $k \ge 1$, and $a_k \uparrow x^*$.

*Proof.* A zero exists by the intermediate value theorem. If $z_1 < z_2$ were two zeros in $(a_0, b_0)$, then $z_1 = \lambda a_0 + (1 - \lambda) z_2$ with $\lambda \in (0, 1)$, and strict convexity gives $f(z_1) < \lambda f(a_0) + (1 - \lambda) f(z_2) < 0$, a contradiction. So the zero is unique. Now let $\ell$ be the affine function through $(a_k, f(a_k))$ and $(b_0, f(b_0))$. By strict convexity $f < \ell$ on $(a_k, b_0)$, and $c_{k+1}$ is the zero of $\ell$ in that interval, so $f(c_{k+1}) < \ell(c_{k+1}) = 0$. Line L8 then replaces $a$, and $b$ never moves. By Claim 2, $a$ moves infinitely often and tends to a zero in $[a_0, b_0]$; $f(a_0) < 0 < f(b_0)$ rules out the ends, so the limit is $x^*$. $\square$

**Lemma (the error identity with a fixed end).** In the setting of Claim 3, with $b = b_0$,
$$e_{k+1} = \frac{(b - x^*)\, f[x_k, b, x^*]}{f[x_k, b]}\; e_k .$$

*Proof.* Line L6 is the secant step from the points $x_k$ and $b$, so the secant error identity (the lemma in the proof for the [secant method](/secant-method/)) holds with $e_{k-1}$ replaced by $b - x^*$. Its proof uses only $f(x^*) = 0$ and the definition of divided differences. Here $f[x_k, b] > 0$ because $f(x_k) < 0 < f(b)$. $\square$

**Claim 4 (linear rate).** In the setting of Claim 3, if no $e_k$ is zero, then
$$\lim_{k \to \infty} \frac{e_{k+1}}{e_k} = C = 1 - \frac{f'(x^*)\,(b - x^*)}{f(b)}, \qquad 0 < C < 1.$$

*Proof.* As $x_k \to x^*$, the divided differences are continuous in their arguments for $f \in C^2$, so $f[x_k, b] \to f[x^*, b] = f(b)/(b - x^*)$ and $f[x_k, b, x^*] \to f[x^*, x^*, b] = (f[x^*, b] - f'(x^*))/(b - x^*)$. Putting these into the lemma,
$$\frac{e_{k+1}}{e_k} \to \frac{(b - x^*)\,\big(f[x^*, b] - f'(x^*)\big)/(b - x^*)}{f(b)/(b - x^*)} = \frac{f(b) - f'(x^*)(b - x^*)}{f(b)} = C.$$
For the bounds, convexity gives $f'(x^*) \ge (f(x^*) - f(a_0))/(x^* - a_0) > 0$, so $C < 1$, and strict convexity gives $f(b) > f(x^*) + f'(x^*)(b - x^*) = f'(x^*)(b - x^*)$, so $C > 0$. $\square$

So the convergence is linear with a nonzero rate, and the order is exactly $1$.

**Floating point.** Claim 1 holds as stated. Claims 2 to 4 hold in exact arithmetic. In floating point the iterates follow them until $|f(c)|$ reaches its rounding error, after which the computed signs, and so the moves of line L8, are no longer governed by the true $f$. $\blacksquare$
