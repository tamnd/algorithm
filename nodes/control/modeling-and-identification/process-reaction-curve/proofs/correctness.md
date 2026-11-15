---
title: The FOPDT fit recovers K, L and T from a first-order plus dead time response
proves: [correctness]
status: full
---

We work in exact real arithmetic, with $e^x$ and $\ln$ as exact operations. Measure time from the step, so $t_0 = 0$, and let $K \ne 0$, $L \ge 0$ and $T > 0$. Let

$$\phi(t) = 0 \text{ for } t < L, \qquad \phi(t) = 1 - e^{-(t - L)/T} \text{ for } t \ge L,$$

the normalized step response of the FOPDT model.

**Hypotheses.** The samples are $y_i = y_0 + K \Delta u\, \phi(t_i)$ for $0 \le i \le n-2$ and $y_{n-1} = y_0 + K \Delta u$. The record is long enough in this sense: $t_{n-2} \ge L + T$, and the last chord of $z$, from $t_{n-2}$ to $t_{n-1}$, is not steeper than any chord of $z$ that lies in $[L, t_{n-2}]$. (The second condition holds when the last interval is not much shorter than the others, since $1 - \phi(t_{n-2}) \le e^{-1}$ is small.)

**Lemma 1 (gain and normalization).** L1 returns $K$, and after L2, $z_i = \phi(t_i)$ for $i \le n - 2$ and $z_{n-1} = 1$.

*Proof.* $y_{n-1} - y_0 = K \Delta u$, which is nonzero, so L1 gives $K \Delta u / \Delta u = K$, and L2 gives $z_i = K \Delta u\, \phi(t_i) / (K \Delta u) = \phi(t_i)$. $\square$

Note that the sign of $K$ and of $\Delta u$ plays no role after L2: $z$ always rises from 0 to 1.

**Lemma 2 (the two levels).** For $0 < c < 1$, the first time at which $\phi$ reaches $c$ is $L - T \ln(1 - c)$. In particular $\phi$ reaches $1 - e^{-1/3}$ at $L + T/3$ and $1 - e^{-1}$ at $L + T$.

*Proof.* $\phi = 0 < c$ before $L$, and on $[L, \infty)$ it is continuous and strictly increasing, so the first time is the unique solution of $1 - e^{-(t - L)/T} = c$, which is $t = L - T \ln(1 - c)$. For $c = 1 - e^{-1/3}$ this is $L + T/3$, and for $c = 1 - e^{-1}$ it is $L + T$. $\square$

**Theorem 1 (two-point, exact crossings).** If L4 returns the exact first crossing times of $\phi$, then L5 and L6 return $T$ and $L$.

*Proof.* By Lemma 2, $t_{63} - t_{28} = (L + T) - (L + T/3) = 2T/3$, so L5 gives $1.5 \cdot 2T/3 = T$, and L6 gives $(L + T) - T = L$. $\square$

**Theorem 2 (two-point, linear interpolation).** Let every sample interval have length at most $h \le T/3$. Then each of the times returned by L4 differs from the exact crossing time by at most $\frac{h^2 e^{h/T}}{8 T}$.

*Proof.* Fix a level $c \in \{1 - e^{-1/3}, 1 - e^{-1}\}$ and let $t^* = L - T \ln(1 - c)$, so $t^* \ge L + T/3$ by Lemma 2. Since $t_{n-2} \ge L + T \ge t^*$ and $\phi$ is nondecreasing, the scan of L4 stops at the first $i \le n - 2$ with $z_i \ge c$; then $z_{i-1} < c \le z_i$ and so $t_{i-1} < t^* \le t_i$. Hence $t_{i-1} \ge t^* - h \ge L$, and $\phi$ is smooth on $[t_{i-1}, t_i]$ with

$$\phi'(t) = \tfrac{1}{T} e^{-(t - L)/T} \ge \tfrac{1}{T} e^{-(t_i - L)/T}, \qquad \lvert \phi''(t) \rvert = \tfrac{1}{T^2} e^{-(t - L)/T} \le \tfrac{1}{T^2} e^{-(t_{i-1} - L)/T}.$$

Let $\ell$ be the line through $(t_{i-1}, z_{i-1})$ and $(t_i, z_i)$, and $\hat t$ the time with $\ell(\hat t) = c$, which L4 returns; $\hat t \in (t_{i-1}, t_i]$. The error of linear interpolation is $\lvert \phi(t) - \ell(t) \rvert \le \frac{(t_i - t_{i-1})^2}{8} \max \lvert \phi'' \rvert \le \frac{h^2}{8} \max \lvert \phi'' \rvert$ on the interval. So $\lvert \phi(\hat t) - \phi(t^*) \rvert = \lvert \phi(\hat t) - \ell(\hat t) \rvert \le \frac{h^2}{8} \max \lvert \phi'' \rvert$. By the mean value theorem, $\lvert \phi(\hat t) - \phi(t^*) \rvert \ge \min \phi' \cdot \lvert \hat t - t^* \rvert$, both extremes taken over $[t_{i-1}, t_i]$. Therefore

$$\lvert \hat t - t^* \rvert \le \frac{h^2}{8} \cdot \frac{\max \lvert \phi'' \rvert}{\min \phi'} \le \frac{h^2}{8} \cdot \frac{1}{T} e^{(t_i - t_{i-1})/T} \le \frac{h^2 e^{h/T}}{8 T}. \qquad \square$$

**Theorem 3 (tangent).** Suppose $L$ is a sample time $t_m$ with $m \le n - 3$, and let $h = t_{m+1} - t_m$. Then L7 selects the chord from $t_m$ to $t_{m+1}$, L8 returns $L$ exactly, and L9 returns $\frac{h}{1 - e^{-h/T}}$, which lies in $(T, T + h]$ and equals $T + h/2 + O(h^2)$ as $h \to 0$.

*Proof.* For $i < m$, $z_i = z_{i+1} = 0$, so those chords have slope 0. The chord from $t_m$ to $t_{m+1}$ has slope $s_m = (1 - e^{-h/T})/h > 0$. On $[L, \infty)$, $\phi$ is strictly concave, so the slopes of consecutive chords between samples in $[L, t_{n-2}]$ strictly decrease from left to right. By the hypothesis on the last chord, no chord is steeper than $s_m$, and every chord after it in $[L, t_{n-2}]$ is strictly less steep. L7 keeps the first chord of largest slope, so it selects the chord at $m$, with midpoint $\bar t = L + h/2$ and $\bar z = (0 + \phi(L + h))/2 = h s_m / 2$. L8 gives $L + h/2 - (h s_m/2)/s_m = L$, and L9 gives $1/s_m = h/(1 - e^{-h/T})$.

For the bounds, put $x = h/T > 0$; then $1/s_m = T \cdot x/(1 - e^{-x})$. Since $e^{-x} > 1 - x$, $1 - e^{-x} < x$ and the ratio is greater than 1. Since $e^{x} \ge 1 + x$, $e^{-x} \le 1/(1 + x)$, so $1 - e^{-x} \ge x/(1 + x)$ and the ratio is at most $1 + x$. Multiplying by $T$ gives $T < 1/s_m \le T + h$. Finally, $x/(1 - e^{-x})$ is analytic at $x = 0$ with the expansion $1 + x/2 + x^2/12 + \cdots$, so $1/s_m = T + h/2 + O(h^2)$. $\square$

**Corollary.** Under the hypotheses, the algorithm returns $K$ exactly by both methods; the two-point method returns $L$ and $T$ exactly with exact crossings, and within $O(h^2)$ with interpolated crossings, since L5 and L6 are linear in $t_{28}$ and $t_{63}$; and the tangent method returns $L$ exactly and $T$ within $h$, with error $h/2 + O(h^2)$, when the dead time is a sample time. $\blacksquare$
