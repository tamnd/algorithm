---
title: The cofactor rule gives the normals of Barr's deformations, and the taper, twist and bend have the stated Jacobians
proves: [correctness]
status: full
---

We use the notation of the page.
A surface through $p$ has the tangent vectors $a$ and $b$, and its normal is a positive multiple of $a \times b$.
A smooth map $F$ sends the tangent vectors to $J_F(p)a$ and $J_F(p)b$, the tangent vectors of the moved surface at $F(p)$.

## The chain

**Lemma 1.** After line L3 and line L4 have run for the operations $F_1, \dots, F_i$, $J$ is the Jacobian of $F_i \circ \dots \circ F_1$ at the original point $p_0$, and $p = F_i(\cdots F_1(p_0))$.

*Proof.*
By induction on $i$.
For $i = 0$, $J = I$ and $p = p_0$.
Line L3 multiplies by $J_{F_{i+1}}$ at the current $p = F_i(\cdots F_1(p_0))$, which is the chain rule $D(F_{i+1} \circ G)(p_0) = DF_{i+1}(G(p_0))\,DG(p_0)$; then line L4 moves $p$. $\square$

## The cofactor rule

**Lemma 2.** For every 3 by 3 matrix $J$ and all vectors $a$, $b$: $(Ja) \times (Jb) = \operatorname{cof}(J)(a \times b)$. If $J$ is invertible, $\operatorname{cof}(J) = \det(J)J^{-\mathsf T}$.

*Proof.*
For any vector $c$, $c \cdot ((Ja) \times (Jb)) = \det[c, Ja, Jb]$.
Write $c = Jd$ when $J$ is invertible: then $\det[Jd, Ja, Jb] = \det(J)\det[d, a, b] = \det(J)\,d \cdot (a \times b) = \det(J)\,(J^{-1}c) \cdot (a \times b) = c \cdot \det(J)J^{-\mathsf T}(a \times b)$.
This holds for every $c$, so $(Ja) \times (Jb) = \det(J)J^{-\mathsf T}(a \times b)$.
The adjugate formula $J^{-1} = \operatorname{adj}(J)/\det J$ with $\operatorname{adj}(J) = \operatorname{cof}(J)^{\mathsf T}$ gives $\det(J)J^{-\mathsf T} = \operatorname{cof}(J)$.
Both sides of the identity are polynomials in the entries of $J$, and invertible matrices are dense, so it holds for every $J$. $\square$

**Theorem 1.** Line L6 returns a unit normal of the moved surface at the moved point, on the side of $(Ja) \times (Jb)$, whenever $\operatorname{cof}(J)n \ne 0$.

*Proof.*
$n = \lambda(a \times b)$ with $\lambda > 0$, so by Lemma 1 and Lemma 2, $m = \lambda(Ja) \times (Jb)$, which is perpendicular to both moved tangent vectors and on the side of their cross product. $\square$

If $\det J < 0$, $J^{-\mathsf T}n$ is $-m/|\det J|$ and points to the other side; this is the orientation pitfall of the page.

## The three Jacobians

**Taper.** $F = (rx, ry, z)$ with $r = r(z)$. The partial derivatives give the rows $(r, 0, r'x)$, $(0, r, r'y)$ and $(0, 0, 1)$. The matrix is upper triangular, so $\det J = r^2$.

**Twist.** $F = (x\cos\theta - y\sin\theta, x\sin\theta + y\cos\theta, z)$ with $\theta = \theta(z)$. The derivatives by $x$ and $y$ give the rotation block $\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$, the derivative by $z$ gives the third column $\theta'(-x\sin\theta - y\cos\theta,\; x\cos\theta - y\sin\theta,\; 1)$, and the third row is $(0, 0, 1)$. Expanding along the third row gives $\det J = \cos^2\theta + \sin^2\theta = 1$.

**Bend inside the region.** Here $\hat y = y$, so $\theta = k(y - y_0)$ and $d\theta/dy = k$. With $Y = -S(z - 1/k) + y_0$ and $Z = C(z - 1/k) + 1/k$:
$\partial Y/\partial y = -Ck(z - 1/k) = C(1 - kz)$, $\partial Y/\partial z = -S$, $\partial Z/\partial y = -Sk(z - 1/k) = S(1 - kz)$, $\partial Z/\partial z = C$, and $X = x$.
The determinant is $C^2(1 - kz) + S^2(1 - kz) = 1 - kz$.

**Bend outside the region.** Here $\hat y$ is constant, so $\theta$ is constant, and $Y$, $Z$ gain the terms $C(y - \hat y)$ and $S(y - \hat y)$. Then $\partial Y/\partial y = C$, $\partial Z/\partial y = S$, $\partial Y/\partial z = -S$, $\partial Z/\partial z = C$: a rotation block, with the determinant 1.

## The bend at the ends of the region

**Theorem 2.** The bend is continuous at $y = y_{\max}$ and at $y = y_{\min}$. Its Jacobian is continuous there only on the plane $z = 0$.

*Proof.*
At $y = y_{\max}$, both formulas use $\hat y = y_{\max}$, so they have the same $\theta$, and the outside terms $C(y - \hat y)$, $S(y - \hat y)$ are 0. So the two sides agree.
The $\partial/\partial y$ column is $(C(1 - kz), S(1 - kz))$ inside and $(C, S)$ outside, which agree only if $kz = 0$, that is $z = 0$ for $k \ne 0$.
The same holds at $y_{\min}$. $\square$

On the line $z = 0$ inside the region, $F = (x, S/k + y_0, (1 - C)/k)$, which is the circle of radius $1/k$ about $(y_0, 1/k)$, with the arc length $|y - y_0|$ from the center point: the axis bends without stretch.
