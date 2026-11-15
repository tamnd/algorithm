---
title: With an exact model the Smith predictor gives the delay-free loop followed by the delay
proves: [correctness]
status: full
---

Notation is that of the page. The plant is $P(s) = P_0(s) e^{-\theta s}$ with one input and one output, where $P_0$ is a proper rational transfer function. The model is $P_m(s) = P_{0m}(s) e^{-\theta_m s}$. The primary controller is $C(s)$. The controller sees

$$y_f = y + (P_{0m} - P_m) u, \qquad e = r - y_f, \qquad u = C e.$$

A load $v$ acts at the input of $P_0$, after the delay, as in the code, so $y = P u + P_0 v$. The delay-free loop is the loop of $C$ and $P_0$, with $L_0 = C P_0$, $S_0 = 1/(1 + L_0)$ and $T_0 = L_0/(1 + L_0)$. A transfer function is BIBO stable when it is proper and all its poles have negative real part; $e^{-\theta s}$ is BIBO stable. The loop is internally stable when every transfer function from the outside signals $r$, $v$ and a measurement noise $n$ to the signals inside the loop, the model output included, is BIBO stable.

The claims are of two kinds. Claims 1 to 5 are theorems. Claim 6 is about the cost. The numbers on the page that are not covered here are measurements.

## Claim 1: the closed loop with an exact model

*Let $P_m = P$. Then*

$$\frac{y}{r} = \frac{C P_0}{1 + C P_0} e^{-\theta s} = T_0(s) e^{-\theta s}, \qquad \frac{y}{v} = P_0 \left(1 - T_0 e^{-\theta s}\right).$$

*So the delay leaves the characteristic equation, and the set-point response is that of the delay-free loop, delayed by $\theta$.*

*Proof.* From $u = C(r - y - (P_0 - P) u)$,

$$u = K (r - y), \qquad K = \frac{C}{1 + C P_0 - C P}.$$

Then $1 + P K = (1 + C P_0)/(1 + C P_0 - C P)$, so $y/r = P K/(1 + P K) = C P/(1 + C P_0) = T_0 e^{-\theta s}$. For the load, $y = P_0 v/(1 + P K) = P_0 v (1 + C P_0 - C P)/(1 + C P_0) = P_0 v (1 - T_0 e^{-\theta s})$. A load at the plant input, before the delay, only adds the factor $e^{-\theta s}$. $\square$

**The sampled loop.** The code works on the sampled system. With the sampling period $h$, a zero-order hold and $\theta = d h$, the plant is $x_{k+1} = A_d x_k + B_d u_{k-d}$, $y_k = C x_k$, from $x_0 = 0$ and with $u_j = 0$ for $j < 0$. The model with $d_m = d$ and the same matrices has the state $\hat x_k$ with $\hat x_{k+1} = A_d \hat x_k + B_d u_k$, $\hat x_0 = 0$.

*With an exact model, $y_k = y^0_{k-d}$ for $k \ge d$ and $y_k = 0$ for $k < d$, where $y^0$ is the output of the sampled delay-free loop of the same controller from rest.*

*Proof.* Set $\hat x_j = 0$ for $j \le 0$. By induction on $k$, $x_k = \hat x_{k-d}$: it holds for $k \le d$, where both sides are 0, and $x_{k+1} = A_d x_k + B_d u_{k-d} = A_d \hat x_{k-d} + B_d u_{k-d} = \hat x_{k+1-d}$. So $y_k = C \hat x_{k-d}$, which is the oldest value $\hat y_{k-d}$ in the delay line of the model. Line L1 then gives $y_f = \hat y_k + (y_k - \hat y_{k-d}) = \hat y_k$. So the controller sees $C \hat x_k$, and the pair (model, controller) runs exactly as the delay-free loop with the plant state $\hat x$. Thus $\hat x_k = x^0_k$, $u_k = u^0_k$ and $y_k = C x^0_{k-d} = y^0_{k-d}$. $\square$

In the code the plant and the model compute $y_k$ and $\hat y_{k-d}$ by the same floating point operations on the same numbers, so $y_k - \hat y_{k-d}$ is exactly 0 and the equality holds in floating point too. The tests compare with `==`.

## Claim 2: a plant with a pole in the right half-plane

*Let $P_m = P$, and let $P_0$ have a pole $p$ with $\operatorname{Re} p \ge 0$ where $C$ has no zero. Let $\theta > 0$ and $e^{-\theta p} \ne 1$, which holds for every real $p > 0$. Then $y/v$ has the pole $p$, so the loop is not internally stable, for every choice of $C$.*

*Proof.* At $s = p$ the loop gain $L_0 = C P_0$ is infinite, so $T_0(p) = 1$. The factor $1 - T_0 e^{-\theta s}$ in Claim 1 is analytic near $p$ and has the value $1 - e^{-\theta p} \ne 0$ there, so it does not cancel the pole of $P_0$. Thus $y/v = P_0 (1 - T_0 e^{-\theta s})$ has the pole $p$. $\square$

For $P_0 = 1/(s - 1)$ and a load step of size $w$, the term of $y$ from this pole is $w (1 - e^{-\theta}) e^{t}$, so $y$ grows by the factor $e$ each second. The set-point response $T_0 e^{-\theta s}$ still converges. The growing mode is in the plant and in the model, and the two copies cancel in $y - \hat y_d$. A load excites the copy in the plant only, so nothing cancels it.

**A pole at the origin.** For $p = 0$ the factor $1 - T_0 e^{-\theta s}$ is 0 at $s = 0$ and cancels the pole, so Claim 2 does not apply. But let $P_0 = P_1/s$ with $P_1(0) \ne 0$, and let the loop converge. The loop gain $C P_0$ has at least one integrator, so near 0 either $T_0 = c/(s + c) + O(s^2)$ with $c > 0$, which gives $T_0'(0) = -1/c$, or $T_0 = 1 + O(s^2)$ when $C P_0$ has two or more integrators, which gives $T_0'(0) = 0$. In both cases $T_0'(0) \le 0$, and a load step of size $w$ gives, by the final value theorem,

$$\lim_{t \to \infty} y(t) = w \lim_{s \to 0} \frac{P_1(s)}{s} (1 - T_0 e^{-\theta s}) = w P_1(0) \left(\theta - T_0'(0)\right) \ne 0.$$

So a constant load leaves a constant error, even when $C$ has an integrator.

## Claim 3: internal stability with an exact model

*Let $P_m = P$, and let $P_0$ be BIBO stable. Then the Smith predictor loop is internally stable if and only if the delay-free loop of $C$ and $P_0$ is internally stable.*

*Proof.* Write $Q = C/(1 + C P_0) = C S_0$. With an exact model the signal $y - P_m u$ that the predictor feeds back equals $P_0 v + n$, and the controller is $u = Q (r - (y + n - P_m u))$; to check this, solve $u = C(r - y - n - (P_0 - P_m) u)$ for $u$ and compare. So

$$u = Q r - Q P_0 v - Q n, \qquad y = P Q r + P_0 (1 - P Q) v - P Q n,$$

and the model output is $P_{0m} u$ and $P_m u$. If $Q$ is BIBO stable, every one of these is a product of BIBO stable factors, so the loop is internally stable. If the loop is internally stable, then $u/r = Q$ is BIBO stable. So the Smith loop is internally stable if and only if $Q$ is BIBO stable.

For the delay-free loop, internal stability means that $S_0$, $P_0 S_0$, $C S_0$ and $T_0$ are BIBO stable. If so, $Q = C S_0$ is BIBO stable. Conversely, if $Q$ is BIBO stable, then $T_0 = P_0 Q$, $S_0 = 1 - P_0 Q$, $P_0 S_0 = P_0 (1 - P_0 Q)$ and $C S_0 = Q$ are all BIBO stable. $\square$

This is the internal model control structure with the parameter $Q = C/(1 + C P_0)$. The proof also shows why the plant must be BIBO stable: for a plant with a pole in the right half-plane, $P_0 (1 - P Q)$ keeps the pole, as in Claim 2.

## Claim 4: robust stability against model errors

*Let $P$ and $P_m$ be BIBO stable, and let the delay-free loop with the model be internally stable, so that $Q = C/(1 + C P_{0m})$ is BIBO stable. Write $P = P_m (1 + \Delta)$. If*

$$\left| T_{0m}(j\omega) \right| \left| \Delta(j\omega) \right| < 1 \quad \text{for all } \omega, \qquad T_{0m} = \frac{C P_{0m}}{1 + C P_{0m}},$$

*then the loop with the plant $P$ is internally stable. For a delay error only, $P = P_m e^{-\delta s}$, the condition is $|T_{0m}(j\omega)|\, |e^{-j\omega\delta} - 1| < 1$.*

*Proof.* With the model error, the predictor feeds back $y - P_m u = (P - P_m) u + P_0 v + n$, and $u = Q (r - (P - P_m) u - P_0 v - n)$. So the loop is the feedback of $Q$ and $P - P_m = P_m \Delta$, both BIBO stable. On the imaginary axis $|Q (P - P_m)| = |Q P_{0m}|\, |e^{-j\omega\theta_m}|\, |\Delta| = |T_{0m}|\, |\Delta| < 1$. By the [small gain theorem](/small-gain-theorem/), $1/(1 + Q (P - P_m))$ is BIBO stable, and the other closed loop transfer functions are products of it with BIBO stable factors. $\square$

The condition is sufficient only. For $T_{0m} = 2/(s + 2)$ and a delay error $\delta$, the left side has its maximum below 1 for $|\delta| < 0.7387$ s, and the maximum is 0.3573 for $|\delta| = 0.2$ s. For a gain error, $\Delta = g - 1$ is a constant, and since $|T_{0m}| \le 1$ for this $T_{0m}$, every gain ratio $0 < g < 2$ is covered. Since $|e^{-j\omega\delta} - 1|$ reaches 2 at high frequency, a delay error of any size needs $|T_{0m}| < 1/2$ there. That is the reason to keep the bandwidth of the delay-free loop moderate when the delay is not well known.

## Claim 5: integral action and the load response

*Let $P_m = P$, let $P_0$ be BIBO stable with $P_0(0) \ne 0$, let the loop be internally stable, and let $C$ have a simple pole at 0 with the residue $K/T_i$, as the PI controller $K (1 + 1/(T_i s))$ has. Then a set-point step gives zero steady-state error, and for a unit load step at the plant input*

$$\int_0^\infty y(t)\, dt = \frac{T_i}{K} + P_0(0)\, \theta.$$

*Proof.* Near $s = 0$, $L_0 = C P_0 \approx c/s$ with $c = K P_0(0)/T_i$, so $T_0(0) = 1$ and the [final value theorem](/final-value-theorem/) gives $y \to T_0(0) = 1$ for a unit set-point step. For the load, $Y(s) = G(s)/s$ with $G = P_0 (1 - T_0 e^{-\theta s})$. Since $G(0) = P_0(0)(1 - 1) = 0$ and $Y$ is analytic at $0$, the integral of $y$ is $Y(0) = G'(0)$. The derivative is

$$G'(0) = P_0(0) \left( \theta - T_0'(0) \right),$$

and $T_0 = c/(s + c) + O(s^2)$ near 0 gives $T_0'(0) = -1/c$. So $G'(0) = P_0(0)\theta + P_0(0) T_i/(K P_0(0))$. $\square$

The same loop without the delay has the integral $T_i/K$. So the predictor cannot remove the term $P_0(0)\theta$: the controller sees the load only after the delay. With PI control and no predictor the integral is $T_i/K$ as well, but $K/T_i$ must then be small enough for the loop with the delay, which makes $T_i/K$ large.

The same result holds for the sampled loop with the PI law of the code: the sum $h \sum_k y_k$ equals $T_i/K + P_0(0)\, d h$, because the sampled integrator $(K h/T_i)/(z - 1)$ gives $c = K P_0(0) h/T_i$ in the variable $z - 1$. The tests check $2.5$ for $P_0 = 1/(s + 1)$, $\theta = 2$ s, $K = 2$, $T_i = 1$ s and $6.5$ for the plant gain 3.

## Claim 6: the cost

*One controller step costs $O(n^2)$ time and the controller keeps $O(n + d_m)$ numbers, where $n$ is the order of the model and $d_m$ the delay of the model in samples. A run of $k$ samples costs $O(k n^2)$ time.*

*Proof.* Lines L1 to L3 and L6 cost $O(1)$, plus the cost of the primary controller, which is $O(1)$ for a PI controller. Line L4 multiplies an $n \times n$ matrix by a vector, $O(n^2)$, and computing $\hat y$ costs $O(n)$. Line L5 appends to and removes from a queue of length $d_m$, $O(1)$. The state is the model state, $n$ numbers, and the delay line, $d_m$ numbers. The simulated plant has the same cost per step. $\square$
