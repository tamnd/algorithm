---
title: The sampled PID update has the stated filter, steady state and anti-windup properties
proves: [correctness]
status: full
---

Notation is that of the page. The sampling period is $h > 0$, the samples are $r_k$ and $y_k$, the error is $e_k = r_k - y_k$ and the derivative error is $e^d_k = c\, r_k - y_k$. The parameters are $K > 0$, $T_i > 0$ (or no integral action), $T_d \ge 0$, $N > 0$ and $T_t > 0$ (or no tracking). Lines L1 to L9 compute

$$b_i = \frac{K h}{T_i}, \quad a_r = \frac{h}{T_t}, \quad a_d = \frac{T_d}{T_d + N h}, \quad b_d = \frac{K T_d N}{T_d + N h},$$

$$P_k = K (b\, r_k - y_k), \quad D_k = a_d D_{k-1} + b_d (e^d_k - e^d_{k-1}), \quad v_k = P_k + I_k + D_k, \quad u_k = \operatorname{sat}(v_k),$$

$$I_{k+1} = I_k + b_i e_k + a_r (u_k - v_k),$$

with $I_0 = D_{-1} = 0$ and $e^d_{-1} = e^d_0$. Here $\operatorname{sat}$ clips to $[u_{\min}, u_{\max}]$; with no limits, $u_k = v_k$.

## Claim 1: the terms are Euler approximations of the continuous terms

*The integral update is the forward Euler step of $I' = (K/T_i) e$. The derivative update is the backward Euler step of $(T_d/N) D' + D = K T_d\, (e^d)'$. The filter pole $a_d$ is in $[0, 1)$ for every $h > 0$, so the derivative filter is a Schur (asymptotically stable) first order filter for every sampling period.*

*Proof.* The forward Euler step of $I' = (K/T_i) e$ is $I_{k+1} = I_k + h (K/T_i) e_k = I_k + b_i e_k$, which is line L7 when $u_k = v_k$. For the filter, replace $D'$ and $(e^d)'$ at $t_k$ by the backward differences $(D_k - D_{k-1})/h$ and $(e^d_k - e^d_{k-1})/h$:

$$\frac{T_d}{N h}(D_k - D_{k-1}) + D_k = \frac{K T_d}{h} (e^d_k - e^d_{k-1}).$$

Multiply by $N h/(T_d + N h)$. This gives $D_k = a_d D_{k-1} + b_d (e^d_k - e^d_{k-1})$, which is line L4. For $T_d > 0$, $N > 0$ and $h > 0$ the value $a_d = T_d/(T_d + N h)$ is in $(0, 1)$, and for $T_d = 0$ it is 0. The homogeneous recursion $D_k = a_d D_{k-1}$ then decays like $a_d^k$. $\square$

The forward Euler step of the filter would give the pole $1 - N h/T_d$, which is outside the unit disc when $h > 2 T_d/N$. This is why the backward difference is used.

**Closed form on a ramp.** If $c = 0$ and $y_k = k h$, then $e^d_k - e^d_{k-1} = -h$ for $k \ge 1$, so $D_k = a_d D_{k-1} - b_d h$ with $D_0 = 0$. Since $b_d h/(1 - a_d) = K T_d$, induction gives $D_k = -K T_d (1 - a_d^k)$. The continuous filter gives $-K T_d (1 - e^{-N t/T_d})$, and $a_d^k$ tends to $e^{-N t/T_d}$ as $h \to 0$ with $k h = t$. The test checks the discrete formula exactly in Fraction.

## Claim 2: set-point weights change only the response to the set point

*Without limits, $u_k$ is a linear function of the past and present $r$ and $y$, and the part that acts on $y$ does not depend on $b$ or $c$. So the loop transfer function, the response to a load disturbance and the response to measurement noise do not depend on $b$ and $c$.*

*Proof.* Without limits $u_k = v_k$, so the recursions are linear. Write each signal as the sum of the part caused by $r$ and the part caused by $y$. The coefficient of $y$ in $P_k$ is $-K$, in the update of $D_k$ it is $-b_d$ (through $e^d$), and in the update of $I_{k+1}$ it is $-b_i$. None of these contains $b$ or $c$. The parameters $b$ and $c$ multiply only $r$. So the controller is $U = C_r R - C_y Y$ with $C_y$ independent of $b$ and $c$. The loop is closed through $C_y$ only, and every transfer function from a signal that enters the loop (a load disturbance or noise) to $y$ or $u$ contains only $C_y$ and the plant. By linearity, the response to $r$ and a load is the sum of the two separate responses, and only the first one changes with $b$ and $c$. $\square$

With $c = 0$ the derivative acts on $-y$ only, so a step in $r$ causes no impulse in $D$. With $c = 1$ a step of size $\Delta$ in $r$ adds $b_d \Delta$ to $u$ at that sample.

## Claim 3: zero steady-state error with integral action

*Let $T_i$ be finite and $r_k = r$ constant. If the closed loop converges, so that $y_k \to y_\infty$, $I_k \to I_\infty$ and $u_k \to u_\infty$, and if $u_\infty = v_\infty$ (the output is not held at a limit, or there are no limits), then $y_\infty = r$.*

*Proof.* From line L7, $I_{k+1} - I_k = b_i e_k + a_r (u_k - v_k)$. The left side tends to 0. The second term tends to $a_r (u_\infty - v_\infty) = 0$. So $b_i (r - y_\infty) = 0$, and $b_i = K h/T_i \ne 0$, so $y_\infty = r$. $\square$

The claim does not say that the loop converges. That depends on the plant and the tuning, and it is the subject of the stability analysis of the loop, for example with the [Nyquist stability criterion](/nyquist-stability-criterion/).

## Claim 4: back-calculation keeps the integral bounded under saturation

*Let the output be at the limit $u_{\max}$ for $k \ge k_0$, with $e_k = e$ and $P_k + D_k = q$ constant. If $0 < h/T_t < 2$, then $I_k$ converges geometrically with ratio $1 - h/T_t$, and $v_k$ converges to*

$$v_\infty = u_{\max} + \frac{T_t}{T_i} K e.$$

*Without tracking ($a_r = 0$), $I_k$ grows by $b_i e$ at each sample, without bound if $e \ne 0$.*

*Proof.* With $u_k = u_{\max}$ and $v_k = q + I_k$, line L7 reads $I_{k+1} = (1 - a_r) I_k + b_i e + a_r (u_{\max} - q)$. This is an affine recursion with the factor $1 - a_r$, and $|1 - a_r| < 1$ exactly when $0 < a_r < 2$. Its fixed point satisfies $a_r I_\infty = b_i e + a_r (u_{\max} - q)$, so $v_\infty = q + I_\infty = u_{\max} + (b_i/a_r) e = u_{\max} + (T_t/T_i) K e$. With $a_r = 0$ the recursion is $I_{k+1} = I_k + b_i e$. $\square$

So with tracking, $v$ stays within $(T_t/T_i) K |e|$ of the limit, and $v$ comes back below the limit as soon as $e$ changes sign, up to this offset. Without tracking, $v$ comes back only after the sum of the errors has undone the growth of $I$. This is the [integrator windup](/integrator-windup/) effect.

## Claim 5: the forms convert into each other

*The series form $K' (1 + 1/(T_i' s)) (1 + T_d' s)$ equals the ideal form $K (1 + 1/(T_i s) + T_d s)$ with*

$$K = K' \frac{T_i' + T_d'}{T_i'}, \quad T_i = T_i' + T_d', \quad T_d = \frac{T_i' T_d'}{T_i' + T_d'}.$$

*An ideal form has a series form with real $T_i', T_d' > 0$ if and only if $T_i \ge 4 T_d$. Then, with $q = \sqrt{1 - 4 T_d/T_i}$, one series form is $K' = K (1 + q)/2$, $T_i' = T_i (1 + q)/2$ and $T_d' = T_i (1 - q)/2$. The parallel form $k_p + k_i/s + k_d s$ has $k_p = K$, $k_i = K/T_i$ and $k_d = K T_d$.*

*Proof.* Expand the series form: $K' (1 + 1/(T_i' s))(1 + T_d' s) = K' (1 + T_d'/T_i') + K'/(T_i' s) + K' T_d' s$. Match the constant, the $1/s$ and the $s$ terms with $K + K/(T_i s) + K T_d s$. The constant gives $K = K'(T_i' + T_d')/T_i'$. The $1/s$ term gives $K/T_i = K'/T_i'$, so $T_i = T_i' K/K' = T_i' + T_d'$. The $s$ term gives $K T_d = K' T_d'$, so $T_d = T_d' K'/K = T_i' T_d'/(T_i' + T_d')$.

The ideal form is $K (T_i T_d s^2 + T_i s + 1)/(T_i s)$. The series form has the real zeros $-1/T_i'$ and $-1/T_d'$. So a series form exists only if the numerator $T_i T_d s^2 + T_i s + 1$ has real roots, that is $T_i^2 - 4 T_i T_d \ge 0$, or $T_i \ge 4 T_d$. Conversely, if $T_i \ge 4 T_d$, the given $T_i'$ and $T_d'$ are real and positive, $T_i' + T_d' = T_i$, $T_i' T_d' = T_i^2 (1 - q^2)/4 = T_i T_d$, so $T_i' T_d'/(T_i' + T_d') = T_d$, and $K'(T_i' + T_d')/T_i' = K (1 + q)/2 \cdot 2/(1 + q) = K$. The parallel form follows by expanding the ideal form. $\square$

The series form is unique up to swapping the roles of $T_i'$ and $T_d'$ (with the gain changed to match); the formula returns the one with $T_i' \ge T_d'$.

## Cost

Line L1 runs once. Lines L3 to L8 use a fixed number of operations (at most 10 multiplications and 10 additions) and keep three numbers of state ($I$, $D$ and $e^d_{k-1}$). So $k$ samples cost $O(k)$ time and $O(1)$ space.
