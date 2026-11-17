---
title: The discrete harmonic coordinates exist, are unique and nonnegative, sum to 1, and reproduce linear functions at the grid nodes
proves: [correctness]
status: full
---

We use the notation of the page.
For a node $p \in U$ and one axis, let the two arms along that axis have the lengths $\ell_-$ and $\ell_+$, at most $\delta$, and end at the points $q_-$ and $q_+$.
An end is either a node of $U$, with the unknown value there, or a point on the cage, with the value of the boundary data there.
The arm weights are $a_\pm = 2/(\ell_\pm(\ell_- + \ell_+))$, and the discrete Laplacian at $p$ is

$$(L u)(p) = \sum_{\text{both axes}} a_-(u(q_-) - u(p)) + a_+(u(q_+) - u(p)).$$

The system $Ax = b_i$ of lines L4 to L6 is $(Lu)(p) = 0$ for every $p \in U$, with the boundary data $\phi_i$, after the known boundary values are moved to the right side.
We assume that every arm whose neighbour node is not in $U$ ends at a crossing with the cage. The implementation has a fallback for rounding cases where the crossing is not found, and there the exactness claims hold only up to the rounding.

## Exactness on quadratics

**Lemma 1.** For every polynomial $g(t) = \alpha + \beta t + \gamma t^2$ and all $\ell_-, \ell_+ > 0$: $a_-(g(-\ell_-) - g(0)) + a_+(g(\ell_+) - g(0)) = 2\gamma = g''$.

*Proof.*
The left side is $a_-(-\beta\ell_- + \gamma\ell_-^2) + a_+(\beta\ell_+ + \gamma\ell_+^2) = \frac{2}{\ell_- + \ell_+}(-\beta + \gamma\ell_- + \beta + \gamma\ell_+) = 2\gamma$. $\square$

So if $g(x, y)$ is a polynomial whose restriction to each horizontal and each vertical line has degree at most 2, $Lg = \partial^2g/\partial x^2 + \partial^2g/\partial y^2$ exactly at every node. This holds for $1$, $x$, $y$, $xy$, $x^2$ and $y^2$.

## A discrete maximum principle

**Lemma 2.** Every connected set of nodes of $U$, where two nodes are joined when an arm of one ends at the other, contains a node with an arm that ends on the cage.

*Proof.*
Take the node $p$ of the set with the largest $x$, and among those the largest $y$. Its right arm cannot end at a node of $U$, because that node is joined to $p$ and has a larger $x$. So it ends on the cage. $\square$

**Lemma 3.** If $Lu = 0$ on $U$ with boundary data $\ge 0$, then $u \ge 0$ on $U$. If the boundary data are 0, then $u = 0$.

*Proof.*
Let $m = \min_U u$ and assume $m < 0$, with $m = u(p)$.
$(Lu)(p) = 0$ says that $u(p)$ is the weighted mean, with the positive weights $a$, of the values at the ends of its four arms.
Each end value is $\ge m$: a node value by the choice of $m$, a boundary value because it is $\ge 0 > m$.
So all end values equal $m$; in particular no arm of $p$ ends on the cage, and every neighbour node in $U$ also has the value $m$.
Repeating the argument, every node of the connected set of $p$ has the value $m$ and no arm on the cage, which Lemma 2 forbids.
So $u \ge 0$.
With the data 0, the same argument applied to $u$ and to $-u$ gives $u \ge 0$ and $u \le 0$. $\square$

**Theorem 1.** The matrix $A$ is nonsingular, so each $h_i$ exists and is unique, and $h_i \ge 0$ at every node.

*Proof.*
If $Ax = 0$, then $x$ solves $Lu = 0$ with the data 0, so $x = 0$ by Lemma 3. The data $\phi_i$ are $\ge 0$, so $h_i \ge 0$ by Lemma 3. $\square$

This is the M-matrix property: $A$ has a positive diagonal, nonpositive entries off it and $A^{-1} \ge 0$. It is also why the LU factorization without pivoting of line L5 is stable: the Schur complements of a nonsingular M-matrix are M-matrices, so every pivot is positive.

## Partition of unity and linear precision

**Lemma 4.** On the cage boundary, $\sum_i \phi_i = 1$ and $\sum_i \phi_i(q)c_i = q$.

*Proof.*
A point $q$ on the edge from $c_k$ to $c_{k+1}$ at the fraction $s$ has $\phi_k(q) = 1 - s$, $\phi_{k+1}(q) = s$ and $\phi_i(q) = 0$ otherwise. So the sum is 1, and $\sum_i \phi_i(q)c_i = (1 - s)c_k + sc_{k+1} = q$. $\square$

**Theorem 2.** At every node $p \in U$: $\sum_i h_i(p) = 1$ and $\sum_i h_i(p)c_i = p$.

*Proof.*
The system is linear in the data, so $u = \sum_i h_i$ solves $Lu = 0$ with the data $\sum_i \phi_i = 1$, and $v = \sum_i h_i c_{i,x}$ solves it with the data $\sum_i \phi_i c_{i,x}$, which is the $x$ coordinate of the boundary point by Lemma 4.
$L$ applied to the constant 1 or to the coordinate function $x$ gives 0 exactly, by Lemma 1, and these functions have the same boundary values.
By Theorem 1 the solution is unique, so $u = 1$ and $v = x$; the same holds for $y$. $\square$

**Theorem 3.** If the cage is an axis-aligned rectangle with the corners as its four vertices, the discrete $h_i$ at every node equal the bilinear coordinates of the rectangle.

*Proof.*
Each bilinear coordinate, such as $(1 - x/w)(1 - y/v)$ for the rectangle $[0, w] \times [0, v]$, is linear on each edge and equals 1 at its corner and 0 at the others, so it agrees with $\phi_i$ on the boundary.
On each horizontal or vertical line it is linear, so $L$ of it is 0 by Lemma 1.
By uniqueness it is the discrete solution. $\square$

## Evaluation between nodes

Line L8 interpolates the four corner nodes of the grid cell that holds $p$ with the bilinear weights, which are $\ge 0$ and sum to 1.
A corner outside $U$ takes $\phi(q^*)$ at its nearest boundary point $q^*$, which is $\ge 0$ and sums to 1 by Lemma 4.
So $\sum_i h_i(p) = 1$ and $h_i(p) \ge 0$ at every point.
If all four corners are in $U$, bilinear interpolation of the nodal values of a linear function gives that function, so $\sum_i h_i(p)c_i = p$.
If a corner $z$ is not in $U$, its value reproduces $q^*$ instead of $z$; the segment from $z$ to $p$ crosses the cage and has the length at most $\sqrt2\,\delta$, so $|q^* - z| \le \sqrt2\,\delta$, and $|\sum_i h_i(p)c_i - p| \le \sqrt2\,\delta$.

## The continuous coordinates

For the exact $h_i$ of the Laplace equation, the weak maximum principle gives $0 \le h_i \le 1$, and the strong maximum principle gives $0 < h_i < 1$ inside when $\phi_i$ is not constant, which holds for a cage with at least three vertices.
These are standard facts about harmonic functions and are not proved here.
