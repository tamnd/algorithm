---
title: Overlap-add inverts the STFT under the COLA condition
proves: [correctness]
status: full
---

We write $x[i] = 0$ for $i < 0$ and $i \ge L$, and $w[j] = 0$ for $j < 0$ and $j \ge N$. The hop is $1 \le R \le N$. The DFT of line L5 and the inverse DFT of line L9 are exact, as in the real RAM.

**Lemma (the frames).** Line L2 lists exactly the integers $m$ with $-N < mR < L$. For every $n$ with $0 \le n \le L - 1$ and every integer $m$ with $w[n - mR] \ne 0$, the index $m$ is in that list.

*Proof.* The integers $m$ with $mR < L$ are those with $m \le \lfloor (L - 1)/R \rfloor$, because $mR \le L - 1$. The integers with $mR > -N$ are those with $mR \ge -(N - 1)$, that is $m \ge -\lfloor (N - 1)/R \rfloor$. So line L2 runs over exactly these $m$. If $w[n - mR] \ne 0$, then $0 \le n - mR \le N - 1$, so $mR \le n \le L - 1$ and $mR \ge n - N + 1 \ge -(N - 1)$. $\square$

**Lemma (one frame).** For the frame with start $s = mR$, the vector $v$ of line L9 is $v[j] = x[s + j]\, w[j]$ for $0 \le j \le N - 1$.

*Proof.* Line L5 stores $X = \mathrm{DFT}_N(u)$ with $u[j] = x[s + j]\, w[j]$ from line L4. The inverse DFT with the factor $1/N$ gives $\mathrm{IDFT}_N(\mathrm{DFT}_N(u)) = u$. $\square$

**Theorem (OLA).** If $\sum_{m \in \mathbb{Z}} w[n - mR] = C$ for all $n$ with $C \ne 0$, then ISTFT-OLA$(\mathrm{STFT}(x, w, R), L, C)$ returns $x$.

*Proof.* Fix $n$ with $0 \le n \le L - 1$. Line L11 adds $v[j]/C$ to $y[n]$ for each frame with $s + j = n$ and $0 \le j \le N - 1$, and for no other pair. By the second lemma this term is $x[n]\, w[n - s]/C$. So after the loop

$$y[n] = \frac{x[n]}{C} \sum_{m \in M} w[n - mR],$$

where $M$ is the list of line L2. A frame with $0 \le n - mR \le N - 1$ but outside $M$ does not exist by the first lemma, and a frame in $M$ with $n - mR$ outside $[0, N - 1]$ adds nothing because then $w[n - mR] = 0$ and line L11 does not touch $y[n]$. So the sum over $M$ equals the sum over all integers $m$, which is $C$ by the hypothesis, and $y[n] = x[n]$. $\blacksquare$

**Theorem (WOLA).** Let $D[n] = \sum_{m \in \mathbb{Z}} w[n - mR]^2$ and suppose $D[n] > 0$ for $0 \le n \le L - 1$. If line L11 adds $w[j]\, v[j]$ instead of $v[j]/C$, and each $y[n]$ is divided by $D[n]$ at the end, the result is $x$.

*Proof.* As in the OLA theorem, $y[n] = \sum_{m} w[n - mR]\, x[n]\, w[n - mR] = x[n]\, D[n]$ before the division, so $y[n]/D[n] = x[n]$. $\blacksquare$

**The least squares property.** Let $Y_m$ be arbitrary spectra, one per frame, and $y_m = \mathrm{IDFT}_N(Y_m)$. By Parseval's identity for the DFT, $\sum_m \sum_k |X_m[k] - Y_m[k]|^2 = N \sum_m \sum_j |x[mR + j]\, w[j] - y_m[j]|^2$ for the STFT $X$ of a signal $x$. The right side is a sum of squares that is separate for each $n = mR + j$: it equals $N \sum_n \sum_m |x[n]\, w[n - mR] - y_m[n - mR]|^2$. For a fixed $n$ the minimum over the number $x[n]$ is at $x[n] = \sum_m w[n - mR]\, y_m[n - mR] / D[n]$, which is the WOLA output. For consistent spectra $Y_m = X_m$ it gives back $x$, as the theorem says. This is equation (6) of Griffin and Lim (1984).

**Floating point.** With a floating-point FFT, each $v[j]$ has a rounding error of the order of $\varepsilon \log_2 N$ times the size of the frame, and each output sample adds at most $\lceil N/R \rceil$ such errors. The structure of the proof does not change.
