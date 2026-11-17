---
title: The SHOT reference frame is orthonormal and moves with the cloud, so the descriptor is invariant under rigid motions
proves: [correctness]
status: full
---

Fix the feature point $p$, the radius $R$, and the neighbors $q_1, \ldots, q_m$ of line L1, with offsets $o_i = q_i - p$ and distances $d_i = \lVert o_i \rVert$, $0 < d_i < R$, and $m \ge 3$. A *rigid motion* here is $x \mapsto Q x + t$ with $Q$ a rotation, $Q^\top Q = I$ and $\det Q = 1$; it acts on points by this map and on normals by $Q$.

**Lemma 1 (the matrix).** The matrix $M$ of line L2 is symmetric and positive semidefinite. Under a rigid motion it becomes $Q M Q^\top$.

*Proof.* Each weight $R - d_i$ is positive, so $M$ is a positive combination of the matrices $o_i o_i^\top$, each symmetric with $y^\top o_i o_i^\top y = (o_i \cdot y)^2 \ge 0$. A rigid motion keeps distances, so the neighbor set and the weights stay the same, and it maps $o_i$ to $Q o_i$, because the translation cancels in the difference. So $M$ becomes $\sum w_i Q o_i o_i^\top Q^\top / \sum w_i = Q M Q^\top$. $\square$

By the spectral theorem, $M$ has an orthonormal basis of eigenvectors. When its three eigenvalues are distinct, each eigenvector is fixed up to its sign, and the eigenvectors of $Q M Q^\top$ are $\pm Q x^+$, $\pm Q y^+$, $\pm Q z^+$.

The sign rule of lines L4 and L5 compares, for an axis $a$, the number of offsets with $a \cdot o_i > 0$ and the number with $a \cdot o_i < 0$, and keeps $a$ if the first is larger, or flips it if the second is larger. If the counts are equal, it flips $a$ when $\sum_i a \cdot o_i < 0$ and keeps it otherwise. Call the axis $a$ *decided* when the two counts differ or the sum of the projections is not 0. Both conditions are the same for $a$ and $-a$.

**Lemma 2 (the sign rule).** Let $D(a)$ be the result of the sign rule for an axis $a$ and the offsets $o_i$. If $a$ is decided, then $D(a) = D(-a)$, and the rule applied to $Q a$ and the offsets $Q o_i$ returns $Q D(a)$.

*Proof.* Replacing $a$ by $-a$ swaps the two counts and negates the sum. If the counts differ, the larger count moves to the other side, so the rule flips $-a$ exactly when it keeps $a$, and both give the same vector. If the counts are equal and the sum is not 0, the sum changes sign, and the same argument applies. The projections $(Q a) \cdot (Q o_i) = a \cdot o_i$ are the same for the moved data, so the rule makes the same choice, and returns $Q D(a)$. $\square$

An axis that is not decided has a neighborhood that is balanced on the two sides of the plane orthogonal to it. The rule then keeps the sign from the eigenvalue solver, and no rule that uses only the projections can do better, because these projections give the same counts and the same sum for both signs.

**Theorem 1 (the frame).** Suppose $M$ has three distinct eigenvalues and the axes $x^+$ and $z^+$ are decided. Then the frame $(x, y, z)$ of lines L3 to L5 is orthonormal and right handed, it depends only on $p$ and the neighbors (not on the signs returned by the eigenvalue solver), and under a rigid motion it becomes $(Q x, Q y, Q z)$.

*Proof.* $x$ and $z$ are unit eigenvectors for different eigenvalues of a symmetric matrix, so they are orthogonal. Then $y = z \times x$ is a unit vector orthogonal to both, and $x \times y = x \times (z \times x) = z\,(x \cdot x) - x\,(x \cdot z) = z$, so the frame is right handed. The eigenvectors are fixed up to sign, and by Lemma 2 the sign rule gives the same $x$ and $z$ from either sign, so the frame does not depend on the solver. Under a rigid motion, the eigenvectors become $\pm Q x^+$ and $\pm Q z^+$ by Lemma 1, and Lemma 2 gives $Q x$ and $Q z$. Since $Q$ is a rotation, $Q z \times Q x = Q (z \times x) = Q y$. $\square$

**Theorem 2 (the descriptor).** Under the assumptions of Theorem 1, the following hold.

1. Each neighbor adds 1 to exactly one of the 352 entries, so before the scaling at line L12 the entries sum to $m$, and the result has unit Euclidean norm.
2. Under a rigid motion, every neighbor has the same local coordinates and the same cosine, so the descriptor is unchanged, except for a value that lies exactly on a cell border, where rounding can move it to the next cell.

*Proof.* (1) The volume index of line L9 is $(s \cdot 2 + e) \cdot 2 + h$ with a sector $s \in \{0, \ldots, 7\}$, a half $e \in \{0, 1\}$ and a shell $h \in \{0, 1\}$, so it is an integer in $[0, 32)$, and each triple $(s, e, h)$ gives a different index. The bin $k$ of line L10 is in $[0, 11)$. So $11 v + k$ is a one to one map onto $[0, 352)$, and line L11 adds 1 to one entry. With $m \ge 3$ the vector is not zero, and line L12 divides it by its norm.

(2) By Theorem 1 the moved frame is $(Q x, Q y, Q z)$, and the moved offset is $Q o_i$, so the local coordinates are $(Q o_i) \cdot (Q x) = o_i \cdot x$, and the same for $y$ and $z$. The moved normal is $Q \mathbf{n}_i$, and $(Q \mathbf{n}_i) \cdot (Q z) = \mathbf{n}_i \cdot z$. The distance, the azimuth, the sign of the elevation and the cosine are functions of these numbers, so every neighbor lands in the same cell, and the descriptor is the same. $\square$

**What the assumptions exclude.** If two eigenvalues of $M$ are equal, as on a symmetric neighborhood, the eigenvectors in their eigenspace can be any orthonormal pair, and the frame, and so the descriptor, is not repeatable. If an axis is not decided, its sign is arbitrary. These are properties of the neighborhood, not of the procedure; they are the main source of error of SHOT on real data, together with noise near cell borders, which the quadrilinear interpolation of the original method softens. $\blacksquare$
