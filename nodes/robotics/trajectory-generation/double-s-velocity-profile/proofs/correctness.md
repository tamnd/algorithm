---
title: The double-S profile covers the distance and respects the velocity, acceleration and jerk limits
proves: [correctness]
status: full
---

We use the notation of the page. One axis moves the distance $D > 0$ from rest to rest with $|v| \le V$, $|a| \le A$ and $|j| \le J$. Lines L1 to L8 return the jerk time $T_j$, the acceleration time $T_a$, the cruise time $T_v$, the peak velocity $v_p$ and $T = 2T_a + T_v$. The seven pieces have jerk $+J, 0, -J, 0, -J, 0, +J$ and durations $T_j, T_a - 2T_j, T_j, T_v, T_j, T_a - 2T_j, T_j$. This file proves that the profile is admissible and covers $D$. It does not prove that the profile is the fastest one.

## One acceleration phase

**Lemma 1.** Let $0 < T_j$ and $2T_j \le T_a$. The phase with jerk $+J$ for $T_j$, jerk $0$ for $T_a - 2T_j$ and jerk $-J$ for $T_j$, started at rest, has:

1. acceleration between $0$ and $J T_j$,
2. a velocity that does not decrease, from $0$ to $J T_j (T_a - T_j)$,
3. the distance $\frac12 v_p T_a$, where $v_p$ is the final velocity, and a final acceleration of $0$.

*Proof.* The acceleration is a trapezoid in time: it rises to $J T_j$, stays there and falls back to 0. This gives 1, the final acceleration 0, and, as it is not negative, the monotone velocity. The final velocity is the area of the acceleration trapezoid, $J T_j \cdot (T_a - T_j)$, which is 2. The acceleration is symmetric about $T_a / 2$, so the velocity satisfies $v(T_a - t) = v_p - v(t)$. Then $\int_0^{T_a} v = \int_0^{T_a} (v_p - v)$, which gives $\int_0^{T_a} v = \frac12 v_p T_a$. $\square$

The deceleration phase is the same phase with the opposite signs, run from $v_p$ down to 0, and it covers $\frac12 v_p T_a$ too. With a cruise of $T_v$ at $v_p$ in between, the whole move covers

$$v_p T_a + v_p T_v = v_p (T_a + T_v), \tag{1}$$

it ends at rest with zero acceleration, its jerk is in $\{-J, 0, J\}$, its acceleration is at most $J T_j$ in size, and its speed is at most $v_p$. So it remains to show, for each branch, that $2T_j \le T_a$, $J T_j \le A$, $v_p \le V$, $T_v \ge 0$ and $v_p (T_a + T_v) = D$, with $v_p = J T_j (T_a - T_j)$ as in Lemma 1.

## The phase that reaches V

**Lemma 2.** After line L1 or line L2, the phase of Lemma 1 reaches exactly $V$ and its acceleration stays within $A$.

*Proof.* If $VJ \ge A^2$: $T_j = A/J$ and $T_a = T_j + V/A$, so $T_a - 2T_j = V/A - A/J \ge 0$, the peak acceleration is $J T_j = A$, and the final velocity is $A \cdot V/A = V$. If $VJ < A^2$: $T_j = \sqrt{V/J}$ and $T_a = 2T_j$, so the peak acceleration is $\sqrt{VJ} < A$, and the final velocity is $J T_j^2 = V$. $\square$

## With a cruise

If $V T_a \le D$ (line L3), line L4 sets $T_v = D/V - T_a \ge 0$ and $v_p = V$. By (1) the move covers $V(T_a + T_v) = D$. If also $VJ \ge A^2$, the total time is $T = T_a + (T_a + T_v) = A/J + V/A + D/V$.

## Without a cruise

Otherwise $V T_a > D$ for the times of Lemma 2, and line L5 sets $T_v = 0$. The move must cover $D = v_p T_a$ with a peak $v_p$ below $V$. For a peak $u$, let $g(u) = u \cdot T_a(u)$, where $T_a(u) = u/A + A/J$ if $uJ \ge A^2$ and $T_a(u) = 2\sqrt{u/J}$ otherwise. These are the times of Lemma 2 with $u$ in place of $V$. Both pieces of $g$ are increasing, they agree at $u = A^2/J$ where $g = 2A^3/J^2$, so $g$ is continuous and strictly increasing, and $g(V) = V T_a > D$.

**Line L6**, $DJ^2 \ge 2A^3$. Then the solution of $g(u) = D$ has $u \ge A^2/J$, and solves $u^2/A + uA/J = D$, that is $u^2 + (A^2/J)u - AD = 0$. Its positive root is the $v_p$ of line L6, and line L6 sets $T_j = A/J$ and $T_a = v_p/A + A/J$, so $T_a - 2T_j = v_p/A - A/J \ge 0$ and the peak acceleration is $A$.

**Line L7**, $DJ^2 < 2A^3$. Then the solution has $u < A^2/J$ and solves $2u\sqrt{u/J} = D$, that is $u^3 = D^2 J / 4$, which is line L7. Line L7 sets $T_j = \sqrt{v_p/J}$ and $T_a = 2T_j$, and the peak acceleration is $\sqrt{v_p J} < A$.

In both lines, $v_p < V$ because $g$ is increasing and $g(v_p) = D < g(V)$, and the move covers $v_p T_a = D$ by (1). In both lines Lemma 1 gives the final velocity $J T_j (T_a - T_j) = v_p$, as a direct check shows: $A (v_p / A) = v_p$ for line L6 and $J T_j^2 = v_p$ for line L7. $\square$

## Sampling

Lines L9 and L10 integrate the pieces with the exact formulas for constant jerk $j$ over a time $h$: $s \leftarrow s + vh + \frac12 a h^2 + \frac16 j h^3$, $v \leftarrow v + ah + \frac12 j h^2$, $a \leftarrow a + jh$. These are the Taylor expansions of a cubic, which have no remainder, so the samples are exact in exact arithmetic.

## What is not proved here

The profile is the natural extension of the trapezoid. When $V$ and $A$ are both reached, its time exceeds the time $D/V + V/A$ of the trapezoid by exactly $A/J$. In the other cases the difference can be smaller or larger than $A/J$. For example, with $D = 0.2$, $V = 1$, $A = 2$ and $J = 8$, the trapezoid is a triangle with time $2\sqrt{0.1} \approx 0.6325$, and the double S needs $0.9283$, which is $0.296$ more, while $A/J = 0.25$. This file does not prove that no other jerk-limited motion is faster, so the page does not claim that as a theorem.
