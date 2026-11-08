---
title: Taylor-mode recurrences give the exact Taylor coefficients, and the Taylor method of order p converges with error O(h^p)
proves: [correctness, termination, convergence]
status: full
---

**Setting.** $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$ is built from $t$, $y$ and constants by finitely many operations $+$, $-$, $\times$, $/$ (with nonzero divisors), integer powers, $\exp$, $\sin$ and $\cos$. Then $f$ is real analytic where it is defined, the solution $y$ of $y' = f(t, y)$, $y(t_0) = y_0$ is analytic, and $f$ is locally Lipschitz in $y$. We assume the solution stays in a compact set $K$ on $[t_0, T]$ where $f$ is defined. Norms are any fixed norm on $\mathbb{R}^d$. Write $y_{[k]}(t) = y^{(k)}(t)/k!$ for the normalized Taylor coefficients, so $y(t + s) = \sum_k y_{[k]}(t) s^k$ near $s = 0$.

**Termination.** Line L1 gives a finite $N \ge 0$. Each step runs the loop of line L3 exactly $p$ times, and each pass evaluates $f$ once on finite series. So the method stops after $Np$ series evaluations.

**Lemma 1 (causality of the series operations).** For each operation $\circ$ above, coefficient $k$ of the result depends only on coefficients $0, \ldots, k$ of the arguments, and equals coefficient $k$ of the exact power series of the result.

*Proof.* For sums this is clear. For products, $(uv)_{[k]} = \sum_{i=0}^{k} u_{[i]} v_{[k-i]}$ (Cauchy product). For quotients $w = u/v$, $wv = u$ gives $w_{[k]} = (u_{[k]} - \sum_{i<k} w_{[i]} v_{[k-i]}) / v_{[0]}$, which uses $w_{[0]}, \ldots, w_{[k-1]}$ only. For $e = \exp(x)$, $e' = x' e$ gives $k e_{[k]} = \sum_{j=1}^{k} j x_{[j]} e_{[k-j]}$. For $s = \sin x$, $c = \cos x$, $s' = x'c$ and $c' = -x's$ give $k s_{[k]} = \sum_{j=1}^k j x_{[j]} c_{[k-j]}$ and $k c_{[k]} = -\sum_{j=1}^k j x_{[j]} s_{[k-j]}$. Each formula involves only coefficients of index at most $k$, and each is an identity between the coefficients of the exact series. $\square$

By induction over the expression that defines $f$, the same holds for $f$: if two pairs of series $(t + s, u)$ and $(t + s, v)$ agree in coefficients $0, \ldots, k$, so do $f(t + s, u)$ and $f(t + s, v)$, and these coefficients equal those of the exact series of $f(t + s, y(t + s))$ when $u$ is the truncation of $y(t + s)$.

**Lemma 2 (the coefficients are exact).** After pass $k$ of the loop (lines L3 to L5), the stored values are $y_{[0]}, \ldots, y_{[k+1]}$ of the solution through $(t, y)$.

*Proof.* By induction on $k$. Line L2 stores $y_{[0]} = y$. Suppose $y_{[0]}, \ldots, y_{[k]}$ are correct. Differentiating $y(t + s) = \sum_j y_{[j]} s^j$ gives $y'(t + s) = \sum_j (j + 1) y_{[j+1]} s^j$, and $y'(t + s) = f(t + s, y(t + s))$. Line L4 evaluates $f$ on the truncated series, whose coefficient $k$ is, by Lemma 1, coefficient $k$ of $f(t + s, y(t + s))$. Comparing coefficients of $s^k$, $(k + 1) y_{[k+1]} = f(t + s, y(t + s))_{[k]}$, which is what line L5 stores. $\square$

**Lemma 3 (local error).** The step $y_{n+1} = \sum_{k=0}^{p} y_{[k]}(t_n) h^k$ (line L6) has local error $y(t_n + h) - y_{n+1} = y_{[p+1]}(\xi) h^{p+1}$ in each component for some $\xi$ in $(t_n, t_n + h)$, so it is $O(h^{p+1})$ uniformly on $K$.

*Proof.* Taylor's theorem with the Lagrange remainder for each component, using Lemma 2. $\square$

**Theorem (convergence, proved).** Under the assumptions above there are $h_0$ and $C$ such that for $h \le h_0$ the global error satisfies $\max_{n \le N} \|y(t_n) - y_n\| \le C h^p$.

*Proof.* The method is a one-step method $y_{n+1} = y_n + h\Phi(t_n, y_n, h)$ with $\Phi(t, u, h) = \sum_{k=1}^{p} y_{[k]}(t, u) h^{k-1}$, where $y_{[k]}(t, u)$ is the $k$-th coefficient of the solution through $(t, u)$. Each $y_{[k]}(t, u)$ is a composition of the operations of $f$ with the recurrences of Lemma 1, so it is $C^1$ in $u$ and Lipschitz on a compact neighbourhood $K'$ of $K$, with some constant $L_k$. Hence $\Phi$ is Lipschitz in $u$ with constant $\Lambda = \sum_k L_k h_0^{k-1}$. With the local error of Lemma 3, the standard argument for one-step methods (as for the [Euler method](/euler-method/) and [Runge-Kutta methods](/runge-kutta-methods/)) gives $\|e_{n+1}\| \le (1 + h\Lambda)\|e_n\| + c h^{p+1}$, so $\|e_n\| \le c h^p (T - t_0) e^{\Lambda(T - t_0)}$, as long as the numerical solution stays in $K'$, which holds for $h$ small by the same bound. $\square$

**Stability function.** For $y' = \lambda y$, Lemma 2 gives $y_{[k]} = \lambda^k y / k!$, so $y_{n+1} = R(z) y_n$ with $R(z) = \sum_{k=0}^{p} z^k / k!$, $z = h\lambda$. This is the stability function of every explicit $p$-stage Runge-Kutta method of order $p \le 4$. It is a polynomial, so the stability region is bounded and the method is not suited to stiff problems.
