---
title: Correctness of the determinant of Hessian detector
proves: [correctness]
status: full
---

We prove that line L4 returns the strict positive maxima, that the parabola step is exact on parabolas, that the normalized response is unchanged by a magnification, and that for a Gaussian blob the response selects the scale $t = t_0$.

**Lemma 1 (the maxima).** Line L4 returns exactly the samples $(u, v, i)$ with $2 \le i \le K - 1$, $u$ and $v$ at least one pixel from the border, $D_i(u, v) > \tau$, and $D_i(u, v) > D_{i'}(u', v')$ for each of the 26 neighbours.

*Proof.* The loops run over exactly these ranges of $i$, $u$ and $v$, so every neighbour is a valid sample. A sample with $D_i(u, v) \le \tau$ is skipped. For the others, the test "every neighbour is strictly smaller" is evaluated over the 26 offsets $(a, b, c) \ne (0, 0, 0)$ in $\{-1, 0, 1\}^3$, and the sample is added exactly when it holds. $\square$

**Lemma 2 (the parabola step).** If $f(x) = a - b(x - x_0)^2$ with $b > 0$, then the offset computed from $f(-1)$, $f(0)$, $f(1)$ is $x_0$.

*Proof.* $f(-1) - 2f(0) + f(1) = -2b < 0$, so the step does not return $0$ for a flat case, and $f(-1) - f(1) = -b\big((1 + x_0)^2 - (1 - x_0)^2\big) = -4b x_0$. The step returns $\frac12 \cdot \frac{-4b x_0}{-2b} = x_0$. $\square$

At a sample of Lemma 1 the center value is larger than both neighbours in each direction, so the denominator $f(-1) - 2f(0) + f(1)$ is negative and the offset is in $(-\frac12, \frac12)$; the fitted point stays within half a step of the sample.

**Lemma 3 (magnification).** Let $I'(\mathbf x) = I(\mathbf x / s)$ for $s > 0$, in the continuous setting. Then $D'(s\mathbf x, s^2 t) = D(\mathbf x, t)$.

*Proof.* A change of variables in the convolution gives $L'(s\mathbf x, s^2 t) = L(\mathbf x, t)$, because $g_{s^2 t}(s\mathbf y) = s^{-2} g_t(\mathbf y)$ and the area element scales by $s^2$. Each second derivative in $\mathbf x'$ is $s^{-2}$ times the one in $\mathbf x$, so $\det \mathcal H L'(s\mathbf x, s^2 t) = s^{-4} \det \mathcal H L(\mathbf x, t)$. The factor $(s^2 t)^2 = s^4 t^2$ cancels the $s^{-4}$. $\square$

So a maximum of $D$ at $(\mathbf x, t)$ becomes a maximum of $D'$ at $(s\mathbf x, s^2 t)$, with the same value: the selected scale follows the size of the pattern.

**Proposition 4 (the scale of a Gaussian blob).** Let $I(\mathbf x) = \exp(-|\mathbf x|^2 / (2 t_0))$ in the continuous plane. Then $D(\mathbf 0, t) = t_0^2 t^2 / (t_0 + t)^4$, and as a function of $t > 0$ it has a single maximum, at $t = t_0$, with the value $1/16$.

*Proof.* $I = 2\pi t_0\, g_{t_0}$, and Gaussians add their variances, so $L(\cdot, t) = 2\pi t_0\, g_{t_0 + t}$. For $g_T(\mathbf x) = \frac{1}{2\pi T} e^{-|\mathbf x|^2/(2T)}$, at $\mathbf x = \mathbf 0$ we have $\partial_{xx} g_T = \partial_{yy} g_T = -\frac{1}{2\pi T^2}$ and $\partial_{xy} g_T = 0$. So $\det \mathcal H L(\mathbf 0, t) = (2\pi t_0)^2 \cdot \frac{1}{4\pi^2 (t_0 + t)^4} = \frac{t_0^2}{(t_0 + t)^4}$, and $D = t_0^2 t^2 / (t_0 + t)^4$. Let $\psi(t) = \log D = 2\log t - 4\log(t_0 + t) + \text{const}$. Then $\psi'(t) = 2/t - 4/(t_0 + t)$, which is positive for $t < t_0$, zero at $t = t_0$ and negative for $t > t_0$. So $t_0$ is the single maximum, and $D(\mathbf 0, t_0) = t_0^4 / (2t_0)^4 = 1/16$. $\square$

**Theorem.** DOH returns, for each strict positive maximum of Lemma 1, the point refined by the three parabola steps, with the scale $\exp(\log t_i + \delta \cdot \frac12(\log t_{i+1} - \log t_{i-1}))$ for the offset $\delta$ in scale; and no other point.

*Proof.* Lines L1 and L2 fill the stack $D_1, \dots, D_K$. By Lemma 1, line L4 visits exactly the strict positive maxima. Line L5 computes three offsets as in Lemma 2 and maps the offset in scale to $\log t$ with the half spacing of the two neighbouring scales, which is the spacing when the ratio is constant. Line L6 adds one point per maximum, and nothing else adds points. $\blacksquare$
