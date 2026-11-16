---
title: Why one cross-correlation of feature maps scores every sub-window, why the logistic loss is a sound training target, and why bicubic upsampling can move the peak between grid nodes
proves: [correctness]
status: full
---

Notation as on the page. Siamese tracking as a whole is a heuristic: nothing proves that the maximum of the score map is on the target, because that depends on what the network learned. What can be proved is that the score map computes what the method says it computes, that the loss has the stated properties, and that the steps from the map to the new box are exact. The claims below do that.

## Claim 1: the score map equals the similarity of every translated sub-window

Let $\varphi$ be a stack of layers, each of the form

$$
y_c[p] = \sigma\Big( \sum_{c'} \sum_{q \in Q} K_{c c'}[q]\, x_{c'}[k p + q] + b_c \Big),
$$

where $Q$ is a finite window of offsets, $k \ge 1$ is the stride of the layer, $\sigma$ is applied point by point, and $p$ runs over the positions where $k p + q$ is inside the input for every $q \in Q$ (no padding). Let $k_\varphi$ be the product of the strides. For an exemplar $z$ and a search image $x$, let $x_\tau$ be the sub-window of $x$ with the size of $z$ whose top left corner is at $k_\varphi \tau$. Then for every position $\tau$ of the score map of line L6,

$$
\big(\varphi(z) \star \varphi(x) + b\big)[\tau] = \langle \varphi(z), \varphi(x_\tau) \rangle + b,
$$

where $\star$ is the cross-correlation summed over channels and $\langle \cdot, \cdot \rangle$ is the sum of all products of matching entries.

*Proof.* First one layer. Let $x' = x[\,\cdot + k \tau\,]$ be the input shifted by $k \tau$. Then $y'[p] = \sigma(\sum K[q]\, x[k p + k \tau + q] + b) = y[p + \tau]$, for every $p$ that is valid for $x'$; these $p + \tau$ are valid for $x$, because the window of $x'$ is inside $x$. So shifting the input by $k \tau$ shifts the output by $\tau$, and cutting a sub-window of the input cuts the matching sub-window of the output. By induction over the layers, a shift of $k_\varphi \tau$ at the input is a shift of $\tau$ at the output of $\varphi$, so $\varphi(x_\tau)$ is the part of $\varphi(x)$ that starts at $\tau$ and has the size of $\varphi(z)$. The cross-correlation at $\tau$ is $\sum_c \sum_a \varphi(z)_c[a]\, \varphi(x)_c[a + \tau]$, which is the inner product of $\varphi(z)$ with that part. $\square$

This is equation (1) of Bertinetto and colleagues, a function that commutes with translation by multiples of its stride, applied to the score. The test `test_score_map_equals_every_sub_window` checks it entry by entry with the fixed features of the implementation, where $k_\varphi = 1$.

**Why padding breaks it.** With zero padding, the output of $\varphi(x_\tau)$ near its border uses zeros, while the matching part of $\varphi(x)$ uses the real pixels around the sub-window. The two differ, so the map is no longer the similarity of the sub-windows. This is why the network has no padding.

**Translation of the search image.** A corollary: if the search image is shifted by $k_\varphi \tau$, the score map is shifted by $\tau$ on the positions where both maps are defined. The test `test_shift_of_the_search_image_shifts_the_score_map` checks this.

**Cost.** Scoring the $M$ sub-windows one by one costs $M$ evaluations of $\varphi$ on a window of the size of $z$. The cross-correlation costs one evaluation of $\varphi$ on $x$, in which every overlapping part is computed once, and $\Theta(C Z M)$ for the products, with $C$ channels and $Z$ cells in $\varphi(z)$.

## Claim 2: the logistic loss is convex, has the stated gradient, and rewards the right sign

For $y \in \{+1, -1\}$ and real $v$, $\ell(y, v) = \log(1 + e^{-y v})$ satisfies:

(a) $\ell(y, 0) = \log 2$ and $\ell(y, v) = \ell(-y, -v)$;

(b) $\partial \ell / \partial v = -y / (1 + e^{y v})$, which has the sign of $-y$ and absolute value below 1;

(c) $\partial^2 \ell / \partial v^2 = e^{y v} / (1 + e^{y v})^2 > 0$, so $\ell$ is strictly convex in $v$;

(d) $\ell$ is strictly decreasing in the margin $y v$, goes to 0 as $y v \to \infty$, and is at least $-y v$.

*Proof.* (a) is direct. (b) $\frac{d}{dv} \log(1 + e^{-y v}) = \frac{-y e^{-y v}}{1 + e^{-y v}} = \frac{-y}{e^{y v} + 1}$. (c) Differentiate again: $\frac{d}{dv} \frac{-y}{1 + e^{y v}} = \frac{y^2 e^{y v}}{(1 + e^{y v})^2}$ and $y^2 = 1$. (d) The function $m \mapsto \log(1 + e^{-m})$ has derivative $-1/(1 + e^m) < 0$, and $\log(1 + e^{-m}) \ge \log(e^{-m}) = -m$. $\square$

The map loss of line L2 is a weighted mean of such terms with positive weights, so it is also convex in the scores; with the balanced weights (half of the weight on the positive cells, half on the negative cells) it equals $\log 2$ when all scores are 0. The loss is convex in the scores, not in the weights of the network, so training finds a local minimum at best. The implementation computes $\ell$ as $m + \log(1 + e^{-m})$ for $m = -y v > 0$, the same value without overflow.

**The label map of line L1.** With stride $k$ and radius $R$, a cell $u$ is positive if $k |u - c| \le R$. For the $17 \times 17$ map, $k = 8$ and $R = 16$, the positive cells are the lattice points with $|u - c| \le 2$: the center, 4 at distance 1, 4 at distance $\sqrt 2$ and 4 at distance 2, so 13 cells. The test checks this count.

## Claim 3: bilinear upsampling cannot move the peak; bicubic upsampling can

(a) On a grid cell, the bilinear interpolant attains its maximum at a corner, so the maximum of a bilinear upsampling of a map is a value of the map at a node.

(b) With the cubic convolution kernel of Keys with $a = -\frac12$, the weights of the four taps at $-1, 0, 1, 2$ for a point $t \in [0, 1)$ are

$$
w_{-1} = -\tfrac12 t (1 - t)^2, \quad w_0 = \tfrac32 t^3 - \tfrac52 t^2 + 1, \quad w_1 = \tfrac12 t + 2 t^2 - \tfrac32 t^3, \quad w_2 = -\tfrac12 t^2 (1 - t),
$$

and they satisfy $\sum_d w_d = 1$, $\sum_d w_d\, d = t$, $\sum_d w_d\, d^2 = t^2$. So the interpolant is equal to the map at the nodes and reproduces every polynomial of degree at most 2 in each coordinate, away from the border where the taps are clamped.

*Proof.* (a) For fixed $b$, $f(a, b)$ is affine in $a$, so its maximum over $a \in [0, 1]$ is at $a = 0$ or $a = 1$. On each of those two edges $f$ is affine in $b$, so the maximum is at a corner. (b) The weights follow from $k(s) = \frac32 |s|^3 - \frac52 |s|^2 + 1$ for $|s| \le 1$ and $k(s) = -\frac12 |s|^3 + \frac52 |s|^2 - 4 |s| + 2$ for $1 < |s| < 2$, evaluated at $t + 1$, $t$, $1 - t$ and $2 - t$ and expanded. Adding the four polynomials, the coefficients of $t^3$, $t^2$ and $t$ cancel and the constant is 1. For the first moment, $-w_{-1} + w_1 + 2 w_2 = (\frac12 t - t^2 + \frac12 t^3) + (\frac12 t + 2 t^2 - \frac32 t^3) + (-t^2 + t^3) = t$. For the second, $w_{-1} + w_1 + 4 w_2 = (-\frac12 t + t^2 - \frac12 t^3) + (\frac12 t + 2 t^2 - \frac32 t^3) + (-2 t^2 + 2 t^3) = t^2$. At $t = 0$ the weights are $(0, 1, 0, 0)$, so nodes are kept. In two dimensions the interpolant is the product of two such one-dimensional rules, so it reproduces products of such polynomials. $\square$

So the bicubic map can have its maximum between nodes, which gives a position finer than one cell; the test `test_bicubic_upsampling_keeps_nodes_and_quadratics` checks the nodes, a quadratic and a peak that moves toward a large neighbor. That the finer position is closer to the truth is a heuristic: it holds when the score is smooth near its peak.

## Claim 4: the map position gives the displacement, and the scale update is a damped step

Let the search crop have $n_x$ cells per side and the exemplar crop $n_z$, both centered on the old position, with crop pixels of size $\rho$ image pixels, and let the score map be upsampled by the factor $U$ to positions $j / U$. A map position $j / U$ (in each coordinate) puts the exemplar window at search offset $k_\varphi j / U$, whose center is at $k_\varphi j / U + (n_z - 1) / 2$ in the crop, while the old center is at $(n_x - 1) / 2$. So the displacement of line L10 is

$$
d = \rho \Big( k_\varphi \frac{j}{U} - \frac{n_x - n_z}{2} \Big) = \rho\, k_\varphi \Big( \frac{j}{U} - c \Big), \qquad c = \frac{n_x - n_z}{2 k_\varphi},
$$

and $c$ is the center of the map when the map has $(n_x - n_z) / k_\varphi + 1$ cells per side. With $k_\varphi = 1$ this is the formula in the code.

For line L11, if the chosen scale factor is $s$ and the damping is $\gamma$, the size is multiplied by $(1 - \gamma) + \gamma s$, which lies between 1 and $s$. A constant true scale change $g$ per frame is then followed with a lag; the size never jumps by more than the largest scale factor in one frame. $\square$

## What is not claimed

The score map is a correct similarity of every sub-window, but nothing proves that the largest similarity is the target. A fixed embedding, like the gradient features of the implementation, gives high scores to any region with strong edges, as the example on the page shows. The learned embedding is trained to avoid this on the training videos, which is an empirical result. The cosine window and the scale penalty are heuristics that prefer small changes. The exemplar is never updated, so a target that changes its appearance can be lost.
