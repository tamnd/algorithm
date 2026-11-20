---
title: The least squares mismatched filter has the least integrated sidelobe level at unit peak, its signal to noise loss is at most one, and a longer filter is never worse
proves: [correctness]
status: full
---

The notation is that of the page. The code is $s[0], \dots, s[N-1]$, not all zero, and the filter is $h[0], \dots, h[L-1]$. The output is the linear convolution $y[m] = \sum_i h[i]\, s[m-i]$ for $m = 0, \dots, N + L - 2$, with $s[n] = 0$ outside $0 \le n \le N-1$. The peak index is $c$, with $0 \le c \le N + L - 2$. Write $y = Ch$ with the $(N+L-1) \times L$ matrix $C[m][i] = s[m-i]$, and let $d$ be the unit vector at index $c$. Line L1 gives $r[k] = \sum_n s[n+k]\,\overline{s[n]}$, line L2 the matrix $R$, and line L3 the vector $e$. We assume $e \ne 0$. This holds for every phase code, because every chip is nonzero and the index range $c - L + 1 \le c - i \le c$ meets $0, \dots, N-1$.

**Lemma 1 (the normal equations).** $C^H C = R$ and $C^H d = e$, so $y[c] = e^H h$ for every $h$.

*Proof.* $(C^H C)[i][j] = \sum_m \overline{s[m-i]}\, s[m-j]$. Put $n = m - i$: the sum is $\sum_n s[n + i - j]\,\overline{s[n]} = r[i-j]$ for $i \ge j$. For $i < j$ the same sum is $\overline{r[j-i]}$, and it is zero when $|i - j| \ge N$ because no $n$ has both $s[n]$ and $s[n + i - j]$ inside the code. This is line L2. Next, $(C^H d)[i] = \overline{C[c][i]} = \overline{s[c-i]}$, which is line L3. Last, $y[c] = (Ch)[c] = \sum_i s[c-i]\, h[i] = e^H h$. $\square$

**Lemma 2 ($R$ is positive definite).** For every $h \ne 0$, $h^H R h > 0$. So line L4 has exactly one solution $g$, and $q = e^H g = e^H R^{-1} e$ is real and positive.

*Proof.* By Lemma 1, $h^H R h = \|Ch\|^2 = \sum_m |y[m]|^2$. Let $i_0$ be the smallest index with $h[i_0] \ne 0$ and $n_0$ the smallest index with $s[n_0] \ne 0$. In $y[i_0 + n_0] = \sum_i h[i]\, s[i_0 + n_0 - i]$, a term with $i < i_0$ has $h[i] = 0$, and a term with $i > i_0$ has $s[\cdot] = 0$ because its index is below $n_0$. So $y[i_0 + n_0] = h[i_0]\, s[n_0] \ne 0$ and $\|Ch\|^2 > 0$. A positive definite matrix is invertible, its inverse is positive definite, and $e \ne 0$ gives $q = e^H R^{-1} e > 0$. $\square$

**Theorem 1 (least squares).** The vector $g$ of line L4 is the unique minimizer of $\|Ch - d\|^2$ over all $h$ of length $L$, and the minimum is $1 - q$.

*Proof.* With $Rg = e$ and Lemma 1, expand both sides of

$$\|Ch - d\|^2 = (h - g)^H R\, (h - g) + 1 - q.$$

The left side is $h^H R h - h^H e - e^H h + 1$. The right side is $h^H R h - h^H R g - g^H R h + g^H R g + 1 - q = h^H R h - h^H e - e^H h + g^H e + 1 - q$, and $g^H e = \overline{e^H g} = q$ because $q$ is real. So the two sides are equal. By Lemma 2 the first term on the right is positive unless $h = g$. $\square$

**Theorem 2 (least integrated sidelobe level).** Let $\mathrm{ISL}(h) = \sum_{m \ne c} |y[m]|^2 / |y[c]|^2$ for every $h$ with $y[c] \ne 0$. Then

$$\mathrm{ISL}(h) \ge \frac{1}{q} - 1,$$

with equality if and only if $h$ is a nonzero multiple of $g$. The filter $h = g/q$ returned by lines L5 and L6 has $y[c] = 1$ and $\mathrm{ISL} = 1/q - 1$.

*Proof.* By Lemma 1, $\mathrm{ISL}(h) = \|Ch\|^2/|y[c]|^2 - 1 = h^H R h / |e^H h|^2 - 1$. Lemma 2 makes $\langle u, v \rangle_R = u^H R v$ an inner product. Since $e = Rg$, $e^H h = g^H R h = \langle g, h \rangle_R$, and the Cauchy-Schwarz inequality gives $|e^H h|^2 \le \langle g, g \rangle_R \langle h, h\rangle_R = q\, h^H R h$. So $h^H R h / |e^H h|^2 \ge 1/q$, with equality exactly when $h$ and $g$ are proportional. Line L5 computes $p = e^H g = q$, and for $h = g/q$, $y[c] = e^H g / q = 1$. $\square$

So the least squares filter and the filter of least integrated sidelobe level at a fixed peak are the same filter up to scale. Neither statement says anything about the peak sidelobe level, which can be higher than that of the matched filter.

**Theorem 3 (signal to noise loss).** In white noise, the ratio of the output signal to noise ratio of $h$ at index $c$ to that of the matched filter is

$$\ell(h) = \frac{|y[c]|^2}{\|h\|^2\, \|s\|^2} \le 1,$$

with equality if and only if $h$ is a multiple of the code reversed in time and conjugated, padded with zeros, and the window $c - L + 1 \le n \le c$ holds every nonzero chip.

*Proof.* The noise at the output has variance $\sigma^2 \|h\|^2$, and the matched filter reaches $\|s\|^2/\sigma^2$, which gives the ratio. By the Cauchy-Schwarz inequality, $|y[c]|^2 = |\sum_i h[i]\, s[c-i]|^2 \le \|h\|^2 \sum_{i=0}^{L-1} |s[c-i]|^2 \le \|h\|^2 \|s\|^2$. The first step is an equality exactly when $h[i]$ is proportional to $\overline{s[c-i]}$. The second is an equality exactly when no nonzero chip falls outside the window. $\square$

**Theorem 4 (a longer filter is never worse).** Let $J(L, c)$ be the least integrated sidelobe level of Theorem 2. Then $J(L+1, c) \le J(L, c)$ and $J(L+1, c+1) \le J(L, c)$. With the default $c = \lfloor (N + L - 2)/2 \rfloor$, the least level is nonincreasing in $L$.

*Proof.* Let $h$ be optimal for $(L, c)$. The filter $(h[0], \dots, h[L-1], 0)$ of length $L + 1$ gives the same output followed by a zero, so its level at $c$ is $J(L, c)$. The filter $(0, h[0], \dots, h[L-1])$ gives the output delayed by one sample, so its level at $c+1$ is $J(L, c)$. The optimum for the longer length is at most the level of either filter. The default index for $L + 1$ is $\lfloor (N + L - 1)/2 \rfloor$, which is $c$ or $c + 1$, so one of the two cases applies. $\square$

**Exactness.** If the code has integer or rational chips, lines L1 to L6 use only additions, multiplications and divisions of rational numbers, and Gaussian elimination on the nonsingular matrix $R$ always finds a nonzero pivot. So the filter, its output and the values of Theorems 2 and 3 are exact rational numbers. The tests compare them with equality. $\square$
