---
title: SINUSOIDAL-PE computes the formula, PE(pos + k) = M_k PE(pos) with a block rotation M_k that does not depend on pos, PE(p) . PE(p + k) depends only on k, and every PE vector has norm sqrt(d/2)
proves: [correctness]
status: full
---

We use the notation of the page. $d$ is even, $\omega_i = 10000^{-2i/d}$ for $i = 0, \ldots, d/2 - 1$, and the encoding is $\mathrm{PE}(pos)_{2i} = \sin(pos\, \omega_i)$, $\mathrm{PE}(pos)_{2i+1} = \cos(pos\, \omega_i)$, for any real $pos$.

**Lemma 1 (the procedure).** SINUSOIDAL-PE$(pos, d)$ returns $\mathrm{PE}(pos)$.

*Proof.* The loop at line L1 runs once for each $i = 0, \ldots, d/2 - 1$. Line L2 sets $\omega_i$, and lines L3 and L4 write coordinates $2i$ and $2i + 1$ by the formula. The pairs $\{2i, 2i + 1\}$ for different $i$ are disjoint and together are $\{0, \ldots, d - 1\}$, so every coordinate is written exactly once. Line L5 returns the vector. $\square$

For an angle $\theta$ let

$$R(\theta) = \begin{pmatrix} \cos\theta & \sin\theta \\ -\sin\theta & \cos\theta \end{pmatrix}, \qquad u_i(pos) = \begin{pmatrix} \sin(pos\, \omega_i) \\ \cos(pos\, \omega_i) \end{pmatrix},$$

so that $\mathrm{PE}(pos)$ is the stack of $u_0(pos), \ldots, u_{d/2-1}(pos)$. Let $M_k$ be the block-diagonal matrix with blocks $R(k\omega_0), \ldots, R(k\omega_{d/2-1})$.

**Theorem 2 (linear shift).** For all real $pos$ and $k$, $\mathrm{PE}(pos + k) = M_k\, \mathrm{PE}(pos)$.

*Proof.* Since $M_k$ is block diagonal, it suffices to show $u_i(pos + k) = R(k\omega_i)\, u_i(pos)$ for each $i$. Write $a = pos\,\omega_i$ and $b = k\omega_i$. The angle-sum formulas give

$$\sin(a + b) = \cos b \sin a + \sin b \cos a, \qquad \cos(a + b) = -\sin b \sin a + \cos b \cos a,$$

which are the two rows of $R(b)$ applied to $(\sin a, \cos a)^\top$. And $a + b = (pos + k)\omega_i$. $\square$

$M_k$ depends on $k$ and on the frequencies only, not on $pos$, which is the property stated in Section 3.5 of Vaswani and colleagues.

**Lemma 3 (rotation blocks).** $R(\theta)^\top R(\theta) = I$ and $R(\alpha) R(\beta) = R(\alpha + \beta)$. Hence $M_k^\top M_k = I$ and $M_k M_l = M_{k+l}$.

*Proof.* The columns of $R(\theta)$ are $(\cos\theta, -\sin\theta)$ and $(\sin\theta, \cos\theta)$; each has length $\sqrt{\cos^2\theta + \sin^2\theta} = 1$ and their dot product is $\cos\theta\sin\theta - \sin\theta\cos\theta = 0$. Multiplying out $R(\alpha) R(\beta)$ gives the entries $\cos\alpha\cos\beta - \sin\alpha\sin\beta = \cos(\alpha + \beta)$ and $\cos\alpha\sin\beta + \sin\alpha\cos\beta = \sin(\alpha + \beta)$ in the first row, and the second row follows in the same way. Block-diagonal matrices multiply block by block. $\square$

**Theorem 4 (distance in the dot product).** For all real $p$ and $k$,

$$\mathrm{PE}(p) \cdot \mathrm{PE}(p + k) = \sum_{i=0}^{d/2-1} \cos(k\omega_i), \qquad \lVert \mathrm{PE}(p) \rVert = \sqrt{d/2}.$$

*Proof.* For each $i$, $u_i(p) \cdot u_i(p + k) = \sin(p\omega_i)\sin((p + k)\omega_i) + \cos(p\omega_i)\cos((p + k)\omega_i) = \cos((p + k)\omega_i - p\omega_i) = \cos(k\omega_i)$ by the formula $\cos(x - y) = \cos x \cos y + \sin x \sin y$. Summing over $i$ gives the first claim. With $k = 0$ each term is $\cos 0 = 1$, so $\lVert \mathrm{PE}(p) \rVert^2 = d/2$. $\blacksquare$

The dot product in Theorem 4 is the one between two encoding vectors. In a transformer the score is taken after the linear maps $W^Q$ and $W^K$ of the sum of the token embedding and the encoding, and $(W^Q)^\top W^K$ is not in general a function of the rotations $M_k$, so the trained score is not a function of the offset alone. That is the gap that [rotary position embedding](/rotary-position-embedding/) closes.
