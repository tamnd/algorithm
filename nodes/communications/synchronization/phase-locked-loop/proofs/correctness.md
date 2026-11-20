---
title: The second-order digital PLL follows phase and frequency steps with zero steady-state error, and its phase error variance is B_L T / SNR in the linear model
proves: [correctness]
status: full
---

The input is $r_k = e^{j\theta_k} + w_k$ with $w_k \sim \mathcal{CN}(0, N_0)$ independent, $E_s = 1$ and $\mathrm{SNR} = E_s/N_0 = 1/N_0$. Write $\phi_k$ for the estimate recorded in line L3 at step $k$, $e_k$ for the detector output of line L4 and $s_k$ for the integrator after line L5. Lines L5 and L6 give

$$s_k = s_{k-1} + K_i e_k, \qquad \phi_{k+1} = \phi_k + K_p e_k + s_k, \qquad s_{-1} = 0,\ \phi_0 = \phi_{\text{start}}. \tag{1}$$

We work in exact real arithmetic, as in the real RAM.

**Lemma 1 (the phase detector).** $e_k = \sin(\theta_k - \phi_k) + n_k$, where $n_k = \operatorname{Im}(w_k e^{-j\phi_k})$. Given the past, $n_k$ is Gaussian with mean $0$ and variance $N_0/2$, and the $n_k$ are independent.

*Proof.* $r_k e^{-j\phi_k} = e^{j(\theta_k - \phi_k)} + w_k e^{-j\phi_k}$, and the imaginary part of the first term is $\sin(\theta_k - \phi_k)$. The phase $\phi_k$ depends only on $w_0, \ldots, w_{k-1}$. A circular Gaussian variable keeps its law under a rotation, so $w_k e^{-j\phi_k} \sim \mathcal{CN}(0, N_0)$ given the past, and its imaginary part has variance $N_0/2$. $\square$

So the detector gain is $K_d = 1$: near lock, $e_k \approx (\theta_k - \phi_k) + n_k$. The *linear model* replaces $\sin x$ by $x$. It is exact in the limit of small errors, and the tests check it with a step of $10^{-4}$ rad.

**Lemma 2 (the closed loop).** In the linear model, with $Z$-transforms $\Theta(z)$, $\Phi(z)$ and $N(z)$,

$$\Phi(z) = H(z)\,\bigl(\Theta(z) + N(z)\bigr), \qquad H(z) = \frac{(K_p + K_i) z - K_p}{z^2 + (K_p + K_i - 2) z + (1 - K_p)}.$$

*Proof.* With $e_k = \theta_k + n_k - \phi_k$, (1) gives the loop filter $F(z) = K_p + K_i/(1 - z^{-1})$ from $e$ to $\phi_{k+1} - \phi_k$, so $(z - 1)\Phi(z) = F(z) E(z)$. The open loop is $G(z) = F(z)/(z - 1) = ((K_p + K_i) z - K_p)/(z - 1)^2$, and $\Phi = G(\Theta + N - \Phi)$ gives $\Phi = \frac{G}{1 + G}(\Theta + N)$. Multiply the numerator and the denominator by $(z - 1)^2$: $(z-1)^2 + (K_p + K_i) z - K_p = z^2 + (K_p + K_i - 2) z + 1 - K_p$. $\square$

**Lemma 3 (stability).** Both poles of $H$ lie inside the unit circle if and only if $0 < K_p < 2$, $K_i > 0$ and $2K_p + K_i < 4$.

*Proof.* By the Jury test, the roots of $z^2 + a_1 z + a_2$ lie inside the unit circle if and only if $|a_2| < 1$, $1 + a_1 + a_2 > 0$ and $1 - a_1 + a_2 > 0$. Here $a_2 = 1 - K_p$, $1 + a_1 + a_2 = K_i$ and $1 - a_1 + a_2 = 4 - 2K_p - K_i$. $\square$

**Theorem 1 (zero steady-state error).** Assume the gains satisfy Lemma 3, there is no noise and the linear model holds. If the input phase is $\theta_k = \theta_0 + \omega k$ for $k \ge 0$ (a phase step together with a frequency step), then $\theta_k - \phi_k \to 0$.

*Proof.* The error is $E(z) = (1 - H(z))\Theta(z)$ with $1 - H(z) = (z - 1)^2/D(z)$, where $D$ is the denominator of $H$. The input transform is $\Theta(z) = \theta_0 z/(z - 1) + \omega z/(z - 1)^2$. So $E(z) = (\theta_0 z (z - 1) + \omega z)/D(z)$. All poles of $E$ are the roots of $D$, inside the unit circle, so $e_k$ is a sum of terms $c\,p^k$ and $c\,k\,p^k$ with $|p| < 1$, and it tends to $0$. $\square$

The loop has two integrators, the one of line L5 and the oscillator of line L6. A frequency ramp $\theta_k = \alpha k^2/2$ gives the error $\alpha/K_i$ in the steady state by the same argument.

**Lemma 4 (the noise bandwidth).** Let $h_k$ be the impulse response of $H$ and $B_L T = \frac12 \sum_k h_k^2$. With $b_0 = K_p + K_i$, $b_1 = -K_p$, $a_1 = K_p + K_i - 2$ and $a_2 = 1 - K_p$,

$$2 B_L T = \frac{(b_0^2 + b_1^2)(1 + a_2) - 2 b_0 b_1 a_1}{(1 - a_2)\bigl((1 + a_2)^2 - a_1^2\bigr)}.$$

*Proof.* Feed $H$ with white noise $x_k$ of unit variance. The output $y_k$ is stationary, $y_k + a_1 y_{k-1} + a_2 y_{k-2} = b_0 x_{k-1} + b_1 x_{k-2}$, and $r_0 = E[y_k^2] = \sum h_k^2$. Let $r_m = E[y_k y_{k-m}]$. Since $E[y_k x_{k-m}] = h_m$ with $h_0 = 0$, $h_1 = b_0$ and $h_2 = b_1 - a_1 b_0$, multiplying the recursion by $y_k$, $y_{k-1}$ and $y_{k-2}$ and taking means gives

$$r_0 + a_1 r_1 + a_2 r_2 = b_0 h_1 + b_1 h_2, \quad a_1 r_0 + (1 + a_2) r_1 = b_0 b_1, \quad a_2 r_0 + a_1 r_1 + r_2 = 0.$$

Eliminate $r_2$ with the third equation and $r_1$ with the second; the result is the formula. The tests compare it with $\frac12 \sum h_k^2$ from 20000 terms of the impulse response. $\square$

**Theorem 2 (phase error variance in the linear model).** With a constant $\theta$, stable gains and the linear model, the phase error $\theta - \phi_k$ has mean $0$ and variance $\frac{N_0}{2} \cdot 2 B_L T = B_L T/\mathrm{SNR}$ in the steady state.

*Proof.* By Lemma 2, $\phi_k - \theta$ tends to the response of $H$ to $n_k$ plus a transient that decays. By Lemma 1 the $n_k$ are white with variance $N_0/2$, so the variance of the output is $\frac{N_0}{2} \sum h_k^2 = N_0 B_L T$. $\square$

The design rule of `loop_gains` is the analog formula $\omega_n T = 2 B_L T/(\zeta + 1/(4\zeta))$, $K_p = 2\zeta\omega_n T$ and $K_i = (\omega_n T)^2$. It is not exact for the digital loop: for $B_L T = 0.02$ and $\zeta = 1/\sqrt2$, Lemma 4 gives $0.020738$. The tests check the design within 5 percent for $B_L T \le 0.02$, and they check Theorem 2 by simulation at an SNR of 10 dB within a factor of 1.25.
