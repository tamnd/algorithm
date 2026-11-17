---
title: As-rigid-as-possible shape interpolation has a unique solution that starts at the source, ends at the target and keeps rigid motions rigid
proves: [correctness]
status: full
---

We use the notation of the page.
The triangulation has the vertices $1, \dots, n$ and the triangles $f = (i, j, k)$, each with a nondegenerate source triangle.
For a triangle $f$, let $E_f(V)$ be the 2 by 2 matrix with the columns $v_j - v_i$ and $v_k - v_i$, and $M_f = E_f(P)^{-1}$.
Then $B_f(V) = E_f(V)M_f$ and $A_f = E_f(Q)M_f$.

## The matrix path

**Lemma 1.** For a 2 by 2 matrix $A$ with $a_{11} + a_{22}$ and $a_{21} - a_{12}$ not both zero, let $\gamma = \operatorname{atan2}(a_{21} - a_{12}, a_{11} + a_{22})$ and $S = R(\gamma)^{\mathsf T}A$. Then $S$ is symmetric and $A = R(\gamma)S$. If $\det A > 0$, $S$ is positive definite.

*Proof.*
With $c = \cos\gamma$ and $s = \sin\gamma$, the off-diagonal entries of $S = R(\gamma)^{\mathsf T}A$ are $s_{12} = c\,a_{12} + s\,a_{22}$ and $s_{21} = -s\,a_{11} + c\,a_{21}$.
Their difference is $s_{21} - s_{12} = c(a_{21} - a_{12}) - s(a_{11} + a_{22})$, which is 0 because $(c, s)$ is parallel to $(a_{11} + a_{22}, a_{21} - a_{12})$.
So $S$ is symmetric, and $R(\gamma)S = A$ since $R(\gamma)$ is orthogonal.
The trace of $S$ is $c(a_{11} + a_{22}) + s(a_{21} - a_{12}) = \sqrt{(a_{11} + a_{22})^2 + (a_{21} - a_{12})^2} > 0$ and $\det S = \det A$.
A symmetric 2 by 2 matrix with a positive trace and a positive determinant has two positive eigenvalues. $\square$

The implementation uses this closed form (the function `polar` of the helper file for 2 by 2 matrices) and then sets the off-diagonal entries of $S$ to their mean, which changes them only by roundoff.

**Lemma 2.** $A_f(0) = I$, $A_f(1) = A_f$, and if $\det A_f > 0$ then $\det A_f(t) > 0$ for all $t \in [0, 1]$. Adding $2\pi k$ to $\gamma_f$ changes $A_f(t)$ for $0 < t < 1$ but not $A_f(1)$.

*Proof.*
$A_f(0) = R(0)I = I$ and $A_f(1) = R(\gamma_f)S_f = A_f$ by Lemma 1.
By Lemma 1, $S_f$ is positive definite, so $(1 - t)I + tS_f$ is positive definite as a convex combination of positive definite matrices, and $\det A_f(t) = \det((1 - t)I + tS_f) > 0$.
$R(\gamma_f + 2\pi k) = R(\gamma_f)$, but $R(t(\gamma_f + 2\pi k)) = R(t\gamma_f)R(2\pi kt)$, which differs for $kt$ not an integer. $\square$

**Lemma 3.** After line L4, the angles of two triangles $f$ and $g$ are within $\pi$ of each other whenever $g$ was first reached from $f$ in the walk.

*Proof.*
When $g$ is first reached from $f$, the walk adds $2\pi k$ with $k = \operatorname{round}((\gamma_f - \gamma_g)/(2\pi))$, so the new difference $\gamma_f - \gamma_g - 2\pi k$ is at most $\pi$ in absolute value.
The angle of $f$ is not changed again, because $f$ was reached before. $\square$

The walk is a breadth-first search, so the pairs of Lemma 3 are the edges of a spanning tree of each connected part of the dual graph.
Other neighbouring pairs are not checked; for meshes whose triangles turn by similar angles they are close as well.

## The least squares problem

**Lemma 4.** The energy $E(V) = \sum_f \lVert B_f(V) - A_f(t)\rVert_F^2$ is the sum of a function of the $x$ coordinates and a function of the $y$ coordinates of $V$, and both have the same quadratic part $z^{\mathsf T}Hz$, which does not depend on $t$.

*Proof.*
Row $r$ of $B_f(V) = E_f(V)M_f$ is row $r$ of $E_f(V)$ times $M_f$, and row $r$ of $E_f(V)$ contains only the coordinate $r$ of the vertices.
So entry $(r, c)$ of $B_f(V)$ is $a_{f,c}\cdot z_r$, where $z_r$ is the vector of coordinate $r$ of all vertices and $a_{f,c}$ has the entries $-(M_f)_{1c} - (M_f)_{2c}$, $(M_f)_{1c}$ and $(M_f)_{2c}$ at $i$, $j$ and $k$.
The energy is $\sum_r\sum_{f,c}(a_{f,c}\cdot z_r - A_f(t)_{rc})^2$, whose quadratic part in $z_r$ is $z_r^{\mathsf T}Hz_r$ with $H = \sum_{f,c}a_{f,c}a_{f,c}^{\mathsf T}$, the same for both $r$ and free of $t$. $\square$

**Lemma 5.** If the triangulation is connected through shared edges and every vertex is in some triangle, the matrix $H'$ obtained from $H$ by removing the row and the column of vertex 1 is positive definite.

*Proof.*
By the proof of Lemma 4, $z^{\mathsf T}Hz = \sum_f\lVert e_f(z)M_f\rVert^2$, where $e_f(z) = (z_j - z_i, z_k - z_i)$ is a row vector.
Each term is at least 0, so $H$ is positive semidefinite.
If $z^{\mathsf T}Hz = 0$, then $e_f(z)M_f = 0$ for every $f$, and since $M_f$ is invertible, $z_i = z_j = z_k$ on every triangle.
Triangles that share an edge share two vertices, so by connectedness $z$ is constant on all vertices.
If also $z_1 = 0$, then $z = 0$.
So the quadratic form of $H'$, which is $z^{\mathsf T}Hz$ restricted to $z_1 = 0$, is positive for $z \ne 0$. $\square$

**Theorem 1.** For each $t$, with $v_1(t)$ fixed, $E$ has exactly one minimizer, and line L8 computes it.

*Proof.*
With $z_1$ fixed, each coordinate part of the energy is a quadratic function of the free coordinates whose quadratic part is given by the positive definite $H'$ (Lemmas 4 and 5).
Such a function is strictly convex and has exactly one minimizer, the solution of its normal equations $H'z' = b' - h_1z_1$, where $b$ collects $\sum_{f,c}A_f(t)_{rc}a_{f,c}$ and $h_1$ is the column of $H$ for vertex 1 without its first entry.
This is the system of line L8. $\square$

## The ends and rigid motions

**Theorem 2.** $V(0) = P$ and $V(1) = Q$.

*Proof.*
At $t = 0$, $A_f(0) = I$ by Lemma 2, and $B_f(P) = E_f(P)M_f = I$, so $E(P) = 0$, and $P$ has $v_1 = p_1 = v_1(0)$.
A point with the energy 0 is a minimizer, and by Theorem 1 it is the only one, so $V(0) = P$.
At $t = 1$, $A_f(1) = A_f = E_f(Q)M_f = B_f(Q)$, so $E(Q) = 0$ with $v_1 = q_1 = v_1(1)$, and $V(1) = Q$. $\square$

**Theorem 3.** If $q_i = R(\theta)p_i + c$ for all $i$, with $-\pi < \theta < \pi$, then $V(t)$ is the source turned by $t\theta$ about $p_1$ and moved so that $p_1$ goes to $v_1(t)$: $v_i(t) = v_1(t) + R(t\theta)(p_i - p_1)$.

*Proof.*
$E_f(Q) = R(\theta)E_f(P)$, so $A_f = R(\theta)$.
By Lemma 1, $\gamma_f = \operatorname{atan2}(2\sin\theta, 2\cos\theta) = \theta$ and $S_f = I$.
All angles are equal, so line L4 changes none of them, and $A_f(t) = R(t\theta)$.
The shape $W$ with $w_i = v_1(t) + R(t\theta)(p_i - p_1)$ has $E_f(W) = R(t\theta)E_f(P)$, so $B_f(W) = R(t\theta) = A_f(t)$ and $E(W) = 0$, with $w_1 = v_1(t)$.
By Theorem 1, $V(t) = W$. $\square$

**Remark.** $B_f$ does not change when all vertices move by the same vector, so the minimizers of $E$ without a fixed vertex are the translates of one shape, by Lemma 5. Fixing a different vertex picks a different translate, so the shapes for two choices of the fixed vertex differ at each time by a translation.
