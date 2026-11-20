---
title: For one isolated scatterer per range bin, one PGA iteration recovers the phase error exactly up to a constant and a linear term
proves: [correctness]
status: full
---

PGA as a whole is a heuristic: for images with clutter there is no theorem that its iterations converge to the true phase error, and its accuracy there is a measurement, given on the main page. We prove three exact facts about one iteration as written on the main page (lines L1 to L5): the part of the error that cannot be found, the effect of the center shift, and exact recovery for isolated scatterers.

**Setting.** Indices are taken mod $N$ and $c = N/2$. The DFT is $X(k) = \sum_j x[j] e^{-i 2\pi k j/N}$ and $\text{IDFT}$ is its inverse. The image rows are $g_m = \text{IDFT}(F_m e^{i\phi})$ with the focused histories $F_m$ and a phase error $\phi$ common to all rows. Let $b = \text{IDFT}(e^{i\phi})$, the blur of a point. $\text{wrap}(t)$ is the representative of $t$ mod $2\pi$ in $(-\pi, \pi]$.

**Theorem 1 (the part that cannot be found).** For real $a$ and an integer $s$, replacing $\phi(k)$ by $\phi(k) + a + 2\pi s k/N$ multiplies every row by $e^{ia}$ and shifts it circularly by $s$ pixels.

*Proof.* $\text{IDFT}(X e^{i 2\pi s k/N})[j] = x[j + s]$ by the shift theorem of the DFT, and the constant $e^{ia}$ factors out. $\square$

So no method that uses only the image can tell $\phi$ from $\phi + a + 2\pi s k/N$ when the scene is unknown, and PGA reports $\hat\phi$ with its best line removed.

**Theorem 2 (the center shift lines up isolated scatterers).** Let row $m$ hold one scatterer, $F_m(k) = \alpha_m e^{-i 2\pi k p_m/N}$ with $\alpha_m \ne 0$, and let $|b|$ have a unique largest value at the index $j^*$. Then after L1, $s_m[j] = \alpha_m\, b[j + j^* - c]$ for every $m$, so every row is the same blur times its own amplitude, peaking at $c$.

*Proof.* $g_m = \text{IDFT}(\alpha_m e^{-i 2\pi k p_m/N} e^{i\phi})$, so by the shift theorem $g_m[j] = \alpha_m b[j - p_m]$. Its largest modulus is at $j_m = p_m + j^*$, a unique index because $|b|$ has a unique maximum. L1 gives $s_m[j] = g_m[j + j_m - c] = \alpha_m b[j + j^* - c]$. $\square$

**Theorem 3 (exact recovery).** Under the hypotheses of Theorem 2, let the window of L2 keep whole rows, and let the differences $\delta(k) = \phi(k) - \phi(k - 1)$, $k = 1, \ldots, N - 1$, all lie in an open interval of length $\pi$. Then the estimate of L5 satisfies $\hat\phi(k) = \phi(k) - \bar a - \bar b k$ for real numbers $\bar a$, $\bar b$, that is, one iteration finds $\phi$ up to a constant and a linear term.

*Proof.* With $d = c - j^*$, Theorem 2 and the shift theorem give $h_m(k) = \text{DFT}(s_m)(k) = \alpha_m e^{i\phi(k)} e^{-i 2\pi k d/N}$. Hence $h_m[k]\, \overline{h_m[k - 1]} = |\alpha_m|^2 e^{i(\delta(k) - 2\pi d/N)}$, and the sum over $m$ is $\big(\sum_m |\alpha_m|^2\big) e^{i(\delta(k) - 2\pi d/N)}$ with a positive factor, so L4 gives $\Delta(k) \equiv \delta(k) - 2\pi d/N \pmod{2\pi}$. Let $\theta$ be the circular mean of the $\delta(k)$, the argument of $\sum_k e^{i\delta(k)}$. All $e^{i\delta(k)}$ lie on an open half circle, so the sum is not zero and $\theta$ can be taken in the same open interval of length $\pi$; therefore $|\delta(k) - \theta| < \pi$ for every $k$. The circular mean of the $\Delta(k)$ is $\psi \equiv \theta - 2\pi d/N$, so $\Delta(k) - \psi \equiv \delta(k) - \theta$, and since $|\delta(k) - \theta| < \pi$, $\text{wrap}(\Delta(k) - \psi) = \delta(k) - \theta$ exactly. Summing from 1 to $k$ gives $\phi(k) - \phi(0) - k\theta$, which is $\phi$ minus a constant and a linear term. Removing the best line changes it by another constant and linear term. $\square$

By Theorem 1 this is all that can be recovered. With clutter, each row of L4 adds noise to $|\alpha_m|^2 e^{i(\delta(k) - 2\pi d_m/N)}$ and the shift $d_m$ may differ between rows when the brightest pixel is not the scatterer; the sum over rows averages the noise, which is why the method works well in measurements, but this is not a theorem.

**Cost.** One iteration does $M$ shifts and windows in $O(M N)$, $M$ DFTs and $M$ inverse DFTs in $O(M N \log N)$ with an FFT, and the sums of L4 and L5 in $O(M N)$. With $I$ iterations the total is $O(I M N \log N)$ in the real-RAM model, with $O(M N)$ extra space.
