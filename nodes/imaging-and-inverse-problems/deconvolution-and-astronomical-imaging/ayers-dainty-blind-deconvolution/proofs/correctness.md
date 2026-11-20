---
title: Each Ayers-Dainty pass solves two regularized least squares problems, keeps the constraints, and has the true pair and the trivial pair as fixed points
proves: [correctness]
status: full
---

**Setting.** Images live on a periodic $n_1 \times n_2$ grid with $N = n_1 n_2$ pixels. The blur is $(h \ast f)(r) = \sum_s h(s) f(r - s)$ with indices taken modulo the grid, and the DFT is unnormalized, $\hat x(k) = \sum_r x(r) e^{-2\pi i\,k \cdot r/N'}$, where $k \cdot r / N'$ means $k_1 r_1/n_1 + k_2 r_2/n_2$. So $\widehat{h \ast f} = \hat h \hat f$ (the convolution theorem) and $\sum_k |\hat x(k)|^2 = N \sum_r |x(r)|^2$ (Parseval). The data are $y$ with $C = \hat y$. The constraint sets are

$$\mathcal F = \{f \text{ real} : f \ge 0,\ f = 0 \text{ outside } S_f\}, \qquad \mathcal H = \{h \text{ real} : h \ge 0,\ h = 0 \text{ outside } S_h,\ \textstyle\sum h = 1\}.$$

One pass of lines L4 to L7, with $\beta = 1$, maps $(f, h)$ to $(f', h')$:

$$\hat h_{\text{new}} = W(C, \hat f), \quad h' = P_{\mathcal H}\big(\mathcal F^{-1}\hat h_{\text{new}}\big), \quad \hat f_{\text{new}} = W(C, \hat h'), \quad f' = P_{\mathcal F}\big(\mathcal F^{-1}\hat f_{\text{new}}\big),$$

where $W(C, A)(k) = \overline{A(k)}\,C(k)/(|A(k)|^2 + \alpha)$, with $W = 0$ where the denominator is $0$. $P_{\mathcal F}$ takes the real part, sets negative values and values outside $S_f$ to $0$. $P_{\mathcal H}$ does the same with $S_h$ and then divides by the sum.

**Claim 1 (each Fourier step is a least squares fit).** Let $a$ and $y$ be real images and $\alpha > 0$. Then $b = \mathcal F^{-1} W(\hat y, \hat a)$ is real, and it is the unique minimizer over all images $b$ of

$$J(b) = \lVert y - a \ast b\rVert^2 + \alpha\lVert b\rVert^2.$$

With $\alpha = 0$, $b$ minimizes $\lVert y - a \ast b\rVert^2$, and it is the minimizer of least norm.

*Proof.* By the convolution theorem and Parseval, $N J(b) = \sum_k \big(|C(k) - A(k)B(k)|^2 + \alpha|B(k)|^2\big)$ with $A = \hat a$, $B = \hat b$, $C = \hat y$. The sum splits into one term per frequency. Each term is a strictly convex quadratic in the complex number $B(k)$ when $\alpha > 0$. Its derivative with respect to $\overline{B(k)}$ is $-\overline{A(k)}(C(k) - A(k)B(k)) + \alpha B(k)$, which is $0$ exactly at $B(k) = \overline{A(k)}C(k)/(|A(k)|^2 + \alpha)$. So $W$ gives the unique minimizer. Since $a$ and $y$ are real, $A(-k) = \overline{A(k)}$ and $C(-k) = \overline{C(k)}$, so $B(-k) = \overline{B(k)}$ and $b$ is real. With $\alpha = 0$ the term is $|C(k) - A(k)B(k)|^2$. Where $A(k) \ne 0$ it is $0$ only at $B(k) = C(k)/A(k)$, which is what $W$ gives. Where $A(k) = 0$ every $B(k)$ gives the same value, and $W$ picks $B(k) = 0$, which has the least modulus. By Parseval the least norm in the Fourier domain is the least norm in the image domain. $\square$

So line L4 fits the PSF to the data for the current object, and line L6 fits the object to the data for the current PSF. The fit ignores the constraints; the constraints come after.

**Claim 2 (the constraints hold after every pass).** For every input, $f' \in \mathcal F$. If the clipped PSF has a positive sum, $h' \in \mathcal H$; otherwise the code keeps the previous $h$, which is in $\mathcal H$ from the pass before (or from line L1).

*Proof.* $P_{\mathcal F}$ returns real values that are at least $0$ and are $0$ outside $S_f$, so its output is in $\mathcal F$. For the PSF, after the clip the values are real, at least $0$ and $0$ outside $S_h$. If their sum $s$ is positive, dividing by $s$ keeps these properties and makes the sum $1$. Line L1 applies the same maps to the start, with the delta PSF as the fallback, and the delta PSF is in $\mathcal H$ when $0 \in S_h$. $\square$

$P_{\mathcal F}$ is the Euclidean projection onto the closed convex cone $\mathcal F$ (each pixel is projected onto $[0, \infty)$ or onto $\{0\}$ on its own). The clip and divide of $P_{\mathcal H}$ is not the Euclidean projection onto $\mathcal H$, which would subtract a common constant before the clip. The method only needs a map into $\mathcal H$, and the scaling keeps the shape of the PSF.

**Claim 3 (the blind problem has exact ambiguities).** For every pair $(f, h)$, every integer shift $t$ and every $c > 0$, the pairs $(f(\cdot - t), h(\cdot + t))$ and $(cf, h/c)$ give the same data $h \ast f$. Inside $\mathcal H$ the scale is fixed. A shift survives when both shifted images still satisfy the support constraints.

*Proof.* $\sum_s h(s + t) f(r - s - t)$ is the sum for $h \ast f$ at $r$ after the change of index $s \to s + t$. The scale cancels in the product. $\sum h = 1$ fixes $c = 1$. $\square$

In one dimension there are many more ambiguities. Write the data, the object and the PSF as polynomials in $z$ (their $z$ transforms, with finite support). The data polynomial is the product of the other two. By the fundamental theorem of algebra it splits into linear factors, and each way to share these factors between two groups gives another pair with the same data. Positivity removes only some of these splits. In two dimensions a polynomial in two variables has, in general, no nontrivial factors, so the factorization is unique up to Claim 3. This is the reason why blind deconvolution is better posed for images than for signals; the implementation therefore works on images.

**Claim 4 (the true pair is a fixed point).** Let $\alpha = 0$, $y = h_0 \ast f_0$ with $f_0 \in \mathcal F$ and $h_0 \in \mathcal H$, and suppose that $\hat f_0(k) \ne 0$ and $\hat h_0(k) \ne 0$ for every $k$. Then one pass maps $(f_0, h_0)$ to itself.

*Proof.* $C = \hat h_0\hat f_0$. Line L4 gives $W(C, \hat f_0) = C/\hat f_0 = \hat h_0$ at every frequency, so the inverse DFT is $h_0$. It is real, at least $0$, $0$ outside $S_h$ and sums to $1$, so $P_{\mathcal H}$ leaves it unchanged. Line L6 gives $C/\hat h_0 = \hat f_0$, and $P_{\mathcal F}$ leaves $f_0$ unchanged. $\square$

**Claim 5 (the trivial pair is a fixed point, and it attracts the start $f = y$).** Let $\alpha = 0$, $y \in \mathcal F$, $0 \in S_h$ and $C(k) \ne 0$ for every $k$. Then the pair $(y, \delta)$, with $\delta$ the delta PSF, is a fixed point. Moreover, from the start $f = y$ and any start PSF, the first pass already returns $(y, \delta)$.

*Proof.* With $f = y$, line L4 gives $W(C, C) = C/C = 1$ at every frequency, whose inverse DFT is $\delta$, whatever $h$ was. $\delta \in \mathcal H$, so $h' = \delta$. Line L6 gives $W(C, 1) = C$, whose inverse DFT is $y \in \mathcal F$, so $f' = y$. $\square$

The trivial pair explains the warning that the start object must not be the data: the method then reports "no blur" and stops. With $\alpha > 0$ the pair moves a little, but the same pull is there.

**What is not proved.** A pass is two regularized least squares fits, each followed by a map onto a constraint set. Each fit uses the other unknown as fixed, and the map after it can undo part of the fit. The model $h \ast f$ is bilinear, so the set of pairs that fit the data is not convex, and the theory of alternating projections onto convex sets does not apply. No quantity is known to decrease along the passes, and there is no general convergence proof; the tests record a run where the misfit rises between passes. The tests check Claims 1 to 5 and record, as measurements, one run that recovers the true pair to $10^{-3}$ in 110 passes.
