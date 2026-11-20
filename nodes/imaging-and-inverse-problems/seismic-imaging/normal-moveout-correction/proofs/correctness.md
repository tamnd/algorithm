---
title: NMO correction moves a hyperbolic event to its zero-offset time, stretches it by t/t0, and the hyperbola is exact for one layer and second-order accurate for flat layers
proves: [correctness]
status: full
---

**Setting.** A trace $d(t)$ is recorded at offset $x$ and sampled at $t_k = k\,\Delta t$, $k = 0, \ldots, n - 1$. Times are two-way times. The velocity $v(t_0) > 0$ is given for each output time $t_0 = j\,\Delta t$. NMO (lines L1 to L6) sets the output sample $j$ to $\tilde d(t_j^\ast)$, where $t_j^\ast = \sqrt{t_0^2 + x^2 / v(t_0)^2}$ and $\tilde d$ is the linear interpolant of the samples, or to $0$ when line L4 mutes it. We write $T(t_0) = \sqrt{t_0^2 + x^2/v^2}$ for a constant $v$.

**Claim 1 (one flat layer).** Let a flat reflector lie at depth $z$ under a layer of constant velocity $v$, with the source and the receiver on the surface at offset $x$, symmetric about the midpoint. Then the reflection time is $t(x) = \sqrt{t_0^2 + x^2/v^2}$ with $t_0 = 2z/v$.

*Proof.* By the law of reflection at a flat interface, the ray goes from the source to the point under the midpoint and back up. Each leg is the hypotenuse of a right triangle with sides $z$ and $x/2$, so the path length is $2\sqrt{z^2 + x^2/4}$. Dividing by $v$ gives $t(x) = \sqrt{4z^2/v^2 + x^2/v^2} = \sqrt{t_0^2 + x^2/v^2}$. $\square$

**Claim 2 (an event is moved to $t_0$).** Let the trace hold one event $d(t) = w(t - T(\tau))$ with a wavelet $w$ that peaks at $0$, at the time $T(\tau)$ of the hyperbola through the zero-offset time $\tau$, and let the velocity used in line L3 equal the $v$ of the event. Without the interpolation error and the mute, the output is $u(t_0) = w(T(t_0) - T(\tau))$, and it peaks at $t_0 = \tau$ for every offset $x$.

*Proof.* Lines L2 and L3 compute $t = T(t_0)$, and line L5 reads the input at that time, so $u(t_0) = d(T(t_0)) = w(T(t_0) - T(\tau))$. The map $T$ is strictly increasing on $t_0 \ge 0$, because $T'(t_0) = t_0 / T(t_0) > 0$ for $t_0 > 0$. So $T(t_0) - T(\tau) = 0$ only at $t_0 = \tau$, and $u$ takes the peak value $w(0)$ there. The argument holds for each $x$, so all traces of the gather have the event at the same time $\tau$: the event is flat after the correction. $\square$

**Claim 3 (the stretch).** Near $t_0$, the output is the input wavelet stretched in time by the factor $T(t_0)/t_0 \ge 1$. For small offsets, the relative stretch is $(T(t_0) - t_0)/t_0 = x^2 / (2 v^2 t_0^2) + O(x^4)$.

*Proof.* By Claim 2, $u(t_0 + h) = w(T(t_0 + h) - T(t_0) + T(t_0) - T(\tau))$, and $T(t_0 + h) - T(t_0) = T'(t_0)\,h + O(h^2)$ with $T'(t_0) = t_0 / T(t_0)$. So an output interval $h$ reads an input interval $(t_0/T(t_0))\,h$, and a feature of length $\ell$ in the input has length $(T(t_0)/t_0)\,\ell$ in the output. Its dominant frequency falls by the factor $t_0/T(t_0)$. The expansion $\sqrt{1 + s} = 1 + s/2 + O(s^2)$ with $s = x^2/(v^2 t_0^2)$ gives the small-offset form. Line L4 sets to $0$ the samples with $(T - t_0)/t_0$ above the chosen limit; this is a choice of the user, not part of the correction. For $t_0 = 0$ and $x \ne 0$ the stretch is infinite, so line L4 always mutes that sample when a limit is given. $\square$

**Claim 4 (interpolation error).** If $d$ has a continuous second derivative, the output differs from the exact value $d(T(t_0))$ by at most $\Delta t^2 \max |d''| / 8$. If $T(t_0)$ falls on a sample time, the output is exact.

*Proof.* Line L5 evaluates the linear interpolant between the two samples around $t = T(t_0)$. The standard error formula of linear interpolation on an interval of length $\Delta t$ gives $|d(t) - \tilde d(t)| = |d''(\xi)|\,(t - t_k)(t_{k+1} - t)/2 \le \Delta t^2 \max |d''| / 8$. At a sample time the weight $f$ in the code is $0$, and the interpolant returns the sample. $\square$

**Claim 5 (flat layers: the hyperbola is a second-order approximation).** Let there be $N$ flat layers with velocities $v_k$ and two-way vertical times $\Delta t_k$, with $t_0 = \sum_k \Delta t_k$ and the rms velocity $V^2 = \sum_k v_k^2 \Delta t_k / t_0$. Then the exact reflection time from the bottom of layer $N$ satisfies $t(x)^2 = t_0^2 + x^2/V^2 + O(x^4)$. It equals the hyperbola for all $x$ only when all $v_k$ are equal.

*Proof.* Let $p$ be the ray parameter, constant along the ray by Snell's law, and $c_k = \sqrt{1 - p^2 v_k^2}$, the cosine of the angle in layer $k$. In layer $k$ the ray travels the vertical distance $v_k \Delta t_k / 2$ down and again up; it covers the horizontal distance $p v_k^2 \Delta t_k / (2 c_k)$ and spends the time $\Delta t_k / (2 c_k)$ on each leg. Summing both legs gives
$$x(p) = p \sum_k \frac{v_k^2 \Delta t_k}{c_k}, \qquad t(p) = \sum_k \frac{\Delta t_k}{c_k}.$$
With $1/c_k = 1 + p^2 v_k^2/2 + O(p^4)$ this is $x = p\,t_0 V^2 + O(p^3)$ and $t = t_0 + p^2 t_0 V^2 / 2 + O(p^4)$. So $t^2 = t_0^2 + p^2 t_0^2 V^2 + O(p^4)$ and $x^2/V^2 = p^2 t_0^2 V^2 + O(p^4)$, which gives $t^2 = t_0^2 + x^2/V^2 + O(p^4)$. Since $x$ is proportional to $p$ for small $p$, $O(p^4) = O(x^4)$. If all $v_k = v$, then $V = v$ and the stack of layers is one layer, so Claim 1 gives equality. If the $v_k$ differ, take one more term: $1/c_k = 1 + p^2 v_k^2/2 + 3 p^4 v_k^4/8 + O(p^6)$ gives $t^2 - t_0^2 - x^2/V^2 = -p^4 t_0^2 (\overline{v^4} - V^4)/4 + O(p^6)$, where $\overline{v^4} = \sum_k v_k^4 \Delta t_k / t_0$. By the Cauchy-Schwarz inequality $\overline{v^4} > V^4$ when the $v_k$ are not all equal, so the term is not zero, and the true time is earlier than the hyperbola at moderate offsets. $\square$

**Claim 6 (cost).** One trace of $n$ samples costs $O(n)$ operations: lines L2 to L5 do a fixed amount of work for each $j$. A gather of $m$ traces costs $O(m n)$, and the extra space is the $n$ output samples per trace. $\square$
