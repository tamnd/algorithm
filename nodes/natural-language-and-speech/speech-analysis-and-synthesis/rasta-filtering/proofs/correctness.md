---
title: The RASTA recursion is a stable band-pass filter that removes offsets exactly
proves: [correctness]
status: full
---

We work in the real RAM on one band, since lines L1 and L2 only select the bands one at a time and each band is filtered on its own. Fix $0 \le \rho < 1$ and a trajectory $x[0], \ldots, x[T-1]$. Line L2 sets $x[-4] = \cdots = x[-1] = x[0]$ and $y[-1] = 0$. Write $b = (b_0, \ldots, b_4) = 0.1\,(2, 1, 0, -1, -2)$, so line L3 computes $u[t] = \sum_{k=0}^{4} b_k x[t - k]$: the pairs $2(x[t] - x[t-4])$ and $(x[t-1] - x[t-3])$ are just a grouping of the same sum. Line L4 computes $y[t] = u[t] + \rho\, y[t-1]$.

Let $h$ be the impulse response of $H_c(z) = (\sum_k b_k z^{-k}) / (1 - \rho z^{-1})$, the filter of the paper without the factor $z^4$: $h[n] = \sum_{k=0}^{\min(n, 4)} b_k \rho^{\,n-k}$ for $n \ge 0$.

**Lemma 1 (the taps sum to zero).** $\sum_{k=0}^{4} b_k = 0$, so $u[t]$ does not change when the same constant is added to $x[t-4], \ldots, x[t]$.

*Proof.* $0.1(2 + 1 + 0 - 1 - 2) = 0$, and $\sum_k b_k (x[t-k] + a) = u[t] + a \sum_k b_k$. $\square$

**Lemma 2 (the recursion is the filter).** Let $\tilde x[t] = x[t] - x[0]$ for $t \ge 0$ and $\tilde x[t] = 0$ for $t < 0$. Then for every $t \ge 0$,

$$y[t] = \sum_{s=0}^{t} h[s]\, \tilde x[t - s].$$

*Proof.* For $t \ge 0$ the five inputs of $u[t]$ are $x[t-k]$, which equal $\tilde x[t-k] + x[0]$ for every $k$, also for $t - k < 0$ where both sides are $x[0]$. By Lemma 1, $u[t] = \sum_k b_k \tilde x[t-k]$. Unrolling line L4 with $y[-1] = 0$ gives $y[t] = \sum_{i=0}^{t} \rho^{\,i} u[t - i]$. Substitute $u$ and collect the terms with $s = i + k$; since $\tilde x$ is 0 at negative times, $y[t] = \sum_{s=0}^{t} \tilde x[t-s] \sum_{k=0}^{\min(s,4)} b_k \rho^{\,s-k} = \sum_{s} h[s] \tilde x[t - s]$. $\square$

So the output is the zero-state response of $H_c$ to $\tilde x$, and the output of the paper's filter $H = z^4 H_c$ is the same sequence shifted 4 frames earlier.

**Lemma 3 (offsets are removed exactly).** If $x[t] = a$ for all $t$, then $y[t] = 0$ for all $t \ge 0$. If $x'[t] = x[t] + a$ for all $t$, then $y'[t] = y[t]$ for all $t \ge 0$.

*Proof.* In the first case $\tilde x = 0$, and Lemma 2 gives $y = 0$. In the second case $x'[0] = x[0] + a$, so $\tilde x' = \tilde x$, and Lemma 2 gives the same output. $\square$

**Lemma 4 (the impulse and step responses).** $h[0] = 0.2$, $h[1] = 0.1 + 0.2\rho$, $h[2] = \rho\, h[1]$, $h[3] = -0.1 + \rho\, h[2]$, $h[4] = -0.2 + \rho\, h[3]$, and $h[n] = \rho^{\,n-4} h[4]$ for $n \ge 4$. The step response $g[n] = \sum_{s=0}^{n} h[s]$ satisfies $g[n] = \rho^{\,n-3} g[3]$ for $n \ge 3$.

*Proof.* The impulse response satisfies line L4 with $u[n] = b_n$ for $n \le 4$ and $u[n] = 0$ after, which gives the values. For the step, $u[n] = \sum_{k=0}^{\min(n,4)} b_k$, which is 0 for $n \ge 4$ by Lemma 1, so $g[n] = \rho\, g[n-1]$ for $n \ge 4$. $\square$

With $\rho = 0.98$ this gives $h = 0.2, 0.296, 0.29008, 0.18428, -0.01941, \ldots$ and $g[3] = 0.97036$, the values in the example.

**Lemma 5 (stability).** $\sum_{n \ge 0} |h[n]| < \infty$, so a bounded input gives a bounded output: if $|\tilde x[t]| \le K$ for all $t$, then $|y[t]| \le K \sum_n |h[n]|$.

*Proof.* By Lemma 4, $\sum_{n \ge 4} |h[n]| = |h[4]| / (1 - \rho)$, which is finite since $\rho < 1$. The bound follows from Lemma 2 and the triangle inequality. $\square$

**Lemma 6 (the frequency response).** For a frame rate $r$ and a modulation frequency $f$, let $z = e^{j 2\pi f / r}$. Then $|H(z)| = |H_c(z)|$, and $H_c$ is 0 exactly at $f = 0$, at $f = r/2$, and at $f = \frac{r}{2\pi} \arccos(-\frac14)$ in $[0, r/2]$.

*Proof.* $|z^4| = 1$ on the unit circle. The numerator is $0.1\,(2(1 - z^{-4}) + z^{-1}(1 - z^{-2})) = 0.1\,(1 - z^{-2})(2 + z^{-1} + 2 z^{-2})$, using $1 - z^{-4} = (1 - z^{-2})(1 + z^{-2})$. The first factor is 0 at $z = \pm 1$. The second is $z^{-1}(2 z + 2 z^{-1} + 1) = z^{-1}(4 \cos\omega + 1)$ on the unit circle, which is 0 exactly when $\cos \omega = -\frac14$. The denominator $1 - \rho z^{-1}$ is never 0 on the unit circle because $\rho < 1$. $\square$

**Lemma 7 (same on cepstra).** Let $D$ be any fixed $K \times B$ matrix, such as the DCT of MFCC. Filtering every band of $X$ and then applying $D$ to each frame gives the same result as applying $D$ to each frame and then filtering every coefficient.

*Proof.* By Lemma 2 each output is $Y[t][j] = \sum_{s} h[s] (X[t-s][j] - X[0][j])$, a linear map of the trajectory with the same weights for every $j$. So $\sum_j D_{i j} Y[t][j] = \sum_s h[s] \bigl(\sum_j D_{ij} X[t-s][j] - \sum_j D_{ij} X[0][j]\bigr)$, which is the filter applied to the trajectory of coefficient $i$. $\square$

**Theorem.** For $0 \le \rho < 1$, RASTA returns for each band the output of the stable filter $H_c$, the paper's filter delayed by 4 frames, applied to the trajectory minus its first value. A constant offset on a band changes no output, and the filter has zeros at 0 Hz and at half the frame rate.

*Proof.* Lemmas 2, 3, 5 and 6. $\square$

The tests check Lemma 4 against the first values of the impulse and step responses, Lemma 3 on a constant and on an offset trajectory, Lemma 6 by comparing the gain on long sines with $|H_c|$, and a fixed channel added to every frame of a log band spectrogram.
