---
title: The Zheng-Xiao simulator has the autocorrelation of Clarke's model for every M, and its fourth moment depends on how the phases are drawn
proves: [correctness]
status: full
---

Write $w = 2\pi f_D$, $x = w\tau$, $\alpha_n = (2\pi n - \pi + \theta)/(4M)$ and $\Phi_n(t) = w t \cos\alpha_n + \phi_n$, where $\theta$, $\psi_1, \ldots, \psi_M$ and the phases are independent and uniform on $[-\pi, \pi)$. In the per-sinusoid form the $\phi_n$ are independent; in the common form $\phi_n = \phi$ for all $n$. The output is

$$h(t) = \sqrt{2\Omega/M}\, S(t), \qquad S(t) = \sum_{n=1}^{M} e^{j\psi_n} \cos\Phi_n(t),$$

so that $X_c = \operatorname{Re} S$ and $X_s = \operatorname{Im} S$.

**Lemma 1 (phase averages).** For a uniform $\psi$, $E e^{j\psi} = E e^{2j\psi} = 0$, $E\cos^2\psi = E\sin^2\psi = \frac12$ and $E \cos\psi \sin\psi = 0$. For a uniform $\phi$ and constants $A, B$, $E[\cos(A + \phi)\cos(B + \phi)] = \frac12 \cos(A - B)$, $E\cos^2\phi = \frac12$ and $E\cos^4\phi = \frac38$.

*Proof.* Each is the average of a trigonometric polynomial over a full period: write $\cos(A+\phi)\cos(B+\phi) = \frac12[\cos(A - B) + \cos(A + B + 2\phi)]$ and $\cos^4\phi = \frac38 + \frac12\cos 2\phi + \frac18 \cos 4\phi$, and drop the terms with a nonzero multiple of the variable. $\square$

**Lemma 2 (the angle average).** For every real $x$, $\frac1M\sum_{n=1}^{M} E_\theta \cos(x\cos\alpha_n) = J_0(x)$.

*Proof.* As $\theta$ runs uniformly over $[-\pi, \pi)$, $\alpha_n$ runs uniformly over $I_n = [(n-1)\pi/(2M), n\pi/(2M))$ with density $2M/\pi$. The intervals $I_1, \ldots, I_M$ are disjoint and their union is $[0, \pi/2)$. So the left side is $\frac1M \cdot \frac{2M}{\pi} \int_0^{\pi/2} \cos(x\cos\alpha)\, d\alpha = \frac{2}{\pi}\int_0^{\pi/2}\cos(x\cos\alpha)\, d\alpha$. Bessel's integral is $J_0(x) = \frac1\pi \int_0^\pi \cos(x\cos\alpha)\, d\alpha$, and the substitution $\alpha \to \pi - \alpha$ shows that the halves $[0, \pi/2]$ and $[\pi/2, \pi]$ give equal parts. $\square$

**Theorem 1 (second order).** In both forms, for all $t$ and $\tau$,

$$E[X_c(t+\tau)X_c(t)] = E[X_s(t+\tau)X_s(t)] = \tfrac{M}{4} J_0(x), \qquad E[X_c(t+\tau)X_s(t)] = 0,$$

so $E[h(t+\tau)\overline{h(t)}] = \Omega J_0(x)$, and each quadrature of $h$ has autocorrelation $\frac\Omega2 J_0(x)$.

*Proof.* $E[X_c(t+\tau)X_c(t)] = \sum_{n,m} E[\cos\psi_n\cos\psi_m]\, E[\cos\Phi_n(t+\tau)\cos\Phi_m(t)]$, because the $\psi$ are independent of $\theta$ and of the phases. For $n \ne m$, $E[\cos\psi_n\cos\psi_m] = (E\cos\psi)^2 = 0$. For $n = m$, Lemma 1 gives $\frac12$ for the first factor, and, conditional on $\theta$, $\frac12\cos(w\tau\cos\alpha_n)$ for the second one, in both forms, because only $\phi_n$ enters it. So the sum is $\frac14\sum_n E_\theta\cos(x\cos\alpha_n) = \frac M4 J_0(x)$ by Lemma 2. The same steps with $\sin\psi$ give $X_s$, and with $\cos\psi_n\sin\psi_n$ give the cross-correlation $0$. Then $E[S(t+\tau)\overline{S(t)}] = E[X_cX_c] + E[X_sX_s] + j(E[X_sX_c] - E[X_cX_s]) = \frac M2 J_0(x)$, and the factor $2\Omega/M$ gives $\Omega J_0(x)$. $\square$

The result does not depend on $t$, so both forms are wide-sense stationary, and it holds for every $M \ge 1$.

**Theorem 2 (fourth moment, a phase per sinusoid).** $E|h(t)|^4 = \Omega^2 (2 - \frac{1}{2M})$ for every $t$, and $h(t)$ tends in distribution to a circular complex Gaussian with variance $\Omega$ as $M \to \infty$.

*Proof.* Condition on $\theta$. The terms $Z_n = e^{j\psi_n}\cos\Phi_n(t)$ are then independent, with $E Z_n = 0$, $E Z_n^2 = 0$ (by $E e^{2j\psi} = 0$) and $E|Z_n|^2 = \frac12$, $E|Z_n|^4 = \frac38$ (by Lemma 1, since $\Phi_n(t)$ is uniform modulo $2\pi$). Expand $E|S|^4 = \sum_{a,b,c,d} E[Z_a \overline{Z_b} Z_c \overline{Z_d}]$. A term is nonzero only if no index appears once; the pairings $a = b \ne c = d$ and $a = d \ne b = c$ each give $E|Z_a|^2E|Z_c|^2 = \frac14$, the pairing $a = c \ne b = d$ gives $E Z_a^2\, \overline{E Z_b^2} = 0$, and $a = b = c = d$ gives $\frac38$. So $E|S|^4 = \frac38 M + 2\cdot\frac14 M(M-1) = \frac{M^2}{2} - \frac{M}{8}$, which does not depend on $\theta$. Multiply by $(2\Omega/M)^2$. For the limit, given $\theta$ the real and imaginary parts are sums of independent bounded terms with total covariance $\frac M4 I$, so the Lyapunov form of the central limit theorem applies to $S/\sqrt M$, and the limit does not depend on $\theta$. $\square$

A circular complex Gaussian $h$ with $E|h|^2 = \Omega$ has $E|h|^4 = 2\Omega^2$, so the excess $-\Omega^2/(2M)$ measures the distance from Rayleigh fading.

**Theorem 3 (fourth moment, the common phase at $t = 0$).** $E|h(0)|^4 = \Omega^2(3 - \frac{3}{2M})$.

*Proof.* At $t = 0$, $\Phi_n(0) = \phi$ for all $n$, so $S(0) = \cos\phi \cdot U$ with $U = \sum_n e^{j\psi_n}$, and $\phi$ is independent of $U$. By the same pairing count with $E|e^{j\psi}|^2 = E|e^{j\psi}|^4 = 1$, $E|U|^4 = M + 2M(M-1) = 2M^2 - M$. With $E\cos^4\phi = \frac38$, $E|S(0)|^4 = \frac38(2M^2 - M)$, and the factor $(2\Omega/M)^2$ gives the claim. $\square$

So the common form has $E|h(0)|^4 \to 3\Omega^2$, not $2\Omega^2$, as $M \to \infty$: $h(0)$ is a Gaussian-like variable times the independent factor $\sqrt 2\cos\phi$, and is not Gaussian for any $M$. For $t \ne 0$ the Doppler terms $wt\cos\alpha_n$ differ between sinusoids and spread the phases, so the fourth moment changes with $t$. This is the defect that Xiao, Zheng and Beaulieu (2006) remove by using one phase per sinusoid. For $M = 8$, Theorems 2 and 3 give 1.9375 and 2.8125.
