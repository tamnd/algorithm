---
title: The front forces of front tracking have zero sum and zero torque, and the transfer to the grid keeps both
proves: [correctness]
status: full
---

We use the notation of the page. The front is a closed polygon with points $X_1, \dots, X_M$, indices taken mod $M$, and $t_{k+1/2} = (X_{k+1} - X_k)/|X_{k+1} - X_k|$. Line L2 gives the force $F_k = \sigma(t_{k+1/2} - t_{k-1/2})$ on point $k$. The 1D kernel is Peskin's

$$\phi(r) = \begin{cases} \bigl(3 - 2|r| + \sqrt{1 + 4|r| - 4r^2}\bigr)/8, & |r| \le 1, \\ \bigl(5 - 2|r| - \sqrt{-7 + 12|r| - 4r^2}\bigr)/8, & 1 \le |r| \le 2, \\ 0, & |r| \ge 2, \end{cases}$$

and $\delta_h(x, y) = \phi(x/h)\phi(y/h)/h^2$. We claim, in exact arithmetic:

1. $\sum_kF_k = 0$ and $\sum_kX_k \times F_k = 0$, where $a \times b = a_xb_y - a_yb_x$.
2. For every real $r$, $\sum_j\phi(r - j) = 1$ and $\sum_j(r - j)\phi(r - j) = 0$, with $j$ over the integers.
3. If the kernel stencils of the front points do not wrap around the periodic box, the grid force $f = \sum_kF_k\delta_h(x - X_k)$ of line L3 has $\sum_{ij}f_{ij}h^2 = \sum_kF_k$ and $\sum_{ij}x_{ij} \times f_{ij}h^2 = \sum_kX_k \times F_k$. So surface tension gives the grid flow no net force and no net torque. Also, line L5 interpolates every linear velocity field exactly.
4. The splitting part of the regrid (line L7) does not change the polygon, so it keeps the enclosed area and the shape.

**Claim 1.** The sum telescopes: $\sum_k(t_{k+1/2} - t_{k-1/2}) = 0$ for a closed front. For the torque, reorder the sum by elements:

$$\sum_kX_k \times (t_{k+1/2} - t_{k-1/2}) = \sum_kX_k \times t_{k+1/2} - \sum_kX_{k+1} \times t_{k+1/2} = -\sum_k(X_{k+1} - X_k) \times t_{k+1/2}.$$

Each term is the cross product of the element with its own direction, which is $0$. The same argument shows that the force is that of a tension $\sigma$ pulling along each element on its two end points: each element pulls its end points toward each other with equal and opposite forces, so the forces are internal to the front.

**Claim 2.** Both sums are periodic in $r$ with period 1, so take $0 \le r < 1$. The only integers with $|r - j| < 2$ are $j = -1, 0, 1, 2$, at distances $1 + r$, $r$, $1 - r$ and $2 - r$. Put $s = \sqrt{1 + 4r - 4r^2}$. Expanding the expression under each square root gives $s^2$ in all four cases: for example, $-7 + 12(1 + r) - 4(1 + r)^2 = 1 + 4r - 4r^2$. So

$$8\phi(r) = 3 - 2r + s, \quad 8\phi(1 - r) = 1 + 2r + s, \quad 8\phi(1 + r) = 3 - 2r - s, \quad 8\phi(2 - r) = 1 + 2r - s.$$

These add up to 8, which is the first identity. For the second,

$$8\sum_j(r - j)\phi(r - j) = (1 + r)(3 - 2r - s) + r(3 - 2r + s) + (r - 1)(1 + 2r + s) + (r - 2)(1 + 2r - s).$$

The coefficient of $s$ is $-(1 + r) + r + (r - 1) - (r - 2) = 0$. The rest is $(-2r^2 + r + 3) + (3r - 2r^2) + (2r^2 - r - 1) + (2r^2 - 3r - 2) = 0$.

**Claim 3.** Write the 2D weight of grid point $(i, j)$ for front point $k$ as $w_{ij} = \phi(\xi_i)\phi(\eta_j)$, with $\xi_i = (x_i - X_{k,x})/h$ and $\eta_j = (y_j - X_{k,y})/h$. The cell centers are $h$ apart, so the $\xi_i$ are a shifted copy of the integers, and since $\phi$ is even, Claim 2 gives $\sum_{ij}w_{ij} = 1$, $\sum_{ij}x_iw_{ij} = X_{k,x}$ and $\sum_{ij}y_jw_{ij} = X_{k,y}$ (the first moment identity says that the weighted mean of the grid points is the front point). Then $\sum_{ij}f_{ij}h^2 = \sum_kF_k\sum_{ij}w_{ij} = \sum_kF_k$, and

$$\sum_{ij}x_{ij} \times f_{ij}h^2 = \sum_k\Bigl(\sum_{ij}w_{ij}x_{ij}\Bigr) \times F_k = \sum_kX_k \times F_k.$$

With Claim 1, both are zero. For interpolation, $U_k = \sum_{ij}w_{ij}u(x_{ij})$, and for $u(x) = a + Bx$ the same identities give $U_k = a + BX_k$. If a stencil wraps around the box, the coordinates $x_{ij}$ jump by 1 and the moment identities fail; the code assumes the front stays away from the boundary, or a velocity that is periodic.

**Claim 4.** A split element is replaced by points on the segment between its end points, so the polygon, as a set, is the same. The dropping step removes a point, which replaces two elements by one, and in general changes the area; the page measures this change. $\blacksquare$
