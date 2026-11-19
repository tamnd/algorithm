---
title: Correctness of the phase vocoder
proves: [correctness]
status: full
---

The phase vocoder has no exact specification for a general sound, so we prove what it does exactly: the frequency estimate is exact for a complex exponential, equal hops give back the input, and a complex exponential is stretched with no change of frequency or amplitude.

## Setup

The window $w$ has length $N$. Frame $t$ of the analysis is $X_t[k] = \sum_{m=0}^{N-1} w[m]\, x[t H_a + m]\, e^{-i \omega_k m}$ with $\omega_k = 2\pi k / N$. The function $\text{princarg}(a) = a - 2\pi \lfloor (a + \pi) / (2\pi) \rfloor$ returns the unique value in $[-\pi, \pi)$ that differs from $a$ by an integer multiple of $2\pi$. Write $\varphi_t[k] = \arg X_t[k]$. The algorithm sets $\psi_0 = \varphi_0$ and, for $t \ge 1$,

$$\omega'_t[k] = \omega_k + \frac{1}{H_a} \text{princarg}\big(\varphi_t[k] - \varphi_{t-1}[k] - H_a \omega_k\big), \qquad \psi_t[k] = \psi_{t-1}[k] + H_s\, \omega'_t[k],$$

and output frame $t$ is $f_t = \text{IFFT}(Y_t)$ with $Y_t[k] = |X_t[k]|\, e^{i \psi_t[k]}$. The output is $y[n] = \sum_t w[n - t H_s] f_t[n - t H_s] / S(n)$ with $S(n) = \sum_t w[n - t H_s]^2$, at every $n$ with $S(n) > 0$ (terms with the index outside $0 .. N - 1$ are 0).

## Lemma 1 (the overlap-add inverts windowed frames)

If $f_t[m] = w[m]\, z[t H + m]$ for all $t$ and $m$, for some signal $z$, then the weighted overlap-add at hop $H$ returns $z[n]$ at every $n$ with $S(n) > 0$.

*Proof.* $\sum_t w[n - tH] f_t[n - tH] = \sum_t w[n - tH]^2 z[n] = S(n) z[n]$. Divide by $S(n)$. $\square$

## Theorem 1 (exact frequency for one exponential)

Let $x[n] = c\, e^{i \omega n}$ with $c \ne 0$, and let $k$ be a bin with $X_0[k] \ne 0$ and $|\omega - \omega_k| H_a < \pi$. Then $\omega'_t[k] = \omega$ for every $t \ge 1$.

*Proof.* Substituting $x$,

$$X_t[k] = c\, e^{i \omega t H_a} \sum_m w[m]\, e^{i(\omega - \omega_k) m} = e^{i \omega t H_a} X_0[k].$$

So $X_t[k] \ne 0$ and $\varphi_t[k] - \varphi_{t-1}[k] = \omega H_a + 2\pi j$ for some integer $j$. The argument of princarg is $(\omega - \omega_k) H_a + 2\pi j$. The value $(\omega - \omega_k) H_a$ is in $(-\pi, \pi)$ and differs from it by a multiple of $2\pi$, so princarg returns it. Then $\omega'_t[k] = \omega_k + (\omega - \omega_k) = \omega$. $\square$

## Theorem 2 (identity for equal hops)

If $H_s = H_a$, then $Y_t = X_t$ for every $t$, and $y[n] = x[n]$ at every $n$ with $S(n) > 0$.

*Proof.* We show $\psi_t[k] - \varphi_t[k] \in 2\pi\mathbb{Z}$ by induction on $t$. It holds for $t = 0$. For $t \ge 1$, princarg changes its argument by a multiple of $2\pi$, so

$$\psi_t[k] = \psi_{t-1}[k] + H_a \omega_k + \big(\varphi_t[k] - \varphi_{t-1}[k] - H_a \omega_k\big) + 2\pi j = \varphi_t[k] + (\psi_{t-1}[k] - \varphi_{t-1}[k]) + 2\pi j,$$

which is $\varphi_t[k]$ plus a multiple of $2\pi$ by the hypothesis. Hence $Y_t[k] = |X_t[k]| e^{i \varphi_t[k]} = X_t[k]$ (for $X_t[k] = 0$ both sides are 0). The IFFT inverts the FFT, so $f_t[m] = w[m]\, x[t H_a + m]$, and Lemma 1 with $H = H_a$ gives $y = x$ where $S > 0$. $\square$

## Theorem 3 (a complex exponential is stretched exactly)

Let $x[n] = c\, e^{i \omega n}$, and suppose every bin $k$ with $X_0[k] \ne 0$ satisfies $|\omega - \omega_k| H_a < \pi$. Then for any $H_s$, $y[n] = c\, e^{i \omega n}$ at every $n$ with $S(n) > 0$.

*Proof.* Take a bin with $X_0[k] \ne 0$. By Theorem 1, $\psi_t[k] = \varphi_0[k] + t H_s \omega$, and $|X_t[k]| = |X_0[k]|$ by the formula in its proof. So $Y_t[k] = |X_0[k]| e^{i\varphi_0[k]} e^{i \omega t H_s} = e^{i \omega t H_s} X_0[k]$. For a bin with $X_0[k] = 0$, also $X_t[k] = 0$ and $Y_t[k] = 0 = e^{i \omega t H_s} X_0[k]$. Hence $Y_t = e^{i \omega t H_s} X_0$ and

$$f_t[m] = e^{i \omega t H_s} w[m]\, c\, e^{i \omega m} = w[m]\, c\, e^{i \omega (t H_s + m)},$$

which is the windowed frame of the signal $z[n] = c\, e^{i \omega n}$ at hop $H_s$. Lemma 1 gives $y = z$ where $S > 0$. $\square$

For example, with the periodic Hann window and $\omega = \omega_j$ on a bin center, $X_0[k] \ne 0$ only for $k = j - 1, j, j + 1$, and the condition holds whenever $H_a < N / 2$.

## Remarks

**Real signals.** For a real input, $X_t[N - k] = \overline{X_t[k]}$. Since $H_a \omega_{N-k} = 2\pi H_a - H_a \omega_k$ and $\text{princarg}(-a) = -\text{princarg}(a)$ except when $a$ is an odd multiple of $\pi$, the updates give $\psi_t[N - k] = -\psi_t[k]$ modulo $2\pi$ outside that case, so $Y_t$ is conjugate symmetric and $f_t$ is real. The code takes the real part, which only removes rounding.

**Real sinusoids.** A real sinusoid is the sum of two exponentials, at $\omega$ and $-\omega$. Their sum in a bin is not of the form of Theorem 1, so the estimate is only close, with an error that falls as the window rejects the other exponential better. The tests measure 440.0000 Hz for a 440 Hz sine at $N = 1024$.

**The tests.** The tests check Theorem 1 for complex exponentials at several frequencies, Theorem 2 on random noise (error below $10^{-10}$) and Lemma 1 directly.
