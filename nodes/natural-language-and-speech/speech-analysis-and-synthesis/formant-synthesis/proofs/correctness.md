---
title: Correctness of the digital formant resonator
proves: [correctness]
status: full
---

Formant synthesis is a fixed linear recursion, so its correctness is the set of properties of the resonator that the method relies on. Throughout, $T = 1/f_s$, $F$ is the center frequency, $B > 0$ the bandwidth, $r = e^{-\pi B T}$ and $\theta = 2\pi F T$ with $0 \le \theta \le \pi$, and

$$C = -e^{-2\pi B T} = -r^2, \qquad B_1 = 2 e^{-\pi B T} \cos(2\pi F T) = 2 r \cos\theta, \qquad A = 1 - B_1 - C .$$

The resonator is $y[n] = A x[n] + B_1 y[n-1] + C y[n-2]$, with transfer function $H(z) = A / (1 - B_1 z^{-1} - C z^{-2})$.

## Lemma 1 (the poles)

$1 - B_1 z^{-1} - C z^{-2} = (1 - r e^{i\theta} z^{-1})(1 - r e^{-i\theta} z^{-1})$. So the poles are $r e^{\pm i\theta}$, and since $0 < r < 1$ for $B > 0$, the filter is stable.

*Proof.* Expand the right side: $1 - r(e^{i\theta} + e^{-i\theta}) z^{-1} + r^2 z^{-2} = 1 - 2r\cos\theta\, z^{-1} + r^2 z^{-2}$, which is $1 - B_1 z^{-1} - C z^{-2}$. A causal rational filter is stable if and only if its poles are inside the unit circle, and $|r e^{\pm i\theta}| = r = e^{-\pi B T} < 1$. $\square$

## Lemma 2 (unit gain at 0 Hz)

$H(1) = 1$. Hence a constant input $x[n] = c$ gives an output that tends to $c$.

*Proof.* $H(1) = A / (1 - B_1 - C) = A / A = 1$, and $A = (1 - r e^{i\theta})(1 - r e^{-i\theta}) = |1 - r e^{i\theta}|^2 > 0$ by Lemma 1 at $z = 1$, so the division is defined. For a stable filter, the response to a step of size $c$ tends to $c H(1)$. $\square$

## Lemma 3 (the impulse response)

For $0 < \theta < \pi$, the impulse response is $h[n] = A r^n \sin((n+1)\theta) / \sin\theta$ for $n \ge 0$.

*Proof.* Let $g[n] = r^n \sin((n+1)\theta) / \sin\theta$. Then $g[0] = 1$ and $g[1] = r \sin 2\theta / \sin\theta = 2r\cos\theta = B_1$. For $n \ge 2$, the identity $\sin((n+1)\theta) = 2\cos\theta \sin(n\theta) - \sin((n-1)\theta)$ gives

$$g[n] = 2r\cos\theta \cdot r^{n-1} \frac{\sin(n\theta)}{\sin\theta} - r^2 \cdot r^{n-2} \frac{\sin((n-1)\theta)}{\sin\theta} = B_1 g[n-1] + C g[n-2].$$

The impulse response satisfies $h[0] = A$, $h[1] = B_1 h[0] = A B_1$, and $h[n] = B_1 h[n-1] + C h[n-2]$ for $n \ge 2$. So $h$ and $A g$ satisfy the same recursion with the same first two values, and they are equal by induction. $\square$

## Lemma 4 (the peak)

Let $c^* = (1 + r^2)\cos\theta / (2r)$. On $0 \le \omega \le \pi$, $|H(e^{i\omega})|$ has its maximum at $\omega^* = \arccos c^*$ if $-1 \le c^* \le 1$, and at $\omega = 0$ if $c^* > 1$.

*Proof.* By Lemma 1, $|H(e^{i\omega})|^{-2} = A^{-2} |e^{i\omega} - r e^{i\theta}|^2 |e^{i\omega} - r e^{-i\theta}|^2$. Expand each factor: $|e^{i\omega} - r e^{\pm i\theta}|^2 = 1 + r^2 - 2r\cos(\omega \mp \theta)$. Their product, with $p = 1 + r^2$ and $u = \cos\omega$, is

$$(p - 2r\cos(\omega - \theta))(p - 2r\cos(\omega + \theta)) = p^2 - 2rp \cdot 2\cos\omega\cos\theta + 4r^2 \cos(\omega - \theta)\cos(\omega + \theta).$$

With $\cos(\omega - \theta)\cos(\omega + \theta) = \cos^2\omega - \sin^2\theta = u^2 - \sin^2\theta$, this is $Q(u) = 4r^2 u^2 - 4rp\cos\theta\, u + p^2 - 4r^2\sin^2\theta$, a quadratic in $u$ with positive leading coefficient. Its minimum over the reals is at $u = p\cos\theta / (2r) = c^*$. The gain is largest where $Q$ is least. If $c^* \in [-1, 1]$, the least value on $u \in [-1, 1]$ is at $u = c^*$, that is $\omega = \arccos c^*$. If $c^* > 1$, $Q$ is decreasing on $[-1, 1]$, so the least value is at $u = 1$, $\omega = 0$. $\square$

Since $(1 + r^2)/(2r) \ge 1$, with equality only at $r = 1$, we have $|c^*| \ge |\cos\theta|$, so the peak is below $F$ when $\theta < \pi/2$ and moves further down as $B$ grows. In the example of the page, $F = 500$, $B = 60$ and $f_s = 10000$ give $\omega^* f_s / 2\pi = 499.13$ Hz.

## Lemma 5 (the antiresonator is the inverse)

With $A' = 1/A$, $B_1' = -B_1/A$ and $C' = -C/A$, the filter $y[n] = A' x[n] + B_1' x[n-1] + C' x[n-2]$ has $H'(z) = (1 - B_1 z^{-1} - C z^{-2}) / A = 1 / H(z)$. So a resonator followed by the antiresonator with the same $F$ and $B$ returns the input exactly, from zero states.

*Proof.* $H'(z) = A' + B_1' z^{-1} + C' z^{-2} = (1 - B_1 z^{-1} - C z^{-2}) / A$, and $H(z) H'(z) = 1$. Both filters are causal and start from zero states, so the output of the pair is the input convolved with the impulse response of $H H' = 1$, which is the input. $\square$

## Lemma 6 (the cascade)

If $K$ resonators with fixed coefficients are in series, the transfer function of the chain is $\prod_k H_k(z)$, and its gain at 0 Hz is 1.

*Proof.* Each section is a linear time-invariant filter, and the transfer function of a series of such filters is the product of theirs, since the z-transform turns convolution into multiplication. At $z = 1$, each factor is 1 by Lemma 2. $\square$

## The synthesis loop

When the coefficients change at a frame boundary, the states $y[n-1]$ and $y[n-2]$ keep their values, so the output is continuous in the sense that the new recursion starts from the old state; the system is then linear but not time-invariant, and Lemmas 3 and 4 hold only inside each frame. The radiation step $v[n] - v[n-1]$ has the response $1 - e^{-i\omega}$, which is 0 at 0 Hz and rises by 6 dB per octave at low frequencies. The whole chain therefore passes no DC, by design.

The half-power width of a single resonator is close to $B$ when $B T$ is small: near the peak, $|e^{i\omega} - r e^{i\theta}|^2 \approx (1 - r)^2 + (\omega - \theta)^2$, which doubles at $|\omega - \theta| = 1 - r \approx \pi B T$, a total width of $2\pi B T$ in radians, that is $B$ in Hz. This is a first-order approximation, not an identity, and the tests check it only to 3 percent.
