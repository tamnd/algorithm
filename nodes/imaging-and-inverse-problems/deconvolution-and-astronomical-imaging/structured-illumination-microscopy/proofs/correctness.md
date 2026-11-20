---
title: Three phases separate the bands, the shifted bands carry the object spectrum outside the passband, and the noise-free result is the object limited to the extended support
proves: [correctness]
status: full
---

**Setting.** Images are periodic on $n_1 \times n_2$ pixels. The DFT is $X(k) = \sum_r x(r) e^{-2\pi i (k_1 r_1/n_1 + k_2 r_2/n_2)}$, and all frequency indices are taken modulo the image size. The OTF $H$ is real and symmetric, $H(-k) = H(k)$, so the PSF $h$ with $\hat h = H$ is real. For one stripe direction with the integer frequency $k_0$, the depth $m$ and the phases $\varphi_1, \varphi_2, \varphi_3$, frame $j$ is $d_j = h \circledast (P_j x)$ with $P_j(r) = 1 + m\cos(2\pi k_0 \cdot r/n + \varphi_j)$, where $k_0 \cdot r/n$ means $k_{0,1}r_1/n_1 + k_{0,2} r_2/n_2$. Write $a = m/2$.

**Claim 1 (forward model).** $\hat d_j(k) = H(k)\bigl[X(k) + a e^{i\varphi_j} X(k - k_0) + a e^{-i\varphi_j} X(k + k_0)\bigr]$.

*Proof.* $\cos\theta = (e^{i\theta} + e^{-i\theta})/2$, and the DFT of $x(r) e^{2\pi i k_0 \cdot r/n}$ is $X(k - k_0)$, by the definition of the DFT. So $\widehat{P_j x}(k) = X(k) + a e^{i\varphi_j}X(k - k_0) + a e^{-i\varphi_j}X(k + k_0)$. The DFT of a periodic convolution is the product of the DFTs (the [convolution theorem](/convolution-theorem/)). $\square$

The test compares the frames, which the code computes with the DFT, with a direct periodic convolution.

**Claim 2 (band separation).** Let $S_0(k) = H(k)X(k)$, $S_+(k) = H(k)X(k - k_0)$ and $S_-(k) = H(k)X(k + k_0)$. Then $\hat d(k) = M\,(S_0, S_+, S_-)^T(k)$ with the rows $M_j = (1, a e^{i\varphi_j}, a e^{-i\varphi_j})$, and $M$ is invertible if and only if $m \ne 0$ and the three phases are distinct modulo $2\pi$.

*Proof.* The first part is Claim 1. Let $z_j = e^{i\varphi_j}$. Multiplying row $j$ by $z_j$ gives the rows $(z_j, a z_j^2, a)$, so $\det M \cdot z_1z_2z_3 = a^2 \det[z_j, z_j^2, 1]$. Moving the last column to the front is a cyclic permutation of the columns, which has the sign $+1$, so this is $a^2$ times the [Vandermonde](/vandermonde-matrix/) determinant $\prod_{i<j}(z_j - z_i)$. It is $0$ if and only if $a = 0$ or two $z_j$ are equal. $\square$

So line L3 recovers the three bands exactly at every $k$. The code inverts $M$ once by the adjugate and raises an error when $|\det M|$ is tiny. For the equally spaced phases $0, 2\pi/3, 4\pi/3$, the columns of $M$ are orthogonal, because $\sum_j z_j = \sum_j z_j^{-2} = 0$, and their norms are $\sqrt 3$, $a\sqrt 3$ and $a\sqrt 3$. So for white noise of the same variance in each frame, the noise of the three bands is uncorrelated, and the noise of $S_\pm$ is $1/a = 2/m$ times the noise of $S_0$.

**Claim 3 (shifted bands).** Let $T_+(k) = S_+(k + k_0)$ and $T_-(k) = S_-(k - k_0)$ (line L4). Then $T_+(k) = H(k + k_0)X(k)$ and $T_-(k) = H(k - k_0)X(k)$.

*Proof.* Substitute $k + k_0$ and $k - k_0$ in the definitions of $S_+$ and $S_-$. $\square$

So each band is a copy of $X$ seen through a shifted OTF. Where $H(k) = 0$ but $H(k + k_0) \ne 0$, the frequency $k$ of the object, which the widefield image does not contain, is measured.

**Claim 4 (noise-free result).** Let the directions $k_{0,1}, \ldots, k_{0,D}$ each give three frames without noise, and let $\Sigma(k) = \sum_d \bigl[H(k)^2 + H(k + k_{0,d})^2 + H(k - k_{0,d})^2\bigr]$. Lines L5 to L7 give the image with the DFT $\frac{\Sigma(k)}{\Sigma(k) + w} X(k)$ where $\Sigma(k) + w > 0$, and $0$ elsewhere. With $w = 0$ it is $x$ with every frequency outside the extended support $E = \{k : \Sigma(k) > 0\}$ set to $0$.

*Proof.* By Claims 2 and 3, the sum of line L5 is $\sum_d \sum_b H_b(k) \cdot H_b(k) X(k) = \Sigma(k) X(k)$, with the three OTFs $H_b \in \{H(k), H(k + k_{0,d}), H(k - k_{0,d})\}$, and the denominator is $\Sigma(k) + w$. $\square$

The test checks this for three directions against the projection computed directly from the DFT of $x$, and checks that a grating outside the widefield passband is recovered exactly.

**Claim 5 (real output).** For real frames, the DFT of the estimate is Hermitian, $\hat x(-k) = \overline{\hat x(k)}$, so the estimate is real and the real part in line L7 removes only rounding.

*Proof.* The frames are real, so $\hat d_j(-k) = \overline{\hat d_j(k)}$. The conjugate of row $M_j$ is $M_j$ with its last two entries swapped. Let $\Pi$ swap the last two components. Then $\overline{\hat d(k)} = \overline M\, \overline{S(k)} = M \Pi \overline{S(k)}$, and also $\hat d(-k) = M S(-k)$. Since $M$ is invertible, $S(-k) = \Pi \overline{S(k)}$: $S_0(-k) = \overline{S_0(k)}$ and $S_\pm(-k) = \overline{S_\mp(k)}$. Hence $T_+(-k) = S_+(-k + k_0) = \overline{S_-(k - k_0)} = \overline{T_-(k)}$, and the OTF paired with $T_+$ at $-k$ is $H(-k + k_0) = H(k - k_0)$, the one paired with $T_-$ at $k$. So the numerator at $-k$ is the conjugate of the numerator at $k$, and the denominator is symmetric. $\square$

**Claim 6 (the support and the factor of two).** If $H(k) = 0$ for $|k| \ge k_c$, then $E \subseteq \{|k| < k_c + \max_d |k_{0,d}|\}$, and $E$ contains every $k = k_0 + t$ with $|t| < k_c$ and $H(t) \ne 0$. If the stripes are made by the same optics, so that $|k_{0,d}| \le k_c$, the extended support lies inside the disk of radius $2k_c$, and it reaches $2k_c$ along $k_{0,d}$ only when $|k_{0,d}|$ is at the cutoff.

*Proof.* $k \in E$ means $|k| < k_c$ or $|k \pm k_{0,d}| < k_c$ for some $d$, and in the last case $|k| < k_c + |k_{0,d}|$ by the triangle inequality. For $k = k_0 + t$, $H(k - k_0) = H(t) \ne 0$. The last statement follows from the first with $|k_{0,d}| \le k_c$. $\square$

That the stripe frequency is limited by the cutoff of the same objective is a fact about the optics, not about the computation: in a real microscope the stripes are made with the excitation light and the image with the emission light, whose cutoffs differ a little, so the gain is close to, not exactly, a factor of two.

**Claim 7 (widefield frame).** For the phases $0, 2\pi/3, 4\pi/3$, the mean of the three frames is $h \circledast x$.

*Proof.* $\sum_j e^{\pm i\varphi_j} = 0$ for three equally spaced phases, so the side terms of Claim 1 cancel in the mean. $\square$ $\blacksquare$
