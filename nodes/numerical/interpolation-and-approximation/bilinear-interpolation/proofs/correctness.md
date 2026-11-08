---
title: Bilinear interpolation returns the unique continuous piecewise Q1 interpolant, and its error is at most (h_x^2/8) max|f_xx| + (h_y^2/8) max|f_yy|
proves: [correctness, termination, error-bound]
status: full
---

We use the notation of the page: increasing axes $x_0 < \cdots < x_m$ and $y_0 < \cdots < y_n$ with $m, n \ge 1$, table $f_{ij}$, and $Q_1 = \operatorname{span}\{1, x, y, xy\}$.

## Claim 1: termination and the cell

Lines L1 and L2 are binary searches over sorted arrays, which end after $O(\log m)$ and $O(\log n)$ comparisons; the clamps give $0 \le i \le m - 1$ and $0 \le j \le n - 1$. For $X \in [x_0, x_m)$ the index $i$ satisfies $x_i \le X < x_{i+1}$, and $X = x_m$ gives $i = m - 1$; similarly for $j$. The denominators in L3 and L4 are positive because the coordinates are distinct. Lines L3 to L7 are straight-line code.

## Claim 2: uniqueness of the Q1 interpolant on a rectangle

Let $q = c_0 + c_1 x + c_2 y + c_3 xy$ vanish at the four corners of $R = [x_i, x_{i+1}] \times [y_j, y_{j+1}]$. For fixed $y$, $q$ is affine in $x$. On the edge $y = y_j$ it vanishes at both ends, so it vanishes on the whole edge; likewise on $y = y_{j+1}$. For fixed $x$, $q$ is affine in $y$ and vanishes at $y_j$ and $y_{j+1}$, hence on the whole vertical segment. So $q = 0$ on $R$, and since a polynomial that vanishes on a set with interior is zero, $q = 0$. The linear map from $Q_1$ (dimension 4) to the four corner values is therefore injective, hence bijective: for any corner data there is exactly one interpolant in $Q_1$.

## Claim 3: lines L3 to L7 compute it

Let $u, v$ be as in L3 and L4; they are affine functions of $X$ and $Y$ with $u = 0, 1$ at $X = x_i, x_{i+1}$ and $v = 0, 1$ at $Y = y_j, y_{j+1}$. Expanding L5 to L7,
$$P = (1 - u)(1 - v) f_{i,j} + u(1 - v) f_{i+1,j} + (1 - u) v f_{i,j+1} + u v f_{i+1,j+1}.$$
Each product $(1 - u)(1 - v)$, $u(1 - v)$, $(1 - u)v$, $uv$ lies in $Q_1$ as a function of $(X, Y)$, because it is a product of an affine function of $X$ and an affine function of $Y$. At a corner exactly one of the four weights is 1 and the others are 0, so $P$ takes the corner value. By Claim 2, $P$ is the $Q_1$ interpolant on the cell. The same expansion with the roles of $u$ and $v$ exchanged shows that interpolating in $y$ first gives the same $P$.

## Claim 4: continuity across cells

On a vertical grid line $X = x_{i+1}$ shared by the cells with indices $i$ and $i + 1$ (and the same $j$), the left cell has $u = 1$ and the right cell has $u = 0$. Both give $(1 - v) f_{i+1,j} + v f_{i+1,j+1}$. On a horizontal line $Y = y_{j+1}$, both adjacent cells give $(1 - u) f_{i,j+1} + u f_{i+1,j+1}$. So the piecewise $Q_1$ function is continuous on the grid rectangle, and by Claims 2 and 3 it is the unique continuous function that is in $Q_1$ on every cell and matches the table.

## Claim 5: the error bound

Assume $f_{xx}$ and $f_{yy}$ exist and are continuous on the cell $R$ with sides $h_x$ and $h_y$. Define $(I_x g)(X, Y) = (1 - u) g(x_i, Y) + u\, g(x_{i+1}, Y)$ and $(I_y g)(X, Y) = (1 - v) g(X, y_j) + v\, g(X, y_{j+1})$. By Claim 3, $P = I_x I_y f$. Then
$$f - P = (f - I_x f) + I_x (f - I_y f).$$
For each fixed $Y$, $f - I_x f$ is the error of linear interpolation of $x \mapsto f(x, Y)$ at $x_i, x_{i+1}$, which equals $\frac12 f_{xx}(\xi, Y)(X - x_i)(X - x_{i+1})$ for some $\xi$ in the interval, and $|(X - x_i)(X - x_{i+1})| \le h_x^2/4$. So $|f - I_x f| \le \frac{h_x^2}{8} \max_R |f_{xx}|$. In the same way $|(f - I_y f)(x, Y)| \le \frac{h_y^2}{8} \max_R |f_{yy}|$ for $x = x_i$ and $x = x_{i+1}$. For $(X, Y) \in R$ we have $0 \le u \le 1$, so $I_x$ forms a convex combination of these two values, which is bounded by the same number. Adding the two bounds gives the claim.

For $f(x, y) = x^2$ and $X = (x_i + x_{i+1})/2$, the error is $h_x^2/4 = \frac{h_x^2}{8} \cdot 2$, so the constant $1/8$ is attained and cannot be lowered.

## Claim 6: maximum principle and exactness at nodes in floating point

For $(X, Y) \in R$ the four weights are nonnegative and sum to 1, so $P$ lies between the smallest and largest corner value. In floating point with round to nearest, if $X = x_i$ then $X - x_i = 0$ exactly and $u = 0$; if $X = x_{i+1}$ then the numerator and the denominator of L3 are the same rounded difference and $u = 1$ exactly. In both cases $1 - u \in \{0, 1\}$ exactly, so L5 and L6 return the exact edge values when the corner values are finite, and the same argument for $v$ shows that L7 returns $f_{ij}$ exactly at every grid point.
