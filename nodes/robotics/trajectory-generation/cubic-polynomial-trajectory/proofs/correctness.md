---
title: The cubic meets the four end conditions, is the only cubic that does, and minimizes the integral of squared acceleration
proves: [correctness]
status: full
---

We use the notation of the page. The input is $q_0, v_0, q_1, v_1$ and a duration $T > 0$, and $h = q_1 - q_0$. Lines L1 to L4 set

$$a_0 = q_0, \quad a_1 = v_0, \quad a_2 = \frac{3h - (2v_0 + v_1)T}{T^2}, \quad a_3 = \frac{-2h + (v_0 + v_1)T}{T^3},$$

and the trajectory is $q(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3$ on $[0, T]$. The proof is in exact arithmetic.

## The end conditions hold

**Lemma 1.** $q(0) = q_0$, $q'(0) = v_0$, $q(T) = q_1$ and $q'(T) = v_1$.

*Proof.* $q(0) = a_0 = q_0$ and $q'(0) = a_1 = v_0$ at once. Next,

$$a_2 T^2 + a_3 T^3 = 3h - (2v_0 + v_1)T - 2h + (v_0 + v_1)T = h - v_0 T,$$

so $q(T) = q_0 + v_0 T + h - v_0 T = q_0 + h = q_1$. Also

$$2a_2 T + 3a_3 T^2 = \frac{6h - 2(2v_0 + v_1)T - 6h + 3(v_0 + v_1)T}{T} = v_1 - v_0,$$

so $q'(T) = v_0 + (v_1 - v_0) = v_1$. $\square$

## Uniqueness

**Lemma 2.** No other polynomial of degree at most 3 meets the four conditions.

*Proof.* Let $p$ be the difference of two such polynomials. Then $p$ has degree at most 3 and $p(0) = p'(0) = p(T) = p'(T) = 0$. So $0$ and $T$ are double roots, and $t^2 (t - T)^2$ divides $p$. This product has degree 4, so $p = 0$. $\square$

So the four conditions form a linear system in $(a_0, a_1, a_2, a_3)$ with a nonsingular matrix when $T > 0$, and Lemma 1 gives its solution.

## Minimum squared acceleration

**Theorem 1.** Among all functions $x$ on $[0, T]$ with a square integrable second derivative and the same four end conditions, the cubic $q$ has the smallest value of $J(x) = \int_0^T x''(t)^2\, dt$, and it is the only minimizer.

*Proof.* Write $x = q + \eta$. Then $\eta(0) = \eta'(0) = \eta(T) = \eta'(T) = 0$, and

$$J(x) = J(q) + 2\int_0^T q'' \eta''\, dt + J(\eta).$$

Integrate the middle term by parts twice:

$$\int_0^T q'' \eta''\, dt = \big[q'' \eta'\big]_0^T - \big[q''' \eta\big]_0^T + \int_0^T q'''' \eta\, dt.$$

The two brackets are zero because $\eta'$ and $\eta$ vanish at both ends, and $q'''' = 0$ because $q$ is a cubic. So $J(x) = J(q) + J(\eta) \ge J(q)$. Equality needs $\eta'' = 0$ almost everywhere, so $\eta$ is linear, and a linear function with $\eta(0) = \eta(T) = 0$ is zero. $\square$

## Via points

**Theorem 2.** For via points $q_0, \dots, q_n$ at times $t_0 < \dots < t_n$ with chosen velocities $v_0, \dots, v_n$, the piecewise cubic built by calling the method on each interval $[t_i, t_{i+1}]$ is continuous with a continuous first derivative.

*Proof.* By Lemma 1, the piece on $[t_{i-1}, t_i]$ ends with position $q_i$ and velocity $v_i$, and the piece on $[t_i, t_{i+1}]$ starts with the same position and velocity. $\square$

The acceleration is not continuous at the via points in general. It is continuous only for the special choice of the inner velocities that a [cubic spline](/cubic-spline-interpolation/) makes.
