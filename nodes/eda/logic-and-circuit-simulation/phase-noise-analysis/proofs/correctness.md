---
title: The perturbation projection vector exists, is computed by the adjoint recurrence, and gives the phase diffusion constant
proves: [correctness]
status: full
---

We use the notation of the page. The oscillator is $\dot x = F(x) + B\,\xi(t)$ with $n$ states, $F$ twice continuously differentiable with Jacobian $A(x) = \partial F/\partial x$, a constant $n \times p$ matrix $B$, and $p$ independent white noises with $\mathbb E\,\xi(t)\xi(s)^{\mathsf T} = I\,\delta(t - s)$. The noiseless system has a periodic orbit $x_s(t)$ of period $T$ with $\dot x_s(t) \ne 0$. Put $A(t) = A(x_s(t))$, which has period $T$, and let $\Phi(t)$ be the solution of $\dot\Phi = A(t)\Phi$, $\Phi(0) = I$. The monodromy matrix is $M = \Phi(T)$. We assume that the orbit is asymptotically stable in the sense of Floquet theory: the eigenvalue 1 of $M$ is simple and every other eigenvalue has magnitude less than 1.

## The continuous perturbation projection vector

**Lemma 1.** $\dot x_s(t) = \Phi(t)\dot x_s(0)$. In particular $M\dot x_s(0) = \dot x_s(0)$, so 1 is an eigenvalue of $M$ with right eigenvector $\dot x_s(0)$.

*Proof.* Differentiate $\dot x_s = F(x_s)$ with respect to $t$: $\frac{d}{dt}\dot x_s = A(t)\dot x_s$. So $\dot x_s$ solves the variational equation, and the solution with value $\dot x_s(0)$ at $t = 0$ is $\Phi(t)\dot x_s(0)$. At $t = T$, periodicity gives $\dot x_s(T) = \dot x_s(0)$. $\square$

**Lemma 2.** If $\dot y = A(t) y$ and $\dot w = -A(t)^{\mathsf T} w$, then $w(t)^{\mathsf T} y(t)$ does not depend on $t$.

*Proof.* $\frac{d}{dt}(w^{\mathsf T} y) = -w^{\mathsf T} A y + w^{\mathsf T} A y = 0$. $\square$

**Theorem 1 (the PPV).** There is exactly one $T$-periodic solution $v(t)$ of the adjoint equation $\dot v = -A(t)^{\mathsf T} v$ with $v(0)^{\mathsf T}\dot x_s(0) = 1$. It satisfies $v(t)^{\mathsf T}\dot x_s(t) = 1$ for all $t$, and $v(0)$ is the left eigenvector of $M$ for the eigenvalue 1.

*Proof.* Every solution of the adjoint equation is $w(t) = \Phi(t)^{-\mathsf T} w(0)$, because $\frac{d}{dt}\Phi^{-\mathsf T} = -\Phi^{-\mathsf T}\dot\Phi^{\mathsf T}\Phi^{-\mathsf T} = -A^{\mathsf T}\Phi^{-\mathsf T}$. Since the eigenvalue 1 of $M$ is simple, its left and right eigenvectors $\ell$ and $\dot x_s(0)$ satisfy $\ell^{\mathsf T}\dot x_s(0) \ne 0$ (otherwise $\ell$ would be orthogonal to the whole range of $M - I$ and to $\dot x_s(0)$, which together span $\mathbb R^n$ when the eigenvalue is simple). Scale $\ell$ so that $\ell^{\mathsf T}\dot x_s(0) = 1$ and put $v(t) = \Phi(t)^{-\mathsf T}\ell$. Then $v(T) = M^{-\mathsf T}\ell = \ell$ because $M^{\mathsf T}\ell = \ell$. The function $t \mapsto v(t + T)$ solves the same adjoint equation, because $A$ has period $T$, and it has the value $v(T) = v(0)$ at $t = 0$; by uniqueness it equals $v$, so $v$ has period $T$. By Lemmas 1 and 2, $v(t)^{\mathsf T}\dot x_s(t) = v(0)^{\mathsf T}\dot x_s(0) = 1$.

For uniqueness, a $T$-periodic adjoint solution $w$ has $w(0) = w(T) = M^{-\mathsf T}w(0)$, so $M^{\mathsf T}w(0) = w(0)$ and $w(0)$ is a multiple of $\ell$. The normalization fixes the multiple. $\square$

## The discrete PPV of the implementation

The implementation replaces the flow by $S$ steps of a one-step method $\psi$ with step $h = T/S$ (the classical Runge-Kutta method). Line L1 returns a closed orbit of the map: $x_{k+1} = \psi(x_k)$ for $k = 0, \ldots, S - 1$ and $x_S = x_0$. Put $P_k = \psi'(x_k)$, the exact Jacobian of the step that the implementation forms by differentiating the four stages, and $M_h = P_{S-1}\cdots P_0$.

**Theorem 2 (discrete adjoint).** Let $v_S$ be any vector and $v_k = P_k^{\mathsf T} v_{k+1}$ for $k = S - 1, \ldots, 0$ (line L4). Then for every sequence with $y_{k+1} = P_k y_k$, $v_k^{\mathsf T} y_k = v_S^{\mathsf T} y_S$ for every $k$. If $M_h^{\mathsf T} v_S = v_S$, then $v_0 = v_S$.

*Proof.* $v_k^{\mathsf T} y_k = v_{k+1}^{\mathsf T} P_k y_k = v_{k+1}^{\mathsf T} y_{k+1}$; apply this from $k$ to $S - 1$. Also $v_0 = (P_{S-1}\cdots P_0)^{\mathsf T} v_S = M_h^{\mathsf T} v_S$. $\square$

So $v_k^{\mathsf T} d$ is the exact component, measured by $v_S$, that a small kick $d$ at step $k$ leaves at the end of the period: this is the discrete form of Lemma 2. The discrete map is not a flow, so 1 is an eigenvalue of $M_h$ only up to the step error, and $\psi(x_k) - x_k$ is not exactly an eigenvector. Line L3 therefore solves the bordered system $(M_h^{\mathsf T} - I)v_S + \mu F(x_0) = 0$, $F(x_0)^{\mathsf T} v_S = 1$, whose solution has $\mu = 0$ when the eigenvalue is exactly 1. The size of $\mu$, and so the error in $v_0 = v_S - \mu F(x_0)$ and in $v_k^{\mathsf T}F(x_k) = 1$, is measured on the page, not proved; it falls with the step error of the method.

## The phase of the linearized noise is a random walk

**Theorem 3.** Let $y$ solve the linearized noise equation $dy = A(t)\,y\,dt + B\,dW$ with $y(0) = 0$, where $W$ is a standard $p$-dimensional Wiener process. Then $\alpha(t) = v(t)^{\mathsf T} y(t)$ is a Gaussian process with mean 0 and

$$\operatorname{Var}\alpha(t) = c\,t + \beta(t), \qquad c = \frac1T\int_0^T v(s)^{\mathsf T} B B^{\mathsf T} v(s)\,ds,$$

where $\beta$ has period $T$ and $|\beta(t)| \le T\max_s v(s)^{\mathsf T}BB^{\mathsf T}v(s)$. The increments of $\alpha$ over disjoint intervals are independent.

*Proof.* $v$ is deterministic and continuously differentiable, so the Itô product rule has no correction term: $d\alpha = \dot v^{\mathsf T} y\,dt + v^{\mathsf T}(A y\,dt + B\,dW) = v^{\mathsf T} B\,dW$, because $\dot v^{\mathsf T} = -v^{\mathsf T} A$. Hence $\alpha(t) = \int_0^t v(s)^{\mathsf T} B\,dW(s)$, a Wiener integral of a deterministic function: it is Gaussian with mean 0, its increments over disjoint intervals are independent, and by the Itô isometry $\operatorname{Var}\alpha(t) = \int_0^t g(s)\,ds$ with $g = v^{\mathsf T}BB^{\mathsf T}v \ge 0$. The function $g$ has period $T$ and mean $c$, so $\beta(t) = \int_0^t (g(s) - c)\,ds$ has period $T$, and on one period it lies between $-cT$ and $T\max g$. $\square$

Line L5 computes $c$ by the rectangle rule on the $S$ samples of one period. For a smooth periodic integrand this rule converges faster than any power of $h$, so its error is far below the error in $v_k$.

**Corollary 1 (the Hopf oscillator).** For $F(a, b) = (\mu a - \omega b - r^2 a,\ \omega a + \mu b - r^2 b)$ with $r^2 = a^2 + b^2$, $\mu > 0$, and $B = \sigma I$, the orbit is $x_s(t) = \sqrt\mu(\cos\omega t, \sin\omega t)$, $v(t) = (-\sin\omega t, \cos\omega t)/(\omega\sqrt\mu)$, and $c = \sigma^2/(\mu\omega^2)$.

*Proof.* In polar form the system is $\dot r = r(\mu - r^2)$, $\dot\vartheta = \omega$, so the circle $r = \sqrt\mu$ is an orbit of period $2\pi/\omega$ with $\dot x_s = \omega\sqrt\mu(-\sin\omega t, \cos\omega t)$. The given $v$ has $v^{\mathsf T}\dot x_s = 1$. On the orbit, $A(t) = \begin{pmatrix} -2\mu\cos^2 & -\omega - 2\mu\cos\sin \\ \omega - 2\mu\cos\sin & -2\mu\sin^2 \end{pmatrix}$ with argument $\omega t$, and a direct product gives $A^{\mathsf T}(-\sin, \cos) = \omega(\cos, \sin)$, so $-A^{\mathsf T}v = -(\cos, \sin)/\sqrt\mu$. Differentiation gives $\dot v = \omega(-\cos, -\sin)/(\omega\sqrt\mu) = -(\cos, \sin)/\sqrt\mu$, the same vector. So $v$ solves the adjoint equation, and it is periodic, so it is the PPV by Theorem 1. Then $v^{\mathsf T}BB^{\mathsf T}v = \sigma^2|v|^2 = \sigma^2/(\omega^2\mu)$, a constant, which is $c$. $\square$

## From the phase diffusion to the Lorentzian

**Proposition 1.** Let $\alpha$ be a Wiener process with $\operatorname{Var}\alpha(t) = ct$ and $f_0 = 1/T$. The stationary spectral density of $e^{j2\pi f_0(t + \alpha(t))}$ is

$$S(f) = \frac{f_0^2 c}{\pi^2 f_0^4 c^2 + (f - f_0)^2},$$

and $\int_{-\infty}^{\infty} S(f)\,df = 1$.

*Proof.* Put $\omega_0 = 2\pi f_0$. The increment $\alpha(t + \tau) - \alpha(t)$ is Gaussian with variance $c|\tau|$, so the autocorrelation is $\mathbb E\big[e^{j\omega_0(t + \tau + \alpha(t+\tau))}e^{-j\omega_0(t + \alpha(t))}\big] = e^{j\omega_0\tau}e^{-\omega_0^2 c|\tau|/2}$, which does not depend on $t$. With $a = \omega_0^2 c/2 = 2\pi^2 f_0^2 c$, the Fourier transform of $e^{-a|\tau|}$ is $2a/(a^2 + 4\pi^2 f_m^2)$ at $f_m = f - f_0$, which is $4\pi^2 f_0^2 c/(4\pi^4 f_0^4c^2 + 4\pi^2 f_m^2) = S(f)$. For the integral, put $b = \pi f_0^2 c$, so that $S = f_0^2 c/(b^2 + f_m^2)$. Since $\int_{-\infty}^{\infty} df_m/(b^2 + f_m^2) = \pi/b$, the integral is $f_0^2 c\,\pi/(\pi f_0^2 c) = 1$. $\square$

Line L6 reports $10\log_{10} S(f_0 + f_m)$, the density at offset $f_m$ relative to the power of the first harmonic, in dBc/Hz.

## What is not proved

- The step from the linearized equation of Theorem 3 to the nonlinear oscillator: that the noisy solution is $x_s(t + \alpha(t))$ plus a deviation that stays small, and that the nonlinear phase $\alpha(t)$ is asymptotically a Wiener process with the same $c$. This is the main theorem of Demir, Mehrotra and Roychowdhury (2000), and we cite it. The Monte Carlo runs on the page measure it for two oscillators; they do not prove it.
- That line L1 converges: it is Newton's method on the shooting equations with the period as an unknown, and its convergence near a stable orbit with a nonsingular bordered matrix follows from the local theorem for [Newton's method for systems](/newton-method-for-systems/); the starting point is a matter of practice.
- The size of $\mu$ in line L3 and the error of the discrete PPV, which are measured.
- The near-sinusoidal estimate $c \approx kT/(R C^2 A^2\omega_0^2)$ for the LC oscillator, which is an approximation and is compared, not proved.
