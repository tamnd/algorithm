---
title: Bluestein's algorithm computes the DFT of any length with three FFTs of length M, and has a first-order error bound
proves: [correctness, complexity, error-bound]
status: full
---

Let $R$ be a commutative ring, $n \ge 1$, and $\zeta \in R$ with $\zeta^{2n} = 1$ such that $\omega = \zeta^2$ is a principal $n$-th root of unity. Let $M$ be the least power of two with $M \ge 2n - 1$, and suppose $R$ has a principal $M$-th root of unity and $M$ is a unit in $R$. For an integer $m$ put $c_m = \zeta^{m^2}$; since $\zeta^{2n} = 1$, $c_m = \zeta^{m^2 \bmod 2n}$, which is the value of line L2, and $c_{-m} = c_m$. Each $c_m$ is a unit, with inverse $\zeta^{2n - (m^2 \bmod 2n)}$.

**Lemma 1 (the identity).** For all integers $j$ and $k$, $\omega^{jk} = c_j \, c_k \, c_{k-j}^{-1}$.

*Proof.* $j^2 + k^2 - (k - j)^2 = 2jk$, so $c_j c_k c_{k-j}^{-1} = \zeta^{j^2 + k^2 - (k-j)^2} = \zeta^{2jk} = \omega^{jk}$. $\square$

**Lemma 2 (the kernel).** After line L4, for every integer $d$ with $|d| < n$, $b[d \bmod M] = c_d^{-1}$, and $b[r] = 0$ for every other position $r$.

*Proof.* For $0 \le m < n$, line L4 writes $c_m^{-1}$ at $m$ and at $(M - m) \bmod M$, which is $d \bmod M$ for $d = m$ and $d = -m$; as $c_{-m} = c_m$, the value written is $c_d^{-1}$ in both cases. The positions $0, 1, \ldots, n - 1$ and $M - n + 1, \ldots, M - 1$ are distinct, because $M - n + 1 \ge n$ when $M \ge 2n - 1$. For $m = 0$ both writes go to position $0$ with the same value. No other position is written, and all start at $0$. $\square$

**Theorem 1 (forward).** BLUESTEIN$(x, \zeta)$ returns the DFT $X_k = \sum_{j=0}^{n-1} x_j \omega^{jk}$, $0 \le k < n$.

*Proof.* After line L3, $a_j = x_j c_j$ for $j < n$ and $a_j = 0$ for $n \le j < M$. Let $z = a \circledast b$ be the cyclic convolution of length $M$, $z_k = \sum_{j=0}^{M-1} a_j b[(k - j) \bmod M]$. Lines L5 to L7 compute $z$ exactly: by the [convolution theorem](/convolution-theorem/) over $R$, with the principal $M$-th root and $M$ a unit, $F_M^{-1}(F_M a \odot F_M b) = a \circledast b$, and the FFT and its inverse compute $F_M$ and $F_M^{-1}$ exactly in $R$ by the [FFT page](/fast-fourier-transform/). For $0 \le k < n$, only $j < n$ contribute, and then $d = k - j$ satisfies $|d| < n$, so by Lemma 2, $z_k = \sum_{j<n} x_j c_j c_{k-j}^{-1}$. By Lemma 1, line L8 gives $c_k z_k = \sum_{j<n} x_j \omega^{jk} = X_k$. $\square$

**Theorem 2 (inverse).** INVERSE-BLUESTEIN$(X, \zeta)$ returns the $x$ whose DFT is $X$, provided $n$ is a unit.

*Proof.* $\zeta^{-1}$ satisfies $(\zeta^{-1})^{2n} = 1$, and $(\zeta^{-1})^2 = \omega^{-1}$ is again a principal $n$-th root of unity: $(\omega^{-1})^n = 1$, and for $0 < i < n$, $\sum_k \omega^{-ik} = \sum_k \omega^{(n-i)k} = 0$ because $0 < n - i < n$. So by Theorem 1, line L10 returns $y_j = \sum_k X_k \omega^{-jk}$. By the inversion formula on the [DFT page](/discrete-fourier-transform/), $y_j = n x_j$, and line L11 divides by $n$. $\square$

**Operation count.** Line L3 does $n$ multiplications and line L8 does $n$; line L6 does $M$. Lines L2 and L4 form the chirp and copy its inverses, which the cost model counts apart like a table. Each of the two forward FFTs of length $M$ in line L5 uses $\frac{M}{2} \lg M$ multiplications and $M \lg M$ additions, and the inverse FFT of line L7 uses the same plus $M$ multiplications by $M^{-1}$. The total is $\frac{3}{2} M \lg M + 2M + 2n$ multiplications and $3 M \lg M$ additions. As $M$ is the least power of two $\ge 2n - 1$, $M < 2(2n - 1)$, so $M = \Theta(n)$ and the cost is $\Theta(n \log n)$; the extra space is the arrays of length $M$ and $n$.

**Theorem 3 (rounding error).** Work over $\mathbb{C}$ in floating point with unit roundoff $u$, and $\gamma_2 = 2u/(1 - 2u)$. Suppose (i) each computed chirp value satisfies $|\hat c_m - c_m| \le \mu$, and $\hat b_m = \overline{\hat c_m}$, which is exact; (ii) a complex multiplication satisfies $\mathrm{fl}(pq) = pq(1 + \epsilon)$ with $|\epsilon| \le \sqrt 2 \gamma_2$ (Higham, Section 3.6); (iii) the computed FFT of length $M$ satisfies $\lVert \mathrm{fl}(\mathrm{FFT}(v)) - F_M v \rVert_2 \le \varepsilon_M \lVert F_M v \rVert_2$, and the inverse FFT, done as an FFT with conjugate twiddles followed by the exact division by the power of two $M$, satisfies the same bound with $F_M^{-1}$; Higham's Theorem 24.2 gives $\varepsilon_M = \lg M \cdot \eta + O(u^2)$. Then, with $\beta = 2n - 1$,

$$\lVert \hat X - X \rVert_2 \le \beta \left(2\mu + 2\sqrt 2 \gamma_2 + (2 + \sqrt 2) \varepsilon_M\right) \lVert x \rVert_2 + (\mu + \sqrt 2 \gamma_2) \lVert X \rVert_2 + O(u^2).$$

*Proof.* All norms are Euclidean unless marked. Put $\delta = \mu + \sqrt 2 \gamma_2$, and recall $|c_m| = 1$, $\lVert F_M v \rVert_2 = \sqrt M \lVert v \rVert_2$ and $\lVert F_M^{-1} v \rVert_2 = \lVert v \rVert_2 / \sqrt M$. Terms of order $u^2$ are dropped throughout.

*Step 1 (line L3).* $|\hat a_j - a_j| \le |x_j| |\hat c_j - c_j| + \sqrt 2 \gamma_2 |x_j \hat c_j| \le \delta |x_j|$, so $\lVert \hat a - a \rVert \le \delta \lVert x \rVert$, and $\lVert a \rVert = \lVert x \rVert$.

*Step 2 (line L5, the kernel).* $b$ has $\beta$ nonzero entries of modulus $1$, so $\lVert B \rVert_\infty \le \lVert b \rVert_1 = \beta$ and $\lVert b \rVert_2 = \sqrt\beta$. Write $\hat B = F_M \hat b + e_2$. Then $\lVert F_M(\hat b - b) \rVert_\infty \le \lVert \hat b - b \rVert_1 \le \beta \mu$, and $\lVert e_2 \rVert_\infty \le \lVert e_2 \rVert_2 \le \varepsilon_M \sqrt M \sqrt \beta$. Since $M < 2\beta$, $\sqrt{M \beta} < \sqrt 2 \beta$, so $\lVert \hat B - B \rVert_\infty \le \beta(\mu + \sqrt 2 \varepsilon_M)$.

*Step 3 (line L5, the data).* Write $\hat A = F_M \hat a + e_1$ with $\lVert e_1 \rVert \le \varepsilon_M \sqrt M \lVert \hat a \rVert$. Then $\lVert \hat A - A \rVert \le \sqrt M \lVert \hat a - a \rVert + \lVert e_1 \rVert \le \sqrt M (\delta + \varepsilon_M) \lVert x \rVert$, and $\lVert A \rVert = \sqrt M \lVert x \rVert$.

*Step 4 (line L6).* With $P = A \odot B$ and $\hat P_r = \hat A_r \hat B_r (1 + \epsilon_r)$,

$$\hat P - P = (\hat A - A) \odot \hat B + A \odot (\hat B - B) + \epsilon \odot \hat A \odot \hat B,$$

so $\lVert \hat P - P \rVert \le \lVert \hat A - A \rVert \lVert \hat B \rVert_\infty + \lVert A \rVert \lVert \hat B - B \rVert_\infty + \sqrt 2 \gamma_2 \lVert \hat A \rVert \lVert \hat B \rVert_\infty \le \sqrt M \beta \lVert x \rVert \left(\delta + \mu + \sqrt 2 \gamma_2 + (1 + \sqrt 2) \varepsilon_M\right)$. Also $\lVert P \rVert \le \beta \sqrt M \lVert x \rVert$.

*Step 5 (line L7).* $\hat z = F_M^{-1} \hat P + e_3$ with $\lVert e_3 \rVert \le \varepsilon_M \lVert \hat P \rVert / \sqrt M \le \varepsilon_M \beta \lVert x \rVert$. Since $z = F_M^{-1} P$, $\lVert \hat z - z \rVert \le \lVert \hat P - P \rVert / \sqrt M + \lVert e_3 \rVert \le \beta \lVert x \rVert \left(2\mu + 2\sqrt 2 \gamma_2 + (2 + \sqrt 2) \varepsilon_M\right)$, using $\delta = \mu + \sqrt 2 \gamma_2$.

*Step 6 (line L8).* For $k < n$, $|\hat X_k - X_k| \le |\hat c_k \hat z_k - c_k z_k| + \sqrt 2 \gamma_2 |\hat c_k \hat z_k| \le |\hat z_k - z_k| + \delta |z_k|$, and $|z_k| = |X_k|$ because $X_k = c_k z_k$ with $|c_k| = 1$. Summing in the Euclidean norm over $k < n$ and using Step 5 gives the bound.

Finally $\lVert X \rVert_2 = \sqrt n \lVert x \rVert_2$ by Parseval's identity for $F_n$, and $\beta / \sqrt n < 2 \sqrt n$, so the relative error is at most $2\sqrt n \left(2\mu + 2\sqrt 2 \gamma_2 + (2 + \sqrt 2)\varepsilon_M\right) + \delta + O(u^2)$. $\blacksquare$
