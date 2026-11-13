---
title: For a circular shift, the phase correlation surface is the unit impulse at the shift when no bin is zero, and its peak stays unique while fewer than half of the bins are zero
proves: [correctness]
status: full
---

Let $N = WH$ and write $\omega(k, l; x, y) = e^{-2\pi i (kx/W + ly/H)}$. The DFT is $\hat f(k, l) = \sum_{x,y} f(x, y)\,\omega(k, l; x, y)$, and the inverse is $h(x, y) = \frac{1}{N}\sum_{k,l} \hat h(k, l)\,\overline{\omega(k, l; x, y)}$. We work in exact arithmetic and take $\varepsilon = 0$ at line L4, so a bin is set to zero exactly when $P = 0$.

**Lemma 1 (shift theorem).** If $g(x, y) = f((x - d_x) \bmod W, (y - d_y) \bmod H)$, then $\hat g(k, l) = \hat f(k, l)\,\omega(k, l; d_x, d_y)$.

*Proof.* Substitute $x' = (x - d_x) \bmod W$ and $y' = (y - d_y) \bmod H$. As $(x, y)$ runs over the grid, so does $(x', y')$. Since $e^{-2\pi i k (x' + d_x)/W}$ depends on $x' + d_x$ only mod $W$, we get $\omega(k, l; x, y) = \omega(k, l; x', y')\,\omega(k, l; d_x, d_y)$. Hence $\hat g(k, l) = \sum_{x', y'} f(x', y')\,\omega(k, l; x', y')\,\omega(k, l; d_x, d_y) = \hat f(k, l)\,\omega(k, l; d_x, d_y)$. $\square$

**Lemma 2 (orthogonality).** $\frac{1}{N}\sum_{k,l} \overline{\omega(k, l; x - d_x, y - d_y)}$ is $1$ if $(x, y) = (d_x, d_y)$ and $0$ for every other pixel of the grid.

*Proof.* The sum splits into $\frac{1}{W}\sum_{k} e^{2\pi i k (x - d_x)/W}$ times the same sum in $l$. A sum of the $W$-th roots of unity $\zeta^k$ with $\zeta = e^{2\pi i (x - d_x)/W}$ is $W$ if $\zeta = 1$, that is $x \equiv d_x \pmod W$, and $(\zeta^W - 1)/(\zeta - 1) = 0$ otherwise. On the grid, $x \equiv d_x$ means $x = d_x \bmod W$. $\square$

**Theorem 1.** Let $g$ be the circular shift of $f$ by $(d_x, d_y)$ with $0 \le d_x < W$ and $0 \le d_y < H$, and let $Z$ be the set of bins with $\hat f(k, l) = 0$, of size $z$. Then the surface $r$ of line L5 satisfies $r(d_x, d_y) = 1 - z/N$ and $|r(x, y)| \le z/N$ at every other pixel.

*Proof.* By Lemma 1, $P(k, l) = \hat g\,\overline{\hat f} = |\hat f(k, l)|^2\,\omega(k, l; d_x, d_y)$. So $P = 0$ exactly on $Z$, and off $Z$ line L4 gives $R(k, l) = \omega(k, l; d_x, d_y)$, because $|\omega| = 1$. Write $R = \omega(\cdot; d_x, d_y) - E$, where $E$ equals $\omega(\cdot; d_x, d_y)$ on $Z$ and $0$ off $Z$. The inverse DFT is linear. Since $\omega(k, l; d_x, d_y)\,\overline{\omega(k, l; x, y)} = \overline{\omega(k, l; x - d_x, y - d_y)}$, by Lemma 2 the inverse DFT of the first part is the unit impulse $\delta$ at $(d_x, d_y)$. The inverse DFT of $E$ is $e(x, y) = \frac{1}{N}\sum_{(k,l) \in Z} \overline{\omega(k, l; x - d_x, y - d_y)}$, a sum of $z$ terms of magnitude $1/N$, so $|e(x, y)| \le z/N$, and $e(d_x, d_y) = z/N$ because each term is $1/N$ there. Since $f$ is real, $Z$ is closed under $(k, l) \mapsto (-k \bmod W, -l \bmod H)$, so $e$ is real, and $r = \delta - e$ is real too. Hence $r(d_x, d_y) = 1 - z/N$ and $|r(x, y)| = |e(x, y)| \le z/N$ elsewhere. $\square$

**Corollary 1 (no zero bins).** If $z = 0$, then $r$ is the unit impulse at $(d_x, d_y)$, so line L6 returns $(d_x, d_y)$ and line L7 returns $1$.

**Corollary 2 (unique peak).** If $z < N/2$, then $1 - z/N > z/N$, so $(d_x, d_y)$ is the only maximum of $r$ and line L6 returns it.

**Lemma 3 (signed shift).** Lines L8 and L9 return the unique representative of $d_x \bmod W$ in $(-W/2, W/2]$, and the same for $d_y$.

*Proof.* For $0 \le d_x \le \lfloor W/2 \rfloor$ the value is kept and it lies in $[0, W/2]$. For $\lfloor W/2 \rfloor < d_x < W$ the value $d_x - W$ lies in $(-W/2, 0)$: indeed $d_x - W < 0$, and $d_x \ge \lfloor W/2 \rfloor + 1 > W/2$ gives $d_x - W > -W/2$. The interval $(-W/2, W/2]$ has length $W$ and is half open, so it holds exactly one value of each class mod $W$. $\square$

**Theorem 2 (gain and offset).** Let $g' = a g + b$ with $a > 0$, and assume that $\hat f(0, 0)$ and $\hat g'(0, 0)$ have the same sign as $\hat g(0, 0)$ (for example, all three images have a positive mean). Then $g'$ gives the same normalized spectrum $R$ as $g$, and so the same surface.

*Proof.* The DFT of a constant $b$ is $bN$ at $(0, 0)$ and $0$ elsewhere. So $\hat g' = a\hat g$ at every bin except $(0, 0)$, and $P' = aP$ there; since $a > 0$, $P'/|P'| = P/|P|$, and $P' = 0$ exactly when $P = 0$. At $(0, 0)$ both $P$ and $P'$ are real, equal to $\hat g(0, 0)\hat f(0, 0)$ and $\hat g'(0, 0)\hat f(0, 0)$, and by the sign assumption they have the same sign, so both normalize to the same value $\pm 1$. $\square$
