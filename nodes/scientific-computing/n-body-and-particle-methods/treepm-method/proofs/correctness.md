---
title: The TreePM split is exact, the exact tree walk finds every close pair, and an accepted node has a relative error of order theta squared
proves: [correctness]
status: partial
---

We use exact arithmetic. The masses $m_i > 0$ are in the periodic unit square, the split scale is $r_s > 0$, and the cutoff is $r_{\text{cut}} = c \, r_s \le \frac12$. The exact force on particle $i$ is $F_i = -\sum_j \sum_{n \in \mathbb{Z}^2}' m_i m_j \frac{x_i - x_j + n}{|x_i - x_j + n|^2}$, where the prime omits $j = i$, $n = 0$; it is the force of the potential $m_i m_j \log r$ over all images, defined as the limit of the Ewald sums. For a displacement $z \ne 0$ write $K(z) = \frac{z}{|z|^2} e^{-|z|^2 / (4 r_s^2)}$, so the short-range force of $j$ on $i$ is $-m_i m_j K(z)$.

**Lemma 1 (the split).** Let $\alpha = 1 / (2 r_s)$. Then $e^{-k^2 / (4\alpha^2)} = e^{-k^2 r_s^2}$, and $F_i = F_i^{\text{short}} + F_i^{\text{long}}$, where $F_i^{\text{short}} = -\sum_j \sum_n' m_i m_j K(x_i - x_j + n)$ and $F_i^{\text{long}}$ is the force of the potential with the Fourier coefficients $\frac{2\pi}{k^2} e^{-k^2 r_s^2} S(k)$, $k \in 2\pi\mathbb{Z}^2 \setminus \{0\}$, $S(k) = \sum_j m_j e^{-i k \cdot x_j}$.

*Proof.* This is Lemma 1 of the [P3M proof](/p3m-method/) with $\alpha^2 = 1 / (4 r_s^2)$ and the sign of gravity: $\frac1r = \frac{e^{-\alpha^2 r^2}}{r} + \frac{1 - e^{-\alpha^2 r^2}}{r}$, the second term is the field of a Gaussian cloud of density $\frac{\alpha^2}{\pi} e^{-\alpha^2 |x|^2}$, and the Fourier transform of that cloud is $e^{-k^2 / (4\alpha^2)}$. $\square$

Line L1 approximates $F_i^{\text{long}}$ on the mesh. Lines L2 to L6 approximate $F_i^{\text{short}}$.

**Lemma 2 (pruning is safe).** Let a node be the square $B$ of side $s \le 1$ and center $c_B$, and let $b = (b_x, b_y)$ with $b_x = \max(0, |w(x_{i,x} - c_{B,x})| - s/2)$, where $w(t) = t - \mathrm{round}(t)$, and the same for $y$. For every point $p \in B$, the minimum image distance from $x_i$ to $p$ is at least $|b|$.

*Proof.* The periodic distance $|w(t)|$ on the circle of length 1 satisfies the triangle inequality, so $|w(x_{i,x} - p_x)| \ge |w(x_{i,x} - c_{B,x})| - |w(c_{B,x} - p_x)| \ge |w(x_{i,x} - c_{B,x})| - s/2$, and it is also $\ge 0$. So each component of the minimum image displacement is at least the corresponding component of $b$ in absolute value. $\square$

**Lemma 3 (the exact walk).** If $\theta = 0$, lines L3 to L6 add $-m_i m_j K(z)$ for every ordered pair $i \ne j$ whose minimum image displacement $z$ has $|z| < r_{\text{cut}}$, exactly once, and add nothing else.

*Proof.* The tree build puts each index into exactly one child, so the leaves partition the particles. With $\theta = 0$ the test $s^2 < \theta^2 d^2$ of line L6 never holds, so every node that is not pruned at line L4 is opened, and every leaf that is not pruned is summed at line L5. By Lemma 2, a pruned node holds no particle within $r_{\text{cut}}$ of $x_i$. Line L5 keeps exactly the particles $j \ne i$ with $|z| < r_{\text{cut}}$. Since $r_{\text{cut}} \le \frac12$, an image at distance below $r_{\text{cut}}$ is the minimum image, and it is unique, so no image is counted twice. $\square$

**Lemma 4 (the cutoff).** The images omitted by Lemma 3 change $F_i^{\text{short}}$ by at most $m_i \sum_j m_j \, \frac{e^{-c^2/4}}{r_{\text{cut}}} \, \gamma$, where $\gamma$ bounds the sum of the Gaussian tails over the lattice and tends to 1 as $c$ grows.

*Proof.* Each omitted image is at distance $r \ge r_{\text{cut}}$, and $|K| = e^{-r^2 / (4 r_s^2)} / r$ is decreasing, with the value $e^{-c^2/4} / r_{\text{cut}}$ at $r_{\text{cut}}$. The farther images of a pair are at distances $r_{\text{cut}} + t$ with $t$ growing like the lattice, so their sum is a convergent Gaussian series dominated by its first term. $\square$

**Lemma 5 (one accepted node).** Let a node hold the masses $m_j$ at $y_j$ in a square of side $s$, with total mass $M$ and center of mass $y_c$, and let $d = |x_i - y_c| > 0$ in the frame where all $y_j$ and $y_c$ are taken in one image. If $s < \theta d$ with $\theta < 1/\sqrt2$, then

$$\Big| \sum_j m_j K(x_i - y_j) - M K(x_i - y_c) \Big| \le \frac{C \, M \, \theta^2}{(1 - \sqrt2\,\theta)^3 \, d},$$

where $C$ is an absolute constant. Relative to the size $M / d$ of the node's Newtonian force, the error is $O(\theta^2)$.

*Proof.* Write $z = r_s w$. Then $K(z) = r_s^{-1} \frac{w}{|w|^2} e^{-|w|^2/4}$, and each second derivative of $K$ in $z$ is $r_s^{-3}$ times a sum of terms $|w|^{-3} P(|w|) e^{-|w|^2/4}$ with polynomials $P$. Since $u^k e^{-u^2/4}$ is bounded on $u \ge 0$ for each $k$, $\|D^2 K(z)\| \le C / |z|^3$. Expand $K(x_i - y_j)$ about $y_c$ with the Taylor formula with remainder. The constant terms give $M K(x_i - y_c)$; the linear terms give $DK \cdot \sum_j m_j (y_c - y_j) = 0$, by the definition of the center of mass. Both $y_j$ and $y_c$ lie in the square, so $|y_j - y_c| \le \sqrt2 s$, and every point of the segment between them is at distance at least $d - \sqrt2 s > (1 - \sqrt2\theta) d$ from $x_i$. The remainder is then at most $\frac12 \sum_j m_j \frac{C (\sqrt2 s)^2}{((1 - \sqrt2\theta) d)^3} = \frac{C M s^2}{((1 - \sqrt2\theta) d)^3}$, and $s < \theta d$ gives the bound. $\square$

**Theorem.** With exact arithmetic, the TreePM force on particle $i$ is $F_i + E_i^{\text{mesh}} + E_i^{\text{cut}} + E_i^{\text{tree}}$, where $E_i^{\text{mesh}}$ is the error of line L1 against $F_i^{\text{long}}$, $|E_i^{\text{cut}}|$ is bounded by Lemma 4, and $E_i^{\text{tree}}$ is the sum, over the nodes accepted at line L6, of the errors of Lemma 5. If $\theta = 0$, then $E_i^{\text{tree}} = 0$.

*Proof.* By Lemma 1, $F_i = F_i^{\text{short}} + F_i^{\text{long}}$. The walk visits disjoint sets of particles: an accepted node is not opened, and the leaves partition the particles. So the short-range output equals the exact cut-off sum of Lemma 3 plus, for each accepted node, the difference bounded in Lemma 5. Lemma 4 bounds the difference between the cut-off sum and $F_i^{\text{short}}$. $\square$

**Momentum.** If $\theta = 0$, the short-range part obeys Newton's third law pair by pair, because $K(-z) = -K(z)$ and Lemma 3 adds both ordered pairs. The mesh part sums to zero by Lemma 3 of the P3M proof, because the code uses the same TSC weights for assignment and interpolation, a real even filter and the zero derivative at the Nyquist index. So the total force is zero. If $\theta > 0$, the force of node $A$ on particle $i$ and the force of the node that contains $i$ on the particles of $A$ are not the same approximation, and the total force is not zero in general.

**What is not proved here.** We do not bound $E_i^{\text{mesh}}$. The mesh solver deconvolves the TSC assignment and interpolation by $\hat U^2$, which is not the optimal influence function, and its error depends on how fast $e^{-k^2 r_s^2}$ decays before the Nyquist wave number $\pi / h$, where it is $e^{-\pi^2 r_s^2 / h^2}$, and on aliasing. The page measures this error against an Ewald sum. Lemma 5 also assumes that the node and its center of mass are seen from $x_i$ in one image; the code takes the minimum image of the center of mass, which is the same thing when the node is small and far from the half-period distance.
