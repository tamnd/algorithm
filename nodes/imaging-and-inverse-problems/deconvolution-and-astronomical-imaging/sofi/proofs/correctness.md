---
title: The SOFI cumulant removes the background and the white noise and keeps the n-th power of the PSF of each independent emitter
proves: [correctness]
status: full
---

**Setting.** The intensity at pixel $r$ and frame $t$ is

$$F(r, t) = b(r) + \sum_{k} \varepsilon_k\, U(r - r_k)\, s_k(t) + N(r, t),$$

with a constant background $b$, emitters at $r_k$ with brightness $\varepsilon_k$, a PSF $U$, blinking processes $s_k$ and noise $N$. The model assumptions are: the processes $s_1, s_2, \ldots$ and $N$ are mutually independent and stationary, and the noise values at different frames are independent (white in time). For the lags $\tau_1, \ldots, \tau_n$, the SOFI value of order $n$ is the joint cumulant

$$C_n(r) = \kappa\bigl(F(r, t + \tau_1), \ldots, F(r, t + \tau_n)\bigr).$$

The joint cumulant of $X_1, \ldots, X_n$ is $\kappa = \sum_\pi (-1)^{|\pi| - 1}(|\pi| - 1)! \prod_{B \in \pi} \mathbb E\bigl[\prod_{q \in B} X_q\bigr]$, summed over the partitions $\pi$ of $\{1, \ldots, n\}$. Equivalently, it is the coefficient of $t_1 \cdots t_n$ in the cumulant generating function $K(t) = \log \mathbb E\, e^{\sum_q t_q X_q}$, when this function exists, as it does for bounded variables. The code computes the cumulant of the *empirical* law, which puts the mass $1/L$ on each of the $L$ vectors $(X_1(t), \ldots, X_n(t))$ in the window. All the algebraic claims below hold for any law, so they hold exactly for the empirical one too.

**Claim 1 (moment formulas).** For $n = 2, 3, 4$ the code's formulas on the centered series equal the partition formula: $\kappa_2 = \mathbb E[ab]$, $\kappa_3 = \mathbb E[abc]$, $\kappa_4 = \mathbb E[abcd] - \mathbb E[ab]\mathbb E[cd] - \mathbb E[ac]\mathbb E[bd] - \mathbb E[ad]\mathbb E[bc]$.

*Proof.* By Claim 2, adding constants does not change $\kappa$ for $n \ge 2$, so we may center. For centered variables every partition with a block of one element contributes $0$. For $n = 2, 3$ only the partition with one block is left. For $n = 4$ the one block gives $\mathbb E[abcd]$ and the three partitions into two pairs have the coefficient $(-1)^1 1! = -1$. $\square$

The test checks the identity in exact rational arithmetic against a direct sum over all partitions.

**Claim 2 (constants and scaling).** For $n \ge 2$, $\kappa(X_1 + c_1, \ldots, X_n + c_n) = \kappa(X_1, \ldots, X_n)$, and $\kappa(a_1 X_1, \ldots, a_n X_n) = a_1 \cdots a_n\, \kappa(X_1, \ldots, X_n)$.

*Proof.* $K$ of the shifted variables is $K(t) + \sum_q c_q t_q$, which has no term in $t_1 \cdots t_n$ when $n \ge 2$. Scaling $X_q$ by $a_q$ replaces $t_q$ by $a_q t_q$ in $K$. $\square$

**Claim 3 (independent sums).** If $X_q = Y_q + Z_q$ and the families $(Y_q)$ and $(Z_q)$ are independent, then $\kappa(X) = \kappa(Y) + \kappa(Z)$.

*Proof.* By independence, $\mathbb E\, e^{\sum t_q (Y_q + Z_q)} = \mathbb E\, e^{\sum t_q Y_q}\, \mathbb E\, e^{\sum t_q Z_q}$, so the cumulant generating functions add. $\square$

**Claim 4 (independent groups).** If $\{1, \ldots, n\}$ splits into two nonempty groups $A$ and $B$ such that $(X_q)_{q \in A}$ is independent of $(X_q)_{q \in B}$, then $\kappa(X_1, \ldots, X_n) = 0$.

*Proof.* $K(t)$ is then the sum of a function of $(t_q)_{q \in A}$ and a function of $(t_q)_{q \in B}$, and neither has a term with all of $t_1, \ldots, t_n$. $\square$

**Claim 5 (the SOFI formula).** Under the model assumptions, if the lags are distinct,

$$C_n(r) = \sum_k \varepsilon_k^n\, U(r - r_k)^n\, \kappa_n[s_k](\tau), \qquad \kappa_n[s_k](\tau) = \kappa\bigl(s_k(t + \tau_1), \ldots, s_k(t + \tau_n)\bigr).$$

*Proof.* The background is a constant, which Claim 2 removes. The emitters and the noise are independent, so by Claim 3 the cumulant is the sum of one cumulant per emitter and one for the noise. The noise values at the $n$ distinct frames are independent, so by Claim 4 the noise cumulant is $0$. For emitter $k$, Claim 2 with $a_q = \varepsilon_k U(r - r_k)$ gives the factor $\varepsilon_k^n U(r - r_k)^n$. $\square$

With equal lags, the noise cumulant is the $n$-th cumulant of the noise at one frame, for example its variance $\sigma^2$ when $n = 2$. The test measures this bias for $n = 2$ and checks that the lag $1$ removes it.

**Claim 6 (single emitter, exact).** For one emitter and a constant background, the empirical SOFI image is exactly $\varepsilon^n U(r - r_1)^n$ times the empirical cumulant of the lagged blinking series, for any lags, at every pixel.

*Proof.* Without noise, $F(r, t) = b(r) + \varepsilon U(r - r_1) s(t)$ for every $t$. Apply Claim 2 to the empirical law. $\square$

The test checks this in exact rational arithmetic for $n = 2, 3, 4$.

**Claim 7 (narrowing).** If $U(r) = e^{-|r|^2/(2\sigma^2)}$, then $U^n(r) = e^{-|r|^2/(2\sigma^2/n)}$, a Gaussian of width $\sigma/\sqrt n$. For any PSF whose OTF vanishes outside a disk of radius $k_c$, the Fourier transform of $U^n$ vanishes outside the disk of radius $n k_c$.

*Proof.* The first part is algebra. The Fourier transform of $U^n$ is the $n$-fold convolution of the OTF with itself, whose support lies in the $n$-fold sum of the disk, the disk of radius $n k_c$. $\square$

So the $\sqrt n$ narrowing is a statement about a Gaussian PSF. For another PSF, $U^n$ is narrower too, but by a different factor, and the support of its spectrum grows by $n$; a later deconvolution can use the larger support.

**Claim 8 (blinking cumulants).** For a stationary two-state process with $P(\text{off} \to \text{on}) = a$, $P(\text{on} \to \text{off}) = b$ and the on fraction $\rho = a/(a + b)$:

- with all lags equal, $\kappa_2 = \rho(1 - \rho)$, $\kappa_3 = \rho(1 - \rho)(1 - 2\rho)$ and $\kappa_4 = \rho(1 - \rho)(1 - 6\rho(1 - \rho))$, the cumulants of a Bernoulli law;
- with the lags $0$ and $1$, $\kappa_2 = \rho(1 - \rho)(1 - a - b)$.

*Proof.* At one time $s$ is Bernoulli with mean $\rho$. Since $s^j = s$, all raw moments are $\rho$, and the centered moments are $\mu_2 = \rho(1 - \rho)$, $\mu_3 = \rho(1 - \rho)(1 - 2\rho)$ and $\mu_4 = \rho(1 - \rho)(1 - 3\rho + 3\rho^2)$. Claim 1 gives $\kappa_4 = \mu_4 - 3\mu_2^2 = \rho(1 - \rho)(1 - 3\rho(1 - \rho) - 3\rho(1 - \rho))$. For the lag $1$, $\mathbb E[s(t)s(t + 1)] = \rho(1 - b)$, so $\kappa_2 = \rho(1 - b) - \rho^2 = \rho(1 - b - \rho)$, and $(a + b)(1 - b) - a = b(1 - a - b)$ gives $1 - b - \rho = (1 - \rho)(1 - a - b)$. $\square$

So $\kappa_4 < 0$ when $\rho(1 - \rho) > 1/6$, that is for $0.211 < \rho < 0.789$: the fourth order image can change sign between emitters with different on fractions. The test checks the Bernoulli values exactly for $\rho = 3/10$, where they are $0.21$, $0.084$ and $-0.0546$.

**Remark (estimation).** The claims about $C_n$ are about the cumulant of the process. The code computes the cumulant of the empirical law of a finite window, which is a biased but consistent estimate for ergodic blinking and noise: the cross terms between emitters and the noise terms are $0$ only in the limit of long movies. This is the role of the measurement tests with long series. $\blacksquare$
