---
title: Correctness of closed-form matting
proves: [correctness]
status: full
---

This proof covers lines L1 to L8 of the main page. The image has $N$ pixels, each with a vector $I_i \in \mathbb R^c$ ($c = 1$ for gray, $c = 3$ for color). The windows $w_k$ are the $3 \times 3$ windows that lie inside the image, so each has $m = |w_k| = 9$ pixels. The image has at least 3 rows and 3 columns, so there is at least one window. The parameter is $\epsilon \ge 0$. For a window, $\mu_k$ is the mean of the $I_i$, and $\Sigma_k = \frac1m \sum_{i \in w_k} (I_i - \mu_k)(I_i - \mu_k)^T$ is the covariance. The cost of Levin, Lischinski and Weiss (equations 3 and 10 of the CVPR paper) is
$$J(\alpha, a, b) = \sum_k \Bigl( \sum_{i \in w_k} (\alpha_i - a_k^T I_i - b_k)^2 + \epsilon \lVert a_k \rVert^2 \Bigr).$$
When $\epsilon = 0$, assume that each $\Sigma_k$ is nonsingular, so that line L4 is defined.

## Lemma 1 (one window)

Fix a window $w$ with $m$ pixels, and let $C$ be the $m \times c$ matrix with rows $c_i = (I_i - \mu)^T$. Let $M = (\Sigma + \frac{\epsilon}{m} \mathrm{Id})^{-1}$. For each vector $\alpha$ on the window,
$$\min_{a, b} \Bigl( \sum_{i \in w} (\alpha_i - a^T I_i - b)^2 + \epsilon \lVert a \rVert^2 \Bigr) = \alpha^T L_w \alpha, \qquad (L_w)_{ij} = \delta_{ij} - \frac{1}{m}\bigl(1 + c_i^T M c_j\bigr).$$

*Proof.* For a fixed $a$, the cost is a sum of squares in $b$, and its minimizer is the mean $b = \bar\alpha - a^T \mu$, with $\bar\alpha = \frac1m \sum_i \alpha_i$. Put this back and write $\tilde\alpha = \alpha - \bar\alpha \mathbf 1$. The cost becomes
$$\lVert \tilde\alpha - C a \rVert^2 + \epsilon \lVert a \rVert^2 .$$
Since $C^T C = m \Sigma$, the matrix $C^T C + \epsilon\, \mathrm{Id} = m M^{-1}$ is positive definite when $\epsilon > 0$, or when $\epsilon = 0$ and $\Sigma$ is nonsingular. This is ridge regression, and its minimum is
$$\tilde\alpha^T \tilde\alpha - \tilde\alpha^T C (C^T C + \epsilon\, \mathrm{Id})^{-1} C^T \tilde\alpha = \tilde\alpha^T \tilde\alpha - \tfrac1m\, \tilde\alpha^T C M C^T \tilde\alpha .$$
The columns of $C$ sum to zero, so $C^T \mathbf 1 = 0$ and $C^T \tilde\alpha = C^T \alpha$. Also $\tilde\alpha^T \tilde\alpha = \alpha^T (\mathrm{Id} - \frac1m \mathbf 1 \mathbf 1^T) \alpha$. So the minimum is $\alpha^T \bigl(\mathrm{Id} - \frac1m (\mathbf 1 \mathbf 1^T + C M C^T)\bigr) \alpha$, and the entry $(i, j)$ of that matrix is $(L_w)_{ij}$. $\square$

## Theorem 1 (the matting Laplacian)

Let $L$ be the matrix built by lines L1 to L5. Then $\min_{a, b} J(\alpha, a, b) = \alpha^T L \alpha$ for each $\alpha$.

*Proof.* The pairs $(a_k, b_k)$ of different windows are independent, so the minimum of the sum is the sum of the minima. By Lemma 1, the minimum for window $k$ is $\alpha^T L_{w_k} \alpha$ with $L_{w_k}$ placed in the rows and columns of the window. Line L5 adds exactly these entries, so $L = \sum_k L_{w_k}$ and the sum is $\alpha^T L \alpha$. $\square$

This is Theorem 1 of the paper. For $c = 1$ the entry is the formula of equation 5, and for $c = 3$ it is equation 12.

## Lemma 2 (shape of $L$)

$L$ is symmetric, positive semidefinite, and $L \mathbf 1 = 0$.

*Proof.* Each $L_{w}$ is symmetric because $M$ is. By Lemma 1, $\alpha^T L \alpha$ is a minimum of sums of squares, so it is at least $0$. For the row sums, $L_w \mathbf 1 = \mathbf 1 - \frac1m (m \mathbf 1 + C M C^T \mathbf 1) = 0$, because $C^T \mathbf 1 = 0$. $\square$

So $L$ is never positive definite: the constant vector is in its null space. The paper calls $L$ "positive definite" in its Section 4, but the paper itself notes that the rows sum to zero, so the right word is semidefinite.

## Lemma 3 (null space for $\epsilon > 0$)

If $\epsilon > 0$, then $L \alpha = 0$ only for constant $\alpha$.

*Proof.* For a semidefinite $L$, $L\alpha = 0$ if and only if $\alpha^T L \alpha = 0$. By Theorem 1, $\alpha^T L \alpha = 0$ means that in each window some $(a_k, b_k)$ gives zero cost. Then $\epsilon \lVert a_k \rVert^2 = 0$, so $a_k = 0$, and $\alpha_i = b_k$ on the whole window. Two windows whose centers are neighbors share 6 pixels, so $\alpha$ has the same constant on both. The centers form a connected grid, so $\alpha$ is one constant on the union of the windows. Each pixel lies in at least one window (the window whose center is the nearest interior pixel), so $\alpha$ is constant. $\square$

If $\epsilon = 0$, the null space also holds each color channel $I^c$, because $\alpha = I^c$ fits each window with zero cost. The test file checks this.

## Theorem 2 (the solution of lines L6 to L8)

Let $S$ be the scribbled pixels with the values $s$, and $U$ the other pixels. If $\epsilon > 0$ and $S$ is not empty, then the problem
$$\min_\alpha \alpha^T L \alpha \quad \text{subject to} \quad \alpha_i = s_i \text{ for } i \in S$$
(equation 13 of the paper) has exactly one solution, and it is the vector of line L8, with $\alpha_U$ from $L_{UU} \alpha_U = -L_{US} s$.

*Proof.* For $y$ on $U$, extend it by $0$ on $S$ to $\bar y$. Then $y^T L_{UU} y = \bar y^T L \bar y \ge 0$. If it is $0$, then $\bar y$ is constant by Lemma 3, and it is $0$ on $S$, so $y = 0$. So $L_{UU}$ is positive definite. With $\alpha_S = s$ fixed, the cost is
$$s^T L_{SS} s + 2 \alpha_U^T L_{US} s + \alpha_U^T L_{UU} \alpha_U,$$
a strictly convex function of $\alpha_U$. Its only minimizer is the zero of the gradient, $L_{UU} \alpha_U + L_{US} s = 0$, which line L7 solves. $\square$

Two consequences follow from linearity and $L \mathbf 1 = 0$. If all scribbles are $1$, then $\alpha = \mathbf 1$. If each scribble value $s_i$ is replaced by $1 - s_i$, the matte becomes $\mathbf 1 - \alpha$. So the foreground and the background are treated the same way.

## Theorem 3 (exact recovery)

Let $\epsilon = 0$, and let the true matte $\alpha^*$ be an affine function of $I$ in each window: $\alpha^*_i = a_k^T I_i + b_k$ for $i \in w_k$. If the scribbles agree with $\alpha^*$, then $\alpha^*$ is a solution of the problem of Theorem 2.

*Proof.* The cost $J(\alpha^*, a, b)$ with these $(a_k, b_k)$ is $0$, so $\alpha^{*T} L \alpha^* = 0$ by Theorem 1. Each feasible $\alpha$ has $\alpha^T L \alpha \ge 0$ by Lemma 2, and $\alpha^*$ is feasible. $\square$

This is Theorem 3 of the paper. Its Theorem 2 shows that the affine model holds when the foreground colors and the background colors of each window each lie on a line in color space (the color line model). For gray images it holds when $F$ and $B$ are constant on each window and $F \ne B$, since then $\alpha = (I - B)/(F - B)$.

The theorem uses the assumption of the setup that each $\Sigma_k$ is nonsingular when $\epsilon = 0$. With constant colors $F$ and $B$, the colors of a window lie on one line, $\Sigma_k$ has rank 1, and $L$ exists only for $\epsilon > 0$. Even when $L$ exists for $\epsilon = 0$, the solution need not be unique: the null space holds the constants and the channels, and the scribbles must pin all of them. The code uses a small $\epsilon > 0$, so Theorem 2 gives one solution. As $\epsilon \to 0$ it approaches $\alpha^*$; the test file checks this with $\epsilon = 10^{-8}$ for a gray and a color image.

## What is not proved

There is no maximum principle. Unlike a graph Laplacian with positive weights, $L$ can have positive entries off the diagonal, so $\alpha$ can leave $[0, 1]$. The test file shows such a case, and in practice the result is clipped. Nothing here says that the matte matches the true matte of a natural image where the color line model fails.
