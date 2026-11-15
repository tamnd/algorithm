---
title: The ultimate point search and the tangent fit compute what the Ziegler-Nichols rules need
proves: [correctness]
status: full
---

Notation is that of the page. The plant is $P(s) = \frac{n(s)}{d(s)} e^{-\theta s}$ with real polynomials $n$ and $d$, $\deg n < \deg d$, and a delay $\theta \ge 0$. The P controller is a gain $K > 0$, so the loop transfer function is $L = K P$ and the closed-loop poles are the roots of $d(s) + K n(s) e^{-\theta s} = 0$. The ultimate frequency $\omega_u$ is the smallest $\omega > 0$ where the continuous phase of $P(j\omega)$ is $-\pi$. Then $K_u = 1/|P(j\omega_u)|$ and $T_u = 2\pi/\omega_u$.

The rules themselves (lines L5 and L8) are rules of thumb. Nothing below proves that they give a good loop. The claims prove that lines L1 to L4 and L6 to L7 compute the quantities that the rules take as input.

## Claim 1: at $K = K_u$ the closed loop has the poles $\pm j\omega_u$

*If $\arg P(j\omega_u) = -\pi$ (modulo $2\pi$) and $K_u = 1/|P(j\omega_u)|$, then $s = j\omega_u$ and $s = -j\omega_u$ are roots of $d(s) + K_u n(s) e^{-\theta s}$. Conversely, if $j\omega$ with $\omega > 0$ is a root for some $K > 0$, then $\arg P(j\omega) = -\pi$ modulo $2\pi$ and $K = 1/|P(j\omega)|$.*

*Proof.* By the assumptions $P(j\omega_u) = |P(j\omega_u)| e^{-j\pi} = -1/K_u$. So $1 + K_u P(j\omega_u) = 0$. Multiply by $d(j\omega_u)$, which is not 0 because $P(j\omega_u)$ is finite: $d(j\omega_u) + K_u n(j\omega_u) e^{-j\omega_u \theta} = 0$. The coefficients are real, so the conjugate $-j\omega_u$ is a root too. For the converse, a root $j\omega$ with $d(j\omega) \ne 0$ gives $K P(j\omega) = -1$, so $P(j\omega)$ is a negative real number with modulus $1/K$. If $d(j\omega) = 0$, the equation gives $n(j\omega) = 0$ too, and $P$ has a common factor that cancels; remove it first. $\square$

So the gain $K_u$ puts a pair of closed-loop poles on the imaginary axis, and the loop then oscillates with the period $T_u$. This is the experiment that Ziegler and Nichols did by hand.

## Claim 2: for $0 < K < K_u$ the closed loop is asymptotically stable, under a monotone gain

*Assume that $P$ has no poles in the open right half plane, that its only possible pole on the imaginary axis is a simple pole at the origin, that the low-frequency gain is positive, and that $|P(j\omega)|$ is strictly decreasing for $\omega > 0$. Then the closed loop with the gain $K$ is asymptotically stable for every $0 < K < K_u$.*

*Proof.* Take $0 < K < K_u$. By the [Nyquist stability criterion](/nyquist-stability-criterion/), for an open loop with no poles in the open right half plane, the closed loop is asymptotically stable if the Nyquist curve of $K P$ does not pass through or encircle $-1$. (With a delay the criterion still holds, because $P$ is analytic in the right half plane away from the origin and tends to 0 as $|s| \to \infty$ there.) For a pole at the origin the Nyquist contour goes around it on a small half circle $s = \varepsilon e^{j\phi}$, $\phi$ from $-\pi/2$ to $\pi/2$. There $K P(s)$ is close to $(K c/\varepsilon) e^{-j\phi}$ with $c > 0$, a large arc through the positive real axis, which does not meet the ray $(-\infty, -1]$. On the imaginary axis the curve can meet the negative real axis only at a frequency where $\arg P(j\omega) = -\pi$ modulo $2\pi$. Every such $\omega > 0$ satisfies $\omega \ge \omega_u$, because $\omega_u$ is the smallest one, and the same holds for $-\omega$ by symmetry. By the monotone gain, $K |P(j\omega)| \le K |P(j\omega_u)| = K/K_u < 1$. So the curve meets the negative real axis only to the right of $-1$. A closed curve that does not meet the ray $(-\infty, -1]$ has the winding number 0 about $-1$. $\square$

A product of at least one real lag $1/(s + p)$ with $p > 0$, perhaps with one integrator $1/s$, an all-pass factor $(1 - s/z)/(1 + s/z)$ and a delay, has a strictly decreasing $|P(j\omega)|$. So the claim holds for the plants that the method was made for. For a plant with a resonance the gain is not monotone and the claim can fail. The tests show for random products of 3 to 5 real lags that the closed loop has a root in the right half plane at $K = 1.1 K_u$. That part is a measurement, not a theorem of this page.

## Claim 3: lines L1 to L3 find $\omega_u$

*Assume that between neighbours of the log grid the phase of the rational part changes by less than $\pi$, and that the continuous phase $\varphi(\omega)$ does not go below $-\pi$ and back between two neighbours. Then the scan finds the first interval $[\omega_{i-1}, \omega_i]$ that contains $\omega_u$, and the bisection converges to $\omega_u$.*

*Proof.* As $\omega \to 0^+$, $P(j\omega)$ is close to $c (j\omega)^{-m}$, with $c = n_0/d_0$ the ratio of the lowest nonzero coefficients and $m$ the number of net poles at the origin. For $c > 0$ the phase starts at $-m\pi/2$; for $c < 0$ the code stops with an error, because the controller then needs the reverse action. The phase of the rational part is known modulo $2\pi$ at each grid point. Line L1 adds the wrapped difference $\operatorname{wrap}(\arg_i - \arg_{i-1}) \in (-\pi, \pi]$ to the running phase. Under the first assumption this wrapped difference is the true change of the continuous phase, so by induction $\varphi_i$ is the continuous phase at $\omega_i$. The delay adds $-\omega\theta$ exactly. Line L2 takes the first $i$ with $\varphi_i \le -\pi$. Then $\varphi_{i-1} > -\pi \ge \varphi_i$. Under the second assumption no crossing lies below $\omega_{i-1}$, so $\omega_u \in (\omega_{i-1}, \omega_i]$. On this interval the function $g(\omega) = \varphi(\omega) + \pi$ is continuous, because the rational part has no pole on the imaginary axis away from the origin (a pole there would give an infinite gain). The code computes $g$ from the phase at $\omega_{i-1}$ plus a wrapped difference, which is right by the first assumption. Line L3 keeps $g(a) > 0 \ge g(b)$, and each step halves $b - a$, so $a$ and $b$ converge to a zero of $g$ in the bracket. A zero of $g$ in the bracket is $\omega_u$ when $\varphi$ is decreasing there; this holds for the plants of Claim 2, where each lag and the delay decrease the phase. $\square$

With 4000 grid points from $10^{-6}$ to $10^3$ rad/s, neighbours differ by the factor $10^{9/4000} = 1.0052$. A real lag changes its phase by at most $0.0026$ rad over such a step, and a delay $\theta$ by $0.0052\, \omega \theta$. The assumptions hold with a large margin unless the delay is long compared with $10^3/\omega_u$ or the plant has lightly damped poles.

## Claim 4: the tangent fit has an error of order $\Delta t^2$

*Let $y$ be four times continuously differentiable with a single inflection point $t^*$, where $y'(t^*) = R > 0$ is the largest slope and $y''(t^*) = 0$, $y'''(t^*) < 0$. Sample $y$ with the step $\Delta t$. Then lines L6 and L7 give $R$ and the apparent delay $L = t^* - (y(t^*) - y(0))/R$ with errors $O(\Delta t^2)$.*

*Proof.* The central difference $D_j = (y_{j+1} - y_{j-1})/(2\Delta t)$ equals $y'(t_j) + O(\Delta t^2)$. Line L6 takes the $j$ with the largest $D_j$. Near $t^*$, $y'(t) = R + \frac12 y'''(t^*) (t - t^*)^2 + O(|t - t^*|^3)$, so the chosen $t_j$ satisfies $|t_j - t^*| \le \Delta t/2 + O(\Delta t^2)$, and $D_j = R + O(\Delta t^2)$. For line L7 let $\ell(t) = t - (y(t) - y(0))/y'(t)$, the time where the tangent at $t$ crosses $y(0)$. Its derivative is

$$\ell'(t) = 1 - \frac{y'(t)^2 - (y(t) - y(0)) y''(t)}{y'(t)^2} = \frac{(y(t) - y(0)) y''(t)}{y'(t)^2},$$

which is 0 at $t^*$. So $\ell(t_j) = \ell(t^*) + O(\Delta t^2)$. Line L7 computes $\ell(t_j)$ with $D_j$ in place of $y'(t_j)$, which adds a further $O(\Delta t^2)$. $\square$

For $P(s) = 1/(s + 1)^3$ and a unit step, $y(t) = 1 - e^{-t}(1 + t + t^2/2)$ and $y'(t) = \frac12 t^2 e^{-t}$. The slope is largest at $t^* = 2$, so $R = 2 e^{-2} = 0.270671$. With $y(2) = 1 - 5 e^{-2}$ the apparent delay is $L = 2 - (e^2 - 5)/2 = (9 - e^2)/2 = 0.805472$, and $a = R L = 9 e^{-2} - 1 = 0.218018$. With $\Delta t = 0.01$ the code gives $L = 0.805462$, an error of $10^{-5}$, as the claim predicts.

## Claim 5: the cost

*The ultimate point search costs $O(g\, n)$ operations for $g$ grid points and a plant of degree $n$, plus $O(n)$ per bisection step. The tangent fit costs $O(k)$ for $k$ samples.*

*Proof.* Each grid point needs two Horner evaluations of degree at most $n$ and a fixed number of other operations. The bisection stops after at most 200 steps, and in practice after about 50, when $b - a \le 10^{-15} b$. Line L6 visits each sample once and line L7 is a fixed number of operations. $\square$
