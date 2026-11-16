---
title: Correctness of calibrated stereo rectification
proves: [correctness]
status: full
---

We prove that the homographies of lines L1 to L8 rectify the pair: a point seen by both cameras has the same row in both new images, and its disparity is $f_x b / Z$. We use the conventions of the page: $X_i = R_i X + t_i$, $P_i = K_i [R_i \mid t_i]$, $C_i = -R_i^{\mathsf T} t_i$, and $\sim$ means equal up to a nonzero scale.

## Lemma 1. $R_n$ is a rotation and $R_n (C_2 - C_1) = (b, 0, 0)^{\mathsf T}$

Line L2 fails if $b = 0$, so $b > 0$ after it, and $r_1 = (C_2 - C_1)/b$ is a unit vector. Line L4 fails if $y = z_1 \times r_1 = 0$. Otherwise $y$ is perpendicular to $r_1$, and $r_2 = y / \lVert y \rVert$ is a unit vector perpendicular to $r_1$. Then $r_3 = r_1 \times r_2$ is a unit vector perpendicular to both, and $(r_1, r_2, r_3)$ is a right-handed orthonormal basis. The matrix $R_n$ with these rows satisfies $R_n R_n^{\mathsf T} = I$ and $\det R_n = r_1 \cdot (r_2 \times r_3) = r_1 \cdot r_1 = 1$, so it is a rotation. Its rows are orthonormal and $C_2 - C_1 = b r_1$, so $R_n (C_2 - C_1) = (b\, r_1 \cdot r_1, b\, r_2 \cdot r_1, b\, r_3 \cdot r_1) = (b, 0, 0)$. $\square$

The test of line L4 fails exactly when $z_1$ is parallel to $r_1$, that is, when the baseline lies along the optical axis of camera 1. In this case the epipole is the principal point and no rotation can move it to infinity, so the failure is not a defect of the method.

## Lemma 2. $H_i x_i \sim P'_i X$ for every point $X$ with $x_i \sim P_i X$

Let $X$ be a point and $x_i \sim P_i X = K_i (R_i X + t_i)$. Since $t_i = -R_i C_i$, this is $x_i \sim K_i R_i (X - C_i)$. The matrix $K_i$ is invertible because $f_x f_y \ne 0$, so

$$H_i x_i = K_n R_n R_i^{\mathsf T} K_i^{-1} x_i \sim K_n R_n R_i^{\mathsf T} R_i (X - C_i) = K_n R_n (X - C_i) = P'_i X ,$$

with $P'_i = K_n R_n [I \mid -C_i]$. The scale factor is the same nonzero number on both sides, so the two homogeneous vectors give the same pixel. $\square$

Lemma 2 does not use the depth of $X$. That is why one homography per image serves every point of the scene: a change of rotation about a fixed center maps rays to rays.

## Lemma 3. An upper triangular $K_n$ maps $e_X$ to a multiple of itself

Write $K_n = [[f_x, s, c_x], [0, f_y, c_y], [0, 0, 1]]$ and $e_X = (1, 0, 0)^{\mathsf T}$. Then $K_n e_X$ is the first column, $(f_x, 0, 0)^{\mathsf T} = f_x e_X$. $\square$

## Theorem. Equal rows and $d = f_x b / Z$

Let $X$ be a point and $Y = R_n (X - C_1) = (Y_x, Y_y, Z)$ its coordinates in the new frame of camera 1, with $Z \ne 0$. By Lemma 2 and Lemma 1,

$$H_1 x_1 \sim K_n Y, \qquad H_2 x_2 \sim K_n R_n (X - C_1 - (C_2 - C_1)) = K_n (Y - b e_X) = K_n Y - b f_x e_X ,$$

where the last step is Lemma 3. The vector $b f_x e_X$ has zero second and third entries. So $K_n Y$ and $K_n (Y - b e_X)$ have the same third entry $Z$ and the same second entry $f_y Y_y + c_y Z$, and their first entries differ by $b f_x$. Divide both by $Z$: the rows are $v_1 = v_2 = f_y Y_y / Z + c_y$, and the columns satisfy $u_1 - u_2 = f_x b / Z$. For a point in front of the new camera 1, $Z > 0$ and $d > 0$. $\square$

The proof uses only one $K_n$ for both images. If camera 2 used $c'_x$ instead of $c_x$, its first entry would change by $(c'_x - c_x) Z$, and $d$ would change by the constant $c_x - c'_x$. A different $f_y$ or $c_y$ would break the equality of rows.

## Corollary. The fundamental matrix of the new pair

The new cameras are $K_n [I \mid 0]$ and $K_n [I \mid t]$ in the new frame of camera 1, with $t = -b e_X$. The fundamental matrix of $x_2^{\mathsf T} F x_1 = 0$ is then $F' = K_n^{-\mathsf T} [t]_\times K_n^{-1}$, as on the page of the [fundamental matrix](/fundamental-matrix/). For any invertible $M$ and vector $a$, $M^{\mathsf T} [M a]_\times M = \det(M) [a]_\times$. Put $M = K_n$ and $a = e_X$. Lemma 3 gives $[K_n e_X]_\times = f_x [e_X]_\times$, so $f_x K_n^{\mathsf T} [e_X]_\times K_n = \det(K_n) [e_X]_\times$, which gives $K_n^{-\mathsf T} [e_X]_\times K_n^{-1} = (f_x / \det K_n) [e_X]_\times$. Hence

$$F' = -\frac{b f_x}{\det K_n} [e_X]_\times = -\frac{b}{f_y} \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 1 & 0 \end{pmatrix},$$

and $x_2^{\mathsf T} F' x_1 = -(b / f_y)(v_1 - v_2)$, which is zero exactly when the rows are equal. $\square$

## The warp

Lines L9 to L13 compute $J(x') = I(H^{-1} x')$ for each output pixel $x'$. By Lemma 2, the pixel $x'$ of the new image and the pixel $H^{-1} x'$ of the old image see the same ray, so $J$ is the image that the new camera would record, up to the error of the interpolation and the pixels whose source is outside $I$, which get the fill value. Every output pixel is visited once, so the result has no holes. $\square$
