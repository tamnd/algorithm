---
title: Each step of SIFT does what it claims, from the blur levels and the 26-neighbour extrema to the quadratic fit, the edge test, the normalized descriptor and the ratio test
proves: [correctness]
status: full
---

SIFT has no theorem that it finds the same scene points in two images; that depends on the scene. What can be proved is that each line computes the quantity it is meant to compute. The blur statements are for the continuous Gaussian; the sampled and truncated kernel of the implementation is an approximation of it.

**Lemma 1 (blur levels).** Let $G_\sigma$ be the Gaussian of standard deviation $\sigma$. Then $G_a \ast G_b = G_{\sqrt{a^2 + b^2}}$. Hence, if level $i - 1$ has blur $\sigma_{i-1}$ and line L1 blurs it by $\sqrt{\sigma_i^2 - \sigma_{i-1}^2}$, level $i$ has blur $\sigma_i = \sigma_0 2^{i/s}$. If the input has blur $0.5$ and the first blur is $\sqrt{\sigma_0^2 - 0.5^2}$, level $0$ has blur $\sigma_0$.

*Proof.* The Fourier transform of $G_\sigma$ is $e^{-\sigma^2 |\omega|^2 / 2}$. Convolution multiplies the transforms, and $e^{-a^2|\omega|^2/2} e^{-b^2|\omega|^2/2} = e^{-(a^2 + b^2)|\omega|^2/2}$. Apply this once per level, by induction on $i$. $\square$

**Lemma 2 (octaves).** Level $s$ of octave $o$ has blur $\sigma_0 2^{s/s} = 2\sigma_0$ in the pixel units of octave $o$. Taking every second pixel doubles the unit length, so the same image has blur $\sigma_0$ in the units of octave $o + 1$, which is the blur that level $0$ of an octave must have. A blur of $\sigma$ in octave $o$ is a blur of $2^o \sigma$ in image pixels.

*Proof.* A Gaussian of standard deviation $2\sigma_0$ in a unit $u$ is a Gaussian of standard deviation $\sigma_0$ in the unit $2u$. By induction on $o$, a unit of octave $o$ is $2^o$ image pixels. $\square$

**Lemma 3 (extrema).** Line L4 accepts a sample exactly when its value is strictly larger than each of its 26 neighbours, or strictly smaller than each.

*Proof.* The implementation keeps two flags, "larger than all so far" and "smaller than all so far". It clears the first when a neighbour is $\ge$ the value and the second when a neighbour is $\le$ the value, and it accepts when a flag is still set after all 26 neighbours. It stops early only when both flags are clear, and then the sample is rejected in either case. $\square$

**Lemma 4 (quadratic fit).** Suppose that near a sample $D$ is a quadratic, $D(z) = c + g^{\mathsf T} z + \frac{1}{2} z^{\mathsf T} H z$ in the offset $z \in \mathbb{R}^3$ from the sample. Then the central differences of line L5 return exactly $g$ and $H$. If $H$ is nonsingular, $z^* = -H^{-1} g$ is the only stationary point of $D$, and $D(z^*) = c + \frac{1}{2} g^{\mathsf T} z^*$.

*Proof.* Along axis $a$, $D(\pm e_a) = c \pm g_a + \frac{1}{2} H_{aa}$, so $(D(e_a) - D(-e_a))/2 = g_a$ and $D(e_a) - 2c + D(-e_a) = H_{aa}$. For two axes $a \ne b$, $D(\pm e_a \pm e_b) = c + (\pm g_a \pm g_b) + \frac{1}{2}(H_{aa} + H_{bb}) + (\pm 1)(\pm 1) H_{ab}$, and the combination $(D(e_a + e_b) - D(e_a - e_b) - D(-e_a + e_b) + D(-e_a - e_b))/4$ cancels every term except $H_{ab}$. The gradient of $D$ is $g + Hz$, which is zero only at $z^*$ when $H$ is nonsingular. Finally $D(z^*) = c + g^{\mathsf T} z^* + \frac{1}{2} z^{*\mathsf T} H z^* = c + g^{\mathsf T} z^* - \frac{1}{2} z^{*\mathsf T} g = c + \frac{1}{2} g^{\mathsf T} z^*$, using $H z^* = -g$ and the symmetry of $H$. The implementation solves $Hz = -g$ by Cramer's rule, which is exact for exact input. $\square$

If $D$ is not a quadratic, line L5 returns the extremum of the quadratic with the measured differences, which is the model of Lowe and Brown. Each move at line L5 changes the sample, and the loop stops after at most 5 moves, so line L5 ends.

**Lemma 5 (edge test).** Let $\alpha$ and $\beta$ be the eigenvalues of the symmetric matrix $H_{xy}$, with $|\alpha| \ge |\beta|$, and let $r > 1$. The test of line L6 passes, that is $\det H_{xy} > 0$ and $r (\operatorname{tr} H_{xy})^2 < (r + 1)^2 \det H_{xy}$, exactly when $\alpha$ and $\beta$ have the same sign and $\alpha / \beta < r$.

*Proof.* $\det = \alpha\beta$ and $\operatorname{tr} = \alpha + \beta$. If $\det \le 0$ the test fails, and the eigenvalues are not of the same strict sign. If $\det > 0$, put $\rho = \alpha/\beta \ge 1$. Then $\operatorname{tr}^2/\det = (\rho + 1)^2/\rho = \rho + 2 + 1/\rho$, whose derivative $1 - 1/\rho^2$ is positive for $\rho > 1$. So the map is strictly increasing on $[1, \infty)$, and $(\rho + 1)^2/\rho < (r + 1)^2/r$ holds exactly when $\rho < r$. Multiplying by $r \det > 0$ gives the test. $\square$

**Lemma 6 (orientation peak).** Let $c$ be a bin value with neighbours $\ell$ and $\rho$, and $c > \ell$, $c > \rho$. The parabola through $(-1, \ell)$, $(0, c)$ and $(1, \rho)$ has its maximum at $\delta = \frac{1}{2}\frac{\ell - \rho}{\ell - 2c + \rho}$, and $|\delta| < \frac{1}{2}$.

*Proof.* The parabola is $p(t) = c + \frac{\rho - \ell}{2} t + \frac{\ell - 2c + \rho}{2} t^2$; check $p(-1) = \ell$, $p(0) = c$, $p(1) = \rho$. Its leading coefficient is negative because $\ell - 2c + \rho = -(a + b)$ with $a = c - \ell > 0$ and $b = c - \rho > 0$, so its stationary point $\delta = -\frac{\rho - \ell}{2(\ell - 2c + \rho)}$ is the maximum. In terms of $a$ and $b$, $\delta = \frac{1}{2}\frac{a - b}{a + b}$, and $|a - b| < a + b$. $\square$

So the refined angle lies within half a bin of the center of the peak bin.

**Lemma 7 (descriptor).** If the descriptor histogram $d$ is not zero, line L10 returns a unit vector. If every gradient is multiplied by a constant $c > 0$, for example because the image is replaced by $cI + b$, the result does not change.

*Proof.* After the first division $\lVert d \rVert = 1$. The clip keeps the vector nonzero: a nonzero entry $v$ becomes $\min(v, 0.2) > 0$. The second division gives norm $1$. Adding $b$ does not change any gradient. Multiplying the gradients by $c$ multiplies every magnitude, and so every histogram entry, by $c$, and it does not change any direction, so the bins and the interpolation weights are the same. The first division removes $c$, and the rest is the same computation. $\square$

**Lemma 8 (matching).** For each $a$, lines L11 and L12 with early abandoning end with $\mathit{best}$ and $\mathit{second}$ equal to the smallest and the second smallest squared distance from $a$ to the descriptors of $B$, and with $\mathit{arg}$ an index of a nearest one. Line L13 reports $(a, b_1)$ exactly when $\lVert a - b_1 \rVert < 0.8 \lVert a - b_2 \rVert$.

*Proof.* We use the invariant that after each candidate, $\mathit{best} \le \mathit{second}$ are the two smallest squared distances among the candidates seen so far, and $\mathit{arg}$ is the index of one with distance $\mathit{best}$. It holds at the start with both equal to $\infty$. For a candidate, the running sum is a sum of nonnegative terms, so it never decreases, and each partial sum is at most the full distance. If the loop stops early, the partial sum is $\ge \mathit{second}$, so the full distance is $\ge \mathit{second}$ too and the two smallest values do not change; the update then changes nothing, because the partial sum is neither $< \mathit{best}$ nor $< \mathit{second}$. If the loop does not stop, the sum is the full distance, and the update inserts it in the right place. At the end the invariant gives the claim. Since all distances are nonnegative, $\mathit{best} < 0.8^2 \cdot \mathit{second}$ is the same as $\sqrt{\mathit{best}} < 0.8 \sqrt{\mathit{second}}$. $\square$
