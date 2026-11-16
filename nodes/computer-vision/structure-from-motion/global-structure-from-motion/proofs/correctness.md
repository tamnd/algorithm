---
title: Global SfM recovers exact data up to a similarity when the view graph is parallel rigid
proves: [correctness]
status: full
---

We use the notation of the page and exact arithmetic, as in the real RAM model. The true cameras are $(R_k^*, t_k^*)$ with centers $c_k^* = -(R_k^*)^{\mathsf T} t_k^*$, the true points are $X_j^*$, and the observations are exact projections with positive depths. Index the images of the largest connected part of the view graph by $0, \dots, N - 1$, so image 0 is the first one. We assume:

- (G1) For every image pair that line L1 tests, the conditions of the eight-point method hold as in the proof of [incremental structure from motion](/incremental-structure-from-motion/): every 8 common tracks give a conditioned system with a null space of dimension 1, the two centers differ, and no point lies on the baseline.
- (G2) Let $M$ be the matrix of line L5 for the true directions, with the row and column blocks of $c_0$ removed. Its null space has dimension 1. This is the condition that the view graph with the true centers is parallel rigid.
- (G3) Each track that is triangulated is seen from two centers that do not lie on one line with its point.

**Claim.** (a) Each bundle adjustment returns a cost no larger than its start cost. (b) Under (G1) to (G3), the output is the truth after the similarity $X' = s R_0^* (X - c_0^*)$ with $s = 1 / (\sum_k \|c_k^* - c_0^*\|^2)^{1/2}$. That is, $R_k = R_k^* (R_0^*)^{\mathsf T}$, $c_k = s R_0^* (c_k^* - c_0^*)$, $t_k = -R_k c_k$ and $X_j = s R_0^* (X_j^* - c_0^*)$.

**Proof of (a).** Levenberg-Marquardt accepts a trial step only if it lowers the cost strictly, and otherwise raises the damping and tries again, so the cost never rises. $\square$

**Proof of (b).** *The target.* For each camera, $s (R_k^* X + t_k^*) = s R_k^* (X - c_k^*) = R_k^* (R_0^*)^{\mathsf T} \, s R_0^* \big((X - c_0^*) - (c_k^* - c_0^*)\big) = R_k (X' - c_k) = R_k X' + t_k$. The camera coordinates are scaled by $s > 0$, so the projections and the signs of the depths are the same. So the target explains the data, with $R_0 = I$ and $c_0 = 0$.

*Line L1.* By (G1) and the argument of the incremental proof, each edge $(i, j)$ gets the exact relative pose $R_{ij} = R_j^* (R_i^*)^{\mathsf T}$, $t_{ij} = \hat t_{ij} / \|\hat t_{ij}\|$, where $\hat t_{ij} = -R_j^* (c_j^* - c_i^*)$ is the true relative translation. All common tracks are inliers.

*Line L2.* The tree start chains $R_j = R_{ij} R_i$ from $R_0 = I$, which gives $R_k = R_k^* (R_0^*)^{\mathsf T}$ by induction on the depth in the tree. Then every residual $\log(R_j^{\mathsf T} R_{ij} R_i)$ is $\log I = 0$, for tree edges and other edges alike. So the right side $b$ of every Lie-algebraic step is 0, and since the grounded Laplacian of a connected graph with positive weights is invertible (see the proof of [Lie-algebraic rotation averaging](/lie-algebraic-rotation-averaging/)), the step is $\omega = 0$, with the $L_1$ weights and with the Geman-McClure weights. So line L2 returns $R_k = R_k^* (R_0^*)^{\mathsf T}$.

*Line L3.* Every edge has $R_j R_i^{\mathsf T} = R_j^* (R_i^*)^{\mathsf T} = R_{ij}$, so its angle is 0 and no edge is removed. The graph stays connected.

*Line L4.* For each edge,
$$v_{ij} = \frac{-R_j^{\mathsf T} \hat t_{ij}}{\|\hat t_{ij}\|} = \frac{R_0^* (R_j^*)^{\mathsf T} R_j^* (c_j^* - c_i^*)}{\|c_j^* - c_i^*\|} = \frac{R_0^* (c_j^* - c_i^*)}{\|c_j^* - c_i^*\|}.$$
So $v_{ij}$ is the unit vector along $c_j' - c_i'$ for the points $c_k' = R_0^* (c_k^* - c_0^*)$, and $c_0' = 0$.

*Line L5.* The matrix $M$ is a sum of terms $\|(I - v_{ij} v_{ij}^{\mathsf T})(c_j - c_i)\|^2$, so it is positive semidefinite, and its smallest eigenvalue is at least 0. Each term is 0 at $c'$, because $c_j' - c_i'$ is parallel to $v_{ij}$, so $M c' = 0$, where $c'$ stacks $c_1', \dots, c_{N-1}'$. By (G2), the null space is spanned by $c'$, so the unit eigenvector of the smallest eigenvalue is $\pm c' / \|c'\| = \pm s' c'$ with $s' = 1 / \|c'\|$. Since $R_0^*$ is a rotation, $\|c'\|^2 = \sum_k \|c_k^* - c_0^*\|^2$, so $s' = s$. For the plus sign, $\sum v_{ij} \cdot (c_j - c_i) = s \sum \|c_j' - c_i'\| > 0$, because the two centers of each edge differ by (G1). For the minus sign the sum is negative. So the sign test of line L5 picks $c = s c'$, which is the target.

*Line L6.* It sets $t_k = -R_k c_k$, the target.

*Line L7.* The cameras are exact, so by (G3) each linear triangulation returns the target point, with all errors 0. All views pass the gate of $10 \tau$.

*Lines L8 and L9.* The cost of the target is 0, so no step can lower it, and each bundle adjustment returns its start unchanged. No error exceeds $\tau$, and each kept point has at least two views, so the filter removes nothing.

So line L10 returns the target. $\blacksquare$
