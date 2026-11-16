---
title: Shape from focus picks the frame of largest focus, and its Gaussian fit is exact for Gaussian focus profiles
proves: [correctness]
status: full
---

We use the pseudocode of the page. The stack has $N$ frames at focus positions $d_0 + k \Delta$ for $k = 0, \dots, N - 1$. $F_k(p)$ is the focus measure of frame $k$ at pixel $p$ from line L2.

**Lemma 1 (window sums).** The integral image $S[v][u] = \sum_{v' < v,\, u' < u} x(v', u')$ gives the sum of $x$ over the rows $[v_0, v_1)$ and columns $[u_0, u_1)$ as $S[v_1][u_1] - S[v_0][u_1] - S[v_1][u_0] + S[v_0][u_0]$.

*Proof.* The code builds $S[v+1][u+1] = S[v][u+1] + \sum_{u' \le u} x(v, u')$, which is the definition. Inclusion and exclusion of the four corner rectangles gives the formula. $\square$

So line L2 computes $F_k(p) = \sum_{q} \mathrm{ML}_k(q) [\mathrm{ML}_k(q) \ge T_1]$ over the window of $p$ cut at the border, as Nayar and Nakagawa define the sum-modified-Laplacian.

**Lemma 2 (selection).** Line L4 sets $m$ to the least index with $F_m(p) = \max_k F_k(p)$. $\square$

**Theorem 1 (the Gaussian fit).** Let $0 < m < N - 1$ and suppose that the three values near the peak follow a Gaussian,

$$F_k = A \exp\left(-\frac{(k - c)^2}{2 s^2}\right) \quad \text{for } k \in \{m - 1, m, m + 1\},$$

with $A > 0$ and $s > 0$. Then line L5 finds $m + \delta = c$, so line L6 returns $d_0 + c \Delta$, the position of the peak.

*Proof.* Let $a, b, e$ be the logarithms of $F_{m-1}, F_m, F_{m+1}$. Then $\ln F_k = \ln A - (k - c)^2 / (2 s^2)$, a parabola in $k$. A direct computation gives

$$a - 2 b + e = -\frac{1}{s^2} < 0, \qquad a - e = \frac{2 (m - c)}{s^2}.$$

So the code accepts the fit, and

$$\delta = \frac{1}{2} \cdot \frac{a - e}{a - 2 b + e} = \frac{1}{2} \cdot \frac{2 (m - c) / s^2}{-1 / s^2} = c - m. \qquad \blacksquare$$

**Lemma 3 (the step stays in the interval).** If $F_m \ge F_{m-1}$, $F_m \ge F_{m+1}$, all three are positive and the fit is accepted, then $|\delta| \le 1/2$.

*Proof.* Let $x = b - a \ge 0$ and $y = b - e \ge 0$. Then $a - 2 b + e = -(x + y)$, which is negative because the fit was accepted, and $a - e = y - x$. So $\delta = (x - y) / (2 (x + y))$, and $|x - y| \le x + y$. $\square$

So the refined position lies within half a frame of the best frame, and a fit that is not exact still cannot move the result past a neighboring frame.

**Lemma 4 (gain and offset).** If every frame is replaced by $a I + b$ with $a > 0$, then $\mathrm{ML}$ is multiplied by $a$. With $T_1 = 0$, every $F_k$ is multiplied by $a$, and the choice of $m$ and the offset $\delta$ do not change.

*Proof.* The weights $2, -1, -1$ in each term of $\mathrm{ML}$ sum to 0, so $b$ cancels and $a$ comes out of the absolute values. Scaling all $F_k$ by $a$ keeps the argmax, and adds $\ln a$ to $a, b, e$ in Theorem 1, which cancels in both differences. With $T_1 > 0$ the threshold must be scaled by $a$ too. $\square$

**Theorem 2 (blur lowers the energy of the Laplacian).** Let $T$ be a periodic image on the plane whose Laplacian is square integrable over one period, and let $B_\sigma = G_\sigma * T$ for the Gaussian $G_\sigma$ of standard deviation $\sigma$. Then $E(\sigma) = \int |\Delta B_\sigma|^2$ over one period is strictly decreasing in $\sigma \ge 0$, unless $T$ is constant.

*Proof.* Write $T$ as a Fourier series with coefficients $\hat T(\omega)$. The Laplacian multiplies the coefficient at frequency $\omega$ by $-|\omega|^2$, and the Gaussian multiplies it by $\exp(-\sigma^2 |\omega|^2 / 2)$. By Parseval's theorem,

$$E(\sigma) = C \sum_{\omega} |\omega|^4 |\hat T(\omega)|^2 \exp(-\sigma^2 |\omega|^2)$$

for a constant $C > 0$. The term with $\omega = 0$ is 0. Every other term is nonnegative and nonincreasing in $\sigma$, and strictly decreasing if $\hat T(\omega) \ne 0$. If $T$ is not constant, some $\hat T(\omega)$ with $\omega \ne 0$ is not zero. $\square$

For a scene at one depth whose blur grows with the distance from focus, Theorem 2 says that the squared Laplacian, summed over the image, is largest in the sharpest frame. This is the reason for Laplacian-based focus measures.

**What is not proved.** The modified Laplacian uses absolute values instead of squares, the window is small, the threshold drops small values, and real blur is not an exact Gaussian. Theorem 2 covers none of these, so the claim that SML peaks at the right frame is a heuristic that Nayar and Nakagawa support by experiments. The test file shows one way it can fail: a blur kernel cut off at a radius of 3 pixels behaves like a box filter at large $\sigma$, and the measure is then not monotone far from focus, though it still peaks at the sharp frame. Theorem 1 also assumes a Gaussian focus profile; for other shapes the fit is only an approximation, bounded by Lemma 3.
