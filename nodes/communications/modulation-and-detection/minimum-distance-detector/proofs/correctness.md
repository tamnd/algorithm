---
title: The slicers return a nearest point, which is a maximum likelihood decision
proves: [correctness]
status: full
---

The model is $y = h x + w$ with $h \ne 0$ known, $x$ uniform on the unit-energy constellation $\{a_0, \ldots, a_{M-1}\}$, and $w \sim \mathcal{CN}(0, N_0)$. We write $z = y/h$.

**Lemma 1 (ML is minimum distance).** For each $i$, the density of $y$ given $x = a_i$ is $p(y \mid a_i) = \frac{1}{\pi N_0} \exp(-|y - h a_i|^2 / N_0)$. With equal priors, the MAP rule maximizes $\frac{1}{M} p(y \mid a_i)$, which is the ML rule. The function $t \mapsto \exp(-t/N_0)$ is strictly decreasing, so the maximizers of $p(y \mid a_i)$ are exactly the minimizers of $|y - h a_i|^2$.

*Proof.* The density is that of a circularly symmetric complex Gaussian with mean $h a_i$ and variance $N_0$: the real and imaginary parts of $y - h a_i$ are independent $\mathcal{N}(0, N_0/2)$, and the product of their two densities is the given formula. The rest is the monotonicity of the exponential. $\square$

**Lemma 2 (removing the gain).** $|y - h a|^2 = |h|^2 |z - a|^2$ for every $a$. So the minimizers of $|y - h a_i|^2$ are the minimizers of $|z - a_i|^2$.

*Proof.* $y - h a = h(z - a)$ and $|h(z - a)| = |h|\,|z - a|$. Since $|h|^2 > 0$, the factor does not change the order. $\square$

**Lemma 3 (one axis).** Let $L \ge 2$, let $c_m = L - 1 - 2m$ for $m = 0, \ldots, L - 1$, and let $u$ be real. Put $t = (L - 1 - u)/2$ and $m^* = \min(\max(\lfloor t + 1/2 \rfloor, 0), L - 1)$. Then $|u - c_{m^*}| \le |u - c_m|$ for every $m$.

*Proof.* $u - c_m = 2(m - t)$, so $|u - c_m| = 2|m - t|$, and we must minimize $f(m) = |m - t|$ over the integers $0, \ldots, L - 1$. Let $r = \lfloor t + 1/2 \rfloor$, so $r - 1/2 \le t < r + 1/2$ and $|r - t| \le 1/2$. There are three cases.

- If $t \le 0$, then $r \le \lfloor 1/2 \rfloor = 0$, so $m^* = 0$. Every $m \ge 0$ has $f(m) = m - t \ge -t = f(0)$.
- If $t \ge L - 1$, then $r \ge \lfloor L - 1/2 \rfloor = L - 1$, so $m^* = L - 1$. Every $m \le L - 1$ has $f(m) = t - m \ge t - (L - 1) = f(L - 1)$.
- If $0 < t < L - 1$, then $1/2 < t + 1/2 < L - 1/2$, so $0 \le r \le L - 1$ and $m^* = r$. Every integer $m \ne r$ has $|m - r| \ge 1$, so $f(m) \ge |m - r| - |r - t| \ge 1/2 \ge f(r)$.

In each case $f(m^*) \le f(m)$ for all $m$ in $0, \ldots, L - 1$. $\square$

**Lemma 4 (labels).** In the reference constellations, the PAM point with label $i$ is $c_m / \sqrt{(M^2 - 1)/3}$ with $g(m) = i$, the QAM point with label $i = i_I L + i_Q$ is $(c_{m_I} + j c_{m_Q}) / \sqrt{2(M - 1)/3}$ with $g(m_I) = i_I$ and $g(m_Q) = i_Q$, and the PSK point with label $i$ is $e^{j(2\pi k/M + \phi_0)}$ with $g(k) = i$. Since $g$ is a bijection on $\{0, \ldots, L - 1\}$ for $L$ a power of two, each level has exactly one label.

*Proof.* This is the definition of the labels in the area conventions. The map $g(m) = m \oplus \lfloor m/2 \rfloor$ has the inverse $m = g \oplus \lfloor g/2 \rfloor \oplus \lfloor g/4 \rfloor \oplus \cdots$, so it is a bijection on the integers of $b$ bits for each $b$. $\square$

**Theorem.** For every $y$ with $z = y/h$, DETECT-PAM, DETECT-QAM and DETECT-PSK return the label of a point that minimizes $|y - h a_i|^2$. So each returns a maximum likelihood decision.

*Proof.* By Lemmas 1 and 2 it suffices to show that the returned point minimizes $|z - a_i|^2$.

*PAM.* All points are real, so $|z - a|^2 = (\mathrm{Re}\,z - a)^2 + (\mathrm{Im}\,z)^2$. The second term is the same for every point. With the scale $s = \sqrt{(M^2 - 1)/3}$, $(\mathrm{Re}\,z - c_m/s)^2 = (u - c_m)^2 / s^2$ for $u = s\,\mathrm{Re}\,z$, which is line L4. Lemma 3 with $L = M$ shows that line L1 and line L2 give a nearest level $m^*$, and line L3 returns its label by Lemma 4.

*Square QAM.* With $s = \sqrt{2(M - 1)/3}$ and $s z = u_I + j u_Q$ (line L6), the squared distance to the point with levels $(m_I, m_Q)$ is $\big((u_I - c_{m_I})^2 + (u_Q - c_{m_Q})^2\big)/s^2$. The constellation is the full product of the $L$ levels on each axis, so the two levels can be chosen independently, and the sum is smallest when each term is smallest. Lemma 3 gives a minimizing level on each axis, and line L7 combines the two labels in the order of Lemma 4.

*PSK.* Each point has $|a| = 1$. If $z = 0$, every point has the distance 1, and any output is a minimizer. Otherwise write $z = |z| e^{j\psi}$. For the point at angle $\alpha_k = 2\pi k/M + \phi_0$,

$$|z - e^{j\alpha_k}|^2 = |z|^2 + 1 - 2|z| \cos(\psi - \alpha_k).$$

So the nearest point maximizes $\cos(\psi - \alpha_k)$, that is, it minimizes the distance on the circle between $\psi$ and $\alpha_k$. Put $\theta = \psi - \phi_0$ (line L8) and $t = M\theta/(2\pi)$. The circular distance from $\theta$ to $2\pi k/M$ is $(2\pi/M)$ times the distance from $t$ to the set $k + M\mathbb{Z}$. The integer $r = \lfloor t + 1/2 \rfloor$ is nearest to $t$ among all integers, as in Lemma 3, so $r$ minimizes the distance from $t$ to $k + M\mathbb{Z}$ over $k$ when we take $k = r \bmod M$ (line L9). Line L10 returns its label by Lemma 4.

In each case a tie between two points happens only when $z$ lies on the boundary between their decision regions. These boundaries are lines (PAM and QAM) or rays (PSK), which have probability zero under the Gaussian density, and on them every tied point is a maximum likelihood decision. $\blacksquare$

**Cost.** Each procedure runs a fixed sequence of lines with no loop, so its number of operations is a constant that does not depend on $M$.
