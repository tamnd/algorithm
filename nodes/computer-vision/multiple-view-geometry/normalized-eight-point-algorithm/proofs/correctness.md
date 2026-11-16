---
title: The normalized eight-point algorithm recovers F exactly from exact data, and its output moves with the data under similarities
proves: [correctness]
status: full
---

We use the notation of the page. The input is $n \ge 8$ pairs of 2D points, written as $\mathbf{x}_i = (u_i, v_i, 1)^{\mathsf T}$ and $\mathbf{x}'_i = (u'_i, v'_i, 1)^{\mathsf T}$. For a $3 \times 3$ matrix $G$ we write $\mathbf{g} \in \mathbb{R}^9$ for its rows put one after the other. The canonical form of a nonzero matrix is the matrix divided by its Frobenius norm, times the sign of its entry of largest absolute value. $A_{\mathrm{raw}}$ is the matrix of the plain eight-point algorithm on the input points, and $A$ is the matrix of line L5, built from the moved points $\mathbf{y}_i = T\mathbf{x}_i$ and $\mathbf{y}'_i = T'\mathbf{x}'_i$.

**Claim.** (a) Let $F$ be a real matrix of rank 2 with $\mathbf{x}'^{\mathsf T}_i F\mathbf{x}_i = 0$ for all $i$, and let $A_{\mathrm{raw}}$ have rank 8. Then the algorithm returns the canonical form of $F$. (b) On any input, the output has rank at most 2, and line L9 gives the matrix of rank at most 2 closest to $G$ in the Frobenius norm, in the normalized coordinates. (c) Let $S$ and $S'$ be similarities of the two images, and move the input to $S\mathbf{x}_i$ and $S'\mathbf{x}'_i$. If the smallest singular value of $A$ is simple and the third singular value of $G$ is simple, the output for the moved input is the canonical form of $S'^{-\mathsf T} F_{\mathrm{out}} S^{-1}$, where $F_{\mathrm{out}}$ is the output for the original input.

**Lemma 1 (change of coordinates).** Let $T$ and $T'$ be invertible. A matrix $G$ satisfies $\mathbf{y}'^{\mathsf T}_i G\mathbf{y}_i = 0$ for all $i$ if and only if $F = T'^{\mathsf T} G T$ satisfies $\mathbf{x}'^{\mathsf T}_i F\mathbf{x}_i = 0$ for all $i$. The map $G \mapsto T'^{\mathsf T} G T$ is linear, one to one, and keeps the rank.

*Proof.* $\mathbf{x}'^{\mathsf T}_i T'^{\mathsf T} G T\mathbf{x}_i = (T'\mathbf{x}'_i)^{\mathsf T} G (T\mathbf{x}_i) = \mathbf{y}'^{\mathsf T}_i G\mathbf{y}_i$. The inverse map is $F \mapsto T'^{-\mathsf T} F T^{-1}$, and multiplication by invertible matrices does not change the rank. $\square$

By Lemma 1 of the [eight-point proof](/eight-point-algorithm/), $A_{\mathrm{raw}}\mathbf{f} = \mathbf{0}$ exactly when $F$ satisfies the constraints, and $A\mathbf{g} = \mathbf{0}$ exactly when $G$ does. So Lemma 1 here says that the linear map $G \mapsto T'^{\mathsf T} G T$ sends the null space of $A$ onto the null space of $A_{\mathrm{raw}}$, and the two null spaces have the same dimension. Both matrices have 9 columns, so $A$ has rank 8 exactly when $A_{\mathrm{raw}}$ has rank 8.

The similarities of lines L1 and L2 are invertible. Their last row is $(0, 0, 1)$, and their scale $\sqrt2 / d$ is finite and positive, because the code stops when all points of one image coincide ($d = 0$).

**Proof of part (a).** Put $G_0 = T'^{-\mathsf T} F T^{-1}$. By Lemma 1, $G_0$ has rank 2 and satisfies the constraints on the moved points, so $A\mathbf{g}_0 = \mathbf{0}$. Since $A$ has rank 8, the null space of $A$ is the line spanned by $\mathbf{g}_0$. Line L6 returns a unit vector in it (Lemma 2 of the eight-point proof), so line L7 gives $G = \lambda G_0$ with $\lambda \ne 0$. This matrix has rank 2, so its third singular value is 0, and line L9 does not change it. Line L10 gives $T'^{\mathsf T}\lambda G_0 T = \lambda F$, and line L11 gives the canonical form of $F$, for every $\lambda \ne 0$. $\blacksquare$

**Proof of part (b).** Line L9 is Lemma 3 (i) of the eight-point proof, applied to $G$. The output $T'^{\mathsf T} G T$ has the rank of $G$ by Lemma 1, so at most 2. $\square$

Part (b) does not say that the output is the matrix of rank 2 closest to anything in the original coordinates. The rank step happens in the normalized frame, as Hartley (1997) does it.

**Lemma 2 (the similarity part of the normalization).** Let $S$ be a similarity of the plane, $S\mathbf{x} = (sQ\mathbf{p} + \mathbf{c}, 1)$ for $\mathbf{x} = (\mathbf{p}, 1)$, with $s > 0$, $Q$ a $2 \times 2$ orthogonal matrix and $\mathbf{c} \in \mathbb{R}^2$. Let $T$ be the normalizing similarity of the points $\mathbf{x}_i$ and $\hat T$ that of the points $S\mathbf{x}_i$. Then $\hat T S = \hat Q T$ with $\hat Q = \begin{pmatrix} Q & \mathbf{0} \\ \mathbf{0}^{\mathsf T} & 1 \end{pmatrix}$.

*Proof.* The centroid of the moved points is $sQ\bar{\mathbf{p}} + \mathbf{c}$, where $\bar{\mathbf{p}}$ is the old centroid, and each distance to it is multiplied by $s$. So $\hat T$ subtracts $sQ\bar{\mathbf{p}} + \mathbf{c}$ and scales by $\sqrt2/(s d)$. Then $\hat T S\mathbf{x} = ((\sqrt2/d)\,Q(\mathbf{p} - \bar{\mathbf{p}}), 1) = \hat Q T\mathbf{x}$. $\square$

**Proof of part (c).** By Lemma 2, the moved points in the normalized frame are $\hat Q\mathbf{y}_i$ and $\hat Q'\mathbf{y}'_i$, with $\hat Q$ and $\hat Q'$ orthogonal. For a matrix $G$ put $\hat G = \hat Q' G\hat Q^{\mathsf T}$. Then $(\hat Q'\mathbf{y}'_i)^{\mathsf T}\hat G(\hat Q\mathbf{y}_i) = \mathbf{y}'^{\mathsf T}_i G\mathbf{y}_i$ and $\|\hat G\|_F = \|G\|_F$. So the new matrix $\hat A$ satisfies $\|\hat A\hat{\mathbf{g}}\| = \|A\mathbf{g}\|$ for all $\mathbf{g}$, and the unit minimizer of line L6 moves from $\mathbf{g}$ to $\pm\hat{\mathbf{g}}$ when the minimizer is unique up to sign. The SVD of $\hat G$ is that of $G$ with $U$ and $V$ multiplied by $\hat Q'$ and $\hat Q$, so line L9 also commutes with $G \mapsto \hat Q' G\hat Q^{\mathsf T}$ when the third singular value is simple. Line L10 for the moved input gives
$$\hat T'^{\mathsf T}\hat Q' G\hat Q^{\mathsf T}\hat T = (\hat Q'^{\mathsf T}\hat T')^{\mathsf T} G (\hat Q^{\mathsf T}\hat T) = (T' S'^{-1})^{\mathsf T} G (T S^{-1}) = S'^{-\mathsf T}(T'^{\mathsf T} G T) S^{-1},$$
using $\hat Q^{\mathsf T}\hat T = T S^{-1}$ from Lemma 2. Up to the sign of $\mathbf{g}$, this is $S'^{-\mathsf T} F_{\mathrm{out}} S^{-1}$ before line L11, and line L11 removes the sign. $\blacksquare$

**Remark (the plain algorithm is not covariant).** Without lines L1 and L2, a translation of the pixel frame changes $A_{\mathrm{raw}}$ by a change of variables in $\mathbf{f}$ that is not orthogonal, so the minimizer of $\|A_{\mathrm{raw}}\mathbf{f}\|$ over unit vectors does not move with the data. The page shows a measured example of the effect on the accuracy. That the normalization improves the accuracy is a property of the condition number of $A$ (Hartley 1997); it is supported by analysis and by experiments, not by a theorem on the error of the output.
