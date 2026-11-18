---
title: Deformation transfer has one solution, keeps the rest shape, copies a similarity exactly and gives back the source under self transfer
proves: [correctness]
status: full
---

We use the notation of the page.
The target mesh is connected, no triangle is degenerate, every target triangle is in at least one pair, and vertex $f$ is fixed at $x_f$.
For a target triangle $T = (a, b, c)$ with the unknown points $x_a, x_b, x_c$ and the unknown fourth point $y_T$, write $\tilde U_T = [x_b - x_a,\ x_c - x_a,\ y_T - x_a]$.
The energy is $E = \sum_{(T, S)} \lVert \tilde U_T Q_T - S_S \rVert_F^2$ with $Q_T = U_T^{-1}$.
The arithmetic is exact.

## The rows of line L3 are the energy

Column $k$ of $\tilde U_T Q_T$ is $\sum_{r} Q_T[r][k]\, (\text{column } r \text{ of } \tilde U_T) = Q_T[0][k](x_b - x_a) + Q_T[1][k](x_c - x_a) + Q_T[2][k](y_T - x_a)$.
The square of the Frobenius norm is the sum over the columns $k$ of the squared lengths of the column differences, and the squared length is the sum over the three coordinates.
So $E = \lVert A X - B \rVert_F^2$, where $A$ has one row per pair and column $k$, with the coefficients of line L3, $X$ has one row per unknown point and one column per coordinate, and $B$ holds the columns of $S_S$.
Moving the known point $x_f$ to the right side, as in line L4, does not change the value of $E$.

## One solution

**Lemma 1.** With vertex $f$ removed, $A$ has full column rank.

*Proof.*
Let $A z = 0$ for one coordinate column $z$, with $z_f = 0$.
Then $\lVert A z \rVert^2 = \sum_{(T,S)} \lVert Z_T Q_T \rVert_F^2 = 0$, where $Z_T$ is the frame built from $z$ as $\tilde U_T$ is built from $x$, but in one coordinate, so it is a row vector.
Since $Q_T$ is invertible, $Z_T = 0$ for every triangle $T$ in a pair, which is every triangle.
So $z_b = z_a$, $z_c = z_a$ and $z_{4,T} = z_a$ in every triangle.
The mesh is connected, so all vertex values are equal, and they equal $z_f = 0$.
Then every fourth value is $0$ too, so $z = 0$. $\square$

**Theorem 1.** Line L5 has exactly one solution, and it is the unique minimizer of $E$ with $\tilde u_f = x_f$.

*Proof.*
By Lemma 1, $A^\top A$ is symmetric positive definite.
$E$ is a convex quadratic in $X$ with the Hessian $2 A^\top A$, so it is strictly convex, and its only stationary point is the solution of $A^\top A X = A^\top B$. $\square$

So in each of the cases below it is enough to show a point with $E = 0$ and $\tilde u_f = x_f$: since $E \ge 0$, that point is the minimizer, and by Theorem 1 it is the output.

## The rest shape and self transfer

**Theorem 2.** If $\tilde v = v$, the output is the target rest mesh.

*Proof.*
Every $S_S = V_S V_S^{-1} = I$.
Take $x = u$ and $y_T$ the rest fourth vertex of $T$, so $\tilde U_T = U_T$ and $\tilde U_T Q_T = I$.
Then $E = 0$, and $x_f = u_f$ by the choice of the fixed position. $\square$

**Theorem 3.** If the target is the source, the pairs are $(T, T)$, and $x_f = \tilde v_f$, the output is $\tilde v$.

*Proof.*
Take $x = \tilde v$ and $y_T$ the fourth vertex of the deformed source triangle.
Then $\tilde U_T = \tilde V_T$, so $\tilde U_T Q_T = \tilde V_T V_T^{-1} = S_T$, and $E = 0$. $\square$

## A similarity is copied exactly

**Lemma 2.** Let $g(x) = M x + c$ with $M = sR$, $R$ a rotation and $s > 0$.
Then the fourth vertex of $(g(v_1), g(v_2), g(v_3))$ is $g(v_4)$.

*Proof.*
For a rotation, $R a \times R b = R(a \times b)$, so $M a \times M b = s^2 R (a \times b)$.
With $n = (v_2 - v_1) \times (v_3 - v_1)$, the new cross product is $s^2 R n$, its length is $s^2 \lVert n \rVert$, and the square root of the length is $s \sqrt{\lVert n \rVert}$.
So the new fourth vertex is $g(v_1) + s^2 R n / (s \sqrt{\lVert n \rVert}) = M v_1 + c + M n / \sqrt{\lVert n \rVert} = g(v_4)$. $\square$

**Theorem 4.** If $\tilde v_i = g(v_i)$ for all $i$, and $x_f = g(u_f)$, the output is $g(u_i)$ for all $i$.

*Proof.*
By Lemma 2, $\tilde V_S = M V_S$, so every $S_S = M$.
Take $x_i = g(u_i)$ and $y_T = g(u_{4,T})$.
Then $\tilde U_T = M U_T$, because the translation $c$ cancels in the differences, so $\tilde U_T Q_T = M = S_S$ for every pair and $E = 0$. $\square$

For a general affine $M$, the cross product of $M a$ and $M b$ is $\det(M) M^{-\top}(a \times b)$, which in general is not parallel to $M (a \times b)$, for example for a shear.
So the deformed fourth vertex does not follow $g$, $S_S$ differs from $M$ in its third column, and the result is in general not $g(u)$.

## Duplicated pairs

If every pair appears twice, $E$ is multiplied by 2, and the minimizer does not change.

## The check value

For the shear of the page, $V_S = I$ and $S = \tilde V_S$ has the columns $(1,0,0)$, $(0.5,1,0)$ and $(0,0,1)$.
For the target, $U$ has the columns $(2,0,0)$, $(0,1,0)$ and $(0,0,\sqrt 2)$, and $S U$ has the columns $(2,0,0)$, $(0.5,1,0)$ and $(0,0,\sqrt 2)$.
With the first vertex fixed at the origin, the point $x = ((0,0,0), (2,0,0), (0.5,1,0))$ and $y = (0,0,\sqrt 2)$ gives $E = 0$, so it is the output.
