---
title: Correctness of the Harris-Laplace detector
proves: [correctness]
status: full
---

We prove that lines L6 to L8 return exactly the points that pass the tests of line L7, that the normalized measures do not change under a magnification, so the selected points follow the size of the pattern, and that for a Gaussian blob the Laplacian selects the scale of the blob.

**Lemma 1 (the selection).** Lines L6 to L8 return exactly the triples $(u, v, \sigma_n)$ with $1 \le n \le K - 2$, $1 \le u \le W - 2$, $1 \le v \le H - 2$, such that $R_n(u, v) > \tau_H$, $R_n(u, v) > R_n(u + a, v + b)$ for the 8 offsets $(a, b) \ne (0, 0)$ in $\{-1, 0, 1\}^2$, $F_n(u, v) > \tau_L$, $F_n(u, v) > F_{n-1}(u, v)$ and $F_n(u, v) > F_{n+1}(u, v)$. Each such triple is returned once.

*Proof.* Line L6 visits each triple of the stated ranges exactly once, so all the neighbours in space and scale that line L7 reads exist. Line L7 evaluates the conjunction of the five conditions, and line L8 adds the triple exactly when the conjunction holds. No other line adds to the list. $\square$

For the next two results we work in the continuous plane, with exact Gaussians and exact derivatives. Write $g_\sigma$ for the Gaussian of standard deviation $\sigma$ in two variables and $L(\cdot, \sigma) = g_\sigma \ast I$.

**Lemma 2 (magnification).** Let $f > 0$ and $I'(\mathbf x) = I(\mathbf x / f)$. Then $L'(f\mathbf x, f\sigma) = L(\mathbf x, \sigma)$, and with $\sigma_I' = f\sigma_I$ and $\sigma_D' = f\sigma_D$:

$$\mu'(f\mathbf x) = \mu(\mathbf x), \qquad R'(f\mathbf x) = R(\mathbf x), \qquad F'(f\mathbf x, f\sigma) = F(\mathbf x, \sigma).$$

*Proof.* $g_{f\sigma}(f\mathbf y) = f^{-2} g_\sigma(\mathbf y)$. Substituting $\mathbf y' = f\mathbf y$ in $L'(f\mathbf x, f\sigma) = \int g_{f\sigma}(f\mathbf x - \mathbf y')\, I(\mathbf y' / f)\, d\mathbf y'$ gives $d\mathbf y' = f^2 d\mathbf y$, and the factors $f^{-2}$ and $f^2$ cancel, so $L'(f\mathbf x, f\sigma) = L(\mathbf x, \sigma)$.

Each derivative in the new coordinates is $1/f$ times the derivative in the old ones, so $L'_x(f\mathbf x, f\sigma_D) = f^{-1} L_x(\mathbf x, \sigma_D)$, and in the same way for $L_y$. Each product of two first derivatives gains the factor $f^{-2}$, and $\sigma_D'^2 = f^2 \sigma_D^2$ removes it. The Gaussian sum with $g_{f\sigma_I}$ of a function $h'(\mathbf y') = h(\mathbf y' / f)$ at $f\mathbf x$ is, by the same substitution, the Gaussian sum with $g_{\sigma_I}$ of $h$ at $\mathbf x$. So each entry of $\mu'$ at $f\mathbf x$ equals the entry of $\mu$ at $\mathbf x$. Then $\det$ and $\operatorname{tr}$ agree, and so does $R$.

For $F$, each second derivative gains $f^{-2}$, and $(f\sigma)^2 = f^2\sigma^2$ removes it. $\square$

So if $(\mathbf x, \sigma_n)$ passes the tests of line L7 for $I$, with the conditions read in the continuous plane and the neighbours taken at the scaled positions, then $(f\mathbf x, f\sigma_n)$ passes them for $I'$ with the scales $f\sigma_0 \xi^n$, and the reverse holds with $1/f$. The thresholds compare values that are equal on both sides. On the grid and with a fixed list of scales this holds only up to sampling.

**Proposition 3 (the scale of a Gaussian blob).** Let $I(\mathbf x) = \exp(-|\mathbf x|^2 / (2\sigma_b^2))$. Then $F(\mathbf 0, \sigma) = 2 t t_0 / (t_0 + t)^2$ with $t = \sigma^2$ and $t_0 = \sigma_b^2$, and as a function of $\sigma > 0$ it has a single maximum, at $\sigma = \sigma_b$, with the value $\frac12$.

*Proof.* $I = 2\pi t_0\, g$ where $g$ is the Gaussian of variance $t_0$, and Gaussians add their variances, so $L(\mathbf x, \sigma) = \frac{t_0}{t_0 + t} \exp\!\big(-|\mathbf x|^2 / (2(t_0 + t))\big)$. For $c\exp(-|\mathbf x|^2 / (2T))$ the Laplacian at $\mathbf 0$ is $-2c/T$. So $L_{xx} + L_{yy} = -2t_0 / (t_0 + t)^2$ at $\mathbf 0$, and $F(\mathbf 0, \sigma) = t \cdot 2t_0 / (t_0 + t)^2$. Let $\psi(t) = \log t - 2\log(t_0 + t)$. Then $\psi'(t) = 1/t - 2/(t_0 + t) = (t_0 - t) / (t (t_0 + t))$, which is positive for $t < t_0$, zero at $t = t_0$ and negative for $t > t_0$. Since $\sigma \mapsto \sigma^2$ is increasing, the single maximum over $\sigma$ is at $\sigma = \sigma_b$, where $F = 2t_0^2 / (2t_0)^2 = \frac12$. $\square$

So if $\sigma_b = \sigma_n$ for some $1 \le n \le K - 2$, then $F_n(\mathbf 0) > F_{n-1}(\mathbf 0)$ and $F_n(\mathbf 0) > F_{n+1}(\mathbf 0)$, and the Laplacian test of line L7 at the center selects exactly the scale $\sigma_n$ of the blob.

**Theorem.** HARRIS-LAPLACE returns exactly the points $(u, v, \sigma_n)$ that are strict spatial maxima of the scale-adapted Harris measure above $\tau_H$ and strict maxima over scale of the normalized Laplacian above $\tau_L$, and in the continuous setting the set of these points is covariant with a magnification of the image.

*Proof.* Line L1 sets the scales $\sigma_n = \sigma_0 \xi^n$. Lines L2 and L3 compute $\mu_n$ and $R_n$ from their definitions with $\sigma_I = \sigma_n$ and $\sigma_D = s\sigma_n$, and line L4 computes $F_n$. Line L5 starts with an empty list. By Lemma 1, lines L6 to L8 add exactly the points with the stated properties, each once, and line L9 returns them. By Lemma 2, under a magnification by $f$ the values $R$ and $F$ at $(f\mathbf x, f\sigma)$ equal those at $(\mathbf x, \sigma)$, so each test of line L7 has the same outcome at the two points, and the returned sets correspond by $(\mathbf x, \sigma) \mapsto (f\mathbf x, f\sigma)$. $\blacksquare$
