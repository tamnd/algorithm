---
title: The quintic meets the six end conditions and is the only quintic that does
proves: [correctness]
status: full
---

We use the notation of the page. The input is the start state $(q_0, v_0, c_0)$, the end state $(q_1, v_1, c_1)$ of position, velocity and acceleration, and a duration $T > 0$. Let $h = q_1 - q_0$. Line L1 sets $a_0 = q_0$, $a_1 = v_0$ and $a_2 = c_0 / 2$, and lines L2 to L4 set

$$a_3 = \frac{20h - (8v_1 + 12v_0)T - (3c_0 - c_1)T^2}{2T^3}, \quad a_4 = \frac{-30h + (14v_1 + 16v_0)T + (3c_0 - 2c_1)T^2}{2T^4}, \quad a_5 = \frac{12h - 6(v_1 + v_0)T + (c_1 - c_0)T^2}{2T^5}.$$

The trajectory is $q(t) = \sum_{k=0}^{5} a_k t^k$ on $[0, T]$. The proof is in exact arithmetic.

## The start conditions

$q(0) = a_0 = q_0$, $q'(0) = a_1 = v_0$ and $q''(0) = 2a_2 = c_0$, directly.

## The end conditions

Let $u = a_3 T^3$, $v = a_4 T^4$ and $w = a_5 T^5$. Then

$$q(T) = q_0 + v_0 T + \tfrac12 c_0 T^2 + u + v + w,$$
$$T q'(T) = v_0 T + c_0 T^2 + 3u + 4v + 5w,$$
$$T^2 q''(T) = c_0 T^2 + 6u + 12v + 20w.$$

Each of $u, v, w$ is half of a combination of $h$, $v_1 T$, $v_0 T$, $c_0 T^2$ and $c_1 T^2$. The table gives the coefficients of these five terms in $2u$, $2v$, $2w$ and in the three sums.

| | $h$ | $v_1 T$ | $v_0 T$ | $c_0 T^2$ | $c_1 T^2$ |
|---|---|---|---|---|---|
| $2u$ | 20 | $-8$ | $-12$ | $-3$ | 1 |
| $2v$ | $-30$ | 14 | 16 | 3 | $-2$ |
| $2w$ | 12 | $-6$ | $-6$ | $-1$ | 1 |
| $2(u + v + w)$ | 2 | 0 | $-2$ | $-1$ | 0 |
| $2(3u + 4v + 5w)$ | 0 | 2 | $-2$ | $-2$ | 0 |
| $2(6u + 12v + 20w)$ | 0 | 0 | 0 | $-2$ | 2 |

So $u + v + w = h - v_0 T - \frac12 c_0 T^2$, $3u + 4v + 5w = v_1 T - v_0 T - c_0 T^2$, and $6u + 12v + 20w = c_1 T^2 - c_0 T^2$. Putting these into the three lines above gives $q(T) = q_0 + h = q_1$, $T q'(T) = v_1 T$ and $T^2 q''(T) = c_1 T^2$. Since $T > 0$, $q'(T) = v_1$ and $q''(T) = c_1$. $\square$

## Uniqueness

Let $p$ be the difference of two polynomials of degree at most 5 that meet the six conditions. Then $p$, $p'$ and $p''$ vanish at $0$ and at $T$, so $0$ and $T$ are roots of multiplicity at least 3, and $t^3 (t - T)^3$ divides $p$. That product has degree 6, so $p = 0$. So the $6 \times 6$ linear system of the six conditions is nonsingular for $T > 0$, and the formulas above are its solution. $\square$

## The rest-to-rest profile

With $h = 1$, $T = 1$ and zero end velocities and accelerations, the formulas give $a_3 = 10$, $a_4 = -15$, $a_5 = 6$, so $s(\tau) = 10\tau^3 - 15\tau^4 + 6\tau^5$, which is line L7. Its derivatives are

$$s'(\tau) = 30\tau^2(1 - \tau)^2, \quad s''(\tau) = 60\tau(1 - \tau)(1 - 2\tau), \quad s'''(\tau) = 60(1 - 6\tau + 6\tau^2).$$

The velocity $s'$ is not negative on $[0, 1]$, so $s$ rises from 0 to 1 without overshoot. Its largest value is at $\tau = 1/2$, where $s' = 30/16 = 15/8$. The acceleration $s''$ has its extremes where $s''' = 0$, at $\tau = (3 \mp \sqrt3)/6$. There $\tau(1 - \tau) = 1/6$ and $1 - 2\tau = \pm\sqrt3/3$, so $|s''| = 60 \cdot \frac16 \cdot \frac{\sqrt3}{3} = 10/\sqrt3$. The jerk at both ends is $s'''(0) = s'''(1) = 60$. For a move of length $D$ in time $T$ the values scale by $D/T$, $D/T^2$ and $D/T^3$.
