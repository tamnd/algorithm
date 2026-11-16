---
title: Correctness of the DAISY descriptor
proves: [correctness]
status: full
---

Pixels are $(u, v)$ with $u$ the column and $v$ the row. Let $g = (g_u, g_v)$ be the gradient at a pixel, $\theta_o = 2 \pi o / B$, and $G_o = (\cos \theta_o\, g_u + \sin \theta_o\, g_v)^+$ with $(a)^+ = \max(a, 0)$.

**Lemma 1 (orientation maps).** $G_o$ is the positive part of the derivative of $I$ in the direction $\theta_o$. When $B$ is even, $G_o$ and $G_{o + B/2}$ are never both positive, and $G_o - G_{o + B/2}$ is the directional derivative itself.

*Proof.* The derivative of $I$ in the unit direction $e = (\cos \theta_o, \sin \theta_o)$ is $e \cdot g$, which is the argument of the positive part. Since $\theta_{o + B/2} = \theta_o + \pi$, the direction of $G_{o + B/2}$ is $-e$, so its argument is $-e \cdot g$. For any real $a$, $a^+$ and $(-a)^+$ are not both positive and $a^+ - (-a)^+ = a$. $\square$

**Lemma 2 (incremental convolution).** Let $G_s$ be the Gaussian of standard deviation $s$ on the plane. For $0 \le \Sigma_1 < \Sigma_2$ and $\Sigma = \sqrt{\Sigma_2^2 - \Sigma_1^2}$, $G_\Sigma * (G_{\Sigma_1} * f) = G_{\Sigma_2} * f$ for every bounded $f$. So the layers of line L3 are the convolutions of the maps with $G_{\Sigma_i}$.

*Proof.* Convolution is associative, so it suffices that $G_\Sigma * G_{\Sigma_1} = G_{\Sigma_2}$. In one dimension the Gaussian of standard deviation $s$ is the density of a normal variable with variance $s^2$, and the density of the sum of two independent variables is the convolution of their densities; the sum of independent normal variables is normal with the sum of the variances, which is $\Sigma^2 + \Sigma_1^2 = \Sigma_2^2$. The plane Gaussian is the product of two such factors in $u$ and $v$, so the same holds in the plane. For $i = 0$ the step is the direct convolution with $G_{\Sigma_0}$, and induction on $i$ gives the claim for every layer. $\square$

In the code the kernels are sampled on the integers, cut at $\lceil 4 \sigma \rceil$ and scaled to sum 1, and the border pixels are repeated, so the identity of Lemma 2 is approximate. The tests check that the incremental and the direct layers agree to $10^{-3}$ of the largest value away from the border.

**Lemma 3 (kernels).** Each sampled kernel is symmetric and sums to 1, so a constant map is unchanged by the convolution, and the convolution of a nonnegative map is nonnegative.

*Proof.* The weights $e^{-x^2 / (2 \sigma^2)}$ for $x = -r, \dots, r$ are positive and depend only on $x^2$, and they are divided by their sum. A convolution with weights that sum to 1 maps a constant $c$ to $c$, also at the border, where the repeated pixels are equal to $c$. A sum of nonnegative values with positive weights is nonnegative. $\square$

**Lemma 4 (shape and unit histograms).** The descriptor has $1 + Q T$ histograms of $B$ values, and each histogram has unit Euclidean length unless all its values are 0.

*Proof.* Line L5 adds one histogram and line L6 adds one for each of the $Q$ rings and $T$ points, each with one value per map. By Lemma 3 the values are nonnegative. If a histogram $h$ is not 0, its length $n$ is positive and $h / n$ has length 1; if it is 0, it stays 0. $\square$

**Lemma 5 (offset and gain).** For a constant $c$, the image $I + c$ has the same descriptor as $I$. For a constant $a > 0$, the image $a I$ has the same descriptor as $I$.

*Proof.* The gradient is a difference of pixel values, so it does not change when $c$ is added to every pixel. For $a I$ the gradient is multiplied by $a$, and so are the maps, since $(a x)^+ = a x^+$ for $a > 0$. The convolutions and the bilinear reads are linear, so every histogram is multiplied by $a$, and $a h / \lVert a h \rVert = h / \lVert h \rVert$. $\square$

**Lemma 6 (a quarter turn).** Let $N$ be the side of a square image $I$ and $J(u', v') = I(v', N - 1 - u')$, so that the pixel $(u, v)$ of $I$ is the pixel $(N - 1 - v, u)$ of $J$. Let $B = T = 8$. Then the descriptor of $J$ at $(N - 1 - v, u)$ turned by $k = 2$ equals the descriptor of $I$ at $(u, v)$.

*Proof.* By the chain rule, and also for the central differences with repeated border pixels, the gradient of $J$ at the image of $p$ is $(-g_v, g_u)$, the gradient $g$ of $I$ at $p$ turned by $+\pi/2$. Then $\cos \theta_o (-g_v) + \sin \theta_o\, g_u = \cos(\theta_o - \pi/2)\, g_u + \sin(\theta_o - \pi/2)\, g_v$, so the map $o$ of $J$ is the map $o - 2$ of $I$, moved by the turn. The Gaussian kernels are symmetric, so the separable convolution with repeated borders commutes with the turn of the grid, and so does bilinear interpolation, including the clamp to the image. With $k = 2$ the code reads the map $o + 2$ of $J$, which is the map $o$ of $I$. The ring point $j$ is read at the angle $\theta_j + \pi/2$ around the image of $p$; an offset $r(\cos(\theta_j + \pi/2), \sin(\theta_j + \pi/2)) = r(-\sin \theta_j, \cos \theta_j)$ in $J$ is the offset $r(\cos \theta_j, \sin \theta_j)$ in $I$. So every read value is the same value of the same layer of $I$, and so is every histogram. $\square$

**Theorem.** The code returns, for each pixel of the grid, the vector $D(p)$ of $1 + Q T$ unit histograms of the convolved orientation maps, the center from the first layer and the ring $i$ from the layer $i$ at the radius $R (i + 1) / Q$. The descriptor does not change under an offset or a positive gain of the image, and a quarter turn of the image maps it to the turned descriptor of Lemma 6.

*Proof.* Lines L1 and L2 compute the maps of Lemma 1. Line L3 computes the layers by Lemma 2, up to the sampling of the kernels. Lines L4 to L7 read and scale the histograms at the points of the definition, which gives the shape of Lemma 4. Lemma 5 gives the invariance to an offset and a gain, and Lemma 6 the quarter turn. $\square$
