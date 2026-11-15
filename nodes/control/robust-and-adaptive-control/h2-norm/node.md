---
tag: V16R0N
kind: definition
slug: h2-norm
name: H2 norm
aliases:
- H2 norm of a system
area: control/robust-and-adaptive-control
level: core
summary: "For A Hurwitz and D = 0, the root of the frequency integral of trace(G^H G) over 2 pi. It equals the L2 norm of the impulse response, and its square is trace(C W_c C^T)."
prereqs: [transfer-function, controllability-gramian, observability-gramian]
see_also: [h-infinity-norm, h2-optimal-control, lqg-control, lyapunov-equation, parseval-theorem, impulse-response, kalman-filter, hankel-singular-values]
sources:
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 4, Performance Specifications (the H2 norm, its time domain form and its computation from the gramians)
  - paper: "John C. Doyle, Keith Glover, Pramod P. Khargonekar and Bruce A. Francis, State-space solutions to standard H2 and H-infinity control problems, IEEE Transactions on Automatic Control 34(8), 831-847, 1989"
    locator: the H2 norm in state-space form and the H2 optimal control problem
---

The H2 norm of a strictly proper linear system with all its poles in the open left half plane is the square root of the energy of its impulse response, summed over all inputs and outputs. By Parseval's theorem it is also the root mean square of the frequency response over all frequencies, and it is the root mean square of the output when the input is white noise of unit intensity. For a state-space model it comes from one [Lyapunov equation](/lyapunov-equation/): its square is $\operatorname{trace}(C W_c C^T)$, with $W_c$ the [controllability gramian](/controllability-gramian/). It measures average gain, while the [H-infinity norm](/h-infinity-norm/) measures worst case gain.

## Definition

**Notation.** The system is $x' = A x + B u$, $y = C x + D u$ with $x \in \mathbb{R}^n$, $u \in \mathbb{R}^m$ and $y \in \mathbb{R}^p$. Its [transfer function](/transfer-function/) is $G(s) = C (sI - A)^{-1} B + D$, and its [impulse response](/impulse-response/) is $g(t) = C e^{At} B$ for $t > 0$ (plus $D\,\delta(t)$). $G^H$ is the conjugate transpose, and $\|M\|_F^2 = \operatorname{trace}(M^H M)$ is the squared Frobenius norm.

**The space H2.** $H_2$ is the set of $p \times m$ matrix functions $G(s)$ that are analytic in the open right half plane and have

$$\|G\|_2^2 = \sup_{\sigma > 0} \frac{1}{2\pi} \int_{-\infty}^{\infty} \|G(\sigma + j\omega)\|_F^2\, d\omega < \infty .$$

For a rational $G$ that is analytic in the closed right half plane, the supremum is reached on the imaginary axis, and

$$\|G\|_2 = \left( \frac{1}{2\pi} \int_{-\infty}^{\infty} \operatorname{trace}\bigl(G(j\omega)^H G(j\omega)\bigr)\, d\omega \right)^{1/2}.$$

A real rational $G$ is in $H_2$ if and only if it is strictly proper and has no poles in the closed right half plane. For a state-space model with $A$ [Hurwitz](/hurwitz-matrix/), this means $D = 0$. If $D \ne 0$, the integrand tends to $\|D\|_F^2 > 0$ and the norm is infinite.

**Time domain form.** By [Parseval's theorem](/parseval-theorem/), for $A$ Hurwitz and $D = 0$,

$$\|G\|_2^2 = \int_0^\infty \operatorname{trace}\bigl(g(t)^T g(t)\bigr)\, dt = \sum_{i=1}^m \int_0^\infty |g(t) e_i|^2\, dt ,$$

where $g(t) e_i$ is the output for a unit impulse at input $i$ and zero initial state. So $\|G\|_2^2$ is the total output energy of the $m$ impulse responses.

**Gramian form.** Let $A$ be Hurwitz and $D = 0$. The controllability gramian solves $A W_c + W_c A^T + B B^T = 0$, and the [observability gramian](/observability-gramian/) solves $A^T W_o + W_o A + C^T C = 0$. Then

$$\|G\|_2^2 = \operatorname{trace}(C W_c C^T) = \operatorname{trace}(B^T W_o B).$$

Proof: $\operatorname{trace}(g^T g) = \operatorname{trace}(g g^T)$ and $W_c = \int_0^\infty e^{At} B B^T e^{A^T t} dt$, so $\int_0^\infty \operatorname{trace}(g g^T) dt = \operatorname{trace}(C W_c C^T)$. The second form uses $W_o = \int_0^\infty e^{A^T t} C^T C e^{At} dt$ in the same way. Both need only one $n \times n$ Lyapunov solve, $O(n^3)$ flops with the Bartels-Stewart method, and they do not need a minimal realization.

**Stochastic reading.** Let $u$ be white noise with $E[u(t) u(\tau)^T] = I\,\delta(t - \tau)$, and let $A$ be Hurwitz and $D = 0$. In steady state, the state covariance is $W_c$ and $E[y(t)^T y(t)] = \operatorname{trace}(C W_c C^T) = \|G\|_2^2$. This is why the [Kalman filter](/kalman-filter/), [LQG control](/lqg-control/) and [H2 optimal control](/h2-optimal-control/) all minimize an H2 norm.

**Energy to peak reading.** For $m = p = 1$, the Cauchy-Schwarz inequality gives $|y(t)| \le \|g\|_{L_2} \|u\|_{L_2} = \|G\|_2 \|u\|_{L_2}$ for zero initial state, and the input $u(\tau) = g(t - \tau)$ on $[0, t]$ reaches the bound as $t \to \infty$. So for one input and one output, the H2 norm is the gain from input energy ($L_2$ norm) to output peak ($L_\infty$ norm). For more channels this gain is $\lambda_{\max}(C W_c C^T)^{1/2}$, which is in general smaller than $\|G\|_2$.

**Properties.**

- It is a norm on $H_2$. It is not an induced norm from $L_2$ to $L_2$, and it is not submultiplicative. The bound $\|G H\|_2 \le \|G\|_\infty \|H\|_2$ holds, with the H-infinity norm on one factor.
- It does not depend on the realization: a change of state coordinates $x = T \bar x$ turns $W_c$ into $T^{-1} W_c T^{-T}$ and $C$ into $C T$, and the trace is the same.
- No general inequality holds between $\|G\|_2$ and $\|G\|_\infty$ in either direction: the example $a/(s + a)$ below has $\|G\|_\infty = 1$ for every $a > 0$, while $\|G\|_2 = \sqrt{a/2}$.

**Discrete time.** For $G(z) = C (zI - A)^{-1} B + D$ with $A$ Schur, the impulse response is $g_0 = D$ and $g_k = C A^{k-1} B$ for $k \ge 1$, and

$$\|G\|_2^2 = \frac{1}{2\pi} \int_{-\pi}^{\pi} \operatorname{trace}\bigl(G(e^{j\theta})^H G(e^{j\theta})\bigr)\, d\theta = \sum_{k \ge 0} \operatorname{trace}(g_k^T g_k) = \operatorname{trace}(C W C^T + D D^T),$$

where $W$ solves the Stein equation $A W A^T - W + B B^T = 0$. Here $D \ne 0$ is allowed.

## Examples and non-examples

- **First order, the check value.** $G(s) = 1/(s + 1)$, with $A = -1$, $B = C = 1$, $D = 0$. The gramian is $W_c = 1/2$, so $\|G\|_2 = 1/\sqrt 2 = 0.70711$. The same value comes from $\int_0^\infty e^{-2t} dt = 1/2$ and from $\frac{1}{2\pi} \int d\omega / (1 + \omega^2) = 1/2$. The H-infinity norm is 1.
- **Lightly damped mode, the check value.** $G(s) = 1/(s^2 + 0.2 s + 1)$, with $A = \begin{bmatrix} 0 & 1 \\ -1 & -0.2 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $C = \begin{bmatrix} 1 & 0 \end{bmatrix}$. The gramians are $W_c = 2.5\, I$ and $W_o = \begin{bmatrix} 2.6 & 0.5 \\ 0.5 & 2.5 \end{bmatrix}$, so $\operatorname{trace}(C W_c C^T) = \operatorname{trace}(B^T W_o B) = 2.5$ and $\|G\|_2 = \sqrt{2.5} = 1.58114$. For $\omega_n^2/(s^2 + 2\zeta\omega_n s + \omega_n^2)$ the general value is $\|G\|_2^2 = \omega_n/(4\zeta)$. The H-infinity norm is $5.02519$, more than three times larger, because the peak is narrow.
- **Two inputs and two outputs.** $G(s) = \operatorname{diag}(1/(s + 1), 1/(s + 2))$. The squares add over the channels: $\|G\|_2^2 = 1/2 + 1/4 = 3/4$, so $\|G\|_2 = 0.86603$. The H-infinity norm is the larger channel peak, 1.
- **Wide bandwidth.** $G(s) = a/(s + a)$ with $a > 0$: $W_c = 1/(2a)$ and $\|G\|_2^2 = a^2/(2a) = a/2$. For $a = 10$, $\|G\|_2 = \sqrt 5 = 2.23607$ while $\|G\|_\infty = 1$. The H2 norm grows with the bandwidth because it adds the gain over all frequencies.
- **Discrete time.** $G(z) = 1/(z - 0.5)$: $g_k = 0.5^{k-1}$ for $k \ge 1$, so $\|G\|_2^2 = \sum_{k \ge 0} 0.25^k = 4/3$. The Stein equation $0.25 W - W + 1 = 0$ gives the same $W = 4/3$, and $\|G\|_2 = 1.15470$.
- **Non-example: a direct feedthrough.** $G(s) = (s + 2)/(s + 1) = 1 + 1/(s + 1)$ has $D = 1$. The integrand tends to 1 at high frequency, so the integral diverges and $G \notin H_2$. Its H-infinity norm is finite (it is 2, at $\omega = 0$).
- **Non-example: an unstable pole.** $G(s) = 1/(s - 1)$. The integral $\frac{1}{2\pi} \int d\omega/(1 + \omega^2) = 1/2$ is finite, so $G$ has a finite $L_2$ norm on the imaginary axis, but $G$ has a pole in the right half plane and is not in $H_2$. The causal impulse response $e^t$ has infinite energy. The Lyapunov equation $2 W + 1 = 0$ has the solution $W = -1/2$, which is not a gramian, and the trace formula does not apply.

## Related definitions

- [H-infinity norm](/h-infinity-norm/): the peak over frequency of the largest singular value, the worst case $L_2$ gain. It is an induced norm and is submultiplicative; the H2 norm is neither.
- [Controllability gramian](/controllability-gramian/) and [observability gramian](/observability-gramian/): the two matrices that give the H2 norm by a trace. The [Lyapunov equation](/lyapunov-equation/) page gives the methods to compute them.
- [H2 optimal control](/h2-optimal-control/) and [LQG control](/lqg-control/): the controller design problems that minimize the H2 norm of a closed-loop transfer function.
- [Impulse response](/impulse-response/) and [Parseval's theorem](/parseval-theorem/): the link between the time domain and the frequency domain forms.
- [Hankel singular values](/hankel-singular-values/): also built from the two gramians, from the eigenvalues of $W_c W_o$ instead of a trace.

## References
