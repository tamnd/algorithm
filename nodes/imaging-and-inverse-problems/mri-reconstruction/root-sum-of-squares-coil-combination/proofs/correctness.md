---
title: The root-sum-of-squares combination returns the object magnitude times the coil norm, and it bounds the optimal combination
proves: [correctness]
status: full
---

The setting is one pixel. The coil values form the vector $v \in \mathbb{C}^c$. The model is $v = \rho s + \eta$ with the object value $\rho \in \mathbb{C}$, the map vector $s \ne 0$ and the noise $\eta$. The noise has zero mean and the Hermitian positive definite covariance $\Psi = \mathrm{E}[\eta \eta^H]$, and $\Psi = L L^H$ is its Cholesky factorization (line L1). Line L4 computes $w = L^{-1} v$ and line L5 returns $\lVert w \rVert$. Write $u = L^{-1} s$ and $q = s^H \Psi^{-1} s = \lVert u \rVert^2 > 0$. The optimal combination is $\hat\rho = s^H \Psi^{-1} v / q = u^H w / q$.

**Theorem.**
1. Without noise, the prewhitened combination is $|\rho| \sqrt{q}$, and with $\Psi = I$ the plain combination is $|\rho| \lVert s \rVert$. The plain combination does not change when each coil value is multiplied by its own phase factor $e^{i\theta_k}$.
2. For any $v$, $\lVert w \rVert^2 = q\, |\hat\rho|^2 + \lVert P^\perp w \rVert^2$, where $P^\perp$ is the orthogonal projection onto the complement of $u$. Hence $\lVert w \rVert \ge \sqrt{q}\, |\hat\rho|$, with equality if and only if $w$ is a multiple of $u$.
3. Among the linear combinations $a^H v$ with $a^H s = 1$, which are unbiased for $\rho$, the variance $a^H \Psi a$ is smallest for $a = \Psi^{-1} s / q$, which gives $\hat\rho$, and the smallest variance is $1/q$.
4. If $\rho = 0$ and $\eta$ is circular complex Gaussian with covariance $\Psi$, then $\mathrm{E} \lVert w \rVert = \Gamma(c + \tfrac12)/\Gamma(c)$.

*Proof of 1.* Without noise, $w = \rho L^{-1} s = \rho u$, so $\lVert w \rVert = |\rho| \lVert u \rVert = |\rho| \sqrt{q}$. For $\Psi = I$, $L = I$ and $u = s$. Multiplying $v_k$ by $e^{i\theta_k}$ does not change $|v_k|$, so the plain sum $\sum_k |v_k|^2$ does not change. $\square$

*Proof of 2.* Let $P = u u^H / q$ be the orthogonal projection onto the span of $u$, and $P^\perp = I - P$. Then $\lVert w \rVert^2 = \lVert P w \rVert^2 + \lVert P^\perp w \rVert^2$ by Pythagoras. And $\lVert P w \rVert^2 = |u^H w|^2 / q = q\, |u^H w / q|^2 = q |\hat\rho|^2$, because $u^H w = s^H L^{-H} L^{-1} v = s^H \Psi^{-1} v$. Equality in the bound holds if and only if $P^\perp w = 0$. $\square$

*Proof of 3.* Write $b = L^H a$. Then $a^H s = b^H u$ and $a^H \Psi a = \lVert b \rVert^2$. By the Cauchy-Schwarz inequality, $1 = |b^H u|^2 \le \lVert b \rVert^2 \lVert u \rVert^2$, so $a^H \Psi a \ge 1/q$, with equality if and only if $b$ is a multiple of $u$. With $b^H u = 1$ this gives $b = u/q$, so $a = L^{-H} u / q = \Psi^{-1} s / q$. This is the Gauss-Markov theorem for one unknown. $\square$

*Proof of 4.* The whitened noise $w = L^{-1}\eta$ has the covariance $L^{-1} \Psi L^{-H} = I$, so its entries are independent circular complex Gaussians with $\mathrm{E}|w_k|^2 = 1$. Then $|w_k|^2$ is exponential with mean 1, and $T = \lVert w \rVert^2$ is a sum of $c$ of them, with the Gamma density $t^{c-1} e^{-t}/\Gamma(c)$ on $t > 0$. Hence

$$\mathrm{E}\sqrt{T} = \frac{1}{\Gamma(c)} \int_0^\infty t^{c - 1/2} e^{-t}\, dt = \frac{\Gamma(c + \tfrac12)}{\Gamma(c)}. \qquad \square$$

**Remarks.**
- Part 2 shows that the prewhitened combination is the magnitude of the optimal combination, scaled by $\sqrt{q}$, plus a term that holds only noise. That term has $c - 1$ complex dimensions and causes the bias of the combination at low signal to noise ratio. At high signal to noise ratio the two agree to first order in the noise.
- The theorem is about the pixel model with independent pixels. The noise model is an assumption about the receiver chain; Kellman and McVeigh (2005) describe how to measure $\Psi$ from a noise scan.
- For $c = 4$, part 4 gives the noise-only mean $1.9386$, which the test of this page checks by simulation within 1.5 percent.
