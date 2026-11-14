---
title: Harmonic balance is collocation, exact for linear circuits, with the Toeplitz Jacobian
proves: [correctness]
status: full
---

We use the notation of the page. The circuit is $f(x) + \frac{d}{dt} q(x) = u(t)$ with $N$ unknowns, $f$ and $q$ continuously differentiable, and $u$ periodic with period $T = 2\pi/\omega$. Fix $K \ge 0$, put $M = 2K + 1$, $\theta_i = 2\pi i/M$ and $t_i = \theta_i/\omega$ for $i = 0, \ldots, M - 1$. For samples $y_0, \ldots, y_{M-1}$ (scalars or vectors) the discrete Fourier transform is

$$\mathcal F_k(y) = \frac{1}{M} \sum_{i=0}^{M-1} y_i\, e^{-jk\theta_i}, \qquad k = -K, \ldots, K.$$

A spectrum is $X = (X_{-K}, \ldots, X_K)$ with $X_k \in \mathbb C^N$, and $p_X(t) = \sum_{|k| \le K} X_k e^{jk\omega t}$ is its trigonometric polynomial. Its samples are $x_i = p_X(t_i)$. The harmonic balance (HB) equations are

$$R_k(X) = \mathcal F_k\big(f(x_i)\big) + jk\omega\, \mathcal F_k\big(q(x_i)\big) - \mathcal F_k\big(u(t_i)\big) = 0, \qquad |k| \le K. \tag{1}$$

## Interpolation and collocation

**Lemma 1 (orthogonality).** $\sum_{i=0}^{M-1} e^{jd\theta_i} = M$ if $d \equiv 0 \pmod M$ and $0$ otherwise. For $|k|, |l| \le K$, $k \equiv l \pmod M$ holds only if $k = l$.

*Proof.* The sum is a geometric series with ratio $e^{2\pi j d/M}$, which is 1 exactly when $M$ divides $d$; otherwise the sum is $(1 - e^{2\pi j d})/(1 - e^{2\pi j d/M}) = 0$. If $|k|, |l| \le K$ then $|k - l| \le 2K < M$, so $M \mid k - l$ forces $k = l$. $\square$

**Lemma 2 (the transform is exact on degree K).** For every spectrum $X$, $\mathcal F_k(p_X(t_i)) = X_k$ for $|k| \le K$. Hence the map from spectra to samples is a bijection, and every set of samples has exactly one trigonometric polynomial of degree at most $K$ through it, the interpolant $I_K y$ with coefficients $\mathcal F_k(y)$.

*Proof.* $\mathcal F_k(p_X(t_i)) = \sum_l X_l \frac{1}{M}\sum_i e^{j(l-k)\theta_i} = X_k$ by Lemma 1. So the linear map $X \mapsto (x_i)$ has a left inverse; both spaces have dimension $MN$ over $\mathbb C$, so it is a bijection with inverse $\mathcal F$. $\square$

**Theorem 1 (HB is collocation).** $X$ solves (1) if and only if, at every sample time,

$$f(x_i) + \frac{d}{dt}\big[I_K\, q(x)\big](t_i) = \big[I_K u\big](t_i), \qquad i = 0, \ldots, M - 1,$$

where $I_K q(x)$ is the interpolant of the samples $q(x_0), \ldots, q(x_{M-1})$.

*Proof.* The derivative of $I_K q(x) = \sum_k Q_k e^{jk\omega t}$ has coefficients $jk\omega Q_k$, so the left side minus the right side is the trigonometric polynomial with coefficients $R_k(X)$, evaluated at $t_i$. By Lemma 2 its samples are all zero exactly when all its coefficients are zero. $\square$

So HB asks that the circuit equations hold exactly at $M$ equally spaced times, with the time derivative taken spectrally. The samples of $f(x)$ and $q(x)$ contain harmonics above $K$ in general; Lemma 1 shows that the transform folds harmonic $k + M$ onto $k$. This aliasing is part of the method as it is defined here.

**Lemma 3 (real waveforms).** Call $X$ symmetric if $X_{-k} = \overline{X_k}$ for every $k$. If $X$ is symmetric, its samples are real, $R(X)$ is symmetric, and the Newton step (2) below is symmetric when it exists.

*Proof.* For symmetric $X$, the terms $k$ and $-k$ of $p_X(t_i)$ are conjugate, so $x_i$ is real. The transform of real samples satisfies $\mathcal F_{-k}(y) = \overline{\mathcal F_k(y)}$, and $j(-k)\omega = \overline{jk\omega}$, so $R_{-k} = \overline{R_k}$. For the step, Theorem 2 gives $J_{-k,-l} = \overline{J_{k,l}}$ because $\hat G$ and $\hat C$ below are transforms of real samples. If $J\Delta = -R$, then $\Delta'_k = \overline{\Delta_{-k}}$ satisfies $J\Delta' = -R$ as well, so by uniqueness $\Delta' = \Delta$. $\square$

## The Newton step

**Theorem 2 (the Jacobian).** Let $G_i = \partial f/\partial x$ and $C_i = \partial q/\partial x$ at $x_i$, and for $d = 0, \ldots, M - 1$ put $\hat G_d = \frac{1}{M}\sum_i G_i e^{-jd\theta_i}$ and $\hat C_d = \frac1M \sum_i C_i e^{-jd\theta_i}$. For a symmetric $X$ and a symmetric direction $D$,

$$\frac{d}{d\varepsilon} R_k(X + \varepsilon D)\Big|_{\varepsilon = 0} = \sum_{|l| \le K} \big(\hat G_{(k - l) \bmod M} + jk\omega\, \hat C_{(k-l) \bmod M}\big) D_l. \tag{2}$$

*Proof.* The samples of $X + \varepsilon D$ are $x_i + \varepsilon \delta_i$ with $\delta_i = \sum_l D_l e^{jl\theta_i}$, which is real by Lemma 3. By the chain rule, $\frac{d}{d\varepsilon} f(x_i + \varepsilon\delta_i) = G_i \delta_i$, so

$$\frac{d}{d\varepsilon}\mathcal F_k\big(f\big) = \frac1M \sum_i G_i \sum_l D_l e^{jl\theta_i} e^{-jk\theta_i} = \sum_l \Big(\frac1M\sum_i G_i e^{-j(k-l)\theta_i}\Big) D_l,$$

and $e^{-jd\theta_i}$ depends only on $d \bmod M$. The $q$ term is the same with $C_i$ and the factor $jk\omega$; the source term does not depend on $X$. $\square$

The matrix in (2) is block Toeplitz in $(k, l)$, plus the diagonal factor $jk\omega$ on the $C$ part. It is the matrix of line L7. In matrix form it is $\Gamma\,(\operatorname{diag}(G_i) + \mathcal D\operatorname{diag}(C_i))\,\Gamma^{-1}$, where $\Gamma$ is the transform and $\mathcal D = \Gamma^{-1} \operatorname{diag}(jk\omega)\Gamma$ is the spectral differentiation matrix on the samples. So the HB Newton step is the transform of the Newton step for the collocation equations of Theorem 1, and the two iterations produce the same waveforms. When the Jacobian is nonsingular at a root and $f$ and $q$ are twice continuously differentiable, the full-step iteration converges quadratically from a start close enough to the root, by the local theorem for [Newton's method for systems](/newton-method-for-systems/).

## Linear circuits

**Theorem 3 (exact for linear circuits).** Let $f(x) = Gx$ and $q(x) = Cx$ with constant matrices, let $u$ contain only harmonics $|k| \le K$, with coefficients $U_k$, and let $G + jk\omega C$ be nonsingular for every integer $k$. Then:

1. The HB equations have the unique solution $X_k = (G + jk\omega C)^{-1} U_k$.
2. These are the Fourier coefficients of the unique periodic steady state of the circuit, which has no harmonics above $K$.
3. Newton's method reaches the solution in one full step from any start.

*Proof.* By Lemma 2, $\mathcal F_k(G x_i) = G X_k$, $\mathcal F_k(C x_i) = C X_k$ and $\mathcal F_k(u(t_i)) = U_k$. So $R_k(X) = (G + jk\omega C) X_k - U_k$, which proves 1. For 2, let $x(t)$ be a periodic solution with Fourier coefficients $\xi_k$ for all integers $k$. The Fourier coefficients of $\frac{d}{dt}(Cx)$ are $jk\omega C\xi_k$ for periodic $Cx$, so taking coefficients of the equation gives $(G + jk\omega C)\xi_k = U_k$ for every $k$, with $U_k = 0$ for $|k| > K$. Nonsingularity gives $\xi_k = 0$ there and $\xi_k = X_k$ for $|k| \le K$. Conversely $p_X$ is a solution, so it is the unique one. For 3, $R$ is affine in $X$, so its Jacobian is constant and one Newton step from any $X$ lands on the root. $\square$

**Corollary (K = 0).** With $M = 1$ the only sample is $t_0 = 0$ and (1) reads $f(X_0) = u(0)$. For constant sources these are the equations of the [DC operating point](/dc-operating-point-analysis/).

## What is not proved

- **Truncation error for nonlinear circuits.** For a nonlinear $f$ or $q$ the steady state has infinitely many harmonics, and HB with $K$ harmonics is an approximation. How fast the error falls with $K$ depends on how smooth the waveforms are; for analytic waveforms the Fourier coefficients fall geometrically. The page measures the error against a transient reference for two circuits; it is not proved here.
- **Existence and uniqueness** of a periodic steady state of a nonlinear circuit, and the nonsingularity of the Jacobian at the root, are assumed.
- **Global convergence.** The step limit of line L8 is a heuristic. Newton's method can fail from a poor start, and continuation in the source amplitude is the usual remedy.
- **Iterative solvers.** Krylov methods such as GMRES with a block-diagonal preconditioner solve (2) approximately; their convergence is not covered.
