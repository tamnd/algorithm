---
title: Newton's method ends, converges quadratically near a simple root, and converges monotonically on a convex side
proves: [correctness, termination, local-convergence, monotone-convergence]
status: full
---

We write $x_k$ for the value of $x$ at the start of pass $k + 1$ of the loop of lines L2 to L11, so $x_0$ is the input, $e_k = x_k - x^*$ and $s_k = x_{k+1} - x_k = -f(x_k)/f'(x_k)$.

**Claim 1 (termination and the meaning of the flags).** NEWTON returns after at most $k_{\max}$ passes. A result with the flag "root" is a point $x$ with $f(x) = 0$. A result with the flag "converged" is a point $x_{k+1}$ with $|x_{k+1} - x_k| \le \delta_a + \delta_r |x_{k+1}|$.

*Proof.* The loop of line L2 runs at most $k_{\max}$ times, each pass does a fixed number of operations besides one call of $f$ and at most one of $f'$, and line L12 returns after the loop. Line L4 returns $x$ only when $f(x) = 0$. Line L10 returns $x_{\text{new}} = x + s$ only when $|s| \le \delta_a + \delta_r |x_{\text{new}}|$. Line L7 is reached only when $d \ne 0$ and $f(x)$, $d$ are finite (line L6), so the division is defined. $\square$

**Lemma (the error identity).** Let $f \in C^2$ on an interval $I$ that holds $x_k$ and a root $x^*$, with $f'(x_k) \ne 0$. Then there is $\xi_k$ between $x_k$ and $x^*$ with
$$e_{k+1} = \frac{f''(\xi_k)}{2 f'(x_k)}\, e_k^2.$$

*Proof.* Taylor's theorem with the Lagrange remainder at $x_k$, evaluated at $x^*$, gives $0 = f(x^*) = f(x_k) - f'(x_k) e_k + \tfrac12 f''(\xi_k) e_k^2$. Divide by $f'(x_k)$: $e_k - f(x_k)/f'(x_k) = \frac{f''(\xi_k)}{2 f'(x_k)} e_k^2$. The left side is $x_{k+1} - x^* = e_{k+1}$. $\square$

**Claim 2 (local quadratic convergence).** Let $f \in C^2$ on $I = [x^* - r, x^* + r]$ with $r > 0$, $f(x^*) = 0$ and $f'(x) \ne 0$ for $x \in I$. Let $M = \max_I |f''| / (2 \min_I |f'|)$, and assume that $x_0 \in I$ and $M |e_0| \le 1/2$. In exact arithmetic, with $k_{\max} = \infty$ and $\delta_a = \delta_r = 0$:

1. each $x_k$ lies in $I$, and $|e_{k+1}| \le M |e_k|^2 \le \tfrac12 |e_k|$;
2. $M |e_k| \le (M |e_0|)^{2^k}$, so $x_k \to x^*$;
3. if no $e_k$ is zero, $e_{k+1}/e_k^2 \to f''(x^*)/(2 f'(x^*))$;
4. for every $k$, $|e_k| \le 2 |s_k|$ and $|e_{k+1}| \le 4 M s_k^2$. So when line L10 returns $x_{k+1}$ after the step $s_k$ with $|s_k| \le \tau$, its error is at most $4 M \tau^2$.

*Proof.* We prove "$x_k \in I$ and $M |e_k| \le (M |e_0|)^{2^k}$" by induction on $k$.

*Base.* $x_0 \in I$ and the bound is an equality for $k = 0$.

*Step.* Assume the statement for $k$. Then $M |e_k| \le M |e_0| \le 1/2$. If $e_k = 0$, then $f(x_k) = 0$, the pass returns at line L4, and there is nothing more to prove. Otherwise $f'(x_k) \ne 0$ because $x_k \in I$, and the lemma applies on $I$, since $\xi_k$ lies between $x_k$ and $x^*$, both in $I$. It gives $|e_{k+1}| \le M |e_k|^2 = (M |e_k|) |e_k| \le \tfrac12 |e_k| \le r$, so $x_{k+1} \in I$, and $M |e_{k+1}| \le (M |e_k|)^2 \le (M |e_0|)^{2^{k+1}}$.

This proves items 1 and 2: since $M |e_0| \le 1/2$, $M |e_k| \le 2^{-2^k} \to 0$. (If $M = 0$, then $f'' = 0$ on $I$, $f$ is linear on $I$, and $e_1 = 0$.) For item 3, $x_k \to x^*$ forces $\xi_k \to x^*$, and $f''$ and $f'$ are continuous with $f'(x^*) \ne 0$, so the factor in the lemma tends to $f''(x^*)/(2 f'(x^*))$.

For item 4, $s_k = e_{k+1} - e_k$, so $|e_k| \le |s_k| + |e_{k+1}| \le |s_k| + \tfrac12 |e_k|$, which gives $|e_k| \le 2 |s_k|$. Then $|e_{k+1}| \le M |e_k|^2 \le 4 M s_k^2$. $\square$

**Claim 3 (monotone convergence on a convex side).** Let $f \in C^2$ on $[x^*, \infty)$ with $f(x^*) = 0$, $f'(x) > 0$ and $f''(x) \ge 0$ for all $x \ge x^*$, and let $x_0 > x^*$. Then in exact arithmetic $x^* \le x_{k+1} \le x_k$ for all $k$, and $x_k \to x^*$.

*Proof.* Assume that $x_k \ge x^*$. If $x_k = x^*$, line L4 returns. Otherwise $x_k > x^*$, and since $f' > 0$, $f(x_k) > f(x^*) = 0$ and $f'(x_k) > 0$, so $s_k = -f(x_k)/f'(x_k) < 0$ and $x_{k+1} < x_k$. The lemma on $[x^*, x_k]$ gives $e_{k+1} = \frac{f''(\xi_k)}{2 f'(x_k)} e_k^2 \ge 0$, so $x_{k+1} \ge x^*$. By induction the sequence is non-increasing and bounded below by $x^*$, so it has a limit $L \ge x^*$. The map $g(x) = x - f(x)/f'(x)$ is continuous on $[x^*, \infty)$ because $f' > 0$ there, and $x_{k+1} = g(x_k)$, so $L = g(L)$, that is $f(L) = 0$. Since $f$ is strictly increasing on $[x^*, \infty)$, its only zero there is $x^*$, so $L = x^*$. $\square$

The cases $f' > 0, f'' \le 0$ with $x_0 < x^*$, and the two cases with $f' < 0$, follow by applying Claim 3 to $-f(x)$, $f(-x)$ or $-f(-x)$, which have the same Newton iterates up to the sign of $x$.

**Floating point.** Claim 1 holds in floating point as stated, because it uses only the tests of lines L2, L4, L6 and L10. Claims 2 and 3 hold in exact arithmetic. In floating point the iterates follow them until the error reaches the limiting accuracy described on the main page. $\blacksquare$
