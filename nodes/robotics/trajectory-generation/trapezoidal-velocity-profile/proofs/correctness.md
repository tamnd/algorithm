---
title: The trapezoidal profile covers the distance within the limits, and no rest-to-rest motion of one axis is faster
proves: [correctness]
status: full
---

We use the notation of the page. One axis moves the distance $D > 0$ from rest to rest. An admissible motion on $[0, T]$ is a function $s$ with $s(0) = 0$, $s(T) = D$, $s'(0) = s'(T) = 0$, an absolutely continuous velocity $v = s'$, $|v| \le V$ and $|v'| \le A$ almost everywhere. Lines L1 to L5 choose the ramp time $T_a$, the peak velocity $v_p$ and the time $T$; the velocity of the profile rises with slope $A$ for $T_a$, stays at $v_p$, and falls with slope $A$ for the last $T_a$.

## The profile is admissible and covers D

**Lemma 1.** The profile of lines L1 to L6 is admissible and covers exactly $D$.

*Proof.* Case $DA \ge V^2$ (lines L2 and L3). $T_a = V/A$ and $T = D/V + V/A$, so the cruise time is $T - 2T_a = D/V - V/A$, which is not negative because $DA \ge V^2$. The velocity is at most $v_p = V$ and its slope is $0$ or $\pm A$. The area under the velocity is that of a trapezoid, $v_p (T - T_a) = V \cdot D/V = D$.

Case $DA < V^2$ (lines L4 and L5). $T_a = \sqrt{D/A}$, $T = 2T_a$ and there is no cruise. The peak is $v_p = A T_a = \sqrt{DA} < V$. The area of the triangle is $v_p T_a = A T_a^2 = D$.

In both cases the velocity starts and ends at 0. $\square$

## No admissible motion is faster

**Lemma 2.** If $s$ is admissible on $[0, T]$, then $v(t) \le e_T(t) = \min(At, V, A(T - t))$ for all $t \in [0, T]$.

*Proof.* $v(t) = v(0) + \int_0^t v' \le At$, and $v(t) = v(T) - \int_t^T v' \le A(T - t)$, and $v(t) \le V$ by the velocity limit. $\square$

Let $E(T) = \int_0^T e_T(t)\, dt$, the area of the envelope.

**Lemma 3.** $E$ is strictly increasing in $T$.

*Proof.* Let $T_1 < T_2$. For $t \in [0, T_1]$, $e_{T_1}(t) \le e_{T_2}(t)$ because $A(T_1 - t) < A(T_2 - t)$. On $(T_1, T_2)$ the function $e_{T_2}$ is positive. So $E(T_2) \ge E(T_1) + \int_{T_1}^{T_2} e_{T_2} > E(T_1)$. $\square$

**Theorem 1.** Let $T^*$ be the time of line L3 or line L5. No admissible motion covers $D$ in a time $T < T^*$.

*Proof.* The velocity of the profile of Lemma 1 is exactly $e_{T^*}$. In the first case this is clear from the shape. In the second case $A t$ and $A(T^* - t)$ are both at most $A T^*/2 = \sqrt{DA} < V$ where they are the minimum, so the term $V$ never acts. So $E(T^*) = D$ by Lemma 1. If an admissible motion covered $D$ in time $T < T^*$, then by Lemma 2 and Lemma 3, $D = \int_0^T v \le E(T) < E(T^*) = D$, a contradiction. $\square$

The proof uses rest at both ends and one axis. With nonzero end velocities, or with several axes that share one path, the envelope is different and the profile of lines L1 to L5 is in general not the fastest.

## A longer prescribed time

**Lemma 4.** Let $T \ge T^*$. Then $T_a = (T - \sqrt{T^2 - 4D/A})/2$ gives a trapezoid with acceleration $A$ that covers $D$ in exactly $T$ with peak velocity at most $V$.

*Proof.* A trapezoid with ramp time $T_a \le T/2$ and slope $A$ has peak $A T_a$ and area $A T_a (T - T_a)$. The equation $A T_a (T - T_a) = D$ is $T_a^2 - T T_a + D/A = 0$. Its discriminant $T^2 - 4D/A$ is not negative because $T \ge T^* \ge 2\sqrt{D/A}$, and the given root is the smaller one, so $T_a \le T/2$. The smaller root decreases as $T$ grows. At $T = T^*$ it is the ramp time of Lemma 1 (in the first case $V/A$ solves the equation and is at most $T^*/2$), whose peak is at most $V$. So for $T \ge T^*$ the peak $A T_a$ is at most $V$. $\square$
