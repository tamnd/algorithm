---
title: The Griffin-Lim distance never increases
proves: [correctness]
status: full
---

The setting is that of the algorithm: a window $w$ of length $N$, a hop $R$, the frames $m$ with starts $s_m = mR$ and $-N < s_m < L$, target magnitudes $A_m[k] \ge 0$, and $W[n] = \sum_m w[n - s_m]^2 > 0$ for $0 \le n \le L - 1$. Arrays of spectra $Z = (Z_m[k])$ have the norm $\|Z\|^2 = \sum_m \sum_k |Z_m[k]|^2$. Arithmetic is exact, as in the real RAM. For a real signal $x$ of length $L$ (with $x[i] = 0$ outside $0 \le i \le L - 1$), $S(x)$ is its STFT.

**Lemma 1 (the magnitude step).** For an array $X$, let $P(X)_m[k] = A_m[k]\, X_m[k] / |X_m[k]|$, and $P(X)_m[k] = A_m[k]$ when $X_m[k] = 0$, as in line L5. Then $\|X - P(X)\| \le \|X - Y\|$ for every array $Y$ with $|Y_m[k]| = A_m[k]$ for all $m, k$, and $\|X - P(X)\|^2 = \sum_{m,k} (|X_m[k]| - A_m[k])^2$.

*Proof.* The norm is a sum over the entries, so it is enough to look at one entry. For complex numbers $z$ and $y$ with $|y| = a$, the triangle inequality gives $|z - y| \ge \bigl||z| - |y|\bigr| = \bigl||z| - a\bigr|$. If $z \ne 0$, the number $a z/|z|$ lies on the ray of $z$, so $|z - a z / |z|| = \bigl||z| - a\bigr|$, which is the lower bound. If $z = 0$, every $y$ with $|y| = a$ has $|z - y| = a = \bigl||z| - a\bigr|$. $\square$

**Lemma 2 (the least squares step).** For an array $Y$, the signal $x^\ast = \mathrm{LSEE}(Y)$ of lines L8 to L12 satisfies $\|S(x^\ast) - Y\| \le \|S(x) - Y\|$ for every real signal $x$ of length $L$.

*Proof.* Let $y_m$ be the inverse DFT of $Y_m$, as in line L10. The DFT of length $N$ multiplies squared norms by $N$ (Parseval's identity for the unnormalized DFT), so

$$\|S(x) - Y\|^2 = N \sum_m \sum_{j=0}^{N-1} \bigl|x[s_m + j]\, w[j] - y_m[j]\bigr|^2.$$

Split each term into real and imaginary parts; $x$ and $w$ are real, so the imaginary part $(\operatorname{Im} y_m[j])^2$ does not depend on $x$. Terms with $s_m + j$ outside $[0, L - 1]$ have $x[s_m + j] = 0$ and do not depend on $x$ either. Group the remaining terms by $n = s_m + j$:

$$\|S(x) - Y\|^2 = N \sum_{n=0}^{L-1} \sum_m \bigl(x[n]\, w[n - s_m] - \operatorname{Re} y_m[n - s_m]\bigr)^2 + \text{const},$$

where the inner sum runs over the frames with $0 \le n - s_m \le N - 1$. Each inner sum is a quadratic in the single number $x[n]$ with leading coefficient $W[n] > 0$, so it has its unique minimum at

$$x[n] = \frac{\sum_m w[n - s_m]\, \operatorname{Re} y_m[n - s_m]}{W[n]},$$

which is what lines L11 and L12 compute: num$[n]$ is the numerator and den$[n] = W[n]$. The minima for different $n$ are independent, so $x^\ast$ minimizes the whole sum. $\square$

**Theorem.** Let $x_t$ be the signal after iteration $t$ of the loop of line L3 ($x_0$ is the signal of line L2), $X_t = S(x_t)$, and $D_t = \sum_{m,k} (|(X_t)_m[k]| - A_m[k])^2$. Then $D_{t+1} \le D_t$ for every $t \ge 0$.

*Proof.* By lines L4 to L6, $x_{t+1} = \mathrm{LSEE}(P(X_t))$. By Lemma 1, $D_t = \|X_t - P(X_t)\|^2$ and $D_{t+1} = \|X_{t+1} - P(X_{t+1})\|^2$. Then

$$\|X_{t+1} - P(X_{t+1})\| \le \|X_{t+1} - P(X_t)\| \le \|X_t - P(X_t)\|.$$

The first inequality is Lemma 1 applied to $X_{t+1}$ with $Y = P(X_t)$, which has the magnitudes $A$. The second is Lemma 2 applied to $Y = P(X_t)$ and the real signal $x = x_t$, because $X_{t+1} = S(\mathrm{LSEE}(P(X_t)))$. Squaring gives $D_{t+1} \le D_t$. $\blacksquare$

**Corollary.** The sequence $D_t$ converges, because it does not increase and $D_t \ge 0$.

**What is not proved.** The limit of $D_t$ need not be the minimum of $D$ over all signals, and the signals $x_t$ need not converge to a minimizer. The set of arrays with magnitudes $A$ is not convex, so the argument for convex sets, which would give convergence to a point of the intersection, does not apply. Both $x$ and $-x$ have the same distance, so even a global minimum is not unique. The example on the page with a random signal of length 64 stops at a relative error near 0.2 while a signal with $D = 0$ exists.

**Floating point.** Lemma 1 and Lemma 2 hold up to rounding, so a computed $D_t$ can rise by a few units of the rounding error. The tests allow an increase of $10^{-12}$ times $\sum A^2$.
