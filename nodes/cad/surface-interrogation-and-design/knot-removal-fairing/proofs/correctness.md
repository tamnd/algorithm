---
title: The fairing step makes the curve C3 at the knot, moves one control point, and keeps the curve within the tolerance
proves: [correctness]
status: full
---

We use the notation of the page. The curve is $c(t) = \sum_{i=0}^{n} N_i(t) d_i$, a planar cubic B-spline on the clamped knots $t_0, \dots, t_{n+4}$ with simple inner knots $t_4 < \dots < t_n$. Let $4 \le r \le n$, and let $\tau$ be the knot vector without $t_r$, so $\tau_i = t_i$ for $i < r$ and $\tau_i = t_{i+1}$ for $i \ge r$.

## Lemma 1 (the step is removal and reinsertion)

Let $e_i = d_i$ for $i \le r - 4$, $e_{r-3} = L$, $e_{r-2} = R$ and $e_i = d_{i+1}$ for $i \ge r - 1$, a cubic spline $e$ with $n$ control points on $\tau$. Boehm insertion of $t_r$ into $e$ gives exactly the control points $\hat d$ of the step: $\hat d_i = d_i$ for $i \ne r - 2$, and $\hat d_{r-2} = (1 - \alpha_{r-2}) L + \alpha_{r-2} R$.

*Proof.* The knot $t_r$ lies in the span $\tau_{r-1} \le t_r < \tau_r$ of $\tau$, since $\tau_{r-1} = t_{r-1} < t_r < t_{r+1} = \tau_r$. Boehm's rule for inserting $t_r$ into a cubic on $\tau$ with span index $r - 1$ keeps $e_i$ for $i \le r - 4$, shifts $e_{i-1}$ to place $i$ for $i \ge r$, and for $i = r - 3, r - 2, r - 1$ sets the new point to $(1 - a_i) e_{i-1} + a_i e_i$ with $a_i = (t_r - \tau_i)/(\tau_{i+3} - \tau_i)$. With $\tau_{r-3} = t_{r-3}$ and $\tau_r = t_{r+1}$ this is $a_{r-3} = \alpha_{r-3}$, and in the same way $a_{r-2} = \alpha_{r-2}$ and $a_{r-1} = \alpha_{r-1}$. The denominators are positive, and $0 < \alpha_{r-3}$ and $\alpha_{r-1} < 1$ because the inner knots are simple, so $L$ and $R$ are defined. Now:

- for $i = r - 3$ the new point is $(1 - \alpha_{r-3}) d_{r-4} + \alpha_{r-3} L = d_{r-3}$, by the definition of $L$;
- for $i = r - 1$ it is $(1 - \alpha_{r-1}) R + \alpha_{r-1} d_r = d_{r-1}$, by the definition of $R$;
- for $i = r - 2$ it is $(1 - \alpha_{r-2}) L + \alpha_{r-2} R = \hat d_{r-2}$;
- all other points are $d_i$.

$\square$

## Theorem 1 (the step removes the jump)

After the step at $t_r$ the curve $\hat c = \sum_i N_i \hat d_i$ is a single cubic polynomial on $(t_{r-1}, t_{r+1})$. Hence $\hat c'''$ is continuous at $t_r$, and, if $\hat c'(t_r) \ne 0$, the jump $\Delta_r$ of the curvature derivative at $t_r$ is $0$. Only the control point $d_{r-2}$ changes.

*Proof.* By Lemma 1, $\hat c$ equals $e$ after knot insertion, and knot insertion does not change a curve, so $\hat c = e$. The knot vector $\tau$ has no knot in $(t_{r-1}, t_{r+1})$, so $e$ is one polynomial of degree $3$ there. Its derivatives of every order are continuous at $t_r$. The curvature derivative is the formula of the page in $c'$, $c''$ and $c'''$, which is continuous wherever $c' \ne 0$. The last claim is part of Lemma 1. $\square$

## Lemma 2 (the jump of the curvature derivative)

At a simple inner knot a cubic spline is $C^2$. If $c'(t_r) \ne 0$, then $\kappa'$ jumps at $t_r$ by $\Delta_r = c'(t_r) \times (c'''(t_r^+) - c'''(t_r^-)) / |c'(t_r)|^3$.

*Proof.* Differentiate $\kappa = (c' \times c'')/|c'|^3$. Since $(c' \times c'')' = c'' \times c'' + c' \times c''' = c' \times c'''$ and $(|c'|^{-3})' = -3 (c' \cdot c'') |c'|^{-5}$,

$$\kappa' = \frac{c' \times c'''}{|c'|^3} - 3 \frac{(c' \times c'')(c' \cdot c'')}{|c'|^5}.$$

At $t_r$ the values $c'$ and $c''$ are the same from both sides, so the second term has no jump and the first jumps by the stated amount. $\square$

The implementation returns $\Delta_r^2 = (c' \times \delta)^2 / (c' \cdot c')^3$ with $\delta$ the jump of $c'''$, which is a rational number when the input is rational.

## Theorem 2 (the curve stays within the tolerance)

Let $d^0$ be the first control points and $d$ the control points at any time. Then $|c_d(t) - c_{d^0}(t)| \le \max_i |d_i - d^0_i| \le \varepsilon$ for all $t$.

*Proof.* The knots never change, so $c_d(t) - c_{d^0}(t) = \sum_i N_i(t)(d_i - d^0_i)$. The B-spline basis functions are non negative and sum to $1$ on the parameter interval, so this is a convex combination of the vectors $d_i - d^0_i$, and its length is at most the largest of their lengths. Line L6 accepts a step only if every $|\hat d_i - d^0_i| \le \varepsilon$, so the bound holds after every accepted step, and it holds at the start. $\square$

## Theorem 3 (termination)

The loop ends after at most the given number of rounds, and the measure $E$ falls strictly with every accepted step.

*Proof.* Each round either accepts one step, in line L7, or stops, in line L8. Line L6 accepts a step only if $E(\hat d) < E$. $\square$

## Lemma 3 (the count of curvature sign changes)

On a knot interval $[a, b]$ the function $f = c' \times c''$ is a polynomial of degree at most $2$, and the signs of $f(a)$, of $f$ at its vertex if the vertex lies in $(a, b)$, and of $f(b)$, with zeros dropped, have exactly as many sign changes as $f$ has on $[a, b]$.

*Proof.* On the interval $c$ is a cubic polynomial, $c(t) = A t^3 + B t^2 + C t + D$ with vectors $A, B, C, D$. Then $c' = 3 A t^2 + 2 B t + C$ and $c'' = 6 A t + 2 B$, and the coefficient of $t^3$ in $c' \times c''$ is $3 \cdot 6 \, (A \times A) = 0$. So $f$ has degree at most $2$. A polynomial of degree at most $2$ is monotone on $[a, b]$, or monotone on each side of its vertex $s$. On a monotone piece $f$ changes sign at most once, and it does so exactly when the signs at the ends of the piece differ, zeros dropped. The pieces are $[a, s]$ and $[s, b]$, or $[a, b]$ alone, so the sequence of signs at $a$, $s$ and $b$ sees every change. Since $c'$ and $c''$ are continuous at simple knots, the sequences of consecutive intervals join without new changes at the knots. The curvature has the sign of $f$ where $c' \ne 0$. The implementation finds $f$ from its values at $a$, $(a + b)/2$ and $b$, which determine a polynomial of degree at most $2$. $\square$

## What is not claimed

The method does not guarantee that the number of curvature sign changes falls. A lower $E$ is a design criterion for fairness, not a theorem about inflections. The test file has a parabola with a dent on its steep side: the step accepted at the worst knot lowers $E$, but both inflections remain, and no further step lowers $E$.
