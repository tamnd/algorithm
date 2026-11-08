---
title: Orders, stability function and error estimate of the Cash-Karp 5(4) pair
proves: [correctness]
status: full
---

**Setting.** $y' = f(t, y)$, $y \in \mathbb{R}^d$ with a norm $\|\cdot\|$. One step uses the six stages $k_i = f(t + c_ih, y + h\sum_{j<i}a_{ij}k_j)$ of the tableau on the page. It gives $y_{n+1} = y + h\sum b_ik_i$, $\hat y_{n+1} = y + h\sum\hat b_ik_i$ and $\mathrm{est} = y_{n+1} - \hat y_{n+1}$. For a rooted tree $t$ with $|t|$ vertices, let $\Phi_i(t)$ be the elementary weight vector: $\Phi(\bullet) = \mathbf 1$, and for $t = [t_1, \dots, t_m]$, $\Phi(t) = \prod_l A\Phi(t_l)$, the product taken componentwise. Let $\gamma(t)$ be the density.

## Lemma 1 (order conditions, verified exactly)

1. $c_i = \sum_ja_{ij}$ for all $i$.
2. $b^T\Phi(t) = 1/\gamma(t)$ for all 17 trees with $|t| \le 5$, and $b^T\Phi(t) \ne 1/\gamma(t)$ for all 20 trees with $|t| = 6$. For example, $\sum b_ic_i^5 = 53/320 \ne 1/6$.
3. $\hat b^T\Phi(t) = 1/\gamma(t)$ for the 8 trees with $|t| \le 4$, and it fails for all 9 trees with $|t| = 5$. For example, $\sum\hat b_ic_i^4 = 82197/409600 \ne 1/5$.

*Proof.* Each statement is a finite identity between rational numbers. The tests generate all rooted trees with up to 6 vertices by adding leaves (the counts 1, 1, 2, 4, 9, 20 are checked), evaluate $\Phi(t)$ with `Fraction` arithmetic and compare. $\square$

By Butcher's order theorem (see [Butcher order conditions](/butcher-order-conditions/)), if $f$ is $C^p$ near the solution, an explicit Runge-Kutta method has local error $O(h^{p+1})$ if and only if $b^T\Phi(t) = 1/\gamma(t)$ for all $|t| \le p$. A failed condition of order $p + 1$ leaves a nonzero $h^{p+1}$ term for suitable $f$. So $y_{n+1}$ has order exactly 5 and $\hat y_{n+1}$ has order exactly 4.

The same exact check shows that $y + h(-\tfrac32k_1 + \tfrac52k_2)$ has order 2 and $y + h(\tfrac{19}{54}k_1 - \tfrac{10}{27}k_3 + \tfrac{55}{54}k_4)$ has order 3, as stated by Cash and Karp.

## Lemma 2 (stability function)

On $y' = \lambda y$ with $z = h\lambda$, the stage vector satisfies $k = \lambda(I - zA)^{-1}\mathbf 1\,y$. Since $A$ is strictly lower triangular, $(I - zA)^{-1} = \sum_{q=0}^5z^qA^q$. So
$$R(z) = 1 + \sum_{q=1}^{6}z^q\,b^TA^{q-1}\mathbf 1.$$
Exact evaluation gives the coefficients $1, 1, \tfrac12, \tfrac16, \tfrac1{24}, \tfrac1{120}, \tfrac1{800}$. The first six follow from the order conditions for the tall trees, $b^TA^{q-1}\mathbf 1 = 1/q!$ for $q \le 5$. The last one is a property of this tableau. $\square$

The real stability interval is $[x^*, 0]$, where $x^* \approx -3.7344$ is the first point left of 0 with $|R(x^*)| = 1$. It was located by bisection and is checked in the tests. That is a numerical result, not a proof.

## Lemma 3 (the estimate)

If $f$ is $C^5$, then $\mathrm{est} = \hat\tau - \tau$, where $\tau = y(t + h) - y_{n+1} = O(h^6)$ and $\hat\tau = y(t + h) - \hat y_{n+1} = O(h^5)$. Hence $\mathrm{est} = \hat\tau + O(h^6)$, so the estimate is asymptotically the local error of the order-4 solution.

*Proof.* Subtract the two definitions, and apply Lemma 1. $\square$

This is only asymptotic. The example on the page shows a step with $h = 0.5$ where the estimate is 45 times smaller than the error.

## Theorem (convergence with fixed steps)

Let $f$ be $L$-Lipschitz in $y$, and suppose the local error of the order-5 solution satisfies $\|\tau\| \le Ch^6$. The increment $\Phi(t, y, h) = \sum b_ik_i$ is Lipschitz in $y$ with a constant $\Lambda = L(1 + O(hL))$. This follows by induction over the stages: $\|k_i - k_i'\| \le L(1 + h\sum_j|a_{ij}|\,\ell_j)\|y - y'\|$, where $\ell_j$ is the constant for stage $j$. Then
$$\|e_n\| \le \frac{Ch^5}{\Lambda}\big(e^{\Lambda(t_n - t_0)} - 1\big),$$
by the same discrete Gronwall argument as for any one-step method. $\square$

## Termination and cost

Each rejection has $\mathrm{err} > 1$, so the step is multiplied by $\min(1, 0.9\,\mathrm{err}^{-1/5}) < 0.9$. If $\|\mathrm{est}\| \le Kh^5$ for small $h$ and $\mathrm{atol} > 0$, a step is accepted after finitely many rejections. When $t + h \ge T$, line L3 sets $h = T - t$, so the last accepted point is $T$. Each attempt evaluates exactly six stages and reuses nothing. The automatic starting step adds one evaluation. So the count is $1 + 6(N + R)$, which the tests check exactly.

## Linear invariants

If $w^Tf(t, y) = 0$ for all $(t, y)$, then $w^Ty_{n+1} = w^Ty_n + h\sum b_iw^Tk_i = w^Ty_n$. Every explicit Runge-Kutta method preserves linear invariants exactly, up to rounding. The tests check this for an SIR model, whose three components have a constant sum.
