---
title: "W-projection is exact with the full kernel, its gridding is the adjoint of its degridding, and a cut kernel has an error bounded by the dropped kernel energy"
proves: [correctness]
status: full
---

**Setting.** The image has $n \times n$ pixels with signed offsets $p = (a, b)$, $-n/2 \le a, b < n/2$, and $N = n^2$. All index arithmetic on the grid is mod $n$ in each coordinate, and $k \cdot p$ is $k_v a + k_u b$. The direction cosines are $l = b\,\Delta l$ and $m = a\,\Delta l$, with $l^2 + m^2 < 1$ on the grid, and $\nu_p = \sqrt{1 - l^2 - m^2} > 0$. The DFT is $\hat f(k) = \sum_p f(p)\, e^{-2\pi i\, k \cdot p/n}$, and its inverse is $f(p) = \frac1N \sum_k \hat f(k)\, e^{2\pi i\, k \cdot p/n}$.

For a real sky $x$ let $y_p = x_p / \nu_p$. For a real $w$ let $G_w(p) = e^{-2\pi i w(\nu_p - 1)}$ and $K_w = \frac1N \hat G_w$. The model visibility at the grid point $k$ and height $w$ is

$$V(k, w) = \sum_p y_p\, G_w(p)\, e^{-2\pi i\, k \cdot p/n} = \widehat{y G_w}(k).$$

The visibilities are $(k_j, w_j, V_j, \omega_j)$ for $j = 1, \dots, m$, with $\omega_j > 0$ and $\Omega = \sum_j \omega_j$. A support $T$ is a set of offsets $q$; the full support is the whole grid, and the cut support of lines L7 to L9 is $T_S = \{q : |q_v|, |q_u| \le S\}$. For a support $T$, degridding is

$$P_j(x) = \sum_{q \in T} K_{w_j}(q)\, \hat y(k_j - q),$$

and lines L1 to L6 give the image

$$D_p = \frac{1}{\Omega\, \nu_p}\, \mathrm{Re} \sum_k F(k)\, e^{2\pi i\, k \cdot p/n}, \qquad F(k) = \sum_j \sum_{q \in T,\; k_j - q = k} \omega_j\, \overline{K_{w_j}(q)}\, V_j .$$

Line L5 computes $N \cdot \mathrm{IDFT}(F)$, which is the sum over $k$ above.

**Claim 1 (the w term is a convolution).** For every $k$ and $w$, $V(k, w) = \sum_q K_w(q)\, V(k - q, 0)$, where $q$ runs over the whole grid.

*Proof.* By the inverse DFT, $G_w(p) = \sum_q K_w(q)\, e^{2\pi i\, q \cdot p/n}$. Put this into the definition of $V(k, w)$:

$$V(k, w) = \sum_q K_w(q) \sum_p y_p\, e^{-2\pi i\,(k - q) \cdot p/n} = \sum_q K_w(q)\, \hat y(k - q).$$

Since $G_0 = 1$, $\hat y(k - q) = V(k - q, 0)$. $\square$

So degridding with the full support gives $P_j(x) = V(k_j, w_j)$, the exact model visibility.

**Claim 2 (the gridded image is the adjoint of degridding).** Fix any support $T$. For every real image $x$ and every set of data $V_j$,

$$\sum_p x_p\, D_p = \frac1\Omega \sum_j \omega_j\, \mathrm{Re}\big(V_j\, \overline{P_j(x)}\big).$$

*Proof.* Write $P_j(x) = \sum_p \tilde a_{jp}\, x_p$ with

$$\tilde a_{jp} = \frac{1}{\nu_p} \sum_{q \in T} K_{w_j}(q)\, e^{-2\pi i\,(k_j - q) \cdot p/n},$$

which follows from $\hat y(k) = \sum_p x_p \nu_p^{-1} e^{-2\pi i\, k \cdot p/n}$. Each pair $(j, q)$ adds $\omega_j \overline{K_{w_j}(q)} V_j$ to $F$ at $k = k_j - q$, so

$$\sum_k F(k)\, e^{2\pi i\, k \cdot p/n} = \sum_j \omega_j V_j \sum_{q \in T} \overline{K_{w_j}(q)}\, e^{2\pi i\,(k_j - q) \cdot p/n} = \sum_j \omega_j V_j\, \nu_p\, \overline{\tilde a_{jp}} .$$

Hence $D_p = \frac1\Omega \sum_j \omega_j\, \mathrm{Re}(V_j\, \overline{\tilde a_{jp}})$. Multiply by the real $x_p$ and sum over $p$. Because $x_p$ is real, $\sum_p x_p \overline{\tilde a_{jp}} = \overline{P_j(x)}$, and the real part is linear over real factors. $\square$

**Claim 3 (the full kernel gives the exact dirty image).** With the full support, $D_p = \frac1\Omega \sum_j \omega_j\, \mathrm{Re}(V_j\, \overline{a_{jp}})$ with $a_{jp} = G_{w_j}(p)\, e^{-2\pi i\, k_j \cdot p/n} / \nu_p$.

*Proof.* By the proof of Claim 2 it is enough to show $\tilde a_{jp} = a_{jp}$ for the full support. Then the sum over $q$ is the whole inverse DFT, $\sum_q K_w(q)\, e^{2\pi i\, q \cdot p/n} = G_w(p)$, so $\tilde a_{jp} = \nu_p^{-1} e^{-2\pi i\, k_j \cdot p/n} G_{w_j}(p) = a_{jp}$. $\square$

**Claim 4 (properties of the kernel).** (a) $K_0(0) = 1$ and $K_0(q) = 0$ for $q \ne 0$. (b) $\sum_q |K_w(q)|^2 = 1$. (c) $K_{-w}(q) = \overline{K_w(-q)}$.

*Proof.* (a) $G_0 = 1$, and the DFT of the constant 1 is $N$ at $k = 0$ and $0$ elsewhere. (b) By Parseval's theorem for this DFT, $\sum_q |\hat G_w(q)|^2 = N \sum_p |G_w(p)|^2 = N \cdot N$, because $|G_w(p)| = 1$. Divide by $N^2$. (c) $G_{-w} = \overline{G_w}$, and $\widehat{\overline f}(q) = \overline{\hat f(-q)}$ for every $f$. Divide by $N$. $\square$

**Claim 5 (the error of a cut kernel).** Let $E = \sum_{q \in T} |K_w(q)|^2$ be the energy that the support $T$ keeps, for the height $w = w_j$. Then

$$\Big|P_j(x) - V(k_j, w_j)\Big| \le \sqrt{1 - E}\; \sqrt N\; \|y\|_2 .$$

*Proof.* By Claim 1 the difference is $-\sum_{q \notin T} K_w(q)\, \hat y(k_j - q)$. By the Cauchy-Schwarz inequality its modulus is at most

$$\Big(\sum_{q \notin T} |K_w(q)|^2\Big)^{1/2} \Big(\sum_{q \notin T} |\hat y(k_j - q)|^2\Big)^{1/2} \le \sqrt{1 - E}\, \Big(\sum_k |\hat y(k)|^2\Big)^{1/2},$$

using Claim 4(b) and the fact that $k_j - q$ meets each grid point at most once. Parseval's theorem gives $\sum_k |\hat y(k)|^2 = N \|y\|_2^2$. $\square$

The bound holds for every sky, and it tends to 0 as $T$ grows to the full grid, where $E = 1$. For the image, Claim 2 says that the cut-kernel image is the exact adjoint of the cut model, and the difference from the exact image at pixel $p$ is $\frac1\Omega \sum_j \omega_j\, \mathrm{Re}\big(V_j\, \overline{(\tilde a_{jp} - a_{jp})}\big)$, where $|\tilde a_{jp} - a_{jp}| = \nu_p^{-1} \big|\sum_{q \notin T} K_{w_j}(q)\, e^{2\pi i\, q \cdot p/n}\big|$ is the error of the cut kernel as an approximation of $G_{w_j}(p)$.

**Claim 6 (the center needs no correction).** If $x$ is zero outside the pixel $p = 0$, then $V(k, w) = V(k, 0)$ for every $w$, so the prediction without the $w$ term is exact for this sky.

*Proof.* At $p = 0$, $l = m = 0$, so $\nu_0 = 1$ and $G_w(0) = 1$. The sum that defines $V(k, w)$ has only the term $p = 0$, which does not depend on $w$. $\square$
