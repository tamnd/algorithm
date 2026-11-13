---
title: HARRIS computes det M minus k times the squared trace from the windowed gradient products, its sign separates edges from corners, and it returns the strict local maxima above the threshold
proves: [correctness]
status: full
---

Let $c_W(x) = \min(\max(x, 0), W - 1)$ and $c_H(y) = \min(\max(y, 0), H - 1)$ be the clamp maps. The window has weights $w_{-r}, \ldots, w_r \ge 0$ with $w_{-i} = w_i$, not all zero. For a table $P$ define the windowed sum

$$(w \ast P)(x, y) = \sum_{j=-r}^{r} \sum_{i=-r}^{r} w_i w_j \, P(c_W(x + i), c_H(y + j)).$$

**Lemma 1 (separable sum).** Line L3, done as a pass over the rows and then a pass over the columns, each with the clamp rule, computes $w \ast P$.

*Proof.* The row pass gives $T(x, y) = \sum_i w_i P(c_W(x + i), y)$ for each $y$. The column pass gives $\sum_j w_j T(x, c_H(y + j)) = \sum_j w_j \sum_i w_i P(c_W(x + i), c_H(y + j))$, which is the double sum. $\square$

So after line L3, $A = w \ast X^2$, $B = w \ast Y^2$ and $C = w \ast (XY)$ at every pixel, and line L5 sets $R = AB - C^2 - k(A + B)^2$.

**Lemma 2 (eigenvalues).** At each pixel $M = \begin{pmatrix} A & C \\ C & B \end{pmatrix}$ is symmetric and positive semidefinite, with eigenvalues $\lambda_1 \ge \lambda_2 \ge 0$, and $R = \lambda_1\lambda_2 - k(\lambda_1 + \lambda_2)^2$.

*Proof.* Let $g_{ij} = (X, Y)$ at the pixel $(c_W(x + i), c_H(y + j))$. Then $M = \sum_{i,j} w_i w_j \, g_{ij} g_{ij}^{\mathsf T}$, and for any vector $v$, $v^{\mathsf T} M v = \sum w_i w_j (g_{ij} \cdot v)^2 \ge 0$. A real symmetric matrix has real eigenvalues, and these are $\ge 0$ by the bound. The determinant $AB - C^2$ is the product of the eigenvalues and the trace $A + B$ is their sum. $\square$

**Lemma 3 (sign of the response).** Let $0 < k < 1/4$ and $\lambda_1 > 0$, and put $t = \lambda_2/\lambda_1 \in [0, 1]$ and $t_0 = \frac{(1 - 2k) - \sqrt{1 - 4k}}{2k}$. Then $0 < t_0 < 1$, and $R > 0$ exactly when $t > t_0$. In particular $R = -k\lambda_1^2 < 0$ when $\lambda_2 = 0$, and $R = (1 - 4k)\lambda^2 > 0$ when $\lambda_1 = \lambda_2 = \lambda > 0$. If $\lambda_1 = 0$, then $M = 0$ and $R = 0$.

*Proof.* $R / \lambda_1^2 = t - k(1 + t)^2 = -(k t^2 + (2k - 1)t + k) = -q(t)$. The quadratic $q$ has discriminant $(1 - 2k)^2 - 4k^2 = 1 - 4k > 0$ and two positive roots $t_0$ and $t_1 = 1/t_0$, whose product is $k/k = 1$. Since $q(1) = 4k - 1 < 0$, the point $1$ lies strictly between the roots, so $t_0 < 1 < t_1$. Since $q(0) = k > 0$, also $t_0 > 0$. On $[0, 1]$ the sign of $q$ is positive before $t_0$, zero at $t_0$ and negative after it, so $R > 0$ exactly when $t > t_0$. The two special cases follow by putting $t = 0$ and $t = 1$. If $\lambda_1 = 0$, then both eigenvalues are $0$ and the symmetric matrix $M$ is $0$. $\square$

**Lemma 4 (selection).** Lines L6 to L10 return the set of pixels $(x, y)$ with $R(x, y) > \tau$ and $R(x, y) > R(x', y')$ for each of the up to 8 pixels $(x', y') \ne (x, y)$ of the image with $|x' - x| \le 1$ and $|y' - y| \le 1$.

*Proof.* Line L7 visits each pixel with $R > \tau$ once, and line L8 tests exactly the stated neighbours. Line L9 adds the pixel when the test holds, and no other line adds or removes elements. $\square$

**Theorem.** HARRIS returns the strict local maxima above $\tau$ of $R = \det M - k(\operatorname{tr} M)^2$, where $M$ is the windowed structure tensor of the clamped central differences, and $R = \lambda_1 \lambda_2 - k(\lambda_1 + \lambda_2)^2$. For $0 < k < 1/4$ and $\tau \ge 0$, no returned pixel has $\lambda_2 \le t_0 \lambda_1$; in particular no returned pixel is a pure edge pixel with $\lambda_2 = 0$, and no pixel with $M = 0$ is returned.

*Proof.* Lemma 1 and line L5 give the formula for $R$, Lemma 2 gives its eigenvalue form, and Lemma 4 gives the output set. A returned pixel has $R > \tau \ge 0$, so by Lemma 3 it has $\lambda_1 > 0$ and $\lambda_2 > t_0 \lambda_1$. $\square$

**Invariances.** Each follows from the formulas above.

- *Offset.* For $I' = I + b$, line L1 gives the same $X$ and $Y$, since the constant cancels in each difference. So $R' = R$ and the output is the same.
- *Gain.* For $I' = cI$, $X' = cX$ and $Y' = cY$, so $A$, $B$ and $C$ gain $c^2$ and $R' = c^4 R$. For $c \ne 0$ and $\tau = 0$ the sign of $R$ and the order of the values are kept, so the output is the same.
- *Transpose.* Let $I'(x, y) = I(y, x)$ on the transposed grid. Then $X'(x, y) = I(y, c(x + 1)) - I(y, c(x - 1)) = Y(y, x)$ and $Y'(x, y) = X(y, x)$, where the clamp maps match because the grid is transposed too. The window weights $w_i w_j$ are symmetric in $i$ and $j$, so $A'(x, y) = B(y, x)$, $B'(x, y) = A(y, x)$ and $C'(x, y) = C(y, x)$. $R$ is symmetric in $A$ and $B$, so $R'(x, y) = R(y, x)$.
- *Mirror.* Let $I'(x, y) = I(W - 1 - x, y)$. The clamp map commutes with $x \mapsto W - 1 - x$, so $X'(x, y) = -X(W - 1 - x, y)$ and $Y'(x, y) = Y(W - 1 - x, y)$. Since $w_{-i} = w_i$, $A$ and $B$ are carried over and $C$ changes sign, and $C^2$ does not change. So $R'(x, y) = R(W - 1 - x, y)$.
- *Rotation by $90°$.* A rotation by $90°$ of the grid is a transpose followed by a mirror. Both maps carry the response to the response, and both map the 8-neighbourhood of a pixel inside the image to the 8-neighbourhood of its image. So the corners of the rotated image are the rotated corners.
