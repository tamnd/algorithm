---
title: Correctness of eigenfaces
proves: [correctness]
status: full
---

This proof covers lines L1 to L13 of the main page. The training set has $M$ images $\Gamma_1, \dots, \Gamma_M \in \mathbb R^P$, each with a class label. Line L1 gives the mean $\Psi$, and line L2 gives $\Phi_i = \Gamma_i - \Psi$ and the $P \times M$ matrix $A = [\Phi_1 \cdots \Phi_M]$. The scatter matrix is $S = A A^T = \sum_i \Phi_i \Phi_i^T$; the covariance of Turk and Pentland is $C = \frac1M S$, which has the same eigenvectors. Arithmetic is exact. The claim is about the linear algebra, not about how well the method recognizes faces.

## Lemma 1 (the small matrix)

Let $A^T A v = \lambda v$ with $\lVert v \rVert = 1$ and $\lambda > 0$. Then $u = A v / \lVert A v \rVert$ is a unit eigenvector of $S = A A^T$ with the eigenvalue $\lambda$, and $\lVert A v \rVert = \sqrt{\lambda}$. If $v_1, \dots, v_r$ are orthonormal eigenvectors of $A^T A$ with positive eigenvalues, the vectors $u_1, \dots, u_r$ are orthonormal. Each positive eigenvalue of $S$ is an eigenvalue of $A^T A$ with the same multiplicity.

*Proof.* $S (A v) = A (A^T A v) = \lambda A v$, and $\lVert A v \rVert^2 = v^T A^T A v = \lambda > 0$, so $A v \ne 0$. For two such vectors,
$$u_i^T u_j = \frac{v_i^T A^T A v_j}{\sqrt{\lambda_i \lambda_j}} = \frac{\lambda_j\, v_i^T v_j}{\sqrt{\lambda_i \lambda_j}} = \delta_{ij}.$$
In the other direction, if $S u = \lambda u$ with $\lambda > 0$, then $A^T A (A^T u) = \lambda A^T u$ and $A^T u \ne 0$, because $\lVert A^T u \rVert^2 = \lambda$. The two maps $v \mapsto A v$ and $u \mapsto A^T u$ are injective on the eigenspaces of $\lambda$, so the eigenspaces have the same dimension. $\square$

So line L3 builds the $M \times M$ matrix $A^T A$, line L4 finds its eigenpairs, and line L5 turns them into the leading eigenvectors of $S$, the eigenfaces. Their eigenvalues for $C$ are $\lambda / M$.

## Lemma 2 (rank)

$S$ has rank at most $M - 1$, so there are at most $M - 1$ eigenfaces with a positive eigenvalue.

*Proof.* $\sum_i \Phi_i = \sum_i \Gamma_i - M \Psi = 0$, so the columns of $A$ are linearly dependent and $\operatorname{rank} S = \operatorname{rank} A \le M - 1$. $\square$

The code stops at eigenvalues that are $0$ up to rounding, so it returns at most $M - 1$ eigenfaces, and with all of them it rebuilds each training image exactly (they lie in $\Psi + \operatorname{span}(A)$).

## Lemma 3 (projection)

Let $U = [u_1 \cdots u_K]$ have orthonormal columns. For an image $\Gamma$ with $\Phi = \Gamma - \Psi$, the weights $\omega = U^T \Phi$ of line L8 give the point $\Psi + U \omega$ of the face space $\Psi + \operatorname{span}(U)$ that is closest to $\Gamma$, and the distance of line L9 satisfies $\epsilon^2 = \lVert \Phi \rVert^2 - \lVert \omega \rVert^2$. For two images, $\lVert \omega - \omega' \rVert$ is the distance between their projections.

*Proof.* $U U^T$ is the orthogonal projection onto $\operatorname{span}(U)$, so $\Phi - U U^T \Phi$ is orthogonal to the span, and the Pythagorean theorem gives both the minimality and $\lVert \Phi \rVert^2 = \lVert U \omega \rVert^2 + \epsilon^2 = \lVert \omega \rVert^2 + \epsilon^2$. Also $\lVert U \omega - U \omega' \rVert = \lVert \omega - \omega' \rVert$ because $U^T U = \mathrm{Id}$. $\square$

## Theorem 1 (eigenfaces are the best subspace)

Let $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_P \ge 0$ be the eigenvalues of $S$. For each $P \times K$ matrix $Q$ with orthonormal columns,
$$\sum_{i=1}^M \lVert \Phi_i - Q Q^T \Phi_i \rVert^2 \ge \sum_{l > K} \lambda_l,$$
and equality holds for the $K$ eigenfaces of line L5.

*Proof.* By Lemma 3 for each $\Phi_i$, the left side is $\sum_i \lVert \Phi_i \rVert^2 - \sum_i \lVert Q^T \Phi_i \rVert^2 = \operatorname{tr} S - \operatorname{tr}(Q^T S Q)$. Write $S = \sum_l \lambda_l e_l e_l^T$ with orthonormal eigenvectors $e_l$. Then
$$\operatorname{tr}(Q^T S Q) = \sum_l \lambda_l \lVert Q^T e_l \rVert^2 = \sum_l \lambda_l c_l, \qquad c_l = \lVert Q^T e_l \rVert^2 .$$
Each $c_l$ lies in $[0, 1]$, because $Q Q^T$ is a projection, and $\sum_l c_l = \lVert Q \rVert_F^2 = K$. Under these constraints the sum $\sum_l \lambda_l c_l$ is largest when $c_l = 1$ for the $K$ largest $\lambda_l$ and $0$ for the others: moving weight from a larger $\lambda$ to a smaller one never increases the sum. So $\operatorname{tr}(Q^T S Q) \le \sum_{l \le K} \lambda_l$, and the left side is at least $\operatorname{tr} S - \sum_{l \le K} \lambda_l = \sum_{l > K} \lambda_l$. For $Q = U$, the eigenfaces, $c_l = 1$ for $l \le K$ and $0$ otherwise, which gives equality. $\square$

When $\lambda_K = \lambda_{K+1}$ the best subspace is not unique, and the eigenfaces are one of the best ones.

## Theorem 2 (recognition)

Line L6 stores, for each class $c$, the mean $\Omega_c$ of the weight vectors of its training images. Lines L8 to L13 return "not a face" if $\epsilon > \theta_{\text{face}}$; otherwise they return the class whose $\Omega_c$ is nearest to $\omega$, or "unknown" if that distance is above $\theta_{\text{class}}$.

*Proof.* Line L8 computes $\omega$ and line L9 the distance $\epsilon$ of Lemma 3. Lines L10 to L13 test the thresholds and scan the classes for the least distance. By Lemma 3 the distances in weight space are distances in face space. $\square$

## What is not proved

Nothing here says that the nearest class is the right person. The eigenfaces keep the directions of largest variance of the training set, and these can come from lighting or pose rather than identity. Belhumeur, Hespanha and Kriegman (1997) showed that such variation can dominate the first eigenfaces. That is a limit of the model, not of the computation.
