---
title: Both steps of as-rigid-as-possible shape manipulation have unique minimizers, rigid motions are reproduced, and the fit is the Procrustes rotation
proves: [correctness]
status: full
---

We use the notation of the page and identify the plane with $\mathbb{C}$, so $R_{90}$ is the multiplication by $i$.
For a triangle in one vertex order, the frame relation reads $v_2 - v_0 = \zeta(v_1 - v_0)$ with $\zeta = x + iy$.
We assume that the rest triangles are not degenerate and that the mesh is connected through shared edges: any two triangles are joined by a chain of triangles in which neighbours share an edge.

## Step 1

**Lemma 1.** $E_1(u) = 0$ if and only if there are $\alpha, \beta \in \mathbb{C}$ with $u_k = \alpha v_k + \beta$ for every vertex $k$.

*Proof.*
If $u = \alpha v + \beta$, then $u_2 - u_0 = \alpha(v_2 - v_0) = \alpha\zeta(v_1 - v_0) = \zeta(u_1 - u_0)$ for every triangle and order, so every term of $E_1$ is 0.
Conversely, let $E_1(u) = 0$. In one triangle, put $\alpha = (u_1 - u_0)/(v_1 - v_0)$ and $\beta = u_0 - \alpha v_0$. Then $u_0 = \alpha v_0 + \beta$, $u_1 = \alpha v_1 + \beta$, and $u_2 = u_0 + \zeta\alpha(v_1 - v_0) = \alpha v_2 + \beta$.
Two triangles that share an edge share two vertices with different rest positions, and two such values fix $\alpha$ and $\beta$, so the neighbours have the same $\alpha$, $\beta$. By connectivity, all triangles do. $\square$

So $E_1$ is 0 on the similarity images $\alpha v + \beta$ with $\alpha \ne 0$, which are rotations and uniform scales followed by translations, and on the constant maps with $\alpha = 0$.

**Theorem 1.** If at least two handles have different rest positions, the block of $G$ for the free vertices is positive definite, and step 1 has a unique minimizer. With one handle, the block is singular.

*Proof.*
$E_1$ is a sum of squares of linear functions of $u$, so it is a positive semidefinite quadratic form, and its restriction to free vertices with the handles fixed at 0 is the quadratic form of the free block.
If this restriction is 0 for some $u$, then $E_1(u) = 0$, so $u = \alpha v + \beta$ by Lemma 1. The two handles $a$ and $b$ give $\alpha v_a + \beta = 0 = \alpha v_b + \beta$ with $v_a \ne v_b$, so $\alpha = \beta = 0$ and $u = 0$. So the block is positive definite.
A positive definite quadratic plus linear terms has a unique minimizer, the solution of its normal equations, which line L4 solves with the factor of line L2.
With one handle $a$, $u = v - v_a$ on the free vertices and $u_a = 0$ is nonzero and has $E_1 = 0$, so the block is singular. $\square$

**Corollary.** If the handle targets are $q_k = \alpha v_k + \beta$ for all $k \in H$, step 1 returns $\alpha v + \beta$ for all vertices.

*Proof.*
$\alpha v + \beta$ meets the handles and has $E_1 = 0$, the smallest possible value, so it is the unique minimizer. $\square$

This covers the rest handles ($\alpha = 1$, $\beta = 0$), rigid motions ($|\alpha| = 1$), and uniform scales, as the tests check.

## The fit

**Theorem 2.** For a triangle with the rest vertices $r_0, r_1, r_2$ and the step 1 vertices $p_0, p_1, p_2$, line L5 returns $c_p + \rho(r_k - c_r)$, where $c_r$ and $c_p$ are the centroids and $\rho = \gamma/|\gamma|$ with $\gamma = \sum_k\overline{(r_k - c_r)}(p_k - c_p)$, provided $\gamma \ne 0$. This $\rho$ is the rotation that minimizes $\sum_k|c_p + \rho(r_k - c_r) - p_k|^2$ over $|\rho| = 1$.

*Proof.*
The triangles $w$ that satisfy the frame relation of the rest triangle are exactly $w_k = \alpha r_k + \beta$ for $\alpha, \beta \in \mathbb{C}$, by the argument of Lemma 1 on one triangle; $w_0$ and $w_1$ are free, and so are $\alpha$ and $\beta$.
So the fit minimizes $\sum_k|\alpha r_k + \beta - p_k|^2$.
For fixed $\alpha$ the best $\beta$ makes the centroids agree: $\beta = c_p - \alpha c_r$.
Then the sum is $\sum_k|\alpha s_k - t_k|^2$ with $s_k = r_k - c_r$ and $t_k = p_k - c_p$, minimized by $\alpha = \gamma/\sum_k|s_k|^2$.
The fitted triangle has the centroid $c_p$ and the edge $w_1 - w_0 = \alpha(r_1 - r_0)$, so the rescale factor is $|r_1 - r_0|/|w_1 - w_0| = 1/|\alpha|$, and the rescaled triangle is $c_p + \frac{\alpha}{|\alpha|}s_k = c_p + \rho s_k$.
For $|\rho| = 1$, $\sum_k|\rho s_k - t_k|^2 = \sum_k|s_k|^2 + \sum_k|t_k|^2 - 2\operatorname{Re}(\overline{\rho}\gamma)$, which is smallest when $\rho$ has the direction of $\gamma$. $\square$

If $\gamma = 0$, the step 1 triangle is collapsed or turned so that no rotation fits better than another, and the rescale divides by 0; this happens only for extreme drags.

## Step 2

**Theorem 3.** If every connected part of the mesh has a handle, the block of the matrix of $E_2$ for the free vertices is positive definite, and step 2 has a unique minimizer.

*Proof.*
For the coordinate $x$, $E_2$ is $\sum_{\text{edges } ij}(u_i - u_j - e_{ij})^2$ with fixed numbers $e_{ij}$ from the fitted triangles. Its quadratic part is $\sum(u_i - u_j)^2$, the form of the graph Laplacian $H$.
If it is 0 with the handles at 0, $u$ is constant on each connected part, and that constant is the value 0 at a handle. So the free block is positive definite, and line L6 solves its normal equations. The same holds for $y$. $\square$

**Theorem 4.** If the handle targets are a rigid motion $q_k = \alpha v_k + \beta$ with $|\alpha| = 1$, the final result is $\alpha v + \beta$.

*Proof.*
By the Corollary, step 1 returns $p = \alpha v + \beta$.
In Theorem 2, $t_k = \alpha s_k$, so $\gamma = \alpha\sum|s_k|^2$ and $\rho = \alpha$; each fitted triangle is $c_p + \alpha s_k = \alpha r_k + \beta$, the image of the rest triangle.
So $u = \alpha v + \beta$ meets the handles and makes every term of $E_2$ zero, and by Theorem 3 it is the unique minimizer. $\square$

## What is not proved

Step 2 depends on step 1 through the fitted triangles, so the final mesh minimizes $E_2$ for fixed fitted triangles, not an energy of the final mesh alone.
The page therefore makes no claim that the result is the most rigid mesh that meets the handles.
For a uniform scale of the handles by 2, the tests measure that step 2 brings the free vertical edges from the length 2 back to below 1.2.
