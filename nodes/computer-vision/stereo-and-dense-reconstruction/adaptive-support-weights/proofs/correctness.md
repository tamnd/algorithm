---
title: Correctness of the adaptive support weight method
proves: [correctness]
status: full
---

Fix the images, $D$, $r$, $\gamma_c > 0$, $\gamma_p > 0$ and $T > 0$. For a left pixel $p = (u, v)$ and a disparity $d$ with $0 \le d \le \min(D - 1, u)$, let $\Omega(p, d)$ be the set of offsets $o$ with $|o_u|, |o_v| \le r$ such that $q = p + o$ is in the left image and $\bar q_d = q - (d, 0)$ is in the right image. We prove that ASW returns $d^*(p)$, the least disparity with the least value of

$$E(p, d) = \frac{\sum_{o \in \Omega(p, d)} \omega_o\, e(q, \bar q_d)}{\sum_{o \in \Omega(p, d)} \omega_o}, \qquad \omega_o = w(p, q)\, w(\bar p_d, \bar q_d).$$

## Lemma 1. The denominator is at least 1

The offset $o = (0, 0)$ is in $\Omega(p, d)$: $q = p$ is in the left image, and $\bar p_d = (u - d, v)$ is in the right image because $0 \le d \le u$ and the two images have the same size. For this offset $\Delta c = 0$ and $\Delta g = 0$ in both images, so $\omega_{(0,0)} = e^0 \cdot e^0 = 1$. Every other $\omega_o$ is a product of two exponentials and so is positive. Hence $\sum_{o} \omega_o \ge 1$, and line L7 never divides by zero. $\square$

The restriction $d \le u$ of line L2 is what makes this true: for $d > u$ the center pixel has no match in the right image, and the set $\Omega$ could be empty.

## Lemma 2. Lines L3 to L7 compute $E(p, d)$

Line L3 sets $\textit{num} = \textit{den} = 0$. The loop of line L4 visits each offset of the window once and skips exactly the offsets with $q$ outside the left image or $\bar q_d$ outside the right image, that is, it visits exactly $\Omega(p, d)$. In the code, an offset outside the left image has the weight `None` in the stored left weights of $p$, and an offset with $\bar q_d$ outside the right image has the weight `None` in the stored right weights of $\bar p_d$, because $\bar p_d + o = \bar q_d$. For a visited offset, line L5 forms $\omega_o$, and line L6 adds $\omega_o e(q, \bar q_d)$ to $\textit{num}$ and $\omega_o$ to $\textit{den}$. After the loop, by induction on the number of visited offsets, $\textit{num}$ and $\textit{den}$ are the two sums of the definition, and line L7 gives $E(p, d)$. $\square$

The stored weights are correct because $w(p, q)$ depends only on the left image, $p$ and $o$, and $w(\bar p_d, \bar q_d)$ only on the right image, $\bar p_d$ and $o$. Neither depends on $d$ except through the pixel $\bar p_d$, so one table of weights per pixel and image serves all disparities.

## Lemma 3. $0 \le E(p, d) \le T$

Put $\lambda_o = \omega_o / \sum_{o'} \omega_{o'}$. Then $\lambda_o > 0$ and $\sum_o \lambda_o = 1$, so $E(p, d) = \sum_o \lambda_o e(q, \bar q_d)$ is a convex combination of the raw costs. Each raw cost is a minimum of a sum of absolute values and $T$, so it lies in $[0, T]$, and so does every convex combination of them. $\square$

## Theorem. ASW returns $d^*(p)$

For each pixel, line L8 keeps the first disparity whose value is strictly less than all values before it. By the same invariant as for block matching, after the loop of line L2 this is the least $d$ in $[0, \min(D - 1, u)]$ with the least $E(p, d)$, using Lemma 2 for the values. The pixels are handled independently. $\square$

## The limit of uniform weights

As $\gamma_c \to \infty$ and $\gamma_p \to \infty$, each exponent tends to 0, so each $\omega_o$ tends to 1 and, the sums being finite, $E(p, d)$ tends to $\lvert \Omega(p, d) \rvert^{-1} \sum_{o} e(q, \bar q_d)$, the mean of the truncated costs over the window. Inside the image, where $\Omega(p, d)$ is the full window of $(2r + 1)^2$ offsets, this mean is a fixed multiple of the box sum of [block matching](/block-matching-stereo/) with the truncated cost, so the two methods choose the same disparities there. So adaptive support weights generalize box aggregation. $\square$

## Symmetry of the weights

$w(p, q) = w(q, p)$ for two pixels of the same image, because the Euclidean distances of colors and of positions are symmetric. The tests check this on random images.

## What is not proved

The theorem says that the code chooses the minimizer of $E$. That the minimizer is the true disparity near a depth edge depends on the assumption that a depth edge is also a color edge, which is a property of the scene and not a theorem. The tests show it on a synthetic scene where the assumption holds: near the edges of a red square on a blue background, the method makes no errors on the pixels that have a true match, while the box window with the same radius makes many.

## Exactness

The method uses $\exp$, square roots and divisions, so the code computes in floating point and is not exact. Two disparities whose values differ by less than the rounding error may be ordered wrongly. The model of the page is the real RAM, where these operations are exact.
