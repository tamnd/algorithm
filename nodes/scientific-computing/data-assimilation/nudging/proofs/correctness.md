---
title: Nudging integrates the relaxed model, and a large enough gain makes the error decay
proves: [correctness, termination]
status: full
---

**Setting.** The model is $\dot x = f(x)$ on $\mathbb R^n$ with a locally Lipschitz $f$. The observations are $y^o(t) \in \mathbb R^p$, $H$ is a $p \times n$ matrix and $G$ an $n \times p$ matrix. The nudged equation is

$$\dot x = q(t, x) = f(x) + G\big(y^o(t) - Hx\big). \qquad (1)$$

**Termination and what the code computes.** Line L1 sets $x_0$. Line L3 defines the right side $q$ of (1). The loop of line L2 runs $m$ times, and each pass does one classical Runge-Kutta step of (1) in line L4, with four evaluations of $q$. So the algorithm stops after $4m$ evaluations of $f$ and returns at line L5. The output is the Runge-Kutta solution of (1). For a $y^o$ with four continuous derivatives its global error on a fixed interval is $O(dt^4)$, the order of the method. With $y^o$ linear in time between observation times, $q$ is only continuous in $t$ at those times, and the error of the forcing term is $O(dt^2)$; the tests use a tolerance that allows for this. The statements below are about the exact solution of (1).

**Theorem 1 (linear scalar case).** For $\dot x = -a x + g(y - x)$ with constants $a$, $g$, $y$ and $a + g \ne 0$, the solution is

$$x(t) = x_e + (x(0) - x_e)\,e^{-(a + g)t}, \qquad x_e = \frac{g y}{a + g}.$$

*Proof.* The equation is $\dot x = -(a + g)(x - x_e)$, a linear equation for $x - x_e$ with the solution $(x(0) - x_e)e^{-(a + g)t}$. $\square$

For $a + g > 0$ the solution relaxes to $x_e$ with the time scale $1/(a + g)$. The limit $x_e$ is between the free equilibrium $0$ and the observation $y$: nudging does not reach the observation unless the model agrees with it.

**Theorem 2 (error decay with full observations).** Let the truth $x^t$ solve $\dot x^t = f(x^t)$ and be observed exactly and completely, $y^o(t) = x^t(t)$, with $H = I$ and $G = gI$. Suppose that along the truth

$$e^\top\big(f(x^t(t) + e) - f(x^t(t))\big) \le \ell\,|e|^2 \quad \text{for all } e \in \mathbb R^n \text{ and } t \ge 0. \qquad (2)$$

Then the error $e(t) = x(t) - x^t(t)$ of the solution of (1) satisfies $|e(t)| \le e^{(\ell - g)t}|e(0)|$. So for $g > \ell$ the nudged solution converges to the truth exponentially, whatever its initial value.

*Proof.* Subtract the two equations: $\dot e = f(x^t + e) - f(x^t) - g e$. Then

$$\tfrac12 \tfrac{d}{dt}|e|^2 = e^\top \dot e = e^\top\big(f(x^t + e) - f(x^t)\big) - g|e|^2 \le (\ell - g)|e|^2.$$

So $\tfrac{d}{dt}\big(e^{-2(\ell - g)t}|e|^2\big) \le 0$, which gives $|e(t)|^2 \le e^{2(\ell - g)t}|e(0)|^2$. $\square$

If $f(x) = Ax$ with a skew-symmetric $A$, then $e^\top A e = 0$, so (2) holds with $\ell = 0$ and the proof gives the equality $|e(t)| = e^{-gt}|e(0)|$. The tests check this for a rotation.

**Lemma 3 (energy conservation of the Lorenz-96 advection).** For $N(x)_j = (x_{j+1} - x_{j-2})x_{j-1}$ with indices modulo $n$, $x^\top N(x) = 0$ for every $x$.

*Proof.* $x^\top N(x) = \sum_j x_{j+1}x_j x_{j-1} - \sum_j x_j x_{j-1} x_{j-2}$. Replace $j$ by $j + 1$ in the second sum: it becomes $\sum_j x_{j+1} x_j x_{j-1}$, the first sum. $\square$

**Lemma 4 (one-sided bound for Lorenz-96).** For the Lorenz-96 tendency $f(x) = N(x) - x + F$ and any $x^t$, $e$,

$$e^\top\big(f(x^t + e) - f(x^t)\big) \le (4M - 1)|e|^2, \qquad M = \max_j |x^t_j|.$$

*Proof.* Expand: $N(x^t + e)_j - N(x^t)_j = (e_{j+1} - e_{j-2})x^t_{j-1} + (x^t_{j+1} - x^t_{j-2})e_{j-1} + N(e)_j$. By Lemma 3, $e^\top N(e) = 0$. The other terms give

$$\sum_j e_j e_{j+1} x^t_{j-1} - \sum_j e_j e_{j-2} x^t_{j-1} + \sum_j e_j e_{j-1}(x^t_{j+1} - x^t_{j-2}),$$

whose absolute value is at most $M\sum_j|e_j||e_{j+1}| + M\sum_j|e_j||e_{j-2}| + 2M\sum_j|e_j||e_{j-1}|$. Each sum $\sum_j |e_j||e_{j+s}|$ is at most $|e|^2$ by the Cauchy-Schwarz inequality, because the shift does not change the norm. So these terms are at most $4M|e|^2$. The linear term gives $e^\top(-e) = -|e|^2$, and the constant $F$ cancels. $\square$

**Corollary 5 (synchronization of Lorenz-96).** With full exact observations, $H = I$ and $G = gI$, let $M$ bound $|x^t_j(t)|$ for all $j$ and $t \ge 0$. If $g > 4M - 1$, the nudged Lorenz-96 solution converges to the truth exponentially, at the rate $g + 1 - 4M$.

*Proof.* Lemma 4 gives (2) with $\ell = 4M - 1$, and Theorem 2 applies. $\square$

The truth enters the bound only through $M$, so the bound holds for any initial value of the nudged run. The condition is sufficient, not necessary: the measured threshold on the page is much smaller than $4M - 1$.

**Summary.** The algorithm stops after $m$ Runge-Kutta steps of the nudged equation (1). For a linear scalar model the nudged solution relaxes to a weighted mean of the model equilibrium and the observation. With full exact observations, $G = gI$ and a model that satisfies the one-sided bound (2), the error decays like $e^{(\ell - g)t}$, and for Lorenz-96 the bound holds with $\ell = 4\max_j|x^t_j| - 1$. $\blacksquare$
