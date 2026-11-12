---
title: In the ideal case spectral clustering returns the connected components
proves: [correctness]
status: full
---

We use the pseudocode of the page. $W$ is symmetric with $w_{ij} \ge 0$ and $w_{ii} = 0$, $d_i = \sum_j w_{ij}$, $D = \mathrm{diag}(d_i)$, $L = D - W$, $L_{\mathrm{sym}} = D^{-1/2} L D^{-1/2}$ and $L_{\mathrm{rw}} = D^{-1} L$. For a set $A$ of vertices, $\mathbb{1}_A$ is its indicator vector.

**Lemma 1 (quadratic forms).** For each $f \in \mathbb{R}^n$, $f^T L f = \sum_{i<j} w_{ij} (f_i - f_j)^2$. If each $d_i > 0$, then $g^T L_{\mathrm{sym}} g = \sum_{i<j} w_{ij} (g_i/\sqrt{d_i} - g_j/\sqrt{d_j})^2$.

*Proof.* $f^T L f = \sum_i d_i f_i^2 - \sum_{i,j} w_{ij} f_i f_j = \frac12 \sum_{i,j} w_{ij} (f_i^2 + f_j^2 - 2 f_i f_j)$, by $d_i = \sum_j w_{ij}$ and the symmetry of $W$. This is $\frac12 \sum_{i,j} w_{ij}(f_i - f_j)^2 = \sum_{i<j} w_{ij}(f_i - f_j)^2$. For the second form put $f = D^{-1/2} g$; then $g^T L_{\mathrm{sym}} g = f^T L f$. $\square$

**Lemma 2 (the null spaces).** Let the graph with edges $\{i, j : w_{ij} > 0\}$ have the connected components $A_1, \ldots, A_c$. Then the null space of $L$ is $\mathrm{span}(\mathbb{1}_{A_1}, \ldots, \mathbb{1}_{A_c})$, of dimension $c$. If each $d_i > 0$, the null space of $L_{\mathrm{rw}}$ is the same space, and the null space of $L_{\mathrm{sym}}$ is $\mathrm{span}(D^{1/2}\mathbb{1}_{A_1}, \ldots, D^{1/2}\mathbb{1}_{A_c})$.

*Proof.* $L$ is symmetric and, by Lemma 1, positive semidefinite. For such a matrix $Lf = 0$ if and only if $f^T L f = 0$: one direction is clear, and if $f^T L f = 0$ then $\lVert L^{1/2} f \rVert^2 = 0$, so $L f = L^{1/2} L^{1/2} f = 0$. By Lemma 1, $f^T L f = 0$ if and only if $f_i = f_j$ for each pair with $w_{ij} > 0$. Along a path the value of $f$ then stays the same, so $f$ is constant on each component, that is, $f = \sum_t a_t \mathbb{1}_{A_t}$. Conversely, such an $f$ makes each term zero. The indicator vectors have disjoint non-empty supports, so they are linearly independent, and the dimension is $c$.

$L_{\mathrm{rw}} f = D^{-1} L f$ and $D^{-1}$ is invertible, so $L_{\mathrm{rw}}$ has the same null space as $L$. Finally $L_{\mathrm{sym}} g = D^{-1/2} L D^{-1/2} g$ is zero if and only if $L (D^{-1/2} g) = 0$, that is, $D^{-1/2} g \in \mathrm{span}(\mathbb{1}_{A_t})$, that is, $g \in \mathrm{span}(D^{1/2}\mathbb{1}_{A_t})$. $\square$

Because $L$ and $L_{\mathrm{sym}}$ are symmetric and positive semidefinite, the multiplicity of their eigenvalue 0 equals the dimension of the null space, which is $c$. $L_{\mathrm{rw}}$ is similar to $L_{\mathrm{sym}}$ ($L_{\mathrm{rw}} = D^{-1/2} L_{\mathrm{sym}} D^{1/2}$), so it has the same eigenvalues with the same multiplicities.

**Lemma 3 (generalized eigenvectors).** If $L_{\mathrm{sym}} v = \lambda v$ and $u = D^{-1/2} v$, then $L u = \lambda D u$ and $L_{\mathrm{rw}} u = \lambda u$.

*Proof.* $L u = D^{1/2} (D^{-1/2} L D^{-1/2}) v = D^{1/2} \lambda v = \lambda D (D^{-1/2} v) = \lambda D u$. Multiply by $D^{-1}$ for the second equation. $\square$

So line L6 turns the eigenvectors of $L_{\mathrm{sym}}$ into the generalized eigenvectors of Shi and Malik.

**Lemma 4 (k-means++ on k distinct points).** Let the points $y_1, \ldots, y_n$ take exactly $k$ distinct values $z_1, \ldots, z_k$. Then k-means++ seeding with $k$ centers picks each $z_t$ once, with probability 1, and Lloyd's algorithm then stops with cost 0 and the clusters $\{i : y_i = z_t\}$.

*Proof.* The first center is some $z_t$. Suppose the centers so far are $j < k$ distinct values. A point equal to a chosen center has weight $\min_c \lVert y - c \rVert^2 = 0$ and is picked with probability 0. A point with another value has positive weight, and such a point exists because $j < k$. So the next center is a new value. After $k$ steps the centers are $z_1, \ldots, z_k$. Each point is then assigned to the center equal to it, at distance 0, and each center is the mean of the points assigned to it, which are all equal to it. So the assignment does not change and Lloyd's algorithm stops. $\square$

**Theorem.** Suppose the graph has exactly $k$ connected components $A_1, \ldots, A_k$, and, for the Shi and Malik and the NJW variants, each $d_i > 0$. Then SPECTRAL-CLUSTERING$(W, k, \text{variant})$ returns the partition $\{A_1, \ldots, A_k\}$ with probability 1.

*Proof.* By Lemma 2 the matrix $M$ of lines L2 and L3 has the eigenvalue 0 with multiplicity exactly $k$, and its other eigenvalues are positive (it is positive semidefinite). So the $k$ smallest eigenvalues are all 0, and line L4 returns an orthonormal basis $v_1, \ldots, v_k$ of the null space of $M$, whatever basis the solver picks.

*Unnormalized.* Let $H$ be the $n \times k$ matrix with columns $\mathbb{1}_{A_1}, \ldots, \mathbb{1}_{A_k}$. The columns of $U$ lie in the column space of $H$, so $U = H R$ for a $k \times k$ matrix $R$. $U$ has rank $k$ (its columns are orthonormal), so $R$ is invertible. Row $i$ of $H$ is the unit vector $e_t$ for the component $A_t$ that holds $i$, so row $i$ of $U$ is row $t$ of $R$. The rows of an invertible matrix are linearly independent, so they are non-zero and pairwise distinct.

*Shi and Malik.* The columns of $V$ lie in $\mathrm{span}(D^{1/2}\mathbb{1}_{A_t})$, so $V = D^{1/2} H R$ with $R$ invertible as before. Line L6 gives $U = D^{-1/2} V = H R$, the same form.

*NJW.* As in the Shi and Malik case $V = D^{1/2} H R$, so row $i$ of $U$ before line L7 is $\sqrt{d_i}\, r_t$, where $r_t$ is row $t$ of $R$ for the component of $i$. Line L7 divides it by its norm $\sqrt{d_i} \lVert r_t \rVert > 0$ and gives $r_t / \lVert r_t \rVert$. Two rows $r_t$ and $r_s$ with $t \ne s$ are linearly independent, so neither is a positive multiple of the other, and $r_t / \lVert r_t \rVert \ne r_s / \lVert r_s \rVert$.

In all three cases the points $y_i$ of line L8 take exactly $k$ distinct values, and $y_i = y_j$ if and only if $i$ and $j$ are in the same component. By Lemma 4, line L9 returns the classes of equal points, which are the components. $\blacksquare$

**Remark.** The theorem needs $\lambda_{k+1} > 0$, which here is the statement that there are not more than $k$ components. With more than $k$ components, the null space has dimension above $k$, line L4 picks an arbitrary $k$-dimensional part of it, and the theorem does not hold. Outside the ideal case the method has no exact guarantee; the [Davis-Kahan theorem](/davis-kahan-theorem/) bounds how far the computed eigenspace moves from the ideal one.
