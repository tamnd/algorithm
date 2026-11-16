---
title: The candidate enumeration returns a time-optimal motion, and the online cycle loses no time
proves: [correctness]
status: full
---

We use the notation of the page. One axis has the state $(p, v)$, the limits $|v| \le V$ and $|\dot v| \le A$, the current state $(p_0, v_0)$ and the target state $(p_T, v_T)$, with $|v_0| \le V$ and $|v_T| \le V$. Let $D = p_T - p_0$. A motion of duration $T$ is admissible if its velocity $v$ on $[0, T]$ is Lipschitz with constant $A$, stays in $[-V, V]$, has $v(0) = v_0$ and $v(T) = v_T$, and $\int_0^T v = D$. The proof is in exact arithmetic.

## The set of reachable times

Let $T_0 = |v_T - v_0| / A$. For $T \ge T_0$ define the envelopes

$$u_T(t) = \min(v_0 + At,\ V,\ v_T + A(T - t)), \qquad l_T(t) = \max(v_0 - At,\ -V,\ v_T - A(T - t)),$$

and $P_{\max}(T) = \int_0^T u_T$, $P_{\min}(T) = \int_0^T l_T$.

**Lemma 1.** A motion of duration $T$ exists if and only if $T \ge T_0$ and $P_{\min}(T) \le D \le P_{\max}(T)$.

*Proof.* If $v$ is admissible, then $|v_T - v_0| \le AT$, so $T \ge T_0$. The Lipschitz bound gives $v(t) \le v_0 + At$ and $v(t) \le v_T + A(T - t)$, and $v(t) \le V$, so $v \le u_T$; in the same way $v \ge l_T$. Integrating gives $P_{\min}(T) \le D \le P_{\max}(T)$.

Conversely, let $T \ge T_0$. Each of the three functions in $u_T$ is Lipschitz with constant $A$ and at least $-V$, so $u_T$ is too, and $u_T \le V$. At $t = 0$, $v_0 \le V$ and $v_T + AT \ge v_0$, so $u_T(0) = v_0$; in the same way $u_T(T) = v_T$. So $u_T$ is an admissible velocity profile except for the distance, and so is $l_T$, and so is every convex combination $(1 - \lambda) l_T + \lambda u_T$. Its distance $(1 - \lambda) P_{\min}(T) + \lambda P_{\max}(T)$ takes every value in between. $\square$

The set of reachable times need not be an interval: for some states a short motion and a long motion exist, but a motion of medium length does not. Kroger and Wahl call such gaps inoperative time intervals. The minimum still exists.

**Lemma 2.** The set $F$ of reachable times has a least element $T^*$, and $D = P_{\max}(T^*)$ or $D = P_{\min}(T^*)$.

*Proof.* $P_{\max}$ and $P_{\min}$ are continuous in $T$, so $F$ is closed. For large $T$, $u_T = V$ and $l_T = -V$ on most of $[0, T]$, so $P_{\max}(T) \to \infty$ and $P_{\min}(T) \to -\infty$, and $F$ is not empty. Let $T^* = \min F$. If $T^* = T_0$, then $u_{T^*} = l_{T^*}$ is the single ramp from $v_0$ to $v_T$, so both equalities hold. If $T^* > T_0$ and $P_{\min}(T^*) < D < P_{\max}(T^*)$, then by continuity a slightly smaller $T$ is in $F$, a contradiction. $\square$

## Every candidate is admissible

Lines L2 to L8 build, for $\sigma \in \{+1, -1\}$ and for each root $v_p = \pm\sqrt{r}$ of $v_p^2 = r = \sigma A D + (v_0^2 + v_T^2)/2$ that passes line L5, a profile with acceleration $\sigma A$, then $0$, then $-\sigma A$.

**Lemma 3.** Each candidate is an admissible motion of duration equal to its returned time.

*Proof.* Line L6 ($|v_p| \le V$): the durations $t_1 = \sigma(v_p - v_0)/A$ and $t_3 = \sigma(v_p - v_T)/A$ are not negative by line L5. The velocity moves monotonically from $v_0$ to $v_p$ and then from $v_p$ to $v_T$, all in $[-V, V]$, and ends at $v_p - (v_p - v_T) = v_T$. The distance is

$$\frac{\sigma(v_p^2 - v_0^2)}{2A} + \frac{\sigma(v_p^2 - v_T^2)}{2A} = \frac{\sigma(2r - v_0^2 - v_T^2)}{2A} = D.$$

Line L7 ($|v_p| > V$): with $v_c = \sigma V$, the ramps take $t_1 = (V - \sigma v_0)/A \ge 0$ and $t_3 = (V - \sigma v_T)/A \ge 0$ and cover $d = \sigma(2V^2 - v_0^2 - v_T^2)/(2A)$. Since $r > V^2$, $\sigma D > (2V^2 - v_0^2 - v_T^2)/(2A)$, so the cruise time $t_2 = (D - d)/v_c = (\sigma D - (2V^2 - v_0^2 - v_T^2)/(2A))/V$ is positive, and the distance is $d + v_c t_2 = D$. $\square$

## The best candidate is optimal

**Theorem 1.** Line L9 returns a motion of duration $T^*$.

*Proof.* By Lemma 3, every candidate time is in $F$, so it is at least $T^*$. By Lemma 2, say $D = P_{\max}(T^*)$; the other case is the mirror image with $\sigma = -1$. Then $u_{T^*}$ is an optimal velocity profile. It rises with slope $A$, may stay at $V$ for a time $t_2 \ge 0$, and falls with slope $A$.

If $t_2 = 0$, its peak $v_p$ satisfies $v_p \ge v_0$, $v_p \ge v_T$ and $|v_p| \le V$, and its distance is $(2v_p^2 - v_0^2 - v_T^2)/(2A) = D$, so $v_p^2 = r$ for $\sigma = +1$. So $v_p$ is one of the two roots of line L4, it passes line L5, and line L6 builds exactly this profile.

If $t_2 > 0$, the peak is $V$ and $D = (2V^2 - v_0^2 - v_T^2)/(2A) + V t_2$, so $r = V^2 + AVt_2 > V^2$. The root $+\sqrt r > V$ passes line L5, and line L7 builds exactly this profile. (The root $-\sqrt r < -V$ fails line L5, because $v_0 \ge -V$.)

So a candidate has time $T^*$, and line L9 returns a candidate of time $T^*$. $\square$

## The online cycle

Line L10 plans from the current state, and line L12 moves the state by $\Delta t$ along the plan. Let $T^*(x)$ be the minimum time from state $x$ to the fixed target.

**Theorem 2.** If the target does not change, $T^*$ of the new state is $T^*(x) - \Delta t$ whenever $T^*(x) > \Delta t$. So the loop reaches the target after $\lceil T^*(x_0) / \Delta t \rceil$ cycles, which is the time of the one-shot profile rounded up to a whole cycle.

*Proof.* The rest of the optimal profile from $x$ is admissible from the new state $x'$ and takes $T^*(x) - \Delta t$, so $T^*(x') \le T^*(x) - \Delta t$. If $T^*(x') < T^*(x) - \Delta t$, the first $\Delta t$ of the profile followed by an optimal motion from $x'$ would reach the target from $x$ in less than $T^*(x)$, a contradiction. In the last cycle, $T^* \le \Delta t$, and line L11 sets the state to the target. $\square$

If the target changes between two cycles, line L10 simply plans from the current state, which is admissible because every step of lines L10 to L12 keeps $|v| \le V$ and changes $v$ by at most $A \Delta t$. Lemma 1 then applies to the new target.
