---
title: Three exact vanishing points of orthogonal directions give K and R, and a returned answer always fits the input
proves: [correctness]
status: full
---

We use the notation of the page. The camera has zero skew and square pixels, so $K = \begin{pmatrix} f & 0 & c_x \\ 0 & f & c_y \\ 0 & 0 & 1 \end{pmatrix}$ with $f > 0$ and $c = (c_x, c_y)$. The rotation $R = [r_1 \; r_2 \; r_3]$ holds the three orthogonal scene directions in the camera frame, and $r_{iz}$ is the $Z$ component of $r_i$. The vanishing point of direction $i$ is $v_i \sim K r_i$. It is a finite pixel exactly when $r_{iz} \ne 0$, and then
$$v_i - c = \frac{f}{r_{iz}} (r_{ix}, r_{iy}), \qquad K^{-1} \begin{pmatrix} v_i \\ 1 \end{pmatrix} = \frac{r_i}{r_{iz}}.$$
For a point $p$ of the image we write $a_i(p) = v_i - p$, and $a_i = a_i(c)$.

**Claim.** (a) Let $v_1, v_2, v_3$ be the exact vanishing points of a camera as above, all finite. Then the points are not on one line, the triangle $v_1 v_2 v_3$ has three acute angles, and lines L1 to L10 return the true $K$ and a rotation whose columns are $\pm r_i$. (b) In exact arithmetic, for any three input points that lines L3 and L5 accept, the returned $R$ is a rotation and $K R e_i \sim (v_i, 1)$ for $i = 1, 2, 3$. So every accepted input is the exact set of vanishing points of some camera with zero skew and square pixels. (c) If line L3 or line L5 rejects the input, then no camera with zero skew and square pixels has these three points as finite vanishing points of three orthogonal directions.

## Step 1: the key identity

Let $i \ne j$. The directions are orthogonal, so $r_i \cdot r_j = 0$. Divide by $r_{iz} r_{jz}$ and use the formula for $K^{-1} (v_i, 1)$:
$$0 = \frac{r_i}{r_{iz}} \cdot \frac{r_j}{r_{jz}} = \frac{a_i}{f} \cdot \frac{a_j}{f} + 1, \qquad\text{so}\qquad a_i \cdot a_j = (v_i - c) \cdot (v_j - c) = -f^2. \tag{1}$$

## Step 2: the points are not collinear and the triangle is acute

The vectors $(v_i, 1) \sim K r_i$ are images of three independent vectors under the invertible $K$, so they are independent. If $v_1, v_2, v_3$ were on one line $l$, then $l^{\mathsf T} (v_i, 1) = 0$ for all three, and three independent vectors cannot all be orthogonal to one nonzero vector $l$ in $\mathbb R^3$. So the points are not collinear, and the vectors $v_1 - v_2$ and $v_2 - v_3$ are independent. The determinant $D$ of line L3 is not zero.

For the angle at $v_i$, with $\{i, j, k\} = \{1, 2, 3\}$, (1) gives
$$(v_j - v_i) \cdot (v_k - v_i) = (a_j - a_i) \cdot (a_k - a_i) = a_j \cdot a_k - a_j \cdot a_i - a_i \cdot a_k + a_i \cdot a_i = f^2 + \lVert a_i \rVert^2 > 0.$$
So every angle of the triangle is acute.

## Step 3: lines L1 to L6 return c and f

Lines L1 and L2 set $a^{(1)} = v_1 - v_2$, $b_1 = a^{(1)} \cdot v_3$, $a^{(2)} = v_2 - v_3$ and $b_2 = a^{(2)} \cdot v_1$. Line L4 solves the $2 \times 2$ system
$$a^{(1)} \cdot p = b_1, \qquad a^{(2)} \cdot p = b_2 \tag{2}$$
by Cramer's rule. The first equation says $(v_1 - v_2) \cdot (p - v_3) = 0$, so $p$ is on the altitude from $v_3$; the second says $p$ is on the altitude from $v_1$. By Step 2, $D \ne 0$, so (2) has exactly one solution, the orthocenter. The true $c$ solves (2), because by (1)
$$(v_1 - v_2) \cdot (v_3 - c) = a_1 \cdot a_3 - a_2 \cdot a_3 = -f^2 + f^2 = 0,$$
and in the same way $(v_2 - v_3) \cdot (v_1 - c) = a_2 \cdot a_1 - a_3 \cdot a_1 = 0$. So line L4 returns $c$. Line L5 computes $q = -a_1 \cdot a_2 = f^2 > 0$ by (1), so it does not reject, and line L6 sets the true $f$ and $K$.

## Step 4: lines L7 to L10 return a rotation with columns plus or minus r_i

Line L7 computes $d_i = ((v_i - c) / f, 1) = K^{-1} (v_i, 1) = r_i / r_{iz}$ and divides it by its length. As $\lVert r_i \rVert = 1$, the result is $\sigma_i r_i$ with $\sigma_i = \operatorname{sign}(r_{iz}) \in \{1, -1\}$. Line L8 forms $S = R \operatorname{diag}(\sigma_1, \sigma_2, \sigma_3)$, with $\det S = \sigma_1 \sigma_2 \sigma_3$. If this is $-1$, line L8 negates the third column, so the matrix becomes $R \operatorname{diag}(\sigma_1, \sigma_2, \sigma_1 \sigma_2)$, whose determinant is $+1$. In both cases the matrix is a rotation with columns $\pm r_i$. Line L9 runs the iteration $X \leftarrow (X + X^{-\mathsf T}) / 2$. For a rotation $X^{-\mathsf T} = X$, so the iteration does not change it. This proves (a).

## Step 5: a returned answer fits the input (part b)

Take any three input points for which lines L3 and L5 do not reject. Let $p = (p_x, p_y)$ be the solution of (2) and write $a_i = v_i - p$. The first equation of (2) says $(a_1 - a_2) \cdot a_3 = 0$, so $a_1 \cdot a_3 = a_2 \cdot a_3$. The second says $(a_2 - a_3) \cdot a_1 = 0$, so $a_1 \cdot a_2 = a_1 \cdot a_3$. So all three products $a_i \cdot a_j$ with $i \ne j$ have the same value, and line L5 sets $q$ to minus this value, with $q > 0$. With $f = \sqrt q$ and $d_i = (a_i / f, 1)$,
$$d_i \cdot d_j = \frac{a_i \cdot a_j}{q} + 1 = -1 + 1 = 0 \qquad (i \ne j).$$
So the unit vectors of line L7 are orthonormal, the matrix of line L8 is a rotation after the sign fix, and line L9 keeps it (Step 4). Each column is $\pm d_i / \lVert d_i \rVert$, and $K d_i = (v_i, 1)$ by the definition of $d_i$, so $K R e_i \sim (v_i, 1)$. With rounding, the columns are only nearly orthonormal, and line L9 replaces the matrix with its orthogonal polar factor, the nearest rotation in the Frobenius norm (the determinant is positive after line L8).

## Step 6: rejections are correct (part c)

Suppose some camera with zero skew and square pixels had $v_1, v_2, v_3$ as finite vanishing points of three orthogonal directions. Then Step 2 shows that the points are not collinear, so line L3 does not reject. Step 3 shows that the unique solution of (2) is its principal point and that $q = f^2 > 0$ there, so line L5 does not reject either. Hence a rejection at line L3 or line L5 proves that no such camera exists. In particular, three collinear points, or a triangle with a right or an obtuse angle, are rejected. For a right or obtuse angle at $v_i$, the identity of Step 2 holds at the orthocenter $p$ for any triangle (its proof used only that the three products $a_i \cdot a_j$ are equal, which Step 5 shows), so $(v_j - v_i) \cdot (v_k - v_i) = q + \lVert v_i - p \rVert^2 \le 0$ forces $q \le 0$.

## Cost

Each line does a fixed number of arithmetic operations on numbers of the real-RAM, except line L9, which runs at most a fixed number (60) of iterations of fixed cost on a $3 \times 3$ matrix. So the method takes $\Theta(1)$ time and $\Theta(1)$ extra space.
