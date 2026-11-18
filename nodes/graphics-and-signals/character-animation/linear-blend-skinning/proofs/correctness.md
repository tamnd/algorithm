---
title: Linear blend skinning computes the blend of the rigidly moved points and has the basic skinning properties
proves: [correctness]
status: full
---

We use the notation of the page.
All transforms are $4 \times 4$ matrices that act on column vectors, and a point $v$ is the column $(x, y, z, 1)$.
A rigid or affine transform has the bottom row $(0, 0, 0, 1)$.
For one vertex, the weights are $w_j \ge 0$ with $\sum_j w_j = 1$, and $A = \sum_j w_j P_j$ with $P_j = M_j B_j^{-1}$ is the matrix of lines L3 and L4.
The arithmetic is exact.

## The blend

**Lemma 1.** Line L5 gives $v' = \sum_j w_j (P_j v)$.

*Proof.*
Matrix multiplication is linear in the matrix: $(\sum_j w_j P_j) v = \sum_j w_j (P_j v)$. $\square$

**Lemma 2.** $A$ is an affine transform.

*Proof.*
Each $P_j$ is a product of affine transforms, so its bottom row is $(0, 0, 0, 1)$.
The bottom row of $A$ is $\sum_j w_j (0, 0, 0, 1) = (0, 0, 0, 1)$, because $\sum_j w_j = 1$. $\square$

So $v'$ is a point (its last coordinate is 1), and by Lemma 1 it is a convex combination of the points $P_j v$.

## Bind pose, single weights and rigid motions

**Lemma 3.** If $M_j = B_j$ for every joint, then $v' = v$ and $n' = n$ for every vertex.

*Proof.*
Then $P_j = B_j B_j^{-1} = I$, so $A = \sum_j w_j I = I$.
Line L5 gives $v$, and line L6 gives $\operatorname{normalize}(I n) = n$ for a unit $n$. $\square$

**Lemma 4.** If a vertex has the single weight $w_j = 1$, then $v' = P_j v$, and all such vertices of joint $j$ move by the same rigid transform.

*Proof.*
Then $A = P_j$.
$M_j$ and $B_j$ are rigid, so $P_j$ is rigid, and it is the same matrix for all these vertices. $\square$

**Lemma 5.** Let $G$ be a rigid transform. If every $M_j$ is replaced by $G M_j$, then every $v'$ is replaced by $G v'$.

*Proof.*
The new palette is $G M_j B_j^{-1} = G P_j$, so the new blend is $\sum_j w_j G P_j = G A$ by linearity. $\square$

## Normals

**Lemma 6.** Let $A_3$ be invertible, $n$ a normal and $t$ a tangent with $t \cdot n = 0$.
Then $(A_3^{-T} n) \cdot (A_3 t) = 0$.

*Proof.*
$(A_3^{-T} n)^T (A_3 t) = n^T A_3^{-1} A_3 t = n^T t = 0$.
The translation column of $A$ does not act on direction vectors, so a tangent of the surface moves by $A_3$. $\square$

**Lemma 7.** If $\det A_3 \ne 0$, the vector $\operatorname{sign}(\det A_3)\operatorname{cof}(A_3) n$ used by the code has the direction of $A_3^{-T} n$.

*Proof.*
For the columns $c_0, c_1, c_2$ of $A_3$, the code builds the matrix $K$ with the columns $c_1 \times c_2$, $c_2 \times c_0$ and $c_0 \times c_1$.
Then $(A_3^T K)_{ab} = c_a \cdot (c_{b+1} \times c_{b+2})$ with indices mod 3, which is $\det A_3$ for $a = b$ and 0 for $a \ne b$, because a triple product with a repeated column is 0.
So $K = \det(A_3) A_3^{-T}$, and $\operatorname{sign}(\det A_3) K n = |\det A_3|\, A_3^{-T} n$, a positive multiple. $\square$

After the normalization of line L6, the normal has length 1.

## The twist check value

**Lemma 8.** Let $P_1 = I$, $P_2 = R_x(\theta)$ and $w_1 = w_2 = \tfrac12$.
The vertex $(0, 1, 0)$ goes to $(0, \tfrac{1 + \cos\theta}{2}, \tfrac{\sin\theta}{2})$, at the distance $|\cos(\theta/2)|$ from the $x$ axis.

*Proof.*
$R_x(\theta)(0, 1, 0) = (0, \cos\theta, \sin\theta)$, and Lemma 1 averages it with $(0, 1, 0)$.
The squared distance is $\frac{(1 + \cos\theta)^2 + \sin^2\theta}{4} = \frac{2 + 2\cos\theta}{4} = \cos^2(\theta/2)$. $\square$

At $\theta = \pi$ the vertex goes to the origin.
So $A_3 = \tfrac12 (I + R_x(\pi)) = \operatorname{diag}(1, 0, 0)$ is not a rotation, which proves that LBS does not keep lengths.
