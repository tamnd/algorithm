---
title: NCC-MATCH computes the correlation coefficient at every offset, the score is in [-1, 1], and it does not change under a positive gain and an offset
proves: [correctness]
status: full
---

Fix an offset $(u, v)$ with $0 \le u \le W - p$ and $0 \le v \le H - q$. Write the window and the template as vectors $a, b \in \mathbb{R}^n$ with $n = pq$, in the same order of the pairs $(i, j)$: $a_k = f(u + i, v + j)$ and $b_k = t(i, j)$. Let $\bar a = \frac{1}{n}\sum a_k$, $\bar b = \frac{1}{n}\sum b_k$, and let $a' = a - \bar a \mathbf{1}$ and $b' = b - \bar b \mathbf{1}$ be the centered vectors. The definition is $\gamma = \langle a', b' \rangle / (\lVert a' \rVert \, \lVert b' \rVert)$ when both norms are positive.

**Lemma 1 (the parts).** With $F = \sum a_k$, $F_2 = \sum a_k^2$, $T = \sum b_k$, $T_2 = \sum b_k^2$ and $C = \sum a_k b_k$,

$$n\langle a', b' \rangle = nC - FT, \qquad n\lVert a' \rVert^2 = nF_2 - F^2, \qquad n\lVert b' \rVert^2 = nT_2 - T^2.$$

*Proof.* Expand: $\langle a', b' \rangle = \sum a_k b_k - \bar b \sum a_k - \bar a \sum b_k + n \bar a \bar b = C - FT/n - FT/n + FT/n = C - FT/n$. Multiply by $n$. The other two are the case $b = a$ and the case $a = b$. $\square$

**Lemma 2 (the sums).** At line L6, $F$ and $F_2$ are the sums of $f$ and of $f^2$ over the window. At line L7, $C = \sum_{i,j} f(u + i, v + j) t(i, j)$. If line L11 is used instead, its value at $(u, v)$ is the same $C$ in exact arithmetic.

*Proof.* The integral image page proves that RECT-SUM on the table of a function returns the sum of that function over the rectangle; apply it to $f$ and to $f^2$. Line L7 is the definition of $C$. For line L11, let $\tilde f$ and $\tilde t$ be the padded arrays of size $W' \times H'$. By the convolution theorem, the inverse DFT of $\hat{\tilde f} \cdot \overline{\hat{\tilde t}}$ at $(u, v)$ is

$$\sum_{j=0}^{H'-1} \sum_{i=0}^{W'-1} \tilde f((u + i) \bmod W', (v + j) \bmod H') \, \tilde t(i, j).$$

The factor $\tilde t(i, j)$ is zero unless $i < p$ and $j < q$. For those terms $u + i \le (W - p) + (p - 1) = W - 1 < W'$ and likewise $v + j \le H - 1 < H'$, so the mod does nothing and $\tilde f$ reads the true pixel $f(u + i, v + j)$. The sum is therefore $C$, and it is real, so taking the real part changes nothing. $\square$

**Theorem 1.** If $v_t > 0$, then for each offset line L9 sets $\gamma[v][u]$ to the defined score when the window is not flat and to undefined when it is flat, and line L10 returns an offset with the largest defined score. If $v_t = 0$, line L2 reports that no score is defined.

*Proof.* By Lemma 1, $v_t = n \lVert b' \rVert^2$, which is zero exactly when $b' = 0$, that is when the template is flat; then every score has a zero denominator, as line L2 reports. Otherwise, by Lemma 2 the values at line L8 are $\mathit{num} = nC - FT = n \langle a', b' \rangle$ and $v_f = n \lVert a' \rVert^2$. If $v_f = 0$, the window is flat and the score is undefined, as line L9 records. If $v_f > 0$,

$$\frac{\mathit{num}}{\sqrt{v_f v_t}} = \frac{n \langle a', b' \rangle}{\sqrt{n^2 \lVert a' \rVert^2 \lVert b' \rVert^2}} = \frac{\langle a', b' \rangle}{\lVert a' \rVert \, \lVert b' \rVert} = \gamma.$$

Line L10 scans all the entries, so it returns a largest one. $\square$

**Theorem 2 (range).** $-1 \le \gamma \le 1$. Also $\gamma = 1$ exactly when $a = \lambda b + \mu \mathbf{1}$ for some $\lambda > 0$ and some $\mu$, and $\gamma = -1$ exactly when this holds with $\lambda < 0$.

*Proof.* By the Cauchy-Schwarz inequality $|\langle a', b' \rangle| \le \lVert a' \rVert \, \lVert b' \rVert$, with equality exactly when $a' = \lambda b'$ for a real $\lambda$ (both vectors are nonzero). Equality with a plus sign needs $\lambda > 0$, and with a minus sign $\lambda < 0$. Finally $a' = \lambda b'$ is the same as $a = \lambda b + (\bar a - \lambda \bar b)\mathbf{1}$, and conversely $a = \lambda b + \mu\mathbf{1}$ gives $\bar a = \lambda \bar b + \mu$ and so $a' = \lambda b'$. $\square$

**Theorem 3 (gain and offset).** Let $g = \alpha f + \beta$ with $\alpha \ne 0$. At every offset, the score of $g$ against $t$ is $\operatorname{sign}(\alpha)$ times the score of $f$ against $t$, and a window of $g$ is flat exactly when the same window of $f$ is flat. The same holds for a change of the template.

*Proof.* The window of $g$ is $\alpha a + \beta \mathbf{1}$, whose mean is $\alpha \bar a + \beta$, so its centered vector is $\alpha a'$. Then $\langle \alpha a', b' \rangle = \alpha \langle a', b' \rangle$ and $\lVert \alpha a' \rVert = |\alpha| \lVert a' \rVert$, which is zero exactly when $a' = 0$. The quotient gains the factor $\alpha / |\alpha|$. The template case is the same with the roles swapped. $\square$

**Corollary.** For $\alpha > 0$, NCC-MATCH returns the same offset on $f$ and on $\alpha f + \beta$, because the whole score table is the same and line L10 uses a fixed tie rule.

**Exact order.** Let $\kappa = \mathit{num} \, |\mathit{num}| / (v_f v_t)$. Then $\kappa = \gamma |\gamma|$, and the map $x \mapsto x|x|$ is strictly increasing on $\mathbb{R}$. So $\kappa$ and $\gamma$ order the offsets in the same way, and the implementation can compare the rational numbers $\kappa$ instead of the rounded $\gamma$.
