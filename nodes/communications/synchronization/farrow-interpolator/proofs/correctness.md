---
title: The cubic Farrow interpolator equals cubic Lagrange interpolation through four samples, with error at most (3/128) max |f''''|, and the parabolic form is exact for lines
proves: [correctness]
status: full
---

The input is $x[n] = f(n)$ on a grid of spacing $T_s = 1$. Line L1 takes the window $x[m - 1], x[m], x[m + 1], x[m + 2]$. Line L2 computes $c_i = \sum_{j=0}^{3} b_{ij}\,x[m - 1 + j]$ for $i = 0, \ldots, D$, and lines L3 to L5 compute $y = (\cdots(c_D\mu + c_{D-1})\mu + \cdots)\mu + c_0$ by Horner's rule. Lines L7 and L8 split an output time $t$ into $m = \lfloor t\rfloor$ and $\mu = t - m \in [0, 1)$.

**Lemma 1 (Horner's rule).** Lines L3 to L5 return $\sum_{i=0}^{D} c_i\mu^i$.

*Proof.* Let $y_r$ be the value after the step with index $i = D - r$, so $y_0 = c_D$. By induction, $y_r = \sum_{i=D-r}^{D} c_i\mu^{i-D+r}$: the step $y \leftarrow y\mu + c_{D-r-1}$ multiplies each term by $\mu$ and adds the next coefficient. After $r = D$ steps the sum is $\sum_{i=0}^{D} c_i\mu^i$. $\square$

**Theorem 1 (cubic Lagrange).** With the rows of `CUBIC_LAGRANGE`,
$$b = \begin{pmatrix} 0 & 1 & 0 & 0 \\ -\frac13 & -\frac12 & 1 & -\frac16 \\ \frac12 & -1 & \frac12 & 0 \\ -\frac16 & \frac12 & -\frac12 & \frac16 \end{pmatrix},$$
the output $y(\mu)$ is the unique polynomial of degree at most 3 that takes the values $x[m - 1], x[m], x[m + 1], x[m + 2]$ at $\mu = -1, 0, 1, 2$.

*Proof.* By Lemma 1, $y(\mu) = \sum_j x[m - 1 + j]\,\ell_j(\mu)$ with $\ell_j(\mu) = \sum_i b_{ij}\mu^i$. Column $j$ of $b$ holds the coefficients of the Lagrange basis polynomial for the node $j - 1$:
$\ell_0(\mu) = -\frac16\mu(\mu - 1)(\mu - 2) = -\frac13\mu + \frac12\mu^2 - \frac16\mu^3$,
$\ell_1(\mu) = \frac12(\mu + 1)(\mu - 1)(\mu - 2) = 1 - \frac12\mu - \mu^2 + \frac12\mu^3$,
$\ell_2(\mu) = -\frac12(\mu + 1)\mu(\mu - 2) = \mu + \frac12\mu^2 - \frac12\mu^3$,
$\ell_3(\mu) = \frac16(\mu + 1)\mu(\mu - 1) = -\frac16\mu + \frac16\mu^3$.
Each $\ell_j$ is $1$ at its own node and $0$ at the other three, so $y$ takes the four sample values. A polynomial of degree at most 3 through four distinct points is unique, because the difference of two such polynomials has four roots. $\square$

**Corollary 1.** The output is exact when $f$ is a polynomial of degree at most 3. At $\mu = 0$ it returns $x[m]$, and the four weights sum to $1$ for every $\mu$.

**Theorem 2 (error bound).** If $f$ has four continuous derivatives on $[m - 1, m + 2]$ and $|f^{(4)}| \le M_4$ there, then for $0 \le \mu \le 1$,
$$|f(m + \mu) - y(\mu)| \le \frac{M_4}{24}\,|(\mu + 1)\mu(\mu - 1)(\mu - 2)| \le \frac{3}{128}M_4.$$

*Proof.* The first inequality is the standard remainder of [Lagrange interpolation](/lagrange-interpolation/): $f(m + \mu) - y(\mu) = \frac{f^{(4)}(\xi)}{4!}\prod_{j}(\mu - \mu_j)$ for some $\xi$ in the interval, with the nodes $\mu_j \in \{-1, 0, 1, 2\}$. For the second, put $v = \mu - \frac12 \in [-\frac12, \frac12]$. Then $(\mu + 1)(\mu - 2) = v^2 - \frac94$ and $\mu(\mu - 1) = v^2 - \frac14$, so the product is $(\frac94 - v^2)(\frac14 - v^2)$ in absolute value. Both factors are nonnegative and decrease in $v^2$, so the maximum is at $v = 0$: $\frac94\cdot\frac14 = \frac{9}{16}$. And $\frac{9}{16}\cdot\frac{1}{24} = \frac{3}{128}$. $\square$

For $f(t) = \cos(\omega t)$, $M_4 = \omega^4$. This is a theorem; how close the bound is for a given $f$ is a measurement, which the page reports.

**Theorem 3 (piecewise parabolic form).** With the rows $(0, 1, 0, 0)$, $(-\alpha, \alpha - 1, \alpha + 1, -\alpha)$ and $(\alpha, -\alpha, -\alpha, \alpha)$, for every $\alpha$, the output returns $x[m]$ at $\mu = 0$, a constant input gives the same constant, and a linear input $x[n] = p + qn$ gives $p + q(m + \mu)$ exactly. The output is continuous in $t$: the value at $\mu \to 1$ in window $m$ equals the value at $\mu = 0$ in window $m + 1$.

*Proof.* At $\mu = 0$, $y = c_0 = x[m]$. Rows 1 and 2 sum to zero, so a constant gives $c_1 = c_2 = 0$. For $x[n] = n$ around $m = 0$, $c_1 = \alpha + 0 + (\alpha + 1) - 2\alpha = 1$ and $c_2 = -\alpha - 0 - \alpha + 2\alpha = 0$, so $y = \mu$; linearity and a shift give the general line. At $\mu = 1$, $y = c_0 + c_1 + c_2 = x[m] + (-\alpha + \alpha)x[m - 1] + (\alpha - 1 - \alpha)x[m] + (\alpha + 1 - \alpha)x[m + 1] + (-\alpha + \alpha)x[m + 2] = x[m + 1]$, which is the value at $\mu = 0$ in the next window. $\square$

The parabolic form is not exact for a quadratic when $\alpha = \frac12$: for $x[n] = n^2$ at $\mu = \frac12$ the taps are $-\frac18, \frac58, \frac58, -\frac18$ on the values $1, 0, 1, 4$, and the output is $0$ instead of $\frac14$. Cubic Lagrange has the taps $-\frac{1}{16}, \frac{9}{16}, \frac{9}{16}, -\frac{1}{16}$ there and returns $\frac14$. Its value is a frequency response that Erup, Gardner and Harris chose for modems, with a cost of only two multiplications for $c_1$ and $c_2$ after shared additions. The tests check Theorem 1 against a direct Lagrange sum to $10^{-12}$, Corollary 1 on random cubics, Theorem 2 on a sinusoid, and Theorem 3.
